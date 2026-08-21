from errors import LexerError

class Token:
    def __init__(self, token_type, value):
        self.type = token_type
        self.value = value

    def __repr__(self):
        return f"Token(type={self.type}, value={self.value})"

class Lexer:
    KEYWORDS = {
        "SELECT": "SELECT",
        "FROM": "FROM",
        "WHERE": "WHERE",
        "ORDER": "ORDER",
        "BY": "BY",
        "ASC": "ASC",
        "DESC": "DESC",
        "AND": "AND",
        "OR": "OR",
        "LIMIT": "LIMIT",
    }

    OPERATORS = {
        ">": "GREATER_THAN",
        "<": "LESS_THAN",
        "=": "EQUAL",
        ">=": "GREATER_EQUAL",
        "<=": "LESS_EQUAL",
        "!=": "NOT_EQUAL",
    }

    def tokenize(self, query):
        tokens = []
        i = 0

        while i < len(query):
            char = query[i]
            if char.isspace():
                i += 1
                continue

            if char.isalpha() or char == "_":
                start = i

                while i < len(query) and (
                    query[i].isalnum() or query[i] == "_"
                ):
                    i += 1
                word = query[start:i]
                upper_word = word.upper()

                if upper_word in self.KEYWORDS:
                    token_type = self.KEYWORDS[upper_word]
                else:
                    token_type = "IDENTIFIER"
                
                tokens.append(Token(token_type, word))
                continue

            if char.isdigit():
                start = i
                has_decimal = False
                while i < len(query):
                    current = query[i]
                    if current.isdigit():
                        i += 1
                    elif current == "." and not has_decimal:
                        has_decimal = True
                        i += 1

                    else:
                        break
                
                number_text = query[start:i]

                if has_decimal:
                    value = float(number_text)
                else:
                    value = int(number_text)
                
                tokens.append(Token("NUMBER", value))
                continue

            if char in "><=!":
                operator = char

                if i + 1 < len(query):
                    two_char_operator = query[i: i + 2]
                    if two_char_operator in self.OPERATORS:
                        operator = two_char_operator
                        i += 2
                    else:
                        if char == "!":
                            raise LexerError(
                                f"Invalid Operator '{char}' at position {i}"
                            )
                    i += 1
                else:
                    if char == "!":
                        raise LexerError(
                            f"Invalid Operator '{char}' at position {i}"
                        )
                    i += 1
                token_type = self.OPERATORS[operator]
                tokens.append(Token(token_type, operator))
                continue
            if char == ",":
                tokens.append(Token("COMMA", ","))
                i += 1
                continue

            if char == "*":
                tokens.append(Token("ASTERISK", "*"))
                i += 1
                continue

            raise LexerError(
                f"Unexpected character '{char}' at position {i}"
            )

        return tokens