#!/usr/bin/env python3

import operator
import unittest
from collections import Counter

def parse_input(f):
    return set(map(int, f))

max_joltage_difference = 3

def find_next_adapter(adapters, joltage):
    for difference in range(1, max_joltage_difference+1):
        if joltage + difference in adapters:
            return joltage + difference

def get_complete_adapter_chain(adapters):
    chain = [0]
    joltage = 0
    while len(adapters) > 0:
        joltage = find_next_adapter(adapters, joltage)
        chain.append(joltage)
        adapters.remove(joltage)
    chain.append(joltage + max_joltage_difference)
    return chain

def get_difference_distribution(adapters):
    chain = get_complete_adapter_chain(adapters)
    diffs = list(map(operator.sub, chain[1:], chain))
    return Counter(diffs)

def find_possible_next_adapters(adapters, joltage):
    return [next_joltage for next_joltage in range (joltage+1, joltage+max_joltage_difference+1) if next_joltage in adapters]

def get_all_adapter_chains(adapters):
    completed_chains = []
    chains = [[0]]
    max_joltage = max(adapters)
    print('max = ', max_joltage)
    while chains:
        new_chains = []
        for chain in chains:
            for n in find_possible_next_adapters(adapters, chain[-1]):
                new_chain = chain + [n]
                if new_chain[-1] == max_joltage:
                    completed_chains.append(new_chain)
                else:
                    new_chains.append(new_chain)
        chains = new_chains
        print(len(chains))
    return completed_chains

class Test(unittest.TestCase):
    def test_get_complete_adapter_chain(self):
        with open('test1.txt') as f:
            adapters = parse_input(f)
        exp = [0, 1, 4, 5, 6, 7, 10, 11, 12, 15, 16, 19, 22]
        self.assertEqual(get_complete_adapter_chain(adapters), exp)

    def test_get_difference_distribution(self):
        with open('test1.txt') as f:
            adapters = parse_input(f)
        self.assertEqual(get_difference_distribution(adapters), Counter({1:7, 3:5}))

        with open('test2.txt') as f:
            adapters = parse_input(f)
        self.assertEqual(get_difference_distribution(adapters), Counter({1:22, 3:10}))

    def test_get_all_adapter_chains(self):
        with open('test1.txt') as f:
            adapters = parse_input(f)
        self.assertEqual(len(get_all_adapter_chains(adapters)), 8)

        with open('test2.txt') as f:
            adapters = parse_input(f)
        self.assertEqual(len(get_all_adapter_chains(adapters)), 19208)

if __name__ == '__main__':
    unittest.main(exit=False)

    with open('input.txt') as f:
        adapters = parse_input(f)

    chains = get_all_adapter_chains(adapters)
    print(chains)
