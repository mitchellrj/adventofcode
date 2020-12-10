import functools
import operator
import sys
import time


ACCEPTABLE_RANGE = range(4)


def main(joltages):
    # Sort the adapters
    joltages = sorted(joltages)
    # Always start at zero
    joltages.insert(0, 0)
    # Always end at +3
    joltages.append(joltages[-1] + 3)
    i = 0
    peeks = {}
    # Work backwards, accumulating the number of permissible steps to reach the target
    for i in range(len(joltages) - 1, -1, -1):
        # We don't care about single steps
        peeks.setdefault(i, 1)
        j = i - 1
        while j >= 0 and (joltages[i] - joltages[j]) in ACCEPTABLE_RANGE:
            peeks.setdefault(j, 0)
            peeks[j] += peeks[i]
            j -= 1

    return peeks[0]


def reader(fh):
    for l in fh:
        yield int(l)


if __name__ == '__main__':
    fname = sys.argv[1]
    with open(fname, 'r') as fh:
        inputs = list(reader(fh))

    start = time.monotonic_ns()
    result = main(inputs)
    end = time.monotonic_ns()

    print(result)
    print(f'Result calculated in {(end - start) / 1e3:0.3f} microseconds.', file=sys.stderr)