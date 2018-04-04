from scanner import scanner
from token import Token

class ParserError(Exception):
    def __init__(self, token_stream, *expected_tokens):
        template = "Received {}, expected {{{}}}"
        if token_stream.lookahead():
            token_msg = "{} ('{}')".format(*token_stream.current)
        else:
            token_msg = 'out of tokens'
        self.message = template.format(token_msg, ', '.join(expected_tokens))

    def __str__(self):
        return self.message


class Lookahead:
    """Give lookahead via __getitem__ for an iterator."""

    def __init__(self, stream):
        self.stream = stream
        self.lookahead = []

    def _buffer_to(self, n):
        while len(self.lookahead) <= n:
            self.lookahead.append(next(self.stream))

    def __getitem__(self, n):
        self._buffer_to(n)
        return self.lookahead[n]

    def __iter__(self):
        while self.lookahead:
            yield self.lookahead.pop(0)
        yield from self.stream

    def __next__(self):
        if self.lookahead:
            return self.lookahead.pop(0)
        return next(self.stream)

    def __bool__(self):
        try:
            self._buffer_to(0)
            return True
        except StopIteration:
            return False


class TokenStream(Lookahead):
    """Stream of tokens, with features needed by a parser."""

    def consume(self, *expected):
        """Consume the current token, return the next token's literal
        representation and type. If expected is empty, all tokens are
        accepted."""
        print("Consuming,", self[0])
        if expected and self[0] not in expected:
            raise ParserError(self, *expected)
        return next(self)

    def try_consume(self, *expected):
        try:
            if self[0] in expected:
                return self.consume(*expected)
        except StopIteration:
            return None

def parser(tokens):
    return statements(TokenStream(tokens))

def statements(tokens):
    statements_list = []
    while tokens:
        statements_list.append(statement(tokens))

def statement(tokens):
    while tokens.consume()[0] != Token.NEWLINE:
        continue
    print("Finished line")
    print()

with open('example.bas') as f:
    ast = parser(scanner(f.read(), Token))
    print(ast.tree())


def ten():
    for i in range(10):
        yield i

lt = Lookahead(ten())
