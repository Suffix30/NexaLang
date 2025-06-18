from src.nexa_interpreter import Environment, tokenize, parse
import pytest

@pytest.fixture
def env():
    return Environment()

@pytest.fixture
def parse_code():
    def _parse(code):
        tokens = tokenize(code)
        return parse(tokens)
    return _parse

@pytest.fixture
def interpret_code(env):
    from src.nexa_interpreter import interpret
    def _interpret(code):
        tokens = tokenize(code)
        ast = parse(tokens)
        interpret(ast, env)
    return _interpret 