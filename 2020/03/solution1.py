import sys
import time


DOWN = 1
RIGHT = 3


def main(terrain_data):
    w = len(terrain_data[0])
    h = len(terrain_data)
    l = p = t = 0
    while True:
        l += DOWN
        p += RIGHT
        p = p % (w - 1)
        t += terrain_data[l][p]
        if l + 1 == h:
            break

    return t


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