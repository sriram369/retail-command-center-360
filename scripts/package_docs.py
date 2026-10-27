"""Generate documentation from verified controls, schema and known scenario design."""
import json, re
from pathlib import Path
import pandas as pd
from generate_data import ROOT

def write(rel,text):
    p=ROOT/rel
    if rel=='README.md' and p.exists() and '<!-- portfolio-readme:curated -->' in p.read_text():
        return  # Preserve the maintained portfolio overview during data rebuilds.
    p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text.strip()+'\n')

def package():
    k=json.loads((ROOT/'reports/kpi_controls.json').read_text());v=json.loads((ROOT/'reports/validation_report.json').read_text())
    raw={p.stem:pd.read_csv(p,keep_default_na=False) for p in (ROOT/'data/raw').glob('*.csv')}
    money=lambda x:f'${x:,.0f}'
    write('requirements.txt','pandas>=2.2,<3\nnumpy>=1.26,<3\nPillow>=10,<13\nreportlab>=4,<5')
    write('.gitignore','__pycache__/\n*.pyc\n.DS_Store\n.env\n.venv/\nnode_modules\n*.inspect.ndjson\nreports/workbook_previews/\nreports/workbook_payload.json\nreports/operations_payload.json\n')
    write('DESIGN.md','''# Aster & Co. report design
The report should make one idea memorable: growth needs operational control.

Use a 1600 × 900, 16:9 canvas with a 48 px outer margin and 24 px gutters.
Use Segoe UI in Power BI, 28 px page titles, 14 px chart titles, 12 px labels and 32 px KPI values.
Use deep navy #14233B for headings, teal #0F766E for actual results, slate #325E85 for secondary series,
amber #C48B42 for budget or caution, and muted red #B54738 for adverse exceptions.
Background #F7F9FB, chart surfaces #FFFFFF, secondary text #63748A, gridlines #E5EAF0.
No gradients, decorative illustrations, 3D charts or repeated pie charts.
Use a thin navy top rail, Aster & Co. wordmark, consistent three-page navigation and a visible reporting cutoff.
Each page has four primary KPI cards, two main charts and one detail/action section. Secondary KPIs belong in tooltips or the detail section.
Use rounded corners of 8 px for panels where supported, consistent number units and accessible labels alongside color.
Charts begin at zero for bars. Percentage line charts may use a clearly labeled nonzero axis. Separate monetary and percentage axes.
Every page ends with a concrete management action and owner. Tooltips define numerator, denominator and date basis.
Current inventory and reconciliation exceptions are as of September 30, 2026 and do not change with the historical month slicer.
Previews are rendered from validated data and must be labeled as previews until native Power BI screenshots exist.
''')
    theme={'name':'Aster Executive | Navy & Teal','dataColors':['#0F766E','#325E85','#C48B42','#8B9CAF','#B54738','#14233B'],
        'background':'#F7F9FB','foreground':'#14233B','tableAccent':'#0F766E',
        'good':'#0F766E','neutral':'#C48B42','bad':'#B54738',
        'textClasses':{'title':{'fontFace':'Segoe UI','fontSize':14,'color':'#14233B'},
          'label':{'fontFace':'Segoe UI','fontSize':11,'color':'#63748A'},
          'callout':{'fontFace':'Segoe UI','fontSize':30,'color':'#14233B'},
          'header':{'fontFace':'Segoe UI','fontSize':12,'color':'#14233B'}}}
    write('powerbi/theme.json',json.dumps(theme,indent=2))
    write('docs/business_requirements.md',f'''# Business requirements
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
''')
    write('docs/functional_requirements.md','''# Functional specification
## Pages and date semantics
Finance uses shipment and return posting dates, inventory uses the selected snapshot/as-of date,
fulfillment uses order cohorts, integration trends use event dates, and support trends use ticket-open cohorts.
Label each date basis. Do not present ticket-cohort SLA compliance as compliance among tickets resolved that month.
Use shared date and location dimensions with single-direction filters from dimensions to facts.
Never join two transaction facts directly for aggregate calculations.

## Behavior
Default finance view covers the available 18 months; Q3 2026 vs Q3 2025 is the comparable headline.
Finance month and channel slicers affect finance tables. Budget is only valid at month/channel/location grain.
Category and product charts have no allocated budget. In the compact browser workbook, category summaries cover all channels.
Current inventory and unresolved-order tables are cutoff snapshots; disable historical month interactions for these visuals.
Click a store/channel to filter applicable finance visuals. Use order/SKU tables for investigation.
Native drillthrough is configured only after the model and report support it; the reproducible design specifies an OrderId or SKU detail view.

## Calculations
Net sales includes signed sale and return postings. COGS uses moving weighted average issue costs and original-cost return reversals.
Net sales less COGS is gross profit. Ratios divide aggregated numerators by aggregated denominators.
Units sold is positive sale quantity; units returned is absolute negative quantity. Return rate is posting-period returns / sale units, not a mature cohort return probability.
Average order value is period net sales / distinct shipped orders in the same posting period. Returns can relate to older orders.
Integration success and failure rates exclude ignored duplicates, which have a separate control count.
SLA denominator includes resolved tickets and unresolved tickets whose deadlines have passed at cutoff.
MTTR is average elapsed hours for resolved tickets. SLA clocks run continuously, not business hours.
Repeat incidents are subsequent tickets sharing a defined root-cause key, ordered by opened timestamp and TicketId.

## Refresh, security and exceptions
Refresh source data, validate, build marts, reconcile, run tests, then update the report.
Block release on accidental errors. Keep known operational failures visible in the exception queue.
No scheduled cloud refresh, gateway, RLS enforcement or notification automation is claimed as implemented.
Recommended production access: executives companywide, operations by location, support by queue. Test RLS separately before deployment.
High-priority unresolved sync orders are cohort-affected orders without an ERP link; order value is exposure, not established lost revenue.
''')
    write('docs/data_flow_diagram.md','''# Data flow and architecture
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
''')
    write('docs/entity_relationship_diagram.md','''# Entity relationships
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
''')
    grains={'DimDate':'one calendar date','DimProduct':'one finished-goods SKU','DimStore':'one physical store',
        'DimLocation':'one physical stocking location','DimChannel':'one sales channel','DimSupplier':'one fictional supplier',
        'DimCustomer':'one anonymous synthetic customer profile','FactSalesOrders':'one source customer order',
        'FactSalesOrderLines':'one product line per source order','FactShipments':'one complete order shipment',
        'FactReturns':'one returned unit of an actual completed sales line','FactSalesTransactions':'one signed sales-line or return posting',
        'FactPurchaseOrders':'one single-SKU purchase order','FactInventoryMovements':'one signed stock/value movement',
        'FactInventorySnapshots':'one month-end / SKU / location balance','FactBudget':'one month / channel / location budget',
        'FactIntegrationEvents':'one received mock integration event or retry','FactERPOrderLinks':'one successfully created simulated ERP order',
        'FactSupportTickets':'one order-linked incident ticket','InjectedAnomalies':'one documented order or PO exception'}
    notes={'NetAmount':'Signed sales amount after discount; negative for refunds. Excludes tax and shipping.',
      'COGS':'Signed moving-average issue cost, reversed at original issue cost on restockable returns.',
      'OrderedAmount':'Order-line amount after discount. Not booked sales until a sale transaction exists.',
      'OpeningUnitCost':'Opening inventory unit cost, not the current issue cost.',
      'RetailPrice':'Undiscounted retail list price in USD.', 'SalesBudget':'Independent monthly net-sales target at channel/location grain.',
      'InventoryValue':'Closing carrying value in USD; not additive over snapshot dates.',
      'WeightedAverageCost':'Closing value divided by on-hand units; zero when no units remain.',
      'ValueChange':'Signed stock carrying-value change in USD to four decimals.',
      'QuantityChange':'Signed stock units; receipts positive and issues negative.',
      'ResolutionHours':'Elapsed hours to resolution, blank for open tickets.',
      'SLAEligible':'1 for resolved tickets or open tickets past their deadline at cutoff.',
      'SLAMet':'1 only when resolved on or before the SLA deadline.',
      'PromisedDate':'Customer promised ship/fulfillment date, not promised delivery.',
      'AvailableDate':'Earliest date the source order may be fulfilled after processing or synchronization.',
      'PromisedReceiptDate':'Approved PO promise date; may lie after the reporting cutoff.',
      'ApprovalDays':'Simulated approval duration; future approval dates are not exposed as completed approvals.',
      'PayloadSKU':'Untrusted mock source payload; UNKNOWN-SKU represents a quarantined mapping error, not an invalid analytical FK.',
      'Deduplicated':'1 if a duplicate webhook is ignored without creating another sale.',
      'Cohort':'Scenario truth flag for the targeted assortment. Hidden from business report; used for scenario verification.',
      'ScenarioAffected':'Scenario truth flag for intentionally delayed purchasing.',
      'RepeatKey':'Root-cause grouping for repeat-incident counts, not a duplicate ticket identifier.',
      'TransferId':'Shared reference between an equal and opposite transfer pair; blank on other movements.',
      'ReferenceId':'Polymorphic movement reference; interpreted together with ReferenceType.',
      'Synthetic':'Always 1. Profiles contain no names or contact information.',
      'DiscountAmount':'Line discount before returns; do not subtract again from NetAmount.',
      'PaymentStatus':'Captured or Voided. Captured is a source order state, not an accounting cash ledger.',
      'RefundAmount':'Original discounted unit price rounded to cents using Python round; actual refund amount is authoritative.'}
    fields=[]; dictionary=['# Data dictionary','', 'Synthetic data. USD. Local dates use America/New_York. Empty fields are permitted only for documented lifecycle or payload fields.','']
    for name,df in sorted(raw.items()):
        dictionary.extend([f'## {name}',f'Grain: {grains[name]}. Rows: {len(df):,}.','', '| Field | Type | Meaning |','|---|---|---|'])
        for col in df:
            if col.endswith('Id') and pd.api.types.is_numeric_dtype(df[col]):typ='integer'
            elif pd.api.types.is_numeric_dtype(df[col]):typ='decimal' if pd.api.types.is_float_dtype(df[col]) else 'integer'
            elif col.endswith('Date') or col=='Date':typ='ISO date'
            elif col.endswith('At') or col=='SLADeadline':typ='ISO timestamp'
            else:typ='text'
            desc=notes.get(col,('Stable identifier for '+col[:-2]+'.' if col.endswith('Id') else re.sub(r'(?<!^)(?=[A-Z])',' ',col).strip()+'.'))
            dictionary.append(f'| {col} | {typ} | {desc} |');fields.append({'Table':name,'Grain':grains[name],'Field':col,'Type':typ,'Definition':desc})
        dictionary.append('')
    write('data/data_dictionary/data_dictionary.md','\n'.join(dictionary))
    pd.DataFrame(fields).to_csv(ROOT/'data/data_dictionary/data_dictionary.csv',index=False)
    write('docs/table_definitions.md','\n'.join(['# Table definitions and granularity','', '| Table | Grain | Rows |','|---|---|---|']+
        [f'| {n} | {grains[n]} | {len(d):,} |' for n,d in sorted(raw.items())])+'''

Identifiers ending in Id are stable keys; each table's primary key is its entity key (Date for DimDate, ReturnId for FactReturns).
DimStore.StoreId shares location IDs 1–7 with the store rows in DimLocation. Use DimLocation in the semantic model to avoid parallel filter paths.
FactBudget is unique on MonthStart, ChannelId and LocationId. Snapshots are unique on SnapshotDate, ProductId and LocationId.
ERP links are unique on both OrderId and ERPOrderId. FactShipments allows at most one shipment per OrderId in this simplified model.
Raw tables are retained for audit. SQLite is a rebuildable analytical store; validation enforces integrity even though pandas loading does not declare database foreign-key constraints.
''')
    write('docs/data_mapping.md','''# Source-to-target mapping
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
''')
    write('docs/process_improvement.md',f'''# Business process improvement
The changes below are recommendations. No production process has been changed.

## Before
```mermaid
flowchart LR
 A[Order arrives] --> B[Integration runs]
 B --> C[Failures remain in separate logs]
 C --> D[Finance compares spreadsheets]
 D --> E[Manual ticket and ad hoc retry]
 E --> F[Unclear ownership and duplicate retry risk]
```

## After
```mermaid
flowchart LR
 A[Expected source orders] --> B[Compare with unique ERP business keys]
 B --> C{{Missing / failed / delayed?}}
 C -- yes --> D[Prioritize by age and order exposure]
 D --> E[Assign analyst and SLA]
 E --> F[Validate SKU mapping before controlled retry]
 F --> G[Confirm one ERP order and close exception]
 C -- no --> G
 G --> H[Daily control totals and weekly root-cause review]
```

| Priority | Action | Owner | Proposed success measure |
|---|---|---|---|
| P1 / first week | Work {k['unreconciled_orders']} unresolved orders with {money(k['unreconciled_order_value'])} ordered-value exposure | Business systems analyst | Every exception owned and reconciled or explained |
| P1 / first week | Correct targeted SKU mapping and replay safely | Integration owner | No duplicate ERP business orders, declining unresolved queue |
| P1 / first week | Review {k['stockout_risk_sku_locations']} at-risk SKU/location pairs and overdue customer promises | Inventory lead | Backlog cleared with approved transfers or supplier expedite |
| P2 / first month | Set discount guardrails and category cost reviews | Merchandising / CFO | Stabilize margin with measured price-volume tradeoffs |
| P2 / first month | Introduce approval delegation and supplier promise tracking | Procurement lead | Reduce cohort approval and delivery delay |
| P2 / first month | Assign repeat root-cause tickets and SLA escalation | IT support lead | Raise SLA compliance from {k['sla_compliance']:.1%} baseline |

Targets are proposed controls, not claimed results. Transfer quantities require donor validation and consideration of shared warehouse stock before execution.
Replenishment suggestions are independent candidate quantities, not a globally optimized allocation plan.
''')
    write('docs/executive_summary.md',f'''# Executive summary
Aster & Co. is fictional. All findings below come from a reproducible synthetic dataset through September 30, 2026.

## What was investigated
Connected sales, returns, stock movements, purchasing, integration events and support incidents across seven stores, e-commerce and wholesale.
Validated {len(raw['FactSalesOrders']):,} orders and {len(raw['FactSalesOrderLines']):,} order lines using {v['check_count']} automated checks.

## What the data indicates
Comparable Q3 net sales rose from {money(k['q3_comparison'][0]['NetSales'])} in 2025 to {money(k['q3_comparison'][1]['NetSales'])} in 2026, an increase of {k['q3_sales_growth']:.1%}.
Gross margin fell from {k['q3_comparison'][0]['GrossMargin']:.1%} to {k['q3_comparison'][1]['GrossMargin']:.1%}, a decline of {-k['q3_margin_change_pp']:.2f} percentage points.
Absolute gross profit still increased; the deterioration is in margin, not a claim that every profit measure fell.

The full 18-month sample produces {money(k['net_sales'])} net sales and {money(k['gross_profit'])} gross profit.
The favorable {money(k['sales_vs_budget'])} budget variance must be interpreted against the independent synthetic plan assumptions.
Current stock carrying value is {money(k['inventory_value'])}. There are {k['stockout_risk_sku_locations']} at-risk SKU/location pairs despite high total holdings.
Trailing-90-day average inventory equates to approximately {k['days_inventory_90d']:.0f} days of COGS, indicating slow stock circulation and substantial inventory investment.

There are {k['unreconciled_orders']} noncanceled e-commerce orders without ERP links, representing {money(k['unreconciled_order_value'])} of ordered-value exposure.
Of these, {k['missing_event_orders']} lack any integration event. These would be missed by a failure-log-only report.
There were {k['deduplicated_events']} correctly ignored duplicate webhook events and {k['failed_integration_events']} failed integration attempts.
SLA compliance is {k['sla_compliance']:.1%}; resolved-ticket mean resolution time is {k['mean_resolution_hours']:.1f} elapsed hours.

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
''')
    write('docs/uat_test_plan.md',f'''# User acceptance testing
Automated data acceptance: {v['check_count']} checks passed. Business stakeholder sign-off is pending.
Native report interaction checks must be recorded separately in reports/powerbi_status.md.

| ID | Scenario / action | Expected result | Execution status |
|---|---|---|---|
| UAT-01 | Sum signed sale and return postings | Net sales {money(k['net_sales'])}, SQL matches within $0.01 | Automated PASS |
| UAT-02 | Compare monthly channel/location budget | Each budget allocated once; no order-line multiplication | Automated PASS |
| UAT-03 | Reconcile every monthly stock snapshot | Zero unit difference; value difference below $0.001 | Automated PASS |
| UAT-04 | Compare expected commerce orders to ERP | {k['unreconciled_orders']} unresolved, including {k['missing_event_orders']} without events | Automated PASS |
| UAT-05 | Inspect duplicate webhooks | {k['deduplicated_events']} ignored; one finalized sale per line | Automated PASS |
| UAT-06 | Inspect incorrect SKU payload | Quarantined payload does not create invalid product FK | Automated PASS |
| UAT-07 | Include overdue open tickets in SLA | Correct eligible population and breach count | Automated PASS |
| UAT-08 | Validate refunds and cost reversals | Actual prior sale, valid quantity and original unit price/cost | Automated PASS |
| UAT-09 | Inject an invalid order-line reference in a disposable database | Orphan detector returns the injected record | See unittest run |
| UAT-10 | Inject a duplicate ERP link in a disposable database | Duplicate business-key query detects it | See unittest run |
| UAT-11 | Select month and channel in finance page | Correct totals and chart filtering | Pending native report test |
| UAT-12 | Change historical month on inventory page | Current snapshot remains labeled Sep 30 and unaffected | Pending native report test |
| UAT-13 | Navigate between all three pages | Consistent layout and no empty or erroneous visuals | Pending native report test |
| UAT-14 | Reopen saved report | Model and report persist and match control totals | Pending native report test |
| UAT-15 | Test zero denominators and immature open tickets | Blank ratio when no eligible population; immature open ticket excluded | See unittest run |

Use tests/test_controls.py for controlled invalid-reference, duplicate, cancellation and SLA boundary tests.
Known operational failures are expected business cases; accidental corruption must fail validation.
''')
    write('docs/interview_demo.md','''# Five-minute interview demonstration
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
''')
    write('docs/resume_bullets.md',f'''# Resume wording
Use only after reviewing and being able to explain the work. Disclose synthetic data and portfolio scope.

- Developed a synthetic retail analytics portfolio spanning {len(raw['FactSalesOrders']):,} orders and {len(raw['DimProduct'])} SKUs, with Python generation, SQL analysis and {v['check_count']} automated integrity and reconciliation checks.
- Modeled sales, returns, perpetual weighted-average inventory, purchasing and order-linked system exceptions; identified {k['q3_sales_growth']:.1%} Q3 sales growth alongside a {-k['q3_margin_change_pp']:.2f}-point gross-margin decline in the simulated business.
- Produced Power BI-ready reporting data, DAX and Power Query definitions, requirements, data mappings and a UAT plan to support financial, inventory and systems-health reporting.

Replace the third bullet with an actual Power BI implementation claim only after the native report has been saved and tested.
Do not claim production deployment, real vendor integration, stakeholder sign-off, revenue recovered or cost savings.
''')
    write('docs/assumptions_and_limitations.md','''# Assumptions and limitations
- Company, suppliers, customers and transactions are fictional. A fixed seed creates one consistent sample.
- 18 months of data begins April 2025; prior-year comparisons before April 2026 lack complete comparable history.
- Sales is recognized at complete shipment as an operational proxy. No general ledger or revenue allocation contract model exists.
- All returns are restockable, one unit per return record, with original issue cost restored. No damage write-off or chargeback modeling.
- Inventory uses perpetual moving weighted average and four-decimal valuation. Original unit-cost reference is not a current standard cost.
- Transfers are same-day stock movements. There is no in-transit inventory, component assembly, split shipment or multi-currency accounting.
- Store orders include reservations and pickups. Fulfillment means shipment/collection processing, not customer delivery.
- Current stock risk uses 28-day ordered demand, reserved backlog and protection days; recommendations are independent candidates.
- Repeat incidents group by configured root-cause key. This is not a learned incident classifier.
- SLA is elapsed time; 24 hours for high severity and 72 hours for medium severity. No pause or business-hours calendar.
- The compact Excel report model aggregates financials by month/channel/location and categories by month/category. It does not support every possible drillthrough.
- The full CSV/SQLite model retains order-line detail for additional analysis. No live refresh or actual systems integration is implemented.
- Python/SQL tests do not prove that DAX compiles or that report interactions work. Native checks and limitations are recorded separately.
- Optional AI output must cite supplied metric keys. It never changes deterministic business totals.
''')
    write('README.md',f'''# Retail Command Center 360
**Find margin pressure, inventory imbalance and missing orders in one connected retail intelligence project.**

Aster & Co. is a fictional accessories retailer. This portfolio uses reproducible synthetic data and simulated ERP, commerce, warehouse and support records.
Reporting cutoff: **September 30, 2026**. Currency: USD. Data period: April 2025–September 2026.

## Start here
1. Read [the executive summary](docs/executive_summary.md) for the business story.
2. Check [Power BI implementation status](reports/powerbi_status.md) for what has actually been built and tested.
3. Open [the Power BI-ready workbook](data/retail360_powerbi.xlsx) or use the detailed CSVs and SQLite store.
4. Follow [the build guide](powerbi/build_guide.md) and [the five-minute demonstration](docs/interview_demo.md).

## Business problem
Sales are growing, but category discounts, supplier cost increases, inventory allocation and synchronization failures weaken operating performance.
The analyst must connect the symptoms, verify the numbers, and assign practical next actions.

## Evidence from the sample
| Finding | Verified result |
|---|---|
| Comparable Q3 sales growth | {k['q3_sales_growth']:.1%} |
| Comparable Q3 gross margin | {k['q3_comparison'][0]['GrossMargin']:.1%} → {k['q3_comparison'][1]['GrossMargin']:.1%} |
| Unreconciled commerce orders | {k['unreconciled_orders']}, including {k['missing_event_orders']} with no event |
| Ordered-value exposure | {money(k['unreconciled_order_value'])}, not established lost revenue |
| Current at-risk SKU/location pairs | {k['stockout_risk_sku_locations']} |
| SLA compliance | {k['sla_compliance']:.1%} |
| Automated dataset checks | {v['check_count']} passed, zero invalid references |

## Architecture
```mermaid
flowchart LR
 A[Simulated retail sources] --> B[Seeded Python / raw CSV]
 B --> C[Validation and reconciliation]
 C --> D[SQLite / SQL analysis]
 D --> E[Excel and reporting marts]
 E --> F[Power Query / Power BI]
 F --> G[Finance / Inventory / Systems health]
```

## Dashboard overview
**Executive financial performance:** net sales, gross profit/margin, budget and channel/category trends.
**Inventory and fulfillment:** stock carrying value, SKU/location risk, customer promises and purchasing.
**Business systems health:** failed attempts, expected orders missing ERP links, ticket SLA and corrective ownership.

The visual direction uses navy, teal and amber, restrained cards and clear action tables. Any generated preview is labeled as such; native screenshots are kept separately.

## Technology and model
Python, pandas, NumPy, SQLite SQL, Power Query M and DAX. The optional Excel export uses the artifact-tool authoring runtime.
The logical dataset has {len(raw)} tables, including {len(raw['FactSalesOrders']):,} orders, {len(raw['FactSalesOrderLines']):,} order lines,
{len(raw['DimProduct'])} SKUs, {len(raw['DimSupplier'])} suppliers and {len(raw['FactInventorySnapshots']):,} monthly SKU/location snapshots.
See [ERD](docs/entity_relationship_diagram.md), [dictionary](data/data_dictionary/data_dictionary.md) and [model configuration](powerbi/model_documentation.md).

## Reproduce the analytical core
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/generate_data.py
python scripts/build_dataset.py
python scripts/reconcile_orders.py
python scripts/validate_data.py
python -m unittest discover -s tests -v
python scripts/package_docs.py
python scripts/render_previews.py
```
On Windows activate `.venv\\Scripts\\activate` instead. No API key is required.
The core CSV/SQLite pipeline is independent of the optional Excel writer. Export instructions are in the Power BI build guide.
To explore SQL, open `data/processed/retail360.sqlite` in a SQLite client and run `sql/business_analysis.sql`.
The seed and SHA-256 row manifests are saved in `data/scenario.json` and `data/manifest.json`.

## Recommendations
Assign unresolved orders, correct mapping before idempotent replay, validate shortage transfers, review purchase approval delays,
introduce category discount controls and address recurring incident causes. Owners and proposed measures are in [process improvements](docs/process_improvement.md).
No production benefits are claimed.

## Project documentation
[BRD](docs/business_requirements.md) · [Functional specification](docs/functional_requirements.md) ·
[Data flow](docs/data_flow_diagram.md) · [Mapping](docs/data_mapping.md) · [UAT](docs/uat_test_plan.md) ·
[Validation evidence](reports/validation_report.md) · [Resume wording](docs/resume_bullets.md)

## Limitations and next steps
Sales is a shipment-date operational proxy. No OPEX, tax, freight allocation or audited accounting profit is available.
Full-detail data supports deeper analysis; the browser workbook uses compact reporting grains.
Production refresh, real system connections, RLS deployment and operational changes require additional implementation and acceptance.
See [assumptions](docs/assumptions_and_limitations.md) and [Power BI status](reports/powerbi_status.md).
''')
    print('Documentation generated from verified controls.')

if __name__=='__main__':package()
