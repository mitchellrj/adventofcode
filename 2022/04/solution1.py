import sys
import time


def main(sections):
    fully_contained = 0
    for first_elf_sections, second_elf_sections in sections:
        if first_elf_sections.start >= second_elf_sections.start and first_elf_sections.stop <= second_elf_sections.stop:
            # first elf's sections are inside the second elf's sections
            fully_contained += 1
        elif first_elf_sections.start <= second_elf_sections.start and first_elf_sections.stop >= second_elf_sections.stop:
            # second elf's sections are inside the first elf's sections
            fully_contained += 1

    return fully_contained


def reader(fh):
    for pair_sections in fh:
        pair_section_ranges = pair_sections.strip().split(',')
        pair_section_range_start_and_end = [tuple(map(int, section_range.split('-'))) for section_range in pair_section_ranges]

        # I started with ranges here thinking they'd help me. They didn't, but I'm committing to them.
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