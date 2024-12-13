import collections
import re
import sys
import time
import typing


def main(list1, list2):
    result = 0
    counter = collections.Counter(list2)
    for location_id in list1:
        result += location_id * counter.get(location_id, 0)

    return result


def reader(fh):
    list1, list2 = [], []
    for l in fh:
        item1, item2 = re.split(r'\s+', l.rstrip())
        list1.append(int(item1, 10)), list2.append(int(item2, 10))

    return list1, list2
        

if __name__ == '__main__':
    fname = sys.argv[1]
    with open(fname, 'r') as fh:
        list1, list2 = reader(fh)
        start = time.monotonic_ns()
        result = main(list1, list2)
        end = time.monotonic_ns()

    print(result)
    print(f'Result calculated in {(end - start) / 1e3:0.3f} microseconds.', file=sys.stderr)