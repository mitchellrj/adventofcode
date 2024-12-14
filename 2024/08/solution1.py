import itertools
import sys
import time


def main(map_):
    node_positions = {}
    antinode_positions = set()
    x_max = len(map_[0])
    y_max = len(map_)
    for y, l in enumerate(map_):
        for x, c in enumerate(l):
            if c == '.':
                continue
            node_positions.setdefault(c, set())
            node_positions[c].add((x, y))

    for _, node_type_positions in node_positions.items():
        for position1, position2 in itertools.product(node_type_positions, node_type_positions):
            if position1 == position2:
                continue
            vector = (position2[0] - position1[0], position2[1] - position1[1])
            antinode_position = (position1[0] + (vector[0] * 2), position1[1] + (vector[1] * 2))
            if antinode_position[0] < 0 or antinode_position[0] >= x_max or antinode_position[1] < 0 or antinode_position[1] >= y_max:
                continue
            antinode_positions.add(antinode_position)

    return len(antinode_positions)
    

def reader(fh):
    map_ = []
    for l in fh:
        map_.append(list(l.strip()))
    return map_
        

if __name__ == '__main__':
    fname = sys.argv[1]
    with open(fname, 'r') as fh:
        map_ = reader(fh)
        start = time.monotonic_ns()
        result = main(map_)
        end = time.monotonic_ns()

    print(result)
    print(f'Result calculated in {(end - start) / 1e3:0.3f} microseconds.', file=sys.stderr)