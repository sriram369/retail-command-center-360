let
    Source = Csv.Document(File.Contents(RootFolder & "/data/processed/ReportTickets.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    EmptyToNull = Table.ReplaceValue(Headers, "", null, Replacer.ReplaceValue, Table.ColumnNames(Headers)),
    Typed = Table.TransformColumnTypes(EmptyToNull, {{"TicketId", Int64.Type}, {"OrderId", Int64.Type}, {"OpenedAt", type datetime}, {"ResolvedAt", type datetime}, {"SLADeadline", type datetime}, {"Category", type text}, {"Severity", type text}, {"Status", type text}, {"Owner", type text}, {"RepeatKey", type text}, {"ResolutionHours", type text}, {"SLAEligible", Int64.Type}, {"SLAMet", Int64.Type}, {"MonthStart", type date}, {"ResolvedCount", Int64.Type}, {"OpenCount", Int64.Type}, {"RepeatIncident", Int64.Type}, {"OpenDate", type date}}, "en-US")
in
    Typed
