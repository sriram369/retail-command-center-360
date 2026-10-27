let
    Source = Csv.Document(File.Contents(RootFolder & "/data/processed/ReportFinance.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    EmptyToNull = Table.ReplaceValue(Headers, "", null, Replacer.ReplaceValue, Table.ColumnNames(Headers)),
    Typed = Table.TransformColumnTypes(EmptyToNull, {{"MonthStart", type date}, {"ChannelId", Int64.Type}, {"LocationId", Int64.Type}, {"NetSales", type number}, {"COGS", type number}, {"SalesBeforeReturns", type number}, {"RefundAmount", type number}, {"UnitsSold", Int64.Type}, {"UnitsReturned", Int64.Type}, {"DiscountAmount", type number}, {"FulfilledOrders", Int64.Type}, {"SalesBudget", type number}, {"GrossProfit", type number}, {"Channel", type text}, {"LocationName", type text}}, "en-US")
in
    Typed
