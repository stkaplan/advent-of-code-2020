#!/usr/bin/env python3

import unittest

def parse_line(line):
    return list(map(lambda x: x == '#', line.rstrip()))

def read_input(f):
    return list(map(parse_line, f))

def count_trees(trees):
    width = len(trees[0])
    assert(all(len(row) == width for row in trees))
    return sum(trees[row][3*row % width] for row in range(1, len(trees)))

class Test(unittest.TestCase):
    def test_part1(self):
        with open('test1.txt') as f:
            trees = read_input(f)
        self.assertEqual(count_trees(trees), 7)

if __name__ == '__main__':
    unittest.main(exit=False)

    with open('input.txt') as f:
        trees = read_input(f)
    print(count_trees(trees))
