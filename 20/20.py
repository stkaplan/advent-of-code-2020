#!/usr/bin/env python3

# This does a ton of duplicated work to find the assembled image: calculating
# tile rotations multiple times, etc. But it's fast enough for the input, so
# whatever. Today's problem is really tedious and not worth working on any
# further.

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

def get_edge_min(edge, length):
    return min(edge, reverse_edge(edge, length))

def rotated_clockwise(array):
    height = len(array)
    width = len(array[0])
    new_array = [[None] * height for _ in range(width)]
    for row in range(height):
        for col in range(width):
            new_array[col][row] = array[height - row - 1][col]
    return new_array

def flipped_y(array):
    return [list(reversed(row)) for row in array]

def get_orientation(array, orientation):
    if orientation == Orientation.NORMAL:
        return array
    elif orientation == Orientation.ROTATED_90:
        return rotated_clockwise(array)
    elif orientation == Orientation.ROTATED_180:
        return rotated_clockwise(rotated_clockwise(array))
    elif orientation == Orientation.ROTATED_270:
        return rotated_clockwise(rotated_clockwise(rotated_clockwise(array)))
    elif orientation == Orientation.FLIPPED:
        return flipped_y(array)
    elif orientation == Orientation.FLIPPED_ROTATED_90:
        return rotated_clockwise(flipped_y(array))
    elif orientation == Orientation.FLIPPED_ROTATED_180:
        return rotated_clockwise(rotated_clockwise(flipped_y(array)))
    elif orientation == Orientation.FLIPPED_ROTATED_270:
        return rotated_clockwise(rotated_clockwise(rotated_clockwise(flipped_y(array))))

class Tile:
    def __init__(self, image, tile_num):
        self.image = image
        self.tile_num = tile_num
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

    def get_orientation(self, orientation):
        return Tile(get_orientation(self.image, orientation), self.tile_num)

def parse_input(f):
    tiles = {}
    tile_num = None
    image = []
    for line in f:
        if line.isspace():
            tiles[tile_num] = Tile(image, tile_num)
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

# Shortcut: assume the picture edges are unique (can't be matched to any other
# edge). Then the corners are the only pieces with 2 unique edges, and the edge
# pieces have 1 unique edge.
def sort_tiles(tiles):
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
    return tiles_sorted, edge_counts

# We're filling in the image left to right, top to bottom. So we only need to
# check left and top neighbors.
def test_orientation(image, tiles, tile_num, orientation, x, y):
    tile_oriented = tiles[tile_num].get_orientation(orientation)

    if x != len(image)-1:
        assert(image[y][x+1] is None)
    if y != len(image)-1:
        assert(image[y+1][x] is None)

    if x != 0:
        assert(image[y][x-1] is not None)
        if image[y][x-1].right != tile_oriented.left:
            return None

    if y != 0:
        assert(image[y-1][x] is not None)
        if image[y-1][x].bottom != tile_oriented.top:
            return None

    return orientation, tile_oriented

def get_matching_orientation(image, tiles, tile_num, x, y):
    for orientation in Orientation:
        match = test_orientation(image, tiles, tile_num, orientation, x, y)
        if match is not None:
            return match

def check_for_matches(image, tiles, tile_set, x, y):
    for tile_num in tile_set:
        match = get_matching_orientation(image, tiles, tile_num, x, y)
        if match is not None:
            orientation, tile_oriented = match
            return tile_num, orientation, tile_oriented
    else:
        raise Exception(f'no matching tile for ({x}, {y})')

def fit_tile(image, tiles, tiles_sorted, x, y):
    if (x == 0 and y == 0) or (x == 0 and y == len(image)-1) or (x == len(image)-1 and y == 0) or (x == len(image)-1 and y == len(image)-1):
        relevant_tiles = tiles_sorted.corners
    elif x == 0 or x == len(image)-1 or y == 0 or y == len(image)-1:
        relevant_tiles = tiles_sorted.edges
    else:
        relevant_tiles = tiles_sorted.middle

    tile_num, orientation, tile_oriented = check_for_matches(image, tiles, relevant_tiles, x, y)
    relevant_tiles.remove(tile_num)
    image[y][x] = tile_oriented

def assemble_image(tiles):
    tiles_sorted, edge_counts = sort_tiles(tiles)
    length = int(math.sqrt(len(tiles)))
    image = [[None] * length for _ in range(length)]

    for y in range(length):
        for x in range(length):
            if x == 0 and y == 0:
                # Fit the first corner, in whichever orientation has unmatched edges on the top and left.
                tile_num = next(iter(tiles_sorted.corners))
                tile = tiles[tile_num]
                tiles_sorted.corners.remove(tile_num)
                for ori in Orientation:
                    tile_oriented = tile.get_orientation(ori)
                    if edge_counts[get_edge_min(tile_oriented.top, tile.length)] == 1 and edge_counts[get_edge_min(tile_oriented.left, tile.length)] == 1:
                        image[0][0] = tile_oriented
                        break
                else:
                    raise Exception('Could not fit tile (0,0)')
            else:
                fit_tile(image, tiles, tiles_sorted, x, y)

    return image

def combine_tiles(image):
    combined_image = []

    outer_length = len(image)
    inner_length = len(image[0][0].image)

    for y in range(outer_length):
        for i in range(1, inner_length-1):
            row = []
            for x in range(outer_length):
                row += image[y][x].image[i][1:-1]
            combined_image.append(row)

    return combined_image

sea_monster_str = [
    '                  # ',
    '#    ##    ##    ###',
    ' #  #  #  #  #  #   ',
]
sea_monster = [[c == '#' for c in s] for s in sea_monster_str]
sea_monster_height = len(sea_monster)
sea_monster_width = len(sea_monster[0])

def is_sea_monster(image, start_x, start_y):
    for y in range(sea_monster_height):
        for x in range(sea_monster_width):
            if sea_monster[y][x]:
                if not image[start_y+y][start_x+x]:
                    return False
    return True

def remove_sea_monster(image, start_x, start_y):
    for y in range(sea_monster_height):
        for x in range(sea_monster_width):
            if sea_monster[y][x]:
                image[start_y+y][start_x+x] = False

def remove_sea_monsters_with_orientation(image, orientation):
    image_length = len(image)
    image_oriented = get_orientation(image, orientation)
    changed = False

    for x in range(0, image_length - sea_monster_width):
        for y in range(0, image_length - sea_monster_height):
            if is_sea_monster(image_oriented, x, y):
                changed = True
                remove_sea_monster(image_oriented, x, y)
    if changed:
        return sum(sum(row) for row in image_oriented)
    else:
        return None

def get_roughness(image):
    # Test each orientation until we find one that had sea monsters.
    for orientation in Orientation:
        roughness = remove_sea_monsters_with_orientation(image, orientation)
        if roughness is not None:
            return roughness
    else:
        raise Exception('No sea monsters found in any orientation')

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
        ], 1234)
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
        rotated_90 = rotated_clockwise(tile.image)
        self.assertEqual(Tile(rotated_90, 0).as_image(), rotated_90_image)
        self.assertEqual(tile.get_orientation(Orientation.ROTATED_90).as_image(), rotated_90_image)

        rotated_180 = rotated_clockwise(rotated_90)
        rotated_180_image = '''\
#.#.
.#.#
..##
##..
'''
        self.assertEqual(Tile(rotated_180, 0).as_image(), rotated_180_image)
        self.assertEqual(tile.get_orientation(Orientation.ROTATED_180).as_image(), rotated_180_image)

        flipped = flipped_y(tile.image)
        flipped_image = '''\
##..
..##
.#.#
#.#.
'''
        self.assertEqual(Tile(flipped, 0).as_image(), flipped_image)
        self.assertEqual(tile.get_orientation(Orientation.FLIPPED).as_image(), flipped_image)

        flipped_rotated_270 = rotated_clockwise(rotated_clockwise(rotated_clockwise(flipped)))
        flipped_rotated_270_image = '''\
.##.
.#.#
#.#.
#..#
'''
        self.assertEqual(Tile(flipped_rotated_270, 0).as_image(), flipped_rotated_270_image)
        self.assertEqual(tile.get_orientation(Orientation.FLIPPED_ROTATED_270).as_image(), flipped_rotated_270_image)

    def test_sort_image(self):
        with open('test1.txt') as f:
            tiles = parse_input(f)

        tiles_sorted, _ = sort_tiles(tiles)
        self.assertEqual(set(tiles_sorted.corners), set((1951, 3079, 2971, 1171)))

    @staticmethod
    def read_image(f):
        return [[c == '#' for c in line.rstrip()] for line in f]

    def test_assemble_image(self):
        with open('test1.txt') as f:
            tiles = parse_input(f)

        image = assemble_image(tiles)
        combined = combine_tiles(image)

        tiles_sorted, _ = sort_tiles(tiles)
        corners = [t.tile_num for t in (image[0][0], image[0][-1], image[-1][-1], image[-1][0])]
        self.assertEqual(set(corners), tiles_sorted.corners)

        with open('test_combined_image.txt') as f:
            expected_image = self.read_image(f)

        self.assertTrue(any(get_orientation(combined, ori) == expected_image for ori in Orientation))

    def test_is_sea_monster(self):
        with open('test_combined_image.txt') as f:
            image = self.read_image(f)

        image_oriented = get_orientation(image, Orientation.FLIPPED_ROTATED_270)
        for y in range(len(image) - sea_monster_height):
            for x in range(len(image) - sea_monster_width):
                self.assertEqual(is_sea_monster(image_oriented, x, y), (x, y) in ((2, 2), (1, 16)))

    def test_remove_sea_monsters(self):
        with open('test_combined_image.txt') as f:
            combined = self.read_image(f)

        expected = [None, None, None, None, None, None, None, 273]
        for ori, exp in zip(Orientation, expected):
            self.assertEqual(remove_sea_monsters_with_orientation(combined, ori), exp, ori)

    def test_get_roughness(self):
        with open('test_combined_image.txt') as f:
            combined = self.read_image(f)
        self.assertEqual(get_roughness(combined), 273)

        with open('test1.txt') as f:
            tiles = parse_input(f)

        image = assemble_image(tiles)
        test1 = combine_tiles(image)
        self.assertEqual(get_roughness(test1), 273)

if __name__ == '__main__':
    unittest.main(exit=False)

    with open('input.txt') as f:
        tiles = parse_input(f)

    image = assemble_image(tiles)
    combined = combine_tiles(image)
    print(get_roughness(combined))
