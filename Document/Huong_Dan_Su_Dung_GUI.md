# TÀI LIỆU HƯỚNG DẪN SỬ DỤNG GIAO DIỆN ĐỒ HỌA (GUI)
## ĐỀ TÀI: GIẢI TRÒ CHƠI SUDOKU BẰNG THUẬT TOÁN TÔ MÀU ĐỒ THỊ
**Khoa Công nghệ Thông tin - Trường Đại học Sư phạm TP. Hồ Chí Minh (HCMUE)**  
**Phụ trách biên soạn:** Thành viên 4 (Giao diện GUI & Trực quan hóa)  
**Ngôn ngữ thực hiện:** Python 3 (Thư viện chuẩn `tkinter` - Chạy độc lập 100%, không cần cài đặt thêm thư viện)

---

## 1. HƯỚNG DẪN KHỞI CHẠY ỨNG DỤNG

### Cách 1: Chạy nhanh trên Windows (Khuyến nghị)
- Vào thư mục `Release/`, click đúp chuột vào tệp:
  ```text
  Release/run_gui.bat
  ```
- Ứng dụng sẽ tự động phát hiện Python trên máy và mở cửa sổ đồ họa ngay lập tức.

### Cách 2: Khởi chạy bằng dòng lệnh Terminal / PowerShell
Tại thư mục gốc của đồ án (`LTDT_SUDOKU`):
```bash
python run_gui.py
# Hoặc:
python -m Source.gui.sudoku_gui
```

---

## 2. BỐ CỤC GIAO DIỆN VÀ CÁC THÀNH PHẦN CHỨC NĂNG

Giao diện được thiết kế hiện đại, bố cục khoa học gồm **2 khu vực chính**:

```text
+-----------------------------------------------------------------------------------------+
| HCMUE - Giải Sudoku bằng Tô màu đồ thị | GUI Thành viên 4                               |
+---------------------------------------------------+-------------------------------------+
|                                                   | 1. THANH TRA ĐỒ THỊ (INSPECTOR)     |
|              BÀN CỜ SUDOKU 9x9                    | • Đỉnh v: Ô (Hàng, Cột, Khối 3x3)   |
|         G = (V, E) | 81 ĐỈNH - 810 CẠNH           | • Bậc deg(v) = 20                   |
|                                                   | • Bậc bão hòa (DSATUR): sat_deg/9   |
|   +-------+-------+-------+                       | • Miền màu khả dụng (MRV)           |
|   | 5 3 . | . 7 . | . . . |                       | • Cảnh báo xung đột Game Validator  |
|   | 6 . . | 1 9 5 | . . . |                       +-------------------------------------+
|   | . 9 8 | . . . | . 6 . |                       | 2. TRỰC QUAN HÓA (STEP-BY-STEP)     |
|   +-------+-------+-------+                       | • Tốc độ trễ: [---O---] (ms/bước)   |
|   | 8 . . | . 6 . | . . 3 |                       | • [▶ Chạy tự động]  [⏭ Bước tiếp]   |
|   | 4 . . | 8 . 3 | . . 1 |                       | • [⚡ Giải nhanh]                    |
|   | 7 . . | . 2 . | . . 6 |                       | • Thống kê số bước & số quay lui    |
|   +-------+-------+-------+                       +-------------------------------------+
|   | . 6 . | . . . | 2 8 . |                       | 3. BẢNG ĐIỀU KHIỂN & CHỨC NĂNG      |
|   | . . . | 4 1 9 | . . 5 |                       | • Đề mẫu: [Dễ] [TB] [Khó] [Ch.Gia]  |
|   | . . . | . 8 . | . 7 9 |                       | • [📂 Mở file]   [💡 Gợi ý (Hint)]  |
|   +-------+-------+-------+                       | • [🔍 Khả giải]  [↺ Đặt lại] [🗑 Xóa]|
|                                                   | • Nhật ký log sự kiện               |
| Phím tắt: [1..9] điền | [0/Del] xóa | [↑↓←→] di chuyển                                  |
+-----------------------------------------------------------------------------------------+
```

---

## 3. HƯỚNG DẪN THAO TÁC CHI TIẾT

### 3.1 Tương tác trên Bàn cờ 9x9 (Khu vực bên trái)
1. **Chọn ô cờ (Đỉnh $v$):**
   - Click chuột trái vào bất kỳ ô nào trên bàn cờ.
   - Ô đang chọn lập tức đổi sang nền màu **Xanh dương nổi bật (`#74b9ff`)**.
2. **Quan sát 20 đỉnh kề $N(v)$ (Tính năng trọng tâm đồ án):**
   - Khi chọn một ô, hệ thống tự động quét danh sách kề và highlight đúng **20 đỉnh kề** bằng nền **Xanh nhạt (`#e8f4fc`)**.
   - Người dùng dễ dàng nhận thấy 20 đỉnh này gồm:
     - $8$ đỉnh cùng hàng ngang.
     - $8$ đỉnh cùng cột dọc.
     - $4$ đỉnh còn lại trong cùng khối con $3 \times 3$.
3. **Nhập và xóa giá trị:**
   - **Điền số:** Nhấn các phím số từ `1` đến `9` trên bàn phím.
   - **Xóa số:** Nhấn phím `0`, `Delete` hoặc `Backspace`.
   - **Di chuyển nhanh:** Dùng 4 phím mũi tên `↑`, `↓`, `←`, `→` để di chuyển vùng chọn giữa các ô.
   - *Lưu ý:* Các ô số cố định của đề bài ban đầu (Precolored) có chữ màu xanh navy đậm và bị khóa không cho phép sửa để đảm bảo tính toàn vẹn của đề bài.

---

### 3.2 Bảng Thanh tra đồ thị (Graph Inspector)
Khi bạn click vào bất kỳ ô nào, bảng bên phải sẽ lập tức hiển thị thông số toán học:
- **Tọa độ đỉnh:** Chỉ số đỉnh $v \in \{0..80\}$, vị trí (Hàng $r+1$, Cột $c+1$) và số thứ tự khối $3 \times 3$ tương ứng.
- **Bậc của đỉnh:** $\deg(v) = 20$ (đẳng cấu trên toàn bộ 81 đỉnh vì đồ thị Sudoku là $20$-regular graph).
- **Bậc bão hòa (DSATUR):** Hiển thị số lượng màu khác nhau đang xuất hiện ở 20 đỉnh kề ($0/9$ đến $8/9$).
- **Miền màu khả dụng (MRV):** Danh sách các số trong $\{1..9\}$ chưa bị 20 đỉnh kề chiếm giữ. Nếu ô đang trống mà miền màu rỗng ($0$ màu), hệ thống sẽ cảnh báo trạng thái bế tắc (cần quay lui).
- **Game Validator thời gian thực:**
   - Nếu bạn điền một số hợp lệ: Hiển thị dòng màu xanh lá báo thành công.
   - Nếu bạn điền một số trùng với bất kỳ đỉnh nào trong 20 đỉnh kề: Ô đó lập tức **đổi nền màu Đỏ (`#ff7675`)**, đồng thời bảng thanh tra xuất cảnh báo cụ thể (ví dụ: *"Trùng màu 5 với ô (1, 1) cùng HÀNG 1"*).

---

### 3.3 Trực quan hóa giải từng bước (Step-by-step DSATUR)
Đây là tính năng quan trọng nhất để phục vụ phần thuyết minh và demo cho Giảng viên:
1. **Thanh trượt tốc độ (Speed Slider):**
   - Kéo về bên trái ($10\text{ms}$): Mô phỏng chạy cực nhanh.
   - Kéo về bên phải ($300\text{ms} - 500\text{ms}$): Mô phỏng chạy chậm từng bước để Giảng viên và sinh viên quan sát kỹ lưỡng.
2. **Nút `▶ Chạy tự động`:**
   - Tự động kích hoạt thuật toán quay lui kết hợp DSATUR.
   - Tại mỗi bước, ô có bậc bão hòa cao nhất sẽ được chọn và tô nền màu **Vàng cam (`#ffeaa7`)**, sau đó thử gán màu hợp lệ đầu tiên.
   - Nếu gặp ngõ cụt, ô sẽ tự động hủy màu và thuật toán quay lui về đỉnh trước đó.
   - Bạn có thể nhấn **`⏸ Tạm dừng`** bất kỳ lúc nào để phân tích trạng thái bàn cờ.
3. **Nút `⏭ Bước tiếp`:**
   - Cho phép bạn bấm từng bước một (Manual Step) để giải thích cơ chế chọn đỉnh của Heuristic DSATUR trong buổi báo cáo.
4. **Nút `⚡ Giải nhanh`:**
   - Giải hoàn tất bảng Sudoku ngay lập tức và hiển thị tổng số bước duyệt cùng số lần quay lui.
5. **Bộ đếm thời gian thực:**
   - Hiển thị số bước gán màu và số lần quay lui (Backtracks) tích lũy.

---

### 3.4 Bảng điều khiển nạp đề & Các chức năng mở rộng
1. **Nạp đề mẫu 4 cấp độ:**
   - Click vào các nút `[Dễ]`, `[Trung bình]`, `[Khó]`, `[Chuyên gia]`. Hệ thống sẽ tự động nạp các bộ đề kiểm thử chuẩn từ thư mục `Release/puzzles/`.
2. **Mở file đề (`📂 Mở file .txt`):**
   - Cho phép chọn file chứa ma trận 9x9 hoặc chuỗi 81 ký tự từ máy tính.
3. **Gợi ý nước đi (`💡 Gợi ý (Hint)`):**
   - Tích hợp **Hint Engine**: Tự động tìm ô tối ưu nhất theo nguyên lý Naked Single (MRV = 1) hoặc đỉnh có bậc bão hòa cao nhất.
   - Ô được gợi ý sẽ đổi sang nền **Xanh ngọc (`#55efc4`)** kèm hộp thoại giải thích chi tiết lý do toán học.
4. **Kiểm tra khả giải (`🔍 Kiểm tra khả giải`):**
   - Tích hợp **Solvability Checker**: Phân tích xem bàn cờ hiện tại đang có $0$ nghiệm (bế tắc), $1$ nghiệm duy nhất (chuẩn Sudoku), hay nhiều hơn $1$ nghiệm.
5. **Đặt lại bàn cờ (`↺ Đặt lại`):**
   - Xóa toàn bộ các ô người chơi hoặc thuật toán đã điền, chỉ giữ lại các ô tiền tô màu ban đầu của đề bài.
6. **Xóa trắng bàn cờ (`🗑 Xóa trắng`):**
   - Xóa toàn bộ 81 ô để người dùng tự nhập đề bài mới từ bàn phím.

---

## 4. BẢNG MÃ MÀU VÀ Ý NGHĨA TRỰC QUAN TRÊN GIAO DIỆN

| Mã màu Hex | Tên màu trực quan | Vị trí áp dụng | Ý nghĩa trong Lý thuyết đồ thị |
|:---:|:---:|:---|:---|
| `#74b9ff` | Xanh dương tươi | Nền ô đang chọn | Đỉnh $v \in V$ đang được khảo sát |
| `#e8f4fc` | Xanh pastel nhạt | Nền 20 ô xung quanh | Tập 20 đỉnh kề $N(v)$ chịu ràng buộc màu với $v$ |
| `#ff7675` | Đỏ san hô | Nền ô bị xung đột | Vi phạm định lý tô màu: $c(u) = c(v)$ với $(u, v) \in E$ |
| `#ffeaa7` | Vàng cam nhạt | Nền ô đang giải | Đỉnh đang được thuật toán DSATUR xử lý từng bước |
| `#55efc4` | Xanh ngọc | Nền ô được gợi ý | Đỉnh có bậc bão hòa lớn nhất hoặc Naked Single (MRV = 1) |
| `#192a56` | Xanh navy đậm | Chữ số đề bài | Đỉnh tiền tô màu cố định (Precolored Vertices) |
| `#273c75` | Xanh tím | Chữ số người điền | Đỉnh được gán màu trong quá trình giải |

---

## 5. BỘ CÂU HỎI VẤN ĐÁP Q&A THÀNH VIÊN 4 CẦN NẮM VỮNG KHI BẢO VỆ

1. **Câu hỏi:** *Tại sao khi click vào một ô, giao diện lại làm nổi bật đúng 20 ô khác mà không phải 24 ô?*
   - **Trả lời:** Vì mỗi ô cờ tương ứng với một đỉnh $v$ trên đồ thị Sudoku. Theo luật Sudoku, một đỉnh chịu ràng buộc với 8 ô cùng hàng, 8 ô cùng cột và 8 ô trong cùng khối $3 \times 3$. Tuy nhiên, trong 8 ô của khối $3 \times 3$ đã có 2 ô trùng với hàng và 2 ô trùng với cột của $v$. Do đó, số đỉnh kề duy nhất là $8 + 8 + 4 = 20$ đỉnh. Đồ thị Sudoku là đồ thị chính quy bậc 20 ($20$-regular graph).

2. **Câu hỏi:** *Bậc bão hòa (Saturation Degree) trên bảng thanh tra được tính như thế nào?*
   - **Trả lời:** Bậc bão hòa của đỉnh $v$ là số lượng **màu khác nhau** đã xuất hiện tại các đỉnh kề trong tập $N(v)$. Giá trị này dao động từ $0$ đến $9$. Thuật toán DSATUR luôn ưu tiên chọn đỉnh chưa tô có bậc bão hòa lớn nhất vì đó là đỉnh đang chịu nhiều ràng buộc nhất, giúp thu hẹp nhanh nhất không gian tìm kiếm.

3. **Câu hỏi:** *Làm thế nào để giao diện cập nhật từng bước (Step-by-step) mà không bị treo đơ (Not Responding)?*
   - **Trả lời:** Em sử dụng kỹ thuật **Python Generator** kết hợp hàm phi nghẽn `root.after()` của Tkinter. Thay vì chạy đệ quy lặp vô tận trên luồng chính, thuật toán `yield` ra từng bước gán màu hoặc quay lui. GUI nhận gói dữ liệu, vẽ lại Canvas và hẹn giờ gọi bước tiếp theo, giữ cho luồng giao diện luôn mượt mà và người dùng có thể bấm Tạm dừng bất kỳ lúc nào.
