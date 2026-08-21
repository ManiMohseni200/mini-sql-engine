from lexer import Lexer
from parser import Parser


def parse_query(query_text):

    lexer = Lexer()

    tokens = lexer.tokenize(query_text)

    parser = Parser(tokens)

    return parser.parse()


def test_parse_select():

    query = parse_query(
        "SELECT name FROM students"
    )

    assert query.columns == ["name"]
    assert query.table == "students"
    assert query.where is None
    assert query.order_by is None


def test_parse_where():

    query = parse_query(
        "SELECT name FROM students WHERE age > 20"
    )

    assert query.columns == ["name"]
    assert query.table == "students"

    assert query.where.column == "age"
    assert query.where.operator == ">"
    assert query.where.value == 20


def test_parse_order_by():

    query = parse_query(
        "SELECT name FROM students ORDER BY gpa"
    )

    assert query.order_by is not None
    assert query.order_by.column == "gpa"
    assert query.order_by.descending is False


def test_parse_order_by_desc():

    query = parse_query(
        "SELECT name FROM students ORDER BY gpa DESC"
    )

    assert query.order_by is not None
    assert query.order_by.column == "gpa"
    assert query.order_by.descending is True


def test_parse_full_query():

    query = parse_query(
        "SELECT name FROM students "
        "WHERE age > 20 "
        "ORDER BY gpa"
    )

    assert query.columns == ["name"]
    assert query.table == "students"

    assert query.where.column == "age"
    assert query.where.operator == ">"
    assert query.where.value == 20

    assert query.order_by.column == "gpa"

def test_parse_multiple_columns():

    query = parse_query(
        "SELECT name, age, gpa FROM students"
    )

    assert query.columns == [
        "name",
        "age",
        "gpa"
    ]


def test_parse_and():

    query = parse_query(
        "SELECT name "
        "FROM students "
        "WHERE age > 20 AND gpa > 17"
    )

    assert query.where.operator == "AND"

    assert query.where.left.column == "age"
    assert query.where.left.value == 20

    assert query.where.right.column == "gpa"
    assert query.where.right.value == 17


def test_parse_or():

    query = parse_query(
        "SELECT name "
        "FROM students "
        "WHERE age > 20 OR gpa > 18"
    )

    assert query.where.operator == "OR"


def test_parse_limit():

    query = parse_query(
        "SELECT name "
        "FROM students "
        "LIMIT 3"
    )

    assert query.limit == 3


def test_parse_desc():

    query = parse_query(
        "SELECT name "
        "FROM students "
        "ORDER BY gpa DESC"
    )

    assert query.order_by.column == "gpa"
    assert query.order_by.descending is True