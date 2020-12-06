import sys
import time


def main(yesses):
    return sum(map(len, yesses))


def reader(fh):
    new_group = True
    for l in fh:
        l = l.strip()
        if not l:
            yield yesses
            new_group = True
            continue
        if new_group:
            yesses = set(l)
            new_group = False
        else:
            yesses = yesses & set(l)

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