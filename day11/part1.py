from __future__ import annotations

import argparse
import os.path

import pytest

import support

from typing import Optional
from typing import List


INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

# Part 1 is my work.

class Monkey:

    def __init__(self,
        operation: str,
        divisibility: int,
        true_test_target: int,
        false_test_target:int,
        starting_items: Optional[List[int]] = None,
        monkey_id: Optional[int] = None,
        ):

        self.items = starting_items
        self.operation_string = operation
        self.divisibility = divisibility
        self.true_test_target = true_test_target
        self.false_test_target = false_test_target
        self.id = monkey_id
        self.num_inspections = 0

    def add_item(self, item: int) -> None:
        self.items.append(item)

    def inspect(self):
        while len(self.items) != 0:
            item = self.items.pop(0)
            # print(f'\tMonkey insepcts an item with worry level {item}')
            item = self.operate(item)
            if item % self.divisibility == 0:
                target = self.true_test_target

                # print(f'\t\tCurrent worry level is divisible by {self.divisibility}')
                # print(f'\t\tItem with worry level {item} is thrown to monkey {target}')

            else:
                target = self.false_test_target
                # print(f'\t\tCurrent worry level is not divisible by {self.divisibility}')
                # print(f'\t\tItem with worry level {item} is thrown to monkey {target}')
            self.num_inspections += 1
            yield (item, target)

    def operate(self, item: int):
        tokens = self.operation_string.split(' ')
        if tokens[4] == '*':
            op = self.multiply
        elif tokens[4] == '+':
            op = self.plus
        else:
            raise Exception(f'Unhandled operation {self.operation_string}')

        a = item
        if tokens[5] == 'old':
            b = item
        else:
            b = int(tokens[5])

        new = op(a,b)
        # new = new//3
        # print(f'\t\tMonkey gets bored with item. Worry level is divided by 3 to {new}')
        return new

    @staticmethod
    def plus(a: int, b: int) -> int:
        # print(f'\t\tWorry level increases by {b} to {a + b}')
        return a + b

    @staticmethod
    def multiply(a: int, b: int) -> int:
        # print(f'\t\tWorry level is multiplied by {b} to {a * b}')
        return a * b

    def __str__(self):
        disp = ''
        disp += f'Monkey {self.id}\n'
        disp += f'\tItems: {self.items}\n'
        disp += f'\t{self.operation_string}\n'
        disp += f'\tTest: divisible by {self.divisibility}\n'
        disp += f'\t\tIf true: throw to monkey {self.true_test_target}\n'
        disp += f'\t\tIf false: throw to monkey {self.false_test_target}\n'
        return disp


def compute(s: str) -> int:

    monkey_defs = s.split('\n\n')

    monkeys : List[Monkey] = []

    for monkey_def in monkey_defs:
        lines = monkey_def.splitlines()

        monkey_num = lines[0].strip(':').split(' ')[1]
        monkey_items = []
        item_list = lines[1].strip().split(' ')[2:]
        for item in item_list:
            token = item.strip(', ')
            monkey_items.append(int(token))
        operation = lines[2].strip()
        divisibility = int(lines[3].strip().split(' ')[-1])
        true_test_target = int(lines[4].strip().split(' ')[-1])
        false_test_target = int(lines[5].strip().split(' ')[-1])

        monkey = Monkey(operation=operation,
            divisibility=divisibility,
            true_test_target=true_test_target,
            false_test_target=false_test_target,
            starting_items=monkey_items,
            monkey_id=monkey_num)

        monkeys.append(monkey)


    for i in range(20):
        # print(f'round {i+1}-----------')
        for monkey in monkeys:
            # print(f'Monkey {monkey.id}')
            for item, target in monkey.inspect():
                monkeys[target].add_item(item)

        # print(f'After round {i+1}')
        # for j, monkey in enumerate(monkeys):
            # print(f'Monkey {j}: {monkey.items}')

    # for monkey in monkeys:
        # print(f'monkey {monkey.id}: {monkey.num_inspections}')

    scores = []
    for monkey in monkeys:
        scores.append(monkey.num_inspections)
    scores.sort(reverse=True)
    mb = scores[0] * scores[1]
    # print(scores)

    # TODO: implement solution here!
    return mb


INPUT_S = '''\
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
'''
EXPECTED = 10605


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
