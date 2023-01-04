from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:

    lines = s.splitlines()

    stacks = {}
    
    top_line = lines[0]

    chars_per_stack = 4
    num_stacks = (len(top_line) + 1)//chars_per_stack

    for i in range(1,num_stacks+1):
        stacks[i] = []

    counter = 0

    for line in lines:
        counter += 1

        boxes = [line[i:i+3] for i in range(0, len(line), 4)]
        # print(boxes)

        # break on the numbered line
        if boxes[0] == ' 1 ':
            break

        for i, box in enumerate(boxes):
            letter = box.strip(' []\n')
            if letter != '':
                stacks[i+1].append(letter)

    instructions = lines[counter+1:]

    for line in instructions:
        tokens = line.split()

        num_to_move = int(tokens[1])
        origin = int(tokens[3])
        dest = int(tokens[5])

        moving = []
        for _ in range(num_to_move):
            moving.append(stacks[origin].pop(0))
        
        for _ in range(num_to_move):
            stacks[dest].insert(0,moving.pop(-1))



    tops = ''
    for stack in stacks.values():
        char = stack.pop(0)
        if char != '':
            tops += char
    # TODO: implement solution here!
    # print(f'{tops!r}')
    return tops


INPUT_S = '''\
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
'''
EXPECTED = 'MCD'


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
