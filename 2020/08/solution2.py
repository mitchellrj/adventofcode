import sys
import time


SWAPPABLE = {'jmp': 'nop', 'nop': 'jmp'}


def main(code):
    acc = 0
    l = 0
    execution_order = []
    while True:
        try:
            acc, l, steps = run_partial(code, l, SWAPPABLE.keys(), set(execution_order), acc)
            execution_order.extend(steps)
        except (RuntimeError, OverflowError):
            operator, operand = code[l]
            acc, l = exec_statement(operator, operand, acc, l)
            execution_order.append(l)
            continue
        try:
            acc = run_with_mutation(code, l, execution_order, acc)
        except (RuntimeError, OverflowError):
            operator, operand = code[l]
            acc, l = exec_statement(operator, operand, acc, l)
            execution_order.append(l)
            continue

        return acc


def run_with_mutation(code, l, execution_order, acc):
    operator, operand = code[l]
    swoperator = SWAPPABLE[operator]
    if operand == 0 and swoperator == 'jmp':
        # this would be an infinite loop by default: unswap it.
        raise RuntimeError('Infinite loop detected!')
    execution_order.append(l)
    acc, l = exec_statement(swoperator, operand, acc, l)
    acc, l, steps = run_partial(code, l, (), set(execution_order), acc)
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
    steps = []
    while l != len(code):
        if l > len(code):
            raise OverflowError()
        operator, operand = code[l]
        if operator in until:
            break
        if l in executed:
            raise RuntimeError("Infinite loop detected!")
        steps.append(l)
        executed.add(l)
        acc, l = exec_statement(operator, operand, acc, l)

    return acc, l, steps

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