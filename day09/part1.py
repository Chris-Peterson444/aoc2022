from __future__ import annotations

import argparse
import os.path

import pytest

import support

import math

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

class Node:

    def __init__(self, start=False, visited=False):
        self.visited = visited
        self.start_node = start

def euclidean_dist(x_1, y_1, x_2, y_2) -> float:
    x_dist = x_1 - x_2
    y_dist = y_1 - y_2
    return math.sqrt( x_dist**2 + y_dist**2)

class Board:

    def __init__(self, rows = 5, columns = 6):
        self.grid = list()

        # first n-1 rows
        for _ in range(rows-1):
            # columns per row
            self.grid.append([Node() for _ in range(columns)])

        # last row
        # start position always in bottom left
        row = []
        row.append(Node(start=True, visited=True))
        row += [Node() for _ in range(columns-1)]
        self.grid.append(row)

        self.traveler_head = (rows-1,0)
        self.traveler_tail = (rows-1,0)

        self.diagonal_dist = math.sqrt(2)


    def move_right(self) -> None:
        head_old = self.traveler_head
        self.traveler_head = (head_old[0], head_old[1]+1)

        # does this move outside the board? 
        # if so, undo; don't move
        if self.traveler_head[1] >= len(self.grid[0]):
            self.traveler_head = head_old
        # otherwise, let's determine if the tail moves
        else:

            dist = euclidean_dist(*self.traveler_head, *self.traveler_tail)

            # if greater than a diagonal away, move closer
            if dist > self.diagonal_dist:

                # if straight line, follow
                if dist == 2:
                    self.traveler_tail = (self.traveler_tail[0], self.traveler_tail[1]+1)

                # otherwise, move to minimize distance. Since the head moved right
                # we want to move right one and up or down one
                else:
                    is_above = False
                    tail_row = self.traveler_tail[0]
                    tail_col = self.traveler_tail[1]
                    if self.traveler_tail[0] < self.traveler_head[0]:
                        is_above = True

                    # move down
                    if is_above:
                        tail_row += 1
                    # move up
                    else:
                        tail_row-= 1

                    # move right
                    tail_col += 1

                    self.traveler_tail = (tail_row, tail_col)

                # update grid point
                self.grid[self.traveler_tail[0]][self.traveler_tail[1]].visited = True



        # print(f'Head now at: {self.traveler_head}')
        return None


    def move_up(self) -> None:
        head_old = self.traveler_head
        self.traveler_head = (head_old[0]-1, head_old[1])

        # does this move outside the board? 
        # if so, undo; don't move
        if self.traveler_head[0] < 0:
            self.traveler_head = head_old
        # otherwise, let's determine if the tail moves
        else:
            dist = euclidean_dist(*self.traveler_head, *self.traveler_tail)

            # if greater than a diagonal away, move closer
            if dist > self.diagonal_dist:

                # if straight line, follow
                if dist == 2:
                    self.traveler_tail = (self.traveler_tail[0]-1, self.traveler_tail[1])

                # otherwise, move to minimize the distance. Since the head moved up
                # we want to move up one, and right or left one
                else:
                    is_left = False
                    tail_row = self.traveler_tail[0]
                    tail_col = self.traveler_tail[1]
                    if self.traveler_tail[1] < self.traveler_head[1]:
                        is_left = True

                    # move right
                    if is_left:
                        tail_col += 1
                    # move left
                    else:
                        tail_col -= 1

                    # move up
                    tail_row -= 1

                    self.traveler_tail = (tail_row, tail_col)

                # update grid point
                self.grid[self.traveler_tail[0]][self.traveler_tail[1]].visited = True

        # print(f'Head now at: {self.traveler_head}')
        return None

    def move_left(self) -> None:
        head_old = self.traveler_head
        self.traveler_head = (head_old[0], head_old[1]-1)

        # does this move outside the board? 
        # if so, undo; don't move
        if self.traveler_head[1] < 0:
            self.traveler_head = head_old
        # otherwise, let's determine if the tail moves
        else:

            dist = euclidean_dist(*self.traveler_head, *self.traveler_tail)

            # if greater than a diagonal away, move closer
            if dist > self.diagonal_dist:

                # if straight line, follow
                if dist == 2:
                    self.traveler_tail = (self.traveler_tail[0], self.traveler_tail[1]-1)

                # otherwise, move to minimize distance. Since the head moved left
                # we want to move left one and up or down one
                else:
                    is_above = False
                    tail_row = self.traveler_tail[0]
                    tail_col = self.traveler_tail[1]
                    if self.traveler_tail[0] < self.traveler_head[0]:
                        is_above = True

                    # move down
                    if is_above:
                        tail_row += 1
                    # move up
                    else:
                        tail_row-= 1

                    # move right
                    tail_col -= 1

                    self.traveler_tail = (tail_row, tail_col)

                # update grid point
                self.grid[self.traveler_tail[0]][self.traveler_tail[1]].visited = True

    def move_down(self) -> None:
        head_old = self.traveler_head
        self.traveler_head = (head_old[0]+1, head_old[1])

        # does this move outside the board? 
        # if so, undo; don't move
        if self.traveler_head[0] >= len(self.grid):
            self.traveler_head = head_old
        # otherwise, let's determine if the tail moves
        else:
            dist = euclidean_dist(*self.traveler_head, *self.traveler_tail)

            # if greater than a diagonal away, move closer
            if dist > self.diagonal_dist:

                # if straight line, follow
                if dist == 2:
                    self.traveler_tail = (self.traveler_tail[0]+1, self.traveler_tail[1])

                # otherwise, move to minimize the distance. Since the head moved down
                # we want to move down one, and right or left one
                else:
                    is_left = False
                    tail_row = self.traveler_tail[0]
                    tail_col = self.traveler_tail[1]
                    if self.traveler_tail[1] < self.traveler_head[1]:
                        is_left = True

                    # move right
                    if is_left:
                        tail_col += 1
                    # move left
                    else:
                        tail_col -= 1

                    # move up
                    tail_row += 1

                    self.traveler_tail = (tail_row, tail_col)

                # update grid point
                self.grid[self.traveler_tail[0]][self.traveler_tail[1]].visited = True

        # print(f'Head now at: {self.traveler_head}')
        return None

        # print(f'Head now at: {self.traveler_head}')
        return None

    def __repr__(self):
        display = ''
        for i, row in enumerate(self.grid):
            row_disp = ''
            for j, n in enumerate(row):

                if (i,j) == self.traveler_head:
                    row_disp += 'H'

                elif (i,j) == self.traveler_tail:
                    row_disp += 'T'

                elif n.start_node:
                    row_disp += 's'
                # elif n.visited:
                #     row_disp += '#'

                else:
                    row_disp += '.'
            row_disp += '\n'
            display += row_disp
        return display

    def show_result(self):
        display = ''
        for i, row in enumerate(self.grid):
            row_disp = ''
            for j, n in enumerate(row):

                # if (i,j) == self.traveler_head:
                #     row_disp += 'H'

                # elif (i,j) == self.traveler_tail:
                #     row_disp += 'T'

                # elif n.start_node:
                #     row_disp += 's'

                if n.visited:
                    row_disp += '#'

                else:
                    row_disp += '.'
            row_disp += '\n'
            display += row_disp
        print(display)





board = ''

def compute(s: str) -> int:
    global board
    board = Board()
    # print('=====START=====')
    # print(board)

    lines = s.splitlines()
    for line in lines:

        direction, times = line.split()

        if direction == 'R':
            move = board.move_right
        elif direction == 'U':
            move = board.move_up
        elif direction == 'L':
            move = board.move_left
        elif direction == 'D':
            move = board.move_down
        else:
            assert direction in ['R', 'L', 'U', 'D']

        print(f'== {direction} {times} ==')


        for i in range(int(times)):
            print(f'[{i}]')
            move()
            print(board)
            print('')

    print('final')
    board.show_result()

    counter = 0
    for row in board.grid:
        for node in row:
            if node.visited:
                counter += 1



    # TODO: implement solution here!

    return counter


INPUT_S = '''\
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
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
