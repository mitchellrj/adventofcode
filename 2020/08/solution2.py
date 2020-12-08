import sys
import time


SWAPPABLE = {'jmp': 'nop', 'nop': 'jmp'}


def main(code):
    acc = 0
    l = 0
    executed = set()
    while True:
        try:
            acc, l = run_partial(code, l, SWAPPABLE.keys(), executed, acc)
        except (RuntimeError, OverflowError):
            operator, operand = code[l]
            acc, l = exec_statement(operator, operand, acc, l)
            executed.add(l)
            continue
        try:
            acc = run_with_mutation(code, l, executed, acc)
        except (RuntimeError, OverflowError):
            operator, operand = code[l]
            acc, l = exec_statement(operator, operand, acc, l)
            executed.add(l)
            continue

        return acc


def run_with_mutation(code, l, executed, acc):
    operator, operand = code[l]
    swoperator = SWAPPABLE[operator]
    if operand == 0 and swoperator == 'jmp':
        # this would be an infinite loop by default: unswap it.
        raise RuntimeError('Infinite loop detected!')
    executed.add(l)
    acc, l = exec_statement(swoperator, operand, acc, l)
    acc, l = run_partial(code, l, (), executed, acc)
    return acc


def exec_statement(operator, operand, acc, l):
    if operator == 'acc':
        acc += operand
        l += 1
    elif operator == 'jmp':
        l += operand
    else:
        l += 1
    return acc, l


def run_partial(code, l, until, executed, acc):
    while l != len(code):
        if l > len(code):
            raise OverflowError()
        operator, operand = code[l]
        if operator in until:
            break
        if l in executed:
            raise RuntimeError("Infinite loop detected!")
        executed.add(l)
        acc, l = exec_statement(operator, operand, acc, l)

    return acc, l

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