# Data dictionary

Synthetic data. USD. Local dates use America/New_York. Empty fields are permitted only for documented lifecycle or payload fields.

## DimChannel
Grain: one sales channel. Rows: 3.

| Field | Type | Meaning |
|---|---|---|
| ChannelId | integer | Stable identifier for Channel. |
| Channel | text | Channel. |

## DimCustomer
Grain: one anonymous synthetic customer profile. Rows: 4,000.

| Field | Type | Meaning |
|---|---|---|
| CustomerId | integer | Stable identifier for Customer. |
| CustomerCode | text | Customer Code. |
| Segment | text | Segment. |
| State | text | State. |
| Synthetic | integer | Always 1. Profiles contain no names or contact information. |

## DimDate
Grain: one calendar date. Rows: 548.

| Field | Type | Meaning |
|---|---|---|
| Date | ISO date | Date. |
| Year | integer | Year. |
| MonthNumber | integer | Month Number. |
| Month | text | Month. |
| MonthStart | text | Month Start. |
| Quarter | text | Quarter. |
| DayOfWeek | text | Day Of Week. |

## DimLocation
Grain: one physical stocking location. Rows: 8.

| Field | Type | Meaning |
|---|---|---|
| LocationId | integer | Stable identifier for Location. |
| LocationName | text | Location Name. |
| LocationType | text | Location Type. |
| State | text | State. |

## DimProduct
Grain: one finished-goods SKU. Rows: 200.

| Field | Type | Meaning |
|---|---|---|
| ProductId | integer | Stable identifier for Product. |
| SKU | text | S K U. |
| ProductName | text | Product Name. |
| Category | text | Category. |
| SupplierId | integer | Stable identifier for Supplier. |
| RetailPrice | decimal | Undiscounted retail list price in USD. |
| OpeningUnitCost | decimal | Opening inventory unit cost, not the current issue cost. |
| Customizable | integer | Customizable. |

## DimStore
Grain: one physical store. Rows: 7.

| Field | Type | Meaning |
|---|---|---|
| StoreId | integer | Stable identifier for Store. |
| StoreName | text | Store Name. |
| City | text | City. |
| State | text | State. |

## DimSupplier
Grain: one fictional supplier. Rows: 28.

| Field | Type | Meaning |
|---|---|---|
| SupplierId | integer | Stable identifier for Supplier. |
| SupplierName | text | Supplier Name. |
| StandardLeadDays | integer | Standard Lead Days. |
| Terms | text | Terms. |

## FactBudget
Grain: one month / channel / location budget. Rows: 162.

| Field | Type | Meaning |
|---|---|---|
| BudgetId | integer | Stable identifier for Budget. |
| MonthStart | text | Month Start. |
| ChannelId | integer | Stable identifier for Channel. |
| LocationId | integer | Stable identifier for Location. |
| SalesBudget | decimal | Independent monthly net-sales target at channel/location grain. |

## FactERPOrderLinks
Grain: one successfully created simulated ERP order. Rows: 23,467.

| Field | Type | Meaning |
|---|---|---|
| ERPLinkId | integer | Stable identifier for ERPLink. |
| OrderId | integer | Stable identifier for Order. |
| ERPOrderId | text | Stable identifier for ERPOrder. |
| SyncedDate | ISO date | Synced Date. |

## FactIntegrationEvents
Grain: one received mock integration event or retry. Rows: 9,954.

| Field | Type | Meaning |
|---|---|---|
| EventId | integer | Stable identifier for Event. |
| OrderId | integer | Stable identifier for Order. |
| EventDate | ISO date | Event Date. |
| SourceSystem | text | Source System. |
| EventType | text | Event Type. |
| Status | text | Status. |
| BusinessKey | text | Business Key. |
| PayloadSKU | text | Untrusted mock source payload; UNKNOWN-SKU represents a quarantined mapping error, not an invalid analytical FK. |
| Deduplicated | integer | 1 if a duplicate webhook is ignored without creating another sale. |

## FactInventoryMovements
Grain: one signed stock/value movement. Rows: 47,192.

| Field | Type | Meaning |
|---|---|---|
| MovementId | integer | Stable identifier for Movement. |
| MovementDate | ISO date | Movement Date. |
| LocationId | integer | Stable identifier for Location. |
| ProductId | integer | Stable identifier for Product. |
| MovementType | text | Movement Type. |
| QuantityChange | integer | Signed stock units; receipts positive and issues negative. |
| ValueChange | decimal | Signed stock carrying-value change in USD to four decimals. |
| ReferenceType | text | Reference Type. |
| ReferenceId | text | Polymorphic movement reference; interpreted together with ReferenceType. |
| TransferId | text | Shared reference between an equal and opposite transfer pair; blank on other movements. |

## FactInventorySnapshots
Grain: one month-end / SKU / location balance. Rows: 28,800.

| Field | Type | Meaning |
|---|---|---|
| SnapshotId | integer | Stable identifier for Snapshot. |
| SnapshotDate | ISO date | Snapshot Date. |
| LocationId | integer | Stable identifier for Location. |
| ProductId | integer | Stable identifier for Product. |
| UnitsOnHand | integer | Units On Hand. |
| InventoryValue | decimal | Closing carrying value in USD; not additive over snapshot dates. |
| WeightedAverageCost | decimal | Closing value divided by on-hand units; zero when no units remain. |

## FactPurchaseOrders
Grain: one single-SKU purchase order. Rows: 374.

| Field | Type | Meaning |
|---|---|---|
| PurchaseOrderId | integer | Stable identifier for PurchaseOrder. |
| PONumber | text | P O Number. |
| ProductId | integer | Stable identifier for Product. |
| SupplierId | integer | Stable identifier for Supplier. |
| LocationId | integer | Stable identifier for Location. |
| PODate | ISO date | P O Date. |
| ApprovalDate | ISO date | Approval Date. |
| PromisedReceiptDate | ISO date | Approved PO promise date; may lie after the reporting cutoff. |
| ReceivedDate | ISO date | Received Date. |
| Quantity | integer | Quantity. |
| UnitCost | decimal | Unit Cost. |
| POAmount | decimal | P O Amount. |
| ApprovalDays | integer | Simulated approval duration; future approval dates are not exposed as completed approvals. |
| POStatus | text | P O Status. |
| ScenarioAffected | integer | Scenario truth flag for intentionally delayed purchasing. |

## FactReturns
Grain: one returned unit of an actual completed sales line. Rows: 1,513.

| Field | Type | Meaning |
|---|---|---|
| ReturnId | text | Stable identifier for Return. |
| OrderId | integer | Stable identifier for Order. |
| OrderLineId | integer | Stable identifier for OrderLine. |
| ReturnDate | ISO date | Return Date. |
| ProductId | integer | Stable identifier for Product. |
| LocationId | integer | Stable identifier for Location. |
| ChannelId | integer | Stable identifier for Channel. |
| CustomerId | integer | Stable identifier for Customer. |
| Quantity | integer | Quantity. |
| RefundAmount | decimal | Original discounted unit price rounded to cents using Python round; actual refund amount is authoritative. |
| CostReversal | decimal | Cost Reversal. |
| Reason | text | Reason. |
| Disposition | text | Disposition. |

## FactSalesOrderLines
Grain: one product line per source order. Rows: 40,573.

| Field | Type | Meaning |
|---|---|---|
| OrderLineId | integer | Stable identifier for OrderLine. |
| OrderId | integer | Stable identifier for Order. |
| ProductId | integer | Stable identifier for Product. |
| Quantity | integer | Quantity. |
| UnitPrice | decimal | Unit Price. |
| DiscountAmount | decimal | Line discount before returns; do not subtract again from NetAmount. |
| OrderedAmount | decimal | Order-line amount after discount. Not booked sales until a sale transaction exists. |

## FactSalesOrders
Grain: one source customer order. Rows: 24,000.

| Field | Type | Meaning |
|---|---|---|
| OrderId | integer | Stable identifier for Order. |
| OrderNumber | text | Order Number. |
| OrderDate | ISO date | Order Date. |
| CustomerId | integer | Stable identifier for Customer. |
| ChannelId | integer | Stable identifier for Channel. |
| LocationId | integer | Stable identifier for Location. |
| PromisedDate | ISO date | Customer promised ship/fulfillment date, not promised delivery. |
| OrderStatus | text | Order Status. |
| PaymentStatus | text | Captured or Voided. Captured is a source order state, not an accounting cash ledger. |
| IntegrationIssue | text | Integration Issue. |
| AvailableDate | ISO date | Earliest date the source order may be fulfilled after processing or synchronization. |
| Cohort | integer | Scenario truth flag for the targeted assortment. Hidden from business report; used for scenario verification. |

## FactSalesTransactions
Grain: one signed sales-line or return posting. Rows: 41,105.

| Field | Type | Meaning |
|---|---|---|
| SalesTransactionId | integer | Stable identifier for SalesTransaction. |
| PostingDate | ISO date | Posting Date. |
| OrderId | integer | Stable identifier for Order. |
| OrderLineId | integer | Stable identifier for OrderLine. |
| ProductId | integer | Stable identifier for Product. |
| LocationId | integer | Stable identifier for Location. |
| ChannelId | integer | Stable identifier for Channel. |
| CustomerId | integer | Stable identifier for Customer. |
| TransactionType | text | Transaction Type. |
| Quantity | integer | Quantity. |
| NetAmount | decimal | Signed sales amount after discount; negative for refunds. Excludes tax and shipping. |
| COGS | decimal | Signed moving-average issue cost, reversed at original issue cost on restockable returns. |
| DiscountAmount | decimal | Line discount before returns; do not subtract again from NetAmount. |

## FactShipments
Grain: one complete order shipment. Rows: 23,425.

| Field | Type | Meaning |
|---|---|---|
| ShipmentId | integer | Stable identifier for Shipment. |
| OrderId | integer | Stable identifier for Order. |
| ShipDate | ISO date | Ship Date. |
| LocationId | integer | Stable identifier for Location. |
| OrderDate | ISO date | Order Date. |
| ChannelId | integer | Stable identifier for Channel. |
| PromisedDate | ISO date | Customer promised ship/fulfillment date, not promised delivery. |
| FulfillmentDays | integer | Fulfillment Days. |
| IsLate | integer | Is Late. |

## FactSupportTickets
Grain: one order-linked incident ticket. Rows: 259.

| Field | Type | Meaning |
|---|---|---|
| TicketId | integer | Stable identifier for Ticket. |
| OrderId | integer | Stable identifier for Order. |
| OpenedAt | ISO timestamp | Opened At. |
| ResolvedAt | ISO timestamp | Resolved At. |
| SLADeadline | ISO timestamp | S L A Deadline. |
| Category | text | Category. |
| Severity | text | Severity. |
| Status | text | Status. |
| Owner | text | Owner. |
| RepeatKey | text | Root-cause grouping for repeat-incident counts, not a duplicate ticket identifier. |
| ResolutionHours | text | Elapsed hours to resolution, blank for open tickets. |
| SLAEligible | integer | 1 for resolved tickets or open tickets past their deadline at cutoff. |
| SLAMet | integer | 1 only when resolved on or before the SLA deadline. |

## InjectedAnomalies
Grain: one documented order or PO exception. Rows: 825.

| Field | Type | Meaning |
|---|---|---|
| AnomalyId | integer | Stable identifier for Anomaly. |
| Scenario | text | Scenario. |
| Entity | text | Entity. |
| EntityId | integer | Stable identifier for Entity. |
| Issue | text | Issue. |
| StartDate | ISO date | Start Date. |
| Cohort | integer | Scenario truth flag for the targeted assortment. Hidden from business report; used for scenario verification. |
