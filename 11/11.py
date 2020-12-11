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

def get_new_seat_state(seats, row, col):
    seat = seats[row][col]
    if seat != Seat.FLOOR:
        neighbors = [
            (row-1, col-1), (row-1, col), (row-1, col+1),
            (row, col-1), (row, col+1),
            (row+1, col-1), (row+1, col), (row+1, col+1),
        ]
        def is_occupied(seats, r, c):
            if r < 0 or c < 0:
                return False
            try:
                return seats[r][c] == Seat.OCCUPIED
            except IndexError:
                return False
        if seat == Seat.EMPTY:
            if all(not is_occupied(seats, r, c) for r, c in neighbors):
                return Seat.OCCUPIED
        elif seat == Seat.OCCUPIED:
            if sum(is_occupied(seats, r, c) for r, c in neighbors) >= 4:
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
    def test_iterate(self):
        with open('test1.txt') as f:
            seats = parse_input(f)

        for i in range(1, 6):
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
        self.assertEqual(count_occupied(seats), 37)

if __name__ == '__main__':
    unittest.main(exit=False)

    with open('input.txt') as f:
        seats = parse_input(f)
    seats = converge(seats)
    print(count_occupied(seats))
