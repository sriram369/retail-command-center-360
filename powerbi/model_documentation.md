# Semantic model configuration
## Compact browser model
Import the ten Excel **tables**, not both tables and worksheets. The exporter may append numbers to native table names.
Rename the Power Query queries to DimChannel, DimDate, DimLocation, DimProduct, ReportCategory,
ReportFinance, ReportInventory, ReportPurchasing, ReportReconciliation and ReportSystems.
Use single-direction 1:* relationships, unique dimension keys on the 1 side:

| Dimension key | Fact key | Active |
|---|---|---|
| DimDate.Date | ReportFinance.MonthStart | Yes |
| DimDate.Date | ReportCategory.MonthStart | Yes |
| DimDate.Date | ReportSystems.MonthStart | Yes |
| DimLocation.LocationId | ReportFinance.LocationId | Yes |
| DimChannel.ChannelId | ReportFinance.ChannelId | Yes |
| DimLocation.LocationId | ReportInventory.LocationId | Yes |
| DimProduct.ProductId | ReportInventory.ProductId | Yes |
| DimProduct.ProductId | ReportPurchasing.ProductId | Yes |
| DimLocation.LocationId | ReportReconciliation.LocationId | Yes |

Do not connect DimDate to ReportInventory or ReportReconciliation: these are current snapshots.
ReportCategory is companywide by month/category. Channel/location selections do not apply to that chart; title it accordingly.
Disable automatically created fact-to-fact relationships. Do not connect dimensions on names.
Date and MonthStart are Date types. IDs and count flags are whole numbers. Currency uses fixed decimal where two decimals suffice,
but preserve four-decimal inventory/COGS precision before formatting. All percentages are measures, never summed row percentages.
Hide technical IDs, Cohort, SnapshotId, ScenarioAffected, Synthetic and duplicated lookup fields.
Mark DimDate as the date table using Date. Set Month sort by MonthStart where the same month key maps to one start date.

## Full-detail extension
Import the raw dimension tables and FactSalesTransactions, FactBudget, FactInventorySnapshots,
FactInventoryMovements and FactIntegrationEvents plus processed ReportOrders, ReportTickets,
ReportPurchasing, ReportReconciliation, ReportInventory, ReportOrderLines and ReportDailyInventory.
Use DimDate.Date to SalesTransactions.PostingDate, Budget.MonthStart, InventorySnapshots.SnapshotDate,
InventoryMovements.MovementDate, IntegrationEvents.EventDate, ReportOrders.OrderDate, ReportOrderLines.OrderDate and DailyInventory.BalanceDate.
For ReportTickets create an OpenDate of type Date from OpenedAt in Power Query and relate to DimDate.Date.
Use common ProductId, LocationId, ChannelId and CustomerId dimension keys directly on each applicable fact.
Raw order headers/lines, shipments, ERP links and returns may stay as disabled-load audit queries; the report uses derived facts to avoid join multiplication.
No many-to-many or bidirectional filters are required. Use inactive relationships/role date tables only for explicitly separate date roles.
Historical inventory averages in ReportDailyInventory are companywide. Do not filter their ratio by product or location without building daily balances at that grain.

## Grain checks
ReportFinance: unique month/channel/location, including one monthly budget. ReportCategory: month/category.
ReportInventory: exactly one cutoff/SKU/location. ReportSystems: month of events and ticket-open cohort.
ReportOrders: one order. ReportReconciliation: one noncanceled source commerce order. ReportTickets: one incident.

## Actual saved browser model
The imported aliases are DimDate7, DimChannel8, DimLocation9, DimProduct10,
ReportFinance, ReportCategory, ReportInventory, ReportSystems, ReportPurchasing5, ReportReconciliation6,
ReportFulfillment1, ReportDailyFinance2, ReportDailyInventory3, ReportTickets4, ReportProduct5 and _Measures.
The native TMDL scripts intentionally use these exact names. Do not rename aliases before replaying those scripts.
The original unsuffixed names in the full CSV model use separate detail-model DAX definitions.
ReportProduct5 numeric fields NetSales, COGS, GrossProfit are Decimal number; ProductId, UnitsSold and UnitsReturned are Whole number; MonthStart is Date.
Inspect every imported type; Excel source numeric cells are typed, but web inference can still produce text.
Additional relationships use Date to fulfillment MonthStart, daily finance PostingDate, daily inventory BalanceDate,
ticket OpenDate and product MonthStart; product ProductId and fulfillment ChannelId/LocationId use their dimensions.
Both TMDL relationship scripts use default many-to-one, single-direction filtering; no fact-to-fact relationships.
After metadata changes, use Home > Queries > Refresh to recalculate imported relationship data, then refresh report visuals.
The supplemental daily facts support historical averages, not a sum of snapshots. Ratio guards blank under company-dimension filters.
