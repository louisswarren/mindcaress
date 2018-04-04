from token import Token
from lexer import Lexer

def parse(tokens):
    return statements(tokens)

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
    ast = parse(Lexer(f.read(), Token))
#    print(ast.tree())
