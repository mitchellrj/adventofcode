import sys
import time


MATCH_MATRIX = [
    (
        ((-1, -1), ( 0,  0), ( 1,  1)), # north west to south east
        (( 1,  1), ( 0,  0), (-1, -1)), # south east to north west
    ),
    (
        ((-1,  1), ( 0,  0), ( 1, -1)), # north east to south west
        (( 1, -1), ( 0,  0), (-1,  1)), # south west to north east
    )
]


def main(grid):
    result = 0
    y_max = len(grid)
    x_max = len(grid[0])
    for x in range(1, x_max - 1):
        for y in range(1, y_max - 1):
            if grid[y][x] != 'A':
                continue
            for axis in MATCH_MATRIX:
                if 'MAS' not in (get_term(grid, x, y, axis[0]), get_term(grid, x, y, axis[1])):
                    break
            else:
                result += 1

    return result

def get_term(grid, x, y, positions):
    term = ''
    for p in positions:
        term += grid[y + p[1]][x + p[0]]

    return term


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