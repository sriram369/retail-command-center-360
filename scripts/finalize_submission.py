"""Add dated native implementation evidence to the reproducible portfolio docs."""
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPORT='https://app.powerbi.com/groups/me/reports/45421c92-9cfc-4bca-ae5d-4f64fcd1b2e3'
MODEL='https://app.powerbi.com/groups/me/modeling/86841f6f-d70b-4947-badc-f2ccb56a93ff/modelView'
def write(name,text): (ROOT/name).write_text(text.strip()+'\n')
def main():
    k=json.loads((ROOT/'reports/kpi_controls.json').read_text())
    write('reports/native_validation.json',json.dumps({
        'captured':'2026-10-27','report_url':REPORT,'native_tables':16,'native_measures':51,'relationships':17,
        'operational_query':{'status':'passed','fulfillment_rate':'0.9970206427','fulfilled_orders':23425,
          'eligible_orders':23495,'late_orders':245,'open_late_orders':23,'average_days':'0.8070864461',
          'days_inventory':'382.7259516304','turnover':'0.9536850021','sla':'0.5096525097',
          'mttr_hours':'60.7834645669','tickets':259,'repeat_incidents':255,'risk_pairs':6},
        'product_query':{'status':'passed','net_sales':6626438.21,'gross_profit':3901002.66,
          'q3_2026_sales':1075281.59,'risk_under_q3_filter':6,'inventory_under_q3_filter':1913202.67},
        'observed_ui_checks':['Three saved pages reopened and navigated in viewing mode',
          'Q3 2026 slicer: net sales 1,075,281.59; gross margin 56.9%; budget variance 18.4%',
          'Finance filter cleared to all dates',
          'Inventory exception table filtered to stockout risk > 0',
          'Reconciliation table filtered to 28 awaiting orders; exposure 4,132.66'],
        'limitations':['No configured native order/SKU drillthrough page','No scheduled refresh or real vendor connection',
          'Additional detailed charts are supplied as SQL outputs and build specifications',
          'Browser PDF export initiated but its downloaded file was not retained; portfolio PDF uses identified browser captures']
    },indent=2))
    write('reports/powerbi_status.md',f'''# Power BI implementation evidence
Captured October 27, 2026. The native three-page executive report is saved in Power BI Service.

[Open report]({REPORT}) · [Open semantic model]({MODEL})
Links require the owner's account or separately granted access. No public sharing was configured.

## Built and observed
- Three 1600 x 900 pages: Financial Performance, Inventory & Fulfillment, Systems Health.
- Sixteen imported/calculated tables, 51 native DAX measures, 17 single-direction dimension relationships.
- Custom navy/teal theme, branded backgrounds, native cards, charts, tables and a financial quarter slicer.
- Supplemental fulfillment, daily historical inventory/COGS, product and ticket facts imported through Power Query.
- Product numeric/date types corrected and product sales/GP checked in the DAX engine.
- Ten initial headline controls checked; thirteen operational values matched independent controls to ten decimal places where shown.
- Five further product and date-isolation controls passed. Q3 2026 sales were $1,075,281.59 while current risk stayed 6 and inventory stayed $1,913,202.67.
- Q3 2026 slicer test: margin 56.9%, budget variance 18.4%. Cleared to all dates afterward.
- Current risk table filtered to positive risk; reconciliation queue filtered to 28 awaiting orders, $4,132.66 exposure.
- All three saved pages reopened in viewing mode and inspected with no erroneous visuals.

Native screenshots: [Finance](../visuals/screenshots/01_financial_native.jpg), [Inventory](../visuals/screenshots/02_inventory_native.jpg), [Systems](../visuals/screenshots/03_systems_native.jpg).
[Operational DAX evidence](../visuals/screenshots/operations_dax_validation.jpg) and [machine-readable observations](native_validation.json).

## Scope and practical limits
The three main pages deliberately prioritize executive decisions. Additional store/product rankings, source-system,
ticket category/severity, SLA trend and priority-matrix analyses are supplied as executable SQL and CSV results.
See the detail visual build specification. Native drillthrough, bookmarks, automated refresh, deployed RLS and live vendor integrations are not configured.
Finance category totals are all-channel monthly aggregates; channel selections do not filter that table.
Inventory and reconciliation are cutoff snapshots and have no active historical-date relationship.
Trailing inventory ratios are companywide; product/location/channel filters return blank.
Native tables may scroll. A PDF is a snapshot and cannot expose offscreen exception rows; full queues are included as CSV.
The Power BI PDF export was initiated; no completed download was retained. The separate portfolio brief assembles explicitly identified native browser captures.
No PBIX/PBIP is fabricated. The editable report remains in Power BI Service, with reproducible data, TMDL, DAX, M and page instructions supplied locally.
''')
    p=ROOT/'README.md';s=p.read_text()
    start=s.index('## Reproduce the analytical core');end=s.index('## Recommendations',start)
    s=s[:start]+'''## Reproduce the analytical core
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/run_all.py
```
On Windows activate `.venv\\Scripts\\activate`. No paid API key is needed.
The seed and raw CSV SHA-256 hashes are in `data/scenario.json` and `data/manifest.json`.
`reports/reproducibility.json` records an independent regeneration with all 20 raw file hashes matching.
The pipeline runs 275 dataset checks, seven control tests, eight supplemental aggregate controls and 15 analytical SQL queries.
The optional Excel writer requires the artifact-tool runtime; use `node scripts/build_workbook.mjs`, then the same command with `--operations`.
Cloud reports are updated separately. Rebuilding local files does not refresh the saved Power BI report or its dated screenshots.
Open `data/processed/retail360.sqlite` to explore `sql/business_analysis.sql`; results are retained as `reports/sql_analysis_01.csv` through `15.csv`.

'''+s[end:]
    marker='\n## Native report and submission files\n'
    s=s.split(marker)[0]
    s+=f'''{marker}
[Open the editable Power BI report]({REPORT}). Access requires the owner account or separately granted permissions.
Three native pages, 51 DAX measures and 17 dimension relationships are implemented. Read [native validation evidence](reports/powerbi_status.md) for tested interactions and remaining extensions.

![Native financial report](visuals/screenshots/01_financial_native.jpg)
![Native inventory report](visuals/screenshots/02_inventory_native.jpg)
![Native systems report](visuals/screenshots/03_systems_native.jpg)

Use [the portfolio brief](Retail360_Portfolio_Brief.pdf) for a short offline walkthrough.
It contains a written case summary and actual native browser captures; it is a snapshot PDF assembled locally.
The two Excel imports are [core reporting tables](data/retail360_powerbi.xlsx) and [supplemental operations](data/retail360_operations.xlsx).
For a hiring manager, send the brief with a repository/package link and disclose synthetic data.
Check report access from the recipient's account before relying on a Power BI URL; public access has not been enabled.
Keep the full raw dataset and SQL available for technical review.
'''
    p.write_text(s)
    p=ROOT/'docs/resume_bullets.md';s=p.read_text().replace('- Produced Power BI-ready reporting data, DAX and Power Query definitions, requirements, data mappings and a UAT plan to support financial, inventory and systems-health reporting.',
      '- Built and verified a three-page Power BI Service report with 51 DAX measures and 17 dimension relationships; documented requirements, mappings, reconciliation controls and UAT cases across finance, inventory and systems reliability.')
    s=s.replace('Replace the third bullet with an actual Power BI implementation claim only after the native report has been saved and tested.\n','')
    p.write_text(s)
    p=ROOT/'docs/functional_requirements.md';s=p.read_text().replace('Finance month and channel slicers affect finance tables.',
      'The implemented finance quarter slicer filters applicable monthly finance facts. Channel breakdown is shown as a bar chart; no separate channel slicer is configured.')
    s=s.replace('inventory uses the selected snapshot/as-of date,','the implemented inventory page uses the September 30 cutoff snapshot,')
    s+='\n## Implemented scope\nThe native report prioritizes executive charts. Additional analyses and drillthrough are specified extensions, not claimed as live functionality. See reports/powerbi_status.md and powerbi/detail_visual_specifications.md.\n'
    p.write_text(s)
    p=ROOT/'docs/uat_test_plan.md';s=p.read_text().replace('| Select month and channel in finance page | Correct totals and chart filtering | Pending native report test |',
      '| Select Q3 2026 in finance | $1,075,281.59 sales; 56.9% margin; 18.4% budget variance | Native PASS; separate channel slicer not configured |')
    s=s.replace('| Change historical month on inventory page | Current snapshot remains labeled Sep 30 and unaffected | Pending native report test |',
      '| Apply Q3 date context to current snapshot measures | Inventory $1,913,202.67 and risk 6 unchanged; current page has no date slicer | Native DAX PASS |')
    s=s.replace('Consistent layout and no empty or erroneous visuals | Pending native report test','Consistent layout and no empty or erroneous visuals | Native PASS')
    s=s.replace('Model and report persist and match control totals | Pending native report test','Model and report persist and match control totals | Native PASS')
    s=s.replace('See unittest run','Automated PASS (seven control tests)')
    p.write_text(s)
    p=ROOT/'docs/assumptions_and_limitations.md';s=p.read_text()
    note='Support resolution and order reconciliation are separate lifecycles. A resolved ticket does not by itself prove that an ERP order link exists; a production closure control should require business reconciliation evidence.'
    if note not in s:s+='\n- '+note+'\n'
    p.write_text(s)
    p=ROOT/'powerbi/model_documentation.md';s=p.read_text().split('\n## Actual saved browser model')[0]
    s+='''\n## Actual saved browser model
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
''';p.write_text(s)
    p=ROOT/'powerbi/build_guide.md';s=p.read_text().split('\n## Reproduce the saved native model')[0]
    s+='''\n## Reproduce the saved native model
1. Import core `data/retail360_powerbi.xlsx` tables once; preserve DimDate7, DimChannel8, DimLocation9, DimProduct10, ReportPurchasing5 and ReportReconciliation6 aliases. Rename only the four reporting summaries to ReportFinance, ReportCategory, ReportInventory and ReportSystems.
2. In model TMDL View apply `browser_measures.tmdl`, then `browser_relationships.tmdl`.
3. Use Get data to import the five Excel tables in `data/retail360_operations.xlsx`, preserving generated aliases (see model documentation). Avoid importing duplicate worksheet objects.
4. Inspect and correct all data types. Date keys must be Date, identifiers/counts Whole number, monetary/ratio inputs Decimal number. Product numerical columns need explicit checking.
5. Apply `operations_extension.tmdl`. It adds/updates measures using `ref table _Measures`; it does not replace the whole model. The editor must show zero remaining syntax errors. The initial measure script is for creating the measure table; use reference scripts for subsequent edits.
6. Refresh through model Home > Queries > Refresh; then refresh report visuals. Test native DAX against `reports/kpi_controls.json` and the dated `native_validation.json` observations.
7. Import `theme.json`, choose a custom 1600 x 900 canvas and apply each matching background at 0% transparency. Backgrounds contain branding and labels only; real values/charts/tables are native visuals.
8. Follow `page_specifications.md`. Save, reopen in Viewing mode, select Q3 2026, verify totals, clear filters and navigate all three pages.
9. Further detailed visuals are described in `detail_visual_specifications.md`. They are extensions to the focused native executive layout.

Do not paste a multi-measure definition file into the DAX query editor. TMDL scripts belong in TMDL View; DAX query checks use EVALUATE.
Workbook numeric values and dates must be inspected even if automatic type detection succeeded for another table.
Date-dimension uniqueness and completeness are validated locally; mark it as the date table when extending time-intelligence reporting.
No native PBIX/PBIP export is included. The Service report is the editable implementation; Windows Desktop can rebuild from the local sources.
''';p.write_text(s)
    write('powerbi/page_specifications.md','''# Saved three-page layout
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
''')
    write('powerbi/detail_visual_specifications.md','''# Detailed analysis extensions and requirement coverage
The saved three-page report prioritizes a small set of executive visuals. The following requested details are supported by executable data/SQL and documented build bindings; they are not presented as already configured native visuals.

| Detail question | Reproducible result | Power BI build binding |
|---|---|---|
| Store ranking | sql_analysis_07.csv | LocationName; NetSales, GrossMargin, BudgetVariance; retail channel only |
| Top/bottom products | sql_analysis_08.csv | ReportProduct5 SKU/ProductName; Product Net Sales / Product Gross Margin %; Top N or Bottom N 10 |
| Margin variance | kpi_controls.json q3_comparison | Gross Margin Q3 2025, Gross Margin Q3 2026, Q3 Margin Change pp; do not call margin decline an absolute GP decline |
| Fulfillment trends | sql_analysis_09.csv | ReportFulfillment1.MonthStart; Fulfillment Rate, Average Fulfillment Duration, Late Orders |
| Late orders by location | sql_analysis_10.csv | DimLocation9.LocationName; Late Orders/Open Late Orders through fulfillment location relationship |
| Failures by source | sql_analysis_11.csv | Detailed FactIntegrationEvents SourceSystem; filtered Status=Failed count |
| Ticket category and severity | sql_analysis_12.csv | ReportTickets4 Category/Severity; Ticket Count and SLA Compliance Rate |
| SLA trend | sql_analysis_13.csv | DimDate7.MonthStart; SLA Compliance Rate; ticket-open cohort basis |
| Operational priority matrix | sql_analysis_14.csv | ExceptionType/Priority; affected orders, ordered-value exposure, oldest age; no invented loss score |
| Category demand | sql_analysis_15.csv | ReportProduct5 MonthStart/Category; UnitsSold, UnitsReturned and Product Net Sales |

Detailed fact import: typed CSV Power Query definitions are supplied for all raw and processed tables. Use the full model relationships and detail DAX file, not a mixture of suffixed and unsuffixed aliases.
For an order drillthrough extension, create a focused detail page with OrderId as the drillthrough field; show source order header/lines, shipment status, ERP-link existence, filtered integration events and support tickets. Pre-aggregate child facts or keep them in separate visuals to prevent multiplication.
For SKU drillthrough use ProductId, show historical demand and current SKU/location candidates, then an open purchase-order table. Test destination filters, back navigation and no-data cases before claiming implementation.
Tooltips should disclose posting dates vs order cohorts, USD units, 90-day inventory basis, cutoff and denominator rules. Risk is also expressed with text/flags; conditional colors can be added using explicit numeric rules.
''')
    print('Dated native evidence and submission documentation updated.')
if __name__=='__main__':main()
