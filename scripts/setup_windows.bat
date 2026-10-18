@echo off
rem ============================================================
rem setup_windows.bat — sekali jalan saat pertama kali di laptop.
rem Buat .venv, install dependensi, verifikasi env.
rem Wajib: Python 3.12+ 64-bit sudah terpasang (python.org).
rem ============================================================
setlocal
cd /d "%~dp0.."

echo [1/4] Cek Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo   ERROR: python tidak ditemukan di PATH. Install Python 3.12+ dari python.org.
    exit /b 1
)
python --version

echo [2/4] Buat .venv...
if not exist ".venv\Scripts\python.exe" (
    python -m venv .venv
    if errorlevel 1 (
        echo   ERROR: gagal membuat .venv
        exit /b 1
    )
)

echo [3/4] Install dependensi (butuh internet)...
".venv\Scripts\python.exe" -m pip install --upgrade pip -q
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (
    echo   ERROR: pip install gagal. Cek koneksi internet / versi Python (harus 3.12+ 64-bit).
    exit /b 1
)

echo [4/4] Verifikasi...
".venv\Scripts\python.exe" scripts\verify_env.py
if errorlevel 1 (
    echo   ERROR: verifikasi gagal.
    exit /b 1
)

echo.
echo SETUP SELESAI. Jalankan aplikasi: scripts\run_gui.bat
exit /b 0
