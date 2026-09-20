@echo off
setlocal
cd /d "%~dp0"

echo Installing runtime and build dependencies...
python -m pip install -r requirements.txt pyinstaller
if errorlevel 1 (
    echo Failed to install dependencies.
    exit /b 1
)

echo Building PhoenixCommand.exe...
python -m PyInstaller PhoenixCommand.spec --noconfirm --clean
if errorlevel 1 (
    echo Build failed.
    exit /b 1
)

if exist "dist\PhoenixCommand.exe" (
    echo.
    echo Build succeeded: dist\PhoenixCommand.exe
) else (
    echo Build finished but dist\PhoenixCommand.exe was not found.
    exit /b 1
)
