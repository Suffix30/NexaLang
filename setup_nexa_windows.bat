@echo off
echo Setting up NexaLang file associations...

REM Create registry entries for .nexa file extension
reg add "HKEY_CLASSES_ROOT\.nexa" /ve /d "NexaLang.File" /f
reg add "HKEY_CLASSES_ROOT\NexaLang.File" /ve /d "NexaLang Script" /f
reg add "HKEY_CLASSES_ROOT\NexaLang.File\DefaultIcon" /ve /d "%SystemRoot%\System32\shell32.dll,152" /f

REM Set up the open command
set "PYTHON_PATH=%~dp0venv\Scripts\python.exe"
set "INTERPRETER_PATH=%~dp0src\nexa_interpreter.py"

reg add "HKEY_CLASSES_ROOT\NexaLang.File\shell\open\command" /ve /d "\"%PYTHON_PATH%\" \"%INTERPRETER_PATH%\" \"%%1\"" /f
reg add "HKEY_CLASSES_ROOT\NexaLang.File\shell\edit\command" /ve /d "\"%%ProgramFiles%%\Microsoft VS Code\Code.exe\" \"%%1\"" /f

echo.
echo File associations created successfully!
echo.
echo You can now:
echo - Double-click .nexa files to run them
echo - Right-click and "Edit" to open in VS Code
echo.
pause 