#!/usr/bin/env python3

import unittest
from collections import namedtuple
from enum import IntEnum

Action = namedtuple('Action', ['type', 'value'])

class ActionType(IntEnum):
    MOVE_NORTH = 0 # Cardinal directions are in clockwise order.
    MOVE_EAST = 1
    MOVE_SOUTH = 2
    MOVE_WEST = 3
    TURN_LEFT = 4
    TURN_RIGHT = 5
    MOVE_FORWARD = 6

str_to_action = {
        'N': ActionType.MOVE_NORTH,
        'S': ActionType.MOVE_SOUTH,
        'E': ActionType.MOVE_EAST,
        'W': ActionType.MOVE_WEST,
        'L': ActionType.TURN_LEFT,
        'R': ActionType.TURN_RIGHT,
        'F': ActionType.MOVE_FORWARD,
}

def parse_action(line):
    return Action(str_to_action[line[0]], int(line.rstrip()[1:]))

def parse_input(f):
    return list(map(parse_action, f))

# North is +x, east is +y.
headings = {
    ActionType.MOVE_NORTH: (0, 1),
    ActionType.MOVE_EAST: (1, 0),
    ActionType.MOVE_SOUTH: (0, -1),
    ActionType.MOVE_WEST: (-1, 0),
}

class Ship:
    def __init__(self, x=0, y=0, heading=ActionType.MOVE_EAST):
        self.x = x
        self.y = y
        self.heading = heading

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.heading == other.heading

    def __repr__(self):
        return f'Ship({self.x}, {self.y}, {self.heading})'

    def move(self, heading, amount):
            self.x += heading[0] * amount
            self.y += heading[1] * amount

    def do_action(self, action):
        if action.type == ActionType.MOVE_FORWARD:
            self.move(headings[self.heading], action.value)
        elif action.type in [ActionType.TURN_LEFT, ActionType.TURN_RIGHT]:
            assert(action.value % 90 == 0)
            direction = 1 if action.type == ActionType.TURN_RIGHT else -1
            amount = action.value // 90
            self.heading += direction * amount
            self.heading %= 4
        else:
            self.move(headings[action.type], action.value)

class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test1actions = [
            Action(ActionType.MOVE_FORWARD, 10),
            Action(ActionType.MOVE_NORTH, 3),
            Action(ActionType.MOVE_FORWARD, 7),
            Action(ActionType.TURN_RIGHT, 90),
            Action(ActionType.MOVE_FORWARD, 11),
        ]

    def test_parse_input(self):
        with open('test1.txt') as f:
            actions = parse_input(f)
        self.assertEqual(actions, self.test1actions)

    def test_do_action(self):
        steps = [
            Ship(10, 0, ActionType.MOVE_EAST),
            Ship(10, 3, ActionType.MOVE_EAST),
            Ship(17, 3, ActionType.MOVE_EAST),
            Ship(17, 3, ActionType.MOVE_SOUTH),
            Ship(17, -8, ActionType.MOVE_SOUTH),
        ]

        ship = Ship()
        self.assertEqual(ship, Ship(0, 0, ActionType.MOVE_EAST))
        for action, pos in zip(self.test1actions, steps):
            ship.do_action(action)
            self.assertEqual(ship, pos)

if __name__ == '__main__':
    unittest.main(exit=False)

    with open('input.txt') as f:
        actions = parse_input(f)

    ship = Ship()
    for action in actions:
        ship.do_action(action)
    print(abs(ship.x) + abs(ship.y))
