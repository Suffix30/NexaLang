# NexaLang Overview

**Created by NET**

NexaLang is a custom programming language designed for safe, concurrent, and AI-optimized execution. It emphasizes simplicity, type safety, and debuggability while providing powerful features for modern programming needs.

## Philosophy

NexaLang was created with the following principles in mind:

1. **Type Safety**: All variables must be explicitly typed, preventing runtime type errors
2. **Error Handling**: Built-in try-catch blocks for robust error management
3. **Concurrency**: Actor-based model for safe concurrent programming
4. **AI Optimization**: Functions can be marked for AI optimization with `@ai.optimize`
5. **Simplicity**: Clean, readable syntax inspired by modern languages
6. **Debuggability**: Clear error messages with line numbers and execution tracing

## Core Features

### Variables and Types
- Strong typing with `Int` as the primary type
- Explicit variable declarations using `let`
- Support for assignment (`=`) and compound assignment (`+=`)

### Functions
- First-class functions with parameters and return types
- AI optimization support via `@ai.optimize` decorator
- Local variable scoping

### Control Flow
- Conditional statements (`if`/`else`)
- Loop constructs (`for`, `while`)
- Exception handling (`try`/`catch`)

### Concurrency
- Actor-based concurrency model
- Message passing between actors
- Thread-safe state management

### Standard Library
- Built-in math operations: `math.add`, `math.subtract`, `math.multiply`, `math.divide`
- Safe division with infinity handling

## Use Cases

NexaLang is ideal for:
- Educational purposes: Learning programming concepts
- Experimental AI optimization research
- Distributed systems prototyping
- Safe concurrent programming
- Domain-specific applications requiring custom language features

## Getting Started

See the [README](../README.md) for installation and setup instructions. Check out the [syntax guide](syntax.md) for language details and the [examples](../examples/) directory for sample programs.