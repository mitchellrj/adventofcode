import sys
import time


def get_priority(c):
    # Get the underlying ASCII codepoint of each character, and use that to get a numeric value
    ordinal_value = ord(c)
    if ordinal_value > 96:
        # a-z (97-122)
        return ordinal_value - 96
    # A-Z (65-90)
    return ordinal_value - 38


def main(rucksacks):
    group = 1
    total_priority = 0
    while True:
        try:
            # The built-in next function takes an item from an iterator
            group_rucksacks = [next(rucksacks), next(rucksacks), next(rucksacks)]
        except StopIteration:
            break

        # There might be a more functional-style way to do this with `operator.and_`, but I don't
        # care for it. Must also explicitly convert back from `frozenset` to `set`.
        badge_candidates = set(group_rucksacks[0] & group_rucksacks[1] & group_rucksacks[2])

        # Throw an error if I've made a false assumption
        assert len(badge_candidates) == 1, (
            "Unexpected number of badge candidates for group {:d}: {:d} ({})".format(
                group, len(badge_candidates), badge_candidates)
            )
        
        # Can't index a set, must use `set.pop` or first convert to a `Sequence` type.
        total_priority += get_priority(badge_candidates.pop())

        group += 1

    return total_priority


def reader(fh):
    for rucksack in fh:
        # we don't care about compartments any more
        yield frozenset(rucksack.strip())


if __name__ == '__main__':
    fname = sys.argv[1]
    with open(fname, 'r') as fh:
        inputs = reader(fh)
        start = time.monotonic_ns()
        result = main(inputs)
        end = time.monotonic_ns()

    print(result)
    print(f'Result calculated in {(end - start) / 1e3:0.3f} microseconds.', file=sys.stderr)