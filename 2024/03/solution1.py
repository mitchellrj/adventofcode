import operator
import re
import sys
import time


UNCORRUPTED = re.compile(r'mul\(([0-9]{1,3}),([0-9]{1,3})\)')


def main(lines):
    result = 0
    for line in lines:
        for uncorrupted_mul_args in re.finditer(UNCORRUPTED, line):
            result += int(uncorrupted_mul_args[1], 10) * int(uncorrupted_mul_args[2], 10)

    return result


def reader(fh):
    yield from fh
        

if __name__ == '__main__':
    fname = sys.argv[1]
    with open(fname, 'r') as fh:
        lines = reader(fh)
        start = time.monotonic_ns()
        result = main(lines)
        end = time.monotonic_ns()

    print(result)
    print(f'Result calculated in {(end - start) / 1e3:0.3f} microseconds.', file=sys.stderr)