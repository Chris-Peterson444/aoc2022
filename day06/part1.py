from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    
    packet = []

    for char in s[0:4]:
        packet.append(char)

    if len(set(packet)) == 4:
        return 4

    # print(f'Packet: {packet}')

    for i, letter in enumerate(s[4:]):
        packet.pop(0)
        packet.append(letter)
        # print(f'Packet: {packet}, head={i+4+1}')
        if len(set(packet)) == 4:
            return i + 4 + 1
        



    return -1


INPUT_S_1 = '''\
mjqjpqmgbljsphdztnvjfqwrcgsmlb
'''
EXPECTED_1 = 7

INPUT_S_2 = '''\
bvwbjplbgvbhsrlpgdmjqwftvncz
'''
EXPECTED_2 = 5

INPUT_S_3 = '''\
nppdvjthqldpwncqszvftbrmjlhg
'''
EXPECTED_3 = 6

INPUT_S_4 = '''\
zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw
'''
EXPECTED_4 = 11

INPUT_S_5 = '''\
nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg
'''
EXPECTED_5 = 10


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S_1, EXPECTED_1),
        (INPUT_S_2, EXPECTED_2),
        (INPUT_S_3, EXPECTED_3),
        (INPUT_S_4, EXPECTED_4),
        (INPUT_S_5, EXPECTED_5),
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
