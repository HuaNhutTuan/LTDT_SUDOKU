@echo off
chcp 65001 > nul
echo ======================================================================
echo    KHOA CNTT - TRUONG DAI HOC SU PHAM TP. HO CHI MINH (HCMUE)
echo    DO AN LY THUYET DO THI: GIAI TRO CHOI SUDOKU BANG TO MAU DO THI
echo    Khoi chay Benchmark thuc nghiem 40 de (Thanh vien 5: Thuc nghiem & Media)
echo ======================================================================
cd ..
python Source/benchmark_runner.py
if errorlevel 1 (
    echo [THONG BAO] Neu lenh 'python' khong chay, dang thu goi trinh thuc thi Python he thong...
    py Source/benchmark_runner.py
)
echo.
echo ======================================================================
echo    Ket qua thuc nghiem da duoc xuat ra:
echo    - Release/benchmark_results.csv
echo    - Release/benchmark_summary.json
echo ======================================================================
pause
