

from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

from itertools import zip_longest

def correctOrder(left, right) -> bool:

    for l,r in zip_longest(left, right, fillvalue=None):
        ret = None
        if isinstance(l,int) and isinstance(r,int):
            if l < r:
                return True
            elif l > r:
                return False

        elif isinstance(l,list) and isinstance(r, list):
            ret = correctOrder(l,r)
        elif isinstance(l, list) and isinstance(r, int):
            ret = correctOrder(l,[r])
        elif isinstance(l, int) and isinstance(r, list):
            ret = correctOrder([l],r)

        elif l is None:
            return True
        elif r is None:
            return False

        if ret is not None:
            return ret


def stringToList(string: str) -> list:

    return eval(string)



def compute(s: str) -> int:

    packets = []
    for line in s.split('\n'):
        if line != '':
            packets.append(line)

    packets.append('[[2]]')
    packets.append('[[6]]')
    orders = []

    """

    The index of packet_1 is the number of packets it's greater to +1 (for 1-indexing)
    or packet_1_index = len({packet_2 in all_packets | packet_1 > packet_2, packet_1 in all_packets}

    """


    # could do all of them if we chose to

    # for i, p1 in enumerate(packets):
    #     index = 0
    #     packet_1 = stringToList(p1)
    #     for j, p2 in enumerate(packets):
    #         if i != j:
    #             packet_2 = stringToList(p2)
    #             if correctOrder(packet_2,packet_1):
    #                 index += 1
                    
    #     orders.append((index,p1))

    # orders.sort(key= lambda x: x[0])

    # Otherwise, do only the elements we care about to save time
    # starting at 1 for 1-indexing
    index_2 = 1
    index_6 = 1
    for packet in packets:
        p = stringToList(packet)
        index_2 += 1 if correctOrder(p,[[2]]) else 0
        index_6 += 1 if correctOrder(p,[[6]]) else 0

    return index_2 * index_6    


   


INPUT_S = '''\
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
'''
EXPECTED = 140


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
