from scanner import scanner
from token import Token

class ParserError(Exception):
    def __init__(self, token_stream, *expected_tokens):
        template = "Received {}, expected {{{}}}"
        if token_stream.lookahead():
            token_msg = "{} ('{}')".format(*token_stream.lookahead)
        else:
            token_msg = 'out of tokens'
        self.message = template.format(token_msg, ', '.join(expected_tokens))

    def __str__(self):
        return self.message


class Lookahead:
    """Give lookahead for an iterator."""

    def __init__(self, stream):
        self.stream = stream
        self.empty = False
        self.lookahead = next(stream)

    def __iter__(self):
        while not self.empty:
            yield next(self)

    def __next__(self):
        if self.empty:
            raise StopIteration
        value = self.lookahead
        try:
            self.lookahead = next(self.stream)
        except StopIteration:
            self.empty = True
        return value

    def __bool__(self):
        return not self.empty


class TokenStream(Lookahead):
    """Stream of tokens, with features needed by a parser."""

    def lookahead_in(self, *expected):
        return self.lookahead[0] in expected

    def consume(self, *expected):
        """Consume the current token, return the next token's literal
        representation and type. If expected is empty, all tokens are
        accepted."""
        print("Consuming,", self.lookahead)
        if expected and not self.lookahead_in(*expected):
            raise ParserError(self, *expected)
        return next(self)

def parser(tokens):
    return statements(TokenStream(tokens))

def statements(tokens):
    statements_list = []
    while tokens:
        statements_list.append(statement(tokens))

def statement(tokens):
    while not tokens.lookahead_in(Token.NEWLINE):
        tokens.consume()
    tokens.consume(Token.NEWLINE)
    print("Finished line")
    print()

with open('example.bas') as f:
    ast = parser(scanner(f.read(), Token))
#    print(ast.tree())
