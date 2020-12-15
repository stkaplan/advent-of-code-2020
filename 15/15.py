#!/usr/bin/env python3

import itertools
import re
import unittest

def iterate(n, ages, turn):
    if n in ages:
        age = ages[n]
        if age[0] is None:
            said = 0
        else:
            said = age[1] - age[0]
        if said in ages:
            ages[said] = (ages[said][1], turn)
        else:
            ages[said] = (None, turn)
        return said
    else:
        ages[n] = (None, turn)
        return n

def memory_game(input_, max_turns):
    ages = {}
    turn = 1
    while turn <= max_turns:
        if turn <= len(input_):
            n = input_[turn-1]
        n = iterate(n, ages, turn)
        turn += 1
    return n

class Test(unittest.TestCase):
    def test_memory_game(self):
        expected = [0, 3, 6, 0, 3, 3, 1, 0, 4, 0]
        input_ = [0, 3, 6]
        for i, x in enumerate(expected):
            result = memory_game(input_, i+1)
            self.assertEqual(result, x, f'{i+1} turns')
        self.assertEqual(memory_game([0, 3, 6], 2020), 436)

        self.assertEqual(memory_game([1, 3, 2], 2020), 1)
        self.assertEqual(memory_game([2, 1, 3], 2020), 10)
        self.assertEqual(memory_game([1, 2, 3], 2020), 27)
        self.assertEqual(memory_game([2, 3, 1], 2020), 78)
        self.assertEqual(memory_game([3, 2, 1], 2020), 438)
        self.assertEqual(memory_game([3, 1, 2], 2020), 1836)

if __name__ == '__main__':
    unittest.main(exit=False)

    input_ = [1, 20, 8, 12, 0, 14]
    print(memory_game(input_, 2020))
