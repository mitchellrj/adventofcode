import functools
import operator
import sys
import time


VECTORS = frozenset([
    (1, 1),
    (3, 1),
    (5, 1),
    (7, 1),
    (1, 2),
])


def main(terrain_data):
    t = []
    for r, d in VECTORS:
        w = len(terrain_data[0])
        h = len(terrain_data)
        l = p = 0
        t.append(0)
        while True:
            l += d
            p += r
            p = p % (w - 1)
            t[-1] += terrain_data[l][p]
            if l + 1 == h:
                break

    return functools.reduce(operator.mul, t, 1)


def reader(fh):
    for l in fh:
        yield list(map(lambda c: c != '.', l))


if __name__ == '__main__':
    fname = sys.argv[1]
    with open(fname, 'r') as fh:
        inputs = list(reader(fh))

    start = time.monotonic_ns()
    result = main(inputs)
    end = time.monotonic_ns()

    print(result)
    print(f'Result calculated in {(end - start) / 1e3:0.3f} microseconds.', file=sys.stderr)