# NexaLang Setup Guide

Welcome to NexaLang! This guide will help you set up the development environment after cloning the repository.

## Prerequisites

- Python 3.8 or higher
- Visual Studio Code (recommended for syntax highlighting)
- Git

## Quick Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/NexaLang.git
cd NexaLang
```

### 2. Set Up Python Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Install VS Code Extension (Recommended)

**Windows:**
```bash
install_vscode_extension.bat
```

**macOS/Linux:**
```bash
chmod +x install_vscode_extension.sh
./install_vscode_extension.sh
```

**Manual Installation:**
1. Open VS Code
2. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on macOS)
3. Type "Extensions: Install from VSIX..."
4. Navigate to `vscode-nexa/nexalang-0.3.2.vsix`
5. Reload VS Code

### 4. Verify Installation

Test the interpreter:
```bash
python src/nexa_interpreter.py examples/counter.nexa
```

Open any `.nexa` file in VS Code and verify syntax highlighting is working.

## What's Included

- **src/**: NexaLang interpreter source code
- **examples/**: Sample NexaLang programs
- **docs/**: Language documentation
- **tests/**: Test suite
- **vscode-nexa/**: VS Code extension for syntax highlighting
- **nexa** / **nexa.bat**: Convenience scripts to run the interpreter

## Next Steps

1. Read the [Language Overview](docs/overview.md)
2. Try the examples in the `examples/` directory
3. Run the test suite: `pytest`
4. Start writing your own NexaLang programs!

## Troubleshooting

### VS Code Extension Not Working
- Make sure you reloaded VS Code after installation
- Check that files have the `.nexa` extension
- Verify "NexaLang" appears in the language mode (bottom right of VS Code)

### Python Import Errors
- Ensure you activated the virtual environment
- Run `pip install -r requirements.txt` again

### Running Tests
- Make sure pytest is installed: `pip install pytest`
- Run from the project root: `pytest`

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on contributing to NexaLang. 