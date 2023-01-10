from __future__ import annotations

import argparse
import os.path

import pytest
import numpy as np
import support

from typing import List

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

BOLD = '\033[1m'
ENDC = '\033[0m'

def visible_left(grid: List[str]) -> List[(int,int)]:
    visible_list = []

    for i, row in enumerate(grid):
        tallest = (i,0,int(row[0]))
        for j, tree in enumerate(row):
            height = int(tree)
            if height > tallest[2]:
                tallest = (i,j, height)
                visible_list.append(tallest)
        visible_list.append(tallest)

    return visible_list


def visible_right(grid: List[str]) -> List[(int,int)]:
    visible_list = []

    for i, row in enumerate(grid):
        tallest = (i,len(row)-1,int(row[-1]))
        # print(f'tallest is {(tallest[0],tallest[1])}={grid[tallest[0]][tallest[1]]}')
        for j, tree in zip(range(len(row)-1,-1,-1),reversed(row)):
            # print(f'\t{(i,j)}={int(tree)}')
            height = int(tree)
            if height > tallest[2]:
                tallest = (i,j, height)
                visible_list.append(tallest)
        visible_list.append(tallest)

    return visible_list





def compute(s: str) -> int:

    lines = s.splitlines()

    left = visible_left(lines)
    right = visible_right(lines)


    # convert to np array
    numpy_array = []
    for line in lines:
        row = []
        for char in line:
            row.append(int(char))
        numpy_array.append(row)

    numpy_array = np.array(numpy_array)
    col_view = numpy_array.T

    visible_from_top = visible_left(col_view)
    visible_from_bottom = visible_right(col_view)


    visible = set()

    for row in range(len(lines)):
        x = row
        y_left = 0
        y_right = len(lines[0]) - 1

        visible.add((x,y_left))
        visible.add((row, y_right ))

    for col in range(len(lines[0])):
        y = col
        x_top = 0
        x_bottom = len(lines) - 1
        visible.add((x_top,col))
        visible.add((x_bottom,col))

    for x,y,height in left:
        visible.add((x,y))

    for x,y,height in right:
        visible.add((x,y))

    for y,x,height in visible_from_top:
        visible.add((x,y))

    for y,x,height in visible_from_bottom:
        visible.add((x,y))

    # debug print chosen trees
    # for i, row in enumerate(numpy_array):
    #     line = ''
    #     for j, col in enumerate(row):
    #         if (i,j) in visible:
    #             line += BOLD + str(numpy_array[i][j]) + ENDC
    #         else:
    #             line += str(numpy_array[i][j])
    #     print(line)

    return len(visible)


INPUT_S = '''\
30373
25512
65332
33549
35390
'''
EXPECTED = 21


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
