_compose = lambda f: lambda g: lambda *a, **k: f(g(*a, **k))

def line(level, s):
    return '\t' * level + s + '\n'

class Statements_AST:
    def __init__(self, statements):
        self.statements = statements

    @_compose(''.join)
    def tree(self, level=0):
        yield line(level, 'Statements')
        for statement in self.statements:
            yield statement.tree(level + 1)

class Comment_AST:
    def __init__(self, literal):
        if literal.startswith('REM '):
            self.comment = literal[4:]
        else:
            assert(literal == 'REM')
            self.comment = ''

    def tree(self, level=0):
        if self.comment:
            return line(level, f'Comment: {self.comment}')
        else:
            return line(level, 'Comment')

    def code(self):
        return ''

class Let_Statement_AST:
    def __init__(self, varname, value):
        self.varname = varname
        self.value = value

    @_compose(''.join)
    def tree(self, level=0):
        yield line(level, 'Let')
        yield line(level + 1, self.varname)
        yield line(level + 1, self.value)

class For_AST:
    def __init__(self, varname, start, stop, step, statements):
        self.varname = varname
        self.start = start
        self.stop = stop
        self.step = step
        self.statements = statements

    @_compose(''.join)
    def tree(self, level=0):
        yield line(level, 'For')
        yield line(level + 1, self.varname)
        yield line(level + 1, self.start)
        yield line(level + 1, self.stop)
        yield line(level + 1, self.step)
        yield self.statements.tree(level + 1)
