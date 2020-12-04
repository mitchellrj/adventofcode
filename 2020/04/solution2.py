import re
import sys
import time


VALID_HEIGHT_CM = (150, 193)
VALID_HEIGHT_IN = (59, 76)
VALID_HAIR_COLOR = re.compile(r'^#[a-fA-F0-9]{6}$')
VALID_EYE_COLORS = frozenset(['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'])
REQUIRED_FIELDS = {
    'byr': lambda y: 1920 <= int(y) <= 2002,
    'iyr': lambda y: 2010 <= int(y) <= 2020,
    'eyr': lambda y: 2020 <= int(y) <= 2030,
    'hgt': lambda h: (VALID_HEIGHT_CM[0] <= int(h[:-2]) <= VALID_HEIGHT_CM[1]) if h.endswith('cm') else (VALID_HEIGHT_IN[0] <= int(h[:-2]) <= VALID_HEIGHT_IN[1]),
    'hcl': lambda c: bool(VALID_HAIR_COLOR.match(c)),
    'ecl': lambda c: c in VALID_EYE_COLORS,
    'pid': lambda n: len(n) == 9 and n.isdigit(),
    # 'cid',
}
MATCHER = re.compile(r'([^:\s]+):([^\s]+)')


def main(passport_data):
    v = 0
    for p in passport_data:
        for k in REQUIRED_FIELDS:
            if k not in p:
                break
            if not REQUIRED_FIELDS[k](p[k]):
                break
        else:
            v += 1

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