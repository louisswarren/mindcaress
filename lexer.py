import re

class ScannerError(Exception):
    def __init__(self, src, pos):
        line_start = src[:pos].rfind('\n') + 1
        line_remaining = src[pos:].find('\n')
        if line_remaining == -1:
            line_end = len(src)
        else:
            line_end = pos + line_remaining
        line = src[line_start:line_end]
        ptr = ' ' * (pos - line_start) + '^'
        line_num = src[:pos].count('\n') + 1
        self.message = f'Scanner Error on line {line_num}\n{line}\n{ptr}'

    def __str__(self):
        return self.message

class ParseError(Exception):
    def __init__(self, tokens, *expected_tokens):
        template = "Received {}, expected {{{}}}"
        if tokens:
            token_msg = "{} ({})".format(*map(str, tokens.lookahead))
        else:
            token_msg = 'out of tokens'
        expected_msg = ', '.join(map(str, expected_tokens))
        self.message = template.format(token_msg, expected_msg)

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


def skip_whitespace(src, pos):
    while pos < len(src) and src[pos].isspace() and src[pos] != '\n':
        pos += 1
    return pos

def tokenise(src, token_enum):
    """Takes source code, and an enumeration of tokens with their regexes.
    Yields pairs (token_name, token_value)."""
    regex = re.compile('|'.join(f'(?P<{t.name}>{t.value})' for t in token_enum))
    i = skip_whitespace(src, 0)
    while i < len(src):
        search = regex.match(src[i:])
        if not search:
            raise ScannerError(src, i)
        matches = ((t, s) for t, s in search.groupdict().items() if s)
        token_typename, token_literal = max(matches, key=lambda x: len(x[1]))
        token = token_enum.__members__[token_typename]
        yield token, token_enum.evaluate(token, token_literal)
        i = skip_whitespace(src, i + len(token_literal))


class Lexer(Lookahead):
    """Stream of tokens, with features needed by a parser."""
    def __init__(self, src, token_enum):
        self.token_enum = token_enum
        return super().__init__(tokenise(src, token_enum))

    def lookahead_in(self, *expected):
        return self.lookahead[0] in expected

    def consume(self, *expected_list):
        """Consume the current token. Returns its type and value."""
        if expected_list and not self.lookahead_in(*expected_list):
            raise ParseError(self, *expected_list)
        token, value = next(self)
        print("Consumed", token, value)
        return token, value

    def chomp(self, expected):
        """Consume the current token and return its value."""
        _, value = self.consume(expected)
        return value

if __name__ == '__main__':
    with open('example.bas') as f:
        from token import Token
        tokens = Lexer(f.read(), Token)
        while tokens:
            print(tokens.consume())
