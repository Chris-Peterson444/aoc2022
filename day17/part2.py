from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

class Rock:

    def move(self, dir_row, dir_col):
        updated_positions = []
        for pos in self.positions:
            row, col = pos
            updated_positions.append((row+dir_row,col+dir_col))
        self.positions = updated_positions

    def move_down(self):
        self.move(-1,0)

    def move_right(self):
        self.move(0,1)

    def move_left(self):
        self.move(0,-1)

    # def bottom(self):
    #     return min(self.positions,key=lambda x: x[0])

    def right(self):
        return max(self.positions,key= lambda x: x[1])

    def left(self):
        return min(self.positions, key= lambda x:x[1])

    def right_intersection(self, grid):
        to_check = []
        right = self.right()[1]
        for pos in self.positions:
            to_check.append(pos)
        for pos in to_check:
            row, col = pos
            if (row,col+1) in grid:
                return True
        return False
    def left_intersection(self, grid):
        to_check = []
        left = self.left()[1]
        for pos in self.positions:
            to_check.append(pos)
        for pos in to_check:
            row, col = pos
            if (row,col-1) in grid:
                return True
        return False


class Rock_1(Rock):
    """
    Rock looks like: ####
    """
    def __init__(self, left_pos, bottom_pos):
        row,col = bottom_pos, left_pos
        self.positions = []
        # left
        self.positions.append((row,col))
        # middle-left
        self.positions.append((row,col+1))
        # middle-right
        self.positions.append((row,col+2))
        # right
        self.positions.append((row,col+3))


class Rock_2(Rock):
    """
    Rock looks like: .#.
                     ###
                     .#.
    """
    def __init__(self, left_pos, bottom_pos):
        self.positions = []
        # top
        self.positions.append((bottom_pos+2,left_pos+1))
        # left-middle 
        self.positions.append((bottom_pos+1,left_pos))
        # middle-middle
        self.positions.append((bottom_pos+1,left_pos+1))
        # middle-right
        self.positions.append((bottom_pos+1,left_pos+2))
        # bottom
        self.positions.append((bottom_pos,left_pos+1))

class Rock_3(Rock):
    """
    Rock looks like: ..#
                     ..#
                     ###
    """
    def __init__(self, left_pos, bottom_pos):
        self.positions = []
        # top-right
        self.positions.append((bottom_pos+2,left_pos+2))
        # middle-right 
        self.positions.append((bottom_pos+1,left_pos+2))
        # bottom-left
        self.positions.append((bottom_pos,left_pos))
        # bottom-middle
        self.positions.append((bottom_pos,left_pos+1))
        # bottom-right
        self.positions.append((bottom_pos,left_pos+2))


class Rock_4(Rock):
    """
    Rock looks like: #
                     #
                     #
    """
    def __init__(self, left_pos, bottom_pos):
        self.positions = []
        # top
        self.positions.append((bottom_pos+3,left_pos))
        # second from top
        self.positions.append((bottom_pos+2,left_pos))
        # second from bottom
        self.positions.append((bottom_pos+1,left_pos))
        # bottom
        self.positions.append((bottom_pos,left_pos))


class Rock_5(Rock):
    """
    Rock looks like: ##
                     ##
    """
    def __init__(self, left_pos, bottom_pos):
        self.positions = []
        # top - left
        self.positions.append((bottom_pos+1,left_pos))
        # top-right 
        self.positions.append((bottom_pos+1,left_pos+1))
        # bottom left
        self.positions.append((bottom_pos,left_pos))
        # bottom-right
        self.positions.append((bottom_pos,left_pos+1))



def print_grid(grid, rock_pos, min_col, max_col):
    top = max(grid,key=lambda x: x[0])[0] + 6
    bottom = top - 6 - 4
    for row in range(top, -1, -1):
        line = ''
        for col in range(min_col-1, max_col+2):
            if row == 0:
                line += '-'
            elif col == min_col -1 or col == max_col + 1:
                line += '|'
            elif (row,col) in grid:
                line += '#'
            elif (row,col) in rock_pos:
                line += '@'
            else:
                line += '.'
        print(line)

    print('')

def top_down_view(grid):
    cols = [ [] for _ in range(7)]
    heights = [-1 for i in range(7)]

    for row,col in grid:
        cols[col].append((row,col))

    for i, col in enumerate(cols):
        heights[i] = max(col, key = lambda x: x[0])[0]
    tallest= max(heights)
    for i, h in enumerate(heights):
        heights[i] = h - tallest 
    return frozenset(heights)

"""
Find a cycle by keeping track of state.
State consists of:
1. top down view from highest block on tower e.g.: [-1,-1,0,-20,-7,...]
2. Index of current gas direction
3. Current block type

Then auto generate as many cycles as possible once a cycle is found (repeating state)

Currently only repeating the first found cycle, but took about a minute to finish simulation
once the first cycle was found. I could probably speed this up by continuing to auto generate cycles
but I'll revist this when I have more motivation.

"""
def compute(s: str) -> int:
    s = s.strip()
    grid = set()
    for i in range(7): grid.add((0,i)) # add floor
    MIN_X = 0
    MAX_X = 6
    MAX_ROCKS = 1000000000000
    gas_flow = list(enumerate(s))
    rock_order = [Rock_1, Rock_2, Rock_3, Rock_4, Rock_5]
    curr_rock_idx = len(rock_order) - 1
    spawn_rock = True
    states = {}
    num_rocks = 0
    pre_auto_height = 0
    auto_generated = False
    post_auto_height = 0
    while True:
        instr_id, flow_dir = gas_flow.pop(0)
        
        if spawn_rock:
            # spawn rock
            if curr_rock_idx == len(rock_order) - 1:
                curr_rock_idx = 0
            else:
                curr_rock_idx += 1

            curr_height = max(grid,key=lambda x: x[0])[0]
            next_height = curr_height + 4
            next_left = MIN_X + 2
            rock = rock_order[curr_rock_idx](next_left,next_height)

            spawn_rock = False
            num_rocks += 1
            if num_rocks == MAX_ROCKS + 1:
                break
            # print(f'iteration: (spawn)', '-'*50)
            # print_grid(grid, rock.positions,MIN_X, MAX_X)
            # input()
        # if num_rocks == 20:
        #     print_grid(grid, rock.positions,MIN_X, MAX_X)

        view = top_down_view(grid)
        state = frozenset([view,rock_order[curr_rock_idx],instr_id])
        # print(num_rocks)
        if state in states and not auto_generated:
            auto_generated = True
            rocks_in_cycle = num_rocks - states[state][0]
            height_in_cycle = max(grid,key= lambda x: x[0])[0] - states[state][1]
            remaining_rocks = 1000000000000 - num_rocks
            quotient, remainder = divmod(remaining_rocks,rocks_in_cycle)
            curr_height = max(grid, key=lambda x: x[0])[0]
            pre_auto_height = curr_height
            post_auto_height = curr_height+ (quotient * height_in_cycle)
            num_rocks += quotient*rocks_in_cycle
            

        else:
            states[state] = num_rocks,max(grid, key=lambda x: x[0])[0]

        # gas moves rock

        if flow_dir == '>':
            # moving right
            right = rock.right()
            if right[1] != MAX_X and not rock.right_intersection(grid):
                rock.move_right()


        elif flow_dir == '<':
            # moving left
            left = rock.left()
            if left[1] != MIN_X and not rock.left_intersection(grid):
                rock.move_left()

        else:
            raise AssertionError



        # print(f'iteration: (post moving left or right)', '-'*50)
        # print_grid(grid, rock.positions,MIN_X, MAX_X)

        # input()



        # rock falls one unit


        # check if resting on another rock or floor before moving
        resting = False
        for pos in rock.positions:
            row,col = pos
            if (row-1,col) in grid:
                resting = True
                break

        if resting:
            spawn_rock = True
            for pos in rock.positions: grid.add(pos)
        else:
            rock.move_down()


        
        # print(f'iteration: (post moving down)', '-'*50)
        # print_grid(grid, rock.positions,MIN_X, MAX_X)
        # if resting:
        #     print('resting')
        # else:
        #     print('not resting')
        # input()



        # repeat instructions
        if not gas_flow:
            gas_flow = list(enumerate(s))

    final_height = (max(grid,key=lambda x:x[0])[0] - pre_auto_height) + post_auto_height

    return final_height


INPUT_S = '''\
>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>
'''
EXPECTED = 1514285714288


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
