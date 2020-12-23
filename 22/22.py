#!/usr/bin/env python3

import copy
import itertools
import unittest
from collections import deque

def parse_input(f):
    decks = (deque(), deque())
    for i in range(2):
        next(f)
        for line in f:
            if line.isspace():
                break
            decks[i].append(int(line.rstrip()))
    return decks

def play_round(decks):
    cards = decks[0].popleft(), decks[1].popleft()
    assert(cards[0] != cards[1])
    if cards[0] > cards[1]:
        decks[0].append(cards[0])
        decks[0].append(cards[1])
    else:
        decks[1].append(cards[1])
        decks[1].append(cards[0])

def get_score(deck):
    return sum((len(deck)-i) * n for i, n in enumerate(deck))

def play_game(decks):
    while decks[0] and decks[1]:
        play_round(decks)
    return get_score(decks[0] if decks[0] else decks[1])

def copy_deck(deck, n):
    return deque(itertools.islice(deck, 0, n))

def play_round_recursive(decks):
    cards = decks[0].popleft(), decks[1].popleft()
    assert(cards[0] != cards[1])

    if len(decks[0]) >= cards[0] and len(decks[1]) >= cards[1]:
        new_decks = (copy_deck(decks[0], cards[0]), (copy_deck(decks[1], cards[1])))
        winner, _ = play_game_recursive(new_decks)
    else:
        winner = 0 if cards[0] > cards[1] else 1

    if winner == 0:
        decks[0].append(cards[0])
        decks[0].append(cards[1])
    else:
        decks[1].append(cards[1])
        decks[1].append(cards[0])

def play_game_recursive(decks):
    prev_rounds = set()
    winner = None

    while decks[0] and decks[1]:
        if (tuple(decks[0]), tuple(decks[1])) in prev_rounds:
            winner = 0
            break

        prev_rounds.add((tuple(decks[0]), tuple(decks[1])))
        play_round_recursive(decks)

    if winner is None:
        winner = 0 if decks[0] else 1
    return winner, get_score(decks[winner])

class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test1decks = (deque([9,2,6,3,1]), deque([5,8,4,7,10]))

    def test_parse_input(self):
        with open('test1.txt') as f:
            decks = parse_input(f)
        self.assertEqual(decks, self.test1decks)

    def test_play_round(self):
        decks = copy.deepcopy(self.test1decks)

        play_round(decks)
        self.assertEqual(decks, (deque([2,6,3,1,9,5]), deque([8,4,7,10])))

        play_round(decks)
        self.assertEqual(decks, (deque([6,3,1,9,5]), deque([4,7,10,8,2])))

    def test_play_game(self):
        decks = copy.deepcopy(self.test1decks)
        self.assertEqual(play_game(decks), 306)

    def test_play_game_recursive(self):
        with open('test2.txt') as f:
            decks = parse_input(f)
        self.assertEqual(play_game_recursive(decks), (0, 105))

        with open('test1.txt') as f:
            decks = parse_input(f)
        self.assertEqual(play_game_recursive(decks), (1, 291))

if __name__ == '__main__':
    unittest.main(exit=False)

    with open('input.txt') as f:
        decks = parse_input(f)

    print(play_game_recursive(decks))
