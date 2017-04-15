import re

class SyntaxError(Exception):
    pass

def express_syntax_error(src, pos):
    line_start = src[:pos].rfind('\n') + 1
    line_remaining = src[pos:].find('\n')
    if line_remaining == -1:
        line_end = len(src)
    else:
        line_end = pos + line_remaining
    line = src[line_start:line_end]
    ptr = ' ' * (pos - line_start) + '^'
    line_num = src[:pos].count('\n') + 1
    return f'Syntax Error on line {line_num}\n{line}\n{ptr}'

def unified_regex(regexes):
    return re.compile('|'.join(f'(?P<{t}>{r})' for t, r in regexes))

def skip_whitespace(src, pos):
    while pos < len(src) and src[pos].isspace():
        pos += 1
    return pos

def scanner(src, regexes):
    """Takes source code, and a list of tuples of the form (token_name,
    token_regex). Yields pairs (token_name, token_literal)."""
    regex = unified_regex(regexes)
    i = skip_whitespace(src, 0)
    while i < len(src):
        search = regex.match(src[i:])
        if not search:
            raise SyntaxError(express_syntax_error(src, i))
        matches = ((t, s) for t, s in search.groupdict().items() if s)
        token, token_literal = max(matches, key=lambda x: len(x[1]))
        yield token, token_literal
        i = skip_whitespace(src, i + len(token_literal))

