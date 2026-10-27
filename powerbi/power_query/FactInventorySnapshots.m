let
    Source = Csv.Document(File.Contents(RootFolder & "/data/raw/FactInventorySnapshots.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    EmptyToNull = Table.ReplaceValue(Headers, "", null, Replacer.ReplaceValue, Table.ColumnNames(Headers)),
    Typed = Table.TransformColumnTypes(EmptyToNull, {{"SnapshotId", Int64.Type}, {"SnapshotDate", type date}, {"LocationId", Int64.Type}, {"ProductId", Int64.Type}, {"UnitsOnHand", Int64.Type}, {"InventoryValue", type number}, {"WeightedAverageCost", type number}}, "en-US")
in
    Typed
