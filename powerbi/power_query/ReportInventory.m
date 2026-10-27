let
    Source = Csv.Document(File.Contents(RootFolder & "/data/processed/ReportInventory.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    EmptyToNull = Table.ReplaceValue(Headers, "", null, Replacer.ReplaceValue, Table.ColumnNames(Headers)),
    Typed = Table.TransformColumnTypes(EmptyToNull, {{"SnapshotId", Int64.Type}, {"SnapshotDate", type date}, {"LocationId", Int64.Type}, {"ProductId", Int64.Type}, {"UnitsOnHand", Int64.Type}, {"InventoryValue", type number}, {"WeightedAverageCost", type number}, {"DailyDemand", type number}, {"BackorderUnits", type number}, {"AvailableUnits", type number}, {"SKU", type text}, {"ProductName", type text}, {"Category", type text}, {"SupplierId", Int64.Type}, {"RetailPrice", type number}, {"OpeningUnitCost", type number}, {"Customizable", Int64.Type}, {"LocationName", type text}, {"LocationType", type text}, {"State", type text}, {"StandardLeadDays", Int64.Type}, {"ProtectionDays", Int64.Type}, {"ReorderPoint", Int64.Type}, {"StockoutRisk", Int64.Type}, {"LowStock", Int64.Type}, {"DaysCover", type text}, {"ExcessUnits", Int64.Type}, {"RecommendedUnits", Int64.Type}, {"WarehouseAvailable", type number}, {"Action", type text}}, "en-US")
in
    Typed
