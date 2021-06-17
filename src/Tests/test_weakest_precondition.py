import unittest
from while_lang.weakest_precondition import weakest_precondition, parse_expr
from adt.tree import Tree
from while_lang.syntax import WhileParser
from z3 import Int, ForAll, Implies, Not, And, Or, Solver, unsat, sat


class MyTestCase(unittest.TestCase):
    def test_parse_expr(self):
        program = "a := b ; while i < n do ( a := a + 1 ; b := b + 1 )"
        ast = WhileParser()(program)
        env = {term: Int(term) for term in ast.terminals if isinstance(term, str)}
        formula = parse_expr(ast.subtrees[1].subtrees[1].subtrees[0].subtrees[1], env)
        self.assertEqual(formula, Int('a') + 1)
        formula2 = parse_expr(ast.subtrees[1].subtrees[0], env)
        self.assertEqual(formula2, Int('i') < Int('n'))


if __name__ == '__main__':
    unittest.main()
