# Saved three-page layout
Canvas 1600 x 900. Header/branding above y=170. Native primary card strip x=48,y=188,w=1504,h=124.
Left native chart x=72,y=380,w=928,h=212. Right chart x=1072,y=380,w=456,h=212.
Lower native table x=72,y=680,w=928,h=144. Right action/support panel x=1048,y=634,w=504,h=202.
Theme: Segoe UI, navy/teal/slate/amber on a soft background. Use native cards with currency to two decimals at automatic display units.

## Financial performance
Cards: Net Sales, Gross Profit, Gross Margin %, Budget Variance %.
Left line: DimDate7.Month (raw date column, not automatic hierarchy); Net Sales and Sales Budget.
Right clustered bar: ReportFinance.Channel, Net Sales.
Lower table: ReportCategory.Category, Category Gross Margin %, SUM(ReportCategory.NetSales).
Quarter dropdown: DimDate7.Quarter; x=1184,y=120,w=368,h=54. Select complete quarters.
Category table is companywide and responds to date only; there is no channel budget allocation to products/categories.
Action: review pouch/travel discount depth and supplier cost trends.

## Inventory and fulfillment
Cards: Current Inventory Value, Units On Hand, Stockout Risk Count, Pending Purchase Orders.
Left clustered bar: ReportInventory.LocationName, Current Inventory Value.
Right clustered bar: ReportPurchasing5.Category, Pending Purchase Orders.
Table: ReportInventory SKU, LocationName, UnitsOnHand, BackorderUnits, RecommendedUnits, StockoutRisk. Visual filter SUM(StockoutRisk)>0.
Right lower card: Fulfillment Rate, Late Orders, Average Fulfillment Duration (days), Days of Inventory on Hand (trailing 90 days).
Supporting card x=1072,y=680,w=456,h=144; grid, two columns, value font 20, label font 10 with text wrap.
No historical-date slicer. Current stock stays September 30. Fulfillment covers all available order cohorts; inventory cover is companywide.
Recommended quantities are candidate actions that require donor/availability checks; never execute all automatically.

## Systems health
Cards: Integration Success Rate, Failed Integration Events, Orders Awaiting Reconciliation, SLA Compliance Rate.
Left line: ReportSystems.MonthStart raw column, Failed Integration Events.
Right card: Mean Time to Resolution (hours), Open Support Tickets.
Lower table: ReportReconciliation6.OrderNumber, ExceptionType, AgeDays, OrderedAmount, SyncStatus. Filter SyncStatus=Awaiting reconciliation.
Default current queue has 28 orders and $4,132.66 ordered-value exposure. Do not label it lost revenue.
Action: fix mapping before idempotent replay; assign owners and prevent repeat incidents.

## Interactions and limits
Use native page tabs or the Viewing page list; background navigation labels are branding, not clickable buttons.
Tables and location bars scroll; inspect full CSVs for every row. The financial quarter slicer and snapshot isolation are verified.
Other metrics are available as native measures, SQL outputs or detailed-model definitions. Dedicated native drillthrough/bookmarks are not configured.
