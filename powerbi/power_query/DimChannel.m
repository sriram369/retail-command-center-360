let
    Source = Csv.Document(File.Contents(RootFolder & "/data/raw/DimChannel.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    EmptyToNull = Table.ReplaceValue(Headers, "", null, Replacer.ReplaceValue, Table.ColumnNames(Headers)),
    Typed = Table.TransformColumnTypes(EmptyToNull, {{"ChannelId", Int64.Type}, {"Channel", type text}}, "en-US")
in
    Typed
