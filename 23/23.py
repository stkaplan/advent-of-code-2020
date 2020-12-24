#!/usr/bin/env python3

import unittest

def parse_input(s):
    return list(map(int, s))

def pop_next_cups(cups, start, num_cups):
    popped = cups[start:start+num_cups]
    del cups[start:start+num_cups]

    if len(popped) < num_cups:
        remaining = num_cups - len(popped)
        popped += cups[0:remaining]
        del cups[0:remaining]

    return popped

def insert_cups(cups, moved, start):
    for i, cup in enumerate(moved):
        cups.insert(start+i, cup)
    
def move_cups(cups, current_index):
    num_cups = 3
    
    current_cup = cups[current_index]
    popped = pop_next_cups(cups, current_index+1, num_cups)

    target = current_cup - 1
    if target == 0:
        target = max(cups)
    while True:
        try:
            dest = cups.index(target) + 1
            break
        except ValueError:
            target -= 1
            if target == 0:
                target = max(cups)

    insert_cups(cups, popped, dest)

def play_game(cups, rounds):
    index = 0
    for _ in range(rounds):
        current_cup = cups[index]
        move_cups(cups, index)

        # The cups have been scrambled, so find where the current one ended up.
        index = cups.index(current_cup)
        index = (index + 1) % len(cups)

def cups_after(cups, n):
    start = cups.index(n)
    return cups[start+1:] + cups[0:start]

class Test(unittest.TestCase):
    def test_pop_next_cups(self):
        starting_cups = parse_input('389125467')
        
        cups = starting_cups.copy()
        popped = pop_next_cups(cups, 0, 3)
        self.assertEqual(cups, [1,2,5,4,6,7])
        self.assertEqual(popped, [3,8,9])

        cups = starting_cups.copy()
        popped = pop_next_cups(cups, 3, 3)
        self.assertEqual(cups, [3,8,9,4,6,7])
        self.assertEqual(popped, [1,2,5])

        cups = starting_cups.copy()
        popped = pop_next_cups(cups, 6, 3)
        self.assertEqual(cups, [3,8,9,1,2,5])
        self.assertEqual(popped, [4,6,7])

        cups = starting_cups.copy()
        popped = pop_next_cups(cups, 8, 3)
        self.assertEqual(cups, [9,1,2,5,4,6])
        self.assertEqual(popped, [7,3,8])

    def test_insert_cups(self):
        cups = [3,2,5,4,6,7]
        moved = [8,9,1]
        insert_cups(cups, moved, 2)
        self.assertEqual(cups, [3,2,8,9,1,5,4,6,7])

        cups = [3,2,5,4,6,7]
        moved = [8,9,1]
        insert_cups(cups, moved, 6)
        self.assertEqual(cups, [3,2,5,4,6,7,8,9,1])

    def test_move_cups(self):
        cups = parse_input('389125467')
        move_cups(cups, 0)
        self.assertEqual(cups, [3,2,8,9,1,5,4,6,7])
        move_cups(cups, 1)
        self.assertEqual(cups, [3,2,5,4,6,7,8,9,1])
        move_cups(cups, 2)
        self.assertEqual(cups, [3,4,6,7,2,5,8,9,1])

    def test_cups_after(self):
        cups = [5,8,3,7,4,1,9,2,6]
        self.assertEqual(cups_after(cups, 1), [9,2,6,5,8,3,7,4])

    def test_play_game(self):
        cups = parse_input('389125467')
        play_game(cups, 10)
        self.assertEqual(cups_after(cups, 1), [9,2,6,5,8,3,7,4])

        cups = parse_input('389125467')
        play_game(cups, 100)
        self.assertEqual(cups_after(cups, 1), [6,7,3,8,4,5,2,9])

if __name__ == '__main__':
    unittest.main(exit=False)

    input_ = '364289715'
    cups = parse_input(input_)
    play_game(cups, 100)
    print(str.join('', map(str, cups_after(cups, 1))))
