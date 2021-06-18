from z3 import BoolRef, And

from while_lang.utils import Environment


def example_1_loop_invariant(env: Environment) -> BoolRef:
    return And(env['x'] > 0, env['y'] >= 0)


def example_2_loop_invariant(env: Environment) -> BoolRef:
    return env['a'] > 0
