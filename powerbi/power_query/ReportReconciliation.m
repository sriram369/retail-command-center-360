let
    Source = Csv.Document(File.Contents(RootFolder & "/data/processed/ReportReconciliation.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    EmptyToNull = Table.ReplaceValue(Headers, "", null, Replacer.ReplaceValue, Table.ColumnNames(Headers)),
    Typed = Table.TransformColumnTypes(EmptyToNull, {{"OrderId", Int64.Type}, {"OrderNumber", type text}, {"OrderDate", type date}, {"CustomerId", Int64.Type}, {"ChannelId", Int64.Type}, {"LocationId", Int64.Type}, {"PromisedDate", type date}, {"OrderStatus", type text}, {"PaymentStatus", type text}, {"IntegrationIssue", type text}, {"AvailableDate", type date}, {"Cohort", Int64.Type}, {"ERPOrderId", type text}, {"SyncedDate", type date}, {"SyncStatus", type text}, {"OrderedAmount", type number}, {"AgeDays", Int64.Type}, {"HasEvent", Int64.Type}, {"ExceptionType", type text}}, "en-US")
in
    Typed
