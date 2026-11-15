# TÀI LIỆU SLIDE THUYẾT TRÌNH & BỘ CÂU HỎI VẤN ĐÁP Q&A
## ĐỒ ÁN: GIẢI TRÒ CHƠI SUDOKU BẰNG THUẬT TOÁN TÔ MÀU ĐỒ THỊ
### PHÂN HỆ: THỰC NGHIỆM, KIỂM THỬ & MEDIA (THÀNH VIÊN 5)
**Khoa Công nghệ Thông tin - Trường Đại học Sư phạm TP. Hồ Chí Minh (HCMUE)**

---

## 1. KHUNG DÀN Ý 18 SLIDE POWERPOINT TOÀN NHÓM

| Slide | Nội dung trọng tâm | Người phụ trách trình bày |
|:---:|:---|:---:|
| **Slide 1** | Tiêu đề đồ án, tên đề tài, logo HCMUE, danh sách 5 thành viên nhóm. | Cả nhóm |
| **Slide 2** | Giới thiệu bài toán Sudoku & Động lực nghiên cứu dưới góc nhìn Lý thuyết đồ thị. | TV1 |
| **Slide 3** | Mô hình hóa đồ thị $G = (V, E)$: 81 đỉnh, 810 cạnh, tính chất chính quy 20-regular. | TV1 |
| **Slide 4** | Quy đổi Sudoku sang bài toán Mở rộng tiền tô màu (Pre-coloring Extension) với sắc số $\chi(G) = 9$. | TV1 |
| **Slide 5** | Thuật toán Welsh-Powell: Nguyên lý tham lam theo bậc giảm dần và giới hạn trên đồ thị chính quy. | TV2 |
| **Slide 6** | Thuật toán DSATUR (Brélaz, 1979): Khái niệm Bậc bão hòa ($\text{sat\_deg}$) và Heuristic chọn đỉnh động. | TV2 |
| **Slide 7** | Minh họa từng bước cập nhật bậc bão hòa và miền màu khả dụng trên bàn cờ Sudoku. | TV2 |
| **Slide 8** | Thuật toán Backtracking kết hợp Forward Checking và Heuristic DSATUR / MRV. | TV3 |
| **Slide 9** | Thuật toán sinh đề tự động 4 cấp độ (Game Generator) đảm bảo tính duy nhất của nghiệm. | TV3 |
| **Slide 10** | Kiến trúc hệ thống và 4 chức năng sản phẩm thực tế (Generator, Validator, Checker, Hint). | TV4 |
| **Slide 11** | Thiết kế giao diện người dùng (GUI) bàn cờ 9x9 và tính năng Highlight 20 đỉnh kề. | TV4 |
| **Slide 12 - 13** | Demo trực tiếp sản phẩm: Chế độ Step-by-step, điều chỉnh tốc độ mô phỏng tô màu. | TV4 & Nhóm |
| **Slide 14** | Môi trường thử nghiệm và Thiết kế Bộ dữ liệu Benchmark 40 đề chuẩn (Dễ, TB, Khó, Chuyên gia). | **TV5** |
| **Slide 15** | Bảng số liệu thực nghiệm đối sánh 120 lượt chạy trên 3 giải thuật (Thời gian, Quay lui, Gán màu). | **TV5** |
| **Slide 16** | Biểu đồ đối sánh hiệu năng và Phân tích bản chất thất bại 0% của Welsh-Powell vs 100% Backtrack-DSATUR. | **TV5** |
| **Slide 17** | Đóng gói sản phẩm Release chạy độc lập và Bộ công cụ Benchmark tự động. | **TV5** |
| **Slide 18** | Kết luận, Hạn chế, Hướng phát triển trong tương lai và Lời cảm ơn Hội đồng. | Cả nhóm |

---

## 2. KỊCH BẢN THUYẾT TRÌNH CHI TIẾT DÀNH CHO THÀNH VIÊN 5 (2 - 3 PHÚT)

> **[BƯỚC LÊN BỤC THUYẾT TRÌNH - TÁC PHONG TỰ TIN, DÕNG DẠC, CHÀO HỘI ĐỒNG]**
>
> *"Kính thưa Thầy/Cô trong Hội đồng và các bạn sinh viên, em là [Tên Thành viên 5], đại diện nhóm phụ trách Phân hệ Thực nghiệm, Đo lường hiệu năng và Đóng gói sản phẩm của đồ án.*
>
> *(Chuyển sang Slide 14)*  
> *Để kiểm chứng các cơ sở lý thuyết toán học mà các bạn vừa trình bày, em đã thiết kế một hệ thống kiểm thử Benchmark tự động với **bộ dữ liệu gồm đúng 40 đề Sudoku chuẩn**, phân bổ đều 4 cấp độ: từ Dễ (36 clues) đến Chuyên gia (17 đến 25 clues, trong đó có đề 17 clues tối thiểu của Gordon Royle và đề siêu khó AI Escargot). Toàn bộ 40 đề đều được kiểm tra toán học nghiêm ngặt để đảm bảo có duy nhất một nghiệm.*
>
> *(Chuyển sang Slide 15 - Bảng số liệu)*  
> *Chúng em đã tiến hành chạy độc lập **120 lượt thực nghiệm** trên 3 thuật toán bằng đồng hồ đo nano-giây. Kết quả định lượng cho thấy:*
> 1. *Thuật toán **Welsh-Powell** đạt tỷ lệ thành công **0%** trên toàn bộ 4 cấp độ.*
> 2. *Thuật toán **DSATUR thuần túy (không quay lui)** giải quyết xuất sắc **100% đề Dễ** chỉ trong 3.3 ms với 0 lần quay lui, nhưng giảm xuống 50% ở mức Trung bình và bế tắc ở mức Khó do không có cơ chế hoàn tác khi chọn sai nhánh.*
> 3. *Thuật toán **Backtracking kết hợp Forward Checking và Heuristic DSATUR** giải quyết thành công tuyệt đối **100% mọi đề bài**, tốc độ cực nhanh: chỉ **0.69 ms** cho đề Dễ và **58.85 ms** cho đề Chuyên gia 17 clues, với số bước quay lui được cắt tỉa triệt để.*
>
> *(Chuyển sang Slide 16 - Biểu đồ)*  
> *Nguyên nhân toán học cốt lõi khiến Welsh-Powell thất bại hoàn toàn nằm ở **tính chất chính quy bậc 20** của đồ thị Sudoku: mọi đỉnh ban đầu đều có bậc 20 như nhau, làm mất đi ưu thế sắp xếp theo bậc tĩnh của Welsh-Powell; cộng thêm các đỉnh tiền tô màu tạo ra các xung đột cục bộ khiến thuật toán tham lam rơi vào ngõ cụt sau chưa đầy 15 bước gán màu.*
>
> *(Chuyển sang Slide 17)*  
> *Cuối cùng, em đã hoàn thành việc đóng gói mã nguồn và phát triển kịch bản `run_benchmark.bat` cùng bộ đề trong thư mục `Release`, cho phép Hội đồng và người dùng có thể khởi chạy kiểm thử tự động một cách độc lập chỉ bằng một cú nhấp chuột.*
>
> *Em xin nhường lời lại cho bạn Nhóm trưởng để tổng kết bài thuyết trình. Em xin trân trọng cảm ơn Thầy/Cô!"*

---

## 3. BỘ CÂU HỎI VẤN ĐÁP PHẢN BIỆN Q&A DÀNH CHO THÀNH VIÊN 5

### Câu hỏi 1: Tại sao em đo thời gian bằng `time.perf_counter()` mà không dùng `time.time()`?
**Trả lời chuẩn:**
> *"Thưa Thầy/Cô, hàm `time.time()` phụ thuộc vào đồng hồ hệ thống (System Wall Clock) và có thể bị trôi, nhảy bước hoặc ảnh hưởng bởi việc đồng bộ giờ mạng NTP, độ phân giải thường chỉ đạt 10-15 ms trên Windows.  
> Trong khi đó, `time.perf_counter()` sử dụng bộ đếm phần cứng chuyên dụng (Performance Counter) có độ phân giải nano-giây và tính đơn điệu tuyệt đối (Monotonic Clock), đảm bảo không bao giờ đi lùi. Do các giải thuật của nhóm chạy siêu tốc chỉ mất từ 0.3 ms đến vài chục ms, việc dùng `time.perf_counter()` là bắt buộc để số liệu đo lường đạt độ chính xác khoa học."*

### Câu hỏi 2: Tại sao Welsh-Powell là thuật toán tô màu kinh điển mà lại giải Sudoku thất bại 0%? Có phải do code lỗi không?
**Trả lời chuẩn:**
> *"Thưa Thầy/Cô, hoàn toàn không phải do lỗi code mà xuất phát từ bản chất hình học của bài toán:  
> 1. Thuật toán Welsh-Powell hoạt động dựa trên việc phân bậc đỉnh để ưu tiên đỉnh bậc cao. Tuy nhiên, đồ thị Sudoku là **đồ thị chính quy bậc 20** ($\deg(v) = 20$ với mọi $v$), tức là trước khi có màu thì độ ưu tiên của mọi đỉnh là như nhau.  
> 2. Bài toán Sudoku là bài toán **Mở rộng tiền tô màu với sắc số cố định $\chi(G) = 9$ màu**. Welsh-Powell duyệt tĩnh tuần tự và gán màu tham lam cục bộ. Chỉ cần gán sai 1 ô, ô láng giềng kề tiếp theo sẽ bị 20 đỉnh kề vét cạn toàn bộ 9 màu khả dụng. Do không có cơ chế quay lui (Backtracking), thuật toán rơi vào Deadlock ngay lập tức (chỉ sau trung bình 7 đến 18 bước gán màu)."*

### Câu hỏi 3: Bộ dữ liệu 40 đề Benchmark của em được lấy từ đâu và làm sao em khẳng định mỗi đề có đúng 1 nghiệm?
**Trả lời chuẩn:**
> *"Thưa Thầy/Cô, bộ 40 đề được cấu trúc thành 4 tầng:  
> - Các đề Dễ, Trung bình, Khó được sinh bằng thuật toán đục lỗ đối xứng tâm từ một bảng giải hợp lệ với số clues tương ứng (36, 32, 26 clues).  
> - Cấp độ Chuyên gia tuyển chọn từ các đề bài nổi tiếng toán học thế giới: 2 đề 17 clues của Gordon Royle (số clues tối thiểu toán học để tồn tại nghiệm duy nhất), đề AI Escargot của Arto Inkala (2012) và đề Easter Monster.  
> - Trước khi đưa vào tệp Benchmark, toàn bộ 40 đề đều được chạy qua hàm `count_solutions(max_solutions=2)` của lớp `SudokuGraph` để xác nhận kết quả trả về đúng bằng 1. Nếu có $\ge 2$ nghiệm hoặc 0 nghiệm thì đề đó bị loại bỏ ngay lập tức."*

### Câu hỏi 4: Số lần quay lui (Backtracks) và số bước gán màu (Color Assignments) khác nhau như thế nào?
**Trả lời chuẩn:**
> *"Thưa Thầy/Cô:  
> - **Color Assignments (Số bước gán màu):** Là tổng số lần thuật toán thử điền một màu hợp lệ vào một đỉnh (mỗi lần gán `working_colors[v] = color` thì bộ đếm tăng 1).  
> - **Backtracks (Số lần quay lui):** Là số lần nhánh đệ quy đi vào ngõ cụt (phát hiện ô khác có 0 màu khả dụng hoặc đã thử hết màu mà không giải được), buộc phải gán trả lại `working_colors[v] = 0` để lùi lại thử nhánh khác.  
> Do đó, với các đề Dễ không rẽ nhánh, số lần quay lui bằng đúng 0 và số bước gán màu bằng đúng số ô trống cần điền (45 bước)."*
