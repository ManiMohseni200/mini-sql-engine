from lexer import Lexer

from query_ast import (
    SelectQuery,
    InsertQuery,
    Condition,
    LogicalCondition,
    OrderBy
)

from errors import ParserError


class Parser:

    def __init__(self, tokens):

        self.tokens = tokens

        self.position = 0

    def current_token(self):

        if self.position >= len(self.tokens):

            return None

        return self.tokens[
            self.position
        ]

    def advance(self):

        self.position += 1

    def expect(self, token_type):

        token = self.current_token()

        if token is None:

            raise ParserError(
                f"Expected {token_type}, "
                f"but reached end of query."
            )

        if token.type != token_type:

            raise ParserError(
                f"Expected {token_type}, "
                f"but got "
                f"{token.type} "
                f"({token.value})"
            )

        self.advance()

        return token

    # ==================================================
    # Main Parser
    # ==================================================

    def parse(self):

        token = self.current_token()

        if token is None:

            raise ParserError(
                "Query cannot be empty."
            )

        if token.type == "SELECT":

            return self.parse_select()

        if token.type == "INSERT":

            return self.parse_insert()

        raise ParserError(
            f"Unsupported query type: "
            f"{token.type}"
        )

    # ==================================================
    # SELECT
    # ==================================================

    def parse_select(self):

        self.expect("SELECT")

        columns = self.parse_columns()

        self.expect("FROM")

        table = self.parse_table()

        where = None

        if self.current_token() is not None:

            if (
                self.current_token().type
                == "WHERE"
            ):

                self.advance()

                where = (
                    self.parse_condition_expression()
                )

        order_by = None

        if self.current_token() is not None:

            if (
                self.current_token().type
                == "ORDER"
            ):

                self.advance()

                self.expect("BY")

                order_by = (
                    self.parse_order_by()
                )

        limit = None

        if self.current_token() is not None:

            if (
                self.current_token().type
                == "LIMIT"
            ):

                self.advance()

                limit_token = self.expect(
                    "NUMBER"
                )

                if not isinstance(
                    limit_token.value,
                    int
                ):

                    raise ParserError(
                        "LIMIT must be "
                        "an integer."
                    )

                if limit_token.value < 0:

                    raise ParserError(
                        "LIMIT cannot be "
                        "negative."
                    )

                limit = (
                    limit_token.value
                )

        if self.current_token() is not None:

            token = self.current_token()

            raise ParserError(
                f"Unexpected token: "
                f"{token.type} "
                f"({token.value})"
            )

        return SelectQuery(
            columns=columns,
            table=table,
            where=where,
            order_by=order_by,
            limit=limit
        )

    def parse_columns(self):

        columns = []

        token = self.current_token()

        if token is None:

            raise ParserError(
                "Expected column name."
            )

        if token.type == "ASTERISK":

            columns.append("*")

            self.advance()

            return columns

        if token.type != "IDENTIFIER":

            raise ParserError(
                f"Expected column name, "
                f"but got "
                f"{token.type} "
                f"({token.value})"
            )

        columns.append(
            token.value
        )

        self.advance()

        while (
            self.current_token()
            is not None
        ):

            if (
                self.current_token().type
                != "COMMA"
            ):

                break

            self.advance()

            token = self.expect(
                "IDENTIFIER"
            )

            columns.append(
                token.value
            )

        return columns

    def parse_table(self):

        token = self.expect(
            "IDENTIFIER"
        )

        return token.value

    # ==================================================
    # WHERE
    # ==================================================

    def parse_condition_expression(self):

        condition = (
            self.parse_condition()
        )

        while (
            self.current_token()
            is not None
        ):

            token_type = (
                self.current_token().type
            )

            if token_type not in {
                "AND",
                "OR"
            }:

                break

            operator = (
                self.current_token().value
            )

            self.advance()

            right_condition = (
                self.parse_condition()
            )

            condition = LogicalCondition(
                left=condition,
                operator=operator.upper(),
                right=right_condition
            )

        return condition

    def parse_condition(self):

        column_token = self.expect(
            "IDENTIFIER"
        )

        operator_token = (
            self.current_token()
        )

        if operator_token is None:

            raise ParserError(
                "Expected comparison "
                "operator."
            )

        valid_operators = {
            "GREATER_THAN",
            "LESS_THAN",
            "EQUAL",
            "GREATER_EQUAL",
            "LESS_EQUAL",
            "NOT_EQUAL"
        }

        if (
            operator_token.type
            not in valid_operators
        ):

            raise ParserError(
                f"Expected comparison "
                f"operator, "
                f"but got "
                f"{operator_token.type}"
            )

        self.advance()

        value_token = (
            self.current_token()
        )

        if value_token is None:

            raise ParserError(
                "Expected value after "
                "comparison operator."
            )

        if value_token.type not in {
            "NUMBER",
            "IDENTIFIER"
        }:

            raise ParserError(
                f"Expected a value, "
                f"but got "
                f"{value_token.type}"
            )

        self.advance()

        return Condition(
            column=column_token.value,
            operator=operator_token.value,
            value=value_token.value
        )

    # ==================================================
    # ORDER BY
    # ==================================================

    def parse_order_by(self):

        column_token = self.expect(
            "IDENTIFIER"
        )

        descending = False

        if self.current_token() is not None:

            if (
                self.current_token().type
                == "DESC"
            ):

                descending = True

                self.advance()

            elif (
                self.current_token().type
                == "ASC"
            ):

                descending = False

                self.advance()

        return OrderBy(
            column=column_token.value,
            descending=descending
        )

    # ==================================================
    # INSERT
    # ==================================================

    def parse_insert(self):

        self.expect("INSERT")

        self.expect("INTO")

        table_token = self.expect(
            "IDENTIFIER"
        )

        self.expect("VALUES")

        self.expect("LPAREN")

        values = []

        while True:

            token = self.current_token()

            if token is None:

                raise ParserError(
                    "Expected value, "
                    "but reached "
                    "end of query."
                )

            if token.type not in {
                "NUMBER",
                "IDENTIFIER"
            }:

                raise ParserError(
                    f"Expected value, "
                    f"but got "
                    f"{token.type} "
                    f"({token.value})"
                )

            values.append(
                token.value
            )

            self.advance()

            if self.current_token() is None:

                raise ParserError(
                    "Expected ')' "
                    "after values."
                )

            if (
                self.current_token().type
                == "RPAREN"
            ):

                break

            self.expect("COMMA")

        self.expect("RPAREN")

        if self.current_token() is not None:

            token = self.current_token()

            raise ParserError(
                f"Unexpected token: "
                f"{token.type} "
                f"({token.value})"
            )

        return InsertQuery(
            table=table_token.value,
            values=values
        )