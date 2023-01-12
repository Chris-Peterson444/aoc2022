from __future__ import annotations

import argparse
import os.path

import pytest

import support

import math

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def euclidean_dist(x_1, y_1, x_2, y_2) -> float:
    x_dist = x_1 - x_2
    y_dist = y_1 - y_2
    return math.sqrt( x_dist**2 + y_dist**2)

class Board:

    def __init__(self):

        # head is 0
        # tail is -1
        self.travelers = [(4,0) for _ in range(10)]

        self.diagonal_dist = math.sqrt(2)



        self.visited = set()
        self.visited.add(self.travelers[-1])


    @staticmethod
    def closest_cord(leader_x, leader_y, follower_x, follower_y):
        x_dist = leader_x - follower_x
        y_dist = leader_y - follower_y

        if x_dist != 0:
            x_dist = x_dist//abs(x_dist)
        if y_dist != 0:
            y_dist = y_dist//abs(y_dist)

        new_x = follower_x + x_dist
        new_y = follower_y + y_dist
        return new_x, new_y


    def move(self, x_disp, y_disp) -> None:
        # breakpoint()
         # move head
        head_old = self.travelers[0]
        self.travelers[0] = (head_old[0]+x_disp, head_old[1]+y_disp)

        for i in range(len(self.travelers)-1):
            leader_knot = self.travelers[i]
            follower_knot = self.travelers[i+1]

            dist = euclidean_dist(*leader_knot, *follower_knot)

            # if greater than a diagonal away, move closer
            if dist > self.diagonal_dist:
                new_x, new_y = self.closest_cord(*leader_knot, *follower_knot)
                self.travelers[i+1] = new_x, new_y

        # Always addd the tail to the visited set
        self.visited.add(self.travelers[-1])


        # print(f'Head now at: {self.traveler_head}')
        return None

    def move_right(self) -> None:
        return self.move(0,1)

    def move_up(self) -> None:
        return self.move(-1, 0)

    def move_left(self) -> None:
        return self.move(0,-1)

    def move_down(self) -> None:
        return self.move(1,0)

    def __repr__(self):

        display = ''
        x_list = []
        y_list = []

        # add the minimum board size
        x_list.append(0)
        x_list.append(4)
        y_list.append(0)
        y_list.append(5)

        for x,y in self.visited:
            x_list.append(x)
            y_list.append(y)
        for x,y in self.travelers:
            x_list.append(x)
            y_list.append(y)


        for i in range(min(x_list),max(x_list)+1):
            row_disp = ''
            for j in range(min(y_list),max(y_list)+1):


                if (i,j) in self.travelers:
                    for idx, coord in enumerate(self.travelers):
                        if (i,j) == coord:
                            if idx == 0:
                                row_disp += 'H'
                            else:
                                # numbers are reversed
                                row_disp += f'{idx}'

                            # quit after the highest order one
                            break
                elif (i,j) == (4,0):
                    row_disp += 's'
                else:
                    row_disp += '.'
            row_disp += '\n'
            display += row_disp
        return display

    def show_result(self):

        display = ''
        x_list = []
        y_list = []

        # add the minimum board size
        x_list.append(0)
        x_list.append(4)
        y_list.append(0)
        y_list.append(5)

        for x,y in self.visited:
            x_list.append(x)
            y_list.append(y)
        for x,y in self.travelers:
            x_list.append(x)
            y_list.append(y)


        for i in range(min(x_list),max(x_list)+1):
            row_disp = ''
            for j in range(min(y_list),max(y_list)+1):


                if (i,j) in self.visited:
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

        # print(f'== {direction} {times} ==')


        for i in range(int(times)):
            # print(f'[{i}]')
            move()
            # print(board)
            # print('')

    # print('final')
    # board.show_result()


    return len(board.visited)


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
EXPECTED = 1

INPUT_2 = '''\
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
'''
EXPECTED_2 = 36


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
        (INPUT_2, EXPECTED_2),
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
