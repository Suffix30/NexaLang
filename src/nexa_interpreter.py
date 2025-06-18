import re
from dataclasses import dataclass
from typing import Dict, List, Any, Optional, Union
from queue import Queue, Empty
import threading
import time

@dataclass(kw_only=True)
class Node:
    line: int = 0

@dataclass(kw_only=True)
class LetStmt(Node):
    name: str
    value: Union[int, 'CallExpr', None]
    type: str
    line: int = 0

@dataclass(kw_only=True)
class ReturnStmt(Node):
    value: Union[int, 'CallExpr']
    line: int = 0

@dataclass(kw_only=True)
class SendStmt(Node):
    actor_var: str
    msg: Union[int, 'CallExpr']
    line: int = 0

@dataclass(kw_only=True)
class FnDecl(Node):
    name: str
    params: List[tuple[str, str]]
    return_type: str
    body: List[Node]
    ai_optimized: bool = False
    line: int = 0

@dataclass(kw_only=True)
class ActorDecl(Node):
    name: str
    state: List[Node]
    methods: List[FnDecl]
    line: int = 0

@dataclass(kw_only=True)
class IfStmt(Node):
    condition: str
    then_body: List[Node]
    else_body: List[Node]
    line: int = 0

@dataclass(kw_only=True)
class ForStmt(Node):
    var: str
    start: int
    end: int
    body: List[Node]
    line: int = 0

@dataclass(kw_only=True)
class WhileStmt(Node):
    condition: str
    body: List[Node]
    line: int = 0

@dataclass(kw_only=True)
class TryStmt(Node):
    try_body: List[Node]
    catch_body: List[Node]
    line: int = 0

@dataclass(kw_only=True)
class SayStmt(Node):
    value: str
    line: int = 0

@dataclass(kw_only=True)
class SpawnStmt(Node):
    actor_name: str
    var_name: str = ""
    line: int = 0

@dataclass(kw_only=True)
class CallExpr(Node):
    fn_name: str
    args: List[Union[str, int]]
    line: int = 0

@dataclass(kw_only=True)
class AssignStmt(Node):
    name: str
    op: str
    value: Union[str, int]
    line: int = 0

class Environment:
    def __init__(self):
        self.vars: Dict[str, Any] = {}
        self.fns: Dict[str, FnDecl] = {}
        self.actors: Dict[str, ActorDecl] = {}
        self.stdlib = {
            'math.add': lambda x, y: x + y,
            'math.subtract': lambda x, y: x - y,
            'math.multiply': lambda x, y: x * y,
            'math.divide': lambda x, y: x / y if y != 0 else float('inf')
        }

    def set_var(self, name: str, value: Any, type: str):
        self.vars[name] = (value, type)

    def get_var(self, name: str) -> tuple[Any, str]:
        if name not in self.vars:
            raise RuntimeError(f"Undefined variable: {name}")
        return self.vars[name]

    def set_fn(self, fn: FnDecl):
        self.fns[fn.name] = fn

    def get_fn(self, name: str) -> FnDecl:
        if name not in self.fns:
            raise RuntimeError(f"Undefined function: {name}")
        return self.fns[name]

    def set_actor(self, actor: ActorDecl):
        self.actors[actor.name] = actor

    def get_actor(self, name: str) -> ActorDecl:
        if name not in self.actors:
            raise RuntimeError(f"Undefined actor: {name}")
        return self.actors[name]

class ActorInstance:
    def __init__(self, actor: ActorDecl, env: Environment):
        self.actor = actor
        self.env = env
        self.state = {}
        self.msg_queue = Queue()
        self.thread = threading.Thread(target=self._process_messages)
        self.thread.daemon = True
        self.thread.start()

    def send(self, msg: Any):
        self.msg_queue.put(msg)

    def _process_messages(self):
        while True:
            try:
                msg = self.msg_queue.get(timeout=1)
                for method in self.actor.methods:
                    if method.name == 'on_message':
                        local_env = Environment()
                        local_env.vars = self.env.vars.copy()
                        local_env.fns = self.env.fns.copy()
                        local_env.stdlib = self.env.stdlib
                        local_env.set_var('msg', msg, 'Any')
                        interpret(method.body, local_env)
                        self.state.update(local_env.vars)
            except Empty:
                continue
            except Exception as e:
                print(f"Error processing message: {e}")
                continue

def tokenize(code: str) -> List[tuple[List[Any], int]]:
    tokens = []
    patterns = [
        (r'@ai\.optimize$', lambda m: ['AI_OPTIMIZE']),
        (r'let\s+([a-zA-Z0-9]+)\s*=\s*([a-zA-Z]+)\.spawn\s*\(\s*\)\s*;', lambda m: ['LET_SPAWN', m.group(1), m.group(2)]),
        (r'([a-zA-Z]+)\s*=\s*([a-zA-Z]+)\.spawn\s*\(\s*\)\s*;', lambda m: ['SPAWN', m.group(1), m.group(2)]),
        (r'let\s+([a-zA-Z]+)\s*:\s*Int\s*=\s*(\d+)\s*;', lambda m: ['LET', m.group(1), 'Int', int(m.group(2))]),
        (r'let\s+([a-zA-Z]+)\s*:\s*Int\s*=\s*([a-zA-Z0-9_\.]+)\s*\(([^)]*)\)\s*;', lambda m: ['LET_CALL', m.group(1), m.group(2), m.group(3).split(',')]),
        (r'([a-zA-Z]+)\s*\+=\s*([a-zA-Z0-9_]+)\s*;', lambda m: ['ASSIGN', m.group(1), '+=', m.group(2)]),
        (r'([a-zA-Z]+)\s*=\s*(\d+)\s*;', lambda m: ['ASSIGN', m.group(1), '=', int(m.group(2))]),
        (r'([a-zA-Z]+)\s*=\s*([a-zA-Z0-9_]+)\s*;', lambda m: ['ASSIGN', m.group(1), '=', m.group(2)]),
        (r'let\s+([a-zA-Z]+)\s*:\s*Int\s*=\s*([a-zA-Z]+)\s*/\s*([a-zA-Z]+)\s*;', lambda m: ['LET_CALL', m.group(1), 'math.divide', [m.group(2), m.group(3)]]),

        (r'fn\s+([a-zA-Z]+)\s*\(([^)]*)\)\s*->\s*Int\s*\{', lambda m: ['FN_START', m.group(1), m.group(2), False, 'Int']),
        (r'fn\s+([a-zA-Z]+)\s*\(([^)]*)\)\s*\{', lambda m: ['FN_START', m.group(1), m.group(2), False, 'Unit']),
        (r'if\s+([a-zA-Z]+)\s*>\s*(\d+)\s*\{', lambda m: ['IF_START', m.group(1), int(m.group(2))]),
        (r'else\s*\{', lambda m: ['ELSE_START']),
        (r'for\s+([a-zA-Z]+)\s+in\s+range\s*\(\s*(\d+)\s*\)\s*\{', lambda m: ['FOR_START', m.group(1), int(m.group(2))]),
        (r'while\s+([a-zA-Z]+)\s*>\s*(\d+)\s*\{', lambda m: ['WHILE_START', m.group(1), int(m.group(2))]),
        (r'try\s*\{', lambda m: ['TRY_START']),
        (r'\}\s*catch\s*\{', lambda m: ['CATCH_START']),
        (r'catch\s*\{', lambda m: ['CATCH_START']),
        (r'\}\s*', lambda m: ['BLOCK_END']),
        (r'return\s+([a-zA-Z]+)\s*\+\s*([a-zA-Z]+)\s*;', lambda m: ['RETURN_ADD', m.group(1), m.group(2)]),
        (r'return\s+([a-zA-Z]+)\s*\*\s*(\d+)\s*;', lambda m: ['RETURN_MUL', m.group(1), int(m.group(2))]),
        (r'return\s+([a-zA-Z]+)\s*;', lambda m: ['RETURN_VAR', m.group(1)]),
        (r'say\s+"([^"]*)\{([a-zA-Z]+)\(([^)]*)\)\}\s*"\s*;', lambda m: ['SAY', m.group(1), m.group(2), m.group(3).split(',')]),
        (r'say\s+"([^"]*)"\s*;', lambda m: ['SAY_SIMPLE', m.group(1)]),
        (r'actor\s+([a-zA-Z]+)\s*\{', lambda m: ['ACTOR_START', m.group(1)]),
        (r'state\s+([a-zA-Z]+)\s*:\s*Int\s*=\s*(\d+)\s*;', lambda m: ['STATE', m.group(1), int(m.group(2))]),
        (r'([a-zA-Z]+)\.send\s*\(\s*(\d+)\s*\)\s*;', lambda m: ['SEND', m.group(1), int(m.group(2))]),
        (r'([a-zA-Z]+)\.send\s*\(\s*([a-zA-Z]+)\(([^)]*)\)\s*\)\s*;', lambda m: ['SEND', m.group(1), m.group(2), m.group(3).split(',')]),
    ]
    
    lines = code.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        line_num = i + 1
        
        if not line:
            i += 1
            continue
            
        if line == '@ai.optimize' and i + 1 < len(lines):
            tokens.append((['AI_OPTIMIZE'], line_num))
            i += 1
            continue
            
        matched = False
        for pattern, handler in patterns:
            match = re.match(pattern, line)
            if match:
                token = handler(match)
                tokens.append((token, line_num))
                matched = True
                break
                
        if not matched:
            raise SyntaxError(f"Invalid syntax at line {line_num}: {line}")
            
        i += 1
        
    return tokens

def parse(tokens: List[tuple[List[Any], int]]) -> List[Node]:
    ast = []
    i = 0
    ai_optimized_next = False
    while i < len(tokens):
        token, line = tokens[i]
        if token[0] == 'AI_OPTIMIZE':
            ai_optimized_next = True
            i += 1
        elif token[0] == 'LET_SPAWN':
            ast.append(SpawnStmt(actor_name=token[2], var_name=token[1], line=line))
            i += 1
        elif token[0] == 'SPAWN':
            ast.append(SpawnStmt(actor_name=token[2], var_name=token[1], line=line))
            i += 1
        elif token[0] == 'LET':
            ast.append(LetStmt(name=token[1], type=token[2], value=token[3], line=line))
            i += 1
        elif token[0] == 'LET_CALL':
            ast.append(LetStmt(name=token[1], type='Int', value=CallExpr(fn_name=token[2], args=token[3], line=line), line=line))
            i += 1
        elif token[0] == 'ASSIGN':
            ast.append(AssignStmt(name=token[1], op=token[2], value=token[3], line=line))
            i += 1
        elif token[0] == 'SAY':
            ast.append(SayStmt(value=f"{token[1]}{token[2]}({','.join(map(str, token[3]))})", line=line))
            i += 1
        elif token[0] == 'SAY_SIMPLE':
            ast.append(SayStmt(value=token[1], line=line))
            i += 1
        elif token[0] == 'TRY_START':
            try_body = []
            i += 1
            while i < len(tokens) and tokens[i][0][0] != 'CATCH_START':
                inner_token, inner_line = tokens[i]
                if inner_token[0] == 'SAY':
                    try_body.append(SayStmt(value=f"{inner_token[1]}{inner_token[2]}({','.join(map(str, inner_token[3]))})", line=inner_line))
                elif inner_token[0] == 'SAY_SIMPLE':
                    try_body.append(SayStmt(value=inner_token[1], line=inner_line))
                elif inner_token[0] == 'LET':
                    try_body.append(LetStmt(name=inner_token[1], type=inner_token[2], value=inner_token[3], line=inner_line))
                elif inner_token[0] == 'LET_CALL':
                    try_body.append(LetStmt(name=inner_token[1], type='Int', value=CallExpr(fn_name=inner_token[2], args=inner_token[3], line=inner_line), line=inner_line))
                elif inner_token[0] == 'ASSIGN':
                    try_body.append(AssignStmt(name=inner_token[1], op=inner_token[2], value=inner_token[3], line=inner_line))
                i += 1
            catch_body = []
            i += 1
            while i < len(tokens) and tokens[i][0][0] != 'BLOCK_END':
                inner_token, inner_line = tokens[i]
                if inner_token[0] == 'SAY':
                    catch_body.append(SayStmt(value=f"{inner_token[1]}{inner_token[2]}({','.join(map(str, inner_token[3]))})", line=inner_line))
                elif inner_token[0] == 'SAY_SIMPLE':
                    catch_body.append(SayStmt(value=inner_token[1], line=inner_line))
                i += 1
            ast.append(TryStmt(try_body=try_body, catch_body=catch_body, line=line))
            i += 1
        elif token[0] == 'FN_START':
            params = []
            if token[2]:
                for param in token[2].split(','):
                    name, type_ = param.strip().split(':')
                    params.append((name.strip(), type_.strip()))
            body = []
            i += 1
            while i < len(tokens) and tokens[i][0][0] != 'BLOCK_END':
                inner_token, inner_line = tokens[i]
                if inner_token[0] == 'RETURN_ADD':
                    body.append(ReturnStmt(value=CallExpr(fn_name='math.add', args=[inner_token[1], inner_token[2]], line=inner_line), line=inner_line))
                elif inner_token[0] == 'RETURN_MUL':
                    body.append(ReturnStmt(value=CallExpr(fn_name='math.multiply', args=[inner_token[1], inner_token[2]], line=inner_line), line=inner_line))
                elif inner_token[0] == 'RETURN_VAR':
                    body.append(ReturnStmt(value=CallExpr(fn_name='identity', args=[inner_token[1]], line=inner_line), line=inner_line))
                i += 1
            ast.append(FnDecl(name=token[1], params=params, return_type=token[4], body=body, ai_optimized=ai_optimized_next or token[3], line=line))
            ai_optimized_next = False
            i += 1
        elif token[0] == 'ACTOR_START':
            state = []
            methods = []
            i += 1
            while i < len(tokens) and tokens[i][0][0] != 'BLOCK_END':
                inner_token, inner_line = tokens[i]
                if inner_token[0] == 'STATE':
                    state.append(LetStmt(name=inner_token[1], type='Int', value=inner_token[2], line=inner_line))
                    i += 1
                elif inner_token[0] == 'FN_START':
                    fn_name = inner_token[1]
                    params = []
                    if inner_token[2]:
                        for param in inner_token[2].split(','):
                            name, type_ = param.strip().split(':')
                            params.append((name.strip(), type_.strip()))
                    body = []
                    i += 1
                    while i < len(tokens) and tokens[i][0][0] != 'BLOCK_END':
                        body_token, body_line = tokens[i]
                        if body_token[0] == 'ASSIGN':
                            body.append(AssignStmt(name=body_token[1], op=body_token[2], value=body_token[3], line=body_line))
                        elif body_token[0] == 'SAY':
                            body.append(SayStmt(value=f"{body_token[1]}{body_token[2]}({','.join(map(str, body_token[3]))})", line=body_line))
                        elif body_token[0] == 'SAY_SIMPLE':
                            body.append(SayStmt(value=body_token[1], line=body_line))
                        i += 1
                    methods.append(FnDecl(name=fn_name, params=params, return_type=inner_token[4], body=body, ai_optimized=inner_token[3], line=inner_line))
                    i += 1
                else:
                    i += 1
            ast.append(ActorDecl(name=token[1], state=state, methods=methods, line=line))
            i += 1
        elif token[0] == 'SEND':
            if len(token) == 3:
                ast.append(SendStmt(actor_var=token[1], msg=token[2], line=line))
            else:
                ast.append(SendStmt(actor_var=token[1], msg=CallExpr(fn_name=token[2], args=token[3], line=line), line=line))
            i += 1
        else:
            i += 1
    return ast

def type_check(ast: List[Node], env: Environment):
    for node in ast:
        if isinstance(node, LetStmt):
            if node.type != 'Int' and node.type not in env.actors:
                raise TypeError(f"Unsupported type at line {node.line}: {node.type}")
            env.set_var(node.name, node.value, node.type)
        elif isinstance(node, FnDecl):
            env.set_fn(node)
            for param in node.params:
                if param[1] != 'Int':
                    raise TypeError(f"Unsupported param type at line {node.line}: {param[1]}")
            for stmt in node.body:
                if isinstance(stmt, IfStmt):
                    var, _ = stmt.condition.split('>')
                    if var not in env.vars:
                        raise TypeError(f"Undefined variable in if at line {stmt.line}: {var}")
                elif isinstance(stmt, ForStmt):
                    if stmt.var not in env.vars:
                        raise TypeError(f"Undefined loop variable at line {stmt.line}: {stmt.var}")
                elif isinstance(stmt, WhileStmt):
                    var, _ = stmt.condition.split('>')
                    if var not in env.vars:
                        raise TypeError(f"Undefined variable in while at line {stmt.line}: {var}")
                elif isinstance(stmt, TryStmt):
                    for try_stmt in stmt.try_body:
                        if isinstance(try_stmt, SayStmt):
                            pass
                    for catch_stmt in stmt.catch_body:
                        if isinstance(catch_stmt, SayStmt):
                            pass
                elif isinstance(stmt, ReturnStmt):
                    if not isinstance(stmt.value, CallExpr):
                        raise TypeError(f"Invalid return at line {stmt.line}")
                elif isinstance(stmt, CallExpr):
                    if stmt.fn_name not in env.fns and stmt.fn_name not in env.stdlib:
                        raise TypeError(f"Undefined function call at line {stmt.line}: {stmt.fn_name}")
        elif isinstance(node, ActorDecl):
            env.set_actor(node)
            local_env = Environment()
            for stmt in node.state:
                if isinstance(stmt, LetStmt):
                    local_env.set_var(stmt.name, stmt.value, stmt.type)
            for method in node.methods:
                if isinstance(method, FnDecl):
                    for param in method.params:
                        if param[1] != 'Int':
                            raise TypeError(f"Unsupported param type in actor at line {method.line}: {param[1]}")
        elif isinstance(node, SpawnStmt):
            env.get_actor(node.actor_name)
        elif isinstance(node, SendStmt):
            if node.actor_var not in env.vars:
                raise TypeError(f"Undefined actor variable at line {node.line}: {node.actor_var}")

def interpret(ast: List[Node], env: Environment):
    print("Interpreting AST...")
    for node in ast:
        print(f"Processing node: {type(node).__name__}")
        if isinstance(node, LetStmt):
            print(f"Setting variable {node.name} = {node.value}")
            if node.value is None:
                continue
            elif isinstance(node.value, CallExpr):
                if node.value.fn_name == 'identity':
                    value, _ = env.get_var(str(node.value.args[0]))
                else:
                    args = []
                    for arg in node.value.args:
                        if isinstance(arg, str):
                            arg_stripped = arg.strip()
                            if arg_stripped.isdigit():
                                args.append(int(arg_stripped))
                            else:
                                arg_value, _ = env.get_var(arg_stripped)
                                args.append(arg_value)
                        else:
                            args.append(arg)
                    if node.value.fn_name in env.stdlib:
                        value = env.stdlib[node.value.fn_name](*args)
                    else:
                        fn = env.get_fn(node.value.fn_name)
                        local_env = Environment()
                        local_env.stdlib = env.stdlib
                        for (param_name, param_type), arg_value in zip(fn.params, args):
                            local_env.set_var(param_name, arg_value, param_type)
                        result = None
                        for stmt in fn.body:
                            result = interpret([stmt], local_env)
                            if result is not None:
                                value = result
                                break
                        else:
                            value = 0
                env.set_var(node.name, value, node.type)
            else:
                env.set_var(node.name, node.value, node.type)
        elif isinstance(node, FnDecl):
            print(f"Defining function: {node.name}")
            env.set_fn(node)
        elif isinstance(node, AssignStmt):
            print(f"Assigning: {node.name} {node.op} {node.value}")
            if node.op == '+=':
                current_value, _ = env.get_var(str(node.name))
                if isinstance(node.value, str):
                    add_value, _ = env.get_var(str(node.value))
                    env.set_var(node.name, current_value + add_value, 'Int')
                else:
                    env.set_var(node.name, current_value + node.value, 'Int')
            else:
                if isinstance(node.value, str):
                    assign_val, _ = env.get_var(str(node.value))
                    env.set_var(node.name, assign_val, 'Int')
                else:
                    env.set_var(node.name, node.value, 'Int')
        elif isinstance(node, IfStmt):
            print(f"Evaluating if condition: {node.condition}")
            cond_var, cond_value = node.condition.split('>')
            var_value, _ = env.get_var(str(cond_var))
            if var_value > int(cond_value):
                interpret(node.then_body, env)
            else:
                interpret(node.else_body, env)
        elif isinstance(node, ForStmt):
            print(f"Starting for loop: {node.var} in range({node.end})")
            for i in range(node.start, node.end):
                env.set_var(node.var, i, 'Int')
                interpret(node.body, env)
        elif isinstance(node, WhileStmt):
            print(f"Starting while loop: {node.condition}")
            cond_var, cond_value = node.condition.split('>')
            while True:
                var_value, _ = env.get_var(str(cond_var))
                if var_value > int(cond_value):
                    interpret(node.body, env)
                else:
                    break
        elif isinstance(node, TryStmt):
            print("Starting try block")
            try:
                interpret(node.try_body, env)
            except (RuntimeError, ZeroDivisionError) as e:
                print(f"Caught exception: {e}")
                interpret(node.catch_body, env)
        elif isinstance(node, SayStmt):
            if '{' in node.value:
                parts = node.value.split('{')
                output = parts[0]
                for part in parts[1:]:
                    expr_end = part.find('}')
                    expr = part[:expr_end]
                    if '(' in expr:
                        fn_name = expr[:expr.find('(')]
                        args_str = expr[expr.find('(')+1:expr.find(')')]
                        args = []
                        for arg in args_str.split(','):
                            arg = arg.strip()
                            if arg.isdigit():
                                args.append(int(arg))
                            else:
                                arg_value, _ = env.get_var(arg)
                                args.append(arg_value)
                        if fn_name in env.stdlib:
                            result = env.stdlib[fn_name](*args)
                        else:
                            fn = env.get_fn(fn_name)
                            local_env = Environment()
                            local_env.stdlib = env.stdlib
                            for (param_name, param_type), arg_value in zip(fn.params, args):
                                local_env.set_var(param_name, arg_value, param_type)
                            result = 0
                            for stmt in fn.body:
                                res = interpret([stmt], local_env)
                                if res is not None:
                                    result = res
                                    break
                        output += str(result)
                    else:
                        value, _ = env.get_var(expr)
                        output += str(value)
                    output += part[expr_end+1:]
                print(f"Output: {output}")
            else:
                print(f"Output: {node.value}")
        elif isinstance(node, ActorDecl):
            print(f"Defining actor: {node.name}")
            env.set_actor(node)
        elif isinstance(node, SpawnStmt):
            print(f"Spawning actor: {node.actor_name}")
            actor = env.get_actor(node.actor_name)
            instance = ActorInstance(actor, env)
            if node.var_name:
                env.set_var(node.var_name, instance, node.actor_name)
        elif isinstance(node, SendStmt):
            print(f"Sending message to actor: {node.actor_var}")
            instance, _ = env.get_var(node.actor_var)
            if isinstance(node.msg, CallExpr):
                args = []
                for arg in node.msg.args:
                    if isinstance(arg, str):
                        arg_value, _ = env.get_var(arg)
                        args.append(arg_value)
                    else:
                        args.append(arg)
                result = env.stdlib[node.msg.fn_name](*args)
                instance.send(result)
            else:
                instance.send(node.msg)
        elif isinstance(node, ReturnStmt):
            if isinstance(node.value, CallExpr):
                if node.value.fn_name == 'identity':
                    value, _ = env.get_var(str(node.value.args[0]))
                    return value
                else:
                    args = []
                    for arg in node.value.args:
                        if isinstance(arg, str):
                            arg_value, _ = env.get_var(arg)
                            args.append(arg_value)
                        else:
                            args.append(arg)
                    if node.value.fn_name in env.stdlib:
                        return env.stdlib[node.value.fn_name](*args)
                    else:
                        fn = env.get_fn(node.value.fn_name)
                        local_env = Environment()
                        local_env.stdlib = env.stdlib
                        for (param_name, param_type), arg_value in zip(fn.params, args):
                            local_env.set_var(param_name, arg_value, param_type)
                        for stmt in fn.body:
                            result = interpret([stmt], local_env)
                            if result is not None:
                                return result
                        return 0
            else:
                return node.value

def repl():
    env = Environment()
    print("NexaLang REPL v0.1")
    print("Type 'exit' to quit")
    while True:
        try:
            code = input("nexa> ")
            if code == 'exit':
                break
            tokens = tokenize(code)
            ast = parse(tokens)
            type_check(ast, env)
            interpret(ast, env)
        except Exception as e:
            print(f"Error: {e}")

def run_nexa(code: str):
    try:
        tokens = tokenize(code)
        ast = parse(tokens)
        env = Environment()
        type_check(ast, env)
        interpret(ast, env)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            code = f.read()
        print(f"Executing file: {sys.argv[1]}")
        run_nexa(code)
    else:
        test_code = """
let x: Int = 10;
let y: Int = 20;

@ai.optimize
fn add(a: Int, b: Int) -> Int {
    return a + b;
}

say "Sum: {add(x, y)}";
"""
        print("Running test code...")
        run_nexa(test_code)