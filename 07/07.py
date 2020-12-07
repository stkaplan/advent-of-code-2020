#!/usr/bin/env python3

import re
import unittest
from collections import namedtuple

RuleChild = namedtuple('RuleChild', ['bag_type', 'count'])

def parse_bag_type(s):
    match = re.fullmatch('(.+) bags?', s.strip())
    return match.group(1)

def parse_bag_type_with_count(s):
    match = re.fullmatch('([0-9]+) (.+) bags?', s.strip().rstrip('.'))
    return match.group(2), int(match.group(1))

def parse_rule(rule):
    bag_type_str, children_str = rule.rstrip().split(' contain ')
    bag_type = parse_bag_type(bag_type_str)
    if children_str == 'no other bags.':
        children = []
    else:
        children = list(map(parse_bag_type_with_count, children_str.split(',')))
    return bag_type, [RuleChild(*c) for c in children]

def parse_input(f):
    return {k: v for k, v in map(parse_rule, f)}

def can_contain(rules, parent, child):
    if any(c.bag_type == child for c in rules[parent]):
        return True
    else:
        return any(can_contain(rules, c.bag_type, child) for c in rules[parent])

def contained_bags(rules, bag_type):
    return sum(child.count + child.count * contained_bags(rules, child.bag_type) for child in rules[bag_type])

class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test1rules = {
            'light red': [RuleChild('bright white', 1), RuleChild('muted yellow', 2)],
            'dark orange': [RuleChild('bright white', 3), RuleChild('muted yellow', 4)],
            'bright white': [RuleChild('shiny gold', 1)],
            'muted yellow': [RuleChild('shiny gold', 2), RuleChild('faded blue', 9)],
            'shiny gold': [RuleChild('dark olive', 1), RuleChild('vibrant plum', 2)],
            'dark olive': [RuleChild('faded blue', 3), RuleChild('dotted black', 4)],
            'vibrant plum': [RuleChild('faded blue', 5), RuleChild('dotted black', 6)],
            'faded blue': [],
            'dotted black': [],
        }

    def test_parse_input(self):
        with open('test1.txt') as f:
            rules = parse_input(f)
        self.assertEqual(rules, self.test1rules)

    def test_can_contain(self):
        true_types = ['bright white', 'muted yellow', 'dark orange', 'light red']
        for bag_type in self.test1rules:
            self.assertEqual(can_contain(self.test1rules, bag_type, 'shiny gold'), bag_type in true_types, msg=f'failed for {bag_type}')

    def test_contained_bags(self):
        self.assertEqual(contained_bags(self.test1rules, 'faded blue'), 0)
        self.assertEqual(contained_bags(self.test1rules, 'dotted black'), 0)
        self.assertEqual(contained_bags(self.test1rules, 'vibrant plum'), 11)
        self.assertEqual(contained_bags(self.test1rules, 'dark olive'), 7)

        with open('test2.txt') as f:
            rules = parse_input(f)
        self.assertEqual(contained_bags(rules, 'shiny gold'), 126)

if __name__ == '__main__':
    unittest.main(exit=False)

    with open('input.txt') as f:
        rules = parse_input(f)
    print(contained_bags(rules, 'shiny gold'))
