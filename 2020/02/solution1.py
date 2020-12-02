import sys
import time


def main(password_data):
    v = 0
    for (n, x), c, p in password_data:
        t = 0
        if len(p) < x:
            # cut early if the password is shorter than the maximum required characters
            continue
        for pc in p:
            t += pc == c
            if t > x:
                break
        else:
            if t >= n:
                v += 1
    return v


def reader(fh):
    for l in fh:
        parts = l.split(' ')
        n, x = map(int, parts[0].split('-'))
        c = parts[1][0]
        p = parts[2]
        yield (n, x), c, p


if __name__ == '__main__':
    fname = sys.argv[1]
    with open(fname, 'r') as fh:
        inputs = list(reader(fh))

    start = time.monotonic_ns()
    result = main(inputs)
    end = time.monotonic_ns()

    print(result)
    print(f'Result calculated in {(end - start) / 1e3:0.3f} microseconds.', file=sys.stderr)