# TODO: make sure not to include this in submission to not get cheating notes
import unittest

from z3 import And

from while_lang.syntax import WhileParser
from while_lang.wp import verify


class TestVerify(unittest.TestCase):
    def test_skip_true_0(self):
        program = "skip"
        ast = WhileParser()(program)

        def pre_condition(env):
            return True

        def post_condition(env):
            return True

        result = verify(pre_condition, ast, post_condition)

        self.assertTrue(result)

    def test_skip_true_1(self):
        program = "skip"
        ast = WhileParser()(program)

        def pre_condition(env):
            return False

        def post_condition(env):
            return False

        result = verify(pre_condition, ast, post_condition)

        self.assertTrue(result)

    def test_skip_false(self):
        program = "skip"
        ast = WhileParser()(program)

        def pre_condition(env):
            return True

        def post_condition(env):
            return False

        result = verify(pre_condition, ast, post_condition)

        self.assertFalse(result)

    def test_assign_true_0(self):
        program = "x := y"
        ast = WhileParser()(program)

        def pre_condition(env):
            return True

        def post_condition(env):
            return env['x'] == env['y']

        result = verify(pre_condition, ast, post_condition)

        self.assertTrue(result)

    def test_assign_true_1(self):
        program = "x := y + 1"
        ast = WhileParser()(program)

        def pre_condition(env):
            return True

        def post_condition(env):
            return env['x'] > env['y']

        result = verify(pre_condition, ast, post_condition)

        self.assertTrue(result)

    def test_assign_true_2(self):
        program = "x := y + 1"
        ast = WhileParser()(program)

        def pre_condition(env):
            return env['x'] < env['y']

        def post_condition(env):
            return env['x'] > env['y']

        result = verify(pre_condition, ast, post_condition)

        self.assertTrue(result)

    def test_assign_false_0(self):
        program = "x := y"
        ast = WhileParser()(program)

        def pre_condition(env):
            return True

        def post_condition(env):
            return env['x'] != env['y']

        result = verify(pre_condition, ast, post_condition)

        self.assertFalse(result)

    def test_assign_false_1(self):
        program = "x := y - 1"
        ast = WhileParser()(program)

        def pre_condition(env):
            return True

        def post_condition(env):
            return env['x'] >= env['y']

        result = verify(pre_condition, ast, post_condition)

        self.assertFalse(result)

    def test_assign_false_2(self):
        program = "x := y - 1"
        ast = WhileParser()(program)

        def pre_condition(env):
            return env['x'] == env['y']

        def post_condition(env):
            return env['x'] >= env['y']

        result = verify(pre_condition, ast, post_condition)

        self.assertFalse(result)

    def test_assign_before_skip_true(self):
        program = "x := y + 1 ; skip"
        ast = WhileParser()(program)

        def pre_condition(env):
            return env['x'] < env['y']

        def post_condition(env):
            return env['x'] > env['y']

        result = verify(pre_condition, ast, post_condition)

        self.assertTrue(result)

    def test_assign_before_skip_false(self):
        program = "x := y - 1 ; skip"
        ast = WhileParser()(program)

        def pre_condition(env):
            return env['x'] == env['y']

        def post_condition(env):
            return env['x'] >= env['y']

        result = verify(pre_condition, ast, post_condition)

        self.assertFalse(result)

    def test_assign_after_skip_true(self):
        program = "skip ; x := y + 1"
        ast = WhileParser()(program)

        def pre_condition(env):
            return env['x'] < env['y']

        def post_condition(env):
            return env['x'] > env['y']

        result = verify(pre_condition, ast, post_condition)

        self.assertTrue(result)

    def test_assign_after_skip_false(self):
        program = "skip ; x := y - 1"
        ast = WhileParser()(program)

        def pre_condition(env):
            return env['x'] == env['y']

        def post_condition(env):
            return env['x'] >= env['y']

        result = verify(pre_condition, ast, post_condition)

        self.assertFalse(result)

    def test_if_true_0(self):
        program = "if x >= y then w := v else w := u"
        ast = WhileParser()(program)

        def pre_condition(env):
            return env['x'] == env['y']

        def post_condition(env):
            return env['w'] == env['v']

        result = verify(pre_condition, ast, post_condition)

        self.assertTrue(result)

    def test_if_true_1(self):
        program = "if x >= y then w := v else w := u"
        ast = WhileParser()(program)

        def pre_condition(env):
            return env['u'] == env['v']

        def post_condition(env):
            return env['w'] == env['v']

        result = verify(pre_condition, ast, post_condition)

        self.assertTrue(result)

    def test_if_false_0(self):
        program = "if x >= y then w := v else w := u"
        ast = WhileParser()(program)

        def pre_condition(env):
            return env['x'] < env['y']

        def post_condition(env):
            return env['w'] == env['v']

        result = verify(pre_condition, ast, post_condition)

        self.assertFalse(result)

    def test_if_false_1(self):
        program = "if x >= y then w := v else w := u"
        ast = WhileParser()(program)

        def pre_condition(env):
            return env['x'] < env['u']

        def post_condition(env):
            return env['y'] == env['v']

        result = verify(pre_condition, ast, post_condition)

        self.assertFalse(result)

    def test_while_true_0(self):
        program = "while x < y do x := x + 1"
        ast = WhileParser()(program)

        def pre_condition(env):
            return True

        def post_condition(env):
            return env['x'] >= env['y']

        def loop_invariant(env):
            return True

        result = verify(pre_condition, ast, post_condition, loop_invariant)

        self.assertTrue(result)

    def test_while_true_1(self):
        program = "i := 0 ; x := 0; while i < 5 do (x := x + y ; i := i + 1)"
        ast = WhileParser()(program)

        def pre_condition(env):
            return True

        def post_condition(env):
            return env['x'] == 5 * env['y']

        def loop_invariant(env):
            return And(env['x'] == env['i'] * env['y'], env['i'] <= 5)

        result = verify(pre_condition, ast, post_condition, loop_invariant)

        self.assertTrue(result)

    def test_while_false_0(self):
        program = "while x < y do x := x + 1"
        ast = WhileParser()(program)

        def pre_condition(env):
            return True

        def post_condition(env):
            return env['y'] >= 0

        def loop_invariant(env):
            return True

        result = verify(pre_condition, ast, post_condition, loop_invariant)

        self.assertFalse(result)

    def test_given_example_0(self):
        program = "a := b ; while i < n do ( a := a + 1 ; b := b + 1 )"
        ast = WhileParser()(program)

        def pre_condition(env):
            return True

        def post_condition(env):
            return env['a'] == env['b']

        def loop_invariant(env):
            return env['a'] == env['b']

        result = verify(pre_condition, ast, post_condition, loop_invariant)

        self.assertTrue(result)

    def test_given_example_1(self):
        program = "y := 0 ; while y < i do ( x := x + y ; if (x * y) < 10 then y := y + 1 else skip )"
        ast = WhileParser()(program)

        def pre_condition(env):
            return env['x'] > 0

        def post_condition(env):
            return env['x'] > 0

        def loop_invariant(env):
            # TODO: find the loop invariant
            from while_lang.example_loop_invariants import example_1_loop_invariant
            return example_1_loop_invariant(env)

        result = verify(pre_condition, ast, post_condition, loop_invariant)

        self.assertTrue(result)

    def test_given_example_2(self):
        program = "while a != b do if a > b then a := a - b else b := b - a"
        ast = WhileParser()(program)

        def pre_condition(env):
            return And(env['a'] > 0, env['b'] > 0)

        def post_condition(env):
            return And(env['a'] > 0, env['a'] == env['b'])

        def loop_invariant(env):
            # TODO: find the loop invariant
            from while_lang.example_loop_invariants import example_2_loop_invariant
            return example_2_loop_invariant(env)

        result = verify(pre_condition, ast, post_condition, loop_invariant)

        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
