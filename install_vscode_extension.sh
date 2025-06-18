#!/bin/bash
# Install NexaLang VS Code Extension

echo "Installing NexaLang VS Code Extension..."

if ! command -v code &> /dev/null; then
    echo "Error: VS Code command line tools not found."
    echo "Please install VS Code and ensure 'code' command is available in PATH."
    exit 1
fi

if [ -f "vscode-nexa/nexalang-0.1.0.vsix" ]; then
    code --install-extension vscode-nexa/nexalang-0.1.0.vsix
    echo "NexaLang extension installed successfully!"
    echo "Please reload VS Code to activate the extension."
else
    echo "Error: VSIX file not found at vscode-nexa/nexalang-0.1.0.vsix"
    echo "Please ensure you're running this script from the NexaLang root directory."
    exit 1
fi 