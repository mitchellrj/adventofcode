import operator
import re
import sys
import time


UNCORRUPTED = re.compile(r'do\(\)|mul\(([0-9]{1,3}),([0-9]{1,3})\)|don\'t\(\)')


def main(lines):
    result = 0
    enabled = True
    for line in lines:
        for uncorrupted_tokens in re.finditer(UNCORRUPTED, line):
            if uncorrupted_tokens[0] == 'do()':
                enabled = True
            elif uncorrupted_tokens[0] == 'don\'t()':
                enabled = False
            elif enabled:
                result += int(uncorrupted_tokens[1], 10) * int(uncorrupted_tokens[2], 10)

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