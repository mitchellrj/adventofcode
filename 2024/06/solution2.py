import sys
import time


MOVEMENT_MATRIX = [
    ( 0, -1), # north
    ( 1,  0), # east
    ( 0,  1), # south
    (-1,  0), # west
]


def main(map_, guard_position):
    # This brute-force solution is slow has all heck. But it does work.

    result = 0
    for p in range(len(map_) * len(map_[0])):
        x = p % len(map_[0])
        y = p // len(map_[0])
        if map_[y][x] or (x, y) == guard_position:
            continue
        map_[y][x] = True
        result += test_path(map_, guard_position)
        map_[y][x] = False

    return result


def test_path(map_, guard_position):
    y_max = len(map_)
    x_max = len(map_[0])
    seen = set()
    direction = 0
    while True:
        pose = guard_position + (direction,)
        if pose in seen:
            return True
        seen.add(pose)
        next_guard_position = (
            guard_position[0] + MOVEMENT_MATRIX[direction][0],
            guard_position[1] + MOVEMENT_MATRIX[direction][1],
            )
        if next_guard_position[0] < 0 or next_guard_position[0] >= x_max or next_guard_position[1] < 0 or next_guard_position[1] >= y_max:
            return False
        if map_[next_guard_position[1]][next_guard_position[0]]:
            direction = (direction + 1) % 4
            continue
        guard_position = next_guard_position


def reader(fh):
    map_ = []
    guard_position = ()
    y = 0
    for l in fh:
        x = 0
        row = []
        map_.append(row)
        for c in l.strip():
            row.append(c == '#')
            if c in ('V', '<', '>', '^'):
                guard_position = (x, y)
            x += 1
        y += 1

    return map_, guard_position
        

if __name__ == '__main__':
    fname = sys.argv[1]
    with open(fname, 'r') as fh:
        map_, guard_postiion = reader(fh)
        start = time.monotonic_ns()
        result = main(map_, guard_postiion)
        end = time.monotonic_ns()

    print(result)
    print(f'Result calculated in {(end - start) / 1e3:0.3f} microseconds.', file=sys.stderr)