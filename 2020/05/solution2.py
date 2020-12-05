import sys
import time


ROWS = 128
COLS = 8
ROW_TRANSLATION = str.maketrans({'B': '1', 'F': '0'})
COL_TRANSLATION = str.maketrans({'R': '1', 'L': '0'})


def main(seats):
    seat_ids = [False] * 1024
    for rpos, cpos in seats:
        seat_ids[(rpos << 3) | cpos] = True

    s = -1
    while True:
        s = i = seat_ids.index(False, s + 1)
        while not seat_ids[s + 1]:
            s += 1
        if s == i and seat_ids[i - 1]:
            return i


def reader(fh):
    for l in fh:
        yield (
            int(l[:7].translate(ROW_TRANSLATION), 2),
            int(l.strip()[7:].translate(COL_TRANSLATION), 2)
        )


if __name__ == '__main__':
    fname = sys.argv[1]
    with open(fname, 'r') as fh:
        inputs = list(reader(fh))

    start = time.monotonic_ns()
    result = main(inputs)
    end = time.monotonic_ns()

    print(result)
    print(f'Result calculated in {(end - start) / 1e3:0.3f} microseconds.', file=sys.stderr)