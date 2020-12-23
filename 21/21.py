#!/usr/bin/env python3

import re
import unittest
from collections import namedtuple

Food = namedtuple('Food', ['ingredients', 'allergens'])

def parse_line(line):
    match = re.fullmatch(r'([a-z ]+) \(contains ([a-z, ]+)\)\n', line)
    ingredients = match.group(1).split()
    allergens = match.group(2).split(', ')
    return Food(set(ingredients), set(allergens))

def parse_input(f):
    return list(map(parse_line, f))

def find_possible_ingredients(foods, allergen):
    ingredients_with_allergen = [food.ingredients for food in foods if allergen in food.allergens]
    return set.intersection(*ingredients_with_allergen)

def remove_from_other_allergens(possible_ingredients, ingredient, allergen):
    changed = False
    for a, i in possible_ingredients.items():
        if a != allergen and ingredient in i:
            i.remove(ingredient)
            changed = True
    return changed

def find_allergens(foods):
    all_allergens = set().union(*(food.allergens for food in foods))
    possible_ingredients = {allergen: find_possible_ingredients(foods, allergen) for allergen in all_allergens}

    # Use process of elimination for narrow down allergens with multiple possible ingredients.
    while True:
        changed = False
        for allergen, ingredients in possible_ingredients.items():
            if len(ingredients) == 1:
                changed |= remove_from_other_allergens(possible_ingredients, next(iter(ingredients)), allergen)
        if not changed:
            break

    assert all(len(i) == 1 for i in possible_ingredients.values())
    return {k: next(iter(v)) for k, v in possible_ingredients.items()}

def count_occurrences(foods, ingredient):
    return sum(ingredient in food.ingredients for food in foods)

def count_occurrences_with_no_allergens(foods, allergens):
    all_ingredients = set().union(*(food.ingredients for food in foods))
    no_allergens = [i for i in all_ingredients if i not in allergens.values()]
    return sum(count_occurrences(foods, i) for i in no_allergens)

class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test1foods = [
            Food({'mxmxvkd', 'kfcds', 'sqjhc', 'nhms'}, {'dairy', 'fish'}),
            Food({'trh', 'fvjkl', 'sbzzf', 'mxmxvkd'}, {'dairy'}),
            Food({'sqjhc', 'fvjkl'}, {'soy'}),
            Food({'sqjhc', 'mxmxvkd', 'sbzzf'}, {'fish'}),
        ]

        cls.test1allergens = {
            'dairy': 'mxmxvkd',
            'fish': 'sqjhc',
            'soy': 'fvjkl',
        }

    def test_parse_input(self):
        with open('test1.txt') as f:
            foods = parse_input(f)
        self.assertEqual(foods, self.test1foods)

    def test_find_allergens(self):
        self.assertEqual(find_allergens(self.test1foods), {'dairy': 'mxmxvkd', 'fish': 'sqjhc', 'soy': 'fvjkl'})

    def test_count_occurrences_with_no_allergens(self):
        self.assertEqual(count_occurrences(self.test1foods, 'kfcds'), 1)
        self.assertEqual(count_occurrences(self.test1foods, 'nhms'), 1)
        self.assertEqual(count_occurrences(self.test1foods, 'trh'), 1)
        self.assertEqual(count_occurrences(self.test1foods, 'sbzzf'), 2)
        self.assertEqual(count_occurrences_with_no_allergens(self.test1foods, self.test1allergens), 5)

if __name__ == '__main__':
    unittest.main(exit=False)

    with open('input.txt') as f:
        foods = parse_input(f)

    allergens = find_allergens(foods)
    print(count_occurrences_with_no_allergens(foods, allergens))
