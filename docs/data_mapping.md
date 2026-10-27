# Source-to-target mapping
The source fields below describe simulated extracts, not tested connections to vendor APIs.
Raw CSV schemas are implemented; vendor mappings are an illustrative design boundary.

| Simulated source | Source concept / raw field | Target | Transformation |
|---|---|---|---|
| Commerce/POS/wholesale order | OrderNumber / OrderDate | FactSalesOrders | Stable OrderId, ISO date, channel/location assignment |
| Source line | ProductId, Quantity, UnitPrice, DiscountAmount | FactSalesOrderLines | Quantity × list price less discount, rounded to cents |
| Warehouse shipment | OrderId, ShipDate | FactShipments | Validate noncanceled order and sufficient physical stock |
| Shipment issue | OrderLineId, ValueChange | FactSalesTransactions.COGS | Negative movement becomes positive COGS |
| Fulfilled source line | OrderedAmount | FactSalesTransactions.NetAmount | Post only at shipment date |
| Return/refund | ReturnId, RefundAmount, CostReversal | FactReturns and negative sales transaction | Original unit price and original issue cost |
| Purchase receipt | PurchaseOrderId, Quantity, UnitCost | FactInventoryMovements | Signed receipt and moving weighted average valuation |
| Stock ledger | QuantityChange, ValueChange | FactInventorySnapshots | Cumulative balances for each month-end/SKU/location |
| Finance plan | MonthStart, ChannelId, LocationId | FactBudget | Independently generated monthly target |
| Integration monitor | OrderId, BusinessKey, Status | FactIntegrationEvents | Keep retries and ignored duplicate events |
| ERP order creation | OrderId, ERPOrderId | FactERPOrderLinks | One successful business order link per source order |
| Support export | OpenedAt, ResolvedAt, SLADeadline | FactSupportTickets | Cutoff-aware SLA eligibility and elapsed resolution hours |
| Signed sales ledger | PostingDate, NetAmount, COGS | ReportFinance / ReportCategory / ReportProduct | Aggregate only at declared grains |
| Source orders vs ERP links | OrderId | ReportReconciliation | Left anti-join expected noncanceled commerce population |
| Monthly inventory and recent demand | UnitsOnHand, Quantity | ReportInventory | Reserved backlog, 28-day demand and protection thresholds |

Python builds SQL/CSV marts. Power Query examples reproduce ingestion, typing, relationship keys and reconciliation in Power BI.
Scenario truth fields and InjectedAnomalies are validation inputs; hide or exclude them from the executive-facing model.
