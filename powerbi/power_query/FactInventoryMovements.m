let
    Source = Csv.Document(File.Contents(RootFolder & "/data/raw/FactInventoryMovements.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    EmptyToNull = Table.ReplaceValue(Headers, "", null, Replacer.ReplaceValue, Table.ColumnNames(Headers)),
    Typed = Table.TransformColumnTypes(EmptyToNull, {{"MovementId", Int64.Type}, {"MovementDate", type date}, {"LocationId", Int64.Type}, {"ProductId", Int64.Type}, {"MovementType", type text}, {"QuantityChange", Int64.Type}, {"ValueChange", type number}, {"ReferenceType", type text}, {"ReferenceId", type text}, {"TransferId", type text}}, "en-US")
in
    Typed
