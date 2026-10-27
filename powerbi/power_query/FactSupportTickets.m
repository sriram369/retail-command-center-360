let
    Source = Csv.Document(File.Contents(RootFolder & "/data/raw/FactSupportTickets.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    EmptyToNull = Table.ReplaceValue(Headers, "", null, Replacer.ReplaceValue, Table.ColumnNames(Headers)),
    Typed = Table.TransformColumnTypes(EmptyToNull, {{"TicketId", Int64.Type}, {"OrderId", Int64.Type}, {"OpenedAt", type datetime}, {"ResolvedAt", type datetime}, {"SLADeadline", type datetime}, {"Category", type text}, {"Severity", type text}, {"Status", type text}, {"Owner", type text}, {"RepeatKey", type text}, {"ResolutionHours", type text}, {"SLAEligible", Int64.Type}, {"SLAMet", Int64.Type}}, "en-US")
in
    Typed
