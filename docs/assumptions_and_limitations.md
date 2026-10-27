# Assumptions and limitations
- Company, suppliers, customers and transactions are fictional. A fixed seed creates one consistent sample.
- 18 months of data begins April 2025; prior-year comparisons before April 2026 lack complete comparable history.
- Sales is recognized at complete shipment as an operational proxy. No general ledger or revenue allocation contract model exists.
- All returns are restockable, one unit per return record, with original issue cost restored. No damage write-off or chargeback modeling.
- Inventory uses perpetual moving weighted average and four-decimal valuation. Original unit-cost reference is not a current standard cost.
- Transfers are same-day stock movements. There is no in-transit inventory, component assembly, split shipment or multi-currency accounting.
- Store orders include reservations and pickups. Fulfillment means shipment/collection processing, not customer delivery.
- Current stock risk uses 28-day ordered demand, reserved backlog and protection days; recommendations are independent candidates.
- Repeat incidents group by configured root-cause key. This is not a learned incident classifier.
- SLA is elapsed time; 24 hours for high severity and 72 hours for medium severity. No pause or business-hours calendar.
- The compact Excel report model aggregates financials by month/channel/location and categories by month/category. It does not support every possible drillthrough.
- The full CSV/SQLite model retains order-line detail for additional analysis. No live refresh or actual systems integration is implemented.
- Python/SQL tests do not prove that DAX compiles or that report interactions work. Native checks and limitations are recorded separately.
- Optional AI output must cite supplied metric keys. It never changes deterministic business totals.

- Support resolution and order reconciliation are separate lifecycles. A resolved ticket does not by itself prove that an ERP order link exists; a production closure control should require business reconciliation evidence.
