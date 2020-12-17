#!/usr/bin/env python3

import functools
import operator
import unittest
from collections import namedtuple

Rule = namedtuple('Rule', ['name', 'ranges'])
Input = namedtuple('Input', ['rules', 'your_ticket', 'nearby_tickets'])

def parse_range(r):
    splits = r.split('-')
    return range(int(splits[0]), int(splits[1])+1)

def parse_rule(line):
    name, ranges = line.rstrip().split(':')
    splits = ranges.split(' ')
    return Rule(name, [parse_range(splits[1]), parse_range(splits[3])])

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
    return any(n in r for r in rule.ranges)

def passes_any_rule(rules, n):
    return any(passes_rule(rule, n) for rule in rules)

# Can't check for error_rate == 0 to see if we have an error, because we could
# have 0 as the only invalid value. So also return a boolean of whether we had
# an error.
def get_ticket_error_rate(rules, ticket):
    invalid_fields = [n for n in ticket if not passes_any_rule(rules, n)]
    return (len(invalid_fields) > 0, sum(invalid_fields))

def remove_from_other_sets(sets, n, i):
    changed = False
    for j, s in enumerate(sets):
        if i != j:
            if n in s:
                s.remove(n)
                changed = True
    return changed

def get_fields(input_):
    valid_tickets = [t for t in input_.nearby_tickets if not get_ticket_error_rate(input_.rules, t)[0]]
    possible_fields = [set(range(len(input_.rules))) for _ in range(len(input_.your_ticket))] # map of fields to which rules they can pass
    for rule_num, rule in enumerate(input_.rules):
        for ticket in valid_tickets:
            for field_num, field in enumerate(ticket):
                field = ticket[field_num]
                if rule_num in possible_fields[field_num] and not passes_rule(rule, field):
                    possible_fields[field_num].remove(rule_num)

    # The possible fields are narrowed down, so we need to use process of
    # elimination for values that could be from multiple fields.
    while True:
        changed = False
        for i, field_set in enumerate(possible_fields):
            if len(field_set) == 1:
                changed |= remove_from_other_sets(possible_fields, next(iter(field_set)), i)
        if not changed:
            break

    assert all(len(p) == 1 for p in possible_fields)
    return {input_.rules[next(iter(field))].name: input_.your_ticket[i] for i, field in enumerate(possible_fields)}

class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test1input = Input(
            [
                Rule('class', [range(1, 4), range(5, 8)]),
                Rule('row', [range(6, 12), range(33, 45)]),
                Rule('seat', [range(13, 41), range(45, 51)]),
            ],
            [7, 1, 14],
            [[7, 3, 47], [40, 4, 50], [55, 2, 20], [38, 6, 12]],
        )

    def test_parse_input(self):
        with open('test1.txt') as f:
            input_ = parse_input(f)
        self.assertEqual(input_, self.test1input)

    def test_get_ticket_error_rate(self):
        error_rates = [(False, 0), (True, 4), (True, 55), (True, 12)]
        for i, (ticket, expected_rate) in enumerate(zip(self.test1input.nearby_tickets, error_rates)):
            error_rate = get_ticket_error_rate(self.test1input.rules, ticket)
            self.assertEqual(error_rate, expected_rate, f'ticket {i}')

    def test_get_fields(self):
        with open('test2.txt') as f:
            input_ = parse_input(f)
        self.assertEqual(get_fields(input_), {'class': 12, 'row': 11, 'seat': 13})

if __name__ == '__main__':
    unittest.main(exit=False)

    with open('input.txt') as f:
        input_ = parse_input(f)

    fields = get_fields(input_)
    print(fields)
    print(functools.reduce(operator.mul, (v for k, v in fields.items() if k.startswith('departure ')), 1))
