from __future__ import annotations

import argparse
import os.path

import pytest

import support


import string

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

cost = {l:c for l,c in zip(string.ascii_lowercase,range(1,27))}
cost['S'] = cost['a']
cost['E'] = cost['z']


def compute(s: str) -> int:

    grid = s.splitlines()
    start_pos = (-1,-1)
    goal_pos = (-1,-1)

    # find goal and start
    for i, row in enumerate(grid):
        for j, letter in enumerate(row):
            if letter == 'E':
                goal_pos = (i,j)
            if letter == 'S':
                start_pos = (i,j)
    ## bfs
    current_pos = start_pos

    visited = set()
    to_visit = [current_pos]
    previous_node = {}
    previous_node[current_pos] = (-1,-1)
    while len(to_visit) > 0:
        current_pos = to_visit.pop(0)
        if current_pos in visited:
            continue
        if current_pos == goal_pos:
            break
        current_elevation = grid[current_pos[0]][current_pos[1]]
        visited.add(current_pos)
        # checking neighbors
        # 1. make sure in bound
        # 2. make sure not visited before
        # 3. make sure cost is <= 1

        # check if has a top neighbor + (-1, 0)
        # check if has a left neighbor + (0, -1)
        # check if has a right neighbor + (0, 1)
        # check if has a down neighbor + (1, 0)
        for disp in [(-1,0), (0,-1), (0,1), (1,0)]:
            neighbor = (current_pos[0]+disp[0],current_pos[1]+disp[1])
            if  0 <= neighbor[0] < len(grid) and 0 <= neighbor[1] < len(grid[0]):
                neighbor_elevation = grid[neighbor[0]][neighbor[1]]
                if neighbor not in visited and cost[neighbor_elevation] <= cost[current_elevation] + 1:
                    to_visit.append(neighbor)
                    previous_node[neighbor] = current_pos

    count = 0
    curr = goal_pos
    # print(previous_node)
    while curr != (-1,-1):
        curr = previous_node[curr]
        count += 1
    count -= 1



    return count



INPUT_S = '''\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
'''
EXPECTED = 31


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
