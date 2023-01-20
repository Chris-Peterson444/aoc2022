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


def compute(s: str, coord_upper_bound : int = 4000000) -> int:

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
                  # #
                   #
    Each corner is a line. Find the region outlined by the intersection of 4 different lines
    Remember the point-slope formula: y - y_1 = m(x-x_1)
    y_1 is going to be the boundary of our scan radius + 1 (so our intersection point is the point we want,
        and we don't get four intersection points that border the point we want)
    So then y_1 = sensor.y +/- (sensor.range + 1)

    The lines going up (m= 1):
    y - sensor.y +/- (sensor.range + 1) = x - sensor.x
    
    The lines going down (m= -1)
    y - sensor.y +/- (sensor.range + 1) = -x + sensor.x

    Rewriting:
    y = x + sensor.y - sensor.x - sensor.range - 1 
    y = x + sensor.y - sensor.x + sensor.range + 1

    y = -x + sensor.y + sensor.x - sensor.range - 1
    y = -x + sensor.y + sensor.x + sensor.range + 1

    """
    coeff_up, coeff_down = [], []
    for sensor in sensors:
        coeff_up.append(sensor.y-sensor.x+sensor.range+1)
        coeff_up.append(sensor.y-sensor.x-sensor.range-1)
        coeff_down.append(sensor.y+sensor.x+sensor.range+1)
        coeff_down.append(sensor.y+sensor.x-sensor.range-1)
    up_candidates = {coeff for coeff in coeff_up if coeff_up.count(coeff) >= 2}
    down_candidates = {coeff for coeff in coeff_down if coeff_down.count(coeff) >= 2}
    for a in up_candidates:
        for b in down_candidates:
            # up: y = x + a
            # down: y = -x + b
            # intersections:
            #   1. add together -> 2y = a + b -> y = (a+b)/2
            #   2. subtract -> 0 = 2x + a - b -> 2x = b - a -> x = (b-a)//2
            x_point, y_point = (b-a)//2, (a+b)//2
            if 0 <= x_point <= coord_upper_bound and 0 <= y_point <= coord_upper_bound:
                if all(l1_dist((sensor.x,sensor.y),(x_point,y_point)) > sensor.range for sensor in sensors):
                    return (x_point * 4000000) + y_point




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
EXPECTED = 56000011


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s, coord_upper_bound = 20) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
