"""Independent structural, financial, inventory and scenario acceptance checks."""
import json, sqlite3, hashlib
import numpy as np
import pandas as pd
from generate_data import ROOT, START, CUTOFF

def validate(write=True):
    t={p.stem:pd.read_csv(p,keep_default_na=False) for p in (ROOT/'data/raw').glob('*.csv')}
    checks=[]
    def check(name,passed,detail=''):
        checks.append({'check':name,'passed':bool(passed),'detail':str(detail)})
    dims={'ProductId':'DimProduct','LocationId':'DimLocation','ChannelId':'DimChannel',
          'CustomerId':'DimCustomer','SupplierId':'DimSupplier','OrderId':'FactSalesOrders',
          'OrderLineId':'FactSalesOrderLines'}
    keys={'DimDate':'Date','DimStore':'StoreId','DimLocation':'LocationId','DimChannel':'ChannelId',
          'DimSupplier':'SupplierId','DimProduct':'ProductId','DimCustomer':'CustomerId',
          'FactSalesOrders':'OrderId','FactSalesOrderLines':'OrderLineId','FactShipments':'ShipmentId',
          'FactReturns':'ReturnId','FactSalesTransactions':'SalesTransactionId','FactPurchaseOrders':'PurchaseOrderId',
          'FactInventoryMovements':'MovementId','FactInventorySnapshots':'SnapshotId','FactIntegrationEvents':'EventId',
          'FactERPOrderLinks':'ERPLinkId','FactBudget':'BudgetId','FactSupportTickets':'TicketId','InjectedAnomalies':'AnomalyId'}
    missing={}; references=0
    allowed_empty={'ReceivedDate','ApprovalDate','ResolvedAt','ResolutionHours','PayloadSKU','TransferId'}
    manifest=json.loads((ROOT/'data/manifest.json').read_text())
    for name,df in t.items():
        check(f'{name}: primary key unique',not df[keys[name]].duplicated().any())
        check(f'{name}: manifest matches',hashlib.sha256((ROOT/'data/raw'/f'{name}.csv').read_bytes()).hexdigest()==manifest[name]['sha256'])
        missing[name]={c:int((df[c].eq('')|df[c].isna()).sum()) for c in df.columns if (df[c].eq('')|df[c].isna()).any()}
        for col in df:
            if col not in allowed_empty:
                check(f'{name}.{col}: required',not (df[col].eq('')|df[col].isna()).any())
            if col in dims and dims[col]!=name:
                bad=~df[col].isin(t[dims[col]][col]);references+=int(bad.sum())
                check(f'{name}.{col}: foreign key',not bad.any(),f'{bad.sum()} invalid references')
    orders=t['FactSalesOrders'];sales=t['FactSalesTransactions'];lines=t['FactSalesOrderLines'];ship=t['FactShipments']
    canceled=set(orders.loc[orders.OrderStatus.eq('Canceled'),'OrderId'])
    check('Canceled orders never posted',not sales.OrderId.isin(canceled).any())
    check('Canceled orders never shipped',not ship.OrderId.isin(canceled).any())
    check('Exactly one shipment per fulfilled order',not ship.OrderId.duplicated().any() and len(ship)==orders.OrderStatus.eq('Fulfilled').sum())
    posted=sales[sales.TransactionType.eq('Sale')]
    check('Duplicate webhooks never duplicate finalized sales',not posted.OrderLineId.duplicated().any())
    erp=t['FactERPOrderLinks'];check('One ERP business order per source order',not erp.OrderId.duplicated().any() and not erp.ERPOrderId.duplicated().any())
    amounts=posted.merge(lines,on='OrderLineId',suffixes=('','_source'))
    check('Sales line amount matches order line',np.allclose(amounts.NetAmount,amounts.OrderedAmount,atol=.005))
    check('Sales quantities match order lines',(amounts.Quantity==amounts.Quantity_source).all())
    ret=t['FactReturns'].merge(posted,on='OrderLineId',suffixes=('','_sale'))
    check('Returns reference actual completed sales',len(ret)==len(t['FactReturns']))
    check('Return dates follow sales',(ret.ReturnDate>=ret.PostingDate).all())
    check('Return belongs to correct order and product',(ret.OrderId==ret.OrderId_sale).all() and (ret.ProductId==ret.ProductId_sale).all())
    returned=ret.groupby('OrderLineId').Quantity.sum()
    check('Returns do not exceed sold quantities',(returned<=posted.set_index('OrderLineId').Quantity.reindex(returned.index)).all())
    expected_refund=np.array([round(float(amount)/int(qty)*int(returnedqty),2) for amount,qty,returnedqty in zip(ret.NetAmount,ret.Quantity_sale,ret.Quantity)])
    check('Refunds use original discounted unit price',np.allclose(ret.RefundAmount,expected_refund,atol=.00001))
    move=t['FactInventoryMovements'];snaps=t['FactInventorySnapshots']
    cumulative=move.groupby(['LocationId','ProductId']).QuantityChange.cumsum()
    check('No negative physical inventory',(cumulative>=0).all())
    valuecum=move.groupby(['LocationId','ProductId']).ValueChange.cumsum()
    check('No negative inventory value',(valuecum>=-.001).all())
    roll=move.groupby(['LocationId','ProductId','MovementDate'])[['QuantityChange','ValueChange']].sum().reset_index()
    roll['QuantityBalance']=roll.groupby(['LocationId','ProductId']).QuantityChange.cumsum()
    roll['ValueBalance']=roll.groupby(['LocationId','ProductId']).ValueChange.cumsum()
    maxqty=0;maxval=0
    for date,grp in snaps.groupby('SnapshotDate'):
        latest=roll[roll.MovementDate.le(date)].sort_values('MovementDate').groupby(['LocationId','ProductId']).tail(1)
        joined=grp.merge(latest,on=['LocationId','ProductId'],validate='one_to_one')
        maxqty=max(maxqty,int((joined.UnitsOnHand-joined.QuantityBalance).abs().max()))
        maxval=max(maxval,float((joined.InventoryValue-joined.ValueBalance).abs().max()))
    check('Every monthly snapshot reconciles to movements',maxqty==0 and maxval<.001,f'max quantity delta={maxqty}; value delta={maxval:.8f}')
    transfers=move[move.TransferId.ne('')].groupby('TransferId').agg(q=('QuantityChange','sum'),v=('ValueChange','sum'),n=('MovementId','count'))
    check('Transfers conserve units and value',transfers.q.eq(0).all() and transfers.v.abs().lt(.001).all() and transfers.n.eq(2).all())
    # Independently replay the cost of every issue using the prior balance.
    previousq=cumulative-move.QuantityChange;previousv=valuecum-move.ValueChange
    issues=move.MovementType.isin(['Shipment','Transfer out'])
    expected=(previousv[issues]/previousq[issues]*move.loc[issues,'QuantityChange']).round(4)
    check('Issues use moving weighted average cost',np.allclose(expected,move.loc[issues,'ValueChange'],atol=.00011))
    issued=move[move.MovementType.eq('Shipment')].copy();issued['OrderLineId']=issued.ReferenceId.astype(int)
    aligned=posted.merge(issued[['OrderLineId','ValueChange']],on='OrderLineId',validate='one_to_one')
    check('COGS reconciles to physical shipment issues',np.allclose(aligned.COGS,-aligned.ValueChange,atol=.00011))
    po=t['FactPurchaseOrders'];receipts=move[move.MovementType.eq('Purchase receipt')].copy();receipts['PurchaseOrderId']=receipts.ReferenceId.astype(int)
    j=receipts.merge(po,on='PurchaseOrderId')
    check('Received PO units and costs reconcile',(j.QuantityChange==j.Quantity).all() and np.allclose(j.ValueChange,j.Quantity*j.UnitCost,atol=.00011))
    check('No shipment occurs before order',(ship.ShipDate>=ship.OrderDate).all())
    tk=t['FactSupportTickets'];resolved=tk.Status.eq('Resolved')
    deadline=pd.to_datetime(tk.SLADeadline);closed=pd.to_datetime(tk.ResolvedAt,errors='coerce');end=CUTOFF+pd.Timedelta(days=1)-pd.Timedelta(seconds=1)
    eligible=(resolved|deadline.le(end)).astype(int);met=(resolved&closed.le(deadline)).astype(int)
    check('SLA eligibility includes overdue open tickets',(tk.SLAEligible==eligible).all())
    check('SLA compliance uses resolution deadline',(tk.SLAMet==met).all())
    check('MTTR uses closed tickets only',tk.loc[~resolved,'ResolutionHours'].eq('').all())
    for name,df in t.items():
        for col in ['OrderDate','ShipDate','PostingDate','EventDate','MovementDate','SnapshotDate','ReturnDate','PODate','ReceivedDate']:
            if col in df:
                actual=df.loc[df[col].ne(''),col]
                check(f'{name}.{col}: cutoff',actual.le(str(CUTOFF.date())).all())
    a=t['InjectedAnomalies'];check('Scenario C anomalies documented',a.Scenario.eq('C').any());check('Scenario E anomalies documented',a.Scenario.eq('E').any())
    with sqlite3.connect(ROOT/'data/processed/retail360.sqlite') as con:
        queries=(ROOT/'sql/validation_queries.sql').read_text().split(';')
        for i,q in enumerate(queries,1):
            if q.strip():
                rows=con.execute(q).fetchall();check(f'SQL structural check {i}',len(rows)==0,f'{len(rows)} exceptions')
        total=con.execute('SELECT SUM(NetAmount),SUM(COGS) FROM FactSalesTransactions').fetchone()
        report=con.execute('SELECT SUM(NetSales),SUM(COGS) FROM ReportFinance').fetchone()
        check('SQL totals equal financial report mart',all(abs(x-y)<.01 for x,y in zip(total,report)))
    metrics=json.loads((ROOT/'reports/kpi_controls.json').read_text())
    check('Scenario A: comparable Q3 revenue grows',metrics['q3_sales_growth']>0)
    check('Scenario A: comparable Q3 margin declines',metrics['q3_margin_change_pp']<0)
    check('Scenario B: inventory imbalance detectable',metrics['stockout_risk_sku_locations']>0)
    check('Scenario C: missing records detectable',metrics['missing_event_orders']>0)
    check('Scenario C: duplicate webhooks present',metrics['deduplicated_events']>0)
    check('Scenario D: SLA breaches present',metrics['sla_compliance']<1)
    p=po[po.ScenarioAffected.eq(1)];check('Scenario E: approval delays present',len(p)>0 and p.ApprovalDays.ge(5).all())
    result={'passed':all(c['passed'] for c in checks),'check_count':len(checks),'failed_checks':[c for c in checks if not c['passed']],
        'rows':{k:len(df) for k,df in t.items()},'missing_values':missing,'invalid_references':references,
        'known_injected_exception_records':len(a),'checks':checks}
    if write:
        (ROOT/'reports/validation_report.json').write_text(json.dumps(result,indent=2))
        rows=['# Dataset validation','',f"Status: {'PASS' if result['passed'] else 'FAIL'}. {len(checks)} checks. Reporting cutoff: {CUTOFF.date()}.",'',
              'Intentional operational failures remain business exceptions. They are not broken foreign keys or duplicate sales.','',
              '| Check | Result | Detail |','|---|---|---|']
        rows.extend(f"| {c['check']} | {'PASS' if c['passed'] else 'FAIL'} | {c['detail']} |" for c in checks)
        (ROOT/'reports/validation_report.md').write_text('\n'.join(rows))
    print(json.dumps({k:v for k,v in result.items() if k in ['passed','check_count','failed_checks','invalid_references']},indent=2))
    if not result['passed']: raise SystemExit(1)
    return result

if __name__=='__main__':validate()
