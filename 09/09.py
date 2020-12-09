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

def find_contiguous_sum(ns, target):
    for start in range(len(ns)):
        for end in range(start+1, len(ns)):
            slice_ = ns[start:end+1]
            sum_ = sum(slice_)
            if sum_ == target:
                return slice_ # Found it.
            elif sum_ > target:
                break # Sum is too large, no need to continue with this starting index.

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

    def test_find_contiguous_sum(self):
        with open('test1.txt') as f:
            _, sums = parse_input(f, 0)
        sum_range = find_contiguous_sum(sums, 127)
        self.assertEqual(min(sum_range), 15)
        self.assertEqual(max(sum_range), 47)

if __name__ == '__main__':
    unittest.main(exit=False)

    with open('input.txt') as f:
        preamble, sums = parse_input(f, 25)
    invalid_sum = find_invalid_sum(preamble, sums)
    ns = list(preamble) + sums
    slice_ = find_contiguous_sum(ns, invalid_sum)
    print(min(slice_) + max(slice_))
