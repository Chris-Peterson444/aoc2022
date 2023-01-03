from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

WIN = 6
DRAW = 3
LOSS = 0

ROCK = ['A', 'X' ]
PAPER = ['B', 'Y']
SCISSORS = ['C', 'Z' ]

ROCK_PICK = 1
PAPER_PICK = 2
SCISSORS_PICK = 3


def compute(s: str) -> int:

    score = 0

    rounds = s.split('\n')[:-1]

    for r in rounds:

        elf, me = r.split(' ')

        round_score = 0

        # winning possibilities
        if elf in ROCK and me in PAPER:
            round_score += WIN
            round_score += PAPER_PICK
        elif elf in PAPER and me in SCISSORS:
            round_score += WIN
            round_score += SCISSORS_PICK
        elif elf in SCISSORS and me in ROCK:
            round_score += WIN
            round_score += ROCK_PICK
        
        # loosing posibilities

        elif elf in ROCK and me in SCISSORS:
            round_score += LOSS
            round_score += SCISSORS_PICK
        elif elf in PAPER and me in ROCK:
            round_score += LOSS
            round_score += ROCK_PICK
        elif elf in SCISSORS and me in PAPER:
            round_score += LOSS
            round_score += PAPER_PICK

        # draw
        else:
            round_score += DRAW
            if me in ROCK:
                round_score += ROCK_PICK
            elif me in PAPER:
                round_score += PAPER_PICK
            elif me in SCISSORS:
                round_score += SCISSORS_PICK
            else:
                raise AssertionError(f'Unknown Pick {me!r}')

        # print(f'Round: {r!r}; score: {round_score}')
        score += round_score
        # else:
        #     raise AssertionError(f'Unhandled case me: {me!r} and elf: {elf!r}')



    return score


INPUT_S = '''\
A Y
B X
C Z
'''
EXPECTED = 15


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
