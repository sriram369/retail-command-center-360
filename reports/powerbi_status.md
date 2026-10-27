# Power BI implementation evidence
Captured October 27, 2026. The native three-page executive report is saved in Power BI Service.

[Open report](https://app.powerbi.com/groups/me/reports/45421c92-9cfc-4bca-ae5d-4f64fcd1b2e3) · [Open semantic model](https://app.powerbi.com/groups/me/modeling/86841f6f-d70b-4947-badc-f2ccb56a93ff/modelView)
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
