from z3 import ForAll, Implies, Not, And, Or, Int

from adt.tree import Tree
from while_lang.syntax import WhileParser
from while_lang.utils import Property, update_environment, init_env_from_ast, tree_expr_to_z3_expr


def get_weakest_pre_condition(ast: Tree, post_condition: Property, loop_invariant: Property = None) -> Property:
    if ast.root == "skip":
        return post_condition

    elif ast.root == ":=":
        to_replace = ast.terminals[0]
        expr_tree = ast.subtrees[1]

        return lambda env: post_condition(update_environment(env, to_replace,
                                                             tree_expr_to_z3_expr(expr_tree, env)))

    elif ast.root == ";":
        ast0 = ast.subtrees[0]
        ast1 = ast.subtrees[1]
        post_condition0 = get_weakest_pre_condition(ast1, post_condition, loop_invariant)
        return get_weakest_pre_condition(ast0, post_condition0, loop_invariant)

    elif ast.root == "if":
        if_condition = ast.subtrees[0]
        true_ast = ast.subtrees[1]
        false_ast = ast.subtrees[2]

        return lambda env: Or(
            And(tree_expr_to_z3_expr(if_condition, env),
                get_weakest_pre_condition(true_ast, post_condition, loop_invariant)(env)),
            And(Not(tree_expr_to_z3_expr(if_condition, env)),
                get_weakest_pre_condition(false_ast, post_condition, loop_invariant)(env))
        )

    elif ast.root == "while":
        # TODO: do we have to be given a loop_invariant?
        assert loop_invariant is not None, "loop encountered, and no loop invariant provided."
        loop_condition = ast.subtrees[0]
        loop_body = ast.subtrees[1]

        return lambda env: And(
            loop_invariant(env),
            ForAll(
                # we do not put directly the values in the dict, since they could be expressions,
                # and this is not valid input for ForAll()
                # TODO - using the forall quantifier here reduces the counter example
                [Int(var_str) for var_str in env.keys()],
                And(
                    Implies(
                        And(loop_invariant(env), tree_expr_to_z3_expr(loop_condition, env)),
                        get_weakest_pre_condition(loop_body, loop_invariant)(env)
                    ),
                    Implies(
                        And(loop_invariant(env), Not(tree_expr_to_z3_expr(loop_condition, env))),
                        post_condition(env)
                    )
                )
            )
        )


def example():
    program = "a := b ; while i < n do ( a := a + 1 ; b := b + 1 )"
    pre_condition = lambda _: True
    post_condition = lambda d: d['a'] == d['b']
    loop_invariant = lambda d: d['a'] == d['b']
    ast = WhileParser()(program)
    env = init_env_from_ast(ast)
    weakest_pre_condition = get_weakest_pre_condition(ast, post_condition, loop_invariant)
    weakest_pre_condition_formula = weakest_pre_condition(env)
    print(weakest_pre_condition_formula)


if __name__ == '__main__':
    example()
