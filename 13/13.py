#!/usr/bin/env python3

import functools
import itertools
import math
import operator
import unittest

def parse_input(f):
    earliest_time = int(next(f).rstrip())
    buses = [int(bus) if bus != 'x' else 'x' for bus in next(f).rstrip().split(',')]
    return earliest_time, buses

def get_next_multiple(num, factor):
    return num + factor - num % factor

def get_next_bus(time, buses):
    next_multiples = {bus: get_next_multiple(time, bus) for bus in buses if bus != 'x'}
    return min(next_multiples.items(), key=lambda x: x[1])

# I have no idea what to call this for part 2: when all the buses leave at consecutive timestamps.
# This uses the Chinese Remainer Theorem, which I hope they didn't expect us to derive on our own.
def get_bus_serendipity(buses):
    mods = [(bus-i, bus) for i, bus in enumerate(buses) if bus != 'x']
    real_buses = [bus for bus in buses if bus != 'x']
    M = functools.reduce(operator.mul, real_buses)

    def get_term(a, m):
        b = M // m
        b_inv = b**(m-2) % m # Magic
        return a * b * b_inv
    return sum(get_term(mod[0], mod[1]) for mod in mods) % M

class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test1earliest = 939
        cls.test1buses = [7, 13, 'x', 'x', 59, 'x', 31, 19]

    def test_parse_input(self):
        with open('test1.txt') as f:
            earliest, buses = parse_input(f)
        self.assertEqual(earliest, self.test1earliest)
        self.assertEqual(buses, self.test1buses)

    def test_get_next_multiple(self):
        self.assertEqual(get_next_multiple(7, 3), 9)
        self.assertEqual(get_next_multiple(7, 10), 10)
        self.assertEqual(get_next_multiple(78, 10), 80)
        self.assertEqual(get_next_multiple(939, 59), 944)

    def test_get_next_bus(self):
        self.assertEqual(get_next_bus(self.test1earliest, self.test1buses), (59, 944))

    def test_get_bus_serendipity(self):
        #self.assertEqual(get_bus_serendipity([7, 13, 'x', 'x', 59, 'x', 31, 19]), 1068781)
        self.assertEqual(get_bus_serendipity([5, 7]), 20)
        self.assertEqual(get_bus_serendipity([5, 'x', 7]), 5)
        self.assertEqual(get_bus_serendipity([17, 'x', 13, 19]), 3417)
        self.assertEqual(get_bus_serendipity([67, 7, 59, 61]), 754018)
        self.assertEqual(get_bus_serendipity([67, 'x', 7, 59, 61]), 779210)
        self.assertEqual(get_bus_serendipity([67, 7, 'x', 59, 61]), 1261476)
        self.assertEqual(get_bus_serendipity([1789, 37, 47, 1889]), 1202161486)

if __name__ == '__main__':
    unittest.main(exit=False)

    with open('input.txt') as f:
        _, buses = parse_input(f)

    print(get_bus_serendipity(buses))
