# TÀI LIỆU HƯỚNG DẪN & BỘ QUY CHUẨN ĐỒ ÁN CUỐI KỲ
## HỌC PHẦN: LÝ THUYẾT ĐỒ THỊ VÀ ỨNG DỤNG - KHOA CNTT, HCMUE
### ĐỀ TÀI: GIẢI TRÒ CHƠI SUDOKU BẰNG THUẬT TOÁN TÔ MÀU ĐỒ THỊ

---

## 1. QUY CHUẨN CHẤM BÀI BÁO CÁO WORD

### 1.1. Quy tắc đặt dấu đề mục (Chuẩn thể thức học thuật)
- **Số thứ tự đề mục:** Sử dụng số Ả Rập phân cấp bằng dấu chấm (`1.1`, `1.1.1`, `2.3.2`). **Tuyệt đối KHÔNG đặt dấu chấm hoặc dấu chấm phẩy sau con số cuối cùng.**
  - *Đúng:* `1.1 Cơ sở lý thuyết đồ thị`
  - *Sai:* `1.1. Cơ sở lý thuyết đồ thị` hoặc `1.1; Cơ sở lý thuyết đồ thị`
- **Cuối câu tên đề mục:** **Tuyệt đối KHÔNG đặt bất kỳ dấu chấm câu nào** ở cuối dòng tiêu đề (không chấm `.`, không chấm phẩy `;`, không hai chấm `:`).
  - *Đúng:* `2.2 Xây dựng đồ thị Sudoku gồm 81 đỉnh và 810 cạnh`
  - *Sai:* `2.2 Xây dựng đồ thị Sudoku gồm 81 đỉnh và 810 cạnh.`
- **Dấu ngắt câu trong đoạn văn:** Dấu phẩy (`,`), chấm (`.`), chấm phẩy (`;`), hai chấm (`:`) phải đặt dính liền ký tự đứng trước, theo sau là 1 dấu cách trống rồi mới đến ký tự tiếp theo.

### 1.2. Quy tắc đưa mã nguồn (Source Code) vào Báo cáo
- **Không nhồi nhét code:** Tuyệt đối không copy hàng chục hay hàng trăm dòng code vào cuối mục hoặc cuối báo cáo làm phình phụ lục. Mã nguồn hoàn chỉnh đã nằm trong thư mục `Source/`.
- **Chỉ trích đoạn ngắn cốt lõi:** Báo cáo chỉ đưa các đoạn code snippet ngắn từ **10 đến 20 dòng** cho thuật toán trọng tâm (ví dụ: hàm chọn đỉnh có `max(sat_deg)` trong DSatur, hàm kiểm tra an toàn `is_safe`, hàm cắt tỉa `Forward Checking`).
- **Ưu tiên Mã giả (Pseudocode) & Lưu đồ (Flowchart):** Giảng viên đánh giá rất cao việc mô tả thuật toán bằng Mã giả chuẩn học thuật kết hợp Sơ đồ khối trực quan thay vì code chi tiết của ngôn ngữ lập trình.

### 1.3. Trực quan hóa Báo cáo Word
- Bổ sung nhiều hình ảnh minh họa chất lượng cao:
  - Sơ đồ trực quan 81 đỉnh và 20 đỉnh kề của một ô.
  - Ảnh chụp màn hình giao diện thực tế qua từng bước: Khởi tạo bàn cờ, cảnh báo ô xung đột, gợi ý nước đi, kết quả giải.
  - Biểu đồ đối sánh thực nghiệm: Thời gian thực thi (ms) và số bước quay lui giữa 3 thuật toán (Welsh-Powell, DSatur, Backtracking).

### 1.4. Trích dẫn khoa học chuẩn & Tuyên bố sử dụng AI
- **Trích dẫn theo chuẩn IEEE:** Đánh số ngoặc vuông `[1]`, `[2]` trong nội dung bài viết và liệt kê đầy đủ thông tin xuất bản ở cuối báo cáo.
- **Tuyên bố sử dụng AI (AI Assistance Statement):** Ghi rõ mục đích sử dụng AI một cách minh bạch (dùng AI để rà soát lỗi chính tả, hỗ trợ biên tập văn phong, đóng vai trò phản biện độc lập kiểm tra tính logic của các công thức toán học).

### 1.5. Quy trình nhờ AI duyệt lại Báo cáo Word trước khi nộp
1. Đưa từng chương vào AI để kiểm tra lỗi chính tả, dấu câu, ngắt câu và văn phong học thuật.
2. Kiểm tra tính đồng bộ của số liệu toán học: $|V| = 81$, $|E| = 810$, $\deg(v) = 20$, $\chi(G) = 9$.
3. Kiểm tra danh mục hình và bảng đã được viện dẫn trong lời văn chưa.

---

## 2. NÂNG CẤP CHỨC NĂNG SẢN PHẨM THỰC TẾ (SUDOKU GAME & SOLVER)

Để sản phẩm mang tính ứng dụng thực tế cao, nhóm bổ sung 4 chức năng chính:

### 2.1. Chức năng Tạo trò chơi (Game Generator)
- Áp dụng thuật toán `BacktrackDSATUR` sinh bảng hoàn chỉnh ngẫu nhiên.
- Xóa các ô theo tính chất đối xứng tâm để tạo đề bài đẹp mắt theo 4 cấp độ khó:
  - Dễ (Easy): 36 - 40 clues.
  - Trung bình (Medium): 32 - 35 clues.
  - Khó (Hard): 26 - 31 clues.
  - Chuyên gia (Expert): 22 - 25 clues.
- Tự động kiểm tra để đảm bảo màn chơi sinh ra có **đúng 1 nghiệm duy nhất**.

### 2.2. Chức năng Kiểm tra trò chơi thời gian thực (Game Validator)
- Khi người chơi nhập một số, hệ thống quét nhanh **20 đỉnh kề** $N(v)$ trên đồ thị.
- Nếu phát hiện trùng màu, lập tức làm nổi bật màu đỏ cảnh báo trên ô vi phạm và hiển thị thông báo xung đột (cùng hàng, cùng cột hay cùng ô $3 \times 3$).

### 2.3. Chức năng Kiểm tra khả giải và số nghiệm (Solvability Checker)
- Đếm số lượng nghiệm khả dĩ từ trạng thái hiện tại:
  - `0 nghiệm`: Bàn cờ đã bế tắc (người chơi đã đi sai ở bước trước).
  - `1 nghiệm`: Bàn cờ hợp lệ, có đường giải duy nhất dẫn đến chiến thắng.
  - `> 1 nghiệm`: Bàn cờ có nhiều hơn một cách giải.

### 2.4. Chức năng Gợi ý các bước giải tiếp theo (Hint Engine theo DSatur)
- Tìm ô có bậc bão hòa lớn nhất $\max(\text{sat\_deg})$ hoặc ô chỉ còn 1 màu khả dụng duy nhất (Naked Single - MRV = 1).
- Hiển thị gợi ý kèm theo lời giải thích logic đồ thị trực quan cho người chơi.

---

## 3. PHẢN BIỆN HỌC THUẬT: TẠI SAO CHỌN TÔ MÀU ĐỒ THỊ?

- **So với Brute-Force (Vét cạn ngây thơ):** Vét cạn có độ phức tạp $O(9^{81})$, bùng nổ tổ hợp trên các đề khó, trong khi Tô màu đồ thị kết hợp DSatur và Forward Checking cắt tỉa không gian tìm kiếm tới hơn 95%, giải bài toán trong chưa đầy 0.05 giây.
- **So với Dancing Links (Algorithm X của Knuth):** Dancing Links giải bài toán Bao phủ chính xác rất nhanh nhưng làm mất đi hoàn toàn trực quan hình học và các khái niệm đồ thị (đỉnh kề, bậc, sắc số, bão hòa), không phù hợp với mục tiêu sư phạm của môn học.
- **So với Thuật toán Di truyền (Genetic Algorithm):** GA là thuật toán metaheuristic xấp xỉ, dễ kẹt ở cực tiểu cục bộ và không cam kết 100% tìm ra lời giải cho các đề bài khó, trong khi giải thuật của nhóm chứng minh được tính đúng đắn tuyệt đối 100%.

---

## 4. QUY CHUẨN SLIDE POWERPOINT & BẢO VỆ ĐỒ ÁN

- **Quy chuẩn Slide:** Tuyệt đối không để code dài trên slide; thay thế bằng sơ đồ khối, hình ảnh bàn cờ và mã giả ngắn gọn (4-5 dòng).
- **Phân công đồng đều 5 thành viên:** Cả 5 thành viên đều phải lên bục thuyết trình (khoảng 2-3 phút/thành viên) và đều phải tham gia trả lời câu hỏi vấn đáp của Giảng viên.
- **Kịch bản Demo trực tiếp (5 - 10 phút):**
  1. Trực quan hóa cấu trúc đồ thị: Nhấp vào 1 ô, làm nổi bật 20 đỉnh kề.
  2. Tạo đề mới 4 cấp độ bằng Game Generator.
  3. Người chơi nhập thử số sai -> Hệ thống kích hoạt kiểm tra xung đột báo đỏ.
  4. Bấm "Gợi ý nước tiếp theo" -> Hệ thống giải thích lý do logic theo bậc bão hòa DSatur.
  5. Bấm "Kiểm tra khả giải" -> Báo trạng thái số nghiệm.
  6. Bấm "Giải tự động" -> Chạy mô phỏng từng bước (Step-by-step) hoặc giải siêu tốc.
- **Tác phong bảo vệ:** Tự tin, giọng to, dõng dạc, làm chủ hoàn toàn kiến thức đề tài, tuyệt đối không dùng AI để trả lời câu hỏi của Giảng viên.
