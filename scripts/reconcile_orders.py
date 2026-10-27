"""Reconciliation compares expected source orders to ERP links, including absent events."""
import sqlite3
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
QUERY='''
SELECT o.OrderId,o.OrderNumber,o.OrderDate,o.IntegrationIssue,
       CASE WHEN e.OrderId IS NULL THEN 'Missing event' ELSE 'Failed or delayed sync' END AS ExceptionType,
       SUM(l.OrderedAmount) AS OrderValue
FROM FactSalesOrders o
LEFT JOIN FactERPOrderLinks r ON r.OrderId=o.OrderId
LEFT JOIN (SELECT DISTINCT OrderId FROM FactIntegrationEvents) e ON e.OrderId=o.OrderId
JOIN FactSalesOrderLines l ON l.OrderId=o.OrderId
WHERE o.ChannelId=2 AND o.OrderStatus<>'Canceled' AND r.OrderId IS NULL
GROUP BY o.OrderId,o.OrderNumber,o.OrderDate,o.IntegrationIssue,e.OrderId
ORDER BY o.OrderDate,o.OrderId
'''
if __name__=='__main__':
    with sqlite3.connect(ROOT/'data/processed/retail360.sqlite') as con:
        df=pd.read_sql_query(QUERY,con)
    df.to_csv(ROOT/'reports/unreconciled_orders.csv',index=False)
    print(f'{len(df)} orders await reconciliation. Exposure is ordered value, not booked loss.')
