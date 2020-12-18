#!/usr/bin/env python3

import unittest
from collections import namedtuple

Expression = namedtuple('Expression', ['lhs', 'op', 'rhs'])

def is_single_expr_in_parens(s):
    if s[0] != '(':
        return False

    parens = 0
    for i, c in enumerate(s):
        if c == '(':
            parens += 1
        elif c == ')':
            parens -= 1
            if parens == 0:
                return i == len(s)-1

def get_end_token(s):
    if s[-1] == ')':
        parens = 0
        for i, c in enumerate(reversed(s)):
            if c == ')':
                parens += 1
            elif c == '(':
                parens -= 1
                if parens == 0:
                    return s[-i:-1], s[0:-i-2]
    else:
        for i, c in enumerate(reversed(s)):
            if c == ' ':
                return s[-i:], s[0:-i-1]
        return s

def parse_string(s):
    while is_single_expr_in_parens(s):
        s = s[1:-1]

    rhs, s = get_end_token(s)
    try:
        rhs = int(rhs)
    except ValueError:
        rhs = parse_string(rhs)

    op, s = get_end_token(s)
    assert(len(op) == 1)

    try:
        lhs = int(s)
    except ValueError:
        lhs = parse_string(s)
    return Expression(lhs, op, rhs)

def evaluate_string(s):
    return evaluate(parse_string(s))

def evaluate(expr):
    if isinstance(expr, int):
        return expr
    elif expr.op == '+':
        return evaluate(expr.lhs) + evaluate(expr.rhs)
    elif expr.op == '*':
        return evaluate(expr.lhs) * evaluate(expr.rhs)
    else:
        raise Exception(f'invalid expression: {expr}')

class Test(unittest.TestCase):
    def test_parse_string(self):
        self.assertEqual(parse_string('1 + 2'), Expression(1, '+', 2))
        self.assertEqual(parse_string('1 + 2 * 3'), Expression(Expression(1, '+', 2), '*', 3))
        self.assertEqual(parse_string('1 + 2 * 3 + 4 * 5 + 6'),
            Expression(
                Expression(
                    Expression(
                        Expression(
                            Expression(1, '+', 2),
                            '*', 3),
                        '+', 4),
                    '*', 5),
                '+', 6))
        self.assertEqual(parse_string('1 + (2 * 3)'), Expression(1, '+', Expression(2, '*', 3)))
        self.assertEqual(parse_string('1 + (2 * (3 + 4) * 5)'),
            Expression(1, '+',
                Expression(
                    Expression(2, '*', Expression(3, '+', 4)),
                '*', 5)
                ))
        self.assertEqual(parse_string('(1 + 2) * 3'), Expression(Expression(1, '+', 2), '*', 3))

    def test_evaluate_string(self):
        self.assertEqual(evaluate_string('1 + 2 * 3 + 4 * 5 + 6'), 71)
        self.assertEqual(evaluate_string('1 + (2 * 3) + (4 * (5 + 6))'), 51)
        self.assertEqual(evaluate_string('2 * 3 + (4 * 5)'), 26)
        self.assertEqual(evaluate_string('5 + (8 * 3 + 9 + 3 * 4 * 3)'), 437)
        self.assertEqual(evaluate_string('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))'), 12240)
        self.assertEqual(evaluate_string('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2'), 13632)

if __name__ == '__main__':
    unittest.main(exit=False)

    with open('input.txt') as f:
        print(sum(evaluate_string(line.rstrip()) for line in f))
