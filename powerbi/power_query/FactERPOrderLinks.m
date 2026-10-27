let
    Source = Csv.Document(File.Contents(RootFolder & "/data/raw/FactERPOrderLinks.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    EmptyToNull = Table.ReplaceValue(Headers, "", null, Replacer.ReplaceValue, Table.ColumnNames(Headers)),
    Typed = Table.TransformColumnTypes(EmptyToNull, {{"ERPLinkId", Int64.Type}, {"OrderId", Int64.Type}, {"ERPOrderId", type text}, {"SyncedDate", type date}}, "en-US")
in
    Typed
