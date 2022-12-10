import sys
import time


def main(stacks, moves):
    # naïve solution to begin with...
    for count, source, target in moves:
        # Take from the top of the source stack the total count, and reverse the order, then add it
        # onto the top of the target stack.
        crates_to_take = stacks[source][-count:]
        del stacks[source][-count:]
        # place them on the target stack in BUT NOT IN reverse order
        stacks[target].extend(crates_to_take)

    return ''.join(map(list.pop, stacks))


def reader(fh):
    initial_stacks = []
    for l in fh:
        l = l.strip('\n')
        if '[' not in l:
            # eat the stack numbers row
            next(fh)
            # start processing moves
            yield initial_stacks
            break
        
        # start at character 1, end at the end, and take every 4th character
        row_crates = tuple(l[1::4])
        for col, crate in enumerate(row_crates):

            if col > (len(initial_stacks) - 1):
                # if we don't have a stack for this column yet, add one in
                initial_stacks.append([])
                
            if crate == ' ':
                continue

            initial_stacks[col].insert(0, crate)

    for l in fh:
        l = l.strip()
        _move, count, _from, source, _to, target = l.split()
        # convert to ints and zero-index the source and target numbers
        yield (int(count), int(source) - 1, int(target) - 1)
        

if __name__ == '__main__':
    fname = sys.argv[1]
    with open(fname, 'r') as fh:
        inputs = reader(fh)
        initial_stacks = next(inputs)
        start = time.monotonic_ns()
        result = main(initial_stacks, inputs)
        end = time.monotonic_ns()

    print(result)
    print(f'Result calculated in {(end - start) / 1e3:0.3f} microseconds.', file=sys.stderr)