#!/usr/bin/env python3

import re
import unittest

class Mask:
    def __init__(self, mask_str):
        self.ones_mask = sum(1 << (len(mask_str)-i-1) for i, bit in enumerate(mask_str) if bit == '1')
        self.zeroes_mask = sum(1 << (len(mask_str)-i-1) for i, bit in enumerate(mask_str) if bit != '0')

    def apply_to(self, n):
        return (n | self.ones_mask) & self.zeroes_mask

class Program:
    def __init__(self, f):
        self.mem = {}
        self.input = f

    def run_line(self, line):
        if line.startswith('mask = '):
            self.mask = Mask(line.rstrip().rsplit(' ', 1)[-1])
        else:
            match = re.fullmatch(r'mem\[([0-9]+)\] = ([0-9]+)\n', line)
            self.mem[int(match.group(1))] = self.mask.apply_to(int(match.group(2)))

    def run(self):
        for line in self.input:
            self.run_line(line)

    def sum(self):
        return sum(self.mem.values())

class Test(unittest.TestCase):
    def test_apply_mask(self):
        mask = Mask('XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X')
        self.assertEqual(mask.ones_mask, 64)
        self.assertEqual(mask.zeroes_mask, 2**36 - 1 - 2) # All bits set except second-least-significant.
        self.assertEqual(mask.apply_to(11), 73)
        self.assertEqual(mask.apply_to(101), 101)
        self.assertEqual(mask.apply_to(0), 64)

    def test_run_program(self):
        with open('test1.txt') as f:
            program = Program(f)
            program.run()
        self.assertEqual(program.sum(), 165)

if __name__ == '__main__':
    unittest.main(exit=False)

    with open('input.txt') as f:
        program = Program(f)
        program.run()
    print(program.sum())
