import sys
import time


def main(password_data):
    v = 0
    for (n, x), c, p in password_data:
        v += (p[n - 1] == c) ^ (p[x - 1] == c)
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

    start = time.time()
    result = main(inputs)
    end = time.time()

    print(result)
    print(f'Result calculated in {round(end - start):0.5f} seconds.', file=sys.stderr)