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

class TokenStream:
    """Stream of tokens, with features needed by a parser. Strips comments and
    handles macros."""

    def __init__(self, source):
        self.source = source
        self.next_token()

    def __iter__(self):
        yield self.current
        yield from self.source

    def lookahead(self):
        """See the token type at the front of the stream"""
        if self.current:
            return self.current[0]

    def consume(self, *expected):
        """Consume the current token, return the next token's literal
        representation and type. If expected is empty, all tokens are
        accepted."""
        print("Consuming,", self.current)
        if self.lookahead() not in expected and expected:
            raise ParserError(self, *expected)
        consumed_type, consumed_literal = self.current
        try:
            self.next_token()
        except StopIteration:
            self.current = None
        return consumed_literal, consumed_type

    def try_consume(self, *expected):
        if self.lookahead() in expected:
            return self.consume(*expected)

    def next_token(self):
        while True:
            self.current = next(self.source)
            if self.stream.lookahead() == Token.COMMENT:
                self.stream.consume(Token.COMMENT)
            elif self.stream.lookahead() == Token.MACRO:
                self._defmacro()
            elif self.stream.lookahead() == Token.MACROID:
                raise NotImplementedError
            else:
                break

    def _defmacro(self):
        self.consume(Token.MACRO)
        name, _ = self.consume(Token.MACROID)
        if self.consume(Token.LPAR):
            params = [self.consume(Token.MACROPARAM)[0]]
            while self.try_consume(Token.COMMA):
                params.append(self.consume(Token.MACROPARAM)[0])
            self.consume(Token.RPAR)
        else:
            params = []
        self.consume(Token.LBRAC)
        contents = []
        while not self.try_consume(Token.RBRAC):
            contents.append(self.consume())
        self.macros[name] = (params, contents)


def parser(tokens):
    stream = Preprocessor(TokenStream(tokens))
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
    if stream.try_consume(Token.LSBRA):
        size_tok, _ = stream.consume(Token.NUM)
        stream.consume(Token.RSBRA)
        size = int(size_tok)
    else:
        size = 1
    var, _ = stream.consume(Token.ID)
    if stream.try_consume(Token.ASSIGN):
        expr = expression()
        return statements_ast(let_ast(var, size), expr)
    else:
        return let_ast(var, size)

def value(stream):
    if stream.lookahead() == Token.NUM:
        return literal_ast(int(stream.consume(Token.NUM)[0]))
    elif stream.lookahead() == Token.CHR:
        return literal_ast(ord(stream.consume(Token.CHR)[0][1]))
    else:
        raise ParserError(stream, Token.NUM, Token.CHR)



with open('example.mc') as f:
    ast = parser(scanner(f.read(), Token.regexes))
    print(ast.tree())


