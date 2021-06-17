from collections import Callable
from typing import Dict

from adt.tree import Tree
from z3 import Int, ForAll, Implies, Not, And, Or, Solver, unsat, sat
import operator
from while_lang.syntax import WhileParser

OP = {'+': operator.add, '-': operator.sub,
      '*': operator.mul, '/': operator.floordiv,
      '!=': operator.ne, '>': operator.gt, '<': operator.lt,
      '<=': operator.le, '>=': operator.ge, '=': operator.eq}


def upd(d, k, v):
    d = d.copy()
    d[k] = v
    return d


def parse_expr(expr: Tree, env):
    if expr.root == "num":
        return expr.terminals[0]
    elif expr.root == "id":
        return env[expr.terminals[0]]
    return OP[expr.root](parse_expr(expr.subtrees[0], env),
                         parse_expr(expr.subtrees[1], env))


def weakest_precondition(c: Tree, Q, linv):
    # should not be bool, but a formula in z3 -NOT BOOL!!
    if c.root == "skip":
        return Q
    elif c.root == ":=":
        to_replace = c.terminals[0]
        return lambda e: Q(upd(e, to_replace, parse_expr(c.subtrees[1], e)))
    elif c.root == ";":
        Q2 = weakest_precondition(c.subtrees[1], Q, linv)
        return weakest_precondition(c.subtrees[0], Q2, linv)
    elif c.root == "if":
        then_clause, else_clause = c.subtrees[1], c.subtrees[2]
        return lambda e: Or(And(parse_expr(c.subtrees[0], e), weakest_precondition(then_clause, Q, e)),
                            And(Not(parse_expr(c.subtrees[0], e)), weakest_precondition(else_clause, Q, e)))
    elif c.root == "while":
        body = c.subtrees[1]
        P = linv
        return lambda e: And(P(e), ForAll([e[k] for k in e.keys()],
                                          And(Implies(And(P(e),parse_expr(c.subtrees[0], e)),
                                                      weakest_precondition(body, P, e)(e)),
                                              Implies(And(P(e), Not(parse_expr(c.subtrees[0], e))), Q(e)))))


if __name__ == "__main__":
    program = "a := b ; while i < n do ( a := a + 1 ; b := b + 1 )"
    P = lambda _: True
    Q = lambda d: d['a'] == d['b']
    linv = lambda d: d['a'] == d['b']
    ast = WhileParser()(program)
    env = {term: Int(term) for term in ast.terminals if isinstance(term, str)}
    wp = weakest_precondition(ast, Q, linv)(env)
    print(wp)
