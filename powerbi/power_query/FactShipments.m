let
    Source = Csv.Document(File.Contents(RootFolder & "/data/raw/FactShipments.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    EmptyToNull = Table.ReplaceValue(Headers, "", null, Replacer.ReplaceValue, Table.ColumnNames(Headers)),
    Typed = Table.TransformColumnTypes(EmptyToNull, {{"ShipmentId", Int64.Type}, {"OrderId", Int64.Type}, {"ShipDate", type date}, {"LocationId", Int64.Type}, {"OrderDate", type date}, {"ChannelId", Int64.Type}, {"PromisedDate", type date}, {"FulfillmentDays", Int64.Type}, {"IsLate", Int64.Type}}, "en-US")
in
    Typed
