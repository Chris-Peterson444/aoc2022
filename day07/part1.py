from __future__ import annotations

import argparse
import os.path

import pytest

import support

import copy

from typing import Optional
from typing import List

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

class Node:

    def __init__(
        self,
        name: str,
        parent: Optional[Node] = None,
        is_dir : bool = False,
        size: int = 0,
        ) -> None:
        self.name = name
        self.parent = parent
        self.children : List[Node] = []
        self.is_dir = is_dir
        self.size = size

    def __repr__(self) -> str:
        if self.is_dir:
            return f'{self.name} (dir)'
        else:
            return f'{self.name} (file, size={self.size})'

    def add_child(self, child: Node) -> None:
        self.children.append(child)

    def has_child(self, child_name: str) -> bool:
        for child in self.children:
            if child.name == child_name:
                return True

        return False

    def get_child(self, child_name: str) -> bool:
        for child in self.children:
            if child.name == child_name:
                return child

        raise Exception(f'Child of {self.name!r} with name {child_name!r} not found.')

    def compute_size(self) -> int:
        size = 0
        for child in self.children:
            if child.is_dir:
                size += child.compute_size()
            else:
                size += child.size
        # print(f'{self}, cost: {size}')
        return size

def eligible(node: Node) -> bool:
    if not node.is_dir:
        return False
    cost = node.compute_size()
    # print(f'node: {node}; cost: {cost}')
    if cost <= 100000:
        return True
    else:
        return False


def dfs_checker(root: Node) -> List[Node]:
    eligible_children = []
    # print(f'Checking {root} children')
    for child in root.children:
        if eligible(child):
            eligible_children.append(child)
            
        eligible_children += dfs_checker(child)
    return eligible_children


def print_tree(root: Node, level: int = 0) -> None:
    indent = '  '*level
    if root.is_dir:
        print(f'{indent} - {root.name} (dir)')
    else:
        print(f'{indent} - {root.name} (file, size={root.size})')
    for child in root.children:
        print_tree(child, level+1)


def compute(s: str) -> int:

    tree_root = Node('root',is_dir=True)
    ptr = copy.copy(tree_root)

    lines = s.splitlines()

    while len(lines) > 0:
        line = lines.pop(0)
        # command
        if line[0] == '$':
            args = line.split()
            # cd
            if len(args) == 3:
                _, command, dir_name = args

                if dir_name == '..':
                    ptr = ptr.parent

                elif not ptr.has_child(dir_name):
                    child = Node(dir_name, parent=ptr, is_dir=True)
                    ptr.add_child(child)

                    ptr = child

                else:
                    ptr = ptr.get_child(dir_name)


            # ls
            elif len(args) == 2:
                children = []
                ls_line = ' '

                while ls_line[0] != '$' and len(lines) > 0:
                    ls_line = lines.pop(0)
                    children.append(ls_line)

                if ls_line[0] == '$':
                    children.pop(-1)
                    lines.insert(0, ls_line)

                for child in children:
                    info, name = child.split(' ')
                    if info == 'dir':
                        child_node = Node(name=name, parent=ptr, is_dir=True)
                        ptr.add_child(child_node)
                    else:
                        _size = int(info)
                        child_node = Node(name=name, parent=ptr, is_dir=False, size=_size)
                        ptr.add_child(child_node)
                
            else:
                raise Exception(f'unknown case for line: {line}')
    # print_tree(tree_root)
    target_children = dfs_checker(tree_root)
    # print('target children:')
    # for child in target_children:
    #     print(child.name)
    _sum = 0
    for node in target_children:
        _sum += node.compute_size()




    return _sum


INPUT_S = '''\
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
'''
EXPECTED = 95437


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
