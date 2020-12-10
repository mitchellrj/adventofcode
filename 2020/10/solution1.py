import sys
import time


def main(joltages):
    # Sort the adapters
    joltages = sorted(joltages)
    # Always start at zero
    joltages.insert(0, 0)
    # Always end at three
    counts = {0: 0, 1: 0, 2: 0, 3: 1}
    for i in range(1, len(joltages)):
        diff = joltages[i] - joltages[i - 1]
        counts[diff] += 1

    return counts[1] * counts[3]


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