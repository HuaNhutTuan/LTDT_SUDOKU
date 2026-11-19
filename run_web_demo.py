"""
Tập lệnh mở giao diện Web Demo tương tác đồ án Sudoku Tô màu đồ thị.
Khoa CNTT - Trường ĐH Sư Phạm TP.HCM.
"""

import os
import sys
import webbrowser

def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    web_demo_path = os.path.join(root_dir, "Release", "web_demo", "index.html")
    
    if not os.path.exists(web_demo_path):
        print(f"Lỗi: Không tìm thấy file {web_demo_path}")
        sys.exit(1)
        
    print("=" * 70)
    print("  ĐỒ ÁN LÝ THUYẾT ĐỒ THỊ VÀ ỨNG DỤNG - KHOA CNTT - HCMUE")
    print("  KHỞI CHẠY SẢN PHẨM WEB DEMO TÔ MÀU ĐỒ THỊ SUDOKU")
    print("=" * 70)
    print(f"Đang mở tệp: {web_demo_path}")
    webbrowser.open(f"file:///{os.path.abspath(web_demo_path)}")
    print("Đã mở giao diện trên trình duyệt mặc định thành công!")

if __name__ == "__main__":
    main()
