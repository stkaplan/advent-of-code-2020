#!/usr/bin/env python3

import unittest
from collections import namedtuple

Input = namedtuple('Input', ['rules', 'your_ticket', 'nearby_tickets'])

def parse_range(r):
    splits = r.split('-')
    return range(int(splits[0]), int(splits[1])+1)

def parse_rule(line):
    line = line.rstrip().split(':')[1]
    splits = line.split(' ')
    return [parse_range(splits[1]), parse_range(splits[3])]

def parse_ticket(line):
    return list(map(int, line.rstrip().split(',')))

def parse_input(f):
    rules = []
    for line in f:
        if line.isspace():
            break
        rules.append(parse_rule(line))
        
    _ = next(f)
    your_ticket = parse_ticket(next(f))

    for _ in range(2):
        next(f)
    nearby_tickets = list(map(parse_ticket, f))

    return Input(rules, your_ticket, nearby_tickets)

def passes_rule(rule, n):
    return any(n in r for r in rule)

def passes_any_rule(rules, n):
    return any(passes_rule(rule, n) for rule in rules)

def get_ticket_error_rate(rules, ticket):
    return sum(n for n in ticket if not passes_any_rule(rules, n))

class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test1input = Input(
            [[range(1, 4), range(5, 8)], [range(6, 12), range(33, 45)], [range(13, 41), range(45, 51)]],
            [7, 1, 14],
            [[7, 3, 47], [40, 4, 50], [55, 2, 20], [38, 6, 12]],
        )

    def test_parse_input(self):
        with open('test1.txt') as f:
            input_ = parse_input(f)
        self.assertEqual(input_, self.test1input)

    def test_get_ticket_error_rate(self):
        error_rates = [0, 4, 55, 12]
        for i, (ticket, expected_rate) in enumerate(zip(self.test1input.nearby_tickets, error_rates)):
            error_rate = get_ticket_error_rate(self.test1input.rules, ticket)
            self.assertEqual(error_rate, expected_rate, f'ticket {i}')

if __name__ == '__main__':
    unittest.main(exit=False)

    with open('input.txt') as f:
        input_ = parse_input(f)
    print(sum(get_ticket_error_rate(input_.rules, ticket) for ticket in input_.nearby_tickets))
