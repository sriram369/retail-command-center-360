# Reproduce the Power BI report
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

## Reproduce the saved native model
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
