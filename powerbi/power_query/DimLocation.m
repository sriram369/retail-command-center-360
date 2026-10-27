let
    Source = Csv.Document(File.Contents(RootFolder & "/data/raw/DimLocation.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    EmptyToNull = Table.ReplaceValue(Headers, "", null, Replacer.ReplaceValue, Table.ColumnNames(Headers)),
    Typed = Table.TransformColumnTypes(EmptyToNull, {{"LocationId", Int64.Type}, {"LocationName", type text}, {"LocationType", type text}, {"State", type text}}, "en-US")
in
    Typed
