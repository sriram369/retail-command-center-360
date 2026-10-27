let
    Source = Csv.Document(File.Contents(RootFolder & "/data/processed/ReportDailyInventory.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    EmptyToNull = Table.ReplaceValue(Headers, "", null, Replacer.ReplaceValue, Table.ColumnNames(Headers)),
    Typed = Table.TransformColumnTypes(EmptyToNull, {{"BalanceDate", type date}, {"QuantityChange", Int64.Type}, {"ValueChange", type number}, {"UnitsOnHand", Int64.Type}, {"InventoryValue", type number}}, "en-US")
in
    Typed
