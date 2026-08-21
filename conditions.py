from errors import (
    UnknownColumnError,
    InvalidConditionError
)

class ConditionEvaluator:

    def evaluate(self, condition, row, columns):
        column_name = condition.column
        operator = condition.operator
        value = condition.value

        if column_name not in columns:
            raise UnknownColumnError(
                f"Column '{column_name}' does not exist."
            )

        column_index = columns.index(column_name)
        row_value = row[column_index]

        value = self.convert_value(value, row_value)

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