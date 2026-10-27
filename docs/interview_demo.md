# Five-minute interview demonstration
## 0:00–0:40 / business problem
“I modeled a fictional retailer where sales growth masked margin pressure and operational exceptions. All data is synthetic.
I connected business requirements to a dimensional model, validation rules and three reporting views.”

## 0:40–1:40 / executive view
Show comparable Q3 sales and gross margin. Explain the difference between margin decline and absolute gross profit.
Show the signed sales/returns ledger and budget grain. Explain why order headers and order lines are never added together.

## 1:40–2:40 / inventory and fulfillment
Show high total stock alongside SKU/location risk. Trace one shortage to demand, location balance and purchase timing.
Explain moving weighted average cost, original-cost return reversal and historical movement reconciliation.

## 2:40–3:40 / systems health
Show unresolved commerce orders. Explain that an absent webhook has no failed event to count, so source-to-ERP comparison is required.
Show that duplicate webhooks remain visible but never become duplicate finalized sales. Explain SLA denominator treatment.

## 3:40–4:30 / evidence
Show validation_report.md, the SQL queries, metric definitions and UAT plan. Describe one deliberately corrupted test fixture.
Distinguish Python/SQL validation from native Power BI/DAX execution and stakeholder acceptance.

## 4:30–5:00 / action and limitations
Prioritize order reconciliation, stock allocation, discount review and repeat-incident fixes. Assign owners.
State that savings and real integrations are not claimed. Explain what a production implementation would add.

## Questions to rehearse
Why this fact grain? Why does inventory value not sum across months? How do you avoid double-counting budgets?
What happens when an order has no event? What if a retry repeats? What does an open overdue ticket do to SLA?
Why is ordered revenue different from posted sales? What would invalidate the stockout recommendation?
What did you personally review, change and verify? Which parts were assisted by AI?
