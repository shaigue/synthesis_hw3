from adt.tree import Tree
from while_lang.find_counter_example import find_counter_example
from while_lang.syntax import WhileParser
from z3 import Int, ForAll, Implies, Not, And, Or, Solver, unsat, sat

from while_lang.weakest_pre_condition import get_weakest_pre_condition
from while_lang.utils import Environment, Property, init_env_from_ast


def verify(pre_condition: Property, ast: Tree, post_condition: Property, loop_invariant: Property = None):
    """
    Verifies a Hoare triple {pre_condition} ast {post_condition}
    Where pre_condition, post_condition are assertions (see below for examples)
    and ast is the AST of the command ast.
    Returns `True` iff the triple is valid.
    Also prints the counterexample (model) returned from Z3 in case
    it is not.
    """
    env = init_env_from_ast(ast)
    weakest_pre_condition = get_weakest_pre_condition(ast, post_condition, loop_invariant)

    counter_example = find_counter_example(pre_condition, weakest_pre_condition, env)
    if counter_example is not None:
        print(counter_example)
        return False

    return True


if __name__ == '__main__':
    # example program
    pvars = ['a', 'b', 'i', 'n']
    program = "a := b ; while i < n do ( a := a + 1 ; b := b + 1 )"
    P = lambda _: True
    Q = lambda d: d['a'] == d['b']
    linv = lambda d: d['a'] == d['b']

    #
    # Following are other programs that you might want to try
    #

    ## Program 1
    #pvars = ['x', 'i', 'y']
    #program = "y := 0 ; while y < i do ( x := x + y ; if (x * y) < 10 then y := y + 1 else skip )"
    #pre_condition = lambda env: env['x'] > 0
    #post_condition = lambda env: env['x'] > 0
    #loop_invariant = lambda env: **figure it out!**

    ## Program 2
    #pvars = ['a', 'b']
    #program = "while a != b do if a > b then a := a - b else b := b - a"
    #pre_condition = lambda env: And(env['a'] > 0, env['b'] > 0)
    #post_condition = lambda env: And(env['a'] > 0, env['a'] == env['b'])
    #loop_invariant = lambda env: ???

    ast = WhileParser()(program)

    if ast:
        print(">> Valid program.")
        # Your task is to implement "verify"
        verify(P, ast, Q, loop_invariant=linv)
    else:
        print(">> Invalid program.")

