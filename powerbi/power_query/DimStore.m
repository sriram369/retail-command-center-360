let
    Source = Csv.Document(File.Contents(RootFolder & "/data/raw/DimStore.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    EmptyToNull = Table.ReplaceValue(Headers, "", null, Replacer.ReplaceValue, Table.ColumnNames(Headers)),
    Typed = Table.TransformColumnTypes(EmptyToNull, {{"StoreId", Int64.Type}, {"StoreName", type text}, {"City", type text}, {"State", type text}}, "en-US")
in
    Typed
