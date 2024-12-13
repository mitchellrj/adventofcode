import sys
import time


def main(reports):
    result = 0
    for report in reports:
        report_is_safe = False
        last_diff = None
        for i in range(1, len(report)):
            diff = report[i] - report[i-1]
            if abs(diff) > 3 or abs(diff) < 1:
                break
            elif last_diff is None:
                last_diff = diff
                continue
            elif diff < 0 and last_diff > 0:
                break
            elif diff > 0 and last_diff < 0:
                break
            last_diff = diff
        else:
            report_is_safe = True

        result += report_is_safe

    return result


def reader(fh):
    for report in fh:
        yield tuple(map(int, report.split()))
        

if __name__ == '__main__':
    fname = sys.argv[1]
    with open(fname, 'r') as fh:
        reports = reader(fh)
        start = time.monotonic_ns()
        result = main(reports)
        end = time.monotonic_ns()

    print(result)
    print(f'Result calculated in {(end - start) / 1e3:0.3f} microseconds.', file=sys.stderr)