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

        # first inside of second
        if int(interval_1[0]) >= int(interval_2[0]) and int(interval_1[1]) <= int(interval_2[1]):
            # print(f'{interval_1}\t{interval_2} - one in two')
            contained += 1
        # # second inside of first
        elif int(interval_2[0]) >= int(interval_1[0]) and int(interval_2[1]) <= int(interval_1[1]):
            # print(f'{interval_1}\t{interval_2} - two in one')
            contained += 1
        else:
            pass




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
EXPECTED = 2


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
