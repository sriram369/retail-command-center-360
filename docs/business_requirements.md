# Business requirements
Version 1.0. Fictional Aster & Co. Reporting period: April 2025–September 2026. USD.

## Business background and problem
Aster sells accessories through seven boutiques, e-commerce and wholesale, fulfilled through stores and one distribution center.
Simulated ERP, commerce, warehouse and support extracts contain separate views of the same transactions.
Management sees growth but cannot quickly distinguish margin pressure, misplaced stock and synchronization failures.

## Stakeholders and decisions
| Stakeholder | Decision | Accountability |
|---|---|---|
| CFO | Discount limits and margin review | Financial definitions and budget approval |
| COO | Replenishment priorities | Operational escalation and ownership |
| Retail operations | Store transfers | Validate donor stock and physical counts |
| Business systems analyst | Reconcile expected orders with ERP | Exception queue and master-data controls |
| IT support lead | Incident prioritization | SLA queue and repeat-incident prevention |

## Objectives and functional requirements
| ID | Requirement | Acceptance evidence |
|---|---|---|
| BR-01 | Explain sales, budget and gross margin by period and channel | Finance report totals reconcile to SQL within $0.01 |
| BR-02 | Identify current SKU/location replenishment risk | Snapshot units and value reconcile to all prior movements |
| BR-03 | Detect missing ERP orders even when no event exists | Anti-join compares noncanceled e-commerce orders with ERP links |
| BR-04 | Preserve event retries without duplicate finalized sales | Unique completed sales per order line and ERP links per order |
| BR-05 | Report SLA compliance and resolution time | Open overdue tickets count as breaches; open immature tickets excluded |
| BR-06 | Trace the affected assortment across processes | Stable product/order/PO identifiers and cohort evidence |
| BR-07 | Make findings reproducible and understandable | Seed, scripts, dictionary, SQL, DAX, UAT and demonstration guide |

## Nonfunctional requirements
Use synthetic customer IDs without names, addresses or contact details. No API credentials in code.
Reproduce with Python and documented dependencies. Preserve stable keys and local ISO dates.
Use three readable 16:9 report pages. Treat underlying facts and validation reports as auditable evidence.
Target refresh completion under five minutes on the supplied sample, measured rather than guaranteed.
Portfolio access uses the report owner's workspace; public sharing and production access controls are outside this demonstration.

## Assumptions and limitations
Revenue is a shipment-date sales proxy. All returns are restockable. Personalization uses finished goods; no bill of materials.
Inventory transfers complete within one simulated day. There is no tax, freight allocation, operating expense, general ledger or audited revenue recognition.
Store orders include reservations/pickups, allowing an unfulfilled order when stock is unavailable.
Historical budget is independently generated, not fitted to actual results. A favorable budget variance does not establish forecast quality.
No real NetSuite, Shopify or warehouse connection is claimed.

## Risks
Power BI browser features depend on tenant permissions and capacity. Preserve the workbook, CSVs, calculations and instructions if a feature is unavailable.
Synthetic scenarios illustrate analytical reasoning, not proof of a real company's losses or improvement results.
Do not claim UAT business sign-off or successful Power BI interactions until they have actually been observed.
