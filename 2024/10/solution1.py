import sys
import time


MOVEMENT_MATRIX = [
    ( 0, -1), # north
    ( 1,  0), # east
    ( 0,  1), # south
    (-1,  0), # west
]


def main(topography):
    total_score = 0

    # find trailheads
    for y, row in enumerate(topography):
        for x, h in enumerate(row):
            if h == 0:
                # start walking
                summits = set()
                walk(summits, topography, x, y)
                trailhead_score = len(summits)
                total_score += trailhead_score

    return total_score


def walk(summits_seen, topography, x, y, current=0, points_seen=None):
    y_max = len(topography)
    x_max = len(topography[0])

    # Cut if we've already reached this same point by some other path
    if points_seen is None:
        points_seen = set()

    if (x, y) in points_seen:
        return

    for m in MOVEMENT_MATRIX:
        next_x, next_y = x + m[0], y + m[1]
        if any([next_x < 0, next_y < 0, next_x >= x_max, next_y >= y_max]):
            # out of bounds
            continue

        points_seen.add((next_x, next_y))
        next_h = topography[next_y][next_x]
        if next_h != current + 1:
            # too big a jump
            continue
        
        if next_h == 9:
            # found the summit
            summits_seen.add((next_x, next_y))
            continue
        
        walk(summits_seen, topography, next_x, next_y, next_h)

    return
    

def reader(fh):
    topography = []
    for l in fh:
        row = []
        for h in l.strip():
            if not h.isdigit():
                row.append(sys.maxsize)
            else:
                row.append(int(h))
        topography.append(row)

    return topography
        

if __name__ == '__main__':
    fname = sys.argv[1]
    with open(fname, 'r') as fh:
        topography = reader(fh)
        start = time.monotonic_ns()
        result = main(topography)
        end = time.monotonic_ns()

    print(result)
    print(f'Result calculated in {(end - start) / 1e3:0.3f} microseconds.', file=sys.stderr)