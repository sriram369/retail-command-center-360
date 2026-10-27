let
    Source = Csv.Document(File.Contents(RootFolder & "/data/processed/ReportMonthly.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    EmptyToNull = Table.ReplaceValue(Headers, "", null, Replacer.ReplaceValue, Table.ColumnNames(Headers)),
    Typed = Table.TransformColumnTypes(EmptyToNull, {{"MonthStart", type date}, {"NetSales", type number}, {"COGS", type number}, {"GrossProfit", type number}, {"SalesBudget", type number}, {"UnitsSold", Int64.Type}, {"UnitsReturned", Int64.Type}, {"FulfilledOrders", Int64.Type}, {"GrossMargin", type number}}, "en-US")
in
    Typed
