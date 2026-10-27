# Functional specification
## Pages and date semantics
Finance uses shipment and return posting dates, the implemented inventory page uses the September 30 cutoff snapshot,
fulfillment uses order cohorts, integration trends use event dates, and support trends use ticket-open cohorts.
Label each date basis. Do not present ticket-cohort SLA compliance as compliance among tickets resolved that month.
Use shared date and location dimensions with single-direction filters from dimensions to facts.
Never join two transaction facts directly for aggregate calculations.

## Behavior
Default finance view covers the available 18 months; Q3 2026 vs Q3 2025 is the comparable headline.
The implemented finance quarter slicer filters applicable monthly finance facts. Channel breakdown is shown as a bar chart; no separate channel slicer is configured. Budget is only valid at month/channel/location grain.
Category and product charts have no allocated budget. In the compact browser workbook, category summaries cover all channels.
Current inventory and unresolved-order tables are cutoff snapshots; disable historical month interactions for these visuals.
Click a store/channel to filter applicable finance visuals. Use order/SKU tables for investigation.
Native drillthrough is configured only after the model and report support it; the reproducible design specifies an OrderId or SKU detail view.

## Calculations
Net sales includes signed sale and return postings. COGS uses moving weighted average issue costs and original-cost return reversals.
Net sales less COGS is gross profit. Ratios divide aggregated numerators by aggregated denominators.
Units sold is positive sale quantity; units returned is absolute negative quantity. Return rate is posting-period returns / sale units, not a mature cohort return probability.
Average order value is period net sales / distinct shipped orders in the same posting period. Returns can relate to older orders.
Integration success and failure rates exclude ignored duplicates, which have a separate control count.
SLA denominator includes resolved tickets and unresolved tickets whose deadlines have passed at cutoff.
MTTR is average elapsed hours for resolved tickets. SLA clocks run continuously, not business hours.
Repeat incidents are subsequent tickets sharing a defined root-cause key, ordered by opened timestamp and TicketId.

## Refresh, security and exceptions
Refresh source data, validate, build marts, reconcile, run tests, then update the report.
Block release on accidental errors. Keep known operational failures visible in the exception queue.
No scheduled cloud refresh, gateway, RLS enforcement or notification automation is claimed as implemented.
Recommended production access: executives companywide, operations by location, support by queue. Test RLS separately before deployment.
High-priority unresolved sync orders are cohort-affected orders without an ERP link; order value is exposure, not established lost revenue.

## Implemented scope
The native report prioritizes executive charts. Additional analyses and drillthrough are specified extensions, not claimed as live functionality. See reports/powerbi_status.md and powerbi/detail_visual_specifications.md.
