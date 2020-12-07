#!/usr/bin/env python3

import unittest

def parse_input(f):
    groups = []
    group = []
    for line in f:
        if line.isspace():
            groups.append(group)
            group = []
        else:
            group.append(line.rstrip())
    if group: # No blank line before EOF, so add final group.
        groups.append(group)
    return groups

def get_union_count(group):
    return len(set().union(*group))

class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test1groups = [['abc'], ['a', 'b', 'c'], ['ab', 'ac'], ['a', 'a', 'a', 'a'], ['b']]

    def test_parse_input(self):
        with open('test1.txt') as f:
            groups = parse_input(f)
        self.assertEqual(groups, self.test1groups)

    def test_get_union_count(self):
        union_count = list(map(get_union_count, self.test1groups))
        self.assertEqual(union_count, [3, 3, 3, 1, 1])

if __name__ == '__main__':
    unittest.main(exit=False)
    with open('input.txt') as f:
        groups = parse_input(f)

    print(sum(map(get_union_count, groups)))
