#!/usr/bin/env python3

import unittest

def parse_input(f):
    earliest_time = int(next(f).rstrip())
    buses = [int(bus) for bus in next(f).rstrip().split(',') if bus != 'x']
    return earliest_time, buses

def get_next_multiple(num, factor):
    return num + factor - num % factor

def get_next_bus(time, buses):
    next_multiples = {bus: get_next_multiple(time, bus) for bus in buses}
    return min(next_multiples.items(), key=lambda x: x[1])

class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test1earliest = 939
        cls.test1buses = [7, 13, 59, 31, 19]

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

if __name__ == '__main__':
    unittest.main(exit=False)

    with open('input.txt') as f:
        earliest, buses = parse_input(f)

    next_bus, next_time = get_next_bus(earliest, buses)
    print(next_bus * (next_time - earliest))
