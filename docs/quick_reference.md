# NexaLang Quick Reference

## Variables
```nexa
let x: Int = 5;          // Declaration
x = 10;                  // Assignment
x += 5;                  // Compound assignment
```

## Functions
```nexa
fn add(a: Int, b: Int) -> Int {
    return a + b;
}

@ai.optimize             // AI optimization
fn compute(x: Int) -> Int {
    return x * 2;
}

let result: Int = add(5, 3);  // Function call
```

## Control Flow
```nexa
// If-else
if x > 5 {
    say "Greater";
} else {
    say "Less or equal";
}

// For loop
for i in range(5) {
    say "i = {i}";
}

// While loop
while x > 0 {
    x += -1;
}
```

## Error Handling
```nexa
try {
    // Code that might fail
    let z: Int = math.divide(x, 0);
} catch {
    say "Error occurred!";
}
```

## Output
```nexa
say "Hello, World!";
say "x = {x}";
say "Sum: {math.add(x, y)}";
```

## Actors (Concurrency)
```nexa
actor Counter {
    state count: Int = 0;
    
    fn handle(msg: Int) {
        count += msg;
    }
}

let c = Counter.spawn();
c.send(5);
```

## Math Operations
```nexa
math.add(x, y)       // Addition
math.subtract(x, y)  // Subtraction
math.multiply(x, y)  // Multiplication
math.divide(x, y)    // Division (safe)
```

## Type Annotations
- `Int` - Integer type
- Actor types (e.g., `Counter`)

## Keywords
`let`, `fn`, `return`, `if`, `else`, `for`, `while`, `try`, `catch`, `say`, `actor`, `state`, `spawn`, `send`, `in`, `range`

## Operators
- `=` - Assignment
- `+=` - Addition assignment
- `>` - Greater than (in conditions)

## Special Syntax
- `@ai.optimize` - AI optimization decorator
- `{expression}` - Expression interpolation in strings
- `;` - Statement terminator