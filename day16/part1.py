from __future__ import annotations

import argparse
import os.path
import re
import itertools


import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

VALVE = re.compile(
    r'Valve ([A-Z]+) has flow rate=(\d+); '
    )

TUNNELS = re.compile(r'([ ][A-Z][A-Z],*)')

def compute(s: str) -> int:

    rate = dict()
    links = dict()

    lines = s.splitlines()
    for line in lines:
        valve_match = VALVE.match(line)
        line = line.split(';')[1]
        tunnels_match = TUNNELS.findall(line)
        rate[valve_match[1]] = int(valve_match[2])
        links[valve_match[1]] = [s.strip(', ') for s in tunnels_match]
        # if len(links[valve_match[1]]) > 1:
        #     tuns = 'tunnels lead to valves '
        # else:
        #     tuns = 'tunnel leads to valve '
        # tuns += "".join(s+', ' for s in links[valve_match[1]])
        # tuns=tuns[:-2]
        # print(f'Valve {valve_match[1]} has flow rate={valve_match[2]}; {tuns}')


    """
    ----------------------
    After some struggling and debugging poor solutions I found this on reddit:
    https://www.reddit.com/r/adventofcode/comments/zn6k1l/comment/j2xhog7/?utm_source=share&utm_medium=web2x&context=3

    I ended up restructing my solution to look like theirs. There were a couple things I think they did better, but
    the biggest bug I ran into in my code is forgetting to eliminate zero-flow nodes from my search. Since we already
    constructed the fully connected graph, they are useless. Below I explain my thoughts on the problem and explain 
    the process behind the algorithm.
    ---------------------

    A greedy approach won't work for all situations. Dashing for the biggest flow valve will fail when differences
    between flows are minimal, but opening flow valves as you come across them will fail when differences are large.
    The first choice that comes to mind is that we will have to do some sort of DFS/BFS but the problem is backtracking
    on an incomplete graph. By using a complete graph, where the edge weight is the total time it takes to travel
    between nodes, we could "bake-in" the backtracking on graph traversal and perform an augmented graph search.
    Finally, and very importantly, we augment the search by ignoring neighbors which have a flow-rate of zero.
    By baking in backtracking into our graph, traversing to zero-flow rate nodes defeats the purpose. Theoretically
    we are traveling to a useless destination or even traveling in a cycle, but practically we are wasting large 
    ammounts of computation time by calcuating sub-optimal trees.

    There may be further savings by 

    General Algorithm:
    1. Generate complete graph using Floyd-Warshall Algorithm
    2. Generate a set of non-zero flow rate vales
    3. Perform pseudo-dfs
        3.1 Starting at AA, look at all non-zero neighbors
        3.2 Travel to unvisited (non-zero) neighbor of AA and turn on valve
        3.2 Recursively repeat 3.1-3.2 with current node until time runs out or visited all valves on current path
        3.3 Append returns of recursive visits to a list of possible pressures, return the max pressure

    """


    # 1. Get distances via Floyd-Warshall Algorithm
    distance = {(i,j): 1 if j in links[i] else 1000 for i in links for j in links}

    # k, i, j order important. If you don't remember Floyd-Warshall algorithm the wiki page is pretty good:
    # https://en.wikipedia.org/wiki/Floyd-Warshall_algorithm
    for k, i, j in itertools.permutations(links, 3):
        distance[i,j] = min(distance[i,j], distance[i,k] + distance[k,j])

    # 2. Generate set of non-zero flow rate valves
    non_zero_rates = {valve:flow for valve,flow in rate.items() if flow != 0}

    # 3. Psuedo DFS 
    
    # Option 1:
    # This was close to my original solution, and probably the more "pythonic" way
    # but set creation might slow us down

    # def visit(current_valve, minutes, visited, pressure, answer):
    #     visited_set = frozenset(visited)
    #     answer[visited_set] = max(answer.get(visited_set, 0), pressure)
    #     for dest_valve, flow in non_zero_rates.items():
    #         new_time = minutes - distance[current_valve, dest_valve] - 1
    #         if new_time <= 0 or dest_valve in visited:
    #             continue
    #         new_pressure = pressure + flow*new_time
    #         visit(dest_valve, new_time, visited + [dest_valve], new_pressure, answer) 

    #     return answer

    # return max(visit('AA', 30, [], 0, dict()).values())

    # Option 2:
    # Less set creation, probably the most intuitive, with less state between each call
    def visit(current_valve, minutes, visited, pressure):
        answers = []
        answers.append(pressure)
        for dest_valve, flow in non_zero_rates.items():
            new_time = minutes - distance[current_valve, dest_valve] - 1
            if new_time <= 0 or dest_valve in visited:
                continue
            new_pressure = pressure + flow*new_time
            answers.append(visit(dest_valve, new_time, visited + [dest_valve], new_pressure))

        return max(answers)

    return visit('AA', 30, [], 0)


    # Option 3: 
    # This is u/Gravitar64's original solution 
    # Intstead of dealing with set creation, they chose to do bit operations by giving them unique bit strings
    # bit_string = {valve : 1 << i for i, valve in enumerate(non_zero_rates)}

    # def visit(current_valve, minutes, visited, pressure, answer):
    #     answer[visited] = max(answer.get(visited, 0), pressure)
    #     for dest_valve, flow in non_zero_rates.items():
    #         new_time = minutes - distance[current_valve, dest_valve] - 1
    #         if new_time <= 0 or bit_string[dest_valve] & visited:
    #             continue
    #         new_pressure = pressure + flow * new_time
    #         visit(dest_valve, new_time, bit_string[dest_valve] | visited, new_pressure, answer) 

    #     return answer

    # return max(visit('AA', 30, 0, 0, {}).values())




INPUT_S = '''\
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
'''
EXPECTED = 1651


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
