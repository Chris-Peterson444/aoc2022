from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    cubes : set[Tuple[int,int,int]] = set()

    lines = s.splitlines()
    for line in lines:
        x,y,z = line.split(',')
        cubes.add((int(x),int(y),int(z)))
    max_sa = 6 * len(cubes)
    while cubes:
        cube_1 = cubes.pop()
        for cube_2 in cubes:
            x,y,z = cube_1
            j,k,l = cube_2

            # x touch
            if y == k and z == l and abs(x-j) == 1:
                max_sa -= 2
            # y touch
            elif x == j and z == l and abs(y-k) == 1:
                max_sa -= 2
            # z touch
            elif x == j and y == k and abs(z-l) == 1:
                max_sa -=  2


    return max_sa


INPUT_S = '''\
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
'''
EXPECTED = 64


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
