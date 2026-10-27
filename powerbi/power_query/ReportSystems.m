let
    Source = Csv.Document(File.Contents(RootFolder & "/data/processed/ReportSystems.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    EmptyToNull = Table.ReplaceValue(Headers, "", null, Replacer.ReplaceValue, Table.ColumnNames(Headers)),
    Typed = Table.TransformColumnTypes(EmptyToNull, {{"MonthStart", type date}, {"SuccessfulEvents", Int64.Type}, {"FailedEvents", Int64.Type}, {"DuplicateEvents", Int64.Type}, {"AttemptedEvents", Int64.Type}, {"TicketsOpened", Int64.Type}, {"ResolvedTickets", Int64.Type}, {"OpenTickets", Int64.Type}, {"SLAEligible", Int64.Type}, {"SLAMet", Int64.Type}, {"ResolutionHours", type number}, {"RepeatIncidents", Int64.Type}}, "en-US")
in
    Typed
