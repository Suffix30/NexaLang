# NexaLang

**Created by NET**

**Nexa** is a modern, multi-paradigm programming language designed for safety, expressiveness, and adaptability. It combines the safety of Rust, the simplicity of Python, and the concurrency of Erlang, with built-in support for AI-driven development and distributed systems. Whether you're building AI pipelines, cloud applications, or embedded systems, Nexa aims to empower developers with a unified, future-proof tool.

## Features

- **Type Safety**: Strong static typing with type inference
- **Concurrency**: Actor-based model for safe parallel execution
- **AI Integration**: Built-in AI optimization decorators
- **Error Handling**: Robust try-catch mechanisms
- **Modern Syntax**: Clean, expressive syntax inspired by Rust and Python

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Suffix30/NexaLang.git
   cd NexaLang
   ```

2. Set up Python environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # or
   source venv/bin/activate  # Linux/macOS
   pip install -r requirements.txt
   ```

## VS Code Extension

NexaLang comes with a VS Code extension for syntax highlighting and language support.

### Quick Install
1. Open VS Code
2. Press `Ctrl+Shift+P` and run "Extensions: Install from VSIX..."
3. Select `vscode-nexa/nexalang-0.3.2.vsix`
4. Reload VS Code

See [vscode-nexa/README.md](vscode-nexa/README.md) for more installation options.

## Usage

Run the NexaLang interpreter:
```bash
python src/nexa_interpreter.py examples/counter.nexa
```

Or use the REPL:
```bash
python src/nexa_interpreter.py
```

## Examples

See the `examples/` directory for sample NexaLang programs.

## Documentation

- [Language Overview](docs/overview.md)
- [Syntax Guide](docs/syntax.md)
- [Developer Guide](docs/developer_guide.md)
- [Quick Reference](docs/quick_reference.md)

## License
