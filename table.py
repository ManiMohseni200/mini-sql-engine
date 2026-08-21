class Table:

    def __init__(self, columns, rows):

        self.columns = columns

        self.rows = rows

    def row_count(self):

        return len(self.rows)

    def get_column(self, column_name):

        if column_name not in self.columns:

            raise ValueError(
                f"Column '{column_name}' "
                f"does not exist."
            )

        column_index = (
            self.columns.index(
                column_name
            )
        )

        return [
            row[column_index]
            for row in self.rows
        ]

    def get_row(self, index):

        if (
            index < 0
            or index >= len(self.rows)
        ):

            raise IndexError(
                "Row index out of Range."
            )

        return self.rows[index]

    def insert_row(self, row):

        if len(row) != len(self.columns):

            raise ValueError(
                "Row has a different "
                "number of values than "
                "the table columns."
            )

        self.rows.append(row)

    def print(self):

        header = " | ".join(
            self.columns
        )

        print(header)

        print(
            "-" * (len(header) + 2)
        )

        for row in self.rows:

            print(
                " | ".join(
                    str(value)
                    for value in row
                )
            )