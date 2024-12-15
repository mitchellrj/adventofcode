import math
import sys
import time


# It's a Game of Life sort of thing.


def main(stones, generations):
    stone_count = 0
    evolutionary_patterns = {}
    # change to evolve one stone at a time rather than one generation at a time, and cache intermediate results
    for stone in stones:
        stone_count += 1 + evolve(evolutionary_patterns, stone, generations)

    return stone_count


def evolve(evolutionary_patterns, stone, remaining_generations):
    if remaining_generations == 0:
        return 0

    if (stone, remaining_generations) in evolutionary_patterns:
        return evolutionary_patterns[(stone, remaining_generations)]

    # not using strings because logarithms are more pro
    digit_count = 1 if stone == 0 else math.floor(math.log10(stone) + 1)
    if stone == 0:
        additional_stone_count = evolve(evolutionary_patterns, 1, remaining_generations - 1)
    elif digit_count % 2 == 0:
        # even number of digits - look ma, no strings
        left_half = int(stone // (10**(digit_count/2)))
        right_half = int(stone - left_half * (10**(digit_count/2)))
        left_count = evolve(evolutionary_patterns, left_half, remaining_generations - 1)
        right_count = evolve(evolutionary_patterns, right_half, remaining_generations - 1)
        additional_stone_count = left_count + right_count + 1
    else:
        additional_stone_count = evolve(evolutionary_patterns, stone * 2024, remaining_generations - 1)

    evolutionary_patterns[(stone, remaining_generations)] = additional_stone_count
    return additional_stone_count


def reader(fh):
    return list(map(int, fh.readline().strip().split()))
        

if __name__ == '__main__':
    fname = sys.argv[1]
    generations = int(sys.argv[2])
    with open(fname, 'r') as fh:
        stones = reader(fh)
        start = time.monotonic_ns()
        result = main(stones, generations)
        end = time.monotonic_ns()

    print(result)
    print(f'Result calculated in {(end - start) / 1e3:0.3f} microseconds.', file=sys.stderr)