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
        elif x == '.':  yield tape[ptr]
        elif x == ',':  tape[ptr] = yield
        elif x == '[':  ctr = jumps[ctr] if tape[ptr] == 0 else ctr
        elif x == ']':  ctr = jumps[ctr] if tape[ptr] != 0 else ctr
        ctr += 1

def buffer_routine(routine):
    """Takes a coroutine that operates on single character inputs and outputs,
    acts as a coroutine on arbitrary strings. The final output buffer is
    returned."""
    input_stack = []
    output_buffer = ''
    output = next(routine)
    try:
        while True:
            if output is None:
                if not input_stack:
                    input_text = yield output_buffer
                    input_stack = list(reversed(input_text))
                    output_buffer = ''
                output = routine.send(ord(input_stack.pop()))
            else:
                output_buffer += chr(output)
                output = next(routine)
    except StopIteration:
        return output_buffer

def repl(evaluator, prompt="? "):
    """Provides a REPL for interacting with a coroutine."""
    output = next(evaluator)
    try:
        while True:
            print(evaluator.send(input(prompt)))
    except StopIteration as final:
        print(final)


if __name__ == '__main__':
    echo = "+[,.----]"
    repl(buffer_routine(bfmachine(echo)))

