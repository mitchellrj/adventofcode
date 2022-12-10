import sys
import time


def main(sections):
    overlaps = 0
    for first_elf_sections, second_elf_sections in sections:
        # see, ranges did finally help a little!
        if first_elf_sections.start in second_elf_sections:
            # overlap between the start of the first elf's sections and the second elf's sections
            overlaps += 1
        elif (first_elf_sections.stop - 1) in second_elf_sections:
            # overlap between the end of the first elf's sections and the second elf's sections
            overlaps += 1
        elif second_elf_sections.start in first_elf_sections:
            # overlap between the start of the second elf's sections and the first elf's sections
            overlaps += 1
        elif (second_elf_sections.stop - 1) in first_elf_sections:
            # overlap between the end of the second elf's sections and the first elf's sections
            overlaps += 1

    return overlaps


def reader(fh):
    for pair_sections in fh:
        pair_section_ranges = pair_sections.strip().split(',')
        pair_section_range_start_and_end = [tuple(map(int, section_range.split('-'))) for section_range in pair_section_ranges]

        yield (
            range(pair_section_range_start_and_end[0][0], pair_section_range_start_and_end[0][1] + 1),
            range(pair_section_range_start_and_end[1][0], pair_section_range_start_and_end[1][1] + 1),
        )


if __name__ == '__main__':
    fname = sys.argv[1]
    with open(fname, 'r') as fh:
        inputs = reader(fh)
        start = time.monotonic_ns()
        result = main(inputs)
        end = time.monotonic_ns()

    print(result)
    print(f'Result calculated in {(end - start) / 1e3:0.3f} microseconds.', file=sys.stderr)