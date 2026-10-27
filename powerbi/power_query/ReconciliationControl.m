let
    Expected = Table.SelectRows(FactSalesOrders, each [ChannelId] = 2 and [OrderStatus] <> "Canceled"),
    MissingERP = Table.NestedJoin(Expected, {"OrderId"}, FactERPOrderLinks, {"OrderId"}, "ERP", JoinKind.LeftAnti),
    EventOrders = Table.Distinct(Table.SelectColumns(FactIntegrationEvents, {"OrderId"})),
    EventFlag = Table.AddColumn(EventOrders, "HasEvent", each 1, Int64.Type),
    WithEvent = Table.NestedJoin(MissingERP, {"OrderId"}, EventFlag, {"OrderId"}, "Event", JoinKind.LeftOuter),
    Expanded = Table.ExpandTableColumn(WithEvent, "Event", {"HasEvent"}),
    Filled = Table.ReplaceValue(Expanded, null, 0, Replacer.ReplaceValue, {"HasEvent"})
in
    Filled
