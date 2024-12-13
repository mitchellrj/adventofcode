import re
import sys
import time


def main(list1, list2):
    sorted_matched_items = zip(sorted(list1), sorted(list2))
    result = 0
    for item1, item2 in sorted_matched_items:
        result += abs(item1 - item2)

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