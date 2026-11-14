"""
Điểm khởi chạy ứng dụng giao diện đồ họa (GUI) cho đề tài:
GIẢI TRÒ CHƠI SUDOKU BẰNG THUẬT TOÁN TÔ MÀU ĐỒ THỊ - KHOA CNTT, HCMUE.
Phụ trách: Thành viên 4 (Giao diện GUI & Trực quan hóa).
"""

import sys
import os

# Thêm đường dẫn gốc
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from Source.gui.sudoku_gui import main

if __name__ == "__main__":
    main()
