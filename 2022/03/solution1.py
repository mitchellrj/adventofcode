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
    total_priority = 0
    for compartment_one_contents, compartment_two_contents in rucksacks:
        # Take the intersection of each set of contents
        items_in_both_compartments = compartment_one_contents & compartment_two_contents
        # Add up the priorities
        total_priority += sum(map(get_priority, items_in_both_compartments))

    return total_priority


def reader(fh):
    for rucksack in fh:
        # special // operator (new to Python 3, default in Python 2) - forces integers to be returned by
        # division operations
        compartment_size = len(rucksack) // 2
        # Convert the string of each compartment into frozen sets of the characters that make up those
        # strings (we don't expect to change them, so why make them mutable?)
        yield frozenset(rucksack[:compartment_size]), frozenset(rucksack[compartment_size:])


if __name__ == '__main__':
    fname = sys.argv[1]
    with open(fname, 'r') as fh:
        inputs = reader(fh)
        start = time.monotonic_ns()
        result = main(inputs)
        end = time.monotonic_ns()

    print(result)
    print(f'Result calculated in {(end - start) / 1e3:0.3f} microseconds.', file=sys.stderr)