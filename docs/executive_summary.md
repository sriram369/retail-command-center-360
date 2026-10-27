# Executive summary
Aster & Co. is fictional. All findings below come from a reproducible synthetic dataset through September 30, 2026.

## What was investigated
Connected sales, returns, stock movements, purchasing, integration events and support incidents across seven stores, e-commerce and wholesale.
Validated 24,000 orders and 40,573 order lines using 275 automated checks.

## What the data indicates
Comparable Q3 net sales rose from $978,242 in 2025 to $1,075,282 in 2026, an increase of 9.9%.
Gross margin fell from 59.7% to 56.9%, a decline of 2.75 percentage points.
Absolute gross profit still increased; the deterioration is in margin, not a claim that every profit measure fell.

The full 18-month sample produces $6,626,438 net sales and $3,901,003 gross profit.
The favorable $1,589,213 budget variance must be interpreted against the independent synthetic plan assumptions.
Current stock carrying value is $1,913,203. There are 6 at-risk SKU/location pairs despite high total holdings.
Trailing-90-day average inventory equates to approximately 383 days of COGS, indicating slow stock circulation and substantial inventory investment.

There are 28 noncanceled e-commerce orders without ERP links, representing $4,133 of ordered-value exposure.
Of these, 4 lack any integration event. These would be missed by a failure-log-only report.
There were 306 correctly ignored duplicate webhook events and 355 failed integration attempts.
SLA compliance is 51.0%; resolved-ticket mean resolution time is 60.8 elapsed hours.

## Root causes and interpretation
The documented scenario increases pouch/travel discounts and supplier costs, raises demand for 20 pouch SKUs, restricts replenishment to two stores,
and introduces order mapping and purchasing delays. Operational records support a trace from demand to stock, PO timing, order sync and support tickets.
This is an engineered demonstration of diagnosis. It does not estimate a real company's causal loss.

## Management action
Assign the reconciliation queue to the business systems analyst and integration owner immediately.
Have operations validate shortage transfers and donor availability, then procurement expedite affected receipts.
Have the CFO and merchandising team review discount depth and cost changes at category/SKU level.
Have the support lead address repeat causes and overdue-ticket escalation.
Track queue age, promise adherence, margin and SLA compliance weekly. Measure subsequent results before claiming any benefit.

## Financial boundaries
Sales is a shipment-date operating proxy. Gross profit excludes operating expenses, freight allocation and payment processing costs.
Unreconciled ordered value is neither lost revenue nor financial savings. Stockout risk is a demand/availability signal, not a guaranteed stockout forecast.
