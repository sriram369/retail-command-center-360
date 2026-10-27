# User acceptance testing
Automated data acceptance: 275 checks passed. Business stakeholder sign-off is pending.
Native report interaction checks must be recorded separately in reports/powerbi_status.md.

| ID | Scenario / action | Expected result | Execution status |
|---|---|---|---|
| UAT-01 | Sum signed sale and return postings | Net sales $6,626,438, SQL matches within $0.01 | Automated PASS |
| UAT-02 | Compare monthly channel/location budget | Each budget allocated once; no order-line multiplication | Automated PASS |
| UAT-03 | Reconcile every monthly stock snapshot | Zero unit difference; value difference below $0.001 | Automated PASS |
| UAT-04 | Compare expected commerce orders to ERP | 28 unresolved, including 4 without events | Automated PASS |
| UAT-05 | Inspect duplicate webhooks | 306 ignored; one finalized sale per line | Automated PASS |
| UAT-06 | Inspect incorrect SKU payload | Quarantined payload does not create invalid product FK | Automated PASS |
| UAT-07 | Include overdue open tickets in SLA | Correct eligible population and breach count | Automated PASS |
| UAT-08 | Validate refunds and cost reversals | Actual prior sale, valid quantity and original unit price/cost | Automated PASS |
| UAT-09 | Inject an invalid order-line reference in a disposable database | Orphan detector returns the injected record | Automated PASS (seven control tests) |
| UAT-10 | Inject a duplicate ERP link in a disposable database | Duplicate business-key query detects it | Automated PASS (seven control tests) |
| UAT-11 | Select Q3 2026 in finance | $1,075,281.59 sales; 56.9% margin; 18.4% budget variance | Native PASS; separate channel slicer not configured |
| UAT-12 | Apply Q3 date context to current snapshot measures | Inventory $1,913,202.67 and risk 6 unchanged; current page has no date slicer | Native DAX PASS |
| UAT-13 | Navigate between all three pages | Consistent layout and no empty or erroneous visuals | Native PASS |
| UAT-14 | Reopen saved report | Model and report persist and match control totals | Native PASS |
| UAT-15 | Test zero denominators and immature open tickets | Blank ratio when no eligible population; immature open ticket excluded | Automated PASS (seven control tests) |

Use tests/test_controls.py for controlled invalid-reference, duplicate, cancellation and SLA boundary tests.
Known operational failures are expected business cases; accidental corruption must fail validation.
