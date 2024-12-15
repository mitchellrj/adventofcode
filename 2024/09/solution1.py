import sys
import time


def main(blocks):
    # fragmenting time
    #print(''.join(['.' if b is None else str(b) for b in blocks]))
    j = len(blocks) - 1
    for i in range(len(blocks)):
        if blocks[i] is None:
            while blocks[j] is None:
                j -= 1
            if j <= i:
                break
            # swapperoo
            blocks[i], blocks[j] = blocks[j], blocks[i]
        #print(''.join(['.' if b is None else str(b) for b in blocks]))
    
    # checksum time
    return sum(map(lambda x: x[0] * x[1], enumerate(blocks[:i])))
    

def reader(fh):
    l = fh.readline()
    blocks = []
    for i, c in enumerate(l):
        blocks += int(c) * ([None] if i%2 else [i//2])

    return blocks
        

if __name__ == '__main__':
    fname = sys.argv[1]
    with open(fname, 'r') as fh:
        blocks = reader(fh)
        start = time.monotonic_ns()
        result = main(blocks)
        end = time.monotonic_ns()

    print(result)
    print(f'Result calculated in {(end - start) / 1e3:0.3f} microseconds.', file=sys.stderr)