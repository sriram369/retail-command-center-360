"""Emit typed Power Query ingestion, DAX definitions and precise report configuration."""
import json
import pandas as pd
from generate_data import ROOT
from package_docs import write

def prepare():
    write('powerbi/power_query/RootFolder.m','"C:\\Retail360\\retail-command-center-360" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]')
    for folder in ['raw','processed']:
        for p in (ROOT/f'data/{folder}').glob('*.csv'):
            df=pd.read_csv(p,keep_default_na=False);types=[]
            for col in df:
                if col.endswith('At') or col=='SLADeadline':typ='type datetime'
                elif col.endswith('Date') or col in ['Date','MonthStart','BalanceDate']:typ='type date'
                elif pd.api.types.is_integer_dtype(df[col]):typ='Int64.Type'
                elif pd.api.types.is_float_dtype(df[col]):typ='type number'
                else:typ='type text'
                types.append('{"'+col+'", '+typ+'}')
            name=p.stem
            write(f'powerbi/power_query/{name}.m',f'''let
    Source = Csv.Document(File.Contents(RootFolder & "/data/{folder}/{p.name}"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    EmptyToNull = Table.ReplaceValue(Headers, "", null, Replacer.ReplaceValue, Table.ColumnNames(Headers)),
    Typed = Table.TransformColumnTypes(EmptyToNull, {{{', '.join(types)}}}, "en-US")
in
    Typed''')
    write('powerbi/power_query/ReconciliationControl.m','''let
    Expected = Table.SelectRows(FactSalesOrders, each [ChannelId] = 2 and [OrderStatus] <> "Canceled"),
    MissingERP = Table.NestedJoin(Expected, {"OrderId"}, FactERPOrderLinks, {"OrderId"}, "ERP", JoinKind.LeftAnti),
    EventOrders = Table.Distinct(Table.SelectColumns(FactIntegrationEvents, {"OrderId"})),
    EventFlag = Table.AddColumn(EventOrders, "HasEvent", each 1, Int64.Type),
    WithEvent = Table.NestedJoin(MissingERP, {"OrderId"}, EventFlag, {"OrderId"}, "Event", JoinKind.LeftOuter),
    Expanded = Table.ExpandTableColumn(WithEvent, "Event", {"HasEvent"}),
    Filled = Table.ReplaceValue(Expanded, null, 0, Replacer.ReplaceValue, {"HasEvent"})
in
    Filled''')
    dax={
      'Net Sales':'SUM(FactSalesTransactions[NetAmount])',
      'COGS':'SUM(FactSalesTransactions[COGS])',
      'Gross Profit':'[Net Sales] - [COGS]',
      'Gross Margin %':'DIVIDE([Gross Profit], [Net Sales])',
      'Previous Period Sales':'CALCULATE([Net Sales], DATEADD(DimDate[Date], -1, MONTH))',
      'Sales Growth %':'DIVIDE([Net Sales] - [Previous Period Sales], [Previous Period Sales])',
      'Prior Year Sales':'CALCULATE([Net Sales], SAMEPERIODLASTYEAR(DimDate[Date]))',
      'Sales Growth YoY %':'DIVIDE([Net Sales] - [Prior Year Sales], [Prior Year Sales])',
      'Sales Budget':'IF(ISFILTERED(DimProduct), BLANK(), SUM(FactBudget[SalesBudget]))',
      'Budget Variance':'IF(NOT ISBLANK([Sales Budget]), [Net Sales] - [Sales Budget])',
      'Budget Variance %':'DIVIDE([Budget Variance], [Sales Budget])',
      'Units Sold':'CALCULATE(SUM(FactSalesTransactions[Quantity]), FactSalesTransactions[TransactionType] = "Sale")',
      'Units Returned':'-CALCULATE(SUM(FactSalesTransactions[Quantity]), FactSalesTransactions[TransactionType] = "Return")',
      'Return Rate':'DIVIDE([Units Returned], [Units Sold])',
      'Shipped Orders':'CALCULATE(DISTINCTCOUNT(FactSalesTransactions[OrderId]), FactSalesTransactions[TransactionType] = "Sale")',
      'Average Order Value':'DIVIDE([Net Sales], [Shipped Orders])',
      'Ordered Revenue':'CALCULATE(SUM(ReportOrderLines[OrderedAmount]), ReportOrderLines[OrderStatus] <> "Canceled")',
      'Inventory Value':'''VAR AsOfDate = MAX(DimDate[Date])
VAR SnapshotDate = CALCULATE(MAX(FactInventorySnapshots[SnapshotDate]), REMOVEFILTERS(DimDate), FactInventorySnapshots[SnapshotDate] <= AsOfDate)
RETURN IF(NOT ISBLANK(SnapshotDate), CALCULATE(SUM(FactInventorySnapshots[InventoryValue]), REMOVEFILTERS(DimDate), FactInventorySnapshots[SnapshotDate] = SnapshotDate))''',
      'Units On Hand':'''VAR AsOfDate = MAX(DimDate[Date])
VAR SnapshotDate = CALCULATE(MAX(FactInventorySnapshots[SnapshotDate]), REMOVEFILTERS(DimDate), FactInventorySnapshots[SnapshotDate] <= AsOfDate)
RETURN IF(NOT ISBLANK(SnapshotDate), CALCULATE(SUM(FactInventorySnapshots[UnitsOnHand]), REMOVEFILTERS(DimDate), FactInventorySnapshots[SnapshotDate] = SnapshotDate))''',
      'Current Inventory Value':'SUM(ReportInventory[InventoryValue])',
      'Stockout Risk Count':'SUM(ReportInventory[StockoutRisk])',
      'Low Stock SKU Count':'SUM(ReportInventory[LowStock])',
      'Eligible Orders':'SUM(ReportOrders[EligibleOrder])',
      'Fulfilled Orders':'SUM(ReportOrders[FulfilledOrder])',
      'Fulfillment Rate':'DIVIDE([Fulfilled Orders], [Eligible Orders])',
      'Late Orders':'SUM(ReportOrders[LateOrder])',
      'Open Late Orders':'SUM(ReportOrders[OpenLateOrder])',
      'Average Fulfillment Duration':'DIVIDE(SUM(ReportOrders[FulfillmentDays]), [Fulfilled Orders])',
      'Pending Purchase Orders':'CALCULATE(COUNTROWS(ReportPurchasing), ReportPurchasing[POStatus] <> "Received")',
      'Integration Attempts':'CALCULATE(COUNTROWS(FactIntegrationEvents), FactIntegrationEvents[Status] IN {"Success", "Failed"})',
      'Failed Integration Events':'CALCULATE(COUNTROWS(FactIntegrationEvents), FactIntegrationEvents[Status] = "Failed")',
      'Integration Failure Rate':'DIVIDE([Failed Integration Events], [Integration Attempts])',
      'Integration Success Rate':'DIVIDE([Integration Attempts] - [Failed Integration Events], [Integration Attempts])',
      'Ignored Duplicate Events':'CALCULATE(COUNTROWS(FactIntegrationEvents), FactIntegrationEvents[Deduplicated] = 1)',
      'Orders Awaiting Reconciliation':'CALCULATE(COUNTROWS(ReportReconciliation), ReportReconciliation[SyncStatus] = "Awaiting reconciliation")',
      'Data Quality Exceptions':'CALCULATE(COUNTROWS(ReportReconciliation), ReportReconciliation[SyncStatus] = "Awaiting reconciliation", ReportReconciliation[ExceptionType] IN {"Missing webhook", "SKU mapping"})',
      'Order Value Awaiting Reconciliation':'CALCULATE(SUM(ReportReconciliation[OrderedAmount]), ReportReconciliation[SyncStatus] = "Awaiting reconciliation")',
      'Open Support Tickets':'SUM(ReportTickets[OpenCount])',
      'SLA Compliance Rate':'DIVIDE(SUM(ReportTickets[SLAMet]), SUM(ReportTickets[SLAEligible]))',
      'Mean Time to Resolution':'DIVIDE(SUM(ReportTickets[ResolutionHours]), SUM(ReportTickets[ResolvedCount]))',
      'Repeat Incidents':'SUM(ReportTickets[RepeatIncident])',
      'High-Priority Exceptions':'CALCULATE(COUNTROWS(ReportReconciliation), ReportReconciliation[SyncStatus] = "Awaiting reconciliation", ReportReconciliation[Cohort] = 1)',
      'Average Inventory Value 90D':'''VAR EndDate = MAX(DimDate[Date])
VAR DataStartDate = CALCULATE(MIN(DimDate[Date]), REMOVEFILTERS(DimDate))
RETURN IF(EndDate - 89 >= DataStartDate && NOT ISFILTERED(DimProduct) && NOT ISFILTERED(DimLocation), CALCULATE(AVERAGE(ReportDailyInventory[InventoryValue]), REMOVEFILTERS(DimDate), DATESBETWEEN(DimDate[Date], EndDate - 89, EndDate)))''',
      'COGS 90D':'''VAR EndDate = MAX(DimDate[Date])
RETURN CALCULATE([COGS], REMOVEFILTERS(DimDate), DATESBETWEEN(DimDate[Date], EndDate - 89, EndDate))''',
      'Inventory Turnover 90D Annualized':'DIVIDE([COGS 90D], [Average Inventory Value 90D]) * 365 / 90',
      'Days of Inventory on Hand':'DIVIDE([Average Inventory Value 90D], [COGS 90D]) * 90'}
    write('powerbi/dax_measures/detail_model.dax','\n\n'.join(f'// Create as an individual measure.\n{name} =\n{expr}' for name,expr in dax.items()))
    # Compact workbook queries can be renamed after import. These expressions assume suffixes removed.
    compact={'Net Sales':'SUM(ReportFinance[NetSales])','COGS':'SUM(ReportFinance[COGS])',
      'Gross Profit':'[Net Sales] - [COGS]','Gross Margin %':'DIVIDE([Gross Profit], [Net Sales])',
      'Sales Budget':'SUM(ReportFinance[SalesBudget])','Budget Variance':'[Net Sales] - [Sales Budget]',
      'Budget Variance %':'DIVIDE([Budget Variance], [Sales Budget])',
      'Previous Period Sales':'CALCULATE([Net Sales], DATEADD(DimDate[Date], -1, MONTH))',
      'Sales Growth %':'DIVIDE([Net Sales] - [Previous Period Sales], [Previous Period Sales])',
      'Units Sold':'SUM(ReportFinance[UnitsSold])','Return Rate':'DIVIDE(SUM(ReportFinance[UnitsReturned]), [Units Sold])',
      'Average Order Value':'DIVIDE([Net Sales], SUM(ReportFinance[FulfilledOrders]))',
      'Current Inventory Value':'SUM(ReportInventory[InventoryValue])','Stockout Risk Count':'SUM(ReportInventory[StockoutRisk])',
      'Units On Hand':'SUM(ReportInventory[UnitsOnHand])',
      'Integration Success Rate':'DIVIDE(SUM(ReportSystems[SuccessfulEvents]), SUM(ReportSystems[AttemptedEvents]))',
      'Failed Integration Events':'SUM(ReportSystems[FailedEvents])',
      'SLA Compliance Rate':'DIVIDE(SUM(ReportSystems[SLAMet]), SUM(ReportSystems[SLAEligible]))',
      'Mean Time to Resolution':'DIVIDE(SUM(ReportSystems[ResolutionHours]), SUM(ReportSystems[ResolvedTickets]))',
      'Orders Awaiting Reconciliation':'CALCULATE(COUNTROWS(ReportReconciliation), ReportReconciliation[SyncStatus] = "Awaiting reconciliation")',
      'Pending Purchase Orders':'CALCULATE(COUNTROWS(ReportPurchasing), ReportPurchasing[POStatus] <> "Received")'}
    write('powerbi/dax_measures/browser_model.dax','\n\n'.join(f'{name} =\n{expr}' for name,expr in compact.items()))
    native={n:e.replace('DimDate[','DimDate7[').replace('ReportPurchasing','ReportPurchasing5').replace('ReportReconciliation','ReportReconciliation6') for n,e in compact.items()}
    native.update({'Gross Margin Q3 2026':'DIVIDE([Gross Profit Q3 2026], [Net Sales Q3 2026])',
      'Net Sales Q3 2026':'CALCULATE([Net Sales], REMOVEFILTERS(DimDate7), ReportFinance[MonthStart] >= DATE(2026,7,1), ReportFinance[MonthStart] <= DATE(2026,9,1))',
      'Gross Profit Q3 2026':'CALCULATE([Gross Profit], REMOVEFILTERS(DimDate7), ReportFinance[MonthStart] >= DATE(2026,7,1), ReportFinance[MonthStart] <= DATE(2026,9,1))',
      'Net Sales Q3 2025':'CALCULATE([Net Sales], REMOVEFILTERS(DimDate7), ReportFinance[MonthStart] >= DATE(2025,7,1), ReportFinance[MonthStart] <= DATE(2025,9,1))',
      'Gross Margin Q3 2025':'CALCULATE([Gross Margin %], REMOVEFILTERS(DimDate7), ReportFinance[MonthStart] >= DATE(2025,7,1), ReportFinance[MonthStart] <= DATE(2025,9,1))',
      'Q3 Sales Growth YoY':'DIVIDE([Net Sales Q3 2026] - [Net Sales Q3 2025], [Net Sales Q3 2025])',
      'Q3 Margin Change pp':'([Gross Margin Q3 2026] - [Gross Margin Q3 2025]) * 100',
      'Category Gross Margin %':'DIVIDE(SUM(ReportCategory[GrossProfit]), SUM(ReportCategory[NetSales]))',
      'Open Support Tickets':'SUM(ReportSystems[OpenTickets])','Ignored Duplicate Events':'SUM(ReportSystems[DuplicateEvents])',
      'Repeat Incidents':'SUM(ReportSystems[RepeatIncidents])',
      'Data Quality Exceptions':'CALCULATE(COUNTROWS(ReportReconciliation6), ReportReconciliation6[SyncStatus] = "Awaiting reconciliation", ReportReconciliation6[ExceptionType] IN {"Missing webhook", "SKU mapping"})',
      'Order Value Awaiting Reconciliation':'CALCULATE(SUM(ReportReconciliation6[OrderedAmount]), ReportReconciliation6[SyncStatus] = "Awaiting reconciliation")',
      'Integration Failure Rate':'DIVIDE(SUM(ReportSystems[FailedEvents]), SUM(ReportSystems[AttemptedEvents]))'})
    tm=['createOrReplace','', '\ttable _Measures','\t\tcolumn _Anchor','\t\t\tdataType: int64','\t\t\tisHidden','\t\t\tsourceColumn: [_Anchor]',
        '\t\tpartition _Measures = calculated','\t\t\tmode: import','\t\t\tsource = ROW("_Anchor", 1)']
    for n,e in native.items():
        fmt='0.0%' if ('Rate' in n or '%' in n or 'Growth' in n or 'Gross Margin Q3' in n) else ('0.00' if ('pp' in n or 'Time' in n) else ('"$"#,##0' if any(w in n for w in ['Sales','COGS','Profit','Budget','Value','Revenue']) else '#,##0'))
        tm.extend(['',f"\t\tmeasure '{n}' = {e}",f'\t\t\tformatString: {fmt}','\t\t\tdisplayFolder: Retail360'])
    write('powerbi/browser_measures.tmdl','\n'.join(tm))
    write('powerbi/dax_measures/README.md','''# Measure definitions and verification
`detail_model.dax` is for the detailed CSV semantic model. `browser_model.dax` is for the compact Excel tables.
Create each definition as a separate measure; these files are not an executable DAX query or an auto-import project.
Remove generated table-name suffixes after workbook import, or update the expression table names to match.
Use a marked date table and the relationships in model_documentation.md. Percentages use 0.0%, currency $#,##0, and durations 0.0.

Important controls are independently calculated in Python and SQLite and recorded in reports/kpi_controls.json.
Python/SQL parity is not DAX engine execution. Native compilation, filter behavior and saved-report checks are recorded in reports/powerbi_status.md.
Previous Period Sales means previous month. Select one complete month for month-on-month comparisons.
Only compare prior years where the complete corresponding dates exist. Q3 2025 and Q3 2026 are complete.
Inventory Value is semi-additive and chooses the last available month-end at/before the selected date.
No prior month-end exists for early April 2025; that historical snapshot measure returns blank.
Trailing-90-day inventory metrics require 90 complete days and use daily historical total balances.
They are companywide: the daily total table has no SKU or location grain. Hide/blank these metrics under product/location filtering.
Ordered Revenue uses the enriched ReportOrderLines fact, excludes canceled orders and uses the source order date.
It is not a posted-sales measure and must be labeled separately.
Current risk and reconciliation measures are cutoff snapshots with historical date interactions disabled.
''')
    write('powerbi/model_documentation.md','''# Semantic model configuration
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
''')
    write('powerbi/build_guide.md','''# Reproduce the Power BI report
## Browser path
Open app.powerbi.com with an account that permits report authoring. Create a report from an Excel workbook, choose Upload file,
and select data/retail360_powerbi.xlsx. An organizational OneDrive upload may be used by Power Query.
In Navigator select the ten Excel tables once. Use Transform data to inspect types and rename generated suffixes.
Create an Import semantic model named Retail Command Center 360. Add the relationships in model_documentation.md.
Create the compact DAX measures individually, then build the three pages from page_specifications.md.
Save, reopen and compare totals with reports/kpi_controls.json. Tenant policies may restrict web model editing or themes.

## Desktop path
Power BI Desktop requires a supported Windows environment. On a Mac, continue in the browser or use access to an existing Windows environment.
Use the workbook for the compact model, or the CSV/M queries for the full model. Create a RootFolder parameter pointing at the project folder.
Paste each needed .m query into a blank query. Configure relationships, mark the date table and add the appropriate DAX definitions.
Import theme.json using the report theme controls. Set the 16:9 canvas and apply the page specifications.

## Workbook regeneration
The analytical pipeline creates CSVs, SQLite and reports/workbook_payload.json without an Excel engine.
The supplied workbook was authored with @oai/artifact-tool. With that package available to Node, run `node scripts/build_workbook.mjs`.
If it is unavailable, import the processed CSV tables directly in Desktop, or create equivalent Excel tables from those CSVs.
Do not claim the workbook contains a prebuilt Power Pivot model or native report.

## Validation checklist
- All-period compact Net Sales: 6,626,438.21. COGS: 2,725,435.5507. Gross Profit: 3,901,002.6593.
- Budget: 5,037,225.00. Inventory value at cutoff: 1,913,202.6724. Units on hand: 42,460.
- Failed integration attempts: 355. Ignored duplicates: 306. Unreconciled orders: 28.
- SLA compliance: 132 / 259 = 50.9653%. MTTR: 60.7835 hours for resolved tickets.
- Confirm a month filter, a channel filter, no double imported data and no current snapshot distortion.
- Save and reopen all three pages. Capture actual report screenshots separately from labeled previews.

The current native build state is documented in reports/powerbi_status.md. No PBIX/PBIP file is fabricated.
''')
    write('powerbi/page_specifications.md','''# Three-page report specification
Common canvas: 1600×900. Margin 48, gutter 24. Header y=24–108, KPI row y=128–252.
Charts y=280–570. Detail/action area y=594–828. Cutoff/disclosure footer y=850.
Use native visuals, Segoe UI, navy titles, teal actuals, amber budget, muted red adverse values.
KPI cards: x=48,430,812,1194; width=358, height=124. Main panels: x=48 width=976 and x=1048 width=504.
Keep chart titles and axis units visible. Every risk color has a text label. Default charts are sorted logically, not by autogenerated totals.

## 01 Executive performance
Headline: Sales are growing. Margin needs attention.
Cards: Net Sales, Gross Profit, Gross Margin %, Budget Variance %.
Main combo/trend: MonthStart; Net Sales and Sales Budget in USD, companywide. Tooltip: COGS, units, return rate, AOV.
Right bar chart: Channel vs Net Sales. Tooltip: gross margin and budget variance.
Lower-left bar or matrix: category net sales and gross margin, all channels. No category budget allocation.
Lower-right store ranking: LocationName, Net Sales, Gross Margin %, Budget Variance %, Retail channel only.
Additional product detail uses ReportProduct in the full model for top/bottom SKUs; keep off the primary page if crowded.
Action text: CFO and merchandising to review pouch/travel discounts and supplier cost changes.
Month slicer and applicable channel slicer. Use full months only because compact finance grain is monthly.

## 02 Inventory and fulfillment
Headline: Put inventory where demand is.
Cards: Current Inventory Value, Units On Hand, Stockout Risk Count, Pending Purchase Orders.
Main bar: LocationName and InventoryValue at cutoff. Tooltip: units, reserved backlog, at-risk count.
Right chart: open purchasing by supplier or PO status, showing overdue counts; do not sum UnitCost.
Lower exception table: SKU, LocationName, UnitsOnHand, BackorderUnits, DailyDemand, ReorderPoint, Action, RecommendedUnits.
Filter StockoutRisk=1. Sort backlog descending. Current date visible; disable historical date interaction.
Full model secondary detail: Fulfillment Rate, Average Fulfillment Duration, Late Orders, annualized turnover and DOH.
Action text: Inventory lead to validate donor availability; procurement to review delayed receipts.
Inventory recommendation totals are candidates; do not imply each candidate can consume the same warehouse stock simultaneously.

## 03 Systems health
Headline: Reconcile orders before exceptions spread.
Cards: Integration Success Rate, Failed Integration Events, Orders Awaiting Reconciliation, SLA Compliance Rate.
Main trend: MonthStart and FailedEvents, optionally a separate labeled success-rate chart.
Right chart: TicketsOpened / ResolvedTickets by month or categories in full-detail ticket model.
Lower reconciliation table: OrderNumber, OrderDate, ExceptionType, AgeDays, OrderedAmount, SyncStatus.
Filter SyncStatus=Awaiting reconciliation; sort oldest first. Current cutoff visible and unaffected by historical event-month selection.
Secondary metrics: ignored duplicates, MTTR, open tickets, repeated incidents and high-priority exceptions.
Action text: Business systems analyst owns queue; integration owner fixes mapping and confirms safe replay.
For full-detail operational priority matrix use issue type, severity, affected orders and ordered exposure; never present an arbitrary score as measured financial loss.

## Interaction and accessibility acceptance
Page navigation must work by mouse and keyboard. Financial charts respond to their documented dimensions.
Month slicers do not affect cutoff inventory/reconciliation snapshots. Tooltips define date basis and denominators.
Use meaningful alternate text. Validate at normal laptop size; avoid tiny tables or more than seven major visuals per page.
Native drillthrough to a focused order/SKU detail page is a full-model extension, not assumed to exist in the compact three-page report.
''')
    print('Power BI M, DAX and model/build specifications written.')

if __name__=='__main__':prepare()
