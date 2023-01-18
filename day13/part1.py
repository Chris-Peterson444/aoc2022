
from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

import re
from itertools import zip_longest

def correctOrder(left, right) -> bool:

    for l,r in zip_longest(left, right, fillvalue=None):
        ret = None
        if isinstance(l,int) and isinstance(r,int):
            if l < r:
                return True
            elif l > r:
                return False

        elif isinstance(l,list) and isinstance(r, list):
            ret = correctOrder(l,r)
        elif isinstance(l, list) and isinstance(r, int):
            ret = correctOrder(l,[r])
        elif isinstance(l, int) and isinstance(r, list):
            ret = correctOrder([l],r)

        elif l is None:
            return True
        elif r is None:
            return False

        if ret is not None:
            return ret


def stringToList(string: str) -> list:

    return eval(string)



def compute(s: str) -> int:

    groups = s.split('\n\n')
    correct_idx = []

    for i, group in enumerate(groups):
        group = group.strip('\n')
        left, right = group.split('\n')
        left = stringToList(left)
        right = stringToList(right)

        if correctOrder(left, right):
            correct_idx.append(i+1)
        # print(f'pair {i+1} is {correctOrder(left, right)}')

    return sum(correct_idx)


INPUT_S = '''\
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
'''
EXPECTED = 13


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
