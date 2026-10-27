"""Compact operational facts for the full Power BI metric extension."""
import json, sqlite3
import numpy as np
import pandas as pd
from generate_data import ROOT

def build():
    folder=ROOT/'data/processed';read=lambda n:pd.read_csv(folder/f'{n}.csv')
    orders=read('ReportOrders');orders['MonthStart']=orders.OrderDate.str[:7]+'-01'
    fulfillment=orders.groupby(['MonthStart','ChannelId','LocationId']).agg(
        EligibleOrders=('EligibleOrder','sum'),FulfilledOrders=('FulfilledOrder','sum'),
        LateOrders=('LateOrder','sum'),OpenLateOrders=('OpenLateOrder','sum'),FulfillmentDays=('FulfillmentDays','sum')).reset_index()
    raw=pd.read_csv(ROOT/'data/raw/FactSalesTransactions.csv')
    daily=raw.groupby('PostingDate').agg(NetSales=('NetAmount','sum'),COGS=('COGS','sum')).reset_index()
    tickets=read('ReportTickets');tickets['OpenDate']=tickets.OpenedAt.str[:10]
    tables={'ReportFulfillment':fulfillment,'ReportDailyFinance':daily,'ReportDailyInventory':read('ReportDailyInventory'),
            'ReportTickets':tickets,'ReportProduct':read('ReportProduct')}
    payload={}
    for name,df in tables.items():
        df.to_csv(folder/f'{name}.csv',index=False,float_format='%.6f')
        payload[name]={'columns':list(df.columns),'rows':df.replace({np.nan:None}).values.tolist()}
    with sqlite3.connect(folder/'retail360.sqlite') as conn:
        for name,df in tables.items():
            df.to_sql(name,conn,if_exists='replace',index=False)
        schema=';\n\n'.join(r[0] for r in conn.execute("SELECT sql FROM sqlite_master WHERE sql IS NOT NULL ORDER BY type,name"))+';\n'
        (ROOT/'sql/schema.sql').write_text(schema)
    controls=json.loads((ROOT/'reports/kpi_controls.json').read_text())
    observed={
        'eligible_orders':int(fulfillment.EligibleOrders.sum()),
        'fulfilled_orders':int(fulfillment.FulfilledOrders.sum()),
        'late_orders':int(fulfillment.LateOrders.sum()),
        'open_late_orders':int(fulfillment.OpenLateOrders.sum()),
        'net_sales':float(daily.NetSales.sum()),'cogs':float(daily.COGS.sum()),
        'open_tickets':int(tickets.OpenCount.sum()),
        'repeat_incidents':int(tickets.RepeatIncident.sum()),
    }
    assert all(abs(v-controls[k])<.0001 for k,v in observed.items()), observed
    (ROOT/'reports/operations_controls.json').write_text(json.dumps({'status':'passed','checks':len(observed),'values':observed},indent=2))
    (ROOT/'reports/operations_payload.json').write_text(json.dumps(payload,allow_nan=False))
    print({k:len(v) for k,v in tables.items()})
if __name__=='__main__':build()
