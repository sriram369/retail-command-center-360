"""Reproducible additive TMDL for the five supplemental Excel tables."""
from pathlib import Path
import re
from generate_data import ROOT

def prepare():
    formulas={
        'Eligible Orders':'SUM(ReportFulfillment1[EligibleOrders])',
        'Fulfilled Orders':'SUM(ReportFulfillment1[FulfilledOrders])',
        'Fulfillment Rate':'DIVIDE([Fulfilled Orders], [Eligible Orders])',
        'Late Orders':'SUM(ReportFulfillment1[LateOrders])',
        'Open Late Orders':'SUM(ReportFulfillment1[OpenLateOrders])',
        'Average Fulfillment Duration':'DIVIDE(SUM(ReportFulfillment1[FulfillmentDays]), [Fulfilled Orders])',
        'Low Stock SKU Location Count':'SUM(ReportInventory[LowStock])',
        'SLA Compliance Rate':'DIVIDE(SUM(ReportTickets4[SLAMet]), SUM(ReportTickets4[SLAEligible]))',
        'Mean Time to Resolution':'DIVIDE(SUM(ReportTickets4[ResolutionHours]), SUM(ReportTickets4[ResolvedCount]))',
        'Open Support Tickets':'SUM(ReportTickets4[OpenCount])',
        'Repeat Incidents':'SUM(ReportTickets4[RepeatIncident])',
        'Ticket Count':'COUNTROWS(ReportTickets4)',
        'High-Priority Exceptions':'CALCULATE(COUNTROWS(ReportReconciliation6), ReportReconciliation6[SyncStatus] = "Awaiting reconciliation", ReportReconciliation6[Cohort] = 1)',
        'Average Inventory Value 90D':'''VAR EndDate = MAX(DimDate7[Date])
VAR DataStartDate = CALCULATE(MIN(DimDate7[Date]), REMOVEFILTERS(DimDate7))
RETURN IF(EndDate - 89 >= DataStartDate && NOT ISFILTERED(DimProduct10) && NOT ISFILTERED(DimLocation9) && NOT ISFILTERED(DimChannel8), CALCULATE(AVERAGE(ReportDailyInventory3[InventoryValue]), REMOVEFILTERS(DimDate7), DATESBETWEEN(DimDate7[Date], EndDate - 89, EndDate)))''',
        'COGS 90D':'''VAR EndDate = MAX(DimDate7[Date])
RETURN CALCULATE(SUM(ReportDailyFinance2[COGS]), REMOVEFILTERS(DimDate7), DATESBETWEEN(DimDate7[Date], EndDate - 89, EndDate))''',
        'Inventory Turnover 90D Annualized':'DIVIDE([COGS 90D], [Average Inventory Value 90D]) * 365 / 90',
        'Days of Inventory on Hand':'DIVIDE([Average Inventory Value 90D], [COGS 90D]) * 90',
        'Product Net Sales':'SUM(ReportProduct5[NetSales])',
        'Product Gross Profit':'SUM(ReportProduct5[GrossProfit])',
        'Product Gross Margin %':'DIVIDE([Product Gross Profit], [Product Net Sales])',
    }
    # Re-declare currency measures with their original expressions and improved precision.
    original=(ROOT/'powerbi/browser_measures.tmdl').read_text()
    for name,expression,fmt in re.findall(r"\t\tmeasure '([^']+)' = (.*?)\n\t\t\tformatString: ([^\n]+)", original, re.S):
        if '"$"' in fmt: formulas[name]=expression
    lines=['createOrReplace','','\tref table _Measures']
    for name,expression in formulas.items():
        if name.endswith('Rate') or '%' in name: fmt='0.0%'
        elif any(word in name for word in ['Sales','COGS','Profit','Budget','Value']): fmt='"$"#,##0.00'
        elif any(word in name for word in ['Duration','Resolution','Turnover','Days of']): fmt='0.00'
        else: fmt='#,##0'
        expression=' '.join(expression.splitlines())
        lines.append(f"\t\tmeasure '{name}' = {expression}")
        lines.extend([f'\t\t\tformatString: {fmt}','\t\t\tdisplayFolder: Retail360',''])
    relationships=[
        ('ReportFulfillment1.MonthStart','DimDate7.Date'),
        ('ReportFulfillment1.ChannelId','DimChannel8.ChannelId'),
        ('ReportFulfillment1.LocationId','DimLocation9.LocationId'),
        ('ReportDailyFinance2.PostingDate','DimDate7.Date'),
        ('ReportDailyInventory3.BalanceDate','DimDate7.Date'),
        ('ReportTickets4.OpenDate','DimDate7.Date'),
        ('ReportProduct5.MonthStart','DimDate7.Date'),
        ('ReportProduct5.ProductId','DimProduct10.ProductId'),
    ]
    for idx,(source,target) in enumerate(relationships,10):
        lines.extend([f'\trelationship Retail360_{idx}',f'\t\tfromColumn: {source}',f'\t\ttoColumn: {target}',''])
    (ROOT/'powerbi/operations_extension.tmdl').write_text('\n'.join(lines))
    (ROOT/'powerbi/dax_measures/operations_model.dax').write_text('\n\n'.join(f'{n} =\n{e}' for n,e in formulas.items()))
    print(f'{len(formulas)} additive or updated measures; {len(relationships)} relationships')

if __name__=='__main__': prepare()
