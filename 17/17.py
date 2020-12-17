#!/usr/bin/env python3

import unittest

def parse_input(f):
    cells = set()
    for y, line in enumerate(f):
        for x, c in enumerate(line.rstrip()):
            if c == '#':
                cells.add((x, y, 0, 0))
    return cells

active_min_neighbors = 2
active_max_neighbors = 3
inactive_neighbors = 3

def should_activate(cells, x, y, z, w):
    current = (x, y, z, w) in cells
    count = 0
    for xx in range(x-1, x+2):
        for yy in range(y-1, y+2):
            for zz in range(z-1, z+2):
                for ww in range(w-1, w+2):
                    if (xx, yy, zz, ww) == (x, y, z, w): # Skip current cell.
                        continue
                    if (xx, yy, zz, ww) in cells:
                        count += 1

                # Early return if too many neighbors are active.
                if count > (active_max_neighbors if current else inactive_neighbors):
                    return False

    if current:
        return count >= active_min_neighbors and count <= active_max_neighbors
    else:
        return count == inactive_neighbors

def iterate(cells):
    min_x = None
    max_x = None
    min_y = None
    max_y = None
    min_z = None
    max_z = None
    min_w = None
    max_w = None

    for x, y, z, w in cells:
        if min_x is None or x < min_x:
            min_x = x
        if max_x is None or x > max_x:
            max_x = x
        if min_y is None or y < min_y:
            min_y = y
        if max_y is None or y > max_y:
            max_y = y
        if min_z is None or z < min_z:
            min_z = z
        if max_z is None or z > max_z:
            max_z = z
        if min_w is None or w < min_w:
            min_w = w
        if max_w is None or w > max_w:
            max_w = w

    new_cells = set()
    for x in range(min_x-1, max_x+2):
        for y in range(min_y-1, max_y+2):
            for z in range(min_z-1, max_z+2):
                for w in range(min_w-1, max_w+2):
                    if should_activate(cells, x, y, z, w):
                        new_cells.add((x, y, z, w))

    return new_cells

class Test(unittest.TestCase):
    def test_iterate(self):
        with open('test1.txt') as f:
            cells = parse_input(f)
        self.assertEqual(cells, set([(1, 0, 0, 0), (2, 1, 0, 0), (0, 2, 0, 0), (1, 2, 0, 0), (2, 2, 0, 0)]))

        cells = iterate(cells) # Cycle 1
        self.assertEqual(len(cells), 29)

        cells = iterate(cells) # Cycle 2
        self.assertEqual(len(cells), 60)

        for _ in range(4): # Skip to cycle 6
            cells = iterate(cells)
        self.assertEqual(len(cells), 848)

if __name__ == '__main__':
    unittest.main(exit=False)

    with open('input.txt') as f:
        cells = parse_input(f)

    for _ in range(6):
        cells = iterate(cells)
    print(len(cells))
