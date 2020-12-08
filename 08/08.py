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

    def check_for_infinite_loop(self):
        instructions_seen = set()
        while True:
            if self.pc in instructions_seen:
                return True
            elif self.pc == len(self.code):
                return False
            instructions_seen.add(self.pc)
            self.run_next_instruction()

def find_corrupted_instruction(code_orig):
    for i in range(len(code_orig)):
        if code_orig[i].opcode not in ['jmp', 'nop']:
            continue

        code = code_orig.copy()
        if code[i].opcode == 'jmp':
            code[i] = Instruction('nop', code[i].argument)
        elif code[i].opcode == 'nop':
            code[i] = Instruction('jmp', code[i].argument)

        program = Program(code)
        infinite = program.check_for_infinite_loop()
        if not infinite:
            return (i, program.accumulator)

    return None

class Test(unittest.TestCase):
    def test_check_for_infinite_loop(self):
        with open('test1.txt') as f:
            code = parse_input(f)
        program = Program(code)
        infinite = program.check_for_infinite_loop()
        self.assertEqual(infinite, True)
        self.assertEqual(program.accumulator, 5)

    def test_find_corrupted_instruction(self):
        with open('test1.txt') as f:
            code = parse_input(f)
        corrupted = find_corrupted_instruction(code)
        self.assertEqual(corrupted, (7, 8))

if __name__ == '__main__':
    unittest.main(exit=False)

    with open('input.txt') as f:
        code = parse_input(f)
    program = Program(code)
    corrupted = find_corrupted_instruction(code)
    print(corrupted)
