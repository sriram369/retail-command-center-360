let
    Source = Csv.Document(File.Contents(RootFolder & "/data/processed/ReportCategory.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    EmptyToNull = Table.ReplaceValue(Headers, "", null, Replacer.ReplaceValue, Table.ColumnNames(Headers)),
    Typed = Table.TransformColumnTypes(EmptyToNull, {{"MonthStart", type date}, {"Category", type text}, {"NetSales", type number}, {"COGS", type number}, {"UnitsSold", Int64.Type}, {"UnitsReturned", Int64.Type}, {"DiscountAmount", type number}, {"GrossProfit", type number}}, "en-US")
in
    Typed
