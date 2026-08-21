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


class LogicalCondition:

    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return (
            f"LogicalCondition("
            f"left={self.left}, "
            f"operator={self.operator}, "
            f"right={self.right}"
            f")"
        )


class OrderBy:

    def __init__(self, column, descending=False):
        self.column = column
        self.descending = descending

    def __repr__(self):
        direction = "DESC" if self.descending else "ASC"

        return (
            f"OrderBy("
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
        order_by=None,
        limit=None
    ):
        self.columns = columns
        self.table = table
        self.where = where
        self.order_by = order_by
        self.limit = limit

    def __repr__(self):
        return (
            f"SelectQuery(\n"
            f"    columns={self.columns},\n"
            f"    table={self.table},\n"
            f"    where={self.where},\n"
            f"    order_by={self.order_by},\n"
            f"    limit={self.limit}\n"
            f")"
        )


class InsertQuery:

    def __init__(self, table, values):
        self.table = table
        self.values = values

    def __repr__(self):
        return (
            f"InsertQuery("
            f"table={self.table}, "
            f"values={self.values}"
            f")"
        )