from typing import Optional
from z3 import ModelRef, Solver, sat, And, Not

from while_lang.utils import Environment, Property


def find_counter_example(pre_condition: Property, weakest_pre_condition: Property,
                         env: Environment) -> Optional[ModelRef]:
    """Finding a counter example where `pre_condition` is satisfied, but `weakest_pre_condition` is not"""
    pre_condition_formula = pre_condition(env)
    weakest_pre_condition_formula = weakest_pre_condition(env)
    implication_negation_formula = And(pre_condition_formula, Not(weakest_pre_condition_formula))
    solver = Solver()
    solver.add(implication_negation_formula)
    if solver.check() == sat:
        return solver.model()
    return None
