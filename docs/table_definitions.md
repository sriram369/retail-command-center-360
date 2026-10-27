# Table definitions and granularity

| Table | Grain | Rows |
|---|---|---|
| DimChannel | one sales channel | 3 |
| DimCustomer | one anonymous synthetic customer profile | 4,000 |
| DimDate | one calendar date | 548 |
| DimLocation | one physical stocking location | 8 |
| DimProduct | one finished-goods SKU | 200 |
| DimStore | one physical store | 7 |
| DimSupplier | one fictional supplier | 28 |
| FactBudget | one month / channel / location budget | 162 |
| FactERPOrderLinks | one successfully created simulated ERP order | 23,467 |
| FactIntegrationEvents | one received mock integration event or retry | 9,954 |
| FactInventoryMovements | one signed stock/value movement | 47,192 |
| FactInventorySnapshots | one month-end / SKU / location balance | 28,800 |
| FactPurchaseOrders | one single-SKU purchase order | 374 |
| FactReturns | one returned unit of an actual completed sales line | 1,513 |
| FactSalesOrderLines | one product line per source order | 40,573 |
| FactSalesOrders | one source customer order | 24,000 |
| FactSalesTransactions | one signed sales-line or return posting | 41,105 |
| FactShipments | one complete order shipment | 23,425 |
| FactSupportTickets | one order-linked incident ticket | 259 |
| InjectedAnomalies | one documented order or PO exception | 825 |

Identifiers ending in Id are stable keys; each table's primary key is its entity key (Date for DimDate, ReturnId for FactReturns).
DimStore.StoreId shares location IDs 1–7 with the store rows in DimLocation. Use DimLocation in the semantic model to avoid parallel filter paths.
FactBudget is unique on MonthStart, ChannelId and LocationId. Snapshots are unique on SnapshotDate, ProductId and LocationId.
ERP links are unique on both OrderId and ERPOrderId. FactShipments allows at most one shipment per OrderId in this simplified model.
Raw tables are retained for audit. SQLite is a rebuildable analytical store; validation enforces integrity even though pandas loading does not declare database foreign-key constraints.
