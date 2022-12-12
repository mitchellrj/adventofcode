import io
import sys
import time


def main(datastream):
    pos = 0
    # What's more efficient? The naive solution or using some sort of ordered set type thing?
    # For a larger sequence than 4, probably the latter, but I reckon naive will beat the hash
    # calculation and lookup. We can probably do something a bit clever with file reads though.
    chars_to_read = 4
    buf = ""
    while True:
        new_chars = datastream.read(chars_to_read)
        if new_chars is None:
            # EOF.
            raise RuntimeError("Did not find the start-of-packet marker")
        chars_read = len(new_chars)

        # truncate and append
        buf = buf[chars_read:] + new_chars
        pos += chars_read
        chars_to_read = -1
        for i in range(1, chars_read + 1):
            # iterate over the new characters only, from last to first, looking for duplicates
            # in the characters that preceed it in our buffer. Use `rfind`, not `find`, to make
            # sure we get the position of the latest occurrence
            idx = buf[:-i].rfind(buf[-i])
            if idx != -1:
                # it's not enough to break after the first match, there might be another match
                # with a later position, which would then get ignored
                chars_to_read = max(chars_to_read, idx + 1)

        if chars_to_read > 0:
            # there was a match: keep reading
            continue
        else:
            return pos


def reader(fh):
    # We'll be reading the stream at most 4 characters at a time, but it's really inefficient to
    # read a file that way. Fortunately, Python's default behaviour is to actually do buffering
    # for us. https://docs.python.org/3/library/functions.html#open
    return fh
        

if __name__ == '__main__':
    fname = sys.argv[1]
    with open(fname, 'r') as fh:
        inputs = reader(fh)
        start = time.monotonic_ns()
        result = main(inputs)
        end = time.monotonic_ns()

    print(result)
    print(f'Result calculated in {(end - start) / 1e3:0.3f} microseconds.', file=sys.stderr)