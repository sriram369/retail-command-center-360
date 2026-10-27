let
    Source = Csv.Document(File.Contents(RootFolder & "/data/raw/DimDate.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    EmptyToNull = Table.ReplaceValue(Headers, "", null, Replacer.ReplaceValue, Table.ColumnNames(Headers)),
    Typed = Table.TransformColumnTypes(EmptyToNull, {{"Date", type date}, {"Year", Int64.Type}, {"MonthNumber", Int64.Type}, {"Month", type text}, {"MonthStart", type date}, {"Quarter", type text}, {"DayOfWeek", type text}}, "en-US")
in
    Typed
