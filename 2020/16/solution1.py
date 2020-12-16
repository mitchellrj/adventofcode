import re
import sys
import time


RULE_PATTERN = re.compile(r'(?:(\w+):|(\d+)-(\d+))')



def main(rules, ticket, nearby_tickets):
    all_bounds = {bound for rule in rules.values() for bound in rule}
    invalid = []
    for t in nearby_tickets:
        for f in t:
            if not any(map(lambda b: f in b, all_bounds)):
                invalid.append(f)
                continue

    return sum(invalid)


def reader(fh):
    rules = {}
    for l in fh:
        if l == '\n':
            # Next section
            break
        rule_bounds = []
        field = None
        for f, lower_bound, upper_bound in RULE_PATTERN.findall(l):
            if f:
                field = f
            else:
                rule_bounds.append(range(int(lower_bound), int(upper_bound) + 1))
        rules[field] = rule_bounds

    assert fh.readline() == 'your ticket:\n'
    ticket = tuple(map(int, fh.readline().split(',')))

    assert fh.readline() == '\n'
    assert fh.readline() == 'nearby tickets:\n'
    
    nearby_tickets = []
    for l in fh:
        nearby_tickets.append(tuple(map(int, l.split(','))))
    
    return rules, ticket, nearby_tickets


if __name__ == '__main__':
    fname = sys.argv[1]
    with open(fname, 'r') as fh:
        rules, ticket, nearby_tickets = reader(fh)

    start = time.monotonic_ns()
    result = main(rules, ticket, nearby_tickets)
    end = time.monotonic_ns()

    print(result)
    print(f'Result calculated in {(end - start) / 1e3:0.3f} microseconds.', file=sys.stderr)