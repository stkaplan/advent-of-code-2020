#!/usr/bin/env python3

import itertools
import unittest

def read_input(f):
    return list(map(int, f))

def get_matching_sum(nums, sum):
    for a, b in itertools.combinations(nums, 2):
        if a + b == sum:
            return (a, b)
    return None

class Test(unittest.TestCase):
    def test_part1(self):
        nums = [1721, 979, 366, 299, 675, 1456]
        a, b = get_matching_sum(nums, 2020)
        self.assertEqual(a * b, 514579)

if __name__ == '__main__':
    unittest.main(exit=False)
    with open('input.txt') as f:
        nums = read_input(f)
        
    a, b = get_matching_sum(nums, 2020)
    print(a*b)
