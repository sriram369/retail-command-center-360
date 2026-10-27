"""Deterministic fictional retailer. No external accounts or data are accessed."""
from __future__ import annotations
from pathlib import Path
from collections import defaultdict
import json, hashlib
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
START = pd.Timestamp('2025-04-01')
CUTOFF = pd.Timestamp('2026-09-30')
SEED = 3602026
RISK_START = pd.Timestamp('2026-07-01')

def ds(d):
    return pd.Timestamp(d).strftime('%Y-%m-%d')

def generate():
    rng = np.random.default_rng(SEED)
    tables = {}
    def put(name, records):
        tables[name] = pd.DataFrame(records)
        return tables[name]
    dates = pd.date_range(START, CUTOFF)
    put('DimDate', [{'Date':ds(d),'Year':d.year,'MonthNumber':d.month,
        'Month':d.strftime('%Y-%m'),'MonthStart':ds(d.replace(day=1)),
        'Quarter':f'{d.year} Q{d.quarter}','DayOfWeek':d.day_name()} for d in dates])
    cities = [('New York','NY'),('Boston','MA'),('Chicago','IL'),('Austin','TX'),
              ('Miami','FL'),('Los Angeles','CA'),('Seattle','WA')]
    put('DimStore',[{'StoreId':i,'StoreName':f'Aster {c}','City':c,'State':s}
                    for i,(c,s) in enumerate(cities,1)])
    put('DimLocation',[{'LocationId':i,'LocationName':f'Aster {c}','LocationType':'Store',
                       'State':s} for i,(c,s) in enumerate(cities,1)] +
                      [{'LocationId':8,'LocationName':'Columbus Distribution','LocationType':'Warehouse','State':'OH'}])
    put('DimChannel',[{'ChannelId':1,'Channel':'Retail'},{'ChannelId':2,'Channel':'E-commerce'},
                      {'ChannelId':3,'Channel':'Wholesale'}])
    put('DimSupplier',[{'SupplierId':i,'SupplierName':f'Aster Supply Partner {i:02}',
        'StandardLeadDays':int(rng.integers(9,19)),'Terms':'Net 30'} for i in range(1,29)])
    categories = [('Handbags',40,220),('Totes',35,145),('Backpacks',30,175),
                  ('Travel',35,95),('Pouches',40,48),('Lifestyle',20,38)]
    products = []
    for cat,n,price in categories:
        for j in range(n):
            p = len(products)+1
            products.append({'ProductId':p,'SKU':f'AST-{cat[:3].upper()}-{j+1:03}',
                'ProductName':f'{cat.rstrip("s")} {("Canvas","Signature","Studio","Everyday")[j%4]} {j+1:02}',
                'Category':cat,'SupplierId':1+(p-1)%28,'RetailPrice':round(price*rng.uniform(.85,1.2),2),
                'OpeningUnitCost':round(price*rng.uniform(.31,.41),4),
                'Customizable':int(cat in ['Handbags','Totes','Pouches'])})
    put('DimProduct',products)
    put('DimCustomer',[{'CustomerId':i,'CustomerCode':f'SYN-C{i:05}',
        'Segment':rng.choice(['New','Returning','VIP'],p=[.35,.5,.15]),
        'State':rng.choice([x[1] for x in cities]),'Synthetic':1} for i in range(1,4001)])
    # Target pouch assortment. Same cohort links demand, costs, replenishment and mapping incidents.
    cohort = set(range(151,171))
    orders, lines, events, erplinks, anomalies = [], [], [], [], []
    weights = np.array([(1+.55*k/len(dates))*(1.3 if d.month in [11,12] else 1)
                        for k,d in enumerate(dates)])
    orderdays = sorted(rng.choice(len(dates),24000,p=weights/weights.sum()))
    by_day = defaultdict(list)
    lineid = 0
    product_weights = np.array([1/(1+(p%35)*.065) for p in range(1,201)])
    for oid,di in enumerate(orderdays,1):
        date=dates[di]; channel=int(rng.choice([1,2,3],p=[.51,.40,.09]))
        loc=int(rng.integers(1,8)) if channel==1 else 8
        count=int(rng.choice([1,2,3],p=[.42,.47,.11]))
        pw=product_weights.copy()
        if date>=RISK_START:
            pw[[p-1 for p in cohort]] *= 4.0
        ids=rng.choice(np.arange(1,201),count,replace=False,p=pw/pw.sum())
        affected=date>=RISK_START and any(p in cohort for p in ids)
        canceled=bool(rng.random()<.018)
        issue='None'; available=date + pd.Timedelta(days=0 if channel==1 else int(rng.integers(1,3)))
        erpdate=date; erpid=f'ERP-{oid:07}'
        if channel==2 and not canceled:
            chance=rng.random()
            if chance < (.20 if affected else .025):
                issue='SKU mapping' if affected else 'Processing delay'
            elif chance < (.24 if affected else .04):
                issue='Missing webhook'
            if issue!='None':
                delay=int(rng.integers(4,14)) if affected else int(rng.integers(2,6))
                erpdate=date+pd.Timedelta(days=delay)
                if issue!='Missing webhook':
                    events.append({'EventId':len(events)+1,'OrderId':oid,'EventDate':ds(date),
                        'SourceSystem':'Shopify simulation','EventType':issue,'Status':'Failed',
                        'BusinessKey':f'WEB-{oid:07}','PayloadSKU':'UNKNOWN-SKU' if issue=='SKU mapping' else '',
                        'Deduplicated':0})
                if erpdate>CUTOFF: erpid=''
                available=max(available,erpdate)
                anomalies.append({'AnomalyId':len(anomalies)+1,'Scenario':'C','Entity':'Order',
                    'EntityId':oid,'Issue':issue,'StartDate':ds(date),'Cohort':int(affected)})
            if erpdate<=CUTOFF:
                events.append({'EventId':len(events)+1,'OrderId':oid,'EventDate':ds(erpdate),
                    'SourceSystem':'Shopify simulation','EventType':'Order sync','Status':'Success',
                    'BusinessKey':f'WEB-{oid:07}','PayloadSKU':'','Deduplicated':0})
            if rng.random()<.035:
                events.append({'EventId':len(events)+1,'OrderId':oid,'EventDate':ds(date),
                    'SourceSystem':'Shopify simulation','EventType':'Duplicate webhook','Status':'Ignored duplicate',
                    'BusinessKey':f'WEB-{oid:07}','PayloadSKU':'','Deduplicated':1})
                anomalies.append({'AnomalyId':len(anomalies)+1,'Scenario':'C','Entity':'Order',
                    'EntityId':oid,'Issue':'Duplicate webhook','StartDate':ds(date),'Cohort':int(affected)})
        if canceled: erpid=''
        if erpid:
            erplinks.append({'ERPLinkId':len(erplinks)+1,'OrderId':oid,'ERPOrderId':erpid,'SyncedDate':ds(erpdate)})
        order={'OrderId':oid,'OrderNumber':f'AST-{oid:07}','OrderDate':ds(date),'CustomerId':int(rng.integers(1,4001)),
            'ChannelId':channel,'LocationId':loc,'PromisedDate':ds(date+pd.Timedelta(days=1 if channel==1 else 4)),
            'OrderStatus':'Canceled' if canceled else 'Open','PaymentStatus':'Voided' if canceled else 'Captured',
            'IntegrationIssue':issue,'AvailableDate':ds(available),'Cohort':int(affected)}
        orders.append(order)
        order['_lines']=[]
        for pid in ids:
            pid=int(pid); prod=products[pid-1]
            qty=int(rng.integers(4,10)) if channel==3 else int(rng.choice([1,2],p=[.88,.12]))
            progression=max(0,(date-pd.Timestamp('2026-01-01')).days)/273
            discount=.32 if channel==3 else float(rng.choice([0,.05,.10],p=[.6,.25,.15]))
            if date>=pd.Timestamp('2026-01-01') and prod['Category'] in ['Pouches','Travel']:
                discount+=.06+.11*progression
            discount=min(discount,.55)
            gross=round(qty*prod['RetailPrice'],2); reduction=round(gross*discount,2)
            lineid+=1
            line={'OrderLineId':lineid,'OrderId':oid,'ProductId':pid,'Quantity':qty,
                'UnitPrice':prod['RetailPrice'],'DiscountAmount':reduction,'OrderedAmount':round(gross-reduction,2)}
            lines.append(line); order['_lines'].append(line)
        by_day[ds(date)].append(order)
    # Physical inventory and moving weighted average valuation. Currency ledger uses four decimals.
    onhand=np.zeros((9,201),dtype=int); values=np.zeros((9,201),dtype=float)
    moves=[]; snapshots=[]; pos=[]; shipments=[]; returns=[]; sales=[]
    receipts=defaultdict(list); return_due=defaultdict(list); pending=[]; open_po={}
    def move(date,loc,pid,qty,value,kind,reference,transfer=''):
        onhand[loc,pid]+=qty; values[loc,pid]=round(values[loc,pid]+value,4)
        if onhand[loc,pid]==0: values[loc,pid]=0.0
        moves.append({'MovementId':len(moves)+1,'MovementDate':ds(date),'LocationId':loc,'ProductId':pid,
            'MovementType':kind,'QuantityChange':int(qty),'ValueChange':round(value,4),
            'ReferenceType':reference[0],'ReferenceId':reference[1],'TransferId':transfer})
    def unit(loc,pid):
        return values[loc,pid]/onhand[loc,pid] if onhand[loc,pid] else 0
    for loc in range(1,9):
        for pid in range(1,201):
            q=int(rng.integers(70,110)) if loc==8 else int(rng.integers(8,23))
            if loc in [3,7] and pid>180: q=60
            move(START,loc,pid,q,round(q*products[pid-1]['OpeningUnitCost'],4),'Opening',('Opening',f'{loc}-{pid}'))
    for day in dates:
        key=ds(day)
        for po in receipts[key]:
            pid=po['ProductId']; qty=po['Quantity']
            move(day,8,pid,qty,round(qty*po['UnitCost'],4),'Purchase receipt',('PO',po['PurchaseOrderId']))
            po['ReceivedDate']=key; po['POStatus']='Received'; open_po.pop(pid,None)
        for ret in return_due[key]:
            pid=ret['ProductId'];loc=ret['LocationId']
            move(day,loc,pid,ret['Quantity'],ret['CostReversal'],'Customer return',('Return',ret['ReturnId']))
            returns.append(ret)
            sales.append({'SalesTransactionId':len(sales)+1,'PostingDate':key,'OrderId':ret['OrderId'],
                'OrderLineId':ret['OrderLineId'],'ProductId':pid,'LocationId':loc,'ChannelId':ret['ChannelId'],
                'CustomerId':ret['CustomerId'],'TransactionType':'Return','Quantity':-ret['Quantity'],
                'NetAmount':-ret['RefundAmount'],'COGS':-ret['CostReversal'],'DiscountAmount':0.0})
        # Store transfers twice weekly. Target products are misallocated in two stores after July.
        if day.weekday() in [0,3]:
            for loc in range(1,8):
                for pid in range(1,201):
                    target=3 if day>=RISK_START and loc in [2,5] and pid in cohort else 17
                    if onhand[loc,pid]<target//2+1:
                        q=min(target-onhand[loc,pid],onhand[8,pid])
                        if q>0:
                            val=round(unit(8,pid)*q,4);tid=f'TRF-{key}-{loc}-{pid}'
                            move(day,8,pid,-q,-val,'Transfer out',('Transfer',tid),tid)
                            move(day,loc,pid,q,val,'Transfer in',('Transfer',tid),tid)
        pending.extend(o for o in by_day[key] if o['OrderStatus']!='Canceled')
        nextpending=[]
        for order in pending:
            if order['AvailableDate']>key or any(onhand[order['LocationId'],l['ProductId']]<l['Quantity'] for l in order['_lines']):
                nextpending.append(order);continue
            order['OrderStatus']='Fulfilled'; sid=len(shipments)+1
            shipments.append({'ShipmentId':sid,'OrderId':order['OrderId'],'ShipDate':key,
                'LocationId':order['LocationId'],'OrderDate':order['OrderDate'],'ChannelId':order['ChannelId'],
                'PromisedDate':order['PromisedDate'],'FulfillmentDays':(day-pd.Timestamp(order['OrderDate'])).days,
                'IsLate':int(key>order['PromisedDate'])})
            for line in order['_lines']:
                pid=line['ProductId'];loc=order['LocationId'];q=line['Quantity'];cost=round(q*unit(loc,pid),4)
                move(day,loc,pid,-q,-cost,'Shipment',('OrderLine',line['OrderLineId']))
                sales.append({'SalesTransactionId':len(sales)+1,'PostingDate':key,'OrderId':order['OrderId'],
                    'OrderLineId':line['OrderLineId'],'ProductId':pid,'LocationId':loc,'ChannelId':order['ChannelId'],
                    'CustomerId':order['CustomerId'],'TransactionType':'Sale','Quantity':q,
                    'NetAmount':line['OrderedAmount'],'COGS':cost,'DiscountAmount':line['DiscountAmount']})
                returnrate=.13 if day>=RISK_START and pid in cohort else .035
                if rng.random()<returnrate:
                    retdate=day+pd.Timedelta(days=int(rng.integers(5,29)))
                    if retdate<=CUTOFF:
                        rid=f'RET-{line["OrderLineId"]:07}'
                        return_due[ds(retdate)].append({'ReturnId':rid,'OrderId':order['OrderId'],
                            'OrderLineId':line['OrderLineId'],'ReturnDate':ds(retdate),'ProductId':pid,
                            'LocationId':loc,'ChannelId':order['ChannelId'],'CustomerId':order['CustomerId'],
                            'Quantity':1,'RefundAmount':round(line['OrderedAmount']/q,2),
                            'CostReversal':round(cost/q,4),'Reason':rng.choice(['Fit / preference','Quality','Personalization']),
                            'Disposition':'Restocked'})
        pending=nextpending
        for pid in range(1,201):
            if onhand[8,pid]<45 and pid not in open_po:
                prod=products[pid-1];supplier=tables['DimSupplier'].iloc[prod['SupplierId']-1]
                impacted=day>=RISK_START and pid in cohort
                approval=int(rng.integers(5,10)) if impacted else int(rng.integers(0,3))
                lead=int(supplier['StandardLeadDays']);delay=int(rng.integers(9,17)) if impacted else int(rng.choice([0,0,0,0,3]))
                approve=day+pd.Timedelta(days=approval); promised=approve+pd.Timedelta(days=lead); actual=promised+pd.Timedelta(days=delay)
                qty=180
                inflation=max(0,(day-pd.Timestamp('2026-01-01')).days)/273
                cost=round(prod['OpeningUnitCost']*(1+inflation*(.28 if prod['Category'] in ['Pouches','Travel'] else .035)),4)
                po={'PurchaseOrderId':len(pos)+1,'PONumber':f'PO-{len(pos)+1:06}',
                    'ProductId':pid,'SupplierId':prod['SupplierId'],'LocationId':8,'PODate':key,
                    'ApprovalDate':ds(approve) if approve<=CUTOFF else '',
                    'PromisedReceiptDate':ds(promised),'ReceivedDate':'','Quantity':qty,'UnitCost':cost,
                    'POAmount':round(qty*cost,2),'ApprovalDays':approval,
                    'POStatus':'Pending approval' if approve>CUTOFF else 'Open','ScenarioAffected':int(impacted)}
                pos.append(po);open_po[pid]=po;receipts[ds(actual)].append(po)
                if impacted:
                    anomalies.append({'AnomalyId':len(anomalies)+1,'Scenario':'E','Entity':'PO',
                        'EntityId':po['PurchaseOrderId'],'Issue':'Approval and supplier delay','StartDate':key,'Cohort':1})
        if day.is_month_end:
            for loc in range(1,9):
                for pid in range(1,201):
                    snapshots.append({'SnapshotId':len(snapshots)+1,'SnapshotDate':key,'LocationId':loc,
                        'ProductId':pid,'UnitsOnHand':int(onhand[loc,pid]),'InventoryValue':round(values[loc,pid],4),
                        'WeightedAverageCost':round(unit(loc,pid),6)})
    put('FactSalesOrders',[{k:v for k,v in o.items() if k!='_lines'} for o in orders])
    put('FactSalesOrderLines',lines);put('FactShipments',shipments);put('FactReturns',returns)
    put('FactSalesTransactions',sales);put('FactPurchaseOrders',pos)
    put('FactInventoryMovements',moves);put('FactInventorySnapshots',snapshots)
    put('FactIntegrationEvents',events);put('FactERPOrderLinks',erplinks)
    # Deterministic budgets at month/channel/location grain, prepared independently from realized sales.
    budgets=[]
    for mi,month in enumerate(pd.date_range(START,CUTOFF,freq='MS')):
        base=235000*(1+.018*mi)*(1.3 if month.month in [11,12] else 1)
        for channel,share in [(1,.49),(2,.32),(3,.19)]:
            for loc in (range(1,8) if channel==1 else [8]):
                budgets.append({'BudgetId':len(budgets)+1,'MonthStart':ds(month),
                    'ChannelId':channel,'LocationId':loc,'SalesBudget':round(base*share/(7 if channel==1 else 1),2)})
    put('FactBudget',budgets)
    tickets=[]
    incident_orders=[o for o in orders if o['IntegrationIssue']!='None']
    for o in incident_orders:
        if rng.random()>.48: continue
        opened=pd.Timestamp(o['OrderDate'])+pd.Timedelta(hours=int(rng.integers(8,18)))
        severity='High' if o['Cohort'] else 'Medium';hours=24 if severity=='High' else 72
        duration=int(rng.integers(12,150)) if o['Cohort'] else int(rng.integers(3,96))
        resolved=opened+pd.Timedelta(hours=duration)
        cutoffend=CUTOFF+pd.Timedelta(days=1)-pd.Timedelta(seconds=1)
        closed=resolved<=cutoffend
        tickets.append({'TicketId':len(tickets)+1,'OrderId':o['OrderId'],'OpenedAt':opened.isoformat(),
            'ResolvedAt':resolved.isoformat() if closed else '',
            'SLADeadline':(opened+pd.Timedelta(hours=hours)).isoformat(),
            'Category':o['IntegrationIssue'],'Severity':severity,'Status':'Resolved' if closed else 'Open',
            'Owner':rng.choice(['Integration analyst A','Integration analyst B','ERP support']),
            'RepeatKey':f'{o["IntegrationIssue"]}-pouch' if o['Cohort'] else o['IntegrationIssue'],
            'ResolutionHours':duration if closed else None,
            'SLAEligible':int(closed or opened+pd.Timedelta(hours=hours)<=cutoffend),
            'SLAMet':int(closed and resolved<=opened+pd.Timedelta(hours=hours))})
    put('FactSupportTickets',tickets)
    put('InjectedAnomalies',anomalies)
    scenario={'seed':SEED,'start_date':ds(START),'reporting_cutoff':ds(CUTOFF),
        'company':'Aster & Co. (fictional)','currency':'USD','timezone':'America/New_York',
        'risk_start':ds(RISK_START),'risk_product_ids':sorted(cohort),'risk_locations':[2,5],
        'scenarios':{
            'A':'Travel and pouch discount increases and supplier inflation after January 2026; higher cohort returns from July.',
            'B':'Boston and Miami cohort transfer targets reduced to 3 units from July. Lifestyle excess at Chicago and Seattle.',
            'C':'Order-linked sync failures, missing webhooks and correctly ignored duplicate webhooks.',
            'D':'Integration incident tickets, with elapsed 24-hour/72-hour SLA rules and cutoff-aware eligibility.',
            'E':'Cohort purchase approvals delayed 5-9 days plus supplier delivery delays 9-16 days from July.'},
        'valuation':'Perpetual moving weighted average, four decimal USD; returns restore original issue cost.',
        'recognition':'Shipment-date operational sales proxy. Not audited GAAP revenue. Tax, freight and operating expenses excluded.'}
    (ROOT/'data/scenario.json').write_text(json.dumps(scenario,indent=2))
    hashes={}
    for name,df in tables.items():
        path=ROOT/'data/raw'/f'{name}.csv';df.to_csv(path,index=False,float_format='%.6f')
        hashes[name]={'rows':len(df),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    (ROOT/'data/manifest.json').write_text(json.dumps(hashes,indent=2))
    print(json.dumps({k:len(v) for k,v in tables.items()},indent=2))
    return tables

if __name__=='__main__': generate()
