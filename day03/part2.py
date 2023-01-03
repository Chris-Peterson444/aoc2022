from __future__ import annotations

import argparse
import os.path

import pytest

import support

import string


INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

letter_prio = {l:n for (l,n) in zip(string.ascii_lowercase,range(1,27))}
letter_prio.update({l:n for (l,n) in zip(string.ascii_uppercase, range(27,53))})

def compute(s: str) -> int:

    lines = s.split()

    priority = 0

    num_lines = len(lines)
    num_groups = num_lines//3
    
    for group in range(num_groups):

        sack_1 = set(lines.pop())
        sack_2 = set(lines.pop())
        sack_3 = set(lines.pop())
        badge = sack_3.intersection(sack_2).intersection(sack_1)
        priority += letter_prio[badge.pop()]

    # for line in lines:
    #     line_len = len(line)
    #     half = line_len//2
    #     front = line[:half]
    #     back = line[half:]

    #     front_set = set(front)
    #     back_set = set(back)
    #     intersection = front_set.intersection(back_set)
    #     sack_prio = letter_prio[intersection.pop()]
    #     priority += sack_prio




    return priority


INPUT_S = '''\
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
'''
EXPECTED = 70


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
