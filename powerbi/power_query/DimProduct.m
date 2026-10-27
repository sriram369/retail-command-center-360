let
    Source = Csv.Document(File.Contents(RootFolder & "/data/raw/DimProduct.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    EmptyToNull = Table.ReplaceValue(Headers, "", null, Replacer.ReplaceValue, Table.ColumnNames(Headers)),
    Typed = Table.TransformColumnTypes(EmptyToNull, {{"ProductId", Int64.Type}, {"SKU", type text}, {"ProductName", type text}, {"Category", type text}, {"SupplierId", Int64.Type}, {"RetailPrice", type number}, {"OpeningUnitCost", type number}, {"Customizable", Int64.Type}}, "en-US")
in
    Typed
