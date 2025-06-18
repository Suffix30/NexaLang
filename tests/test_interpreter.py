from src.nexa_interpreter import tokenize, parse, interpret, Environment
import unittest

class TestInterpreter(unittest.TestCase):
    def setUp(self):
        self.env = Environment()

    def test_variable_assignment(self):
        code = "let x: Int = 10;"
        tokens = tokenize(code)
        ast = parse(tokens)
        interpret(ast, self.env)
        
        value, type_ = self.env.get_var('x')
        self.assertEqual(value, 10)
        self.assertEqual(type_, 'Int')

    def test_function_call(self):
        code = """
        let x: Int = 5;
        let y: Int = 3;
        let result: Int = math.add(x, y);
        """
        tokens = tokenize(code)
        ast = parse(tokens)
        interpret(ast, self.env)
        
        value, _ = self.env.get_var('result')
        self.assertEqual(value, 8)

    def test_try_catch_block(self):
        code = """
        try {
            say "In try block";
        } catch {
            say "In catch block";
        }
        """
        tokens = tokenize(code)
        ast = parse(tokens)
        interpret(ast, self.env)

    def test_actor_message_passing(self):
        code = """
        actor Counter {
            state count: Int = 0;
        }
        let counter = Counter.spawn();
        """
        tokens = tokenize(code)
        ast = parse(tokens)
        interpret(ast, self.env)

    def test_math_operations(self):
        code = """
        let a: Int = 10;
        let b: Int = 5;
        let sum: Int = math.add(a, b);
        let diff: Int = math.subtract(a, b);
        let prod: Int = math.multiply(a, b);
        """
        tokens = tokenize(code)
        ast = parse(tokens)
        interpret(ast, self.env)
        
        self.assertEqual(self.env.get_var('sum')[0], 15)
        self.assertEqual(self.env.get_var('diff')[0], 5)
        self.assertEqual(self.env.get_var('prod')[0], 50)

if __name__ == '__main__':
    unittest.main() 