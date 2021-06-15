from collections import Callable
from typing import Dict

from adt.tree import Tree


def upd(d, k, v):
    d = d.copy()
    d[k] = v
    return d


def weakest_precondition(c: Tree, Q, linv=None):
    # should not be bool, but a formula in z3 -NOT BOOL!!
    if c.root == "skip":
        return Q
    elif c.root == ":=":
        assignment_target = c.subtrees[0].subtree[0]
        expr = c.subtrees[1]
        return lambda env: Q(upd(env, assignment_target, env[assignment_target])
    elif c.root == ";":
        pass
    elif c.root == "if":
        pass
    elif c.root == "while":
        pass
    # elif c.root == "id":
    #     pass
    # elif c.root == "num":
    #     pass

