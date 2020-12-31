#!/usr/bin/env python3

import itertools
import unittest

def get_next_transform(subject_number, value):
    return value * subject_number % 20201227

def transform_subject_number(subject_number, loop_size):
    value = 1
    for _ in range(loop_size):
        value = get_next_transform(subject_number, value)
    return value

initial_subject_number = 7

def get_public_key(loop_size):
    return transform_subject_number(initial_subject_number, loop_size)

def find_loop_size(public_key):
    value = 1
    for i in itertools.count(start=1):
        value = get_next_transform(initial_subject_number, value)
        if value == public_key:
            return i

def get_encryption_key(public_key, loop_size):
    return transform_subject_number(public_key, loop_size)

def crack_handshake(card_public_key, door_public_key):
    card_loop_size = find_loop_size(card_public_key)
    door_loop_size = find_loop_size(door_public_key)

    encryption_key = get_encryption_key(card_public_key, door_loop_size)
    encryption_key2 = get_encryption_key(door_public_key, card_loop_size)
    assert(encryption_key == encryption_key2)
    return encryption_key

class Test(unittest.TestCase):
    def test_get_public_key(self):
        self.assertEqual(get_public_key(8), 5764801)
        self.assertEqual(get_public_key(11), 17807724)

    def test_find_loop_size(self):
        self.assertEqual(find_loop_size(5764801), 8)
        self.assertEqual(find_loop_size(17807724), 11)

    def test_get_encryption_key(self):
        self.assertEqual(get_encryption_key(17807724, 8), 14897079)
        self.assertEqual(get_encryption_key(5764801, 11), 14897079)

    def test_crack_handshake(self):
        self.assertEqual(crack_handshake(5764801, 17807724), 14897079)

if __name__ == '__main__':
    unittest.main(exit=False)

    with open('input.txt') as f:
        card_public_key = int(next(f).rstrip())
        door_public_key = int(next(f).rstrip())

    print(crack_handshake(card_public_key, door_public_key))
