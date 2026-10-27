let
    Source = Csv.Document(File.Contents(RootFolder & "/data/raw/InjectedAnomalies.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    EmptyToNull = Table.ReplaceValue(Headers, "", null, Replacer.ReplaceValue, Table.ColumnNames(Headers)),
    Typed = Table.TransformColumnTypes(EmptyToNull, {{"AnomalyId", Int64.Type}, {"Scenario", type text}, {"Entity", type text}, {"EntityId", Int64.Type}, {"Issue", type text}, {"StartDate", type date}, {"Cohort", Int64.Type}}, "en-US")
in
    Typed
