CREATE INDEX ix_move_date ON FactInventoryMovements(LocationId,ProductId,MovementDate);

CREATE UNIQUE INDEX ix_order ON FactSalesOrders(OrderId);

CREATE INDEX ix_sales_date ON FactSalesTransactions(PostingDate);

CREATE TABLE "DimChannel" (
"ChannelId" INTEGER,
  "Channel" TEXT
);

CREATE TABLE "DimCustomer" (
"CustomerId" INTEGER,
  "CustomerCode" TEXT,
  "Segment" TEXT,
  "State" TEXT,
  "Synthetic" INTEGER
);

CREATE TABLE "DimDate" (
"Date" TEXT,
  "Year" INTEGER,
  "MonthNumber" INTEGER,
  "Month" TEXT,
  "MonthStart" TEXT,
  "Quarter" TEXT,
  "DayOfWeek" TEXT
);

CREATE TABLE "DimLocation" (
"LocationId" INTEGER,
  "LocationName" TEXT,
  "LocationType" TEXT,
  "State" TEXT
);

CREATE TABLE "DimProduct" (
"ProductId" INTEGER,
  "SKU" TEXT,
  "ProductName" TEXT,
  "Category" TEXT,
  "SupplierId" INTEGER,
  "RetailPrice" REAL,
  "OpeningUnitCost" REAL,
  "Customizable" INTEGER
);

CREATE TABLE "DimStore" (
"StoreId" INTEGER,
  "StoreName" TEXT,
  "City" TEXT,
  "State" TEXT
);

CREATE TABLE "DimSupplier" (
"SupplierId" INTEGER,
  "SupplierName" TEXT,
  "StandardLeadDays" INTEGER,
  "Terms" TEXT
);

CREATE TABLE "FactBudget" (
"BudgetId" INTEGER,
  "MonthStart" TEXT,
  "ChannelId" INTEGER,
  "LocationId" INTEGER,
  "SalesBudget" REAL
);

CREATE TABLE "FactERPOrderLinks" (
"ERPLinkId" INTEGER,
  "OrderId" INTEGER,
  "ERPOrderId" TEXT,
  "SyncedDate" TEXT
);

CREATE TABLE "FactIntegrationEvents" (
"EventId" INTEGER,
  "OrderId" INTEGER,
  "EventDate" TEXT,
  "SourceSystem" TEXT,
  "EventType" TEXT,
  "Status" TEXT,
  "BusinessKey" TEXT,
  "PayloadSKU" TEXT,
  "Deduplicated" INTEGER
);

CREATE TABLE "FactInventoryMovements" (
"MovementId" INTEGER,
  "MovementDate" TEXT,
  "LocationId" INTEGER,
  "ProductId" INTEGER,
  "MovementType" TEXT,
  "QuantityChange" INTEGER,
  "ValueChange" REAL,
  "ReferenceType" TEXT,
  "ReferenceId" TEXT,
  "TransferId" TEXT
);

CREATE TABLE "FactInventorySnapshots" (
"SnapshotId" INTEGER,
  "SnapshotDate" TEXT,
  "LocationId" INTEGER,
  "ProductId" INTEGER,
  "UnitsOnHand" INTEGER,
  "InventoryValue" REAL,
  "WeightedAverageCost" REAL
);

CREATE TABLE "FactPurchaseOrders" (
"PurchaseOrderId" INTEGER,
  "PONumber" TEXT,
  "ProductId" INTEGER,
  "SupplierId" INTEGER,
  "LocationId" INTEGER,
  "PODate" TEXT,
  "ApprovalDate" TEXT,
  "PromisedReceiptDate" TEXT,
  "ReceivedDate" TEXT,
  "Quantity" INTEGER,
  "UnitCost" REAL,
  "POAmount" REAL,
  "ApprovalDays" INTEGER,
  "POStatus" TEXT,
  "ScenarioAffected" INTEGER
);

CREATE TABLE "FactReturns" (
"ReturnId" TEXT,
  "OrderId" INTEGER,
  "OrderLineId" INTEGER,
  "ReturnDate" TEXT,
  "ProductId" INTEGER,
  "LocationId" INTEGER,
  "ChannelId" INTEGER,
  "CustomerId" INTEGER,
  "Quantity" INTEGER,
  "RefundAmount" REAL,
  "CostReversal" REAL,
  "Reason" TEXT,
  "Disposition" TEXT
);

CREATE TABLE "FactSalesOrderLines" (
"OrderLineId" INTEGER,
  "OrderId" INTEGER,
  "ProductId" INTEGER,
  "Quantity" INTEGER,
  "UnitPrice" REAL,
  "DiscountAmount" REAL,
  "OrderedAmount" REAL
);

CREATE TABLE "FactSalesOrders" (
"OrderId" INTEGER,
  "OrderNumber" TEXT,
  "OrderDate" TEXT,
  "CustomerId" INTEGER,
  "ChannelId" INTEGER,
  "LocationId" INTEGER,
  "PromisedDate" TEXT,
  "OrderStatus" TEXT,
  "PaymentStatus" TEXT,
  "IntegrationIssue" TEXT,
  "AvailableDate" TEXT,
  "Cohort" INTEGER
);

CREATE TABLE "FactSalesTransactions" (
"SalesTransactionId" INTEGER,
  "PostingDate" TEXT,
  "OrderId" INTEGER,
  "OrderLineId" INTEGER,
  "ProductId" INTEGER,
  "LocationId" INTEGER,
  "ChannelId" INTEGER,
  "CustomerId" INTEGER,
  "TransactionType" TEXT,
  "Quantity" INTEGER,
  "NetAmount" REAL,
  "COGS" REAL,
  "DiscountAmount" REAL
);

CREATE TABLE "FactShipments" (
"ShipmentId" INTEGER,
  "OrderId" INTEGER,
  "ShipDate" TEXT,
  "LocationId" INTEGER,
  "OrderDate" TEXT,
  "ChannelId" INTEGER,
  "PromisedDate" TEXT,
  "FulfillmentDays" INTEGER,
  "IsLate" INTEGER
);

CREATE TABLE "FactSupportTickets" (
"TicketId" INTEGER,
  "OrderId" INTEGER,
  "OpenedAt" TEXT,
  "ResolvedAt" TEXT,
  "SLADeadline" TEXT,
  "Category" TEXT,
  "Severity" TEXT,
  "Status" TEXT,
  "Owner" TEXT,
  "RepeatKey" TEXT,
  "ResolutionHours" TEXT,
  "SLAEligible" INTEGER,
  "SLAMet" INTEGER
);

CREATE TABLE "InjectedAnomalies" (
"AnomalyId" INTEGER,
  "Scenario" TEXT,
  "Entity" TEXT,
  "EntityId" INTEGER,
  "Issue" TEXT,
  "StartDate" TEXT,
  "Cohort" INTEGER
);

CREATE TABLE "ReportCategory" (
"MonthStart" TEXT,
  "Category" TEXT,
  "NetSales" REAL,
  "COGS" REAL,
  "UnitsSold" INTEGER,
  "UnitsReturned" INTEGER,
  "DiscountAmount" REAL,
  "GrossProfit" REAL
);

CREATE TABLE "ReportDailyFinance" (
"PostingDate" TEXT,
  "NetSales" REAL,
  "COGS" REAL
);

CREATE TABLE "ReportDailyInventory" (
"BalanceDate" TEXT,
  "QuantityChange" INTEGER,
  "ValueChange" REAL,
  "UnitsOnHand" INTEGER,
  "InventoryValue" REAL
);

CREATE TABLE "ReportFinance" (
"MonthStart" TEXT,
  "ChannelId" INTEGER,
  "LocationId" INTEGER,
  "NetSales" REAL,
  "COGS" REAL,
  "SalesBeforeReturns" REAL,
  "RefundAmount" REAL,
  "UnitsSold" INTEGER,
  "UnitsReturned" INTEGER,
  "DiscountAmount" REAL,
  "FulfilledOrders" INTEGER,
  "SalesBudget" REAL,
  "GrossProfit" REAL,
  "Channel" TEXT,
  "LocationName" TEXT
);

CREATE TABLE "ReportFulfillment" (
"MonthStart" TEXT,
  "ChannelId" INTEGER,
  "LocationId" INTEGER,
  "EligibleOrders" INTEGER,
  "FulfilledOrders" INTEGER,
  "LateOrders" INTEGER,
  "OpenLateOrders" INTEGER,
  "FulfillmentDays" INTEGER
);

CREATE TABLE "ReportInventory" (
"SnapshotId" INTEGER,
  "SnapshotDate" TEXT,
  "LocationId" INTEGER,
  "ProductId" INTEGER,
  "UnitsOnHand" INTEGER,
  "InventoryValue" REAL,
  "WeightedAverageCost" REAL,
  "DailyDemand" REAL,
  "BackorderUnits" REAL,
  "AvailableUnits" REAL,
  "SKU" TEXT,
  "ProductName" TEXT,
  "Category" TEXT,
  "SupplierId" INTEGER,
  "RetailPrice" REAL,
  "OpeningUnitCost" REAL,
  "Customizable" INTEGER,
  "LocationName" TEXT,
  "LocationType" TEXT,
  "State" TEXT,
  "StandardLeadDays" INTEGER,
  "ProtectionDays" INTEGER,
  "ReorderPoint" INTEGER,
  "StockoutRisk" INTEGER,
  "LowStock" INTEGER,
  "DaysCover" REAL,
  "ExcessUnits" INTEGER,
  "RecommendedUnits" INTEGER,
  "WarehouseAvailable" REAL,
  "Action" TEXT
);

CREATE TABLE "ReportOrderLines" (
"OrderLineId" INTEGER,
  "OrderId" INTEGER,
  "ProductId" INTEGER,
  "Quantity" INTEGER,
  "UnitPrice" REAL,
  "DiscountAmount" REAL,
  "OrderedAmount" REAL,
  "OrderNumber" TEXT,
  "OrderDate" TEXT,
  "CustomerId" INTEGER,
  "ChannelId" INTEGER,
  "LocationId" INTEGER,
  "PromisedDate" TEXT,
  "OrderStatus" TEXT,
  "PaymentStatus" TEXT,
  "IntegrationIssue" TEXT,
  "AvailableDate" TEXT,
  "Cohort" INTEGER
);

CREATE TABLE "ReportOrders" (
"OrderId" INTEGER,
  "OrderNumber" TEXT,
  "OrderDate" TEXT,
  "CustomerId" INTEGER,
  "ChannelId" INTEGER,
  "LocationId" INTEGER,
  "PromisedDate" TEXT,
  "OrderStatus" TEXT,
  "PaymentStatus" TEXT,
  "IntegrationIssue" TEXT,
  "AvailableDate" TEXT,
  "Cohort" INTEGER,
  "ShipDate" TEXT,
  "FulfillmentDays" INTEGER,
  "IsLate" TEXT,
  "EligibleOrder" INTEGER,
  "FulfilledOrder" INTEGER,
  "OpenLateOrder" INTEGER,
  "LateOrder" INTEGER
);

CREATE TABLE "ReportProduct" (
"MonthStart" TEXT,
  "ProductId" INTEGER,
  "SKU" TEXT,
  "ProductName" TEXT,
  "Category" TEXT,
  "NetSales" REAL,
  "COGS" REAL,
  "UnitsSold" INTEGER,
  "UnitsReturned" INTEGER,
  "GrossProfit" REAL
);

CREATE TABLE "ReportPurchasing" (
"PurchaseOrderId" INTEGER,
  "PONumber" TEXT,
  "ProductId" INTEGER,
  "SupplierId" INTEGER,
  "LocationId" INTEGER,
  "PODate" TEXT,
  "ApprovalDate" TEXT,
  "PromisedReceiptDate" TEXT,
  "ReceivedDate" TEXT,
  "Quantity" INTEGER,
  "UnitCost" REAL,
  "POAmount" REAL,
  "ApprovalDays" INTEGER,
  "POStatus" TEXT,
  "ScenarioAffected" INTEGER,
  "LateReceiptDays" REAL,
  "OverdueOpen" INTEGER,
  "SKU" TEXT,
  "ProductName" TEXT,
  "Category" TEXT,
  "SupplierName" TEXT,
  "StandardLeadDays" INTEGER,
  "Terms" TEXT
);

CREATE TABLE "ReportReconciliation" (
"OrderId" INTEGER,
  "OrderNumber" TEXT,
  "OrderDate" TEXT,
  "CustomerId" INTEGER,
  "ChannelId" INTEGER,
  "LocationId" INTEGER,
  "PromisedDate" TEXT,
  "OrderStatus" TEXT,
  "PaymentStatus" TEXT,
  "IntegrationIssue" TEXT,
  "AvailableDate" TEXT,
  "Cohort" INTEGER,
  "ERPOrderId" TEXT,
  "SyncedDate" TEXT,
  "SyncStatus" TEXT,
  "OrderedAmount" REAL,
  "AgeDays" INTEGER,
  "HasEvent" INTEGER,
  "ExceptionType" TEXT
);

CREATE TABLE "ReportSystems" (
"MonthStart" TEXT,
  "SuccessfulEvents" INTEGER,
  "FailedEvents" INTEGER,
  "DuplicateEvents" INTEGER,
  "AttemptedEvents" INTEGER,
  "TicketsOpened" INTEGER,
  "ResolvedTickets" INTEGER,
  "OpenTickets" INTEGER,
  "SLAEligible" INTEGER,
  "SLAMet" INTEGER,
  "ResolutionHours" REAL,
  "RepeatIncidents" INTEGER
);

CREATE TABLE "ReportTickets" (
"TicketId" INTEGER,
  "OrderId" INTEGER,
  "OpenedAt" TEXT,
  "ResolvedAt" TEXT,
  "SLADeadline" TEXT,
  "Category" TEXT,
  "Severity" TEXT,
  "Status" TEXT,
  "Owner" TEXT,
  "RepeatKey" TEXT,
  "ResolutionHours" REAL,
  "SLAEligible" INTEGER,
  "SLAMet" INTEGER,
  "MonthStart" TEXT,
  "ResolvedCount" INTEGER,
  "OpenCount" INTEGER,
  "RepeatIncident" INTEGER,
  "OpenDate" TEXT
);
