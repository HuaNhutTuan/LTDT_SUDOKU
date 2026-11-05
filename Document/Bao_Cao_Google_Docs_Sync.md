# TRƯỜNG ĐẠI HỌC SƯ PHẠM THÀNH PHỐ HỒ CHÍ MINH
# KHOA CÔNG NGHỆ THÔNG TIN

## BÁO CÁO TIỂU LUẬN CUỐI KỲ
### HỌC PHẦN: LÝ THUYẾT ĐỒ THỊ VÀ ỨNG DỤNG
**Đề tài:** GIẢI TRÒ CHƠI SUDOKU BẰNG THUẬT TOÁN TÔ MÀU ĐỒ THỊ  
**Quy mô:** Nhóm 5 thành viên  
**Nhóm trưởng:** Hứa Nhựt Tuấn - MSSV: 51.01.104.114  
**Kho mã nguồn GitHub:** https://github.com/HuaNhutTuan/LTDT_SUDOKU  

---

## I. CẤU TRÚC 3 THƯ MỤC NỘP ĐỒ ÁN CHUẨN KHOA CNTT - HCMUE

Đồ án được tổ chức nghiêm ngặt theo chuẩn 3 thư mục nộp bài của Khoa Công nghệ Thông tin - Trường ĐH Sư Phạm TP.HCM:

```text
LTDT_SUDOKU/
├── Document/                               # THƯ MỤC 1: TÀI LIỆU BÁO CÁO & SLIDE
│   ├── Bao_Cao_Tieu_Luan_Sudoku_To_Mau_Do_Thi.docx  # Báo cáo Word chuẩn A4, TNR 13pt
│   ├── Bao_Cao_Tieu_Luan_Sudoku_To_Mau_Do_Thi.pdf   # Báo cáo PDF tương ứng
│   ├── Slide_Thuyet_Trinh_Sudoku_To_Mau.pptx       # Slide thuyết trình bảo vệ cuối kỳ
│   ├── Huong_Dan_Su_Dung.pdf                        # Tài liệu hướng dẫn sử dụng ứng dụng
│   └── Video_Demo_Thuyet_Trinh.mp4                  # Video clip demo quá trình chạy
├── Source/                                 # THƯ MỤC 2: TOÀN BỘ MÃ NGUỒN CHƯƠNG TRÌNH
│   ├── main.py                             # Điểm khởi chạy console kiểm thử đồ thị
│   ├── core/                               # Module lõi đồ thị (Graph Core)
│   │   ├── graph.py                        # Lớp Graph vô hướng đơn tổng quát
│   │   ├── sudoku_graph.py                 # Lớp SudokuGraph (81 đỉnh, 810 cạnh, 20 đỉnh kề, DSATUR)
│   │   └── io_handler.py                   # Đọc/ghi file đề bài ma trận 9x9 và dataset
│   ├── algorithms/                         # Các thuật toán tô màu đồ thị
│   │   ├── welsh_powell.py                 # Thuật toán Welsh-Powell (TV2)
│   │   ├── dsatur.py                       # Thuật toán DSATUR thuần túy (TV2)
│   │   └── backtrack_dsatur.py             # Quay lui + Forward Checking + Heuristic DSATUR (TV3)
│   ├── generator/                          # Module tự động sinh đề theo 4 cấp độ (TV3)
│   ├── gui/                                # Giao diện bàn cờ trực quan hóa từng bước (TV4)
│   └── tests/                              # Bộ kiểm thử Unit Tests và Benchmark (TV1, TV5)
│       └── test_sudoku_graph.py            # Test nghiệm thu 81 đỉnh, 810 cạnh, bậc 20
└── Release/                                # THƯ MỤC 3: BẢN ĐÓNG GÓI CHẠY ĐỘC LẬP
    ├── SudokuSolver.exe                    # File thực thi chạy độc lập trên Windows
    ├── puzzles/                            # Thư mục bộ đề kiểm thử 4 cấp độ khó
    │   ├── sample_easy.txt                 # Đề Dễ
    │   ├── sample_medium.txt               # Đề Trung bình
    │   ├── sample_hard.txt                 # Đề Khó
    │   └── sample_expert.txt               # Đề Chuyên gia (17 clues tối thiểu)
    └── run_console.bat                     # File script khởi chạy nhanh trên Windows
```

---

## II. BẢNG PHÂN CÔNG NHIỆM VỤ VÀ ĐỊNH MỨC SẢN PHẨM 5 THÀNH VIÊN

| STT | Thành viên & Vai trò | Module Mã nguồn phụ trách (Source/Release) | Nội dung Báo cáo & Tài liệu (Document) | Mức độ hoàn thành |
|:---:|:---|:---|:---|:---:|
| **1** | **Hứa Nhựt Tuấn**<br>*(Nhóm trưởng - Kiến trúc & Đồ thị)* | **Lớp `SudokuGraph`** (81 đỉnh, 810 cạnh, danh sách kề & ma trận kề 81x81), module **`IOHandler`** đọc/ghi file đề bài, kiểm tra tính hợp lệ tiền tô màu (**`validate_precoloring`**), quản lý kho Git/GitHub tổng. | **Phần Mở đầu**, **Toàn bộ Chương 2** (Mô hình hóa bài toán Sudoku bằng lý thuyết đồ thị); tổng hợp và chuẩn hóa thể thức Word toàn báo cáo. | **100% (Đã nghiệm thu)** |
| **2** | **Thành viên 2**<br>*(Thuật toán Tham lam & DSATUR)* | Cài đặt hàm `WelshPowell()` và `DSATUR()` thuần túy; hàm tính và cập nhật bậc bão hòa (`saturation_degree`). | Chương 1 (Mục 1.1, 1.2, 1.3.1, 1.3.2): Cơ sở lý thuyết đồ thị, sắc số, mã giả và sơ đồ khối Welsh-Powell, DSATUR. | Đang tiến hành |
| **3** | **Thành viên 3**<br>*(Quay lui + Heuristic & Sinh đề)* | Cài đặt hàm `BacktrackDSATUR()` kết hợp Forward Checking; xây dựng module `GeneratePuzzle()` sinh đề 4 cấp độ có nghiệm duy nhất. | Chương 1 (Mục 1.3.3) và Chương 3 (Mục 3.2, 3.3): Thiết kế cấu trúc dữ liệu, lưu đồ thuật toán giải và sinh đề. | Đang tiến hành |
| **4** | **Thành viên 4**<br>*(Giao diện GUI & Trực quan hóa)* | Xây dựng giao diện bàn cờ 9x9, làm nổi bật 20 đỉnh kề khi chọn ô, hiển thị tập màu khả dụng, bậc bão hòa và chế độ chạy từng bước (Step-by-step). | Chương 3 (Mục 3.1, 3.4): Kiến trúc hệ thống, thiết kế giao diện; biên soạn cuốn Hướng dẫn sử dụng có ảnh chụp minh họa. | Đang tiến hành |
| **5** | **Thành viên 5**<br>*(Thực nghiệm, Benchmark & Media)* | Xây dựng bộ 40-100 đề Benchmark, module đo thời gian (ms), đếm số bước duyệt và số lần quay lui; đóng gói bản Release độc lập. | Chương 4 (Thực nghiệm & Đánh giá), Kết luận & Hướng phát triển, Tài liệu tham khảo; thiết kế Slide (.pptx) và dựng Video demo. | Đang tiến hành |

---

## III. CHI TIẾT NHIỆM VỤ ĐÃ HOÀN THÀNH CỦA NHÓM TRƯỞNG (THÀNH VIÊN 1)

### 1. Nghiệm thu Kỹ thuật Module Lõi Đồ thị
- **Khởi tạo đúng 81 đỉnh và 810 cạnh:** Ánh xạ song ánh $v = r \times 9 + c$ với $r, c \in \{0..8\}$.
- **Đồ thị chính quy bậc 20 (20-regular graph):** Mọi đỉnh $v \in V$ đều có chính xác đúng 20 đỉnh kề ($8 \text{ hàng} + 8 \text{ cột} + 4 \text{ khối } 3 \times 3$).
- **Lưu trữ kép tối ưu:** Hỗ trợ song song cả **Danh sách kề (`adjacency_list`)** giúp duyệt $O(20) = O(1)$ và **Ma trận kề (`adjacency_matrix` 81x81)** kiểm tra xung đột trong $O(1)$.
- **Bộ bắt lỗi tiền tô màu (`validate_precoloring`):** Phát hiện chính xác mọi xung đột trùng màu ban đầu trên cùng Hàng, Cột, hoặc Khối $3 \times 3$ và ném ngoại lệ `PrecoloringConflictError`.
- **Bộ xử lý tệp tin (`IOHandler`):** Đọc nạp đề bài từ ma trận 9x9 hoặc chuỗi 81 ký tự; hỗ trợ nạp dataset kiểm thử tự động nhiều đề.
- **Bộ kiểm thử tự động (Unit Tests):** Đã xây dựng 10 bài test trong `Source/tests/test_sudoku_graph.py` và vượt qua 100%.

---

## IV. NỘI DUNG BÁO CÁO: PHẦN MỞ ĐẦU (NHÓM TRƯỞNG PHỤ TRÁCH)

### 1. Lý do chọn đề tài
Trò chơi trí tuệ Sudoku từ lâu đã trở thành một trò chơi giải đố phổ biến toàn cầu. Thoạt nhìn, Sudoku có vẻ là một bài toán số học đơn thuần trên ma trận 9x9. Tuy nhiên, dưới góc độ Toán học rời rạc và Khoa học máy tính, các chữ số từ 1 đến 9 không mang bất kỳ ý nghĩa đại số nào (không dùng phép cộng, trừ, nhân, chia), mà chúng chỉ đóng vai trò là 9 nhãn phân biệt độc lập. Bản chất sâu xa của Sudoku chính là bài toán **Tô màu đỉnh đồ thị (Graph Coloring Problem)** và **Mở rộng tiền tô màu (Pre-coloring Extension)**, một trong những bài toán NP-đầy đủ kinh điển.

Nghiên cứu Sudoku bằng lý thuyết đồ thị mang lại giá trị học thuật và thực tiễn to lớn:
1. Chứng minh tính ứng dụng mạnh mẽ của lý thuyết đồ thị vào giải quyết bài toán ràng buộc tổ hợp.
2. Trực quan hóa sinh động các khái niệm: Đồ thị chính quy (Regular Graph), Bậc bão hòa (Degree of Saturation), Sắc số (Chromatic Number).
3. Là mô hình điển hình của các bài toán thực tế: Phân bổ tần số sóng viễn thông, xếp thời khóa biểu tự động, và cấp phát thanh ghi CPU.

### 2. Mục tiêu và nhiệm vụ nghiên cứu
- **Mục tiêu:** Mô hình hóa chuẩn xác bàn cờ Sudoku thành đồ thị vô hướng 20-regular; phân tích đối sánh thực nghiệm 3 thuật toán tô màu đỉnh và phát triển ứng dụng trực quan hóa từng bước.
- **Nhiệm vụ:**
  1. Xây dựng mô hình toán học $G = (V, E)$ gồm 81 đỉnh, 810 cạnh, chứng minh tính chính quy bậc 20.
  2. Cài đặt lớp `SudokuGraph` và module `IOHandler` tối ưu.
  3. Cài đặt các thuật toán Welsh-Powell, DSATUR, Backtracking + Forward Checking + DSATUR/MRV.
  4. Xây dựng thuật toán sinh đề tự động 4 cấp độ khó có nghiệm duy nhất.
  5. Đánh giá thực nghiệm hiệu năng trên tập 40-100 đề.

### 3. Đối tượng và phạm vi nghiên cứu
- **Đối tượng:** Trò chơi Sudoku 9x9, đồ thị vô hướng đơn, bài toán tô màu đỉnh và mở rộng tiền tô màu.
- **Phạm vi:** Tập trung giải Sudoku chuẩn 9x9 với 9 màu trên máy tính cá nhân.

### 4. Phương pháp nghiên cứu
- Nghiên cứu lý thuyết tài liệu chuyên khảo về Graph Theory của Kenneth H. Rosen, thuật toán DSATUR của Daniel Brélaz (1979).
- Lập trình hướng đối tượng bằng Python, kiểm thử tự động bằng Unit Tests.
- Thực nghiệm thống kê định lượng về thời gian (ms), số bước duyệt và số lần quay lui.

### 5. Kết cấu của đề tài
Báo cáo gồm 4 chương chính:
- **Chương 1:** Cơ sở lý thuyết đồ thị và bài toán tô màu.
- **Chương 2:** Mô hình hóa bài toán Sudoku bằng lý thuyết đồ thị.
- **Chương 3:** Thiết kế kiến trúc và cài đặt chương trình.
- **Chương 4:** Thực nghiệm và đánh giá kết quả.

---

## V. NỘI DUNG BÁO CÁO: CHƯƠNG 2. MÔ HÌNH HÓA BÀI TOÁN SUDOKU BẰNG LÝ THUYẾT ĐỒ THỊ (NHÓM TRƯỞNG PHỤ TRÁCH)

### 2.1. Quy tắc trò chơi Sudoku 9x9 và bài toán tổng quát $n^2 \times n^2$
Lưới Sudoku 9x9 gồm 81 ô vuông phân thành 9 khối con $3 \times 3$, thỏa mãn 3 ràng buộc:
1. **Ràng buộc Hàng:** Mỗi hàng chứa đủ 9 số $\{1..9\}$ không trùng lặp.
2. **Ràng buộc Cột:** Mỗi cột chứa đủ 9 số $\{1..9\}$ không trùng lặp.
3. **Ràng buộc Khối 3x3:** Mỗi khối $3 \times 3$ chứa đủ 9 số $\{1..9\}$ không trùng lặp.

### 2.2. Xây dựng đồ thị Sudoku $G = (V, E)$ gồm 81 đỉnh và 810 cạnh
- **Tập đỉnh $V$ (81 đỉnh):** Ánh xạ tọa độ $(r, c)$ với $r, c \in \{0..8\}$ sang đỉnh $v \in \{0..80\}$:
  $$v = r \times 9 + c \iff r = \lfloor v / 9 \rfloor, \ c = v \pmod 9$$
- **Tập cạnh $E$ (810 cạnh vô hướng):** Hai đỉnh phân biệt $u(r_1, c_1)$ và $v(r_2, c_2)$ có cạnh nối nếu:
  $$(r_1 = r_2) \lor (c_1 = c_2) \lor (\lfloor r_1 / 3 \rfloor = \lfloor r_2 / 3 \rfloor \land \lfloor c_1 / 3 \rfloor = \lfloor c_2 / 3 \rfloor)$$
- **Chứng minh Đồ thị chính quy bậc 20 (20-regular graph):** Với mọi đỉnh $v$:
  $$\deg(v) = |N_{\text{row}}(v)| + |N_{\text{col}}(v)| + |N_{\text{box-only}}(v)| = 8 + 8 + 4 = 20$$
  Áp dụng **Bổ đề bắt tay (Handshaking Lemma)**:
  $$\sum \deg(v) = 2|E| \iff 81 \times 20 = 2|E| \iff |E| = 810 \text{ cạnh.}$$

### 2.3. Chuyển đổi sang bài toán Mở rộng tiền tô màu (Pre-coloring Extension)
- **Sắc số $\chi(G) = 9$:** Đồ thị Sudoku chứa 27 đồ thị con đầy đủ (clique) $K_9$ (9 hàng, 9 cột, 9 khối con). Vì $\chi(K_9) = 9$, nên sắc số đồ thị $\chi(G) \ge 9$. Vì bàn cờ giải được bằng 9 màu, ta có $\chi(G) = 9$.
- **Bài toán Pre-coloring Extension:** Đề bài ban đầu cho sẵn một tập đỉnh con đã được tô màu cố định (clues). Cần mở rộng gán màu cho toàn bộ các đỉnh chưa tô sao cho không có 2 đỉnh kề nào trùng màu.

### 2.4. Phân tích ưu nhược điểm của từng thuật toán
1. **Welsh-Powell:** Do đồ thị chính quy bậc 20 (mọi đỉnh đều có bậc 20), tiêu chí sắp xếp bậc bị vô hiệu. Tính tham lam tĩnh không quay lui khiến thuật toán dễ rơi vào ngõ cụt khi có tiền tô màu hoặc vượt quá 9 màu.
2. **DSATUR:** Sử dụng bậc bão hòa động $\text{sat\_deg}(v)$ (số màu khác nhau ở các đỉnh kề). Co cụm không gian tìm kiếm cực tốt, giải rất nhanh đề Dễ và Trung bình mà không cần quay lui. Tuy nhiên có thể bế tắc ở đề Khó nếu không có cơ chế hoàn tác.
3. **Backtracking + Forward Checking + Heuristic DSATUR/MRV:** Kết hợp quay lui với kiểm tra tiến, luôn chọn đỉnh có bậc bão hòa cao nhất (ít màu khả dụng nhất). Đảm bảo tìm ra nghiệm chính xác 100% cho mọi đề Sudoku hợp lệ với số lần quay lui tối ưu nhất.

---

## VI. KHUNG NỘI DUNG CÁC CHƯƠNG TIẾP THEO DÀNH CHO CÁC THÀNH VIÊN

- **Chương 1: Cơ sở lý thuyết** (Thành viên 2 và Thành viên 3 biên soạn): Định nghĩa đồ thị, sắc số, mã giả và sơ đồ khối 3 thuật toán.
- **Chương 3: Thiết kế và cài đặt chương trình** (Thành viên 3 và Thành viên 4 biên soạn): Kiến trúc 3 tầng, cấu trúc dữ liệu, giao diện trực quan hóa và bộ sinh đề.
- **Chương 4: Thực nghiệm và đánh giá kết quả** (Thành viên 5 biên soạn): Bảng số liệu benchmark, biểu đồ so sánh thời gian chạy, số bước duyệt và số lần quay lui trên 40 đề kiểm thử.
- **Kết luận, Hướng phát triển và Tài liệu tham khảo:** Toàn nhóm tổng hợp trước ngày nộp bài.
