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

def get_token(s):
    # Read until first multiplication that isn't in a parenthesized sub-expression.
    parens = 0
    for i, c in enumerate(s):
        if parens == 0 and c == '*':
            return s[0:i-1], s[i:]
        elif c == '(':
            parens += 1
        elif c == ')':
            parens -= 1

    # No multiplication; everything is addition.
    # If the first term is a parenthesized expression, get that.
    if s[0] == '(':
        parens = 0
        for i, c in enumerate(s):
            if c == '(':
                parens += 1
            elif c == ')':
                parens -= 1
                if parens == 0:
                    return s[1:i], s[i+2:]

    # Nothing special, so just read the first term (until space).
    for i, c in enumerate(s):
        if c == ' ':
            return s[0:i], s[i+1:]

def parse_string(s):
    while is_single_expr_in_parens(s):
        s = s[1:-1]

    lhs, s = get_token(s)
    try:
        lhs = int(lhs)
    except ValueError:
        lhs = parse_string(lhs)

    op = s[0]
    s = s[2:]
    assert(len(op) == 1)

    while is_single_expr_in_parens(s):
        s = s[1:-1]
    try:
        rhs = int(s)
    except ValueError:
        rhs = parse_string(s)
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
            Expression(Expression(1, '+', 2), '*',
                Expression(Expression(3, '+', 4), '*', Expression(5, '+', 6))
            ))
        self.assertEqual(parse_string('(1 + 2) * 3'), Expression(Expression(1, '+', 2), '*', 3))
        self.assertEqual(parse_string('1 + (2 * (3 + 4) * 5)'),
            Expression(1, '+',
                    Expression(2, '*',
                        Expression(Expression(3, '+', 4), '*', 5)
                    )
                )
            )
        self.assertEqual(parse_string('(1 + 2) * 3'), Expression(Expression(1, '+', 2), '*', 3))

    def test_evaluate_string(self):
        self.assertEqual(evaluate_string('1 + 2 * 3 + 4 * 5 + 6'), 231)
        self.assertEqual(evaluate_string('1 + (2 * 3) + (4 * (5 + 6))'), 51)
        self.assertEqual(evaluate_string('2 * 3 + (4 * 5)'), 46)
        self.assertEqual(evaluate_string('5 + (8 * 3 + 9 + 3 * 4 * 3)'), 1445)
        self.assertEqual(evaluate_string('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))'), 669060)
        self.assertEqual(evaluate_string('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2'), 23340)

if __name__ == '__main__':
    unittest.main(exit=False)

    with open('input.txt') as f:
        print(sum(evaluate_string(line.rstrip()) for line in f))
