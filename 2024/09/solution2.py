import sys
import time


# This solution could probably be made more efficient by just using a file allocation table and not mapping out
# all the actual blocks.


def main(blocks, fat):
    # fragmenting time
    if len(blocks) <= 1000:
        print(''.join(['.' if b is None else str(b) for b in blocks]))

    last_file_no = None
    i = -1
    while last_file_no is None:
        last_file_no = blocks[i]
        i -= 1
    # map out the unallocated space too
    unallocated = []
    fno = 0
    while fno < last_file_no:
        start = fat[fno][0] + fat[fno][1]
        end = fat[fno + 1][0]
        unallocated.append((start, end - start))
        fno += 1

    file_id = last_file_no
    while file_id > 0:
        file_size = fat[file_id][1]
        for unallocated_block_no in range(len(unallocated)):
            free_block = unallocated[unallocated_block_no]
            if free_block[0] > fat[file_id][0]:
                # don't move a file backwards ever
                break
            if free_block[1] >= file_size:
                # move the file
                for b in range(file_size):
                    # swap the blocks
                    blocks[free_block[0] + b], blocks[fat[file_id][0] + b] = blocks[fat[file_id][0] + b], blocks[free_block[0] + b]
                # update our tables
                fat[file_id] = (free_block[0], file_size)
                unallocated[unallocated_block_no] = (free_block[0] + file_size, free_block[1] - file_size)
                if len(blocks) <= 1000:
                    print(''.join(['.' if b is None else str(b) for b in blocks]))
                break
        file_id -= 1
    
    # checksum time
    return sum(map(lambda x: (0 if None in x else x[0] * x[1]), enumerate(blocks)))
    

def reader(fh):
    l = fh.readline()
    blocks = []
    # This time we'll build a file allocation table of sorts while we read
    fat = {}
    for i, c in enumerate(l):
        if not i%2:
            fat[i//2] = len(blocks), int(c)

        blocks += int(c) * ([None] if i%2 else [i//2])

    return blocks, fat
        

if __name__ == '__main__':
    fname = sys.argv[1]
    with open(fname, 'r') as fh:
        blocks, fat = reader(fh)
        start = time.monotonic_ns()
        result = main(blocks, fat)
        end = time.monotonic_ns()

    print(result)
    print(f'Result calculated in {(end - start) / 1e3:0.3f} microseconds.', file=sys.stderr)