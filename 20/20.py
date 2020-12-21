#!/usr/bin/env python3

import functools
import itertools
import operator
import unittest

class Tile:
    def __init__(self, top, bottom, left, right):
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right
        self.permutations = None

    def edges(self):
        return [self.top, self.bottom, self.left, self.right]

    def __eq__(self, other):
        return self.edges() == other.edges()

    @classmethod
    def from_image(cls, image):
        top = image[0]
        bottom = image[-1]
        left = [row[0] for row in image]
        right = [row[-1] for row in image]
        return cls(top, bottom, left, right)

def parse_input(f):
    tiles = {}
    tile_num = None
    image = []
    for line in f:
        if line.isspace():
            tiles[tile_num] = Tile.from_image(image)
            tile_num = None
            image = []
        elif tile_num is None:
            tile_num = int(''.join(itertools.takewhile(str.isdigit, line.split()[1])))
        else:
            image.append([c == '#' for c in line.rstrip()])
    
    # Blank line at end of input, so no need to add final tile.
    assert(not image)
    return tiles

def canonicalize_edge(edge):
    edge_forwards = sum(bit << i for i, bit in enumerate(edge))
    edge_backwards = sum(bit << i for i, bit in enumerate(reversed(edge)))
    return min(edge_forwards, edge_backwards)

# Shortcut: assume there's a single way the picture can be recreated, and the
# picture edges are unique (can't be matched to any other edge). Then the
# corners are the only pieces with 2 unique edges.
def find_corners(tiles):
    edge_counts = {}
    for tile in tiles.values():
        for edge in tile.edges():
            edge_int = canonicalize_edge(edge)
            if edge_int not in edge_counts:
                edge_counts[edge_int] = 1
            else:
                edge_counts[edge_int] += 1

    assert(all(e in (1,2) for e in edge_counts.values()))

    # If a tile has 2 edges that can't be matched, it must be a corner.
    corners = []
    for tile_num, tile in tiles.items():
        unmatched_edges = sum(edge_counts[canonicalize_edge(e)] == 1 for e in tile.edges())
        if unmatched_edges == 2:
            corners.append(tile_num)

    assert(len(corners) == 4)
    return corners

class Test(unittest.TestCase):
    def test_find_corners(self):
        with open('test1.txt') as f:
            tiles = parse_input(f)

        corners = find_corners(tiles)
        self.assertEqual(set(corners), set((1951, 3079, 2971, 1171)))

if __name__ == '__main__':
    unittest.main(exit=False)

    with open('input.txt') as f:
        tiles = parse_input(f)

    corners = find_corners(tiles)
    print(functools.reduce(operator.mul, corners, 1))
