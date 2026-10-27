let
    Source = Csv.Document(File.Contents(RootFolder & "/data/processed/ReportFulfillment.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    EmptyToNull = Table.ReplaceValue(Headers, "", null, Replacer.ReplaceValue, Table.ColumnNames(Headers)),
    Typed = Table.TransformColumnTypes(EmptyToNull, {{"MonthStart", type date}, {"ChannelId", Int64.Type}, {"LocationId", Int64.Type}, {"EligibleOrders", Int64.Type}, {"FulfilledOrders", Int64.Type}, {"LateOrders", Int64.Type}, {"OpenLateOrders", Int64.Type}, {"FulfillmentDays", Int64.Type}}, "en-US")
in
    Typed
