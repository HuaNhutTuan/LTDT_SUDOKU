# BÁO CÁO KHẢO SÁT CHỨC NĂNG CÁC NỀN TẢNG WEB SUDOKU HIỆN CÓ VÀ ĐỀ XUẤT CẢI TIẾN VỀ MẶT KỸ THUẬT LẪN HÌNH THỨC

---

## I. TỔNG QUAN KHẢO SÁT VÀ BỐI CẢNH ĐỀ TÀI

### 1.1. Bối cảnh thị trường Web Sudoku hiện nay

Trò chơi Sudoku tiêu chuẩn 9×9 là một trong những trò chơi giải đố số học và logic phổ biến nhất trên không gian số. Hiện tại trên Internet có hàng ngàn website và ứng dụng Sudoku phục vụ từ người chơi giải trí đại chúng (casual players) đến các vận động viên thi đấu logic chuyên nghiệp (competitive puzzle solvers).

Tuy nhiên, phần lớn các ứng dụng hiện nay được xây dựng dưới góc nhìn trò chơi giải đố thương mại hoặc logic học hình thức. Rất ít hoặc hầu như chưa có nền tảng nào khai thác trực quan bài toán Sudoku dưới lăng kính của **Lý thuyết Đồ thị** – cụ thể là bài toán **Tô màu đồ thị (Graph Coloring Problem)**, nơi mỗi ô là một đỉnh, mỗi ràng buộc hàng/cột/khối là một cạnh, và mỗi con số từ 1 đến 9 là một màu trong tập 9 màu khả dụng.

### 1.2. Mục đích khảo sát

1. **Phân tích toàn diện trải nghiệm người dùng (UX) và giao diện (UI):** Khảo sát các cơ chế tương tác, nhập liệu, ghi chú và hiển thị của các nền tảng Web Sudoku hàng đầu thế giới.
2. **Khảo sát giải thuật và động cơ hỗ trợ người chơi:** Đánh giá các cơ chế kiểm tra xung đột thời gian thực, hệ thống sinh đề, thẩm định số nghiệm và cơ chế gợi ý nước đi (Hint Engine).
3. **Chỉ ra khoảng trống công nghệ và sư phạm (Gaps):** Nhận diện điểm yếu của các web hiện nay (gợi ý thụ động chỉ điền sẵn đáp án, thiếu khả năng phân tích logic cấu trúc, giao diện quá tải quảng cáo hoặc quá cổ điển).
4. **Đề xuất cải tiến kỹ thuật và hình thức cho Đồ án HCMUE:** Định hình các tính năng đột phá nhằm tích hợp trực tiếp vào sản phẩm phần mềm của nhóm nghiên cứu môn Lý thuyết đồ thị và Ứng dụng.

---

## II. KHẢO SÁT CHI TIẾT CÁC NỀN TẢNG WEB SUDOKU TIÊU BIỂU

Nhóm đã tiến hành khảo sát thực nghiệm 5 nền tảng Web Sudoku tiêu biểu nhất trên thế giới, đại diện cho 5 phân khúc và triết lý thiết kế khác nhau:

---

### 2.1. Nền tảng 1: Sudoku.com (Easybrain)

- **Đơn vị phát triển:** Easybrain (Tập đoàn chuyên về puzzle game di động và web).
- **Phân khúc mục tiêu:** Người chơi đại chúng toàn cầu (Mass Market, Casual Players).

#### A. Tính năng nổi bật về Gameplay và Tương tác
- Hỗ trợ 6 cấp độ chơi: Fast, Easy, Medium, Hard, Expert, Master.
- Có sự kiện hàng ngày (Daily Challenges) và các giải đấu theo mùa (Seasonal Events).
- Cung cấp chế độ tính điểm, đồng hồ bấm giờ, và bảng xếp hạng người chơi.

#### B. Cơ chế Nhập liệu và Ghi chú (Input & Notes)
- Hỗ trợ linh hoạt cả 2 chế độ nhập:
  - *Cell-First (Chọn ô trước):* Người dùng nhấp chọn ô trống trên lưới 9×9 rồi nhấp số 1-9 trên bàn phím ảo hoặc gõ từ bàn phím vật lý.
  - *Digit-First (Chọn số trước):* Chọn trước 1 con số, sau đó nhấp liên tiếp vào các ô muốn điền số đó.
- *Chế độ Ghi chú (Pencil / Notes):* Bật/tắt biểu tượng bút chì để ghi nháp các số tiềm năng. Hệ thống tự động xóa số nháp tương ứng trong cùng hàng, cột và khối khi một ô được điền chính thức (Auto-remove notes).

#### C. Hệ thống Kiểm tra lỗi và Gợi ý (Validation & Hint Engine)
- Giới hạn sai sót (Mistakes Limit): Cho phép bật/tắt luật "3 mạng" (3 mistakes rule) – nếu điền sai quá 3 lần thì màn chơi kết thúc.
- Highlight thông minh: Tự động làm sáng toàn bộ các ô chứa cùng một con số đang chọn trên toàn bàn cờ; đồng thời highlight nhẹ hàng, cột và khối 3×3 chứa ô được chọn.
- **Hạn chế của Hint Engine:** Nút Gợi ý (Hint) của Sudoku.com chỉ đơn giản là điền thẳng con số đúng vào ô hiện tại mà không đưa ra bất kỳ lời giải thích logic hay thuật toán nào, mang tính chất "chép đáp án" thụ động.

#### D. Đánh giá Ưu và Nhược điểm
- *Ưu điểm:* Giao diện trau chuốt, màu sắc hài hòa, animation mượt mà, hỗ trợ cả Dark Mode và Light Mode, thao tác thân thiện với người dùng phổ thông.
- *Nhược điểm:* Chứa nhiều banner quảng cáo gây xao nhãng; cơ chế gợi ý không có tính sư phạm; không giải thích nguyên lý toán học.

---

### 2.2. Nền tảng 2: The New York Times Sudoku (NYT Games)

- **Đơn vị phát triển:** The New York Times Company.
- **Phân khúc mục tiêu:** Độc giả trí thức, người yêu thích trò chơi trí tuệ tinh tế và tối giản (Premium & Minimalist).

#### A. Tính năng nổi bật về Gameplay và Tương tác
- Phát hành định kỳ 3 bài toán mỗi ngày: Easy, Medium, Hard được tuyển chọn và kiểm duyệt kỹ lưỡng bởi chuyên gia biên tập puzzle.
- Không gian chơi tĩnh lặng tuyệt đối: Hoàn toàn không có quảng cáo, không pop-up, không nhạc nền gây mất tập trung.

#### B. Cơ chế Ghi chú Độc quyền (Two-Tier Pencil Marks)
- NYT Sudoku sở hữu cơ chế ghi chú 2 lớp được đánh giá cao nhất thế giới:
  - *Corner Marks (Ghi chú góc):* Ghi các số ứng viên tiềm năng ở các góc ô (thường áp dụng cho kỹ thuật Snyder Notation khi một số chỉ có thể xuất hiện ở 2 vị trí trong một khối 3×3).
  - *Center Marks (Ghi chú trung tâm):* Ghi tập hợp tất cả các số khả dĩ ở giữa ô (dùng cho phân tích tập màu khả dụng tại ô đó).

#### C. Tính năng Hỗ trợ người chơi
- Chế độ "Auto-Check": Tự động gạch chân đỏ cảnh báo ngay khi nhập số sai.
- Chế độ "Check Puzzle": Chỉ kiểm tra và hiển thị các ô bị sai khi người chơi chủ động bấm nút yêu cầu.
- Nút "Reveal": Cho phép hiển thị đáp án của một ô (Reveal Cell) hoặc toàn bộ bảng (Reveal Board).

#### D. Đánh giá Ưu và Nhược điểm
- *Ưu điểm:* Thiết kế Typography đẳng cấp, công thái học (ergonomics) xuất sắc, hệ thống ghi chú 2 lớp chuyên nghiệp, tải trang cực nhanh.
- *Nhược điểm:* Không có bộ sinh đề vô hạn (chỉ chơi được các đề hàng ngày), không phân tích nguyên lý giải thuật.

---

### 2.3. Nền tảng 3: SudokuPad / SudokuExchange.com (Cracking The Cryptic)

- **Đơn vị phát triển:** Sven Neumann và cộng đồng Sudoku quốc tế phối hợp với kênh Cracking The Cryptic.
- **Phân khúc mục tiêu:** Người chơi chuyên sâu, tuyển thủ thi đấu và cộng đồng nghiên cứu biến thể Sudoku (Power-Users, Enthusiasts).

#### A. Tính năng nổi bật về Gameplay và Tương tác
- Tối ưu hóa triệt để cho bàn phím máy tính: Hỗ trợ chuyển đổi chế độ siêu tốc bằng phím tắt (`Space`, `Shift`, `Ctrl`, `Alt`).
- Hỗ trợ đa dạng các biến thể Sudoku phức tạp: Killer Sudoku, Thermo Sudoku, Arrow Sudoku, German Whispers, Sandwich Sudoku...

#### B. Hệ thống Tô màu Ô và Đỉnh (Cell & Vertex Coloring Palette)
- **Tính năng đặc thù vượt trội:** Nền tảng cung cấp một bảng màu gồm 9 đến 12 màu sắc (Xanh lá, Xanh dương, Vàng, Đỏ, Tím, Cam...).
- Người chơi có thể tự do tô màu nền cho bất kỳ ô nào trên bàn cờ.
- Mục đích: Áp dụng các kỹ thuật suy luận chuỗi màu (Coloring Techniques, Simple Coloring, Multi-Coloring, 3D Medusa) để tìm kiếm mâu thuẫn chẵn/lẻ hoặc xác định tập độc lập.
- *Ý nghĩa đối với đề tài:* Đây là nền tảng thương mại hiếm hoi có sự tương đồng trực tiếp với tư tưởng "Tô màu đồ thị", tuy nhiên việc tô màu hiện vẫn làm hoàn toàn thủ công bằng tay của người chơi.

#### C. Đánh giá Ưu và Nhược điểm
- *Ưu điểm:* Bộ công cụ suy luận mạnh nhất hiện nay cho người chơi nâng cao, hỗ trợ vẽ đường nối (lines) và tô màu ô tự do, mã nguồn mở, cộng đồng đông đảo.
- *Nhược điểm:* Đường cong học tập dốc (khó sử dụng đối với người mới bắt đầu), giao diện kỹ thuật chuyên sâu, chưa có hệ thống tự động nhận diện đỉnh kề đồ thị.

---

### 2.4. Nền tảng 4: Andrew Stuart's SudokuWiki Solver

- **Đơn vị phát triển:** Andrew Stuart (Chuyên gia giải thuật Sudoku hàng đầu).
- **Phân khúc mục tiêu:** Công cụ phân tích, giải thuật toán và nghiên cứu logic học thuật (Academic & Logic Solver Engine).

#### A. Tính năng nổi bật về Động cơ Giải (Solver Engine)
- Được xem là "bách khoa toàn thư" chuẩn mực nhất về thuật toán giải Sudoku dựa trên logic thuần túy (Human-style Logic Strategies).
- Hỗ trợ phân tích hơn 30 kỹ thuật giải từ cơ bản đến siêu khó: Naked Single, Hidden Single, Naked Pair/Triple/Quad, Pointing Pairs, Box/Line Reduction, X-Wing, Swordfish, Jellyfish, XY-Wing, XYZ-Wing, Simple Coloring, Forcing Chains, Bivalue Universal Grave (BUG), Aligned Pair Exclusion...

#### B. Cơ chế Gợi ý và Giải thích Sư phạm (Pedagogical Step-by-Step)
- Nút "Take Step": Không giải ngay lập tức mà chỉ thực hiện đúng 1 bước suy luận logic tiếp theo khả dĩ.
- Khung giải thích chi tiết (Reasoning Box): Đưa ra diễn giải bằng lời rõ ràng: *"Tại hàng 4 và hàng 7, con số 5 chỉ có thể xuất hiện ở cột 2 và cột 8. Do đó hình thành cấu trúc X-Wing, cho phép loại bỏ số 5 khỏi tất cả các ô khác thuộc cột 2 và cột 8"*.
- Trực quan hóa tọa độ: Tô màu vàng các ô tạo lập cấu trúc và tô màu đỏ các ứng viên bị loại trừ.

#### C. Đánh giá Ưu và Nhược điểm
- *Ưu điểm:* Giá trị học thuật và sư phạm cao nhất; giúp người dùng hiểu rõ bản chất tại sao lại điền được con số đó; có thang điểm đánh giá độ khó chính xác (Difficulty Grade Score).
- *Nhược điểm:* Giao diện web cổ điển (HTML thô thập niên 2000), không responsive trên điện thoại di động, thao tác thủ công, chưa tận dụng mô hình đồ thị hóa tổng quát (Bậc bão hòa DSATUR).

---

### 2.5. Nền tảng 5: WebSudoku.com & LiveSudoku

- **Đơn vị phát triển:** Web Sudoku.
- **Phân khúc mục tiêu:** Người dùng truyền thống, người làm việc văn phòng cần giải trí nhanh gọn nhẹ (Classic & Lightweight).

#### A. Tính năng nổi bật
- Tối giản hóa ở mức tối đa: Chỉ gồm bàn cờ số 9×9, nút kiểm tra kết quả cuối cùng ("How am I doing?"), nút in ra giấy (Printable Sudoku).
- Tốc độ tải trang gần như tức thời (0.1 giây), tiêu tốn cực ít tài nguyên phần cứng.

#### B. Đánh giá Ưu và Nhược điểm
- *Ưu điểm:* Cực kỳ nhẹ, hoạt động tốt trên mọi trình duyệt cũ, có tính năng xuất file in ấn rất tiện lợi.
- *Nhược điểm:* Hoàn toàn thiếu vắng các trải nghiệm tương tác hiện đại (không có highlight tự động, không có gợi ý thông minh, không có cơ chế hoàn tác Undo/Redo trực quan).

---

## III. MA TRẬN ĐỐI SÁNH TỔNG HỢP CÁC TÍNH NĂNG (BENCHMARK MATRIX)

Bảng đối sánh chi tiết 5 nền tảng khảo sát theo các tiêu chí kỹ thuật và trải nghiệm người dùng:

| Tiêu chí Đánh giá & Tính năng | Sudoku.com | NYT Sudoku | SudokuPad | SudokuWiki | WebSudoku |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Giao diện hiện đại & Dark Mode** | Rất tốt (Có Dark) | Xuất sắc (Có Dark) | Tốt (Tùy biến) | Trung bình (Cổ điển) | Kém (HTML cũ) |
| **Chế độ nhập liệu (Cell/Digit First)** | Cả hai | Cả hai | Cả hai + Phím tắt | Cell-First | Cell-First |
| **Ghi chú 2 lớp (Corner & Center)** | Chỉ 1 lớp | Có (Rất tốt) | Có (Nâng cao) | Chỉ 1 lớp | Không hỗ trợ |
| **Tô màu ô tự do (Coloring Palette)** | Không | Không | Có (Đa dạng) | Tự động khi giải | Không hỗ trợ |
| **Highlight thông minh 20 đỉnh kề** | Có (Hàng/Cột/Khối) | Có | Không | Có khi giải | Không hỗ trợ |
| **Cảnh báo xung đột thời gian thực** | Có (3 lỗi giới hạn) | Có (Auto-check) | Có (Tùy chọn) | Không | Chỉ khi bấm nộp |
| **Động cơ Gợi ý (Hint Engine)** | Điền sẵn (Thụ động) | Tiết lộ đáp án | Không có | Giải thích Logic | Không có |
| **Giải thích cơ sở Lý thuyết Đồ thị** | Hoàn toàn không | Hoàn toàn không | Không | Không (Chỉ logic) | Hoàn toàn không |
| **Bộ sinh đề ngẫu nhiên vô hạn** | Có | Không (3 đề/ngày) | Nhập mã đề | Nhập mã đề | Có |
| **Đảm bảo nghiệm duy nhất (Unique)** | Đảm bảo | Đảm bảo | Tùy đề nhập | Tự động kiểm tra | Đảm bảo |
| **Cảnh báo Bế tắc (Deadlock Alert)** | Không | Không | Không | Có | Không |
| **Mô phỏng từng bước (Step-by-step)** | Không | Không | Không | Có (Từng bước) | Không |
| **Đo lường thời gian thực thi (ms)** | Không | Không | Không | Có | Không |

---

## IV. ĐỀ XUẤT CẢI TIẾN TOÀN DIỆN VỀ MẶT KỸ THUẬT (TECHNICAL PROPOSALS)

Dựa trên kết quả khảo sát các nền tảng thực tế và yêu cầu chuyên môn của đồ án Lý thuyết đồ thị tại HCMUE, nhóm đề xuất 5 cải tiến kỹ thuật mang tính đột phá:

---

### 4.1. Kiến trúc Động cơ Đồ thị thời gian thực (Real-time Graph Engine)

- **Hạn chế của các web hiện nay:** Đa số các web Sudoku chỉ lưu trữ trạng thái bàn cờ dưới dạng ma trận số 2 chiều 9×9 (`board[9][9]`). Khi cần kiểm tra tính hợp lệ, hệ thống phải chạy 3 vòng lặp riêng biệt (quét hàng, quét cột, quét khối).
- **Cải tiến kỹ thuật của nhóm:**
  - Xây dựng mô hình Đồ thị vô hướng chính quy bậc 20: Bàn cờ được mô hình hóa chính xác bằng đồ thị G = (V, E) với |V| = 81 đỉnh và |E| = 810 cạnh. Mỗi đỉnh v có đúng 20 đỉnh kề liên thuộc: N(v) = 8 (hàng) + 8 (cột) + 4 (khối 3×3).
  - Sử dụng cấu trúc Bitmask 9-bit biểu diễn tập màu khả dụng: Mỗi đỉnh quản lý một mặt nạ bit `available_colors`. Khi một đỉnh kề được gán màu c, hệ thống loại bỏ bit c bằng phép toán bitwise `AND NOT` với độ phức tạp thời gian chỉ O(1).
  - Cập nhật tức thời Bậc bão hòa (Saturation Degree): Duy trì biến `sat_deg(v)` cho mỗi đỉnh đại diện cho số lượng màu khác nhau đã gán cho 20 đỉnh kề, tự động tăng/giảm ngay khi người chơi điền hoặc xóa số.

---

### 4.2. Hệ thống Gợi ý Sư phạm dựa trên Heuristic DSATUR (Pedagogical Graph Hint Engine)

- **Hạn chế của các web hiện nay:** Nút Hint của Sudoku.com chỉ "ném" con số đúng vào ô; người chơi không học được phương pháp suy luận. Ngược lại, SudokuWiki giải thích quá dài dòng theo các thuật toán tên gọi phức tạp (X-Wing, Jellyfish) khó tiếp cận với người học phổ thông.
- **Cải tiến kỹ thuật của nhóm:** Xây dựng Động cơ gợi ý chuẩn mực Sư phạm dựa trên nguyên lý DSATUR:
  - *Bước 1 (Quét Heuristic):* Thuật toán quét toàn bộ các đỉnh chưa tô màu, tìm đỉnh v* có bậc bão hòa lớn nhất: `v* = argmax(sat_deg(v))`.
  - *Bước 2 (Phát hiện Naked Single):* Nếu `sat_deg(v*) = 8`, tập màu khả dụng chỉ còn đúng 1 màu duy nhất |C(v*)| = 1. Hệ thống phát tín hiệu gợi ý mức 1.
  - *Bước 3 (Diễn giải ngôn ngữ đồ thị trực quan):* Hiển thị bảng pop-up sư phạm thân thiện:
    > *"Gợi ý tại ô (Hàng 3, Cột 5): Ô này có bậc bão hòa đạt cực đại (sat_deg = 8). Trong 20 đỉnh kề của ô này, các đỉnh hàng xóm đã chiếm trọn 8 màu khác nhau là {1, 2, 3, 4, 6, 7, 8, 9}. Do nguyên lý tô màu đồ thị (hai đỉnh kề nhau không được cùng màu), ô này bắt buộc phải nhận màu duy nhất còn lại là 5!"*
  - *Bước 4 (Phát hiện Hidden Single qua Tập kề):* Nếu không có ô nào đạt `sat_deg = 8`, hệ thống quét trong 20 đỉnh kề để tìm màu chỉ còn xuất hiện duy nhất 1 lần trong miền giá trị của hàng/cột/khối.

---

### 4.3. Động cơ Thẩm định Khả giải và Cảnh báo Bế tắc (Solvability & Deadlock Checker)

- **Hạn chế của các web hiện nay:** Người chơi điền một con số không bị xung đột tức thời với hàng/cột/khối, nhưng nước đi đó dẫn tới việc bàn cờ không còn lời giải hợp lệ (bế tắc về mặt cấu trúc). Các web thông thường không hề cảnh báo, khiến người chơi mất hàng giờ điền tiếp rồi mới phát hiện vô nghiệm.
- **Cải tiến kỹ thuật của nhóm:**
  - Tích hợp giải thuật `BacktrackDSATUR` kết hợp `Forward Checking` chạy ngầm.
  - Thiết lập cơ chế kiểm tra đa luồng (Web Worker / Background Thread): Sau mỗi nước đi của người chơi, hệ thống kích hoạt bộ đếm số nghiệm:
    - **0 nghiệm (Deadlock - Bế tắc):** Bàn cờ không còn đường giải. Lập tức hiển thị huy hiệu cảnh báo màu cam: *"Nước đi gần nhất đã đưa đồ thị vào trạng thái không thể mở rộng tô màu. Khuyến nghị sử dụng nút Hoàn tác (Undo)!"*.
    - **1 nghiệm (Unique Solution - An toàn):** Trạng thái bảng cờ hoàn hảo, có duy nhất 1 con đường dẫn đến chiến thắng.
    - **> 1 nghiệm (Multiple Solutions - Đa nghiệm):** Bảng cờ có nhiều hơn 1 cách điền số (thường xảy ra khi người chơi tự nhập đề tùy biến).

---

### 4.4. Bộ sinh đề ngẫu nhiên Đối xứng tâm chuẩn Quốc tế (Symmetric Puzzle Generator)

- **Hạn chế của các web hiện nay:** Nhiều web sinh đề bằng cách xóa ô ngẫu nhiên không theo quy luật, tạo ra bàn cờ lộn xộn, mất mỹ quan và dễ sinh ra đề có nhiều nghiệm.
- **Cải tiến kỹ thuật của nhóm:**
  - *Giai đoạn 1 (Tô màu bảng đầy đủ):* Sử dụng `BacktrackDSATUR` với thứ tự chọn màu ngẫu nhiên (Randomized Color Ordering) để sinh ra một đồ thị hợp lệ hoàn chỉnh 81 đỉnh.
  - *Giai đoạn 2 (Đào ô đối xứng tâm - Rotational Point Symmetry):* Chọn ngẫu nhiên ô (r, c) và ô đối xứng qua tâm (8-r, 8-c). Xóa màu tại 2 đỉnh này.
  - *Giai đoạn 3 (Thẩm định nghiệm duy nhất):* Chạy `CountSolutions()` với ngưỡng dừng limit = 2. Nếu số nghiệm = 1 thì giữ nguyên việc xóa; nếu số nghiệm > 1 thì khôi phục lại 2 ô đó.
  - *Phân chia 4 cấp độ khó chuẩn hóa:*
    - **Dễ (Easy):** 36 đến 40 clues (sat_deg khởi điểm cao, giải được phần lớn bằng DSATUR thuần túy).
    - **Trung bình (Medium):** 32 đến 35 clues.
    - **Khó (Hard):** 26 đến 31 clues (bắt đầu đòi hỏi quay lui Forward Checking).
    - **Chuyên gia (Expert):** 22 đến 25 clues (không gian tìm kiếm phức tạp).

---

### 4.5. Kiến trúc Công nghệ đề xuất (Recommended Modern Tech Stack)

| Thành phần hệ thống | Công nghệ đề xuất | Lý do lựa chọn và Tối ưu hóa |
| :--- | :--- | :--- |
| **Frontend Framework** | React 19 / Next.js hoặc Vue 3 | Kiến trúc component hóa, quản lý state reactivity mượt mà khi người dùng tương tác liên tục trên 81 ô. |
| **Styling & Animation** | Tailwind CSS + Framer Motion | Xây dựng giao diện Responsive, animation chuyển cảnh 60fps khi tô màu, làm nổi bật 20 đỉnh kề. |
| **Background Processing** | Web Workers | Đẩy toàn bộ tác vụ giải thuật nặng (BacktrackDSATUR, đếm nghiệm) sang luồng riêng, không làm đơ giao diện chính. |
| **Core Algorithm Engine** | TypeScript hoặc WebAssembly (Wasm từ C++/Python) | Tối ưu hóa tốc độ tính toán bitwise và duyệt đồ thị xuống dưới 10 mili-giây. |
| **State Management** | Zustand / Redux Toolkit | Quản lý lịch sử nước đi dạng ngăn xếp kép (Undo Stack / Redo Stack) và tự động đồng bộ LocalStorage. |

---

## V. ĐỀ XUẤT CẢI TIẾN VỀ MẶT HÌNH THỨC VÀ GIAO DIỆN (UI/UX PROPOSALS)

---

### 5.1. Trực quan hóa Cấu trúc Đồ thị 20 Đỉnh kề (Neighborhood Glow Effect)

- **Mô tả thiết kế:**
  - Khi người dùng rê chuột (hover) hoặc bấm chọn một ô bất kỳ v=(r, c):
    - Ô trung tâm v được viền sáng (Focus Ring).
    - **20 ô kề N(v)** thuộc cùng hàng r, cùng cột c và cùng khối 3×3 lập tức đổi màu nền nhẹ nhàng (subtle highlight) để người chơi nhìn thấy trực quan "phạm vi liên thuộc" của đỉnh đồ thị.
    - Tất cả các ô khác trên bàn cờ đang chứa cùng con số với ô v sẽ phát sáng màu tương phản để người dùng dễ dàng kiểm tra các đỉnh độc lập (Independent Set).
- **Lợi ích thị giác:** Giúp người mới chơi lẫn người nghiên cứu toán học "nhìn thấy" được đồ thị vô hướng 20-regular ngay trên lưới số 9×9 quen thuộc mà không bị rối mắt.

---

### 5.2. Chế độ Hiển thị Kép (Dual Presentation Mode)

Hệ thống cho phép chuyển đổi tức thì giữa 2 giao diện phục vụ 2 mục đích khác nhau thông qua một nút gạt:

1. **Chế độ Chơi tiêu chuẩn (Player / Zen Mode):**
   - Lấy cảm hứng từ NYT Games: Tối giản, không viền thừa, font chữ sắc nét (Inter / Roboto Mono).
   - Hỗ trợ hoàn hảo Dark Mode (nền tối đen OLED dịu mắt, giảm căng thẳng thị giác khi chơi đêm).
   - Phục vụ người dùng muốn trải nghiệm một trò chơi giải đố thư giãn thuần khiết.
2. **Chế độ Đồ thị Sư phạm (Graph / Inspector Mode):**
   - Thiết kế đặc thù phục vụ Đồ án và Giảng dạy:
     - **Bảng 9 sắc thái màu (Color Palette 1-9):** Mỗi con số 1-9 được gắn với một màu sắc đặc trưng (Pastel). Khi điền số, ô vừa hiển thị con số vừa nhận màu nền tương ứng.
     - **Chỉ số Bậc bão hòa góc ô (Sat-Deg Badge):** Hiển thị một số nhỏ ở góc trên bên phải mỗi ô trống, báo hiệu `sat_deg` hiện thời (0 đến 8). Người dùng dễ dàng nhận ra ô nào sắp "bão hòa" để ưu tiên xử lý.
     - **Thanh trượt tốc độ giải mô phỏng (Speed Slider):** Khi bấm "Giải tự động", thanh trượt cho phép điều chỉnh từ giải siêu tốc (Instant: < 0.05s) đến giải mô phỏng từng bước (Step-by-step: 50ms - 1000ms/bước) kèm hiệu ứng đổi màu sinh động.
     - **Thanh đo độ phủ đồ thị (Chromatic Progress Bar):** Đo tỷ lệ hoàn thành tô màu đồ thị từ 0/81 đỉnh đến 81/81 đỉnh.

---

### 5.3. Công thái học Nhập liệu và Phím tắt Bàn phím (Ergonomic Input)

- Tích hợp thanh công cụ bàn phím số ảo đặt ngay dưới bàn cờ khi xem trên điện thoại hoặc máy tính bảng.
- Hỗ trợ hệ thống phím tắt bàn phím toàn diện:
  - `Phím mũi tên (Arrow keys)` hoặc `W/A/S/D`: Di chuyển con trỏ giữa 81 ô.
  - `Phím 1 đến 9` hoặc `Numpad 1-9`: Điền số hoặc màu tương ứng.
  - `Phím Space (Dấu cách)`: Bật/tắt nhanh giữa chế độ Điền chính thức và Ghi chú ứng viên (Pencil Note).
  - `Phím Delete / Backspace`: Xóa màu / giá trị ô hiện tại.
  - `Ctrl + Z / Ctrl + Y`: Hoàn tác (Undo) và Làm lại (Redo) không giới hạn số bước.
  - `Phím H (Hint)`: Mở hộp thoại giải thích gợi ý theo thuật toán DSATUR.
  - `Phím C (Check)`: Bật/tắt chế độ kiểm tra lỗi xung đột đồ thị.

---

### 5.4. Hệ thống Màu sắc Chuẩn mực và Khả năng Tiếp cận (Accessibility)

- **Tiêu chuẩn WCAG AAA:** Bộ 9 màu đại diện cho 9 đỉnh đồ thị được lựa chọn khoa học theo thang màu ColorBrewer/Pastel, có độ tương phản cao với chữ số màu đen/trắng.
- **Hỗ trợ người khiếm thị màu (Colorblind-Friendly):** Đảm bảo cả người bị mù màu đỏ - xanh lá (Deuteranopia/Protanopia) vẫn phân biệt rõ ràng 9 màu thông qua sự kết hợp giữa con số hiển thị và độ bão hòa ánh sáng.
- **Phản hồi xúc giác và thị giác (Feedback):**
  - Khi điền một số hợp lệ: Hiệu ứng sóng nhẹ (Ripple animation).
  - Khi vi phạm xung đột 20 đỉnh kề: Hai đỉnh xung đột nhấp nháy đỏ nhẹ nhàng (không rung lắc màn hình thô bạo), giúp người chơi nhận biết nguyên nhân vi phạm ngay lập tức.

---

## VI. KẾ HOẠCH TRIỂN KHAI VÀ TÍCH HỢP VÀO ĐỒ ÁN HCMUE

Dựa trên bảng phân công nhiệm vụ 5 thành viên của nhóm, các cải tiến trên sẽ được tích hợp vào sản phẩm báo cáo cuối kỳ như sau:

| Thành viên phụ trách | Hạng mục cải tiến triển khai thực tế | Sản phẩm đầu ra cụ thể |
| :--- | :--- | :--- |
| **Hứa Nhựt Tuấn** *(Nhóm trưởng)* | Quản lý kiến trúc lớp `SudokuGraph`, tích hợp bitmask cập nhật 20 đỉnh kề O(1), module `IOHandler` chuẩn hóa đề bài. | Mã nguồn lõi `Source/core/sudoku_graph.py`, tài liệu khảo sát tích hợp vào Báo cáo chính thức. |
| **Thành viên 2** | Nâng cấp Heuristic `DSATUR`, thuật toán trích xuất ô có `max(sat_deg)` và phát hiện Naked/Hidden Single. | Module `Source/core/hint_engine.py`, thuật toán sinh chuỗi giải thích sư phạm. |
| **Thành viên 3** | Xây dựng bộ sinh đề đối xứng tâm 4 cấp độ và module kiểm tra số lượng nghiệm `BacktrackDSATUR` + `Forward Checking`. | Module `Source/core/puzzle_generator.py` và `solvability_checker.py`. |
| **Thành viên 4** | Thiết kế giao diện đồ họa GUI (PyQt / Web GUI), hiệu ứng phát sáng 20 đỉnh kề, chế độ Chơi tiêu chuẩn & Chế độ Sư phạm. | Module `Source/gui/`, bộ theme Dark/Light mode, thanh trượt mô phỏng step-by-step. |
| **Thành viên 5** | Xây dựng bộ đo Benchmark (thời gian thực thi ms, số bước quay lui), đóng gói bản Release, quay video demo tính năng. | File chạy độc lập `Release/`, video thuyết trình demo các tính năng cải tiến. |

---

## VII. KẾT LUẬN

Bản khảo sát trên đã phân tích thấu đáo các ưu và nhược điểm của những nền tảng Web Sudoku hàng đầu thế giới hiện nay. Việc áp dụng lý thuyết đồ thị – cụ thể là bài toán Tô màu đồ thị và thuật toán Heuristic DSATUR – không chỉ mang lại giá trị học thuật xuất sắc cho học phần Lý thuyết đồ thị tại Khoa CNTT - HCMUE, mà còn tạo ra một sản phẩm phần mềm Sudoku hoàn toàn khác biệt: **Vừa giải trí mượt mà, vừa có giá trị giáo dục và trực quan hóa khoa học máy tính sâu sắc**.
