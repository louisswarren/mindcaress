import enum

class Token(enum.Enum):
    NEWLINE    = "\\n"
    COMMENT    = 'REM(\s[^\\n]*)?'
    LET        = 'LET'
    IF         = 'IF'
    THEN       = 'THEN'
    ELSEIF     = 'ELSEIF'
    ELSE       = 'ELSE'
    END        = 'END'
    FOR        = 'FOR'
    TO         = 'TO'
    STEP       = 'STEP'
    NEXT       = 'NEXT'
    PRINT      = 'PRINT'
    INPUT      = 'INPUT'
    EQUALS     = '='
    ADD        = '[+]'
    DIV        = '/'
    MUL        = '[*]'
    SUB        = '-'
    LPAR       = '[(]'
    RPAR       = '[)]'
    SID        = '[a-z_][a-z0-9_]*[$]'
    ID         = '[a-z_][a-z0-9_]*'
    NUM        = '[0-9]+'
    STR        = '"(([^"]|\\\\")*[^\\\\])?"'

    @staticmethod
    def evaluate(token, literal):
        if token == Token.COMMENT:
            if literal.startswith('REM '):
                return literal[4:]
            else:
                assert(literal == 'REM')
                return ''
        elif token in (Token.ID, Token.SID, Token.NUM):
            return literal
        elif token == Token.STR:
            return literal[1:-1]
        else:
            return None
