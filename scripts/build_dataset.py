"""Build SQLite analysis store, report marts, KPI controls and browser-import payload."""
from pathlib import Path
import json, sqlite3
import numpy as np
import pandas as pd
from generate_data import ROOT, START, CUTOFF

def build():
    t={p.stem:pd.read_csv(p,keep_default_na=False) for p in (ROOT/'data/raw').glob('*.csv')}
    out=ROOT/'data/processed'
    def save(name,df):
        df.to_csv(out/f'{name}.csv',index=False,float_format='%.6f');t[name]=df
        return df
    s=t['FactSalesTransactions'].copy();s['MonthStart']=s.PostingDate.str[:7]+'-01'
    s['SalesAmount']=s.NetAmount.where(s.TransactionType.eq('Sale'),0)
    s['RefundAmount']=-s.NetAmount.where(s.TransactionType.eq('Return'),0)
    s['SaleUnits']=s.Quantity.clip(lower=0);s['ReturnUnits']=-s.Quantity.clip(upper=0)
    fin=s.groupby(['MonthStart','ChannelId','LocationId']).agg(NetSales=('NetAmount','sum'),COGS=('COGS','sum'),
        SalesBeforeReturns=('SalesAmount','sum'),RefundAmount=('RefundAmount','sum'),UnitsSold=('SaleUnits','sum'),
        UnitsReturned=('ReturnUnits','sum'),DiscountAmount=('DiscountAmount','sum')).reset_index()
    counts=s[s.TransactionType.eq('Sale')].groupby(['MonthStart','ChannelId','LocationId']).OrderId.nunique().rename('FulfilledOrders')
    fin=fin.merge(counts,on=['MonthStart','ChannelId','LocationId'],how='left').merge(t['FactBudget'].drop(columns='BudgetId'),
        on=['MonthStart','ChannelId','LocationId'],how='outer').fillna(0)
    fin['GrossProfit']=fin.NetSales-fin.COGS
    fin=fin.merge(t['DimChannel'],on='ChannelId').merge(t['DimLocation'][['LocationId','LocationName']],on='LocationId')
    save('ReportFinance',fin)
    detail=s.merge(t['DimProduct'][['ProductId','Category','SKU','ProductName']],on='ProductId')
    cat=detail.groupby(['MonthStart','Category']).agg(NetSales=('NetAmount','sum'),COGS=('COGS','sum'),
        UnitsSold=('SaleUnits','sum'),UnitsReturned=('ReturnUnits','sum'),DiscountAmount=('DiscountAmount','sum')).reset_index()
    cat['GrossProfit']=cat.NetSales-cat.COGS;save('ReportCategory',cat)
    product=detail.groupby(['MonthStart','ProductId','SKU','ProductName','Category']).agg(NetSales=('NetAmount','sum'),
        COGS=('COGS','sum'),UnitsSold=('SaleUnits','sum'),UnitsReturned=('ReturnUnits','sum')).reset_index()
    product['GrossProfit']=product.NetSales-product.COGS;save('ReportProduct',product)
    orders=t['FactSalesOrders'].copy();lines=t['FactSalesOrderLines'];ship=t['FactShipments']
    save('ReportOrderLines',lines.merge(orders,on='OrderId',validate='many_to_one'))
    outcomes=orders.merge(ship[['OrderId','ShipDate','FulfillmentDays','IsLate']],on='OrderId',how='left')
    outcomes['EligibleOrder']=orders.OrderStatus.ne('Canceled').astype(int)
    outcomes['FulfilledOrder']=outcomes.ShipDate.notna().astype(int)
    outcomes['OpenLateOrder']=((outcomes.OrderStatus.eq('Open')) & (outcomes.PromisedDate < str(CUTOFF.date()))).astype(int)
    outcomes['LateOrder']=((outcomes.IsLate.fillna(0).eq(1)) | outcomes.OpenLateOrder.eq(1)).astype(int)
    outcomes['FulfillmentDays']=outcomes.FulfillmentDays.fillna(0).astype(int)
    save('ReportOrders',outcomes.fillna(''))
    demand=lines.merge(orders[['OrderId','OrderDate','LocationId','OrderStatus']],on='OrderId')
    recent=demand[(demand.OrderDate>=str((CUTOFF-pd.Timedelta(days=27)).date())) & demand.OrderStatus.ne('Canceled')]
    rate=recent.groupby(['LocationId','ProductId']).Quantity.sum().div(28).rename('DailyDemand')
    reserved=demand[demand.OrderStatus.eq('Open')].groupby(['LocationId','ProductId']).Quantity.sum().rename('BackorderUnits')
    inv=t['FactInventorySnapshots'];inv=inv[inv.SnapshotDate.eq(str(CUTOFF.date()))].copy()
    inv=inv.merge(rate,on=['LocationId','ProductId'],how='left').merge(reserved,on=['LocationId','ProductId'],how='left').fillna(0)
    inv['AvailableUnits']=(inv.UnitsOnHand-inv.BackorderUnits).clip(lower=0)
    inv=inv.merge(t['DimProduct'],on='ProductId').merge(t['DimLocation'],on='LocationId')
    inv=inv.merge(t['DimSupplier'][['SupplierId','StandardLeadDays']],on='SupplierId')
    inv['ProtectionDays']=np.where(inv.LocationId.eq(8),inv.StandardLeadDays+7,7)
    inv['ReorderPoint']=np.ceil(inv.DailyDemand*inv.ProtectionDays).astype(int)
    inv['StockoutRisk']=(inv.AvailableUnits.lt(inv.ReorderPoint) | inv.BackorderUnits.gt(inv.UnitsOnHand)).astype(int)
    inv['LowStock']=(inv.UnitsOnHand.le(inv.ReorderPoint) & inv.DailyDemand.gt(0)).astype(int)
    inv['DaysCover']=np.where(inv.DailyDemand.gt(0),inv.AvailableUnits/inv.DailyDemand,np.nan)
    inv['ExcessUnits']=(inv.AvailableUnits-np.ceil(inv.DailyDemand*60)).clip(lower=0).astype(int)
    inv['RecommendedUnits']=(np.ceil(inv.DailyDemand*(inv.ProtectionDays+7))-inv.AvailableUnits).clip(lower=0).astype(int)
    dc=inv[inv.LocationId.eq(8)].set_index('ProductId').AvailableUnits
    inv['WarehouseAvailable']=inv.ProductId.map(dc)
    inv['Action']=np.select([inv.BackorderUnits.gt(0),inv.StockoutRisk.eq(1)&inv.WarehouseAvailable.gt(0)&inv.LocationId.ne(8),
        inv.StockoutRisk.eq(1),inv.ExcessUnits.gt(20)],['Expedite backlog','Transfer from warehouse','Review purchase order','Review transfer out'],default='Monitor')
    save('ReportInventory',inv)
    # Daily historical inventory totals from all signed movements, not one current snapshot.
    movements=t['FactInventoryMovements']
    balance=movements.groupby('MovementDate').agg(QuantityChange=('QuantityChange','sum'),ValueChange=('ValueChange','sum'))
    balance=balance.reindex(pd.date_range(START,CUTOFF).strftime('%Y-%m-%d'),fill_value=0)
    balance['UnitsOnHand']=balance.QuantityChange.cumsum();balance['InventoryValue']=balance.ValueChange.cumsum()
    balance=balance.reset_index().rename(columns={'index':'BalanceDate'})
    save('ReportDailyInventory',balance)
    events=t['FactIntegrationEvents'];tickets=t['FactSupportTickets'].copy()
    tickets['ResolutionHours']=pd.to_numeric(tickets.ResolutionHours,errors='coerce')
    tickets['MonthStart']=tickets.OpenedAt.str[:7]+'-01'
    tickets['ResolvedCount']=tickets.Status.eq('Resolved').astype(int)
    tickets['OpenCount']=tickets.Status.ne('Resolved').astype(int)
    tickets=tickets.sort_values(['OpenedAt','TicketId'])
    tickets['RepeatIncident']=tickets.duplicated('RepeatKey').astype(int)
    save('ReportTickets',tickets)
    recon=orders[(orders.ChannelId.eq(2)) & orders.OrderStatus.ne('Canceled')].merge(
        t['FactERPOrderLinks'][['OrderId','ERPOrderId','SyncedDate']],on='OrderId',how='left')
    recon['SyncStatus']=np.where(recon.ERPOrderId.notna(),'Reconciled','Awaiting reconciliation')
    recon['OrderedAmount']=recon.OrderId.map(lines.groupby('OrderId').OrderedAmount.sum())
    recon['AgeDays']=(CUTOFF-pd.to_datetime(recon.OrderDate)).dt.days
    recon['HasEvent']=recon.OrderId.isin(events.OrderId).astype(int)
    recon['ExceptionType']=np.where(recon.SyncStatus.eq('Reconciled'),'None',
        np.where(recon.HasEvent.eq(0),'Missing webhook',recon.IntegrationIssue))
    save('ReportReconciliation',recon.fillna(''))
    systems=[]
    for month in pd.date_range(START,CUTOFF,freq='MS'):
        m=month.strftime('%Y-%m');ev=events[events.EventDate.str.startswith(m)];tk=tickets[tickets.MonthStart.eq(m+'-01')]
        # As-of backlog is a cutoff snapshot; do not imply that it is a historical daily series.
        systems.append({'MonthStart':m+'-01','SuccessfulEvents':int(ev.Status.eq('Success').sum()),
            'FailedEvents':int(ev.Status.eq('Failed').sum()),'DuplicateEvents':int(ev.Deduplicated.sum()),
            'AttemptedEvents':int(ev.Status.isin(['Success','Failed']).sum()),'TicketsOpened':len(tk),
            'ResolvedTickets':int(tk.ResolvedCount.sum()),'OpenTickets':int(tk.OpenCount.sum()),
            'SLAEligible':int(tk.SLAEligible.sum()),'SLAMet':int(tk.SLAMet.sum()),
            'ResolutionHours':float(tk.ResolutionHours.sum()),'RepeatIncidents':int(tk.RepeatIncident.sum())})
    sys=save('ReportSystems',pd.DataFrame(systems))
    # PO delays are measured against approved promise, not order creation.
    po=t['FactPurchaseOrders'].copy()
    po['LateReceiptDays']=(pd.to_datetime(po.ReceivedDate,errors='coerce')-pd.to_datetime(po.PromisedReceiptDate)).dt.days
    po['OverdueOpen']=((po.POStatus.ne('Received')) & po.PromisedReceiptDate.lt(str(CUTOFF.date()))).astype(int)
    po=po.merge(t['DimProduct'][['ProductId','SKU','ProductName','Category']],on='ProductId').merge(t['DimSupplier'],on='SupplierId')
    save('ReportPurchasing',po)
    conn=sqlite3.connect(out/'retail360.sqlite')
    for name,df in t.items():
        clean=df.replace('',None)
        clean.to_sql(name,conn,if_exists='replace',index=False)
    conn.execute('CREATE UNIQUE INDEX IF NOT EXISTS ix_order ON FactSalesOrders(OrderId)')
    conn.execute('CREATE INDEX IF NOT EXISTS ix_sales_date ON FactSalesTransactions(PostingDate)')
    conn.execute('CREATE INDEX IF NOT EXISTS ix_move_date ON FactInventoryMovements(LocationId,ProductId,MovementDate)')
    # Independently calculated SQL aggregate is the control for all exported summaries.
    sqlsales=conn.execute('SELECT SUM(NetAmount),SUM(COGS) FROM FactSalesTransactions').fetchone()
    assert abs(sqlsales[0]-fin.NetSales.sum())<.01
    assert abs(sqlsales[1]-fin.COGS.sum())<.01
    monthly=fin.groupby('MonthStart')[['NetSales','COGS','GrossProfit','SalesBudget','UnitsSold','UnitsReturned','FulfilledOrders']].sum().reset_index()
    monthly['GrossMargin']=monthly.GrossProfit/monthly.NetSales
    save('ReportMonthly',monthly)
    comp=[]
    for year in [2025,2026]:
        q=s[s.PostingDate.between(f'{year}-07-01',f'{year}-09-30')]
        comp.append({'Year':year,'NetSales':float(q.NetAmount.sum()),'COGS':float(q.COGS.sum()),
            'GrossMargin':float((q.NetAmount.sum()-q.COGS.sum())/q.NetAmount.sum())})
    latest90=balance[balance.BalanceDate.ge(str((CUTOFF-pd.Timedelta(days=89)).date()))]
    cogs90=s[s.PostingDate.ge(str((CUTOFF-pd.Timedelta(days=89)).date()))].COGS.sum()
    metrics={'cutoff':str(CUTOFF.date()),'net_sales':float(sqlsales[0]),'cogs':float(sqlsales[1]),
        'gross_profit':float(sqlsales[0]-sqlsales[1]),'gross_margin':float(1-sqlsales[1]/sqlsales[0]),
        'sales_budget':float(fin.SalesBudget.sum()),'sales_vs_budget':float(fin.NetSales.sum()-fin.SalesBudget.sum()),
        'fulfilled_orders':int(outcomes.FulfilledOrder.sum()),'eligible_orders':int(outcomes.EligibleOrder.sum()),
        'fulfillment_rate':float(outcomes.FulfilledOrder.sum()/outcomes.EligibleOrder.sum()),
        'average_fulfillment_days':float(ship.FulfillmentDays.mean()),'late_orders':int(outcomes.LateOrder.sum()),
        'open_late_orders':int(outcomes.OpenLateOrder.sum()),'units_sold':int(s.SaleUnits.sum()),
        'units_returned':int(s.ReturnUnits.sum()),'return_rate':float(s.ReturnUnits.sum()/s.SaleUnits.sum()),
        'average_order_value':float(s.NetAmount.sum()/outcomes.FulfilledOrder.sum()),
        'inventory_value':float(inv.InventoryValue.sum()),'units_on_hand':int(inv.UnitsOnHand.sum()),
        'stockout_risk_sku_locations':int(inv.StockoutRisk.sum()),'low_stock_sku_locations':int(inv.LowStock.sum()),
        'inventory_turnover_90d_annualized':float(cogs90/latest90.InventoryValue.mean()*365/90),
        'days_inventory_90d':float(latest90.InventoryValue.mean()/cogs90*90),
        'pending_purchase_orders':int(po.POStatus.ne('Received').sum()),
        'integration_success_rate':float(sys.SuccessfulEvents.sum()/sys.AttemptedEvents.sum()),
        'failed_integration_events':int(sys.FailedEvents.sum()),'deduplicated_events':int(sys.DuplicateEvents.sum()),
        'unreconciled_orders':int(recon.SyncStatus.ne('Reconciled').sum()),
        'unreconciled_order_value':float(recon.loc[recon.SyncStatus.ne('Reconciled'),'OrderedAmount'].sum()),
        'missing_event_orders':int(((recon.SyncStatus.ne('Reconciled')) & recon.HasEvent.eq(0)).sum()),
        'open_tickets':int(tickets.OpenCount.sum()),'sla_compliance':float(tickets.SLAMet.sum()/tickets.SLAEligible.sum()),
        'mean_resolution_hours':float(tickets.ResolutionHours.mean()),'repeat_incidents':int(tickets.RepeatIncident.sum()),
        'high_priority_exceptions':int(((recon.SyncStatus.ne('Reconciled')) & recon.Cohort.eq(1)).sum()),
        'q3_comparison':comp,'sql_control':{'net_sales':sqlsales[0],'cogs':sqlsales[1]}}
    metrics['q3_sales_growth']=comp[1]['NetSales']/comp[0]['NetSales']-1
    metrics['q3_margin_change_pp']=(comp[1]['GrossMargin']-comp[0]['GrossMargin'])*100
    (ROOT/'reports/kpi_controls.json').write_text(json.dumps(metrics,indent=2))
    # Artifact-tool receives typed matrices; canonical full-detail data stays in CSV/SQLite.
    workbook_tables=['ReportFinance','ReportCategory','ReportInventory','ReportSystems','ReportPurchasing',
                     'ReportReconciliation','DimDate','DimChannel','DimLocation','DimProduct']
    payload={name:{'columns':list(t[name].columns),'rows':t[name].replace({np.nan:None}).values.tolist()} for name in workbook_tables}
    (ROOT/'reports/workbook_payload.json').write_text(json.dumps(payload,allow_nan=False))
    conn.commit();conn.close()
    print(json.dumps(metrics,indent=2))
    return metrics

if __name__=='__main__': build()
