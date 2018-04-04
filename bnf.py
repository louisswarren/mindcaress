from token import Token
from lexer import Lexer, ParseError
from ast import *

def parse(tokens):
    return statements(tokens)

def statements(tokens):
    statements_list = []
    while tokens:
        if tokens.lookahead_in(Token.COMMENT):
            tokens.consume(Token.COMMENT)
            tokens.consume(Token.NEWLINE)
        else:
            statements_list.append(statement(tokens))
    return Statements_AST

def statement(tokens):
    if tokens.lookahead_in(Token.LET):
        return let_statement(tokens)
    else:
        raise ParseError(tokens, Token.LET)

def let_statement(tokens):
    tokens.consume(Token.LET)
    varname = tokens.consume(Token.ID)
    tokens.consume(Token.EQUALS)
    value = expression(tokens)
    tokens.consume(Token.NEWLINE)

def expression(tokens):
    return tokens.consume(Token.NUM)


with open('example.bas') as f:
    ast = parse(Lexer(f.read(), Token))
#    print(ast.tree())
