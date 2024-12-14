import sys
import time


def main(ordering_rules, proposed_updates):
    # We can't solve the total ordering, as there are rules that contradict each other or are cyclical in the main set.
    # e.g. 11|15, 12|15, 12|11, 15|18, 18|12

    less_than = {}
    greater_than = {}
    for rule in ordering_rules:
        less_than.setdefault(rule[0], set()).add(rule[1])

    valid_update_middle_page_sum = 0
    for update in proposed_updates:
        for i in range(len(update) - 1, 0, -1):
            for j in range(i - 1, -1, -1):    
                if update[j] in less_than.get(update[i], set()):
                    # Breaks a rule, this page number is in a greater position it should be less than.
                    print(f'{update} breaks rule {update[j]}|{update[i]}')
                    break
            else:
                # No rules broken, keep checking
                continue
            # if we did break a rule, break again
            break
        else:
            valid_update_middle_page_sum += update[len(update)//2]

    return valid_update_middle_page_sum


def reader(fh):
    ordering_rules = set()
    for line in fh:
        if len(line) < 2:
            break

        ordering_rules.add(tuple(map(int, line.split('|'))))

    proposed_updates = []
    for line in fh:
        proposed_updates.append(list(map(int, line.split(','))))
    return ordering_rules, proposed_updates
        

if __name__ == '__main__':
    fname = sys.argv[1]
    with open(fname, 'r') as fh:
        ordering_rules, proposed_updates = reader(fh)
        start = time.monotonic_ns()
        result = main(ordering_rules, proposed_updates)
        end = time.monotonic_ns()

    print(result)
    print(f'Result calculated in {(end - start) / 1e3:0.3f} microseconds.', file=sys.stderr)