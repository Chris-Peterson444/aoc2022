from __future__ import annotations

import argparse
import os.path
import re 
import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

parser = re.compile(
    r'^Sensor at x=(-?\d+), y=(-?\d+): '
    r'closest beacon is at x=(-?\d+), y=(-?\d+)$',)

def l1_dist(a: tuple[int,int], b: tuple[int,int]) -> int:
    """ L1 Distance (i.e taxicab/Manhattan distance) """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

class Sensor:
    def __init__(self,sensor_x,  sensor_y, beacon_x, beacon_y):
        self.x = sensor_x
        self.y = sensor_y
        self.beacon = (beacon_x,beacon_y)
        self.range = l1_dist((sensor_x,sensor_y),(beacon_x,beacon_y))


def compute(s: str, row_of_interest: int = 2000000) -> int:

    lines = s.splitlines()

    sensors : list[Sensor] = []
    for line in lines:
        match = parser.match(line)
        sensor_x, sensor_y = int(match[1]), int(match[2])
        beacon_x, beacon_y = int(match[3]), int(match[4])
        sensors.append(Sensor(sensor_x,sensor_y,beacon_x,beacon_y))


    """ 
    
    The sensor range makes a diamond shape:
            
                   #
                  # #
                 #   #
                #  S  #
                 #   #
            ------#-#-------
                   #
    We want to determine the ranges for which this shape intersects our line of interest
    """
    overlapped : list[tuple[int,int]] = list()
    for sensor in sensors:

        dist = abs(row_of_interest - sensor.y)

        if dist <= sensor.range :
            range_diff = abs(dist - sensor.range)  

            overlap_range = ((sensor.x - range_diff),(sensor.x + range_diff))

            overlapped.append(overlap_range)

    # let's merge to get rid of overlapping ranges
    overlapped.sort(key=lambda x: x[0])
    merged : list[list[int,int]] = [[overlapped[0][0],overlapped[0][1]]]
    for (start, end) in overlapped:
        previous = merged[-1]
        if start <= previous[1]:
            previous[1] = max(previous[1], end)
        else:
            merged.append([start,end])

    # count up all the overlapped points
    total = 0
    for (start, end) in merged:
        total += end - start

    return total



INPUT_S = '''\
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
'''
EXPECTED = 26


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s, row_of_interest=10) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
