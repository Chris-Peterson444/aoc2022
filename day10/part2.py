from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

screen = ''

def draw_screen(cycle: int, x: int) -> None:
    global screen
    WIDTH = 40
    row = (cycle - 1) // WIDTH
    row_pos = cycle - (row * 40) - 1
    x_left = x - 1
    x_right = x + 1
    # print(f'x_range = [{x_left},{x_right}] and row_pos is {row_pos}')
    if row_pos== x_left or row_pos==x or row_pos== x_right:
        screen += '#'
    else:
        screen += '.'

    if cycle % 40 == 0:
        screen += '\n'



def compute(s: str) -> int:

    cycle = 1
    reg_x = 1
    signal_strengths = []


    lines = s.splitlines()
    for line in lines:
        
        tokens = line.split(' ')
        #noop
        if len(tokens) == 1:
            # print(f'noop on cycle {cycle}')
            draw_screen(cycle, reg_x)
            cycle += 1
        # add x
        elif len(tokens) == 2:
            # print(f'addx for {tokens[1]} on cycle {cycle}')
            draw_screen(cycle, reg_x)
            cycle += 1
            # print(f'continue addx for {tokens[1]} on cycle {cycle}')
            draw_screen(cycle, reg_x)
            cycle += 1
            reg_x += int(tokens[1])
            # print(f'updated X is now available at begninning of cycle {cycle}')
        # unhandeled instruction
        else:
            raise AssertionError(f'unexpected instruction {line}')

        # if cycle == 20 or (cycle-20) % 40 == 0:
        #     signal_strengths.append((cycle, reg_x))

    print(screen)
    ret = 0
    # for _cycle, x in signal_strengths:
    #     ret += _cycle * x

    # TODO: implement solution here!
    return ret


# INPUT_S = '''\
# noop
# addx 3
# addx -5
# '''
INPUT_S = ''
with open('pytest_input.txt','r') as file:
    INPUT_S = file.read()
EXPECTED = 13140


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
