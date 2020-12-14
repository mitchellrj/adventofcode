import re
import sys
import time


SET_MASK = 'mask'
SET_MEM = 'mem'
PATTERN = re.compile(r'^([\w]+)(?:\[([\d]+)\])?\s*=\s*([\dX]+)$')


def make_masks(input_mask):
    return (
        # and mask
        int(input_mask.replace('X', '1'), 2),
        # or mask
        int(input_mask.replace('X', '0'), 2)
    )


def main(commands):
    and_mask, or_mask = make_masks('X' * 36)
    mem = []
    for command, op1, op2 in commands:
        if command == SET_MEM:
            op1 = int(op1)
            if op1 >= len(mem):
                mem.extend([None] * (op1 - len(mem) + 1))
            mem[op1] = int(op2) & and_mask | or_mask
        elif command == SET_MASK:
            and_mask, or_mask = make_masks(op2)
    
    return sum([m for m in mem if m])



def reader(fh):
    for l in fh:
        match = PATTERN.match(l)
        command, op1, op2 = match.groups()
        yield command, op1, op2


if __name__ == '__main__':
    fname = sys.argv[1]
    with open(fname, 'r') as fh:
        inputs = list(reader(fh))

    start = time.monotonic_ns()
    result = main(inputs)
    end = time.monotonic_ns()

    print(result)
    print(f'Result calculated in {(end - start) / 1e3:0.3f} microseconds.', file=sys.stderr)