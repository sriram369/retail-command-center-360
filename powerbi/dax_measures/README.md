# Measure definitions and verification
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
