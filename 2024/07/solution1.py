import operator
import sys
import time


OPERATORS = (operator.add, operator.mul)


def main(equations):
    result = 0
    for target, operands in equations:
        if find_solution(operands[0], operands[1:], target):
            result += target

    return result
        

def find_solution(interim_result, operands, target):
    if not operands:
        return interim_result == target
    if interim_result > target:
        return False
    for operator in OPERATORS:
        trial_result = operator(interim_result, operands[0])
        if find_solution(trial_result, operands[1:], target):
            return True


def reader(fh):
    for l in fh:
        target, operands = l.split(':')

        yield int(target), list(map(int, operands.strip().split()))
        

if __name__ == '__main__':
    fname = sys.argv[1]
    with open(fname, 'r') as fh:
        equations = reader(fh)
        start = time.monotonic_ns()
        result = main(equations)
        end = time.monotonic_ns()

    print(result)
    print(f'Result calculated in {(end - start) / 1e3:0.3f} microseconds.', file=sys.stderr)