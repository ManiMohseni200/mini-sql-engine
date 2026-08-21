class SQLError(Exception):
    """Base class for all SQL engine errors."""
    pass


class LexerError(SQLError):
    """Raised when the lexer encounters invalid syntax."""
    pass


class ParserError(SQLError):
    """Raised when the SQL query has invalid syntax."""
    pass


class UnknownTableError(SQLError):
    """Raised when a requested table does not exist."""
    pass


class UnknownColumnError(SQLError):
    """Raised when a requested column does not exist."""
    pass


class UnsupportedQueryError(SQLError):
    """Raised when the engine does not support a query feature."""
    pass


class InvalidConditionError(SQLError):
    """Raised when a WHERE condition is invalid."""
    pass