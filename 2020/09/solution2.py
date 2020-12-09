import itertools
import sys
import time


def main(ciphertext, preamble_length):
    iv = []
    for i in range(preamble_length):
        iv.extend([
            ciphertext[i] + ciphertext[j]
            for j in itertools.chain(range(0, i), range(i + 1, preamble_length))
        ])
    block = ciphertext[:preamble_length]
    alphabet = iv
    for i in range(preamble_length, len(ciphertext)):
        c = ciphertext[i]
        if c not in alphabet:
            break
        block.pop(0)
        block.append(c)
        alphabet = alphabet[preamble_length:]
        alphabet.extend([
            c + b for b in block
        ])
    else:
        return
    
    t = 0
    block = []
    for j in range(i - 1, 0, -1):
        t += ciphertext[j]
        block.insert(0, ciphertext[j])
        if t == c:
            return min(block) + max(block)
        elif t > c:
            t -= block.pop()


def reader(fh):
    for l in fh:
        yield int(l)


if __name__ == '__main__':
    fname = sys.argv[1]
    preamble_length = int(sys.argv[2])
    with open(fname, 'r') as fh:
        inputs = list(reader(fh))

    start = time.monotonic_ns()
    result = main(inputs, preamble_length)
    end = time.monotonic_ns()

    print(result)
    print(f'Result calculated in {(end - start) / 1e3:0.3f} microseconds.', file=sys.stderr)