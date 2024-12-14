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
            antinode_position = position1
            while True:
                antinode_position = (antinode_position[0] + vector[0], antinode_position[1] + vector[1])
                if 0 <= antinode_position[0] < x_max and 0 <= antinode_position[1] < y_max:
                    antinode_positions.add(antinode_position)
                else:
                    break

    # for y, row in enumerate(map_):
    #     for x, c in enumerate(row):
    #         print(c if (x, y) not in antinode_positions else '#', end='')
    #     print()

    # print(antinode_positions)

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