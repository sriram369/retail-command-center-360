let
    Source = Csv.Document(File.Contents(RootFolder & "/data/raw/FactSalesTransactions.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    EmptyToNull = Table.ReplaceValue(Headers, "", null, Replacer.ReplaceValue, Table.ColumnNames(Headers)),
    Typed = Table.TransformColumnTypes(EmptyToNull, {{"SalesTransactionId", Int64.Type}, {"PostingDate", type date}, {"OrderId", Int64.Type}, {"OrderLineId", Int64.Type}, {"ProductId", Int64.Type}, {"LocationId", Int64.Type}, {"ChannelId", Int64.Type}, {"CustomerId", Int64.Type}, {"TransactionType", type text}, {"Quantity", Int64.Type}, {"NetAmount", type number}, {"COGS", type number}, {"DiscountAmount", type number}}, "en-US")
in
    Typed
