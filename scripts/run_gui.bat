@echo off
rem ============================================================
rem run_gui.bat — jalankan dashboard ASV (Windows).
rem Pakai .venv hasil scripts\setup_windows.bat.
rem ============================================================
setlocal
cd /d "%~dp0.."

if not exist ".venv\Scripts\python.exe" (
    echo   .venv belum ada. Jalankan dulu: scripts\setup_windows.bat
    exit /b 1
)

".venv\Scripts\python.exe" -O main.py
exit /b %errorlevel%
