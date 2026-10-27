# Dataset validation

Status: PASS. 275 checks. Reporting cutoff: 2026-09-30.

Intentional operational failures remain business exceptions. They are not broken foreign keys or duplicate sales.

| Check | Result | Detail |
|---|---|---|
| FactIntegrationEvents: primary key unique | PASS |  |
| FactIntegrationEvents: manifest matches | PASS |  |
| FactIntegrationEvents.EventId: required | PASS |  |
| FactIntegrationEvents.OrderId: required | PASS |  |
| FactIntegrationEvents.OrderId: foreign key | PASS | 0 invalid references |
| FactIntegrationEvents.EventDate: required | PASS |  |
| FactIntegrationEvents.SourceSystem: required | PASS |  |
| FactIntegrationEvents.EventType: required | PASS |  |
| FactIntegrationEvents.Status: required | PASS |  |
| FactIntegrationEvents.BusinessKey: required | PASS |  |
| FactIntegrationEvents.Deduplicated: required | PASS |  |
| DimStore: primary key unique | PASS |  |
| DimStore: manifest matches | PASS |  |
| DimStore.StoreId: required | PASS |  |
| DimStore.StoreName: required | PASS |  |
| DimStore.City: required | PASS |  |
| DimStore.State: required | PASS |  |
| FactBudget: primary key unique | PASS |  |
| FactBudget: manifest matches | PASS |  |
| FactBudget.BudgetId: required | PASS |  |
| FactBudget.MonthStart: required | PASS |  |
| FactBudget.ChannelId: required | PASS |  |
| FactBudget.ChannelId: foreign key | PASS | 0 invalid references |
| FactBudget.LocationId: required | PASS |  |
| FactBudget.LocationId: foreign key | PASS | 0 invalid references |
| FactBudget.SalesBudget: required | PASS |  |
| FactShipments: primary key unique | PASS |  |
| FactShipments: manifest matches | PASS |  |
| FactShipments.ShipmentId: required | PASS |  |
| FactShipments.OrderId: required | PASS |  |
| FactShipments.OrderId: foreign key | PASS | 0 invalid references |
| FactShipments.ShipDate: required | PASS |  |
| FactShipments.LocationId: required | PASS |  |
| FactShipments.LocationId: foreign key | PASS | 0 invalid references |
| FactShipments.OrderDate: required | PASS |  |
| FactShipments.ChannelId: required | PASS |  |
| FactShipments.ChannelId: foreign key | PASS | 0 invalid references |
| FactShipments.PromisedDate: required | PASS |  |
| FactShipments.FulfillmentDays: required | PASS |  |
| FactShipments.IsLate: required | PASS |  |
| FactSalesOrders: primary key unique | PASS |  |
| FactSalesOrders: manifest matches | PASS |  |
| FactSalesOrders.OrderId: required | PASS |  |
| FactSalesOrders.OrderNumber: required | PASS |  |
| FactSalesOrders.OrderDate: required | PASS |  |
| FactSalesOrders.CustomerId: required | PASS |  |
| FactSalesOrders.CustomerId: foreign key | PASS | 0 invalid references |
| FactSalesOrders.ChannelId: required | PASS |  |
| FactSalesOrders.ChannelId: foreign key | PASS | 0 invalid references |
| FactSalesOrders.LocationId: required | PASS |  |
| FactSalesOrders.LocationId: foreign key | PASS | 0 invalid references |
| FactSalesOrders.PromisedDate: required | PASS |  |
| FactSalesOrders.OrderStatus: required | PASS |  |
| FactSalesOrders.PaymentStatus: required | PASS |  |
| FactSalesOrders.IntegrationIssue: required | PASS |  |
| FactSalesOrders.AvailableDate: required | PASS |  |
| FactSalesOrders.Cohort: required | PASS |  |
| FactSupportTickets: primary key unique | PASS |  |
| FactSupportTickets: manifest matches | PASS |  |
| FactSupportTickets.TicketId: required | PASS |  |
| FactSupportTickets.OrderId: required | PASS |  |
| FactSupportTickets.OrderId: foreign key | PASS | 0 invalid references |
| FactSupportTickets.OpenedAt: required | PASS |  |
| FactSupportTickets.SLADeadline: required | PASS |  |
| FactSupportTickets.Category: required | PASS |  |
| FactSupportTickets.Severity: required | PASS |  |
| FactSupportTickets.Status: required | PASS |  |
| FactSupportTickets.Owner: required | PASS |  |
| FactSupportTickets.RepeatKey: required | PASS |  |
| FactSupportTickets.SLAEligible: required | PASS |  |
| FactSupportTickets.SLAMet: required | PASS |  |
| FactSalesOrderLines: primary key unique | PASS |  |
| FactSalesOrderLines: manifest matches | PASS |  |
| FactSalesOrderLines.OrderLineId: required | PASS |  |
| FactSalesOrderLines.OrderId: required | PASS |  |
| FactSalesOrderLines.OrderId: foreign key | PASS | 0 invalid references |
| FactSalesOrderLines.ProductId: required | PASS |  |
| FactSalesOrderLines.ProductId: foreign key | PASS | 0 invalid references |
| FactSalesOrderLines.Quantity: required | PASS |  |
| FactSalesOrderLines.UnitPrice: required | PASS |  |
| FactSalesOrderLines.DiscountAmount: required | PASS |  |
| FactSalesOrderLines.OrderedAmount: required | PASS |  |
| DimChannel: primary key unique | PASS |  |
| DimChannel: manifest matches | PASS |  |
| DimChannel.ChannelId: required | PASS |  |
| DimChannel.Channel: required | PASS |  |
| FactReturns: primary key unique | PASS |  |
| FactReturns: manifest matches | PASS |  |
| FactReturns.ReturnId: required | PASS |  |
| FactReturns.OrderId: required | PASS |  |
| FactReturns.OrderId: foreign key | PASS | 0 invalid references |
| FactReturns.OrderLineId: required | PASS |  |
| FactReturns.OrderLineId: foreign key | PASS | 0 invalid references |
| FactReturns.ReturnDate: required | PASS |  |
| FactReturns.ProductId: required | PASS |  |
| FactReturns.ProductId: foreign key | PASS | 0 invalid references |
| FactReturns.LocationId: required | PASS |  |
| FactReturns.LocationId: foreign key | PASS | 0 invalid references |
| FactReturns.ChannelId: required | PASS |  |
| FactReturns.ChannelId: foreign key | PASS | 0 invalid references |
| FactReturns.CustomerId: required | PASS |  |
| FactReturns.CustomerId: foreign key | PASS | 0 invalid references |
| FactReturns.Quantity: required | PASS |  |
| FactReturns.RefundAmount: required | PASS |  |
| FactReturns.CostReversal: required | PASS |  |
| FactReturns.Reason: required | PASS |  |
| FactReturns.Disposition: required | PASS |  |
| DimDate: primary key unique | PASS |  |
| DimDate: manifest matches | PASS |  |
| DimDate.Date: required | PASS |  |
| DimDate.Year: required | PASS |  |
| DimDate.MonthNumber: required | PASS |  |
| DimDate.Month: required | PASS |  |
| DimDate.MonthStart: required | PASS |  |
| DimDate.Quarter: required | PASS |  |
| DimDate.DayOfWeek: required | PASS |  |
| FactERPOrderLinks: primary key unique | PASS |  |
| FactERPOrderLinks: manifest matches | PASS |  |
| FactERPOrderLinks.ERPLinkId: required | PASS |  |
| FactERPOrderLinks.OrderId: required | PASS |  |
| FactERPOrderLinks.OrderId: foreign key | PASS | 0 invalid references |
| FactERPOrderLinks.ERPOrderId: required | PASS |  |
| FactERPOrderLinks.SyncedDate: required | PASS |  |
| FactPurchaseOrders: primary key unique | PASS |  |
| FactPurchaseOrders: manifest matches | PASS |  |
| FactPurchaseOrders.PurchaseOrderId: required | PASS |  |
| FactPurchaseOrders.PONumber: required | PASS |  |
| FactPurchaseOrders.ProductId: required | PASS |  |
| FactPurchaseOrders.ProductId: foreign key | PASS | 0 invalid references |
| FactPurchaseOrders.SupplierId: required | PASS |  |
| FactPurchaseOrders.SupplierId: foreign key | PASS | 0 invalid references |
| FactPurchaseOrders.LocationId: required | PASS |  |
| FactPurchaseOrders.LocationId: foreign key | PASS | 0 invalid references |
| FactPurchaseOrders.PODate: required | PASS |  |
| FactPurchaseOrders.PromisedReceiptDate: required | PASS |  |
| FactPurchaseOrders.Quantity: required | PASS |  |
| FactPurchaseOrders.UnitCost: required | PASS |  |
| FactPurchaseOrders.POAmount: required | PASS |  |
| FactPurchaseOrders.ApprovalDays: required | PASS |  |
| FactPurchaseOrders.POStatus: required | PASS |  |
| FactPurchaseOrders.ScenarioAffected: required | PASS |  |
| FactSalesTransactions: primary key unique | PASS |  |
| FactSalesTransactions: manifest matches | PASS |  |
| FactSalesTransactions.SalesTransactionId: required | PASS |  |
| FactSalesTransactions.PostingDate: required | PASS |  |
| FactSalesTransactions.OrderId: required | PASS |  |
| FactSalesTransactions.OrderId: foreign key | PASS | 0 invalid references |
| FactSalesTransactions.OrderLineId: required | PASS |  |
| FactSalesTransactions.OrderLineId: foreign key | PASS | 0 invalid references |
| FactSalesTransactions.ProductId: required | PASS |  |
| FactSalesTransactions.ProductId: foreign key | PASS | 0 invalid references |
| FactSalesTransactions.LocationId: required | PASS |  |
| FactSalesTransactions.LocationId: foreign key | PASS | 0 invalid references |
| FactSalesTransactions.ChannelId: required | PASS |  |
| FactSalesTransactions.ChannelId: foreign key | PASS | 0 invalid references |
| FactSalesTransactions.CustomerId: required | PASS |  |
| FactSalesTransactions.CustomerId: foreign key | PASS | 0 invalid references |
| FactSalesTransactions.TransactionType: required | PASS |  |
| FactSalesTransactions.Quantity: required | PASS |  |
| FactSalesTransactions.NetAmount: required | PASS |  |
| FactSalesTransactions.COGS: required | PASS |  |
| FactSalesTransactions.DiscountAmount: required | PASS |  |
| DimSupplier: primary key unique | PASS |  |
| DimSupplier: manifest matches | PASS |  |
| DimSupplier.SupplierId: required | PASS |  |
| DimSupplier.SupplierName: required | PASS |  |
| DimSupplier.StandardLeadDays: required | PASS |  |
| DimSupplier.Terms: required | PASS |  |
| DimProduct: primary key unique | PASS |  |
| DimProduct: manifest matches | PASS |  |
| DimProduct.ProductId: required | PASS |  |
| DimProduct.SKU: required | PASS |  |
| DimProduct.ProductName: required | PASS |  |
| DimProduct.Category: required | PASS |  |
| DimProduct.SupplierId: required | PASS |  |
| DimProduct.SupplierId: foreign key | PASS | 0 invalid references |
| DimProduct.RetailPrice: required | PASS |  |
| DimProduct.OpeningUnitCost: required | PASS |  |
| DimProduct.Customizable: required | PASS |  |
| DimCustomer: primary key unique | PASS |  |
| DimCustomer: manifest matches | PASS |  |
| DimCustomer.CustomerId: required | PASS |  |
| DimCustomer.CustomerCode: required | PASS |  |
| DimCustomer.Segment: required | PASS |  |
| DimCustomer.State: required | PASS |  |
| DimCustomer.Synthetic: required | PASS |  |
| FactInventorySnapshots: primary key unique | PASS |  |
| FactInventorySnapshots: manifest matches | PASS |  |
| FactInventorySnapshots.SnapshotId: required | PASS |  |
| FactInventorySnapshots.SnapshotDate: required | PASS |  |
| FactInventorySnapshots.LocationId: required | PASS |  |
| FactInventorySnapshots.LocationId: foreign key | PASS | 0 invalid references |
| FactInventorySnapshots.ProductId: required | PASS |  |
| FactInventorySnapshots.ProductId: foreign key | PASS | 0 invalid references |
| FactInventorySnapshots.UnitsOnHand: required | PASS |  |
| FactInventorySnapshots.InventoryValue: required | PASS |  |
| FactInventorySnapshots.WeightedAverageCost: required | PASS |  |
| FactInventoryMovements: primary key unique | PASS |  |
| FactInventoryMovements: manifest matches | PASS |  |
| FactInventoryMovements.MovementId: required | PASS |  |
| FactInventoryMovements.MovementDate: required | PASS |  |
| FactInventoryMovements.LocationId: required | PASS |  |
| FactInventoryMovements.LocationId: foreign key | PASS | 0 invalid references |
| FactInventoryMovements.ProductId: required | PASS |  |
| FactInventoryMovements.ProductId: foreign key | PASS | 0 invalid references |
| FactInventoryMovements.MovementType: required | PASS |  |
| FactInventoryMovements.QuantityChange: required | PASS |  |
| FactInventoryMovements.ValueChange: required | PASS |  |
| FactInventoryMovements.ReferenceType: required | PASS |  |
| FactInventoryMovements.ReferenceId: required | PASS |  |
| DimLocation: primary key unique | PASS |  |
| DimLocation: manifest matches | PASS |  |
| DimLocation.LocationId: required | PASS |  |
| DimLocation.LocationName: required | PASS |  |
| DimLocation.LocationType: required | PASS |  |
| DimLocation.State: required | PASS |  |
| InjectedAnomalies: primary key unique | PASS |  |
| InjectedAnomalies: manifest matches | PASS |  |
| InjectedAnomalies.AnomalyId: required | PASS |  |
| InjectedAnomalies.Scenario: required | PASS |  |
| InjectedAnomalies.Entity: required | PASS |  |
| InjectedAnomalies.EntityId: required | PASS |  |
| InjectedAnomalies.Issue: required | PASS |  |
| InjectedAnomalies.StartDate: required | PASS |  |
| InjectedAnomalies.Cohort: required | PASS |  |
| Canceled orders never posted | PASS |  |
| Canceled orders never shipped | PASS |  |
| Exactly one shipment per fulfilled order | PASS |  |
| Duplicate webhooks never duplicate finalized sales | PASS |  |
| One ERP business order per source order | PASS |  |
| Sales line amount matches order line | PASS |  |
| Sales quantities match order lines | PASS |  |
| Returns reference actual completed sales | PASS |  |
| Return dates follow sales | PASS |  |
| Return belongs to correct order and product | PASS |  |
| Returns do not exceed sold quantities | PASS |  |
| Refunds use original discounted unit price | PASS |  |
| No negative physical inventory | PASS |  |
| No negative inventory value | PASS |  |
| Every monthly snapshot reconciles to movements | PASS | max quantity delta=0; value delta=0.00000000 |
| Transfers conserve units and value | PASS |  |
| Issues use moving weighted average cost | PASS |  |
| COGS reconciles to physical shipment issues | PASS |  |
| Received PO units and costs reconcile | PASS |  |
| No shipment occurs before order | PASS |  |
| SLA eligibility includes overdue open tickets | PASS |  |
| SLA compliance uses resolution deadline | PASS |  |
| MTTR uses closed tickets only | PASS |  |
| FactIntegrationEvents.EventDate: cutoff | PASS |  |
| FactShipments.OrderDate: cutoff | PASS |  |
| FactShipments.ShipDate: cutoff | PASS |  |
| FactSalesOrders.OrderDate: cutoff | PASS |  |
| FactReturns.ReturnDate: cutoff | PASS |  |
| FactPurchaseOrders.PODate: cutoff | PASS |  |
| FactPurchaseOrders.ReceivedDate: cutoff | PASS |  |
| FactSalesTransactions.PostingDate: cutoff | PASS |  |
| FactInventorySnapshots.SnapshotDate: cutoff | PASS |  |
| FactInventoryMovements.MovementDate: cutoff | PASS |  |
| Scenario C anomalies documented | PASS |  |
| Scenario E anomalies documented | PASS |  |
| SQL structural check 1 | PASS | 0 exceptions |
| SQL structural check 2 | PASS | 0 exceptions |
| SQL structural check 3 | PASS | 0 exceptions |
| SQL structural check 4 | PASS | 0 exceptions |
| SQL structural check 5 | PASS | 0 exceptions |
| SQL structural check 6 | PASS | 0 exceptions |
| SQL structural check 7 | PASS | 0 exceptions |
| SQL totals equal financial report mart | PASS |  |
| Scenario A: comparable Q3 revenue grows | PASS |  |
| Scenario A: comparable Q3 margin declines | PASS |  |
| Scenario B: inventory imbalance detectable | PASS |  |
| Scenario C: missing records detectable | PASS |  |
| Scenario C: duplicate webhooks present | PASS |  |
| Scenario D: SLA breaches present | PASS |  |
| Scenario E: approval delays present | PASS |  |