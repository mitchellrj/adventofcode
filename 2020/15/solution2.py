import sys
import time


TARGET = 30_000_000


def main(numbers):
    history = {v: k for k, v in enumerate(numbers)}
    i = len(numbers)
    last = numbers[-1]
    while i < TARGET:
        n = i - 1 - history.get(last, i - 1)
        history[last] = i - 1
        last = n
        i += 1

    return n


def reader(fh):
    for l in fh:
        for n in l.strip().split(','):
            yield int(n)


if __name__ == '__main__':
    fname = sys.argv[1]
    with open(fname, 'r') as fh:
        inputs = list(reader(fh))

    start = time.monotonic_ns()
    result = main(inputs)
    end = time.monotonic_ns()

    print(result)
    print(f'Result calculated in {(end - start) / 1e3:0.3f} microseconds.', file=sys.stderr)