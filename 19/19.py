#!/usr/bin/env python3

import re
import unittest
from collections import namedtuple

Input = namedtuple('Input', ['rules', 'messages'])

def parse_rule_component(s):
    if s[0] == '"' and s[-1] == '"':
        return s[1:-1]
    else:
        return [int(x) for x in s.split()]

def parse_rule(line):
    splits = re.split(r': | \| ', line.rstrip())
    if len(splits) == 2 and splits[1][0] == '"' and splits[1][-1]:
        rule = splits[1][1:-1] # Remove quotes from string.
    else:
        rule = [[int(x) for x in s.split()] for s in splits[1:]]
    return int(splits[0]), rule

def parse_input(f):
    rules = {}
    for line in f:
        if line.isspace():
            break
        num, rule = parse_rule(line)
        assert(num not in rules)
        rules[num] = rule

    messages = [line.rstrip() for line in f]
    return Input(rules, messages)

def message_matches_sequence(message, rules, sequence, rule_cache, sequence_cache):
    cached_result = sequence_cache.get((message, tuple(sequence)), None)
    if cached_result is not None:
        return cached_result

    if len(sequence) == 1:
        result = message_matches_rule(message, rules, sequence[0], rule_cache, sequence_cache)
    else:
        for i in range(len(message)-1):
            parts = message[0:i+1], message[i+1:]
            if len(parts[1]) < len(sequence)-1:
                result = False
                break
            if message_matches_rule(parts[0], rules, sequence[0], rule_cache, sequence_cache) \
                    and message_matches_sequence(parts[1], rules, sequence[1:], rule_cache, sequence_cache):
                result = True
                break
        else:
            result = False

    sequence_cache[(message, tuple(sequence))] = result
    return result

def message_matches_rule(message, rules, rule_id, rule_cache, sequence_cache):
    cached_result = rule_cache.get((message, rule_id), None)
    if cached_result is not None:
        return cached_result

    rule = rules[rule_id]
    if isinstance(rule, str):
        result = message == rule
    else:
        result = any(message_matches_sequence(message, rules, seq, rule_cache, sequence_cache) for seq in rule)

    rule_cache[(message, rule_id)] = result
    return result

def update_rules(rules):
    rules[8] = [[42], [42, 8]]
    rules[11] = [[42, 31], [42, 11, 31]]

class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test1rules = {
            0: [[1, 2]],
            1: 'a',
            2: [[1, 3], [3, 1]],
            3: 'b',
        }
        cls.test1messages = ['aab', 'aba', 'bba', 'babb', 'aabb']

        cls.test2rules = {
            0: [[4, 1, 5]],
            1: [[2, 3], [3, 2]],
            2: [[4, 4], [5, 5]],
            3: [[4, 5], [5, 4]],
            4: 'a',
            5: 'b',
        }
        cls.test2messages = ['ababbb', 'bababa', 'abbbab', 'aaabbb', 'aaaabbb']

    def test_parse_input(self):
        with open('test1.txt') as f:
            input_ = parse_input(f)
        self.assertEqual(input_, Input(self.test1rules, self.test1messages))

        with open('test2.txt') as f:
            input_ = parse_input(f)
        self.assertEqual(input_, Input(self.test2rules, self.test2messages))

    def test_message_matches(self):
        test1results = [True, True, False, False, False]
        for message, result in zip(self.test1messages, test1results):
            self.assertEqual(message_matches_rule(message, self.test1rules, 0, {}, {}), result, message)

        test2results = [True, False, True, False, False]
        for message, result in zip(self.test2messages, test2results):
            self.assertEqual(message_matches_rule(message, self.test2rules, 0, {}, {}), result, message)

    def test_part2(self):
        with open('test3.txt') as f:
            input_ = parse_input(f)

        for i, message in enumerate(input_.messages):
            result = i in (1, 6, 7)
            self.assertEqual(message_matches_rule(message, input_.rules, 0, {}, {}), result, message)

        update_rules(input_.rules)
        for i, message in enumerate(input_.messages):
            result = i not in (0, 11, 13)
            self.assertEqual(message_matches_rule(message, input_.rules, 0, {}, {}), result, message)

if __name__ == '__main__':
    unittest.main(exit=False)

    with open('input.txt') as f:
        input_ = parse_input(f)

    # Print results individually so I can see the progress.
    update_rules(input_.rules)
    matching = 0
    for m in input_.messages:
        result = message_matches_rule(m, input_.rules, 0, {}, {})
        print(m, result)
        matching += result
    print(matching)
