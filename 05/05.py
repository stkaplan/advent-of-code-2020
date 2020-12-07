#!/usr/bin/env python3

import unittest

class Seat:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def seat_id(self):
        return self.row * 8 + self.col

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

def convert_bools_to_int(bs):
    return sum(int(b) << i for i, b in enumerate(bs))

def parse_seat(s):
    s = s.rstrip()
    assert(len(s) == 10)
    row_str = s[6::-1]
    assert(all(c in ['F', 'B'] for c in row_str))
    col_str = s[:6:-1]
    assert(all(c in ['L', 'R'] for c in col_str))

    row = convert_bools_to_int(c == 'B' for c in row_str)
    col = convert_bools_to_int(c == 'R' for c in col_str)
    return Seat(row, col)

def parse_input(f):
    return list(map(parse_seat, f))

class Test(unittest.TestCase):
    def test_parse_seat(self):
        cases = [
            ('FBFBBFFRLR', Seat(44, 5), 357),
            ('BFFFBBFRRR', Seat(70, 7), 567),
            ('FFFBBBFRRR', Seat(14, 7), 119),
            ('BBFFBBFRLL', Seat(102, 4), 820),
        ]
        for case in cases:
            seat = parse_seat(case[0])
            self.assertEqual(seat, case[1])
            self.assertEqual(seat.seat_id(), case[2])

if __name__ == '__main__':
    unittest.main(exit=False)
    with open('input.txt') as f:
        seats = parse_input(f)

    seat_ids = [s.seat_id() for s in seats]
    min_seat_id = min(seat_ids)
    max_seat_id = max(seat_ids)

    # Magic interview trick to get missing number: add numbers and subtract from expected sum.
    expected_sum = ((max_seat_id * (max_seat_id+1)) - ((min_seat_id-1) * (min_seat_id))) // 2
    actual_sum = sum(seat_ids)
    missing = expected_sum - actual_sum
    print(missing)
