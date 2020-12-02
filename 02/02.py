#!/usr/bin/env python3

import re
import unittest
from collections import namedtuple
from io import StringIO

Policy = namedtuple('Policy', ['first_pos', 'second_pos', 'letter'])

def parse_line(line):
    line = line.rstrip()
    match = re.fullmatch(r'([0-9]+)-([0-9]+) ([a-zA-Z]): (.+)', line)
    try:
        groups = match.groups()
        return Policy(int(groups[0]), int(groups[1]), groups[2]), groups[3]
    except:
        raise Exception(f'invalid input line: "{line}"')

def read_input(f):
    return list(map(parse_line, f))

def password_is_valid(policy, password):
    return (password[policy.first_pos - 1] == policy.letter) ^ (password[policy.second_pos - 1] == policy.letter)

class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.input = StringIO('1-3 a: abcde\n1-3 b: cdefg\n2-9 c: ccccccccc\n')

    def test_read_input(self):
        input_ = read_input(self.input)
        self.assertEqual(input_, [((1, 3, 'a'), 'abcde'), ((1, 3, 'b'), 'cdefg'), ((2, 9, 'c'), 'ccccccccc')])
        valid = [password_is_valid(policy, password) for policy, password in input_]
        self.assertEqual(valid, [True, False, False])

if __name__ == '__main__':
    unittest.main(exit=False)

    with open('input.txt') as f:
        input_ = read_input(f)

    valid = [password_is_valid(policy, password) for policy, password in input_]
    print(sum(valid))
