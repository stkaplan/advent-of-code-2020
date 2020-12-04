#!/usr/bin/env python3

import unittest

def parse_passport(s):
    passport = {}
    for token in s.split(' '):
        k, v = token.split(':')
        passport[k] = v
    return passport

def read_input(f):
    def add_passport(passports, passport):
        passports.append(passport.rstrip().replace('\n', ' '))
    passports = []
    passport = ''
    for line in f:
        if line.isspace():
            add_passport(passports, passport)
            passport = ''
        else:
            passport += line

    if passport: # We won't see an empty line before EOF, so add the last passport.
            add_passport(passports, passport)
    return list(map(parse_passport, passports))

def passport_is_valid(passport):
    required_fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']
    return all(field in passport for field in required_fields)

class Test(unittest.TestCase):
    def test_passport_is_valid(self):
        with open('test1.txt') as f:
            passports = read_input(f)
        valid = list(map(passport_is_valid, passports))
        self.assertEqual(valid, [True, False, True, False])

if __name__ == '__main__':
    unittest.main(exit=False)

    with open('input.txt') as f:
        passports = read_input(f)
    print(sum(map(passport_is_valid, passports)))
