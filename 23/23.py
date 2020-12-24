#!/usr/bin/env python3

import unittest

def parse_input(s, n=None):
    nexts = {}
    for i in range(len(s)-1):
        nexts[int(s[i])] = int(s[i+1])

    if n is None:
        nexts[int(s[len(s)-1])] = int(s[0])
    else:
        last_supplied = int(s[-1])
        nexts[last_supplied] = len(s) + 1
        for i in range(len(s)+1, n):
            nexts[i] = i+1
        nexts[n] = int(s[0])
    return nexts, int(s[0])
    
def move_cups(nexts, current_cup):
    num_cups = 3

    moved = []
    next_moved = nexts[current_cup]
    for _ in range(num_cups):
        moved.append(next_moved)
        next_moved = nexts[next_moved]

    target = current_cup - 1
    if target == 0:
        target = len(nexts)
    while target in moved:
        target -= 1
        if target == 0:
            target = len(nexts)
    old_target_next = nexts[target]

    nexts[current_cup] = nexts[moved[-1]]
    nexts[target] = moved[0]
    nexts[moved[-1]] = old_target_next

def play_game(nexts, start, rounds):
    current_cup = start
    for _ in range(rounds):
        move_cups(nexts, current_cup)
        current_cup = nexts[current_cup]

def cups_after(nexts, start, n=None):
    if n is None:
        n = len(nexts) - 1

    after = []
    current = start
    for _ in range(n):
        current = nexts[current]
        after.append(current)
    return after

class Test(unittest.TestCase):
    def test_parse_input(self):
        nexts, start = parse_input('389125467')
        self.assertEqual(nexts, {3:8, 8:9, 9:1, 1:2, 2:5, 5:4, 4:6, 6:7, 7:3})
        self.assertEqual(start, 3)

        nexts, start = parse_input('389125467', 15)
        self.assertEqual(nexts, {3:8, 8:9, 9:1, 1:2, 2:5, 5:4, 4:6, 6:7, 7:10, 10:11, 11:12, 12:13, 13:14, 14:15, 15:3})
        self.assertEqual(start, 3)

    def test_move_cups(self):
        nexts, _ = parse_input('389125467')

        move_cups(nexts, 3)
        new_nexts, _ = parse_input('328915467')
        self.assertEqual(nexts, new_nexts)

        move_cups(nexts, 2)
        new_nexts, _ = parse_input('325467891')
        self.assertEqual(nexts, new_nexts)

        move_cups(nexts, 5)
        new_nexts, _ = parse_input('725891346')
        self.assertEqual(nexts, new_nexts)

    def test_cups_after(self):
        nexts, _ = parse_input('583741926')
        self.assertEqual(cups_after(nexts, 1), [9,2,6,5,8,3,7,4])

    def test_play_game(self):
        nexts, start = parse_input('389125467')
        play_game(nexts, start, 10)
        self.assertEqual(cups_after(nexts, 1), [9,2,6,5,8,3,7,4])

        nexts, start = parse_input('389125467')
        play_game(nexts, start, 100)
        self.assertEqual(cups_after(nexts, 1), [6,7,3,8,4,5,2,9])

    def test_part2_example(self):
        nexts, start = parse_input('389125467', 1000000)
        play_game(nexts, start, 10000000)
        self.assertEqual(cups_after(nexts, 1, 2), [934001, 159792])

if __name__ == '__main__':
    unittest.main(exit=False)

    input_ = '364289715'
    nexts, start = parse_input(input_, 1000000)
    play_game(nexts, start, 10000000)
    after = cups_after(nexts, 1, 2)
    print(after)
    print(after[0] * after[1])
