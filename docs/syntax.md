# NexaLang Syntax Guide

This guide covers all syntax elements in NexaLang with examples.

## Variables

### Declaration
Variables must be declared with explicit types:
```nexa
let x: Int = 5;
let count: Int = 0;
```

### Assignment
Variables can be reassigned or modified:
```nexa
x = 10;        // Simple assignment
count += 1;    // Compound assignment
```

## Functions

### Basic Function
```nexa
fn add(a: Int, b: Int) -> Int {
    return a + b;
}
```

### AI-Optimized Function
Functions can be marked for AI optimization:
```nexa
@ai.optimize
fn compute(x: Int, y: Int) -> Int {
    return x * y;
}
```

### Function Calls
```nexa
let result: Int = add(5, 3);
let value: Int = math.multiply(x, 2);
```

## Control Flow

### If/Else Statements
```nexa
if x > 5 {
    say "x is greater than 5";
} else {
    say "x is 5 or less";
}
```

### For Loops
```nexa
for i in range(5) {
    say "Iteration: {i}";
}
```

### While Loops
```nexa
while count > 0 {
    count += -1;
    say "Counting down...";
}
```

## Error Handling

### Try-Catch Blocks
```nexa
try {
    let x: Int = 5;
    let y: Int = 0;
    let z: Int = math.divide(x, y);
} catch {
    say "Error: Division by zero!";
}
```

## Output

### Say Statements
```nexa
say "Hello, World!";
say "The value is: {x}";
say "Result: {math.add(x, y)}";
```

## Actors (Concurrency)

### Actor Declaration
```nexa
actor Counter {
    state count: Int = 0;
    
    fn handle(msg: Int) {
        count += msg;
        say "Count is now: {count}";
    }
}
```

### Spawning Actors
```nexa
let counter = Counter.spawn();
```

### Sending Messages
```nexa
counter.send(5);
counter.send(math.add(2, 3));
```

## Standard Library

### Math Operations
```nexa
let sum: Int = math.add(x, y);
let diff: Int = math.subtract(x, y);
let product: Int = math.multiply(x, y);
let quotient: Int = math.divide(x, y);  // Safe division
```

## Type System

### Available Types
- `Int`: Integer values
- Actor types: e.g., `Counter` for actor instances

### Type Annotations
All variables and function parameters require type annotations:
```nexa
let x: Int = 5;
fn process(value: Int) -> Int { ... }
```

## Complete Example

Here's a complete program demonstrating various features:

```nexa
@ai.optimize
fn factorial(n: Int) -> Int {
    if n > 1 {
        return n * factorial(n + -1);
    } else {
        return 1;
    }
}

actor Calculator {
    state result: Int = 0;
    
    fn compute(n: Int) {
        result = factorial(n);
        say "Factorial result: {result}";
    }
}

// Main program
let calc = Calculator.spawn();

try {
    for i in range(5) {
        calc.send(i);
    }
} catch {
    say "Error in calculation!";
}
```

## Grammar Reference

For the formal grammar specification, see [nexa_grammar.ebnf](nexa_grammar.ebnf).