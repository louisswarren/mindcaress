from scanner import scanner
from token import Token

class ParserError(Exception):
    def __init__(self, token, *expected_tokens):
        template = "Received {}, expected {{{}}}"
        self.message = template.format(token, ', '.join(expected_tokens))

    def __str__(self):
        return self.message


def consume(tokcar, tokcdr, *expected_tokens):
    """Consume a given token, checking that it is valid. Returns the next
    token, and the literal representation of the given token. Note that tokcdr
    gets modified.
    Example usage:
        tokcar, _ = consume(tokcar, tokcdr, Token.ADD, Token.MUL)"""
    if tokcar[0] not in expected_tokens:
        raise ParserError(tokcar, *expected_tokens)
    print("Consuming", tokcar)
    return next(tokcdr), tokcar[1]


def parser(tokens):
    statements = []
    for token in tokens:
        statements.append(statement(token, tokens))


def statement(tokcar, tokcdr):
    if tokcar[0] == Token.LET:
        return let(tokcar, tokcdr)
    else:
        raise ParserError(tokcar[0], Token.LET)

def let(tokcar, tokcdr):
    tokcar, _ = consume(tokcar, tokcdr, Token.LET)
    tokcar, var = consume(tokcar, tokcdr, Token.ID)
    if tokcar == Token.LSBRA:
        tokcar, _ = consume(tokcar, tokcdr, Token.LSBRA)
        tokcar, size_tok = consume(tokcar, tokcdr, Token.NUM)
        tokcar, _ = consume(tokcar, tokcdr, Token.RSBRA)
        size = int(size_tok)
    else:
        size = 1


with open('parsetest.mc') as f:
    parser(scanner(f.read(), Token.regexes))

