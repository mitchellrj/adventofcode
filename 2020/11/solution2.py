import collections
import sys
import time


FLOOR = '.'
OCCUPIED = '#'
UNOCCUPIED = 'L'
TRANSLATION = {
    UNOCCUPIED: False,
    OCCUPIED: True,
    FLOOR: None,
}


def get_occupancy(down, left, d_down, d_left, seat_map):
    area_width = len(seat_map[0])
    area_height = len(seat_map)
    next_down = down + d_down
    next_left = left + d_left
    if next_left not in range(area_width) or next_down not in range(area_height):
        return None
    s = seat_map[next_down][next_left]
    if s is None:
        return get_occupancy(next_down, next_left, d_down, d_left, seat_map)
    return s


def get_adjacency(down, left, seat_map):
    return [
        get_occupancy(down, left, -1, -1, seat_map),
        get_occupancy(down, left, -1, 0, seat_map),
        get_occupancy(down, left, -1, 1, seat_map),
        get_occupancy(down, left, 0, -1, seat_map),
        get_occupancy(down, left, 0, 1, seat_map),
        get_occupancy(down, left, 1, -1, seat_map),
        get_occupancy(down, left, 1, 0, seat_map),
        get_occupancy(down, left, 1, 1, seat_map),
    ]


def iterate(seat_map):
    next_generation_seat_map = []
    for d in range(len(seat_map)):
        next_generation_seat_map.append([])
        for l, s in enumerate(seat_map[d]):
            n = None
            if s is not None:
                c = collections.Counter(get_adjacency(d, l, seat_map))
                if not s:
                    n = c[True] == 0
                else:
                    n = c[True] < 5
            next_generation_seat_map[-1].append(n)

    return next_generation_seat_map


def print_seat_map(seat_map):
    inverse_translation = {v: k for k, v in TRANSLATION.items()}
    for r in seat_map:
        print(''.join(inverse_translation[s] for s in r))

    print()


def main(seat_map):
    last_generation_seat_map = []
    while last_generation_seat_map != seat_map:
        last_generation_seat_map = seat_map
        seat_map = iterate(seat_map)
    
    return len([s for r in seat_map for s in r if s])


def reader(fh):
    for l in fh:
        yield list(map(TRANSLATION.get, l.strip()))


if __name__ == '__main__':
    fname = sys.argv[1]
    with open(fname, 'r') as fh:
        inputs = list(reader(fh))

    start = time.monotonic_ns()
    result = main(inputs)
    end = time.monotonic_ns()

    print(result)
    print(f'Result calculated in {(end - start) / 1e3:0.3f} microseconds.', file=sys.stderr)