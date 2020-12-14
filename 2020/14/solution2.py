import functools
import itertools
import operator
import re
import sys
import time


SET_MASK = 'mask'
SET_MEM = 'mem'
PATTERN = re.compile(r'^([\w]+)(?:\[([\d]+)\])?\s*=\s*([\dX]+)$')


def make_masks(input_mask):
    return (
        # floating mask
        int(input_mask.replace('1', '0').replace('X', '1'), 2),
        # or mask
        int(input_mask.replace('X', '0'), 2)
    )


def main(commands):
    floating_mask, or_mask = make_masks('X' * 36)
    mem = {}
    for command, op1, op2 in commands:
        if command == SET_MEM:
            value = int(op2)
            op1 = int(op1) | or_mask | floating_mask
            n = r = floating_mask
            i = -1
            bits = set()
            while n:
                i += 1
                n, r = divmod(n, 2)
                if r:
                    bits.add(2**i)

            memsets = {}
            for l in range(len(bits) + 1):
                for b in itertools.permutations(bits, l):
                    a = functools.reduce(operator.or_, b, 0)
                    memsets[op1 - a] = value
    
            mem.update(memsets)
    
        elif command == SET_MASK:
            floating_mask, or_mask = make_masks(op2)
    
    return sum([v for v in mem.values()])


def print_mem(mem):
    for a in sorted(mem.keys()):
        v = mem[a]
        if v is None:
            continue
        print('{0:036b}  (decimal {0}) = {1}'.format(a, v))


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