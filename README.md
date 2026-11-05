# ĐỒ ÁN LÝ THUYẾT ĐỒ THỊ VÀ ỨNG DỤNG - HCMUE
## ĐỀ TÀI: GIẢI TRÒ CHƠI SUDOKU BẰNG THUẬT TOÁN TÔ MÀU ĐỒ THỊ
**Khoa Công nghệ Thông tin - Trường Đại học Sư phạm TP. Hồ Chí Minh**  
**Repository chính thức:** [https://github.com/HuaNhutTuan/LTDT_SUDOKU](https://github.com/HuaNhutTuan/LTDT_SUDOKU)  
**Nhóm trưởng (Thành viên 1):** Hứa Nhựt Tuấn (MSSV: 51.01.104.114)  

---

## 1. GIỚI THIỆU ĐỀ TÀI
Đồ án quy đổi bài toán giải trò chơi Sudoku 9x9 về bài toán **Tô màu đồ thị (Graph Coloring Problem)** và **Mở rộng tiền tô màu (Pre-coloring Extension)**:
- **Tập đỉnh $V$ (81 đỉnh):** Ánh xạ 1-1 với 81 ô tọa độ $(r, c)$ trên bàn cờ qua công thức:  
  $$v = r \times 9 + c \quad (r, c \in \{0..8\})$$
- **Tập cạnh $E$ (810 cạnh vô hướng):** Nối giữa hai đỉnh phân biệt nếu chúng nằm cùng hàng, cùng cột hoặc cùng khối con $3 \times 3$.
- **Tính chất đồ thị chính quy bậc 20 (20-regular graph):** Mọi đỉnh $v \in V$ đều có chính xác $\deg(v) = 20$ đỉnh kề:
  $$\deg(v) = 8 \text{ (cùng hàng)} + 8 \text{ (cùng cột)} + 4 \text{ (cùng khối } 3 \times 3 \text{ duy nhất)} = 20$$
  Tổng số cạnh: $|E| = (81 \times 20) / 2 = 810$ cạnh.
- **Sắc số của đồ thị:** $\chi(G) = 9$ (tương ứng với 9 màu số từ 1 đến 9).

---

## 2. CẤU TRÚC 3 THƯ MỤC NỘP BÀI CHUẨN KHOA CNTT - HCMUE

```text
LTDT_SUDOKU/
├── Document/                               # Thư mục Báo cáo & Tài liệu
│   ├── Bao_Cao_Tieu_Luan_Sudoku_To_Mau_Do_Thi.docx  # Báo cáo chuẩn thể thức HCMUE (A4, TNR 13pt, lề chuẩn)
│   ├── Noi_Dung_Bao_Cao_Phan_Mo_Dau_Va_Chuong_2.md  # Bản thảo chi tiết Mở đầu và Chương 2
│   └── Ke_Hoach_Thuc_Hien_Do_An_Sudoku_To_Mau_Do_Thi.docx # Bản kế hoạch phân công chi tiết 5 thành viên
├── Source/                                 # Toàn bộ mã nguồn chương trình
│   ├── main.py                             # Điểm khởi chạy Console minh họa lõi đồ thị
│   ├── core/                               # Lõi xử lý đồ thị (Graph Core)
│   │   ├── graph.py                        # Lớp Graph vô hướng tổng quát
│   │   ├── sudoku_graph.py                 # Lớp SudokuGraph (81 đỉnh, 810 cạnh, 20 đỉnh kề, DSATUR, tiền tô màu)
│   │   └── io_handler.py                   # Đọc/ghi đề bài Sudoku (ma trận 9x9, chuỗi 81 ký tự, dataset benchmark)
│   └── tests/                              # Bộ kiểm thử tự động (Unit Tests)
│       └── test_sudoku_graph.py            # Test nghiệm thu: 81 đỉnh, 810 cạnh, bậc 20, bắt lỗi tiền tô màu
└── Release/                                # Bản đóng gói thực thi & bộ dữ liệu mẫu
    ├── puzzles/                            # Các bộ đề kiểm thử 4 cấp độ khó
    │   ├── sample_easy.txt                 # Đề Dễ
    │   ├── sample_medium.txt               # Đề Trung bình
    │   ├── sample_hard.txt                 # Đề Khó
    │   └── sample_expert.txt               # Đề Chuyên gia (17 clues)
    └── run_console.bat                     # File thực thi chạy nhanh trên Windows
```

---

## 3. PHÂN CÔNG NHIỆM VỤ 5 THÀNH VIÊN

| STT | Thành viên & Vai trò | Module Code phụ trách | Báo cáo Tiểu luận | Trạng thái |
|:---:|:---|:---|:---|:---:|
| **1** | **Hứa Nhựt Tuấn** *(Nhóm trưởng)* | Lớp `SudokuGraph`, `IOHandler`, validate tiền tô màu, quản lý GitHub | Mở đầu, toàn bộ Chương 2, chuẩn hóa file Word | **Hoàn thành 100%** |
| **2** | **Thành viên 2** *(Tham lam & DSATUR)* | Hàm `WelshPowell()` & `DSATUR()`, cập nhật bậc bão hòa | Chương 1 (Mục 1.1, 1.2, 1.3.1, 1.3.2) | Đang thực hiện |
| **3** | **Thành viên 3** *(Backtrack & Generator)* | Hàm `BacktrackDSATUR()`, sinh đề `GeneratePuzzle()` 4 cấp độ | Chương 1 (Mục 1.3.3), Chương 3 (Mục 3.2, 3.3) | Đang thực hiện |
| **4** | **Thành viên 4** *(Giao diện GUI)* | Bàn cờ 9x9, highlight 20 đỉnh kề, step-by-step | Chương 3 (Mục 3.1, 3.4), Hướng dẫn sử dụng | Đang thực hiện |
| **5** | **Thành viên 5** *(Benchmark & Media)* | Bộ 40-100 đề test, đo thời gian/bước duyệt, đóng gói Release | Chương 4 (Thực nghiệm & Đánh giá), Slide, Video | Đang thực hiện |

---

## 4. HƯỚNG DẪN KẾ THỪA & SỬ DỤNG API CHO CÁC THÀNH VIÊN

Thành viên 2, 3, 4, 5 chỉ cần import và sử dụng trực tiếp các phương thức đã được Nhóm trưởng hoàn thiện trong `Source.core`:

```python
from Source.core.sudoku_graph import SudokuGraph, PrecoloringConflictError
from Source.core.io_handler import IOHandler

# 1. Khởi tạo đồ thị Sudoku (tự động dựng 81 đỉnh, 810 cạnh, bậc 20)
graph = SudokuGraph()

# 2. Nạp đề bài từ chuỗi hoặc file
graph.load_from_string("530070000600195000098000060800060003400803001700020006060000280000419005000080079")
# Hoặc: graph = IOHandler.read_puzzle_from_file("Release/puzzles/sample_easy.txt")

# 3. Lấy danh sách 20 đỉnh kề của ô (hàng 0, cột 0) -> Đỉnh 0
neighbors = graph.get_neighbors(0)  # len(neighbors) == 20

# 4. Tính bậc bão hòa DSATUR của một đỉnh
sat_degree = graph.get_saturation_degree(vertex=2)

# 5. Lấy tập các màu khả dụng trong {1..9} cho một đỉnh (MRV)
valid_colors = graph.get_available_colors(vertex=2)

# 6. Kiểm tra an toàn trước khi gán màu
if graph.is_safe(vertex=2, color=1):
    graph.assign_color(vertex=2, color=1)

# 7. Hủy màu (phục vụ quay lui của TV3)
graph.unassign_color(vertex=2)

# 8. Kiểm tra hoàn thành lời giải hợp lệ
if graph.is_complete():
    print("Sudoku đã giải thành công!")
```

---

## 5. QUY TRÌNH PHỐI HỢP GIT CHO TOÀN NHÓM

1. **Clone repository về máy:**
   ```bash
   git clone https://github.com/HuaNhutTuan/LTDT_SUDOKU.git
   cd LTDT_SUDOKU
   ```

2. **Quy ước đặt tên nhánh tính năng cho từng thành viên:**
   - TV2: `git checkout -b feature/tv2-greedy-dsatur`
   - TV3: `git checkout -b feature/tv3-backtracking-generator`
   - TV4: `git checkout -b feature/tv4-gui-visualization`
   - TV5: `git checkout -b feature/tv5-benchmark-tests`

3. **Chạy kiểm thử trước khi commit:**
   ```bash
   python -m unittest Source/tests/test_sudoku_graph.py
   python Source/main.py
   ```

4. **Đẩy code lên nhánh của mình và tạo Pull Request (PR):**
   ```bash
   git add .
   git commit -m "feat(tvX): mô tả ngắn gọn công việc"
   git push origin feature/tvX-...
   ```
   *Nhóm trưởng sẽ review và merge vào nhánh `main`.*

---

## 6. HƯỚNG DẪN KHỞI CHẠY & KIỂM THỬ

- **Chạy kiểm thử tự động (Unit Tests):**
  ```bash
  python -m unittest Source/tests/test_sudoku_graph.py
  ```
- **Chạy chương trình minh họa lõi đồ thị:**
  ```bash
  python Source/main.py
  ```
- **Trên Windows:** Click đúp vào file `Release/run_console.bat` để chạy nhanh.
