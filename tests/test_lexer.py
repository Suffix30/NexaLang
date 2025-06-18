from src.nexa_interpreter import tokenize
import unittest

class TestLexer(unittest.TestCase):
    def test_variable_declaration(self):
        code = "let x: Int = 5;"
        tokens = tokenize(code)
        self.assertEqual(tokens[0][0], ['LET', 'x', 'Int', 5])
        self.assertEqual(tokens[0][1], 1)

    def test_ai_optimize(self):
        code = """@ai.optimize
fn add(a: Int, b: Int) -> Int {
    return a + b;
}"""
        tokens = tokenize(code)
        self.assertEqual(tokens[0][0], ['AI_OPTIMIZE'])
        self.assertEqual(tokens[1][0], ['FN_START', 'add', 'a: Int, b: Int', False, 'Int'])

    def test_actor_declaration(self):
        code = """actor Counter {
    state count: Int = 0;
}"""
        tokens = tokenize(code)
        self.assertEqual(tokens[0][0], ['ACTOR_START', 'Counter'])
        self.assertEqual(tokens[1][0], ['STATE', 'count', 0])

    def test_try_catch(self):
        code = """try {
    say "Testing...";
} catch {
    say "Error!";
}"""
        tokens = tokenize(code)
        self.assertEqual(tokens[0][0], ['TRY_START'])
        self.assertEqual(tokens[1][0], ['SAY_SIMPLE', 'Testing...'])
        self.assertEqual(tokens[2][0], ['CATCH_START'])
        self.assertEqual(tokens[3][0], ['SAY_SIMPLE', 'Error!'])

    def test_assignment(self):
        code = "x = 10;"
        tokenize(code)

    def test_increment(self):
        code = "x += 5;"
        tokens = tokenize(code)
        self.assertEqual(tokens[0][0], ['ASSIGN', 'x', '+=', '5'])

    def test_invalid_syntax(self):
        code = "invalid syntax here"
        with self.assertRaises(SyntaxError):
            tokenize(code)

if __name__ == '__main__':
    unittest.main() 