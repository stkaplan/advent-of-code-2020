#!/usr/bin/env python3

import itertools
import unittest
from collections import deque

def parse_input(f, preamble_size):
    preamble_lines = (next(f) for i in range(preamble_size))
    preamble = deque()
    for line in preamble_lines:
        preamble.append(int(line.rstrip()))

    sums = list(map(int, f))
    return preamble, sums

def is_sum(preamble, n):
    return any(a + b == n for a, b in itertools.combinations(preamble, 2) if a != b)

def find_invalid_sum(preamble, sums):
    for n in sums:
        if not is_sum(preamble, n):
            return n
        preamble.popleft()
        preamble.append(n)

class Test(unittest.TestCase):
    def test_is_sum(self):
        with open('test1.txt') as f:
            preamble, sums = parse_input(f, 5)
        for n in sums:
            self.assertEqual(is_sum(preamble, n), n != 127, f'n = {n}') # Only 127 should be False.
            preamble.popleft()
            preamble.append(n)

    def test_invalid_sum(self):
        with open('test1.txt') as f:
            preamble, sums = parse_input(f, 5)
        self.assertEqual(find_invalid_sum(preamble, sums), 127)

if __name__ == '__main__':
    unittest.main(exit=False)

    with open('input.txt') as f:
        preamble, sums = parse_input(f, 25)
    print(find_invalid_sum(preamble, sums))
