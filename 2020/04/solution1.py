import re
import sys
import time


REQUIRED_FIELDS = frozenset([
    'byr',
    'iyr',
    'eyr',
    'hgt',
    'hcl',
    'ecl',
    'pid',
    # 'cid',
])
MATCHER = re.compile(r'([^:\s]+):([^\s]+)')


def main(passport_data):
    v = 0
    for p in passport_data:
        v += REQUIRED_FIELDS >= set(p.keys())
    return v


def reader(fh):
    p = {}
    for l in fh:
        if not l.strip():
            yield p
            p = {}
            continue
        
        p.update(MATCHER.findall(l))
    
    yield p


if __name__ == '__main__':
    fname = sys.argv[1]
    with open(fname, 'r') as fh:
        inputs = list(reader(fh))

    start = time.monotonic_ns()
    result = main(inputs)
    end = time.monotonic_ns()

    print(result)
    print(f'Result calculated in {(end - start) / 1e3:0.3f} microseconds.', file=sys.stderr)