import sys
import time


def main(union_group_yesses):
    return sum(map(len, union_group_yesses))


def reader(fh):
    yesses = set()
    for l in fh:
        l = l.strip()
        if not l:
            yield yesses
            yesses = set()
        yesses = yesses | set(l)

    yield yesses


if __name__ == '__main__':
    fname = sys.argv[1]
    with open(fname, 'r') as fh:
        inputs = list(reader(fh))

    start = time.monotonic_ns()
    result = main(inputs)
    end = time.monotonic_ns()

    print(result)
    print(f'Result calculated in {(end - start) / 1e3:0.3f} microseconds.', file=sys.stderr)