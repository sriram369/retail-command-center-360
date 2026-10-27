# Data flow and architecture
All source systems below are simulations. CSV files are the implemented extraction boundary.

```mermaid
flowchart LR
  A[Simulated POS / commerce / wholesale orders] --> B[Raw CSV extracts]
  C[Simulated ERP / purchasing / warehouse] --> B
  D[Mock integration events / support tickets] --> B
  B --> V[Python integrity and reconciliation checks]
  V --> S[SQLite analytical store]
  S --> M[Typed reporting marts and Excel tables]
  M --> P[Power Query / Power BI semantic model]
  P --> F[Executive financial performance]
  P --> I[Inventory and fulfillment]
  P --> H[Business systems health]
  V --> Q[Validation evidence and UAT]
  S --> E[Deterministic executive findings]
  E -. optional .-> AI[Grounded AI narrative]
```

Raw data is generated with stable keys. Processing derives additive reporting facts, current risk flags,
cutoff-aware reconciliation and historical inventory balances. AI never calculates financial totals.
