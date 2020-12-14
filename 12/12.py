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
    def __init__(self, x=0, y=0, waypoint_x=10, waypoint_y=1):
        self.x = x
        self.y = y
        self.waypoint_x = waypoint_x
        self.waypoint_y = waypoint_y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y \
               and self.waypoint_x == other.waypoint_x and self.waypoint_y == other.waypoint_y

    def __repr__(self):
        return f'Ship({self.x}, {self.y}, {self.waypoint_x}, {self.waypoint_y})'

    def do_action(self, action):
        if action.type == ActionType.MOVE_FORWARD:
            self.x += self.waypoint_x * action.value
            self.y += self.waypoint_y * action.value
        elif action.type == ActionType.TURN_LEFT:
            assert(action.value % 90 == 0)
            amount = action.value // 90
            for _ in range(amount):
                self.waypoint_x, self.waypoint_y = -self.waypoint_y, self.waypoint_x
        elif action.type == ActionType.TURN_RIGHT:
            assert(action.value % 90 == 0)
            amount = action.value // 90
            for _ in range(amount):
                self.waypoint_x, self.waypoint_y = self.waypoint_y, -self.waypoint_x
        else:
            heading = headings[action.type]
            self.waypoint_x += heading[0] * action.value
            self.waypoint_y += heading[1] * action.value

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
            Ship(100, 10, 10, 1),
            Ship(100, 10, 10, 4),
            Ship(170, 38, 10, 4),
            Ship(170, 38, 4, -10),
            Ship(214, -72, 4, -10),
        ]

        ship = Ship()
        self.assertEqual(ship, Ship(0, 0, 10, 1))
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
