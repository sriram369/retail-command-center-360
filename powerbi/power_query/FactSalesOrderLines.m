let
    Source = Csv.Document(File.Contents(RootFolder & "/data/raw/FactSalesOrderLines.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    EmptyToNull = Table.ReplaceValue(Headers, "", null, Replacer.ReplaceValue, Table.ColumnNames(Headers)),
    Typed = Table.TransformColumnTypes(EmptyToNull, {{"OrderLineId", Int64.Type}, {"OrderId", Int64.Type}, {"ProductId", Int64.Type}, {"Quantity", Int64.Type}, {"UnitPrice", type number}, {"DiscountAmount", type number}, {"OrderedAmount", type number}}, "en-US")
in
    Typed
