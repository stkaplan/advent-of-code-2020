#!/usr/bin/env python3

import unittest

def parse_line(line):
    return list(map(lambda x: x == '#', line.rstrip()))

def read_input(f):
    return list(map(parse_line, f))

def count_trees(trees, right, down):
    width = len(trees[0])
    assert(all(len(row) == width for row in trees))
    return sum(trees[row][right*(i+1) % width] for i, row in enumerate(range(down, len(trees), down)))

class Test(unittest.TestCase):
    def test_count_trees(self):
        with open('test1.txt') as f:
            trees = read_input(f)
        self.assertEqual(count_trees(trees, 1, 1), 2)
        self.assertEqual(count_trees(trees, 3, 1), 7)
        self.assertEqual(count_trees(trees, 5, 1), 3)
        self.assertEqual(count_trees(trees, 7, 1), 4)
        self.assertEqual(count_trees(trees, 1, 2), 2)

        with open('input.txt') as f:
            trees = read_input(f)
        self.assertEqual(count_trees(trees, 3, 1), 205)

if __name__ == '__main__':
    unittest.main(exit=False)

    with open('input.txt') as f:
        trees = read_input(f)

    counts = ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2))
    product = 1
    for i, j in counts:
        product *= count_trees(trees, i, j)
    print(product)
