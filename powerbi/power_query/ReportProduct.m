let
    Source = Csv.Document(File.Contents(RootFolder & "/data/processed/ReportProduct.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    EmptyToNull = Table.ReplaceValue(Headers, "", null, Replacer.ReplaceValue, Table.ColumnNames(Headers)),
    Typed = Table.TransformColumnTypes(EmptyToNull, {{"MonthStart", type date}, {"ProductId", Int64.Type}, {"SKU", type text}, {"ProductName", type text}, {"Category", type text}, {"NetSales", type number}, {"COGS", type number}, {"UnitsSold", Int64.Type}, {"UnitsReturned", Int64.Type}, {"GrossProfit", type number}}, "en-US")
in
    Typed
