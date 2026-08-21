class Condition:
    def __init__(self, column, operator, value):
        self.column = column
        self.operator = operator
        self.value = value

    def __repr__(self):
        return (
            f"Condition("
            f"column={self.column}, "
            f"operator={self.operator}, "
            f"value={self.value}"
            f")"
        )

class OrderBy:
    def __init__(self, column, descending=False):
        self.column = column
        self.descending = descending

    def __repre__(self):
        direction = "DESC" if self.descneding else "ASC"

        return (
            f"OrderBY("
            f"column={self.column}, "
            f"direction={direction}"
            f")"
        )

class SelectQuery:
    def __init__(
        self,
        columns,
        table,
        where=None,
        order_by=None
        ):
        self.columns = columns
        self.table = table
        self.where = where
        self.order_by = order_by

    def __repr__(self):
        return (
            f"SelectQuery(\n"
            f"    columns={self.columns},\n"
            f"    table={self.table},\n"
            f"    where={self.where},\n"
            f"    order_by={self.order_by}\n"
            f")"
        )