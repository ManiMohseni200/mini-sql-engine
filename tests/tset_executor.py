from executor import Executor
from table import Table
from lexer import Lexer
from parser import Parser
import pytest

from errors import (
    UnknownColumnError,
    UnknownTableError
)


def create_test_table():

    columns = [
        "id",
        "name",
        "age",
        "gpa"
    ]

    rows = [
        [1, "Ali", 22, 17.5],
        [2, "Sara", 19, 18.2],
        [3, "John", 24, 15.8],
        [4, "Mary", 21, 19.1],
        [5, "David", 20, 16.4],
    ]

    return Table(columns, rows)


def execute_query(query_text):

    table = create_test_table()

    lexer = Lexer()

    tokens = lexer.tokenize(query_text)

    parser = Parser(tokens)

    query = parser.parse()

    executor = Executor()

    return executor.execute(
        query,
        table
    )


def test_select():

    result = execute_query(
        "SELECT name FROM students"
    )

    assert result.columns == ["name"]

    assert result.rows == [
        ["Ali"],
        ["Sara"],
        ["John"],
        ["Mary"],
        ["David"],
    ]


def test_where():

    result = execute_query(
        "SELECT name "
        "FROM students "
        "WHERE age > 20"
    )

    assert result.rows == [
        ["Ali"],
        ["John"],
        ["Mary"],
    ]


def test_order_by():

    result = execute_query(
        "SELECT name "
        "FROM students "
        "ORDER BY gpa"
    )

    assert result.rows == [
        ["John"],
        ["David"],
        ["Ali"],
        ["Sara"],
        ["Mary"],
    ]


def test_where_and_order_by():

    result = execute_query(
        "SELECT name "
        "FROM students "
        "WHERE age > 20 "
        "ORDER BY gpa"
    )

    assert result.rows == [
        ["John"],
        ["Ali"],
        ["Mary"],
    ]


def test_order_by_desc():

    result = execute_query(
        "SELECT name "
        "FROM students "
        "ORDER BY gpa DESC"
    )

    assert result.rows == [
        ["Mary"],
        ["Sara"],
        ["Ali"],
        ["David"],
        ["John"],
    ]

def test_unknown_column():

    with pytest.raises(UnknownColumnError):

        execute_query(
            "SELECT salary FROM students"
        )

def test_unknown_table():

    with pytest.raises(UnknownTableError):

        execute_query(
            "SELECT name FROM employees"
        )

def test_select_multiple_columns():

    result = execute_query(
        "SELECT name, age FROM students"
    )

    assert result.columns == [
        "name",
        "age"
    ]

    assert result.rows[0] == [
        "Ali",
        22
    ]


def test_select_all():

    result = execute_query(
        "SELECT * FROM students"
    )

    assert result.columns == [
        "id",
        "name",
        "age",
        "gpa"
    ]

    assert result.rows == [
        [1, "Ali", 22, 17.5],
        [2, "Sara", 19, 18.2],
        [3, "John", 24, 15.8],
        [4, "Mary", 21, 19.1],
        [5, "David", 20, 16.4],
    ]


def test_where_and():

    result = execute_query(
        "SELECT name "
        "FROM students "
        "WHERE age > 20 AND gpa > 17"
    )

    assert result.rows == [
        ["Ali"],
        ["Mary"],
    ]


def test_where_or():

    result = execute_query(
        "SELECT name "
        "FROM students "
        "WHERE age > 23 OR gpa > 18"
    )

    assert result.rows == [
        ["Sara"],
        ["John"],
        ["Mary"],
    ]


def test_limit():

    result = execute_query(
        "SELECT name "
        "FROM students "
        "LIMIT 3"
    )

    assert result.rows == [
        ["Ali"],
        ["Sara"],
        ["John"],
    ]


def test_order_by_desc_limit():

    result = execute_query(
        "SELECT name "
        "FROM students "
        "ORDER BY gpa DESC "
        "LIMIT 2"
    )

    assert result.rows == [
        ["Mary"],
        ["Sara"],
    ]


def test_combined_query():

    result = execute_query(
        "SELECT name, age, gpa "
        "FROM students "
        "WHERE age > 20 AND gpa > 16 "
        "ORDER BY gpa DESC "
        "LIMIT 2"
    )

    assert result.rows == [
        ["Mary", 21, 19.1],
        ["Ali", 22, 17.5],
    ]