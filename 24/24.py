#!/usr/bin/env python3

import unittest
from collections import namedtuple
from enum import Enum

Point = namedtuple('Point', ['x', 'y'])
class Color(Enum):
    WHITE = 0
    BLACK = 1

def split_tokens(s):
    i = 0
    while i < len(s):
        c = s[i]
        i += 1
        if c == 'n' or c == 's':
            c2 = s[i]
            i += 1
            yield c + c2
        else:
            yield c

def parse_line(line):
    return list(split_tokens(line.rstrip()))

def parse_input(f):
    return list(map(parse_line, f))

# Hex grid looks like this:
# Rows/columns like normal grid, except half the spaces are empty.
# x x x x x x x x
#  x x x G B x x x
# x x x F A C x x
#  x x x E D x x x
# x x x x x x x x
#
# A = (0,0)
# C = (2,0)   F = (-2,0)
# B = (1,1)   D = (1,-1)
# E = (-1,-1) G = (-1,1)

def get_neighbor_point(point, direction):
    if direction == 'e':
        return Point(point.x + 2, point.y)
    elif direction == 'w':
        return Point(point.x - 2, point.y)
    elif direction == 'ne':
        return Point(point.x + 1, point.y + 1)
    elif direction == 'nw':
        return Point(point.x - 1, point.y + 1)
    elif direction == 'se':
        return Point(point.x + 1, point.y - 1)
    elif direction == 'sw':
        return Point(point.x - 1, point.y - 1)

def get_point(steps):
    point = Point(0, 0)
    for step in steps:
        point = get_neighbor_point(point, step)
    return point

def get_black_tiles(step_lists):
    black_tiles = set()
    for step_list in step_lists:
        point = get_point(step_list)
        if point in black_tiles:
            black_tiles.remove(point)
        else:
            black_tiles.add(point)
    return black_tiles

def get_all_neighbors(point):
    return [get_neighbor_point(point, d) for d in ('e', 'w', 'ne', 'nw', 'se', 'sw')]

def get_tile_color(tiles, point):
    try:
        return tiles[point]
    except KeyError:
        return Color.WHITE

def flip_tiles(tiles):
    # Add all neighbors to the list of points we're considering.
    missing_neighbors = []
    for point, color in tiles.items():
        if color == Color.BLACK:
            for neighbor in get_all_neighbors(point):
                if neighbor not in tiles:
                    missing_neighbors.append(neighbor)
    for neighbor in missing_neighbors:
        tiles[neighbor] = Color.WHITE

    new_tiles = {}
    for point, color in tiles.items():
        black_neighbors = sum(get_tile_color(tiles, neighbor) == Color.BLACK for neighbor in get_all_neighbors(point))
        if color == Color.BLACK:
            new_tiles[point] = Color.WHITE if black_neighbors == 0 or black_neighbors > 2 else Color.BLACK
        else:
            new_tiles[point] = Color.BLACK if black_neighbors == 2 else Color.WHITE
    return new_tiles

def count_black_tiles(tiles):
    return sum(color == Color.BLACK for color in tiles.values())

class Test(unittest.TestCase):
    def test_parse_input(self):
        line = 'esenee\n'
        self.assertEqual(parse_line(line), ['e', 'se', 'ne', 'e'])

        with open('test1.txt') as f:
            step_lists = parse_input(f)
        self.assertEqual(len(step_lists), 20)
        self.assertEqual(step_lists[0], ['se', 'se', 'nw', 'ne', 'ne', 'ne', 'w', 'se', 'e', 'sw', 'w', 'sw', 'sw', 'w', 'ne', 'ne', 'w', 'se', 'w', 'sw'])
        self.assertEqual(step_lists[-1], ['w', 'se', 'w', 'e', 'e', 'e', 'nw', 'ne', 'se', 'nw', 'w', 'w', 'sw', 'ne', 'w'])

    def test_get_point(self):
        steps = ['e', 'se', 'ne', 'e']
        self.assertEqual(get_point(steps), Point(6,0))

    def test_get_black_tiles(self):
        with open('test1.txt') as f:
            step_lists = parse_input(f)
        black_tiles = get_black_tiles(step_lists)
        self.assertEqual(len(black_tiles), 10)

    def test_flip_tiles(self):
        with open('test1.txt') as f:
            step_lists = parse_input(f)
        black_tiles = get_black_tiles(step_lists)
        tiles = {point: Color.BLACK for point in black_tiles}
        self.assertEqual(count_black_tiles(tiles), 10)

        tiles = flip_tiles(tiles)
        self.assertEqual(count_black_tiles(tiles), 15)
        tiles = flip_tiles(tiles)
        self.assertEqual(count_black_tiles(tiles), 12)
        tiles = flip_tiles(tiles)
        self.assertEqual(count_black_tiles(tiles), 25)
        tiles = flip_tiles(tiles)
        self.assertEqual(count_black_tiles(tiles), 14)
        tiles = flip_tiles(tiles)
        self.assertEqual(count_black_tiles(tiles), 23)

        for _ in range(5):
            tiles = flip_tiles(tiles)
        self.assertEqual(count_black_tiles(tiles), 37)

        for _ in range(90):
            tiles = flip_tiles(tiles)
        self.assertEqual(count_black_tiles(tiles), 2208)


if __name__ == '__main__':
    unittest.main(exit=False)

    with open('input.txt') as f:
        step_lists = parse_input(f)
    black_tiles = get_black_tiles(step_lists)
    tiles = {point: Color.BLACK for point in black_tiles}
    for _ in range(100):
        tiles = flip_tiles(tiles)
    print(count_black_tiles(tiles))
