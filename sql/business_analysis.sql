-- SQLite 3. Use data/processed/retail360.sqlite. All source systems are simulated.
-- Net sales and gross profit use signed shipment/return posting transactions.
SELECT substr(PostingDate,1,7) AS Month,
       ROUND(SUM(NetAmount),2) AS NetSales,ROUND(SUM(COGS),2) AS COGS,
       ROUND(SUM(NetAmount-COGS),2) AS GrossProfit,
       SUM(NetAmount-COGS)/NULLIF(SUM(NetAmount),0) AS GrossMargin
FROM FactSalesTransactions GROUP BY Month ORDER BY Month;

-- Budget grain is month/channel/location. Aggregate facts before joining.
WITH actual AS (
 SELECT substr(PostingDate,1,7)||'-01' AS MonthStart,ChannelId,LocationId,SUM(NetAmount) AS Sales
 FROM FactSalesTransactions GROUP BY 1,2,3
)
SELECT b.MonthStart,b.ChannelId,b.LocationId,b.SalesBudget,COALESCE(a.Sales,0) AS NetSales,
       COALESCE(a.Sales,0)-b.SalesBudget AS Variance
FROM FactBudget b LEFT JOIN actual a USING(MonthStart,ChannelId,LocationId);

-- One order can have many events, but only one ERP order link.
SELECT o.OrderId,o.OrderNumber,o.OrderDate,o.IntegrationIssue,SUM(l.OrderedAmount) AS OrderValue
FROM FactSalesOrders o JOIN FactSalesOrderLines l USING(OrderId)
LEFT JOIN FactERPOrderLinks e USING(OrderId)
WHERE o.ChannelId=2 AND o.OrderStatus<>'Canceled' AND e.OrderId IS NULL
GROUP BY o.OrderId,o.OrderNumber,o.OrderDate,o.IntegrationIssue;

-- Cohort trace: investigate sales lines without multiplying them by event or ticket rows.
WITH incident AS (SELECT OrderId,COUNT(*) AS FailedEvents FROM FactIntegrationEvents WHERE Status='Failed' GROUP BY OrderId),
ticket AS (SELECT OrderId,COUNT(*) AS Tickets FROM FactSupportTickets GROUP BY OrderId)
SELECT o.OrderId,o.OrderDate,o.OrderStatus,o.LocationId,
       COALESCE(i.FailedEvents,0) AS FailedEvents,COALESCE(t.Tickets,0) AS Tickets,
       SUM(l.Quantity) AS OrderedUnits,SUM(l.OrderedAmount) AS OrderedAmount
FROM FactSalesOrders o JOIN FactSalesOrderLines l USING(OrderId)
LEFT JOIN incident i USING(OrderId) LEFT JOIN ticket t USING(OrderId)
WHERE o.Cohort=1 GROUP BY o.OrderId;

-- Resolved tickets plus open tickets past deadline are SLA eligible at cutoff.
SELECT SUM(SLAMet)*1.0/NULLIF(SUM(SLAEligible),0) AS SLACompliance,
       AVG(CASE WHEN Status='Resolved' THEN ResolutionHours END) AS MTTRHours
FROM FactSupportTickets;

-- Potential donors are recommendations; transfers are not executed automatically.
SELECT LocationName,SKU,UnitsOnHand,BackorderUnits,DailyDemand,ReorderPoint,Action,RecommendedUnits
FROM ReportInventory WHERE StockoutRisk=1 ORDER BY BackorderUnits DESC,RecommendedUnits DESC;

-- Store performance: retail only; warehouse-served commerce and wholesale excluded.
SELECT LocationName,ROUND(SUM(NetSales),2) AS NetSales,
       SUM(GrossProfit)/NULLIF(SUM(NetSales),0) AS GrossMargin,
       SUM(NetSales)/NULLIF(SUM(SalesBudget),0)-1 AS BudgetVariance
FROM ReportFinance WHERE ChannelId=1 GROUP BY LocationId ORDER BY NetSales DESC;

-- Product ranks retain the same posted-sales basis as the headline financials.
WITH p AS (SELECT ProductId,SKU,ProductName,Category,SUM(NetSales) AS NetSales,
                 SUM(GrossProfit) AS GrossProfit FROM ReportProduct GROUP BY ProductId)
SELECT *,RANK() OVER(ORDER BY NetSales DESC) AS SalesRank,
       GrossProfit/NULLIF(NetSales,0) AS GrossMargin FROM p ORDER BY NetSales DESC;

-- Fulfillment uses order cohorts, not posting dates or customer delivery dates.
SELECT MonthStart,SUM(FulfilledOrders)*1.0/NULLIF(SUM(EligibleOrders),0) AS FulfillmentRate,
       SUM(FulfillmentDays)/NULLIF(SUM(FulfilledOrders),0) AS AverageDays,
       SUM(LateOrders) AS LateOrders FROM ReportFulfillment GROUP BY MonthStart ORDER BY MonthStart;

SELECT l.LocationName,SUM(o.LateOrder) AS LateOrders,SUM(o.OpenLateOrder) AS OpenLateOrders
FROM ReportOrders o JOIN DimLocation l USING(LocationId)
GROUP BY o.LocationId ORDER BY LateOrders DESC;

-- Source events and ticket dimensions support optional detailed report visuals.
SELECT SourceSystem,SUM(Status='Failed') AS FailedEvents,
       SUM(Status='Success') AS SuccessfulEvents,SUM(Deduplicated) AS IgnoredDuplicates
FROM FactIntegrationEvents GROUP BY SourceSystem;

SELECT Category,Severity,COUNT(*) AS Tickets,SUM(OpenCount) AS OpenTickets,
       SUM(SLAMet)*1.0/NULLIF(SUM(SLAEligible),0) AS SLACompliance,
       SUM(ResolutionHours)/NULLIF(SUM(ResolvedCount),0) AS MTTRHours
FROM ReportTickets GROUP BY Category,Severity;

SELECT MonthStart,SUM(SLAMet)*1.0/NULLIF(SUM(SLAEligible),0) AS SLACompliance,
       SUM(RepeatIncident) AS RepeatIncidents FROM ReportTickets GROUP BY MonthStart ORDER BY MonthStart;

-- Business risk matrix uses measured counts and exposure, not an invented loss score.
SELECT ExceptionType,CASE WHEN Cohort=1 THEN 'High priority' ELSE 'Standard' END AS Priority,
       COUNT(*) AS AffectedOrders,SUM(OrderedAmount) AS OrderedValueExposure,MAX(AgeDays) AS OldestAgeDays
FROM ReportReconciliation WHERE SyncStatus='Awaiting reconciliation' GROUP BY ExceptionType,Priority;

SELECT MonthStart,Category,SUM(UnitsSold) AS UnitsSold,SUM(UnitsReturned) AS UnitsReturned,
       SUM(NetSales) AS NetSales,SUM(GrossProfit)/NULLIF(SUM(NetSales),0) AS GrossMargin
FROM ReportProduct GROUP BY MonthStart,Category ORDER BY MonthStart,Category;
