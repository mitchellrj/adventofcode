import sys
import time


SEAT_TRANSLATION = str.maketrans({'R': '1', 'L': '0', 'B': '1', 'F': '0'})


def main(seats):
    top_seat_id = 0
    for seat_id in seats:
        top_seat_id = max(seat_id, top_seat_id)
    return top_seat_id



def reader(fh):
    for l in fh:
        yield int(l.translate(SEAT_TRANSLATION), 2)


if __name__ == '__main__':
    fname = sys.argv[1]
    with open(fname, 'r') as fh:
        inputs = list(reader(fh))

    start = time.monotonic_ns()
    result = main(inputs)
    end = time.monotonic_ns()

    print(result)
    print(f'Result calculated in {(end - start) / 1e3:0.3f} microseconds.', file=sys.stderr)