@echo off
chcp 65001 >nul
title Khởi chạy Web Demo - Giải Sudoku bằng Tô màu Đồ thị (HCMUE)
echo =======================================================================
echo   ĐỒ ÁN LÝ THUYẾT ĐỒ THỊ VÀ ỨNG DỤNG - KHOA CNTT - HCMUE
echo   SẢN PHẨM DEMO THỰC TẾ: SUDOKU GRAPH COLORING WEB DEMO
echo =======================================================================
echo.
echo Đang mở giao diện Web Demo tương tác trên trình duyệt mặc định...
start "" "%~dp0web_demo\index.html"
echo.
echo Giao diện Web Demo đã được kích hoạt!
echo Bạn có thể trực tiếp trải nghiệm 4 chức năng sản phẩm thực tế:
echo   1. Sinh đề ngẫu nhiên đối xứng tâm 4 cấp độ (Game Generator).
echo   2. Kiểm tra xung đột thời gian thực trên 20 đỉnh kề (Game Validator).
echo   3. Thẩm định khả giải và đếm số nghiệm (Solvability Checker).
echo   4. Gợi ý nước đi sư phạm theo Heuristic DSATUR (Hint Engine).
echo   5. Mô phỏng giải từng bước (Step-by-step) và Giải siêu tốc (0.01s).
echo.
pause
