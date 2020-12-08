import sys
import time


def main(code):
    run = set()
    acc = 0
    l = 0
    while l not in run:
        run.add(l)
        operator, operand = code[l]
        if operator == 'acc':
            acc += operand
            l += 1
        elif operator == 'jmp':
            l += operand
        else:
            l += 1
    
    return acc


def reader(fh):
    for l in fh:
        operator, operand = l.strip().split(' ')
        yield operator, int(operand)


if __name__ == '__main__':
    fname = sys.argv[1]
    with open(fname, 'r') as fh:
        inputs = list(reader(fh))

    start = time.monotonic_ns()
    result = main(inputs)
    end = time.monotonic_ns()

    print(result)
    print(f'Result calculated in {(end - start) / 1e3:0.3f} microseconds.', file=sys.stderr)