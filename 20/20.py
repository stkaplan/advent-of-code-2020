#!/usr/bin/env python3

import functools
import itertools
import math
import operator
import unittest
from collections import namedtuple
from enum import IntEnum

class Orientation(IntEnum):
    NORMAL = 0
    ROTATED_90 = 1
    ROTATED_180 = 2
    ROTATED_270 = 3
    FLIPPED = 4
    FLIPPED_ROTATED_90 = 5
    FLIPPED_ROTATED_180 = 6
    FLIPPED_ROTATED_270 = 7

def canonicalize_edge(edge):
    return sum(bit << i for i, bit in enumerate(edge))

def reverse_edge(edge, length):
    rev = 0
    for i in range(length):
        if edge & 1:
            rev += 1 << (length-i-1)
        edge >>= 1
    return rev

def edge_matches(edge1, edge2, length):
    if edge1 == edge2:
        return True
    else:
        return edge1 == reverse_edge(edge2, length)

class Tile:
    def __init__(self, image):
        self.image = image
        self.top = canonicalize_edge(image[0])
        self.bottom = canonicalize_edge(image[-1])
        self.left = canonicalize_edge([row[0] for row in image])
        self.right = canonicalize_edge([row[-1] for row in image])
        self.length = len(image[0])

    def edges(self):
        return [self.top, self.bottom, self.left, self.right]

    def as_image(self):
        def row_as_line(row):
            return ''.join('#' if x else '.' for x in row) + '\n'
        return ''.join(row_as_line(row) for row in self.image)

    def rotated_clockwise(self):
        image = [[False] * self.length for _ in range(self.length)]
        for x in range(self.length):
            for y in range(self.length):
                image[y][x] = self.image[self.length - x - 1][y]
        return Tile(image)

    def flipped_y(self):
        image = [list(reversed(row)) for row in self.image]
        return Tile(image)

    def get_orientation(self, orientation):
        if orientation == Orientation.NORMAL:
            return self
        elif orientation == Orientation.ROTATED_90:
            return self.rotated_clockwise()
        elif orientation == Orientation.ROTATED_180:
            return self.rotated_clockwise().rotated_clockwise()
        elif orientation == Orientation.ROTATED_270:
            return self.rotated_clockwise().rotated_clockwise().rotated_clockwise()
        elif orientation == Orientation.FLIPPED:
            return self.flipped_y()
        elif orientation == Orientation.FLIPPED_ROTATED_90:
            return self.flipped_y().rotated_clockwise()
        elif orientation == Orientation.FLIPPED_ROTATED_180:
            return self.flipped_y().rotated_clockwise().rotated_clockwise()
        elif orientation == Orientation.FLIPPED_ROTATED_270:
            return self.flipped_y().rotated_clockwise().rotated_clockwise().rotated_clockwise()

def parse_input(f):
    tiles = {}
    tile_num = None
    image = []
    for line in f:
        if line.isspace():
            tiles[tile_num] = Tile(image)
            tile_num = None
            image = []
        elif tile_num is None:
            tile_num = int(''.join(itertools.takewhile(str.isdigit, line.split()[1])))
        else:
            image.append([c == '#' for c in line.rstrip()])
    
    # Blank line at end of input, so no need to add final tile.
    assert(not image)
    return tiles

TilesSorted = namedtuple('TilesSorted', ['corners', 'edges', 'middle'])
TileInImage = namedtuple('TileInImage', ['tile_num', 'orientation'])

# Shortcut: assume there's a single way the picture can be recreated, and the
# picture edges are unique (can't be matched to any other edge). Then the
# corners are the only pieces with 2 unique edges, and the edge pieces have 1
# unique edge.
def sort_tiles(tiles):
    def get_edge_min(edge, length):
        return min(edge, reverse_edge(edge, length))

    tiles_sorted = TilesSorted(set(), set(), set())

    edge_counts = {}
    for tile in tiles.values():
        for edge in tile.edges():
            edge_min = get_edge_min(edge, tile.length)
            if edge_min not in edge_counts:
                edge_counts[edge_min] = 1
            else:
                edge_counts[edge_min] += 1

    assert(all(e in (1,2) for e in edge_counts.values()))

    # If a tile has 2 edges that can't be matched, it must be a corner.
    for tile_num, tile in tiles.items():
        unmatched_edges = sum(edge_counts[get_edge_min(e, tile.length)] == 1 for e in tile.edges())
        if unmatched_edges == 0:
            tiles_sorted.middle.add(tile_num)
        elif unmatched_edges == 1:
            tiles_sorted.edges.add(tile_num)
        elif unmatched_edges == 2:
            tiles_sorted.corners.add(tile_num)

    assert(len(tiles_sorted.corners) == 4)
    # N-1 pieces on each edge, but subtract out the 4 corner pieces.
    assert(len(tiles_sorted.edges) == (math.sqrt(len(tiles))-1) * 4 - 4)
    assert(len(tiles_sorted.middle) == (math.sqrt(len(tiles))-2) ** 2)
    return tiles_sorted

# We're filling in the image left to right, top to bottom. So we only need to
# check left and top neighbors.
def tile_matches(image, tile, x, y):
    match = True
    orientation = None

    # First figure out if we match the left neighbor (unless we're on the left edge).
    if x != 0:
        pass

    return orientation

def fit_tile(image, tiles_sorted, x, y):
    if (x == 0 and y == 0) or (x == 0 and y == len(image)-1) or (x == len(image)-1 and y == 0) or (x == len(image)-1 and y == len(image)-1):
        # Corner
        pass
    elif x == 0 or x == len(image)-1 or y == 0 or y == len(image)-1:
        # Edge
        pass
    else:
        # Middle
        pass
    pass

def assemble_image(tiles):
    tiles_sorted = sort_tiles(tiles)
    length = int(math.sqrt(tiles))
    image = [[[None] * length] for _ in range(length)]

    for x in range(length):
        for y in range(length):
            fit_tile(image, tiles_sorted, x, y)

class Test(unittest.TestCase):
    def test_reverse_edge(self):
        edge = 0b001100010
        self.assertEqual(reverse_edge(edge, 9), 0b010001100)

    def test_rotate_and_flip(self):
        tile = Tile([
            [False, False, True, True],
            [True, True, False, False],
            [True, False, True, False],
            [False, True, False, True],
        ])
        tile_image = '''\
..##
##..
#.#.
.#.#
'''
        self.assertEqual(tile.as_image(), tile_image)
        self.assertEqual(tile.get_orientation(Orientation.NORMAL).as_image(), tile_image)

        rotated_90_image = '''\
.##.
#.#.
.#.#
#..#
'''
        rotated_90 = tile.rotated_clockwise()
        self.assertEqual(rotated_90.as_image(), rotated_90_image)
        self.assertEqual(tile.get_orientation(Orientation.ROTATED_90).as_image(), rotated_90_image)

        rotated_180 = rotated_90.rotated_clockwise()
        rotated_180_image = '''\
#.#.
.#.#
..##
##..
'''
        self.assertEqual(rotated_180.as_image(), rotated_180_image)
        self.assertEqual(tile.get_orientation(Orientation.ROTATED_180).as_image(), rotated_180_image)

        flipped = tile.flipped_y()
        flipped_image = '''\
##..
..##
.#.#
#.#.
'''
        self.assertEqual(flipped.as_image(), flipped_image)
        self.assertEqual(tile.get_orientation(Orientation.FLIPPED).as_image(), flipped_image)

        flipped_rotated_270 = flipped.rotated_clockwise().rotated_clockwise().rotated_clockwise()
        flipped_rotated_270_image = '''\
.##.
.#.#
#.#.
#..#
'''
        self.assertEqual(flipped_rotated_270.as_image(), flipped_rotated_270_image)
        self.assertEqual(tile.get_orientation(Orientation.FLIPPED_ROTATED_270).as_image(), flipped_rotated_270_image)

    def test_sort_image(self):
        with open('test1.txt') as f:
            tiles = parse_input(f)

        tiles_sorted = sort_tiles(tiles)
        self.assertEqual(set(tiles_sorted.corners), set((1951, 3079, 2971, 1171)))

if __name__ == '__main__':
    unittest.main(exit=False)

    with open('input.txt') as f:
        tiles = parse_input(f)

    tiles_sorted = sort_tiles(tiles)
    print(functools.reduce(operator.mul, tiles_sorted.corners, 1))
