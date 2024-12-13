import re
import sys
import time
import typing


def main(reports):
    result = 0
    for report in reports:
        report_is_safe = test_report(report)
        if not report_is_safe:
            # naïve approach: just keep trying, removing one level at a time
            for i in range(0, len(report)):
                dampened_report = report[0:i] + report[i + 1:]
                report_is_safe = test_report(dampened_report)
                if report_is_safe:
                    break
        result += report_is_safe

    return result


def test_report(report):
    last_diff = None
    for i in range(1, len(report)):
        diff = report[i] - report[i-1]
        if abs(diff) > 3 or abs(diff) < 1:
            return False
        elif last_diff is None:
            last_diff = diff
            continue
        elif diff < 0 and last_diff > 0:
            return False
        elif diff > 0 and last_diff < 0:
            return False
        last_diff = diff
    return True


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