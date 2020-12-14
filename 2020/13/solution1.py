import bisect
import sys
import time


def main(departure_time, departure_intervals):
    departure_intervals = sorted(departure_intervals)
    highest_frequency = departure_intervals[0]
    best_waiting_time = departure_intervals[-1]
    bus_id = departure_time * 2
    bisection_point = min(len(departure_intervals) - 1, bisect.bisect_left(departure_intervals, bus_id))
    last_bisection = len(departure_intervals)
    c = 0
    while last_bisection > 0:
        while bisection_point == last_bisection:
            bisection_point -= 1

        i = bisection_point
        greatest_period = (departure_intervals[bisection_point] % highest_frequency)
        if greatest_period == 0:
            greatest_period = departure_intervals[bisection_point]
        lowest_frequency = departure_intervals[bisection_point] + greatest_period
        while i < last_bisection and departure_intervals[i] < lowest_frequency:
            waiting_time = departure_intervals[i] - (departure_time % departure_intervals[i])
            if waiting_time == 0:
                return departure_intervals[i], 0
            elif waiting_time < best_waiting_time:
                best_waiting_time = waiting_time
                bus_id = departure_intervals[i]
            i += 1
        last_bisection = bisection_point
        bisection_point = min(
            len(departure_intervals) - 1,
            bisect.bisect_left(departure_intervals, departure_intervals[bisection_point] / 2)
        )
        c += 1
    return best_waiting_time, bus_id


def reader(fh):
    departure_time = int(fh.readline())
    departure_intervals = [int(i) for i in fh.readline().split(',') if i != 'x']
    return departure_time, departure_intervals


if __name__ == '__main__':
    fname = sys.argv[1]
    with open(fname, 'r') as fh:
        inputs = reader(fh)

    start = time.monotonic_ns()
    waiting_time, bus_id = main(*inputs)
    result = waiting_time * bus_id
    end = time.monotonic_ns()

    print(result)
    print(f'Result calculated in {(end - start) / 1e3:0.3f} microseconds.', file=sys.stderr)