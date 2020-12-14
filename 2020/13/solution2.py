import functools
import math
import operator
import sys
import time


def get_factors(n):
    i = 2
    factors = set()
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.add(i)
    if n > 1:
        factors.add(n)
    return factors


def main(departure_intervals, init):
    # Sort of a lowest common denominator thing.
    # Start with the biggest numbers
    factors = set()
    for i in departure_intervals:
        factors |= get_factors(i)

    print(factors)

    sorted_departures = sorted(filter(lambda t: t[1], enumerate(departure_intervals)), reverse=True, key=lambda t: t[1])
    big, big_index = sorted_departures[0]

    mult_factor = math.floor(functools.reduce(operator.mul, factors, 1) / big)
    print(f'mult_factor = {mult_factor}')
    m = max(1, math.floor(init / big))
    while True:
        m += mult_factor
        try_range = m % mult_factor + len(departure_intervals)
        while m % mult_factor < try_range:
            m += 1
            n = (big * m) - big_index
            #print(f'try {big} x {m} - {big_index} = {n}')
            for idx, interval in sorted_departures[1:]:
                if interval == 0:
                    continue
                if (n + idx) % interval:
                    break
            else:
                return n + len(departure_intervals) - 1


def reader(fh):
    departure_time = int(fh.readline())
    departure_intervals = [0 if i == 'x' else int(i) for i in fh.readline().split(',')]
    return departure_intervals


if __name__ == '__main__':
    fname = sys.argv[1]
    init = int((sys.argv[2:] + [0])[0])
    with open(fname, 'r') as fh:
        inputs = reader(fh)

    start = time.monotonic_ns()
    result = main(inputs, init)
    end = time.monotonic_ns()

    print(result)
    print(f'Result calculated in {(end - start) / 1e3:0.3f} microseconds.', file=sys.stderr)