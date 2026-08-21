import csv

from table import Table

def convert_value(value):
    value = value.strip()
    try:
        return int(value)
    except ValueError:
        pass
    
    try:
        return float(value)
    except ValueError:
        pass

    return value

def load_csv(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.reader(file)

        columns = next(reader)
        rows = []

        for row in reader:
            converted_row = [convert_value(value) for value in row]
            rows.append(converted_row)

    return Table(columns, rows)