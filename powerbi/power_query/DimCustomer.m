let
    Source = Csv.Document(File.Contents(RootFolder & "/data/raw/DimCustomer.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    EmptyToNull = Table.ReplaceValue(Headers, "", null, Replacer.ReplaceValue, Table.ColumnNames(Headers)),
    Typed = Table.TransformColumnTypes(EmptyToNull, {{"CustomerId", Int64.Type}, {"CustomerCode", type text}, {"Segment", type text}, {"State", type text}, {"Synthetic", Int64.Type}}, "en-US")
in
    Typed
