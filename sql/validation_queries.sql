-- Each query returns zero rows for a passing structural dataset.
SELECT l.OrderLineId FROM FactSalesOrderLines l LEFT JOIN FactSalesOrders o USING(OrderId) WHERE o.OrderId IS NULL;
SELECT s.SalesTransactionId FROM FactSalesTransactions s JOIN FactSalesOrders o USING(OrderId) WHERE o.OrderStatus='Canceled';
SELECT OrderId,COUNT(*) FROM FactERPOrderLinks GROUP BY OrderId HAVING COUNT(*)>1;
SELECT OrderLineId,SUM(Quantity) FROM FactSalesTransactions WHERE TransactionType='Sale' GROUP BY OrderLineId HAVING COUNT(*)>1;
SELECT r.ReturnId FROM FactReturns r JOIN FactSalesOrderLines l USING(OrderLineId)
WHERE r.OrderId<>l.OrderId OR r.ProductId<>l.ProductId OR r.Quantity>l.Quantity;
SELECT TransferId FROM FactInventoryMovements WHERE TransferId IS NOT NULL
GROUP BY TransferId HAVING SUM(QuantityChange)<>0 OR ABS(SUM(ValueChange))>.0001;
SELECT s.SnapshotId FROM FactInventorySnapshots s JOIN FactInventoryMovements m
ON m.ProductId=s.ProductId AND m.LocationId=s.LocationId AND m.MovementDate<=s.SnapshotDate
GROUP BY s.SnapshotId HAVING SUM(m.QuantityChange)<>s.UnitsOnHand OR ABS(SUM(m.ValueChange)-s.InventoryValue)>.001;
