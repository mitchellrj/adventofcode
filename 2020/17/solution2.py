import collections
import copy
import itertools
import sys
import time


def print_state(state):
    hyper_layer_midpoint = len(state) // 2
    layer_midpoint = len(state[0]) // 2
    for hl, hyper_layer in enumerate(state):
        for l, layer in enumerate(hyper_layer):
            print(f'z={l-layer_midpoint}, w={hl-hyper_layer_midpoint}')
            for row in layer:
                print(''.join(map(lambda c: '#' if c else '.', row)))
            print()


def get_neighbours(state, hyper_layer_index, layer_index, row_index, column_index):
    neighbours = []
    for hl, l, r, c in itertools.product(*([
            range(hyper_layer_index - 1, hyper_layer_index + 2),
            range(layer_index - 1, layer_index + 2),
            range(row_index - 1, row_index + 2),
            range(column_index - 1, column_index + 2),
        ])):
        if min(hl, l, r, c) < 0 or hl >= len(state) or l >= len(state[0]) or r >= len(state[0][0]) or c >= len(state[0][0][0]):
            neighbours.append(False)
        else:
            neighbours.append(state[hl][l][r][c])

    # 0-26 = hyper-layer below,
    # 27-35 = layer below,
    # 36-38 = row above,
    # 39 = cube left,
    # 40 = this,
    # 41 = cube right,
    # 42-44 = row below,
    # 45-53 = layer above,
    # 54-80 = hyper-layer above

    neighbours.pop(40)
    return neighbours


def grow_state(state):
    empty_row = [False] * (len(state[0][0][0]) + 2)
    empty_layer = [empty_row[:] for _ in range(len(state[0][0]) + 2)]
    empty_hyper_layer = [copy.deepcopy(empty_layer) for _ in range(len(state[0]) + 2)]
    new_state = [copy.deepcopy(empty_hyper_layer)]
    for hyper_layer in state:
        new_hyper_layer = [copy.deepcopy(empty_layer)]
        for layer in hyper_layer:
            new_layer = [empty_row[:]]
            for row in layer:
                new_layer.append([False] + row + [False])
            new_layer.append(empty_row[:])
            new_hyper_layer.append(new_layer)
        new_hyper_layer.append(copy.deepcopy(empty_layer))
        new_state.append(new_hyper_layer)

    new_state.append(copy.deepcopy(empty_hyper_layer))
    return new_state


def main(initial_state):
    state = [[initial_state]]
    for _ in range(6):
        state = grow_state(state)
        new_state = copy.deepcopy(state)
        for hl, l, r, c in itertools.product(range(0, len(state)), range(0, len(state[0])), range(0, len(state[0][0])), range(0, len(state[0][0][0]))):
            neighbours = get_neighbours(state, hl, l, r, c)
            neighbour_count = collections.Counter(neighbours)
            if state[hl][l][r][c] and neighbour_count[True] not in (2, 3):
                new_state[hl][l][r][c] = False
            elif (not state[hl][l][r][c]) and neighbour_count[True] == 3:
                new_state[hl][l][r][c] = True
        state = new_state

    return sum([c for hl in state for l in hl for r in l for c in r])


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