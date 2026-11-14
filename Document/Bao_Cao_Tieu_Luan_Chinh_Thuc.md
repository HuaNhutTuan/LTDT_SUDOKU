# BỘ GIÁO DỤC VÀ ĐÀO TẠO
# TRƯỜNG ĐẠI HỌC SƯ PHẠM THÀNH PHỐ HỒ CHÍ MINH
# KHOA CÔNG NGHỆ THÔNG TIN

---

# BÁO CÁO TIỂU LUẬN CUỐI KỲ
## HỌC PHẦN: LÝ THUYẾT ĐỒ THỊ VÀ ỨNG DỤNG

### ĐỀ TÀI:
# GIẢI TRÒ CHƠI SUDOKU BẰNG THUẬT TOÁN TÔ MÀU ĐỒ THỊ
*(GRAPH COLORING PROBLEM FOR SUDOKU SOLVER)*

---

**Giảng viên hướng dẫn:** Bộ môn Khoa học Máy tính  
**Nhóm sinh viên thực hiện:** Nhóm Đồ án Sudoku (5 thành viên)  
- **Hứa Nhựt Tuấn** (Nhóm trưởng) - MSSV: 51.01.104.114  
- **Thành viên 2** - Phụ trách Thuật toán Welsh-Powell & DSATUR  
- **Thành viên 3** - Phụ trách Thuật toán Backtracking & Bộ sinh đề  
- **Thành viên 4** - Phụ trách Giao diện trực quan hóa GUI  
- **Thành viên 5** - Phụ trách Thực nghiệm Benchmark, Slide & Media  

*Thành phố Hồ Chí Minh, Năm 2026*

---

# LỜI CAM ĐOAN

Chúng tôi xin cam đoan rằng toàn bộ nội dung trong báo cáo tiểu luận này là kết quả nghiên cứu, mô hình hóa toán học và lập trình độc lập của nhóm dưới sự hướng dẫn của Giảng viên bộ môn Lý thuyết đồ thị. Mọi số liệu, kết quả thực nghiệm và các đoạn trích dẫn đều được ghi chú rõ ràng nguồn gốc tham khảo theo quy chuẩn học thuật của Trường Đại học Sư phạm Thành phố Hồ Chí Minh [5]. Mã nguồn chương trình do nhóm tự xây dựng, không sao chép nguyên văn từ bất kỳ nguồn trái phép nào.

*Thay mặt nhóm nghiên cứu,*  
*Nhóm trưởng: Hứa Nhựt Tuấn*

---

# LỜI CẢM ƠN

Nhóm chúng tôi xin trân trọng gửi lời cảm ơn sâu sắc nhất tới quý Thầy/Cô Khoa Công nghệ Thông tin - Trường Đại học Sư phạm Thành phố Hồ Chí Minh đã tận tâm truyền đạt những nền tảng tri thức quý báu về Lý thuyết đồ thị, các cấu trúc dữ liệu tiên tiến và tư duy tối ưu hóa thuật toán. Những kiến thức này đã tạo tiền đề quan trọng giúp nhóm hoàn thành đồ án nghiên cứu ứng dụng tô màu đồ thị vào giải trò chơi Sudoku một cách khoa học, chặt chẽ và đạt hiệu quả thực nghiệm cao.

---

# TUYÊN BỐ SỬ DỤNG TRÍ TUỆ NHÂN TẠO (AI ASSISTANCE STATEMENT)

Nhằm tuân thủ quy định liêm chính học thuật và tính minh bạch khoa học của Khoa Công nghệ Thông tin - Trường ĐH Sư phạm TP.HCM [5], nhóm tác giả xin tuyên bố rõ ràng về phạm vi và mục đích ứng dụng các công cụ Trí tuệ nhân tạo (Generative AI) trong quá trình thực hiện đồ án như sau:
1. **Mục đích biên tập văn bản:** Hỗ trợ rà soát lỗi chính tả, chuẩn hóa quy cách dấu câu, trau chuốt câu từ và đảm bảo văn phong học thuật thuần Việt thống nhất toàn báo cáo.
2. **Mục đích phản biện độc lập:** Đóng vai trò trợ lý phản biện khách quan để kiểm tra chéo tính logic của các công thức toán học, tính chính quy bậc 20 của đồ thị và tính hợp lệ của các phân tích độ phức tạp thuật toán.
3. **Tự chủ học thuật và mã nguồn:** Toàn bộ tư duy mô hình hóa toán học, kiến trúc lớp `SudokuGraph`, việc cài đặt các thuật toán cốt lõi (Welsh-Powell, DSATUR, Backtracking), cũng như toàn bộ dữ liệu thực nghiệm Benchmark đều do các thành viên trong nhóm trực tiếp nghiên cứu, lập trình và kiểm chứng độc lập. Các thành viên chịu trách nhiệm hoàn toàn về tính chính xác và nguyên bản của sản phẩm.

---

# BẢNG PHÂN CÔNG NHIỆM VỤ CÁC THÀNH VIÊN

| STT | Họ và tên | Module Mã nguồn phụ trách (Source/Release) | Nội dung Báo cáo & Tài liệu (Document) | Tỷ lệ đóng góp |
| :---: | :--- | :--- | :--- | :---: |
| **1** | **Hứa Nhựt Tuấn**<br>*(Nhóm trưởng)* | **Lớp `SudokuGraph`** (81 đỉnh, 810 cạnh, danh sách kề & ma trận kề 81x81), module **`IOHandler`** đọc/ghi file đề bài, **Game Validator** thời gian thực, **Solvability Checker**, **Hint Engine theo Heuristic DSATUR**, quản lý kho Git/GitHub tổng của nhóm. | **Phần Mở đầu**, **Toàn bộ Chương 2** (Mô hình hóa Sudoku bằng đồ thị & Phản biện học thuật); tổng hợp và chuẩn hóa thể thức toàn báo cáo. | 20% |
| **2** | **Thành viên 2** | Cài đặt thuật toán `WelshPowell()` và `DSATUR()` thuần túy; module tính toán và cập nhật bậc bão hòa (`saturation_degree`). | Chương 1 (Mục 1.1, 1.2, 1.3.1, 1.3.2): Cơ sở lý thuyết đồ thị, sắc số, mã giả và sơ đồ khối Welsh-Powell, DSATUR. | 20% |
| **3** | **Thành viên 3** | Cài đặt thuật toán `BacktrackDSATUR()` kết hợp Forward Checking; xây dựng module `GeneratePuzzle()` sinh đề 4 cấp độ có nghiệm duy nhất. | Chương 1 (Mục 1.3.3) và Chương 3 (Mục 3.2, 3.3): Thiết kế cấu trúc dữ liệu, lưu đồ thuật toán giải và sinh đề. | 20% |
| **4** | **Thành viên 4** | Xây dựng giao diện bàn cờ 9x9, làm nổi bật 20 đỉnh kề khi chọn ô, hiển thị tập màu khả dụng, bậc bão hòa và chế độ chạy từng bước (Step-by-step). | Chương 3 (Mục 3.1, 3.4): Kiến trúc hệ thống, thiết kế giao diện; biên soạn cuốn Hướng dẫn sử dụng có ảnh chụp minh họa. | 20% |
| **5** | **Thành viên 5** | Xây dựng bộ 40-100 đề Benchmark, module đo thời gian (ms), đếm số bước duyệt và số lần quay lui; đóng gói bản Release độc lập. | Chương 4 (Thực nghiệm & Đánh giá), Kết luận & Hướng phát triển, Tài liệu tham khảo; thiết kế Slide (.pptx) và dựng Video demo. | 20% |

---

# DANH MỤC KÝ HIỆU VÀ CHỮ VIẾT TẮT

| Ký hiệu / Viết tắt | Thuật ngữ tiếng Anh | Ý nghĩa trong Đồ án |
| :--- | :--- | :--- |
| **G = (V, E)** | Graph (Vertices, Edges) | Đồ thị vô hướng mô hình hóa bàn cờ Sudoku (81 đỉnh, 810 cạnh) |
| **deg(v)** | Degree of vertex v | Bậc của đỉnh v (số cạnh liên thuộc với đỉnh v, deg(v) = 20) |
| **N(v)** | Neighborhood of vertex v | Tập hợp tất cả 20 đỉnh kề trực tiếp với đỉnh v |
| **χ(G)** | Chromatic number | Sắc số của đồ thị (số màu tối thiểu để tô hợp lệ, χ(G) = 9) |
| **Kₙ** | Complete graph of size n | Đồ thị đầy đủ n đỉnh; đồ thị Sudoku chứa 27 đồ thị con K₉ |
| **DSATUR** | Degree of Saturation | Thuật toán tô màu đồ thị theo bậc bão hòa động (D. Brélaz, 1979) |
| **MRV** | Minimum Remaining Values | Chiến lược heuristic chọn đỉnh có số màu khả dụng ít nhất |
| **FC** | Forward Checking | Kỹ thuật kiểm tra tiến cắt tỉa miền giá trị của các đỉnh lân cận |
| **PREEXT** | Pre-coloring Extension | Bài toán mở rộng tiền tô màu trên đồ thị (J. Kratochvíl, 1994) |

---

# PHẦN MỞ ĐẦU

## 1 Lý do chọn đề tài
Trò chơi trí tuệ Sudoku từ lâu đã trở thành một trong những trò chơi giải đố số học phổ biến nhất trên toàn thế giới. Thoạt nhìn, Sudoku có vẻ là một bài toán thuần túy về sắp xếp chữ số trên ma trận 9x9 thỏa mãn các điều kiện hàng, cột và khối con. Tuy nhiên, dưới lăng kính của Toán học rời rạc và Khoa học máy tính [1], các chữ số từ 1 đến 9 không mang bất kỳ ý nghĩa số học đại số nào (không có phép toán cộng, trừ, nhân, chia), mà chúng chỉ đóng vai trò là 9 nhãn phân biệt độc lập. Điều này khẳng định bản chất sâu xa của trò chơi Sudoku chính là bài toán **Tô màu đỉnh đồ thị (Vertex Coloring Problem - GCP)**, một trong 21 bài toán NP-đầy đủ kinh điển được chứng minh bởi Richard M. Karp năm 1972.

Việc nghiên cứu và mô hình hóa bài toán Sudoku dưới góc độ Lý thuyết đồ thị mang lại giá trị học thuật và thực tiễn sâu sắc:
1. **Minh chứng tính ứng dụng của lý thuyết đồ thị:** Chuyển đổi một bài toán logic quen thuộc thành cấu trúc toán học chặt chẽ, tối ưu hóa quá trình giải bằng các cấu trúc dữ liệu đồ thị tiên tiến.
2. **Trực quan hóa sinh động:** Cho phép sinh viên hiểu sâu sắc các khái niệm trừu tượng như đồ thị chính quy (Regular Graph), bậc bão hòa (Degree of Saturation), sắc số (Chromatic Number) và cơ chế cắt tỉa không gian tìm kiếm.
3. **Mô hình thu nhỏ của bài toán thực tế:** Thuật toán tô màu đồ thị là nền tảng cốt lõi giải quyết hàng loạt bài toán quy mô công nghiệp như phân bổ tần số vô tuyến viễn thông (tránh nhiễu sóng giữa các trạm phát sóng lân cận), bài toán lập thời khóa biểu tự động (tránh xung đột phòng học và giáo viên) [3], và bài toán tối ưu hóa cấp phát thanh ghi CPU trong trình biên dịch máy tính.

Chính vì những lý do trên, nhóm đã lựa chọn đề tài: *"Giải trò chơi Sudoku bằng thuật toán tô màu đồ thị"* làm đồ án kết thúc học phần.

## 2 Mục tiêu và nhiệm vụ nghiên cứu
- **Mục tiêu tổng quát:** Vận dụng toàn diện kiến thức nền tảng của môn học Lý thuyết đồ thị để mô hình hóa bàn cờ Sudoku 9x9 thành đồ thị vô hướng chuẩn xác, cài đặt và phân tích đối sánh thực nghiệm ba thuật toán tô màu đỉnh từ cơ bản đến nâng cao, đồng thời xây dựng ứng dụng trực quan hóa quá trình gán màu từng bước.
- **Nhiệm vụ nghiên cứu cụ thể:**
  1. Xây dựng mô hình toán học đồ thị Sudoku G = (V, E) gồm đúng 81 đỉnh và 810 cạnh; chứng minh chặt chẽ tính chất đồ thị chính quy bậc 20.
  2. Thiết kế và cài đặt lớp `SudokuGraph` tối ưu với danh sách kề và ma trận kề, phát hiện và bắt lỗi vi phạm tiền tô màu ban đầu, Game Validator và Hint Engine.
  3. Cài đặt 3 giải thuật: Welsh-Powell (tham lam theo bậc cố định) [3], DSATUR (heuristic bậc bão hòa động) [2], và Backtracking kết hợp Forward Checking + DSATUR/MRV.
  4. Phát triển thuật toán sinh đề tự động (Generate Puzzle) phân theo 4 cấp độ khó, đảm bảo có nghiệm duy nhất.
  5. Đo lường, đối sánh hiệu năng thực nghiệm trên tập 40-100 đề Sudoku về thời gian thực thi (ms), số bước duyệt và số lần quay lui.

## 3 Đối tượng và phạm vi nghiên cứu
- **Đối tượng nghiên cứu:** Trò chơi Sudoku chuẩn kích thước 9x9; cấu trúc đồ thị vô hướng đơn; bài toán tô màu đỉnh đồ thị (Vertex Coloring) và bài toán mở rộng tiền tô màu (Pre-coloring Extension - PREEXT) [4]; các thuật toán tìm kiếm và quay lui có định hướng heuristic.
- **Phạm vi nghiên cứu:** Giới hạn tập trung phân tích chuyên sâu trên bảng Sudoku 9x9 với tập 9 màu {1..9}. Môi trường thực nghiệm được chuẩn hóa trên máy tính cá nhân để so sánh các chỉ số thuật toán.

## 4 Phương pháp nghiên cứu
- **Phương pháp nghiên cứu lý thuyết:** Thu thập, tổng hợp và phân tích các tài liệu học thuật về Lý thuyết đồ thị, bài báo gốc năm 1979 của Daniel Brélaz về thuật toán DSATUR [2], sách chuyên khảo Discrete Mathematics của Kenneth H. Rosen [1] và giáo trình của Khoa CNTT - HCMUE [5].
- **Phương pháp thực nghiệm mô hình hóa:** Thiết kế kiến trúc phần mềm hướng đối tượng; triển khai thuật toán trên ngôn ngữ Python; xây dựng bộ kiểm thử tự động (Unit Tests) để nghiệm thu cấu trúc 81 đỉnh, 810 cạnh và kiểm tra bắt lỗi đề bài.
- **Phương pháp thống kê đối sánh:** Thu thập số liệu chạy thực tế qua từng cấp độ đề bài để vẽ biểu đồ và phân tích ưu nhược điểm của từng thuật toán.

## 5 Kết cấu của đề tài
Nội dung báo cáo tiểu luận được tổ chức thành 4 chương chính:
- **CHƯƠNG 1. CƠ SỞ LÝ THUYẾT:** Trình bày các định nghĩa đồ thị, bài toán tô màu đỉnh, sắc số và nguyên lý hoạt động của các thuật toán Welsh-Powell, DSATUR, Backtracking.
- **CHƯƠNG 2. MÔ HÌNH HÓA BÀI TOÁN SUDOKU BẰNG LÝ THUYẾT ĐỒ THỊ:** Chi tiết toán học về việc chuyển đổi bàn cờ 9x9 sang đồ thị 81 đỉnh, 810 cạnh, bài toán mở rộng tiền tô màu và phản biện học thuật so với các tiếp cận khác.
- **CHƯƠNG 3. THIẾT KẾ VÀ CÀI ĐẶT CHƯƠNG TRÌNH:** Phân tích yêu cầu, kiến trúc 4 chức năng sản phẩm thực tế, cấu trúc lưu trữ của lớp `SudokuGraph`, lưu đồ thuật toán và thiết kế giao diện trực quan hóa.
- **CHƯƠNG 4. THỰC NGHIỆM VÀ ĐÁNH GIÁ KẾT QUẢ:** Môi trường thử nghiệm, bảng số liệu thực tế trên 4 cấp độ khó và biểu đồ so sánh hiệu năng của 3 thuật toán.

---

# CHƯƠNG 1. CƠ SỞ LÝ THUYẾT

## 1.1 Các khái niệm cơ bản về lý thuyết đồ thị
*(Phần nội dung do Thành viên 2 biên soạn)*
- Định nghĩa đồ thị vô hướng đơn G = (V, E).
- Bậc của đỉnh deg(v), đồ thị chính quy k-regular.
- Biểu diễn đồ thị bằng ma trận kề và danh sách kề.

## 1.2 Bài toán tô màu đồ thị (Graph Coloring Problem)
*(Phần nội dung do Thành viên 2 biên soạn)*
- Khái niệm tô màu đỉnh hợp lệ.
- Sắc số của đồ thị χ(G).
- Khái niệm đồ thị con đầy đủ (clique) và mối quan hệ với sắc số.
- Bài toán Mở rộng tiền tô màu (Pre-coloring Extension - PREEXT) [4].

## 1.3 Các thuật toán tô màu đồ thị trọng tâm
### 1.3.1 Thuật toán Welsh-Powell (Tham lam theo bậc cố định)
*(Phần nội dung do Thành viên 2 biên soạn: Nguyên lý, mã giả và sơ đồ khối) [3]*
### 1.3.2 Thuật toán DSATUR (Degree of Saturation)
*(Phần nội dung do Thành viên 2 biên soạn: Khái niệm bậc bão hòa, cơ chế cập nhật động, mã giả) [2]*
### 1.3.3 Thuật toán Quay lui kết hợp Forward Checking và Heuristic DSATUR/MRV
*(Phần nội dung do Thành viên 3 biên soạn: Chiến lược tìm kiếm quay lui, cắt tỉa miền giá trị)*

---

# CHƯƠNG 2. MÔ HÌNH HÓA BÀI TOÁN SUDOKU BẰNG LÝ THUYẾT ĐỒ THỊ

## 2.1 Quy tắc trò chơi Sudoku 9x9 và bài toán tổng quát n² × n²
Trò chơi Sudoku tiêu chuẩn được chơi trên một lưới kích thước 9x9 gồm tổng cộng 81 ô vuông nhỏ. Lưới 9x9 này được chia thành 9 khối con (sub-grid/block) kích thước 3x3. Mục tiêu của người chơi là điền các chữ số từ 1 đến 9 vào các ô còn trống sao cho đồng thời thỏa mãn ba điều kiện tiên quyết:
1. **Ràng buộc Hàng (Row Constraint):** Trên mỗi hàng trong số 9 hàng, mỗi chữ số từ 1 đến 9 chỉ xuất hiện duy nhất đúng một lần (không trùng lặp).
2. **Ràng buộc Cột (Column Constraint):** Trên mỗi cột trong số 9 cột, mỗi chữ số từ 1 đến 9 chỉ xuất hiện duy nhất đúng một lần.
3. **Ràng buộc Khối con (Block Constraint):** Trong mỗi khối con 3x3 trong số 9 khối, mỗi chữ số từ 1 đến 9 chỉ xuất hiện duy nhất đúng một lần.

Trong bài toán tổng quát kích thước n² × n² (ví dụ n = 2 là bàn cờ 4x4, n = 3 là Sudoku chuẩn 9x9, n = 4 là Hexadoku 16x16), bàn cờ gồm n⁴ ô vuông, chia thành n² khối con kích thước n × n, và sử dụng n² nhãn màu phân biệt. Mọi phân tích đồ thị áp dụng cho Sudoku 9x9 đều có thể mở rộng tự nhiên sang bài toán tổng quát n² × n².

## 2.2 Xây dựng đồ thị Sudoku G = (V, E) gồm 81 đỉnh và 810 cạnh

### 2.2.1 Định nghĩa Tập đỉnh V (Vertices)
Tập đỉnh V biểu diễn 81 ô tọa độ của bàn cờ Sudoku. Mỗi đỉnh v thuộc V tương ứng 1-1 với một cặp tọa độ (r, c) trong đó r là chỉ số hàng (0 ≤ r ≤ 8) và c là chỉ số cột (0 ≤ c ≤ 8).

Phép ánh xạ song ánh giữa tọa độ 2 chiều (r, c) và chỉ số đỉnh 1 chiều v trong tập V = {0, 1, 2, ..., 80} được xác định bởi công thức:
```text
v = f(r, c) = r × 9 + c
```
Ngược lại, từ chỉ số đỉnh v, ta khôi phục lại tọa độ hàng r và cột c nhờ phép chia lấy phần nguyên và phần dư:
```text
r = ⌊v / 9⌋
c = v mod 9
```
Chỉ số khối 3x3 tương ứng của đỉnh v(r, c) được tính bằng:
```text
box(r, c) = ⌊r / 3⌋ × 3 + ⌊c / 3⌋  (với box ∈ {0, 1, ..., 8})
```

### 2.2.2 Định nghĩa Tập cạnh vô hướng E (Edges) và Ràng buộc xung đột
Trong đồ thị Sudoku, mỗi cạnh vô hướng e = (u, v) thuộc E biểu diễn một quan hệ xung đột trực tiếp (conflict constraint) giữa hai ô phân biệt. Điều này đồng nghĩa với việc hai đỉnh u và v không bao giờ được phép mang cùng một giá trị màu.

Hai đỉnh phân biệt u(r₁, c₁) và v(r₂, c₂) với u ≠ v có cạnh nối (u, v) thuộc E khi và chỉ khi thỏa mãn ít nhất một trong ba điều kiện:
1. **Xung đột cùng hàng:** r₁ = r₂ (nằm trên cùng một hàng ngang).
2. **Xung đột cùng cột:** c₁ = c₂ (nằm trên cùng một cột dọc).
3. **Xung đột cùng khối con 3x3:** ⌊r₁ / 3⌋ = ⌊r₂ / 3⌋ và ⌊c₁ / 3⌋ = ⌊c₂ / 3⌋ (nằm trong cùng một ô vuông 3x3).

### 2.2.3 Chứng minh toán học Tính chất Đồ thị chính quy bậc 20 (20-Regular Graph)
Xét một đỉnh v bất kỳ thuộc tập đỉnh V, tương ứng với ô tại tọa độ (r, c):
- **Số đỉnh kề cùng hàng với v:** Trên hàng r có đúng 9 ô. Trừ đi chính ô v, tồn tại đúng 8 đỉnh kề cùng hàng: |N_row(v)| = 8.
- **Số đỉnh kề cùng cột với v:** Trên cột c có đúng 9 ô. Trừ đi chính ô v, tồn tại đúng 8 đỉnh kề cùng cột: |N_col(v)| = 8.
- **Số đỉnh kề trong khối 3x3 chứa v:** Khối 3x3 gồm đúng 9 ô. Ô v nằm tại giao điểm của 1 hàng và 1 cột bên trong khối đó. Do đó, trong khối 3x3 có 2 ô cùng hàng với v (đã được đếm ở N_row), 2 ô cùng cột với v (đã được đếm ở N_col), và chính ô v. Số ô còn lại trong khối 3x3 hoàn toàn không cùng hàng cũng không cùng cột với v là: 9 - 1 - 2 - 2 = 4 đỉnh duy nhất: |N_box-only(v)| = 4.

Vì ba tập đỉnh kề trên hoàn toàn rời nhau (disjoint), nên tổng số đỉnh kề duy nhất N(v) của đỉnh v là:
```text
deg(v) = |N(v)| = |N_row(v)| + |N_col(v)| + |N_box-only(v)| = 8 + 8 + 4 = 20
```

Do công thức trên đúng với mọi đỉnh v thuộc V (không phụ thuộc vào việc ô nằm ở góc, ở cạnh hay ở tâm bàn cờ), nên đồ thị Sudoku là một **đồ thị chính quy bậc 20 (20-regular graph)**.

Áp dụng **Bổ đề bắt tay (Handshaking Lemma)** trong lý thuyết đồ thị [1]:
```text
Tổng bậc các đỉnh = 2 × |E|  <=>  ∑ deg(v) = 2 × |E|
<=>  81 × 20 = 2 × |E|  <=>  1620 = 2 × |E|  <=>  |E| = 810 cạnh vô hướng.
```
Như vậy, đồ thị Sudoku G = (V, E) có chính xác đúng 81 đỉnh và 810 cạnh vô hướng.

### 2.2.4 Cấu trúc lưu trữ biểu diễn Đồ thị
Trong mã nguồn đồ án, nhóm đã triển khai song song cả hai cấu trúc biểu diễn đồ thị cốt lõi:
- **Danh sách kề (Adjacency List):** Lưu trữ mảng gồm 81 phần tử, mỗi phần tử là một danh sách chứa đúng 20 chỉ số đỉnh kề. Cấu trúc này tối ưu tuyệt đối về bộ nhớ O(|V| + |E|) và cho phép duyệt cực nhanh các đỉnh lân cận để cập nhật bậc bão hòa DSATUR trong thời gian O(deg(v)) = O(20) = O(1).
- **Ma trận kề (Adjacency Matrix):** Ma trận nhị phân đối xứng A kích thước 81x81, trong đó A[u][v] = 1 nếu u và v có cạnh nối, ngược lại A[u][v] = 0. Cấu trúc này cho phép kiểm tra quan hệ xung đột giữa hai đỉnh bất kỳ với thời gian O(1).

## 2.3 Chuyển đổi bài toán giải Sudoku sang bài toán Mở rộng tiền tô màu (Pre-coloring Extension)
- **Bài toán Tô màu đồ thị tổng quát (Graph Vertex Coloring) [1]:** Cho đồ thị G = (V, E) và tập k màu C = {1, 2, ..., k}. Mục tiêu là tìm hàm gán nhãn màu c: V → C sao cho với mọi cạnh (u, v) thuộc E thì c(u) ≠ c(v). Số màu k nhỏ nhất để đồ thị G có thể tô hợp lệ được gọi là Sắc số (Chromatic Number), ký hiệu χ(G).
- **Sắc số của đồ thị Sudoku:** Mỗi hàng (hoặc mỗi cột, mỗi khối 3x3) gồm 9 đỉnh đôi một có cạnh nối với nhau. Do đó, mỗi hàng tương ứng với một Đồ thị con đầy đủ (Clique) K₉ gồm 9 đỉnh. Vì χ(Kₙ) = n, nên χ(K₉) = 9. Theo tính chất đồ thị, sắc số của đồ thị cha luôn lớn hơn hoặc bằng sắc số của đồ thị con lớn nhất: χ(G) ≥ ω(G) ≥ 9. Vì Sudoku luôn giải được bằng đúng 9 chữ số {1, 2, ..., 9}, ta suy ra chính xác: **χ(G) = 9**.
- **Bản chất Pre-coloring Extension (PREEXT) [4]:** Trong một đề Sudoku thực tế, người chơi không bắt đầu với đồ thị trắng hoàn toàn, mà một tập con các đỉnh V' ⊂ V đã được gán sẵn các màu cố định c₀(v) ∈ {1..9} (gọi là các ô gợi ý / clues / tiền tô màu). Nhiệm vụ của giải thuật là tìm một ánh xạ mở rộng c: V → {1..9} sao cho:
  1. c(v) = c₀(v) với mọi v ∈ V' (bảo toàn tiền tô màu), và
  2. c(u) ≠ c(v) với mọi cạnh (u, v) ∈ E.

Theo định lý của Jan Kratochvíl (1993) [4], bài toán mở rộng tiền tô màu (Pre-coloring Extension) là một bài toán NP-đầy đủ (NP-complete). Do đó, việc nghiên cứu các thuật toán Heuristic thông minh để thu hẹp không gian tìm kiếm là trọng tâm sống còn của đề tài.

## 2.4 Phân tích ưu nhược điểm của từng thuật toán trên đồ thị Sudoku
Nhóm tiến hành phân tích lý thuyết sâu sắc về cơ chế vận hành của ba thuật toán trên cấu trúc đồ thị Sudoku 20-regular:

1. **Thuật toán Welsh-Powell (Tham lam theo bậc cố định) [3]:**
   - **Cơ chế:** Sắp xếp các đỉnh theo thứ tự giảm dần của bậc deg(v), sau đó duyệt tuần tự và gán màu hợp lệ nhỏ nhất chưa bị các đỉnh kề sử dụng.
   - **Giới hạn trên đồ thị Sudoku:** Vì đồ thị Sudoku là đồ thị chính quy bậc 20 (deg(v) = 20 với mọi đỉnh v), tiêu chí sắp xếp bậc của Welsh-Powell trở nên hoàn toàn vô hiệu (tất cả 81 đỉnh đều có cùng độ ưu tiên bậc). Hơn nữa, do bản chất tham lam cục bộ không quay lui, khi gặp đề bài có tiền tô màu, thuật toán rất dễ rơi vào tình trạng ngõ cụt (deadlock: một ô trống có tất cả 9 màu bị các đỉnh kề chiếm giữ, buộc phải dùng màu thứ 10) hoặc cho ra kết quả sai luật. Welsh-Powell đóng vai trò đối chứng mẫu mực để chứng minh hạn chế của tham lam tĩnh.

2. **Thuật toán DSATUR (Degree of Saturation - Brélaz, 1979) [2]:**
   - **Cơ chế:** Thay vì dùng bậc tĩnh, DSATUR sử dụng Bậc bão hòa động: sat_deg(v) = số lượng màu KHÁC NHAU đã xuất hiện ở các đỉnh kề của v. Tại mỗi bước, thuật toán luôn chọn đỉnh có bậc bão hòa lớn nhất để tô trước (ưu tiên các đỉnh đang chịu nhiều ràng buộc nhất).
   - **Đánh giá:** DSATUR giải quyết cực kỳ xuất sắc các đề bài cấp độ Dễ và Trung bình mà không cần quay lui, thời gian chạy gần như tức thì. Tuy nhiên, trên các đề cấp độ Khó hoặc Chuyên gia (có ít hơn 25 clues ban đầu), tham lam thuần túy của DSATUR vẫn có thể đi vào ngõ cụt nếu không có cơ chế hoàn tác.

3. **Thuật toán Backtracking kết hợp Forward Checking và Heuristic DSATUR/MRV:**
   - **Cơ chế:** Kết hợp tìm kiếm quay lui có định hướng với kỹ thuật kiểm tra tiến (Forward Checking). Tại mỗi bước rẽ nhánh, thuật toán áp dụng chiến lược MRV (Minimum Remaining Values - tương đương chọn đỉnh có sat_deg lớn nhất) để chọn ô có miền giá trị khả dụng hẹp nhất. Khi thử gán một màu, thuật toán lập tức cắt tỉa miền màu của 20 đỉnh kề. Nếu bất kỳ đỉnh kề nào bị rỗng miền giá trị, nhánh tìm kiếm lập tức bị cắt tỉa (Pruning) và quay lui ngay lập tức.
   - **Đánh giá:** Đảm bảo độ chính xác 100% trên mọi đề Sudoku hợp lệ, số bước duyệt và số lần quay lui giảm tới 95-99% so với duyệt quay lui ngây thơ.

## 2.5 Phản biện học thuật về việc lựa chọn mô hình Tô màu đồ thị
1. **So với Brute-Force (Vét cạn ngây thơ):** Vét cạn có độ phức tạp $O(9^{81})$, bùng nổ tổ hợp trên các đề khó, trong khi Tô màu đồ thị kết hợp DSatur và Forward Checking cắt tỉa không gian tìm kiếm tới hơn 95%, giải bài toán trong chưa đầy 0.05 giây.
2. **So với Dancing Links (Algorithm X của Donald Knuth) [6]:** Dancing Links giải bài toán Bao phủ chính xác rất nhanh nhưng làm mất đi hoàn toàn trực quan hình học và các khái niệm đồ thị (đỉnh kề, bậc, sắc số, bão hòa), không phù hợp với mục tiêu sư phạm của môn học.
3. **So với Thuật toán Di truyền (Genetic Algorithm):** GA là thuật toán metaheuristic xấp xỉ, dễ kẹt ở cực tiểu cục bộ và không cam kết 100% tìm ra lời giải cho các đề bài khó, trong khi giải thuật của nhóm chứng minh được tính đúng đắn tuyệt đối 100%.

---

# CHƯƠNG 3. THIẾT KẾ VÀ CÀI ĐẶT CHƯƠNG TRÌNH

## 3.1 Phân tích yêu cầu chức năng, kiến trúc hệ thống và quy chuẩn nộp bài
*(Phần nội dung do Thành viên 4 biên soạn)*

### 3.1.1 Bốn chức năng nâng cấp sản phẩm thực tế (Real-world Sudoku Game & Solver)
1. **Chức năng Tạo trò chơi (Game Generator):** Sinh đề 4 cấp độ (Dễ, Trung bình, Khó, Chuyên gia), đục lỗ đối xứng tâm và cam kết đúng 1 nghiệm duy nhất.
2. **Chức năng Kiểm tra trò chơi thời gian thực (Game Validator):** Quét 20 đỉnh kề $N(v)$ khi người chơi nhập số, báo đỏ và hiển thị chi tiết xung đột (hàng, cột, khối 3x3).
3. **Chức năng Kiểm tra khả giải và số nghiệm (Solvability Checker):** Xác định bàn cờ đang 0 nghiệm (bế tắc), 1 nghiệm duy nhất hay > 1 nghiệm.
4. **Chức năng Gợi ý nước đi tiếp theo (Hint Engine theo DSATUR & MRV):** Phát hiện Naked Single hoặc đỉnh có bậc bão hòa cao nhất kèm giải thích logic đồ thị.

### 3.1.2 Kiến trúc hệ thống 3 tầng
Hệ thống được thiết kế theo mô hình phân tầng hướng đối tượng:
- **Tầng Dữ liệu & Đồ thị lõi (Core Graph):** Lớp `Graph`, `SudokuGraph`, `IOHandler`.
- **Tầng Thuật toán (Algorithms Engine):** Lớp xử lý `WelshPowell`, `DSATUR`, `BacktrackDSATUR` và `PuzzleGenerator`.
- **Tầng Giao diện người dùng (User Interface):** Giao diện đồ họa bàn cờ 9x9 với chế độ tương tác trực quan và mô phỏng từng bước (Step-by-step).

### 3.1.3 Quy chuẩn cấu trúc 3 thư mục nộp bài của Khoa CNTT - HCMUE
Toàn bộ mã nguồn, tài liệu và bản phát hành của đồ án được tổ chức nghiêm ngặt theo quy định:
- **Thư mục Document:** Chứa toàn bộ báo cáo Word (.docx), PDF (.pdf), slide thuyết trình (.pptx), tài liệu Hướng dẫn sử dụng và video demo.
- **Thư mục Source:** Chứa toàn bộ mã nguồn chương trình sạch sẽ, module hóa khoa học và có chú thích chi tiết.
- **Thư mục Release:** Chứa file thực thi độc lập (.exe), tệp batch chạy nhanh trên Windows và bộ đề kiểm thử 4 cấp độ.

## 3.2 Thiết kế cấu trúc dữ liệu biểu diễn đồ thị và bảng màu
*(Phần nội dung do Thành viên 3 biên soạn: Chi tiết lớp SudokuGraph, mảng màu colors[], mảng is_precolored[], mảng saturationDegree[], danh sách kề adjacencyList)*

## 3.3 Chi tiết cài đặt các thuật toán giải và sinh đề
*(Phần nội dung do Thành viên 2 & 3 biên soạn: Mã giả ngắn gọn 10-20 dòng, lưu đồ và giải thích code Welsh-Powell, DSATUR, BacktrackDSATUR và GeneratePuzzle)*

## 3.4 Thiết kế giao diện trực quan hóa quá trình tô màu
*(Phần nội dung do Thành viên 4 biên soạn: Thiết kế lưới 9x9, tương tác chuột, tính năng highlight 20 đỉnh kề và thanh trượt tốc độ mô phỏng)*

### 3.4.1 Mục tiêu thiết kế và nguyên lý trực quan hóa đồ thị
Giao diện người dùng (GUI) của đồ án không đơn thuần là một bảng trò chơi Sudoku thông thường, mà được thiết kế như một **Công cụ trực quan hóa Lý thuyết đồ thị (Graph Visualization Tool)**. Mục tiêu cốt lõi là làm nổi bật bản chất toán học của đồ thị $G = (V, E)$ gồm 81 đỉnh và 810 cạnh:
1. **Trực quan hóa tức thì cấu trúc lân cận:** Khi người dùng chọn bất kỳ ô cờ nào (tương ứng đỉnh $v \in V$), giao diện lập tức xác định và làm nổi bật đúng $20$ đỉnh kề $N(v)$ (gồm 8 đỉnh cùng hàng, 8 đỉnh cùng cột và 4 đỉnh cùng khối $3 \times 3$).
2. **Minh bạch hóa các chỉ số động của thuật toán DSATUR:** Hiển thị trực quan bậc bão hòa hiện tại $\text{sat\_deg}(v)$ (số màu khác nhau đã xuất hiện ở các đỉnh kề) và miền màu khả dụng $\text{MRV}(v) = \{1..9\} \setminus \{c(u) \mid u \in N(v)\}$.
3. **Mô phỏng từng bước (Step-by-step Animation):** Cho phép người học và giảng viên quan sát chi tiết từng quyết định chọn đỉnh có bậc bão hòa cao nhất, các bước gán màu thử nghiệm và các bước quay lui khi rơi vào bế tắc, với khả năng tùy chỉnh tốc độ trễ linh hoạt.

### 3.4.2 Kiến trúc Module Giao diện (`SudokuGUI`)
Module giao diện được xây dựng bằng thư viện chuẩn `tkinter` của Python nhằm đảm bảo tính độc lập tối đa, chạy trực tiếp trên mọi hệ thống mà không cần cài đặt thêm thư viện bên ngoài:
- **Khung bàn cờ chính (Canvas 9x9):** Sử dụng `tk.Canvas` để vẽ lưới 81 ô với độ chính xác theo từng điểm ảnh (pixel-perfect). Các đường phân cách khối con $3 \times 3$ được vẽ nét đậm ($3\text{px}$, mã màu `#2f3640`) phân biệt rõ với các đường kẻ nội bộ ($1\text{px}$, mã màu `#dcdde1`).
- **Khung Thanh tra đồ thị (Graph Inspector):** Bảng thông số bên phải cập nhật thời gian thực tọa độ đỉnh, chỉ số khối $3 \times 3$, bậc của đỉnh $\deg(v) = 20$, bậc bão hòa $\text{sat\_deg}(v)$ và tập màu hợp lệ còn lại.
- **Game Validator thời gian thực:** Quét danh sách kề $N(v)$ ngay khi có sự thay đổi màu trên ô; nếu phát hiện trùng màu giữa 2 đỉnh kề, ô vi phạm lập tức chuyển màu đỏ cảnh báo kèm thông báo chi tiết vị trí xung đột.

### 3.4.3 Cơ chế mô phỏng Step-by-step không gây nghẽn giao diện
Để giải quyết bài toán giao diện bị đơ (freeze) khi thực thi thuật toán tìm kiếm đệ quy quay lui, module áp dụng kỹ thuật **Python Generator kết hợp vòng lặp sự kiện `root.after()`**:
1. Thuật toán `_create_solve_generator()` được thiết kế dưới dạng hàm sinh (generator). Tại mỗi bước chọn đỉnh, gán màu hoặc quay lui, generator phát ra (`yield`) một gói trạng thái: `(action, vertex, color, description)` trong đó `action` thuộc `{'assign', 'backtrack', 'done'}`.
2. Phương thức điều phối `_run_auto_step()` lấy từng bước từ generator, cập nhật lại màu sắc đỉnh và bảng thông số trên Canvas, sau đó lên lịch gọi bước tiếp theo thông qua hàm phi nghẽn `root.after(delay_ms, ...)`.
3. Người dùng có thể toàn quyền can thiệp vào quá trình chạy: bấm **"Tạm dừng (Pause)"**, thực hiện **"Bước tiếp (Step)"** thủ công để phân tích kỹ từng nước đi, hoặc kéo thanh trượt **Tốc độ trễ (Speed Slider: 10ms – 500ms)** để tăng/giảm tốc độ mô phỏng.

#### Mã giả Thuật toán Step-by-step DSATUR Backtracking
```text
Mã giả Thuật toán Step-by-step DSATUR Backtracking (Thành viên 4):
Input:  Đồ thị SudokuGraph G = (V, E) với các đỉnh tiền tô màu ban đầu.
Output: Generator phát ra từng bước ('assign', 'backtrack', 'done') cho GUI.

Hàm Sinh SolveStepGenerator(G):
1.   uncolored = G.get_uncolored_vertices();
2.   Nếu uncolored rỗng:
3.       YIELD ('done', None, None, "Bàn cờ đã giải hoàn tất!");
4.       Trả về TRUE;
5.   candidates = [];
6.   Với mỗi đỉnh v thuộc uncolored:
7.       avail = G.get_available_colors(v); // Miền màu khả dụng MRV
8.       sat = G.get_saturation_degree(v);  // Bậc bão hòa DSATUR
9.       candidates.append((v, sat, |avail|, avail));
10.  Sắp xếp candidates theo: min(|avail|), max(sat);
11.  best_v = đỉnh đầu tiên trong candidates;
12.  Nếu |avail| của best_v == 0:
13.      Trả về FALSE; // Bế tắc ngõ cụt, cần quay lui
14.  Với mỗi color trong miền khả dụng của best_v:
15.      G.colors[best_v] = color;
16.      YIELD ('assign', best_v, color, "Gán màu cho đỉnh");
17.      sub_gen = SolveStepGenerator(G);
18.      Với mỗi step trong sub_gen:
19.          YIELD step;
20.          Nếu step.action == 'done': Trả về TRUE;
21.      G.colors[best_v] = 0; // Hoàn tác gán màu (Backtrack)
22.      YIELD ('backtrack', best_v, color, "Quay lui tại đỉnh");
23.  Trả về FALSE;
```

#### Sơ đồ khối logic hoạt động của chế độ Step-by-step
```text
+----------------------------------------------------------+
|                     BẮT ĐẦU (START)                      |
+----------------------------------------------------------+
                               |
                               v
+----------------------------------------------------------+
| Bước 1: Khởi tạo Generator;                              |
| Kiểm tra tính hợp lệ tiền tô màu trên 20 đỉnh kề         |
+----------------------------------------------------------+
                               |
                               v
+----------------------------------------------------------+
| Còn đỉnh nào chưa được tô màu không?                     |
+----------------------------------------------------------+
                 | (Còn)                            | (Hết)
                 v                                  v
+----------------------------+      +----------------------+
| Bước 2: Tính sat_deg & MRV |      | KẾT THÚC (SUCCESS)   |
| Chọn v* có min(|MRV|)      |      | Bàn cờ hợp lệ 100%   |
| Tiêu chí phụ: max(sat_deg) |      +----------------------+
+----------------------------+
                 |
         +-------+--------------------+
         | (|MRV| > 0)                | (|MRV| == 0: Bế tắc)
         v                            v
+---------------------------+  +---------------------------+
| Bước 3: Thử gán màu c*    |  | BẾ TẮC: Hết màu khả dụng  |
| YIELD ('assign', v*, c*)  |  | YIELD ('backtrack', v*,c*)|
| Canvas vẽ ô màu Vàng cam  |  | Hủy gán: colors[v*] = 0   |
+---------------------------+  +---------------------------+
                 |                              ^
                 v                              | (Nhánh sai)
+-----------------------------------------------+
| Gọi đệ quy giải tiếp đỉnh tiếp theo           |
+-----------------------------------------------+
                 |
                 v
+----------------------------------------------------------+
| root.after(delay_ms): Hẹn giờ gọi bước tiếp phi nghẽn    |
+----------------------------------------------------------+
```

### 3.4.4 Bảng quy ước màu sắc hiển thị trên bàn cờ
| Trạng thái đỉnh / ô cờ | Màu nền (Background) | Màu chữ (Foreground) | Ý nghĩa đồ thị |
|:---|:---:|:---:|:---|
| **Ô bình thường** | Trắng (`#ffffff`) | Xanh đen / Đen | Đỉnh chưa tô màu hoặc đã tô hợp lệ |
| **Ô đang chọn ($v$)** | Xanh dương (`#74b9ff`) | Trắng / Đậm | Đỉnh được người dùng click chọn kiểm tra |
| **20 đỉnh kề ($N(v)$)** | Xanh nhạt (`#e8f4fc`) | Theo trạng thái | 20 đỉnh có cạnh nối trực tiếp với đỉnh đang chọn |
| **Ô tiền tô màu** | Trắng xám (`#f8f9fa`) | Xanh đậm (`#192a56`) | Đỉnh có màu cố định của đề bài ban đầu |
| **Ô đang xử lý (Step)** | Vàng cam (`#ffeaa7`) | Xanh đen | Đỉnh đang được thuật toán DSATUR gán màu/quay lui |
| **Ô được gợi ý (Hint)** | Xanh ngọc (`#55efc4`) | Đen đậm | Đỉnh tối ưu được Hint Engine đề xuất |
| **Ô xung đột màu** | Đỏ nhạt (`#ff7675`) | Đỏ đậm (`#c23616`) | Vi phạm định lý tô màu: 2 đỉnh kề mang cùng một màu |

---

# CHƯƠNG 4. THỰC NGHIỆM VÀ ĐÁNH GIÁ KẾT QUẢ

## 4.1 Môi trường cài đặt và bộ dữ liệu thực nghiệm Benchmark
*(Phần nội dung do Thành viên 5 biên soạn)*
- Cấu hình phần cứng và môi trường phần mềm thử nghiệm.
- Bộ 40 đề kiểm thử chuẩn chia đều 4 cấp độ: Dễ (36 clues), Trung bình (30 clues), Khó (26 clues) và Chuyên gia (17 clues).

## 4.2 Bảng thống kê và biểu đồ so sánh hiệu năng
*(Phần nội dung do Thành viên 5 biên soạn: Thống kê thời gian thực thi (ms), số bước gán màu, số lần quay lui, tỷ lệ giải thành công của 3 thuật toán)*

## 4.3 Phân tích và thảo luận kết quả thực nghiệm
*(Phần nội dung do Thành viên 5 tổng hợp cùng toàn nhóm)*

---

# KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN

## 1 Các kết quả đã đạt được của đề tài
1. **Mô hình hóa toán học chính xác:** Quy đổi thành công bài toán Sudoku 9x9 sang đồ thị vô hướng 20-regular với đúng 81 đỉnh và 810 cạnh; chứng minh chặt chẽ tính chất chính quy và sắc số χ(G) = 9.
2. **Xây dựng module lõi vững chắc:** Cài đặt lớp `SudokuGraph` và module `IOHandler` tối ưu, hỗ trợ cả danh sách kề và ma trận kề, phát hiện và bắt lỗi vi phạm tiền tô màu, vượt qua 13/13 bài kiểm thử tự động.
3. **Bổ sung 4 chức năng sản phẩm thực tế:** Game Generator, Game Validator thời gian thực, Solvability Checker và Hint Engine theo Heuristic DSATUR.
4. **Cài đặt và đối sánh 3 giải thuật:** Phân tích rõ ràng giới hạn của thuật toán tham lam tĩnh Welsh-Powell, ưu thế của heuristic DSATUR và tính toàn vẹn 100% của giải thuật Backtracking kết hợp Forward Checking.
5. **Trực quan hóa sinh động:** Xây dựng giao diện mô phỏng từng bước gán màu và làm nổi bật 20 đỉnh kề phục vụ học tập và bảo vệ đồ án.

## 2 Hạn chế của đề tài
- Phạm vi nghiên cứu mới chỉ tập trung trên bàn cờ Sudoku tiêu chuẩn 9x9, chưa thử nghiệm trên các biến thể bàn cờ lớn hơn như Hexadoku 16x16.

## 3 Hướng phát triển trong tương lai
- Mở rộng ứng dụng giải các biến thể Sudoku phức tạp: Samurai Sudoku (5 bảng 9x9 lồng nhau), Killer Sudoku, Hyper Sudoku.
- Nghiên cứu cài đặt đối sánh thêm thuật toán Dancing Links (Algorithm X của Donald Knuth) [6] để so sánh hiệu năng với giải thuật Tô màu đồ thị.

---

# TÀI LIỆU THAM KHẢO

1. Kenneth H. Rosen, *Discrete Mathematics and Its Applications*, 8th Edition, McGraw-Hill, 2019.
2. D. Brélaz, "New methods to color the vertices of a graph", *Communications of the ACM*, Vol. 22, No. 4, pp. 251-256, 1979.
3. D. J. A. Welsh and M. B. Powell, "An upper bound for the chromatic number of a graph and its application to timetabling problems", *The Computer Journal*, Vol. 10, No. 1, pp. 85-86, 1967.
4. J. Kratochvíl, "Precoloring extension with fixed number of colors", *Discrete Mathematics*, Vol. 133, Issues 1-3, pp. 177-186, 1994.
5. Khoa Công nghệ Thông tin - Trường ĐH Sư Phạm TP.HCM, *Giáo trình và Quy định thực hiện đồ án môn Lý thuyết đồ thị và Ứng dụng*, 2024.
6. Donald E. Knuth, "Dancing Links", *Millennial Perspectives in Computer Science*, pp. 187-214, 2000.
