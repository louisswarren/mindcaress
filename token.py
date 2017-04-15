class Token:
    ELSE =            'ELSE'
    END =             'END'
    IF =              'IF'
    INPUT =           'INPUT'
    LET =             'LET'
    MACRO =           'MACRO'
    PRINT =           'PRINT'
    THEN =            'THEN'
    COMMA =           'COMMA'
    ASSIGN =          'ASSIGN'
    ADD =             'ADD'
    DIV =             'DIV'
    MUL =             'MUL'
    SUB =             'SUB'
    LPAR =            'LPAR'
    RPAR =            'RPAR'
    LSBRA =           'LSBRA'
    RSBRA =           'RSBRA'
    ID =              'ID'
    MACROID =         'MACROID'
    MACROPARAM =      'MACROPARAM'
    NUM =             'NUM'
    CHAR =            'CHAR'
    STR =             'STR'

    regexes = [
        (ELSE,        'ELSE'                 ),
        (END,         'END'                  ),
        (IF,          'IF'                   ),
        (INPUT,       'INPUT'                ),
        (LET,         'LET'                  ),
        (MACRO,       'MACRO'                ),
        (PRINT,       'PRINT'                ),
        (THEN,        'THEN'                 ),
        (COMMA,       ','                    ),
        (ASSIGN,      '='                    ),
        (ADD,         '[+]'                  ),
        (DIV,         '[/]'                  ),
        (MUL,         '[*]'                  ),
        (SUB,         '-'                    ),
        (LPAR,        '[(]'                  ),
        (RPAR,        '[)]'                  ),
        (LSBRA,       '\\['                  ),
        (RSBRA,       '\\]'                  ),
        (ID,          '[a-z_][a-z0-9_]*'     ),
        (MACROID,     '@[a-z_][a-z0-9_]*'    ),
        (MACROPARAM,  '[$][a-z_][a-z0-9_]*'  ),
        (NUM,         '[0-9]+'               ),
        (CHAR,        "'.'"                  ),
        (STR,         '"([^"]|\\\\")+"'      ),
    ]


