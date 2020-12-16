import re
import sys
import time


RULE_PATTERN = re.compile(r'(?:^([\w\s]+):|(\d+)-(\d+))')


def make_ticket_validator(all_bounds):
        
    def ticket_is_valid(ticket):
        for value in ticket:
            for b in all_bounds:
                if value in b:
                    break
            else:
                return False

        return True

    return ticket_is_valid


def solve(field_name, field_index, possible_fields_names):
        for other_field_index, other_field_names in enumerate(possible_fields_names):
            if other_field_index == field_index:
                continue
            elif field_name in other_field_names:
                other_field_names.remove(field_name)
                if len(other_field_names) == 1:
                    # TIL getting a single item out of a set is yucky in python unless you're willing to pop it.
                    (other_field_name, ) = other_field_names
                    solve(other_field_name, other_field_index, possible_fields_names)


def main(rules, my_ticket, nearby_tickets):
    all_bounds = {bound for rule in rules.values() for bound in rule}

    # Inefficient - should really combine with the main step
    valid_nearby_tickets = filter(make_ticket_validator(all_bounds), nearby_tickets)

    possible_fields_names = []
    for _ in range(len(nearby_tickets[0])):
        possible_fields_names.append(set(rules.keys()))
    
    # may need to make multiple passes. fun.
    while sum(map(len, possible_fields_names)) != len(possible_fields_names):
        for ticket in valid_nearby_tickets:
            for field_index, value in enumerate(ticket):
                if len(possible_fields_names[field_index]) == 1:
                    # already solved this field
                    continue
                # take a copy and pop items out of it, so we're not mutating
                # the real possible field until we're ready and no-longer
                # iterating over it.
                try_fields = set(possible_fields_names[field_index])
                while try_fields:
                    field_name = try_fields.pop()
                    for bounds in rules[field_name]:
                        if value in bounds:
                            # this rule is valid
                            break
                    else:
                        # this rule is not valid
                        possible_fields_names[field_index].remove(field_name)

                        # if that was the last rule then we've identified a field name
                        if len(possible_fields_names[field_index]) == 1:
                            (solved_field, ) = possible_fields_names[field_index]
                            solve(solved_field, field_index, possible_fields_names)

    result = 1
    for field_index, p in enumerate(possible_fields_names):
        field_name = p.pop()
        if field_name.startswith('departure'):
            result *= my_ticket[field_index]

    return result


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