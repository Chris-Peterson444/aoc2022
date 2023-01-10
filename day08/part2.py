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


def view_right(row: int, col: int, grid: List[int]) -> int:
    height = grid[row][col]
    score = 0
    for j in range(col+1,len(grid[0])):
        score += 1

        if grid[row][j] >= height:
            return score

    return score

def view_left(row: int, col: int, grid: List[int]) -> int:
    height = grid[row][col]
    score = 0
    for j in range(col-1,-1,-1):
        score += 1
        if grid[row][j] >= height:
            return score


    return score

def view_down(row: int, col: int, grid: List[int]) -> int:
    height = grid[row][col]
    score = 0
    for i in range(row+1,len(grid)):
        score += 1
        if grid[i][col] >= height:
            return score

    return score

def view_up(row: int, col: int, grid: List[int]) -> int:
    height = grid[row][col]
    score = 0
    for i in range(row-1,-1,-1):
        score += 1
        if grid[i][col] >= height:
            return score

    return score



def scenic_score(left: int, right: int, up: int, down: int) -> int:
    return left * right * up * down



def compute(s: str) -> int:

    lines = s.splitlines()

    # convert to np array
    numpy_array = []
    for line in lines:
        row = []
        for char in line:
            row.append(int(char))
        numpy_array.append(row)

    numpy_array = np.array(numpy_array)
    col_view = numpy_array.T

    best = (-1,-1,-1)

    for i, row in enumerate(numpy_array):
        for j, col in enumerate(row):
            up = view_up(i,j, lines)
            down = view_down(i,j,lines)
            left = view_left(i,j,lines)
            right = view_right(i,j,lines)
            score = scenic_score(left, right, up, down)
            # print(f'{(i,j)} score={score}, left={left}, up={up}, down={down}, right={right}')
            if score > best[2]:
                best = (i,j,score)



    return best[2]


INPUT_S = '''\
30373
25512
65332
33549
35390
'''
EXPECTED = 8


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
