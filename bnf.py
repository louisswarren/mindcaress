from token import Token
from lexer import Lexer, ParseError
from ast import *

def parse(tokens):
    return statements(tokens)

def statements(tokens):
    statements_list = []
    while tokens:
        if tokens.lookahead_in(Token.COMMENT):
            tokens.chomp(Token.COMMENT)
            tokens.chomp(Token.NEWLINE)
        stmt = statement(tokens)
        if stmt:
            statements_list.append(stmt)
        else:
            break
    return Statements_AST(statements_list)

def statement(tokens):
    if tokens.lookahead_in(Token.LET):
        return let_statement(tokens)
    elif tokens.lookahead_in(Token.FOR):
        return for_block(tokens)

def let_statement(tokens):
    tokens.chomp(Token.LET)
    varname = tokens.chomp(Token.ID)
    tokens.chomp(Token.EQUALS)
    value = expression(tokens)
    tokens.chomp(Token.NEWLINE)
    return Let_Statement_AST(varname, value)

def for_block(tokens):
    tokens.chomp(Token.FOR)
    varname = tokens.chomp(Token.ID)
    tokens.chomp(Token.EQUALS)
    start = expression(tokens)
    tokens.chomp(Token.TO)
    stop = expression(tokens)
    if tokens.lookahead_in(Token.STEP):
        tokens.chomp(Token.STEP)
        step = expression(tokens)
    else:
        step = '1'
    tokens.chomp(Token.NEWLINE)
    # This won't work yet as statements won't stop at NEXT
    inner = statements(tokens)
    tokens.chomp(Token.NEXT)
    if tokens.lookahead_in(Token.ID):
        next_varname = tokens.chomp(Token.ID)
        # Need an error message for this
        assert(varname == next_varname)
    tokens.chomp(Token.NEWLINE)
    return For_AST(varname, start, stop, step, inner)

def expression(tokens):
    print("Expression not fully implemented")
    return tokens.chomp(Token.NUM)


with open('example.bas') as f:
    ast = parse(Lexer(f.read(), Token))
    print(ast.tree())
