import itertools
import sys
import time


def main(ciphertext, block_size):
    iv = []
    for i in range(block_size):
        iv.extend([
            ciphertext[i] + ciphertext[j]
            for j in itertools.chain(range(0, i), range(i + 1, block_size))
        ])
    block = ciphertext[:block_size]
    alphabet = iv
    for i in range(block_size, len(ciphertext)):
        c = ciphertext[i]
        if c not in alphabet:
            break
        block.pop(0)
        block.append(c)
        alphabet = alphabet[block_size:]
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
    block_size = int(sys.argv[2])
    with open(fname, 'r') as fh:
        inputs = list(reader(fh))

    start = time.monotonic_ns()
    result = main(inputs, block_size)
    end = time.monotonic_ns()

    print(result)
    print(f'Result calculated in {(end - start) / 1e3:0.3f} microseconds.', file=sys.stderr)