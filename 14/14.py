#!/usr/bin/env python3

import itertools
import re
import unittest

class Mask:
    def __init__(self, mask_str):
        mask_str = mask_str[::-1] # Reverse string to put least significant bit first.
        self.ones_mask = sum(1 << i for i, bit in enumerate(mask_str) if bit == '1')
        self.zeroes_mask = sum(1 << i for i, bit in enumerate(mask_str) if bit != 'X')
        self.floating_bits = [i for i, bit in enumerate(mask_str) if bit == 'X']

    def floating_bit_subsets(self):
        for r in range(len(self.floating_bits)+1):
            for subset in itertools.combinations(self.floating_bits, r):
                yield subset

    def apply(self, mem, addr, n):
        addr_orig = (addr | self.ones_mask) & self.zeroes_mask
        for subset in self.floating_bit_subsets():
            addr = addr_orig | sum(1 << bit for bit in subset)
            mem[addr] = n

class Program:
    def __init__(self, f):
        self.mem = {}
        self.input = f

    def run_line(self, line):
        if line.startswith('mask = '):
            self.mask = Mask(line.rstrip().rsplit(' ', 1)[-1])
        else:
            match = re.fullmatch(r'mem\[([0-9]+)\] = ([0-9]+)\n', line)
            self.mask.apply(self.mem, int(match.group(1)), int(match.group(2)))

    def run(self):
        for line in self.input:
            self.run_line(line)

    def sum(self):
        return sum(self.mem.values())

class Test(unittest.TestCase):
    def test_apply_mask(self):
        mask = Mask('000000000000000000000000000000X1001X')
        self.assertEqual(mask.ones_mask, 18)
        self.assertEqual(mask.zeroes_mask, 2**36 - 1 - 33)
        self.assertEqual(mask.floating_bits, [0, 5])

        mem = {}
        mask.apply(mem, 42, 100)
        self.assertEqual(mem, {26: 100, 27: 100, 58: 100, 59: 100})

        mask = Mask('00000000000000000000000000000000X0XX')
        self.assertEqual(mask.ones_mask, 0)
        self.assertEqual(mask.zeroes_mask, 2**36 - 1 - 11)
        self.assertEqual(mask.floating_bits, [0, 1, 3])
        mask.apply(mem, 26, 1)
        self.assertEqual(mem, {16:1, 17:1, 18:1, 19:1, 24:1, 25:1, 26: 1, 27: 1, 58: 100, 59: 100})

    def test_run_program(self):
        with open('test1.txt') as f:
            program = Program(f)
            program.run()
        self.assertEqual(program.sum(), 208)

if __name__ == '__main__':
    unittest.main(exit=False)

    with open('input.txt') as f:
        program = Program(f)
        program.run()
    print(program.sum())
