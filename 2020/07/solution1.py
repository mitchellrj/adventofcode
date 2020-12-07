import re
import sys
import time


BAG_DESCRIPTOR_PATTERN = re.compile(r'(?:(\d+) )?(\w+ \w+) bags?')
TARGET_BAG = 'shiny gold'


def walker(bags_of_holding, current, seen):
    branch_count = 0
    for holder in bags_of_holding[current]:
        if holder in seen:
            continue
        if holder not in bags_of_holding:
            seen[holder] = 1
        else:
            seen[holder] = walker(bags_of_holding, holder, seen) + 1

        branch_count += seen[holder]
            
    return branch_count


def main(bags_of_holding):
    return walker(bags_of_holding, TARGET_BAG, {})


def reader(fh):
    bags_of_holding = {}
    for l in fh:
        matches = BAG_DESCRIPTOR_PATTERN.findall(l)
        holder = matches[0][1]
        for _, held in matches[1:]:
            if held == 'no other':
                held = None
            bags_of_holding.setdefault(held, set()).add(holder)

    return bags_of_holding


if __name__ == '__main__':
    fname = sys.argv[1]
    with open(fname, 'r') as fh:
        inputs = reader(fh)

    start = time.monotonic_ns()
    result = main(inputs)
    end = time.monotonic_ns()

    print(result)
    print(f'Result calculated in {(end - start) / 1e3:0.3f} microseconds.', file=sys.stderr)