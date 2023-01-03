from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:

    lines = s.splitlines()

    contained = 0

    for line in lines:
        interval_1, interval_2 = line.split(',')
        interval_1 = interval_1.split('-')
        interval_2 = interval_2.split('-')

        if int(interval_1[0]) < int(interval_2[0]):
            smaller = interval_1
            bigger = interval_2
        else:
            smaller = interval_2
            bigger = interval_1

        smaller_interval_right = int(smaller[1])
        bigger_interval_left = int(bigger[0])

        if smaller_interval_right >= bigger_interval_left:
            # print(f'{interval_1}\t{interval_2} - overlap')
            contained += 1




    return contained


INPUT_S = '''\
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
1-4,2-6
1-4,4-12
'''
EXPECTED = 6


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
