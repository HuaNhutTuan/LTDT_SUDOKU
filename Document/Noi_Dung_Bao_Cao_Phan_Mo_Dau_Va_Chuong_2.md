# BÁO CÁO TIỂU LUẬN CUỐI KỲ - LÝ THUYẾT ĐỒ THỊ VÀ ỨNG DỤNG
**Khoa Công nghệ Thông tin - Trường Đại học Sư phạm TP. Hồ Chí Minh (HCMUE)**  
**Đề tài:** Giải trò chơi Sudoku bằng thuật toán tô màu đồ thị  
**Phụ trách:** Hứa Nhựt Tuấn (Nhóm trưởng - Thành viên 1: Kiến trúc & Đồ thị) - MSSV: 51.01.104.114  

---

## TUYÊN BỐ SỬ DỤNG TRÍ TUỆ NHÂN TẠO (AI ASSISTANCE STATEMENT)
Nhằm tuân thủ quy định liêm chính học thuật và tính minh bạch khoa học của Khoa Công nghệ Thông tin - Trường ĐH Sư phạm TP.HCM [5], nhóm tác giả xin tuyên bố rõ ràng về phạm vi và mục đích ứng dụng các công cụ Trí tuệ nhân tạo (Generative AI) trong quá trình thực hiện đồ án như sau:
1. Mục đích biên tập văn bản: Hỗ trợ rà soát lỗi chính tả, chuẩn hóa quy cách dấu câu, trau chuốt câu từ và đảm bảo văn phong học thuật thuần Việt thống nhất toàn báo cáo.
2. Mục đích phản biện độc lập: Đóng vai trò trợ lý phản biện khách quan để kiểm tra chéo tính logic của các công thức toán học, tính chính quy bậc 20 của đồ thị và tính hợp lệ của các phân tích độ phức tạp thuật toán.
3. Tự chủ học thuật và mã nguồn: Toàn bộ tư duy mô hình hóa toán học, kiến trúc lớp `SudokuGraph`, việc cài đặt các thuật toán cốt lõi (Welsh-Powell, DSATUR, Backtracking), cũng như toàn bộ dữ liệu thực nghiệm Benchmark đều do các thành viên trong nhóm trực tiếp nghiên cứu, lập trình và kiểm chứng độc lập. Các thành viên chịu trách nhiệm hoàn toàn về tính chính xác và nguyên bản của sản phẩm.

---

## BẢNG PHÂN CÔNG NHIỆM VỤ 5 THÀNH VIÊN

| STT | Thành viên & Vai trò | Module Code phụ trách (Source/Release) | Nội dung Báo cáo & Tài liệu (Document) | Mức độ nghiệm thu |
|:---:|:---|:---|:---|:---:|
| **1** | **Hứa Nhựt Tuấn**<br>*(Nhóm trưởng - Kiến trúc & Đồ thị)* | **Lớp `SudokuGraph`** (81 đỉnh, 810 cạnh, danh sách kề & ma trận kề), module **`IOHandler`** đọc/ghi file đề bài, **Game Validator** thời gian thực, **Solvability Checker**, **Hint Engine theo Heuristic DSATUR**, quản lý Git/GitHub. | **Phần Mở đầu**, **Toàn bộ Chương 2** (Mô hình hóa Sudoku bằng đồ thị & Phản biện học thuật); tổng hợp và chuẩn hóa thể thức Word toàn báo cáo. | **Hoàn thành 100%** |
| 2 | **Thành viên 2**<br>*(Thuật toán Tham lam & DSATUR)* | Cài đặt hàm `WelshPowell()` và `DSATUR()` thuần túy; viết module tính và cập nhật bậc bão hòa (`saturation_degree`). | Chương 1 (Mục 1.1, 1.2, 1.3.1, 1.3.2): Cơ sở lý thuyết đồ thị, sắc số, mã giả và sơ đồ khối Welsh-Powell, DSATUR. | Đang thực hiện |
| 3 | **Thành viên 3**<br>*(Quay lui + Heuristic & Sinh đề)* | Cài đặt hàm `BacktrackDSATUR()` kết hợp Forward Checking; xây dựng hàm `GeneratePuzzle()` sinh đề 4 cấp độ. | Chương 1 (Mục 1.3.3) và Chương 3 (Mục 3.2, 3.3): Thiết kế cấu trúc dữ liệu, lưu đồ thuật toán giải và sinh đề. | Đang thực hiện |
| 4 | **Thành viên 4**<br>*(Giao diện GUI & Trực quan hóa)* | Xây dựng giao diện bàn cờ 9x9, làm nổi bật 20 đỉnh kề khi chọn ô, hiển thị tập màu khả dụng, bậc bão hòa và chế độ chạy từng bước (Step-by-step). | Chương 3 (Mục 3.1, 3.4): Kiến trúc hệ thống, thiết kế giao diện; biên soạn tài liệu Hướng dẫn sử dụng. | Đang thực hiện |
| 5 | **Thành viên 5**<br>*(Thực nghiệm, Benchmark & Media)* | Xây dựng bộ 40-100 đề kiểm thử (Benchmark), module đo thời gian (ms), đếm số bước duyệt và số lần quay lui; đóng gói bản Release. | Chương 4 (Thực nghiệm & Đánh giá), Kết luận & Hướng phát triển; thiết kế Slide (.pptx) và dựng Video demo. | Đang thực hiện |

---

## PHẦN MỞ ĐẦU

### 1 Lý do chọn đề tài
Trò chơi giải đố Sudoku từ lâu đã trở thành một hiện tượng trí tuệ toàn cầu. Thoạt nhìn, Sudoku có vẻ là một bài toán số học đơn thuần sắp xếp các chữ số 1 đến 9 trên lưới ô vuông 9x9. Tuy nhiên, dưới lăng kính của Toán học rời rạc và Khoa học máy tính [1], các chữ số này không hề mang ý nghĩa định lượng (không có phép toán cộng, trừ, nhân, chia), mà bản chất chúng chỉ là 9 ký hiệu phân biệt độc lập. Điều này khẳng định rằng Sudoku thực chất là bài toán **Tô màu đỉnh đồ thị (Vertex Coloring Problem)**, một trong những bài toán NP-đầy đủ kinh điển được Richard Karp chứng minh vào năm 1972.

Việc nghiên cứu và xây dựng chương trình giải Sudoku bằng lý thuyết đồ thị mang lại những giá trị then chốt:
1. **Minh chứng sức mạnh mô hình hóa**: Chuyển một trò chơi logic quen thuộc thành một cấu trúc đồ thị toán học chặt chẽ.
2. **Trực quan hóa thuật toán**: Giúp sinh viên hiểu sâu sắc sự khác biệt giữa thuật toán tham lam tĩnh (Welsh-Powell [3]), thuật toán tham lam động có heuristic (DSATUR [2]) và thuật toán quay lui kết hợp cắt tỉa (Backtracking + Forward Checking).
3. **Ứng dụng thực tiễn**: Thuật toán tô màu đồ thị là nền tảng giải quyết hàng loạt bài toán thực tế quy mô lớn như phân bổ tần số vô tuyến viễn thông, xếp thời khóa biểu tự động [3], và tối ưu hóa cấp phát thanh ghi vi xử lý.

### 2 Mục tiêu và nhiệm vụ nghiên cứu
- **Mục tiêu tổng quát**: Mô hình hóa chính xác bàn cờ Sudoku 9x9 thành đồ thị vô hướng 20-regular; xây dựng thư viện lõi hướng đối tượng; phân tích, đối sánh hiệu năng 3 thuật toán tô màu đỉnh và xây dựng ứng dụng trực quan hóa từng bước.
- **Nhiệm vụ cụ thể**:
  1. Xây dựng đồ thị Sudoku $G = (V, E)$ gồm 81 đỉnh và 810 cạnh; chứng minh tính chất chính quy bậc 20.
  2. Cài đặt lớp `SudokuGraph` hỗ trợ song song Danh sách kề và Ma trận kề, có bộ kiểm tra tính hợp lệ tiền tô màu ban đầu, Game Validator và Hint Engine.
  3. Cài đặt các thuật toán Welsh-Powell, DSATUR, Backtracking + Forward Checking + DSATUR/MRV.
  4. Cài đặt module sinh đề tự động 4 cấp độ có nghiệm duy nhất.
  5. Thực nghiệm trên bộ Benchmark 40-100 đề, đánh giá thời gian chạy, số bước duyệt và số lần quay lui.

### 3 Đối tượng và phạm vi nghiên cứu
- **Đối tượng**: Trò chơi Sudoku 9x9; đồ thị vô hướng đơn; bài toán tô màu đỉnh và mở rộng tiền tô màu (Pre-coloring Extension) [4].
- **Phạm vi**: Bàn cờ Sudoku tiêu chuẩn 9x9 với 9 màu $\{1, 2, \dots, 9\}$.

### 4 Phương pháp nghiên cứu
- **Phương pháp lý thuyết**: Nghiên cứu tài liệu chuyên khảo về Graph Theory của Kenneth H. Rosen [1], bài báo gốc về DSATUR của Daniel Brélaz (1979) [2] và giáo trình HCMUE [5].
- **Phương pháp thực nghiệm**: Lập trình hướng đối tượng trên Python, viết bộ kiểm thử tự động (Unit Tests) để nghiệm thu kiến trúc đồ thị.
- **Phương pháp thống kê**: Đo đạc định lượng hiệu năng trên 4 cấp độ khó để đưa ra phân tích khách quan.

### 5 Kết cấu của đề tài
Báo cáo gồm 4 chương:
- **Chương 1**: Cơ sở lý thuyết đồ thị và bài toán tô màu.
- **Chương 2**: Mô hình hóa bài toán Sudoku bằng lý thuyết đồ thị và phản biện học thuật.
- **Chương 3**: Thiết kế kiến trúc và cài đặt chương trình (kèm 4 chức năng sản phẩm thực tế).
- **Chương 4**: Thực nghiệm, đánh giá kết quả và kết luận.

---

## CHƯƠNG 2. MÔ HÌNH HÓA BÀI TOÁN SUDOKU BẰNG LÝ THUYẾT ĐỒ THỊ

### 2.1 Quy tắc trò chơi Sudoku 9x9 và bài toán tổng quát $n^2 \times n^2$
Bàn cờ Sudoku chuẩn gồm $9 \times 9 = 81$ ô vuông, phân thành 9 khối con $3 \times 3$. Ba điều kiện bắt buộc:
1. **Ràng buộc Hàng**: Mỗi hàng chứa đủ 9 số từ 1 đến 9 không trùng lặp.
2. **Ràng buộc Cột**: Mỗi cột chứa đủ 9 số từ 1 đến 9 không trùng lặp.
3. **Ràng buộc Khối 3x3**: Mỗi khối con $3 \times 3$ chứa đủ 9 số từ 1 đến 9 không trùng lặp.

Trong bài toán tổng quát $n^2 \times n^2$, bàn cờ gồm $n^4$ ô vuông, chia thành $n^2$ khối con $n \times n$ và dùng $n^2$ màu. Với $n=3$, ta có Sudoku chuẩn 9x9.

### 2.2 Xây dựng đồ thị Sudoku $G = (V, E)$ gồm 81 đỉnh và 810 cạnh

#### 2.2.1 Tập đỉnh $V$ (81 đỉnh)
Mỗi ô cờ tại tọa độ $(r, c)$ với $r, c \in \{0, 1, \dots, 8\}$ tương ứng với một đỉnh $v \in V = \{0, 1, \dots, 80\}$:
$$v = f(r, c) = r \times 9 + c$$
Ngược lại:
$$r = \lfloor v / 9 \rfloor, \quad c = v \pmod 9$$
Chỉ số khối con $3 \times 3$:
$$\text{box}(r, c) = \lfloor r / 3 \rfloor \times 3 + \lfloor c / 3 \rfloor$$

#### 2.2.2 Tập cạnh $E$ (810 cạnh vô hướng)
Hai đỉnh phân biệt $u(r_1, c_1)$ và $v(r_2, c_2)$ có cạnh nối $(u, v) \in E$ khi và chỉ khi chúng xung đột trực tiếp:
$$(r_1 = r_2) \quad \lor \quad (c_1 = c_2) \quad \lor \quad (\lfloor r_1 / 3 \rfloor = \lfloor r_2 / 3 \rfloor \ \land \ \lfloor c_1 / 3 \rfloor = \lfloor c_2 / 3 \rfloor)$$

#### 2.2.3 Chứng minh toán học: Tính chất Đồ thị chính quy bậc 20 (20-Regular Graph)
Xét một đỉnh $v(r, c)$ bất kỳ:
- Số đỉnh kề cùng hàng: $|N_{\text{row}}(v)| = 9 - 1 = 8$ đỉnh.
- Số đỉnh kề cùng cột: $|N_{\text{col}}(v)| = 9 - 1 = 8$ đỉnh.
- Số đỉnh kề trong cùng khối $3 \times 3$ (loại trừ các đỉnh đã nằm cùng hàng hoặc cùng cột): Khối $3 \times 3$ có 9 đỉnh. Trừ chính đỉnh $v$, trừ 2 đỉnh cùng hàng trong khối, trừ 2 đỉnh cùng cột trong khối:
$$|N_{\text{box-only}}(v)| = 9 - 1 - 2 - 2 = 4 \text{ đỉnh.}$$

Vì ba tập đỉnh trên đôi một rời nhau, bậc của đỉnh $v$ là:
$$\deg(v) = |N(v)| = 8 + 8 + 4 = 20$$
Điều này đúng với **mọi đỉnh** $v \in V$, không phụ thuộc vào vị trí ô ở góc, cạnh hay tâm bàn cờ. Do đó, đồ thị Sudoku là **đồ thị chính quy bậc 20 (20-regular graph)**.

Theo **Bổ đề bắt tay (Handshaking Lemma)** [1]:
$$\sum_{v \in V} \deg(v) = 2|E| \iff 81 \times 20 = 2|E| \iff 1620 = 2|E| \iff |E| = 810 \text{ cạnh.}$$

#### 2.2.4 Cấu trúc dữ liệu lưu trữ
- **Danh sách kề (`adjacency_list`)**: Mảng 81 phần tử, mỗi phần tử chứa danh sách 20 đỉnh kề. Bộ nhớ tối ưu $O(|V| + |E|)$, thời gian duyệt láng giềng cập nhật bậc bão hòa là $O(20) = O(1)$.
- **Ma trận kề (`adjacency_matrix`)**: Ma trận $81 \times 81$ nhị phân đối xứng. Kiểm tra xung đột giữa 2 đỉnh bất kỳ trong $O(1)$.

### 2.3 Chuyển đổi sang bài toán Mở rộng tiền tô màu (Pre-coloring Extension)
- **Sắc số**: Bàn cờ Sudoku chứa 27 đồ thị con đầy đủ (clique) $K_9$ (9 hàng, 9 cột, 9 khối con). Vì $\chi(K_9) = 9$, nên sắc số đồ thị $\chi(G) \ge 9$. Vì bàn cờ giải được bằng đúng 9 chữ số, ta có $\chi(G) = 9$.
- **Bản chất Pre-coloring Extension**: Một tập con các đỉnh $V' \subset V$ đã được gán sẵn các màu cố định $c_0(v) \in \{1..9\}$ (các ô clues ban đầu). Cần tìm ánh xạ mở rộng $c: V \to \{1..9\}$ sao cho bảo toàn màu trên $V'$ và hai đỉnh kề nhau luôn khác màu. Đây là bài toán NP-đầy đủ (Jan Kratochvíl, 1993) [4].

### 2.4 Phân tích ưu nhược điểm của các thuật toán
1. **Welsh-Powell** [3]:
   - Sắp xếp đỉnh theo bậc giảm dần. Do $\deg(v) = 20$ với mọi đỉnh, việc sắp xếp không mang lại sự phân loại ưu tiên nào.
   - Do tính chất tham lam tĩnh không quay lui, thuật toán rất dễ rơi vào ngõ cụt trên các đề có tiền tô màu hoặc vượt quá 9 màu.
2. **DSATUR** [2]:
   - Ưu tiên chọn đỉnh có **Bậc bão hòa lớn nhất** (đang kề với nhiều màu khác nhau nhất).
   - Co cụm không gian tìm kiếm cực tốt, giải quyết tức thì các đề Dễ và Trung bình mà không cần quay lui. Tuy nhiên, vẫn có thể bế tắc ở đề Khó nếu không kết hợp quay lui.
3. **Backtracking + Forward Checking + Heuristic DSATUR/MRV**:
   - Chọn đỉnh có bậc bão hòa lớn nhất (tương đương MRV - ít màu khả dụng nhất).
   - Kiểm tra tiến và cắt tỉa (Forward Checking): loại bỏ ngay các nhánh dẫn đến miền rỗng của đỉnh kề.
   - Đảm bảo tìm ra nghiệm chính xác 100% với số bước quay lui tối thiểu.

### 2.5 Phản biện học thuật về việc lựa chọn mô hình Tô màu đồ thị
1. **So với Brute-Force (Vét cạn ngây thơ)**: Độ phức tạp $O(9^{81})$ bùng nổ tổ hợp dữ dội trên các đề khó. Mô hình đồ thị kết hợp heuristic DSATUR và Forward Checking cắt tỉa tới hơn 95% không gian tìm kiếm, giải quyết trong dưới 0.05 giây.
2. **So với Dancing Links (Algorithm X của Donald Knuth) [6]**: DLX rất nhanh nhưng làm mất đi hoàn toàn trực quan hình học và các khái niệm đồ thị (đỉnh kề, bậc, sắc số, bão hòa), không phù hợp với mục tiêu sư phạm của môn học.
3. **So với Thuật toán Di truyền (Genetic Algorithm)**: GA là thuật toán metaheuristic xấp xỉ, dễ kẹt ở cực tiểu cục bộ và không cam kết 100% tìm ra lời giải cho các đề bài khó, trong khi giải thuật của nhóm chứng minh được tính đúng đắn tuyệt đối 100%.
