let
    Source = Csv.Document(File.Contents(RootFolder & "/data/raw/FactPurchaseOrders.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    EmptyToNull = Table.ReplaceValue(Headers, "", null, Replacer.ReplaceValue, Table.ColumnNames(Headers)),
    Typed = Table.TransformColumnTypes(EmptyToNull, {{"PurchaseOrderId", Int64.Type}, {"PONumber", type text}, {"ProductId", Int64.Type}, {"SupplierId", Int64.Type}, {"LocationId", Int64.Type}, {"PODate", type date}, {"ApprovalDate", type date}, {"PromisedReceiptDate", type date}, {"ReceivedDate", type date}, {"Quantity", Int64.Type}, {"UnitCost", type number}, {"POAmount", type number}, {"ApprovalDays", Int64.Type}, {"POStatus", type text}, {"ScenarioAffected", Int64.Type}}, "en-US")
in
    Typed
