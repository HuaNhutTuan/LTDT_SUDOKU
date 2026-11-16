@echo off
chcp 65001 > nul
echo ======================================================================
echo    KHOA CNTT - TRUONG DAI HOC SU PHAM TP. HO CHI MINH (HCMUE)
echo    DO AN LY THUYET DO THI: GIAI TRO CHOI SUDOKU BANG TO MAU DO THI
echo    Khoi chay Benchmark thuc nghiem 40 de (Thanh vien 5: Thuc nghiem & Media)
echo ======================================================================
cd /d "%~dp0\.."

set "PY_CMD="

python --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set "PY_CMD=python"
)

if not defined PY_CMD (
    py --version >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        set "PY_CMD=py"
    )
)

if not defined PY_CMD (
    if exist "C:\msys64\ucrt64\bin\python.exe" (
        set "PY_CMD=C:\msys64\ucrt64\bin\python.exe"
    )
)

if not defined PY_CMD (
    for /d %%D in ("%LOCALAPPDATA%\Programs\Python\Python*") do (
        if exist "%%D\python.exe" set "PY_CMD=%%D\python.exe"
    )
)

if not defined PY_CMD (
    for /d %%D in ("C:\Program Files\Python*") do (
        if exist "%%D\python.exe" set "PY_CMD=%%D\python.exe"
    )
)

if not defined PY_CMD (
    echo [LOI] Khong tim thay Python tren he thong!
    echo Vui long cai dat Python hoac kiem tra bien moi truong PATH.
    pause
    exit /b 1
)

"%PY_CMD%" Source/benchmark_runner.py
echo.
echo ======================================================================
echo    Ket qua thuc nghiem da duoc xuat ra:
echo    - Release/benchmark_results.csv
echo    - Release/benchmark_summary.json
echo ======================================================================
pause
