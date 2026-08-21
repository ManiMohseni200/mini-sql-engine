from lexer import Lexer
from query_ast import SelectQuery, Condition, OrderBy
from errors import ParserError

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def current_token(self):
        if self.position >= len(self.tokens):
            return None
        return self.tokens[self.position]

    def advance(self):
        self.position += 1

    def expect(self, token_type):
        token = self.current_token()

        if token is None:
            raise ParserError(
                f"Expected {token_type}, but reached end of query."
            )
        if token.type != token_type:
            raise ParserError(
                f"Expected {token_type}, "
                f"but got {token.type} ({token.value})"
            )
        self.advance()

        return token

    def parse(self):
        self.expect("SELECT")

        columns = self.parse_columns()

        self.expect("FROM")

        table = self.parse_table()

        where = None

        if self.current_token() is not None:
            if self.current_token().type == "WHERE":
                self.advance()
                where = self.parse_condition()

        order_by = None

        if self.current_token() is not None:
            if self.current_token().type == "ORDER":
                self.advance()
                self.expect("BY")
                order_by = self.parse_order_by()

        if self.current_token() is not None:
            token = self.current_token()
            raise ParserError(
                f"Unexpected token: {token.type} ({token.value})"
            )

        return SelectQuery(
            columns=columns,
            table=table,
            where=where,
            order_by=order_by
        )

    def parse_columns(self):
        columns = []

        token = self.current_token()

        if token is None:
            raise ParserError("Expected column name.")

        if token.type == "ASTERISK":
            columns.append("*")
            self.advance()
            return columns
        
        if token.type != "IDENTIFIER":
            raise ParserError(
                f"Expected column name, but got "
                f"{token.type} ({token.value})"
            )

        columns.append(token.value)
        self.advance()

        while self.current_token() is not None:
            if self.current_token().type != "COMMA":
                break
            self.advance()

            token = self.expect("IDENTIFIER")
            columns.append(token.value)
        
        return columns

    def parse_table(self):
        token = self.expect("IDENTIFIER")
        return token.value

    def parse_condition(self):
        column_token = self.expect("IDENTIFIER")
        operator_token = self.current_token()

        if operator_token is None:
            raise ParserError(
                "Expecetd comparison operator."
            )

        valid_operators = {
            "GREATER_THAN",
            "LESS_THAN",
            "EQUAL",
            "GREATER_EQUAL",
            "LESS_EQUAL",
            "NOT_EQUAL"
        }

        if operator_token.type not in valid_operators:
            raise ParserError(
                f"Expected comparison operator, "
                f"but got {operator_token.type}"
            )

        self.advance()

        value_token = self.current_token()

        if value_token is None:
            raise ParserError(
                "Expected value after comparison operator."
            )

        if value_token.type not in {
            "NUMBER",
            "IDENTIFIER"
        }:
            raise ParserError(
                f"Expected a value, "
                f"but got {value_token.type}"
            )

        self.advance()

        return Condition(
            column=column_token.value,
            operator=operator_token.value,
            value=value_token.value
        )

    def parse_order_by(self):
        column_token = self.expect("IDENTIFIER")
        
        descending = False

        if self.current_token() is not None:

            if self.current_token().type == "DESC":
                descending = True
                self.advance()

            elif current_token().type == "ASC":
                descending = False
                self.advance()

        return OrderBy(
            column=column_token.value,
            descending=descending
        )