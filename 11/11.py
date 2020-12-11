#!/usr/bin/env python3

import copy
import unittest
from enum import IntEnum

class Seat(IntEnum):
    FLOOR = 0
    EMPTY = 1
    OCCUPIED = 2

str_to_seat = {
        '.': Seat.FLOOR,
        'L': Seat.EMPTY,
        '#': Seat.OCCUPIED,
}

def parse_line(line):
    return [str_to_seat[c] for c in line.rstrip()]

def parse_input(f):
    return list(map(parse_line, f))

neighbors = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1), (0, 1),
    (1, -1), (1, 0), (1, 1),
]

def is_occupied(seats, row_init, col_init, dir_row, dir_col):
    i = 1
    while True:
        row = row_init + i * dir_row
        col = col_init + i * dir_col
        if row < 0 or col < 0:
            return False
        if row >= len(seats) or col >= len(seats[0]):
            return False
        if seats[row][col] != Seat.FLOOR:
            return seats[row][col] == Seat.OCCUPIED
        i += 1

def get_new_seat_state(seats, row, col):
    seat = seats[row][col]
    if seat != Seat.FLOOR:
        if seat == Seat.EMPTY:
            if all(not is_occupied(seats, row, col, dir_row, dir_col) for dir_row, dir_col in neighbors):
                return Seat.OCCUPIED
        elif seat == Seat.OCCUPIED:
            if sum(is_occupied(seats, row, col, dir_row, dir_col) for dir_row, dir_col in neighbors) >= 5:
                return Seat.EMPTY
    return seat

def iterate(seats):
    seats_new = [[Seat.FLOOR for col in range(len(seats[0]))] for row in range(len(seats))]
    for row in range(len(seats)):
        for col in range(len(seats[0])):
            seats_new[row][col] = get_new_seat_state(seats, row, col)
    return seats_new

def converge(seats):
    while True:
        seats_new = iterate(seats)
        if seats_new == seats:
            return seats_new
        seats = seats_new

def count_occupied(seats):
    return sum(row.count(Seat.OCCUPIED) for row in seats)

class Test(unittest.TestCase):
    def test_is_occupied(self):
        with open('test2.txt') as f:
            seats = parse_input(f)
        for dir_row, dir_col in neighbors:
            self.assertTrue(is_occupied(seats, 4, 3, dir_row, dir_col), f'dir = {dir_row},{dir_col}')

        with open('test3.txt') as f:
            seats = parse_input(f)
        for dir_row, dir_col in neighbors:
            self.assertFalse(is_occupied(seats, 1, 1, dir_row, dir_col), f'dir = {dir_row},{dir_col}')

        with open('test4.txt') as f:
            seats = parse_input(f)
        for dir_row, dir_col in neighbors:
            self.assertFalse(is_occupied(seats, 3, 3, dir_row, dir_col), f'dir = {dir_row},{dir_col}')

    def test_iterate(self):
        with open('test1.txt') as f:
            seats = parse_input(f)

        for i in range(1, 7):
            seats = iterate(seats)
            with open(f'test1_{i}.txt') as f:
                exp = parse_input(f)
            self.assertEqual(seats, exp, f'iteration {i}')

        # Final iteration to show convergence.
        seats_new = iterate(seats)
        self.assertEqual(seats, seats_new)

    def test_converge(self):
        with open('test1.txt') as f:
            seats = parse_input(f)
        seats = converge(seats)
        self.assertEqual(count_occupied(seats), 26)

if __name__ == '__main__':
    unittest.main(exit=False)

    with open('input.txt') as f:
        seats = parse_input(f)
    seats = converge(seats)
    print(count_occupied(seats))
