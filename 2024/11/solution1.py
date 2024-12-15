import math
import sys
import time


# It's a Game of Life sort of thing.


def main(stones, generations):
    for i in range(generations):
        evolve(stones)

    return len(stones)


def evolve(stones):
    i = 0
    while i < len(stones):
        stone = stones[i]
        # not using strings because logarithms are more pro
        digit_count = 1 if stone == 0 else math.floor(math.log10(stone) + 1)
        if stone == 0:
            stones[i] = 1
        elif digit_count % 2 == 0:
            # even number of digits - look ma, no strings
            left_half = int(stone // (10**(digit_count/2)))
            right_half = int(stone - left_half * (10**(digit_count/2)))
            stones[i] = left_half
            stones.insert(i + 1, right_half)
            i += 1 # Bonus 1 for the new stone inserted
        else:
            stones[i] = stone * 2024
        i += 1


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