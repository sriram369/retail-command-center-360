let
    Source = Csv.Document(File.Contents(RootFolder & "/data/processed/ReportDailyFinance.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    EmptyToNull = Table.ReplaceValue(Headers, "", null, Replacer.ReplaceValue, Table.ColumnNames(Headers)),
    Typed = Table.TransformColumnTypes(EmptyToNull, {{"PostingDate", type date}, {"NetSales", type number}, {"COGS", type number}}, "en-US")
in
    Typed
