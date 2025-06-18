# NexaLang Developer Guide

This guide is for developers who want to understand, extend, or contribute to the NexaLang interpreter.

## Architecture Overview

The NexaLang interpreter consists of four main components:

### 1. Lexer (Tokenizer)
- **Function**: `tokenize(code: str) -> List[tuple[List[Any], int]]`
- **Purpose**: Converts source code into tokens
- **Location**: `src/nexa_interpreter.py`

The lexer uses regular expressions to match patterns in the source code and convert them into tokens. Each token includes:
- Token type and associated data
- Line number for error reporting

### 2. Parser
- **Function**: `parse(tokens: List[tuple[List[Any], int]]) -> List[Node]`
- **Purpose**: Converts tokens into an Abstract Syntax Tree (AST)
- **Location**: `src/nexa_interpreter.py`

The parser implements a recursive descent parser that builds AST nodes from tokens. It handles:
- Statement parsing
- Expression parsing
- Nested structures (functions, actors, control flow)

### 3. Type Checker
- **Function**: `type_check(ast: List[Node], env: Environment)`
- **Purpose**: Validates types and variable usage
- **Location**: `src/nexa_interpreter.py`

The type checker ensures:
- Variables are declared before use
- Type consistency in operations
- Function parameter and return type matching

### 4. Interpreter
- **Function**: `interpret(ast: List[Node], env: Environment)`
- **Purpose**: Executes the AST
- **Location**: `src/nexa_interpreter.py`

The interpreter:
- Maintains an environment for variables and functions
- Executes statements sequentially
- Handles control flow and function calls
- Manages actor instances and message passing

## AST Node Types

All AST nodes inherit from the base `Node` class and use Python dataclasses:

```python
@dataclass(kw_only=True)
class Node:
    line: int = 0
```

### Statement Nodes
- `LetStmt`: Variable declaration
- `AssignStmt`: Variable assignment
- `FnDecl`: Function declaration
- `ActorDecl`: Actor declaration
- `SpawnStmt`: Actor spawning
- `SendStmt`: Message sending
- `IfStmt`: Conditional statement
- `ForStmt`: For loop
- `WhileStmt`: While loop
- `TryStmt`: Try-catch block
- `SayStmt`: Output statement
- `ReturnStmt`: Function return

### Expression Nodes
- `CallExpr`: Function call expression

## Environment Management

The `Environment` class manages:
- Variable storage: `vars: Dict[str, Any]`
- Function storage: `fns: Dict[str, FnDecl]`
- Actor definitions: `actors: Dict[str, ActorDecl]`
- Standard library: `stdlib: Dict[str, Callable]`

## Adding New Features

### Adding a New Statement Type

1. **Define the AST Node**:
```python
@dataclass(kw_only=True)
class NewStmt(Node):
    # Add fields specific to your statement
    field1: str
    field2: int
    line: int = 0
```

2. **Update the Lexer**:
Add a pattern to the `patterns` list in `tokenize()`:
```python
(r'new\s+pattern', lambda m: ['NEW_TOKEN', m.group(1)]),
```

3. **Update the Parser**:
Add parsing logic in the `parse()` function:
```python
elif token[0] == 'NEW_TOKEN':
    ast.append(NewStmt(field1=token[1], field2=token[2], line=line))
    i += 1
```

4. **Update the Interpreter**:
Add execution logic in the `interpret()` function:
```python
elif isinstance(node, NewStmt):
    # Handle the new statement
    print(f"Executing new statement: {node.field1}")
```

### Adding a New Built-in Function

Add the function to the `stdlib` dictionary in `Environment.__init__()`:
```python
self.stdlib = {
    # ... existing functions ...
    'math.new_function': lambda x, y: x ** y,  # Example: power function
}
```

### Adding a New Type

1. Update type annotations throughout the codebase
2. Add type checking logic in `type_check()`
3. Update the grammar documentation

## Testing

### Unit Tests
Tests are organized by component:
- `tests/test_lexer.py`: Lexer tests
- `tests/test_parser.py`: Parser tests
- `tests/test_interpreter.py`: Interpreter tests

### Running Tests
```bash
python -m pytest tests/ -v --cov=src
```

### Adding Tests
Follow the existing pattern:
```python
def test_new_feature(self):
    code = """your NexaLang code"""
    tokens = tokenize(code)
    ast = parse(tokens)
    interpret(ast, self.env)
    # Add assertions
```

## Code Style

- Use type hints for all functions
- Follow PEP 8 style guidelines
- Add docstrings for complex functions
- Use meaningful variable names
- Keep functions focused and single-purpose

## Common Patterns

### Error Handling
```python
if condition_not_met:
    raise RuntimeError(f"Error message at line {node.line}")
```

### Debug Output
```python
print(f"Processing node: {type(node).__name__}")
```

### Pattern Matching
```python
if isinstance(node, SpecificNodeType):
    # Handle specific node type
```

## Debugging Tips

1. **Enable Debug Prints**: The interpreter includes many `print()` statements for debugging
2. **Check Token Output**: Use `tokenize()` directly to see token generation
3. **Inspect AST**: Print the AST after parsing to verify structure
4. **Step Through Execution**: Follow the interpreter's execution flow with debug prints

## Future Enhancements

Potential areas for extension:
- Additional types (Float, String, Bool)
- More operators (-, *, /, %)
- Advanced control flow (switch/case)
- Module system
- Type inference
- Optimization passes
- Code generation backends

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Update documentation
6. Submit a pull request

For questions or discussions, open an issue on the project repository. 