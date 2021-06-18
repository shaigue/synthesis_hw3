import operator
from typing import Dict, Callable, Set, Union

from z3 import ArithRef, BoolRef, Int

from adt.tree import Tree

OP = {'+': operator.add, '-': operator.sub,
      '*': operator.mul, '/': operator.floordiv,
      '!=': operator.ne, '>': operator.gt, '<': operator.lt,
      '<=': operator.le, '>=': operator.ge, '=': operator.eq}

Environment = Dict[str, ArithRef]
Property = Callable[[Dict[str, ArithRef]], Union[BoolRef, bool]]


def get_unique_variables(ast: Tree) -> Set[str]:
    return set(filter(lambda terminal: isinstance(terminal, str), ast.terminals))


def init_env_from_ast(ast: Tree) -> Environment:
    variables = get_unique_variables(ast)
    return {variable: Int(variable) for variable in variables}


def update_environment(env: Environment, variable: str, expression: ArithRef):
    env = env.copy()
    env[variable] = expression
    return env


def tree_expr_to_z3_expr(expr_tree: Tree, env: Environment) -> Union[ArithRef, BoolRef]:
    if expr_tree.root == "num":
        return expr_tree.terminals[0]

    elif expr_tree.root == "id":
        return env[expr_tree.terminals[0]]

    return OP[expr_tree.root](
        tree_expr_to_z3_expr(expr_tree.subtrees[0], env),
        tree_expr_to_z3_expr(expr_tree.subtrees[1], env)
    )
