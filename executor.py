from table import Table
from query_ast import SelectQuery
from conditions import ConditionEvaluator
from errors import (
    UnknownTableError,
    UnknownColumnError,
    UnsupportedQueryError
)

class Executor:
    def __init__(self):
        self.condition_evaluator = ConditionEvaluator()

    def execute(self, query, table):
        if query.table != "students":
            raise UnknownTableError(
                f"Table '{query.table}' does not exist."
            )
        result = self.execute_select(query, table)

        return result

    def execute_select(self, query, table):
        if query.columns == ["*"]:
            selected_columns = table.columns
        else:
            selected_columns = query.columns
        
        for column in query.columns:
            if column not in table.columns:
                raise UnknownColumnError(
                    f"Column '{column}' does not exist."
                )

        filtered_rows = []

        for row in table.rows:
            if query.where is not None:
                matches = self.condition_evaluator.evaluate(
                    query.where,
                    row,
                    table.columns
                )
                if not matches:
                    continue
            filtered_rows.append(row)

        if query.order_by is not None:
            order_column = query.order_by.column

            if order_column not in table.columns:
                raise UnknownColumnError(
                    f"Column '{order_column}' does not exist."
                )
            order_index = table.columns.index(order_column)

            filtered_rows.sort(
                key=lambda row: row[order_index],
                reverse=query.order_by.descending
            )


        column_indexes = [
            table.columns.index(column)
            for column in query.columns
        ]

        result_rows = []

        for row in filtered_rows:
            result_row = [
                row[index]
                for index in column_indexes
            ]

            result_rows.append(result_row)

        return Table(
            columns=query.columns,
            rows=result_rows
        )

# if __name__ == "__main__":
#     from loader import load_csv
#     from lexer import Lexer
#     from parser import Parser
#     from errors import SQLError

#     table = load_csv("data/students.csv")

#     query_text = """
#         SELECT name
#         FROM students
#         WHERE age > 20
#         ORDER BY gpa DESC
#     """

#     try:
#         lexer = Lexer()
#         tokens = lexer.tokenize(query_text)

#         parser = Parser(tokens)
#         query = parser.parse()

#         executor = Executor()
#         result = executor.execute(query, table)

#         result.print()
#     except SQLError as error:
#         print(f"SQL Error: {error}")