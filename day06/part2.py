from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    
    packet = []

    for char in s[0:14]:
        packet.append(char)

    if len(set(packet)) == 14:
        return 14

    # print(f'Packet: {packet}')

    for i, letter in enumerate(s[14:]):
        packet.pop(0)
        packet.append(letter)
        # print(f'Packet: {packet}, head={i+4+1}')
        if len(set(packet)) == 14:
            return i + 14 + 1
        



    return -1


INPUT_S_1 = '''\
mjqjpqmgbljsphdztnvjfqwrcgsmlb
'''
EXPECTED_1 = 19

INPUT_S_2 = '''\
bvwbjplbgvbhsrlpgdmjqwftvncz
'''
EXPECTED_2 = 23

INPUT_S_3 = '''\
nppdvjthqldpwncqszvftbrmjlhg
'''
EXPECTED_3 = 23

INPUT_S_4 = '''\
nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg
'''
EXPECTED_4 = 29

INPUT_S_5 = '''\
zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw
'''
EXPECTED_5 = 26


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
