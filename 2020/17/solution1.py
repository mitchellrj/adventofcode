import collections
import copy
import itertools
import sys
import time


def print_state(state):
    midpoint = len(state) // 2
    for l, layer in enumerate(state):
        print(f'z={l-midpoint}')
        for row in layer:
            print(''.join(map(lambda c: '#' if c else '.', row)))
        print()


def get_neighbours(state, layer_index, row_index, column_index):
    neighbours = []
    for l, r, c in itertools.product(*([
            range(layer_index - 1, layer_index + 2),
            range(row_index - 1, row_index + 2),
            range(column_index - 1, column_index + 2),
        ])):
        if min(l, r, c) < 0 or l >= len(state) or r >= len(state[0]) or c >= len(state[0][0]):
            neighbours.append(False)
        else:
            neighbours.append(state[l][r][c])


    # 0-8 = layer below,
    # 9-11 = row above,
    # 12 = cube left
    neighbours.pop(13)
    return neighbours


def grow_state(state):
    empty_row = [False] * (len(state[0][0]) + 2)
    empty_layer = [empty_row[:] for _ in range(len(state[0]) + 2)]
    new_state = [copy.deepcopy(empty_layer)]
    for layer in state:
        new_layer = [empty_row[:]]
        for row in layer:
            new_layer.append([False] + row + [False])
        new_layer.append(empty_row[:])
        new_state.append(new_layer)

    new_state.append(copy.deepcopy(empty_layer))
    return new_state


def main(initial_state):
    state = [initial_state]
    for _ in range(6):
        state = grow_state(state)
        new_state = copy.deepcopy(state)
        for l, r, c in itertools.product(range(0, len(state)), range(0, len(state[0])), range(0, len(state[0][0]))):
            neighbours = get_neighbours(state, l, r, c)
            neighbour_count = collections.Counter(neighbours)
            if state[l][r][c] and neighbour_count[True] not in (2, 3):
                new_state[l][r][c] = False
            elif (not state[l][r][c]) and neighbour_count[True] == 3:
                new_state[l][r][c] = True
        state = new_state

    # print(f'After {_ + 1} cycles:')
    # print()
    # print_state(state)
    return sum([c for l in state for r in l for c in r])


def reader(fh):
    for l in fh:
        yield list(map(lambda c: c == '#', l.strip()))


if __name__ == '__main__':
    fname = sys.argv[1]
    with open(fname, 'r') as fh:
        inputs = list(reader(fh))

    start = time.monotonic_ns()
    result = main(inputs)
    end = time.monotonic_ns()

    print(result)
    print(f'Result calculated in {(end - start) / 1e3:0.3f} microseconds.', file=sys.stderr)