from scanner import scanner
from token import Token

class ParserError(Exception):
    def __init__(self, token_stream, *expected_tokens):
        template = "Received {}, expected {{{}}}"
        token = token_stream.current
        self.message = template.format(token, ', '.join(expected_tokens))

    def __str__(self):
        return self.message

class TokenStream:
    """Stream of tokens, with features needed by a parser."""

    def __init__(self, source):
        self.source = source
        self.current = next(self.source)

    def __iter__(self):
        yield self.current
        yield from self.source

    def lookahead(self):
        """See the token type at the front of the stream"""
        if self.current:
            return self.current[0]

    def consume(self, *expected):
        """Consume the current token, return the next token's literal
        representation and type"""
        print("Consuming,", self.current)
        if self.lookahead() not in expected:
            raise ParserError(self.current, expected)
        consumed_type, consumed_literal = self.current
        try:
            self.current = next(self.source)
        except StopIteration:
            self.current = None
        return consumed_literal, consumed_type

def parser(tokens):
    stream = TokenStream(tokens)
    return statements(stream)


class statements_ast:
    def __init__(self, statements):
        self.statements = statements

    def tree(self, indent=0):
        return '\n'.join(st.tree(indent+1) for st in self.statements)

def statements(stream):
    statements_list = []
    while stream.lookahead():
        statements_list.append(statement(stream))
    return statements_ast(statements_list)

def statement(stream):
    if stream.lookahead() == Token.LET:
        return let(stream)
    else:
        raise ParserError(stream, Token.LET)

class let_ast:
    def __init__(self, var, size):
        self.var = var
        self.size = size

    def tree(self, indent=0):
        return '\t' * indent + f'Let {self.var}[{self.size}]'

def let(stream):
    stream.consume(Token.LET)
    var, _ = stream.consume(Token.ID)
    if stream.lookahead() == Token.LSBRA:
        stream.consume(Token.LSBRA)
        size_tok, _ = stream.consume(Token.NUM)
        stream.consume(Token.RSBRA)
        size = int(size_tok)
    else:
        size = 1
    return let_ast(var, size)


with open('parsetest.mc') as f:
    ast = parser(scanner(f.read(), Token.regexes))
    print(ast.tree())

