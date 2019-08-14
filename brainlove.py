class Tape(list):
    def expand(self, n):
        self += [0] * (n - len(self))

    def __getitem__(self, i):
        self.expand(i + 1)
        return super().__getitem__(i)

    def __setitem__(self, i, x):
        self.expand(i + 1)
        return super().__setitem__(i, x)

def jump_table(prog):
    jumps = {}
    jump_stack = []
    for i, x in enumerate(prog):
        if x == '[':
            jump_stack.append(i)
        elif x == ']':
            s = jump_stack.pop()
            jumps[s], jumps[i] = i, s
    return jumps

def bfmachine(prog):
    ctr = ptr = 0
    tape = Tape()
    jumps = jump_table(prog)
    while ctr < len(prog):
        x = prog[ctr]
        if   x == '>':  ptr += 1
        elif x == '<':  ptr -= 1
        elif x == '+':  tape[ptr] += 1
        elif x == '-':  tape[ptr] -= 1
        elif x == '.':  yield chr(tape[ptr])
        elif x == ',':  tape[ptr] = ord((yield))
        elif x == '[':  ctr = jumps[ctr] if tape[ptr] == 0 else ctr
        elif x == ']':  ctr = jumps[ctr] if tape[ptr] != 0 else ctr
        ctr += 1

def buffer_routine(routine):
    """Takes a coroutine that operates on single character inputs and outputs,
    acts as a coroutine on arbitrary strings. The final output buffer is
    returned."""
    input_stack = []
    output_buffer = ''
    try:
        output = next(routine)
        while True:
            if output is None:
                if not input_stack:
                    input_stack = list(reversed((yield output_buffer)))
                    output_buffer = ''
                output = routine.send(input_stack.pop())
            else:
                output_buffer += output
                output = next(routine)
    except StopIteration:
        return output_buffer

def repl(evaluator, prompt="? "):
    """Provides a REPL for interacting with a coroutine."""
    try:
        output = next(evaluator)
        if output:
            print(output)
        while True:
            print(evaluator.send(input(prompt)))
    except EOFError:
        pass
    except StopIteration as final:
        print(final)

if __name__ == '__main__':
    import sys
    echo = "+[,.----]"
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            prog = f.read()
    else:
        prog = echo
    repl(buffer_routine(bfmachine(prog)))
