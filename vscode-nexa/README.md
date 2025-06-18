# NexaLang VS Code Extension

**Created by NET**

This extension provides syntax highlighting and language support for NexaLang (.nexa files).

## Features

- Syntax highlighting for NexaLang keywords, types, strings, comments, and operators
- Auto-closing brackets and quotes
- Comment toggling (Ctrl+/)
- Bracket matching
- Code snippets for common patterns

## Installation

### Option 1: Install from VSIX (Recommended)

1. Open VS Code
2. Press `Ctrl+Shift+P` to open Command Palette
3. Type "Extensions: Install from VSIX..." and select it
4. Navigate to `vscode-nexa/nexalang-0.3.2.vsix` and select it
5. Reload VS Code when prompted

### Option 2: Build and Install from Source

1. Make sure you have Node.js installed
2. Install vsce globally:
   ```bash
   npm install -g @vscode/vsce
   ```
3. Navigate to the extension directory:
   ```bash
   cd vscode-nexa
   ```
4. Package the extension:
   ```bash
   vsce package --no-dependencies
   ```
5. Install the generated VSIX file:
   ```bash
   code --install-extension nexalang-0.3.2.vsix
   ```

### Option 3: Development Install (For Contributors)

For development, you can create a symbolic link to the extension:

**Windows (PowerShell as Administrator):**
```powershell
New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.vscode\extensions\nexalang-dev" -Target "$(pwd)\vscode-nexa"
```

**macOS/Linux:**
```bash
ln -s "$(pwd)/vscode-nexa" ~/.vscode/extensions/nexalang-dev
```

Then reload VS Code.

## Usage

Once installed, the extension will automatically activate for any file with the `.nexa` extension. You should see:
- Syntax highlighting
- "NexaLang" in the language mode indicator (bottom right of VS Code)

## Troubleshooting

If syntax highlighting doesn't work:
1. Make sure the file has a `.nexa` extension
2. Check that "NexaLang" appears in the language mode selector (bottom right)
3. Try reloading VS Code (`Ctrl+Shift+P` → "Developer: Reload Window")

## Development

To modify the extension:
1. Edit files in this directory
2. Test changes by reloading VS Code
3. Package a new version with `vsce package`

### File Structure
- `package.json` - Extension manifest
- `syntaxes/nexa.tmLanguage.json` - Syntax highlighting rules
- `language-configuration.json` - Language configuration
- `snippets/nexa.json` - Code snippets

## Supported Language Features

- Variable declarations with type annotations
- Function declarations with parameters and return types
- AI optimization decorators (`