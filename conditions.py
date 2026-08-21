from errors import (
    UnknownColumnError,
    InvalidConditionError
)

from query_ast import LogicalCondition


class ConditionEvaluator:

    def evaluate(self, condition, row, columns):

        if isinstance(condition, LogicalCondition):

            left_result = self.evaluate(
                condition.left,
                row,
                columns
            )

            right_result = self.evaluate(
                condition.right,
                row,
                columns
            )

            if condition.operator == "AND":
                return left_result and right_result

            if condition.operator == "OR":
                return left_result or right_result

            raise InvalidConditionError(
                f"Unexpected logical operator: "
                f"{condition.operator}"
            )

        column_name = condition.column
        operator = condition.operator
        value = condition.value

        if column_name not in columns:

            raise UnknownColumnError(
                f"Column '{column_name}' does not exist."
            )

        column_index = columns.index(column_name)

        row_value = row[column_index]

        value = self.convert_value(
            value,
            row_value
        )

        if operator == ">":
            return row_value > value

        elif operator == "<":
            return row_value < value

        elif operator == "=":
            return row_value == value

        elif operator == "<=":
            return row_value <= value

        elif operator == ">=":
            return row_value >= value

        elif operator == "!=":
            return row_value != value

        else:
            raise InvalidConditionError(
                f"Unexpected operator: {operator}"
            )

    def convert_value(self, value, reference_value):

        if isinstance(reference_value, int):
            return int(value)

        if isinstance(reference_value, float):
            return float(value)

        return value