#!/usr/bin/env python3

import unittest
from collections import namedtuple

Instruction = namedtuple('Instruction', ['opcode', 'argument'])

def parse_line(line):
    splits = line.rstrip().split()
    return Instruction(splits[0], int(splits[1]))

def parse_input(f):
    return list(map(parse_line, f))

class Program:
    def __init__(self, code):
        self.code = code
        self.accumulator = 0
        self.pc = 0

    def run_next_instruction(self):
        instruction = self.code[self.pc]
        if instruction.opcode == 'acc':
            self.accumulator += instruction.argument
            self.pc += 1
        elif instruction.opcode == 'jmp':
            self.pc += instruction.argument
        elif instruction.opcode == 'nop':
            self.pc += 1
        else:
            raise Exception(f'invalid opcode: "{instruction.opcode}"')

    def run_until_duplicate(self):
        instructions_seen = set()
        while self.pc not in instructions_seen:
            instructions_seen.add(self.pc)
            self.run_next_instruction()

class Test(unittest.TestCase):
    def test_run_until_duplicate(self):
        with open('test1.txt') as f:
            code = parse_input(f)
        program = Program(code)
        program.run_until_duplicate()
        self.assertEqual(program.accumulator, 5)

if __name__ == '__main__':
    unittest.main(exit=False)

    with open('input.txt') as f:
        code = parse_input(f)
    program = Program(code)
    program.run_until_duplicate()
    print(program.accumulator)
