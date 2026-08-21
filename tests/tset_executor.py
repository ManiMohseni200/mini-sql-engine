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