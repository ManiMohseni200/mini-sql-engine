from table import Table

from conditions import ConditionEvaluator

from errors import (
    UnknownTableError,
    UnknownColumnError
)


class Executor:

    def __init__(self):

        self.condition_evaluator = (
            ConditionEvaluator()
        )

    # ==================================================
    # Main Executor
    # ==================================================

    def execute(self, query, table):

        if query.table != "students":

            raise UnknownTableError(
                f"Table '{query.table}' "
                f"does not exist."
            )

        query_type = (
            query.__class__.__name__
        )

        if query_type == "SelectQuery":

            return self.execute_select(
                query,
                table
            )

        if query_type == "InsertQuery":

            return self.execute_insert(
                query,
                table
            )

        raise ValueError(
            f"Unsupported query type: "
            f"{query_type}"
        )

    # ==================================================
    # SELECT
    # ==================================================

    def execute_select(
        self,
        query,
        table
    ):

        # -------------------------
        # SELECT
        # -------------------------

        if query.columns == ["*"]:

            selected_columns = (
                table.columns
            )

        else:

            selected_columns = (
                query.columns
            )

        # -------------------------
        # Validate columns
        # -------------------------

        for column in selected_columns:

            if column not in table.columns:

                raise UnknownColumnError(
                    f"Column '{column}' "
                    f"does not exist."
                )

        # -------------------------
        # WHERE
        # -------------------------

        filtered_rows = []

        for row in table.rows:

            if query.where is not None:

                matches = (
                    self.condition_evaluator.evaluate(
                        query.where,
                        row,
                        table.columns
                    )
                )

                if not matches:

                    continue

            filtered_rows.append(row)

        # -------------------------
        # ORDER BY
        # -------------------------

        if query.order_by is not None:

            order_column = (
                query.order_by.column
            )

            if (
                order_column
                not in table.columns
            ):

                raise UnknownColumnError(
                    f"Column '{order_column}' "
                    f"does not exist."
                )

            order_index = (
                table.columns.index(
                    order_column
                )
            )

            filtered_rows.sort(
                key=lambda row: (
                    row[order_index]
                ),
                reverse=(
                    query.order_by.descending
                )
            )

        # -------------------------
        # LIMIT
        # -------------------------

        if query.limit is not None:

            filtered_rows = (
                filtered_rows[
                    :query.limit
                ]
            )

        # -------------------------
        # SELECT COLUMNS
        # -------------------------

        column_indexes = [
            table.columns.index(column)
            for column in selected_columns
        ]

        result_rows = []

        for row in filtered_rows:

            result_row = [
                row[index]
                for index in column_indexes
            ]

            result_rows.append(
                result_row
            )

        return Table(
            columns=selected_columns,
            rows=result_rows
        )

    # ==================================================
    # INSERT
    # ==================================================

    def execute_insert(
        self,
        query,
        table
    ):

        if (
            len(query.values)
            != len(table.columns)
        ):

            raise ValueError(
                f"Expected "
                f"{len(table.columns)} "
                f"values, but got "
                f"{len(query.values)}."
            )

        table.insert_row(
            query.values
        )

        return table