import sys
import time


TERM = 'XMAS'
MOVEMENT_MATRIX = [
    ( 0, -1), # north
    ( 1, -1), # north east
    ( 1,  0), # east
    ( 1,  1), # south east
    ( 0,  1), # south
    (-1,  1), # south west
    (-1,  0), # west
    (-1, -1), # north west
]


def main(grid):
    result = 0
    # The old word search puzzle. Seen this many years. Let's solve it independently again..
    y_max = len(grid)
    x_max = len(grid[0])
    for x in range(x_max):
        for y in range(y_max):
            # start search
            for direction in MOVEMENT_MATRIX:
                # Check we have room to find the term if moving in this direction
                direction_out_of_bounds = not valid_position(
                    x_max, y_max,
                    x + direction[0] * (len(TERM) - 1),
                    y + direction[1] * (len(TERM) - 1),
                )
                if direction_out_of_bounds:
                    continue
                # check if the term matches
                result += walk(x, y, direction, grid, remaining=TERM)

    return result

def walk(x, y, direction, grid, remaining):
    if not remaining:
        return True
    if remaining[0] != grid[y][x]: # grid is read as y/x, not x/y
        return False
    return walk(x + direction[0], y + direction[1], direction, grid, remaining[1:])


def valid_position(x_max, y_max, x, y):
    return (0 <= x < x_max) and (0 <= y < y_max)


def reader(fh):
    grid = []
    for line in fh:
        grid.append(list(line.strip()))
    return grid
        

if __name__ == '__main__':
    fname = sys.argv[1]
    with open(fname, 'r') as fh:
        grid = reader(fh)
        start = time.monotonic_ns()
        result = main(grid)
        end = time.monotonic_ns()

    print(result)
    print(f'Result calculated in {(end - start) / 1e3:0.3f} microseconds.', file=sys.stderr)