let
    Source = Csv.Document(File.Contents(RootFolder & "/data/raw/FactBudget.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    EmptyToNull = Table.ReplaceValue(Headers, "", null, Replacer.ReplaceValue, Table.ColumnNames(Headers)),
    Typed = Table.TransformColumnTypes(EmptyToNull, {{"BudgetId", Int64.Type}, {"MonthStart", type date}, {"ChannelId", Int64.Type}, {"LocationId", Int64.Type}, {"SalesBudget", type number}}, "en-US")
in
    Typed
