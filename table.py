class Table:
    def __init__(self, columns, rows):
        self.columns = columns
        self.rows = rows

    def row_count(self):
        return len(self.rows)

    def get_column(self, column_name):
        if column_name not in self.columns:
            raise ValueError(f"Column '{column_name}' does not exist.")

        column_index = self.columns.index(column_name)

        return [row[column_index] for row in self.rows]

    def get_row(self, index):
        if index < 0 or index >= len(self.rows):
            raise IndexError("Row index out of Range.")
        return self.rows[index]

    def print(self):
        print(" | ".join(self.columns))
        print("-" * (len(" | ".join(self.columns)) + 2))

        for row in self.rows:
            print(" | ".join(str(value) for value in row))