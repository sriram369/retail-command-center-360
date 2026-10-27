let
    Source = Csv.Document(File.Contents(RootFolder & "/data/raw/DimSupplier.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    EmptyToNull = Table.ReplaceValue(Headers, "", null, Replacer.ReplaceValue, Table.ColumnNames(Headers)),
    Typed = Table.TransformColumnTypes(EmptyToNull, {{"SupplierId", Int64.Type}, {"SupplierName", type text}, {"StandardLeadDays", Int64.Type}, {"Terms", type text}}, "en-US")
in
    Typed
