let
    Source = Csv.Document(File.Contents(RootFolder & "/data/raw/FactReturns.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    EmptyToNull = Table.ReplaceValue(Headers, "", null, Replacer.ReplaceValue, Table.ColumnNames(Headers)),
    Typed = Table.TransformColumnTypes(EmptyToNull, {{"ReturnId", type text}, {"OrderId", Int64.Type}, {"OrderLineId", Int64.Type}, {"ReturnDate", type date}, {"ProductId", Int64.Type}, {"LocationId", Int64.Type}, {"ChannelId", Int64.Type}, {"CustomerId", Int64.Type}, {"Quantity", Int64.Type}, {"RefundAmount", type number}, {"CostReversal", type number}, {"Reason", type text}, {"Disposition", type text}}, "en-US")
in
    Typed
