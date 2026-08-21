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