#!/usr/bin/env python3

import itertools
import unittest

def read_input(f):
    return list(map(int, f))

def get_matching_sum(nums, s, n):
    for i in itertools.combinations(nums, n):
        if sum(i) == s:
            return i
    return None

class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nums = [1721, 979, 366, 299, 675, 1456]

    def test_part1(self):
        a, b = get_matching_sum(self.nums, 2020, 2)
        self.assertEqual(a * b, 514579)

    def test_part2(self):
        a, b, c = get_matching_sum(self.nums, 2020, 3)
        self.assertEqual(a * b * c, 241861950)

if __name__ == '__main__':
    unittest.main(exit=False)
    with open('input.txt') as f:
        nums = read_input(f)
        
    a, b = get_matching_sum(nums, 2020, 2)
    print(a*b)

    a, b, c  = get_matching_sum(nums, 2020, 3)
    print(a*b*c)
