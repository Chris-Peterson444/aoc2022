from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    ENTRY_POINT = 500, 0
    rock_points = set()
    lines = s.splitlines()
    
    for line in lines:
        path_points = line.split('->')

        prev_x, prev_y  =  path_points.pop(0).strip().split(',')
        while path_points:            
            curr_x, curr_y = path_points.pop(0).strip().split(',')

            # moving up or down
            if curr_x == prev_x:
                x = int(curr_x)
                y_1 = int(curr_y)
                y_2 = int(prev_y)

                # need to know sign to get range right
                if y_1 < y_2:
                    _range = range(y_1,y_2+1)
                else:
                    _range = range(y_2, y_1+1)
                for y in _range:
                    rock_points.add((x,y))

            # move left or right
            elif curr_y == prev_y:
                y = int(curr_y)
                x_1 = int(curr_x)
                x_2 = int(prev_x)

                # need to know sign to get range right
                if x_1 < x_2:
                    _range = range(x_1,x_2+1)
                else:
                    _range = range(x_2, x_1+1)
                for x in _range:
                    rock_points.add((x,y))

            prev_x, prev_y = curr_x, curr_y
    ## empty region of interest
    # for y in range(0,max(rock_points, key = lambda x: x[1])[1]+1):
    #     line = ''
    #     for x in range(min(rock_points, key = lambda x: x[0])[0],max(rock_points, key= lambda x : x[0])[0] +1):
    #         if (x,y) in rock_points:
    #             line += '#'
    #         elif (x,y) == ENTRY_POINT:
    #             line += '+'
    #         else:
    #             line += '.'
    #     print(line)

    MAX_DEPTH = max(rock_points, key = lambda x: x[1])[1]

    sand_points = set()

    done = False
    curr_position = ENTRY_POINT
    # print(f'max depth is {MAX_DEPTH}')

    while not done:
        # print(f'current sand piece at {curr_position}')

        # 'generate a sand piece'
        # keep going until it's rested
        curr_x, curr_y = curr_position
        straight_down = (curr_x, curr_y+1)
        diagonal_left = (curr_x-1, curr_y+1)
        diagonal_right = (curr_x+1, curr_y+1)

        # print(f'straight sand piece at {straight_down}')
        # print(f'diagonal left sand piece at {diagonal_left}')
        # print(f'diagonal right sand piece at {diagonal_right}')

        if straight_down not in rock_points and straight_down not in sand_points:
            curr_position = straight_down

            # check if we've hit the abyss
            if curr_y == MAX_DEPTH:
                done = True

        elif diagonal_left not in rock_points and diagonal_left not in sand_points:
            curr_position = diagonal_left
        elif diagonal_right not in rock_points and diagonal_right not in sand_points:
            curr_position = diagonal_right
        else:
            # rested; register sand piece and go to next sand piece to generate
            sand_points.add(curr_position)
            curr_position = ENTRY_POINT

        # print(f'moved to {curr_position}')

        ## prints out region at each step
        # for y in range(0,max(rock_points, key = lambda x: x[1])[1]+1):
        #     line = ''
        #     for x in range(min(rock_points, key = lambda x: x[0])[0],max(rock_points, key= lambda x : x[0])[0] +1):
        #         if (x,y) in rock_points:
        #             line += '#'
        #         elif (x,y) in sand_points:
        #             line += 'o'
        #         elif (x,y) == curr_position:
        #             line += 's'
        #         elif (x,y) == ENTRY_POINT:
        #             line += '+'
        #         else:
        #             line += '.'
        #     print(line)


    # TODO: implement solution here!
    return len(sand_points)


INPUT_S = '''\
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
'''
EXPECTED = 24


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
