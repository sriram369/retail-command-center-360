let
    Source = Csv.Document(File.Contents(RootFolder & "/data/raw/FactSalesOrders.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    EmptyToNull = Table.ReplaceValue(Headers, "", null, Replacer.ReplaceValue, Table.ColumnNames(Headers)),
    Typed = Table.TransformColumnTypes(EmptyToNull, {{"OrderId", Int64.Type}, {"OrderNumber", type text}, {"OrderDate", type date}, {"CustomerId", Int64.Type}, {"ChannelId", Int64.Type}, {"LocationId", Int64.Type}, {"PromisedDate", type date}, {"OrderStatus", type text}, {"PaymentStatus", type text}, {"IntegrationIssue", type text}, {"AvailableDate", type date}, {"Cohort", Int64.Type}}, "en-US")
in
    Typed
