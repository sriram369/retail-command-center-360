# Entity relationships
This logical ERD shows record ownership. The Power BI star uses dimensions to facts with single-direction filtering;
logical transactional links are not all activated as Power BI relationships.

```mermaid
erDiagram
  DimCustomer ||--o{ FactSalesOrders : places
  DimChannel ||--o{ FactSalesOrders : sells
  DimLocation ||--o{ FactSalesOrders : serves
  FactSalesOrders ||--|{ FactSalesOrderLines : contains
  DimProduct ||--o{ FactSalesOrderLines : ordered
  FactSalesOrders ||--o| FactShipments : fulfills
  FactSalesOrderLines ||--o{ FactReturns : returned
  FactSalesOrderLines ||--o{ FactSalesTransactions : posts
  FactSalesOrders ||--o{ FactIntegrationEvents : logs
  FactSalesOrders ||--o| FactERPOrderLinks : reconciles
  FactSalesOrders ||--o{ FactSupportTickets : investigates
  DimProduct ||--o{ FactPurchaseOrders : replenished
  DimSupplier ||--o{ FactPurchaseOrders : supplies
  DimProduct ||--o{ FactInventoryMovements : moves
  DimLocation ||--o{ FactInventoryMovements : holds
  DimProduct ||--o{ FactInventorySnapshots : values
  DimLocation ||--o{ FactInventorySnapshots : snapshots
```
