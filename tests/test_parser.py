from src.nexa_interpreter import tokenize, parse, LetStmt, FnDecl, ActorDecl, TryStmt
import unittest
from typing import cast

class TestParser(unittest.TestCase):
    def test_parse_variable_declaration(self):
        code = "let x: Int = 5;"
        tokens = tokenize(code)
        ast = parse(tokens)
        
        self.assertEqual(len(ast), 1)
        self.assertIsInstance(ast[0], LetStmt)
        node = cast(LetStmt, ast[0])
        self.assertEqual(node.name, 'x')
        self.assertEqual(node.type, 'Int')
        self.assertEqual(node.value, 5)

    def test_parse_function_declaration(self):
        code = """@ai.optimize
fn add(a: Int, b: Int) -> Int {
    return a + b;
}"""
        tokens = tokenize(code)
        ast = parse(tokens)
        
        self.assertEqual(len(ast), 1)
        self.assertIsInstance(ast[0], FnDecl)
        node = cast(FnDecl, ast[0])
        self.assertEqual(node.name, 'add')
        self.assertEqual(node.ai_optimized, True)
        self.assertEqual(len(node.params), 2)

    def test_parse_actor_declaration(self):
        code = """actor Counter {
    state count: Int = 0;
}"""
        tokens = tokenize(code)
        ast = parse(tokens)
        
        self.assertEqual(len(ast), 1)
        self.assertIsInstance(ast[0], ActorDecl)
        node = cast(ActorDecl, ast[0])
        self.assertEqual(node.name, 'Counter')
        self.assertEqual(len(node.state), 1)

    def test_parse_try_catch(self):
        code = """try {
    say "Testing...";
} catch {
    say "Error!";
}"""
        tokens = tokenize(code)
        ast = parse(tokens)
        
        self.assertEqual(len(ast), 1)
        self.assertIsInstance(ast[0], TryStmt)
        node = cast(TryStmt, ast[0])
        self.assertEqual(len(node.try_body), 1)
        self.assertEqual(len(node.catch_body), 1)

if __name__ == '__main__':
    unittest.main() 