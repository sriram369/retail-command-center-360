let
    Source = Csv.Document(File.Contents(RootFolder & "/data/raw/FactIntegrationEvents.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    EmptyToNull = Table.ReplaceValue(Headers, "", null, Replacer.ReplaceValue, Table.ColumnNames(Headers)),
    Typed = Table.TransformColumnTypes(EmptyToNull, {{"EventId", Int64.Type}, {"OrderId", Int64.Type}, {"EventDate", type date}, {"SourceSystem", type text}, {"EventType", type text}, {"Status", type text}, {"BusinessKey", type text}, {"PayloadSKU", type text}, {"Deduplicated", Int64.Type}}, "en-US")
in
    Typed
