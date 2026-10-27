# Detailed analysis extensions and requirement coverage
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
