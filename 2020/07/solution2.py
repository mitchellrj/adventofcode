import re
import sys
import time


BAG_DESCRIPTOR_PATTERN = re.compile(r'(?:(\d+) )?(\w+ \w+) bags?')
SOURCE_BAG = 'shiny gold'


def walker(bags, current, seen):
    branch_count = 0
    for held, count in bags[current].items():
        if held not in seen:
            seen[held] = walker(bags, held, seen) + 1

        branch_count += (seen[held] * count)
            
    return branch_count


def main(bags):
    return walker(bags, SOURCE_BAG, {})


def reader(fh):
    bags = {}
    for l in fh:
        matches = BAG_DESCRIPTOR_PATTERN.findall(l)
        bags[matches[0][1]] = {
            m[1]: int(m[0])
            for m in matches[1:]
            if m[1] != 'no other'
        }
    return bags


if __name__ == '__main__':
    fname = sys.argv[1]
    with open(fname, 'r') as fh:
        inputs = reader(fh)

    start = time.monotonic_ns()
    result = main(inputs)
    end = time.monotonic_ns()

    print(result)
    print(f'Result calculated in {(end - start) / 1e3:0.3f} microseconds.', file=sys.stderr)