#!/usr/bin/env python3

import re
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
    try:
        if not 1920 <= int(passport['byr']) <= 2002:
            return False
        if not 2010 <= int(passport['iyr']) <= 2020:
            return False
        if not 2020 <= int(passport['eyr']) <= 2030:
            return False
        hgt_match = re.fullmatch('([0-9]+)(cm|in)', passport['hgt'])
        if not hgt_match:
            return False
        if hgt_match.group(2) == 'cm' and not 150 <= int(hgt_match.group(1)) <= 193:
            return False
        if hgt_match.group(2) == 'in' and not 59 <= int(hgt_match.group(1)) <= 76:
            return False
        if not re.fullmatch('#[0-9a-f]{6}', passport['hcl']):
            return False
        if not passport['ecl'] in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']:
            return False
        if not re.fullmatch('[0-9]{9}', passport['pid']):
            return False
        # Ignore cid
        return True
    except (KeyError, ValueError):
        return False

class Test(unittest.TestCase):
    def test_passport_is_valid(self):
        with open('test1.txt') as f:
            passports = read_input(f)
        valid = list(map(passport_is_valid, passports))
        self.assertEqual(valid, [False]*4 + [True]*4)

if __name__ == '__main__':
    unittest.main(exit=False)

    with open('input.txt') as f:
        passports = read_input(f)
    print(sum(map(passport_is_valid, passports)))
