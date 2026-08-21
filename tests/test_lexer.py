from lexer import Lexer


def test_select_token():

    lexer = Lexer()

    tokens = lexer.tokenize(
        "SELECT name FROM students"
    )

    assert tokens[0].type == "SELECT"
    assert tokens[1].type == "IDENTIFIER"
    assert tokens[1].value == "name"
    assert tokens[2].type == "FROM"
    assert tokens[3].type == "IDENTIFIER"


def test_number_token():

    lexer = Lexer()

    tokens = lexer.tokenize(
        "SELECT name FROM students WHERE age > 20"
    )

    number_token = tokens[-1]

    assert number_token.type == "NUMBER"
    assert number_token.value == 20


def test_decimal_number_token():

    lexer = Lexer()

    tokens = lexer.tokenize(
        "SELECT name FROM students WHERE gpa > 17.5"
    )

    number_token = tokens[-1]

    assert number_token.type == "NUMBER"
    assert number_token.value == 17.5


def test_comparison_operator():

    lexer = Lexer()

    tokens = lexer.tokenize(
        "SELECT name FROM students WHERE age >= 20"
    )

    operator_token = tokens[-2]

    assert operator_token.type == "GREATER_EQUAL"
    assert operator_token.value == ">="