import sys
import time


TARGET = 2020


def main(expenses):
    expenses_sorted = sorted(expenses, reverse=True)
    for i, e in enumerate(expenses_sorted):
        if e < 2020:
            break
    if i:
        expenses_sorted = expenses_sorted[i:]
    b = 0
    while True:
        l = len(expenses_sorted)
        while True:
            l -= 1
            m = l
            while True:
                m -= 1
                s = expenses_sorted[b] + expenses_sorted[m] + expenses_sorted[l]
                if s == TARGET:
                    return expenses_sorted[l] * expenses_sorted[m] * expenses_sorted[b]
                elif s > TARGET:
                    break
            if l <= b or (expenses_sorted[b] + expenses_sorted[l] + 1) > TARGET:
                break
        b += 1


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