@echo off
REM Install NexaLang VS Code Extension

echo Installing NexaLang VS Code Extension...

REM Check if VS Code is installed
where code >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Error: VS Code command line tools not found.
    echo Please install VS Code and ensure 'code' command is available in PATH.
    exit /b 1
)

REM Install the extension from VSIX
if exist "vscode-nexa\nexalang-0.1.0.vsix" (
    code --install-extension vscode-nexa\nexalang-0.1.0.vsix
    echo NexaLang extension installed successfully!
    echo Please reload VS Code to activate the extension.
) else (
    echo Error: VSIX file not found at vscode-nexa\nexalang-0.1.0.vsix
    echo Please ensure you're running this script from the NexaLang root directory.
    exit /b 1
) 