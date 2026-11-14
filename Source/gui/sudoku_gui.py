"""
Giao diện đồ họa (GUI) cho đề tài: Giải trò chơi Sudoku bằng thuật toán Tô màu đồ thị.
Môn học: Lý thuyết đồ thị và Ứng dụng - Khoa CNTT, HCMUE.
Phụ trách: Thành viên 4 (Giao diện GUI & Trực quan hóa).

Tính năng chính tuần 1:
1. Lưới bàn cờ 9x9 (81 đỉnh) tương tác chuột và bàn phím.
2. Highlight trực quan 20 đỉnh kề N(v) khi click vào một ô.
3. Bảng thanh tra đồ thị (Graph Inspector): hiển thị bậc deg(v)=20, bậc bão hòa DSATUR,
   miền màu khả dụng (MRV) và trạng thái đỉnh.
4. Kiểm tra xung đột thời gian thực (Game Validator) trên 20 đỉnh kề.
5. Tích hợp Gợi ý nước đi (Hint Engine) và Kiểm tra tính khả giải (Solvability Checker).
6. Trực quan hóa giải từng bước (Step-by-step DSATUR Backtracking) với thanh trượt tốc độ.
"""

import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Optional, Set, List, Tuple

# Thêm đường dẫn gốc để import các mô-đun trong Source.core
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(CURRENT_DIR))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from Source.core.sudoku_graph import SudokuGraph, PrecoloringConflictError
from Source.core.io_handler import IOHandler


class SudokuGUI:
    """
    Lớp quản lý Giao diện đồ họa người dùng (Tkinter) kết nối với lõi đồ thị SudokuGraph.
    """

    # Bảng màu giao diện chuẩn, hiện đại và trực quan
    COLOR_BG = "#f5f6fa"
    COLOR_BOARD_BG = "#ffffff"
    COLOR_LINE_THICK = "#2f3640"      # Đường kẻ ngăn cách các khối 3x3
    COLOR_LINE_THIN = "#dcdde1"       # Đường kẻ giữa các ô trong khối
    COLOR_CELL_DEFAULT = "#ffffff"    # Màu nền ô bình thường
    COLOR_CELL_SELECTED = "#74b9ff"   # Ô đang được người dùng chọn
    COLOR_CELL_NEIGHBOR = "#e8f4fc"   # 20 đỉnh kề N(v) của ô đang chọn
    COLOR_CELL_CONFLICT = "#ff7675"   # Ô xung đột màu với đỉnh kề (Game Validator)
    COLOR_CELL_ACTIVE = "#ffeaa7"     # Ô đang được thuật toán xử lý (Step-by-step)
    COLOR_CELL_HINT = "#55efc4"       # Ô được bộ Hint Engine gợi ý

    COLOR_TEXT_PRECOLORED = "#192a56" # Số cố định đề bài (tiền tô màu)
    COLOR_TEXT_USER = "#273c75"       # Số do người dùng / thuật toán điền
    COLOR_TEXT_CONFLICT = "#c23616"   # Số bị xung đột

    CELL_SIZE = 52                     # Kích thước mỗi ô cờ (pixel)
    BOARD_PADDING = 15                 # Khoảng đệm bao quanh bàn cờ

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("HCMUE - Giải Sudoku bằng Tô màu đồ thị | GUI Thành viên 4")
        self.root.geometry("1060x680")
        self.root.minsize(980, 640)
        self.root.configure(bg=self.COLOR_BG)

        # Khởi tạo lõi đồ thị SudokuGraph (81 đỉnh, 810 cạnh, bậc 20)
        self.graph = SudokuGraph()

        # Trạng thái giao diện
        self.selected_vertex: Optional[int] = None
        self.hint_vertex: Optional[int] = None
        self.active_step_vertex: Optional[int] = None

        # Trạng thái mô phỏng Step-by-step
        self.step_generator = None
        self.is_auto_running = False
        self.stats_steps = 0
        self.stats_backtracks = 0

        # Nạp đề mẫu ban đầu
        self._load_default_sample()

        # Dựng các thành phần giao diện
        self._setup_ui()

        # Đăng ký sự kiện bàn phím
        self._bind_events()

        # Vẽ bàn cờ lần đầu
        self.render_board()
        self.update_inspector()

    # =========================================================================
    # KHỞI TẠO VÀ DỰNG BỐ CỤC GIAO DIỆN (UI SETUP)
    # =========================================================================

    def _setup_ui(self) -> None:
        """Thiết lập bố cục 2 cột: Cột trái (Bàn cờ) và Cột phải (Thanh tra & Điều khiển)."""
        main_frame = tk.Frame(self.root, bg=self.COLOR_BG, padx=15, pady=12)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Cột trái: Bàn cờ Sudoku 9x9
        left_frame = tk.Frame(main_frame, bg=self.COLOR_BG)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 15))

        # Tiêu đề bàn cờ
        header_lbl = tk.Label(
            left_frame,
            text="BÀN CỜ SUDOKU G = (V, E) | 81 ĐỈNH - 810 CẠNH",
            font=("Segoe UI", 11, "bold"),
            bg=self.COLOR_BG,
            fg="#2f3640"
        )
        header_lbl.pack(anchor="w", pady=(0, 6))

        # Canvas vẽ 81 ô Sudoku
        canvas_dim = self.CELL_SIZE * 9 + self.BOARD_PADDING * 2
        self.canvas = tk.Canvas(
            left_frame,
            width=canvas_dim,
            height=canvas_dim,
            bg=self.COLOR_BOARD_BG,
            highlightthickness=2,
            highlightbackground="#b2bec3",
            relief=tk.FLAT
        )
        self.canvas.pack()

        # Chú giải bàn phím dưới bàn cờ
        legend_frame = tk.Frame(left_frame, bg=self.COLOR_BG, pady=6)
        legend_frame.pack(fill=tk.X)
        legend_text = (
            "Phím tắt: Click chuột để chọn ô | Phím [1..9]: Điền số | [0/Delete]: Xóa ô\n"
            "Các phím mũi tên [↑ ↓ ← →]: Di chuyển giữa 81 đỉnh đồ thị"
        )
        tk.Label(
            legend_frame,
            text=legend_text,
            font=("Segoe UI", 8, "italic"),
            bg=self.COLOR_BG,
            fg="#636e72",
            justify=tk.LEFT
        ).pack(anchor="w")

        # Cột phải: Khung điều khiển & Thanh tra thông số đồ thị
        right_frame = tk.Frame(main_frame, bg=self.COLOR_BG)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self._setup_inspector_panel(right_frame)
        self._setup_step_solver_panel(right_frame)
        self._setup_control_panel(right_frame)

    def _setup_inspector_panel(self, parent: tk.Widget) -> None:
        """Khung 1: Thanh tra thông số đỉnh đồ thị (Graph Inspector)."""
        group = tk.LabelFrame(
            parent,
            text=" 1. THANH TRA ĐỒ THỊ (GRAPH INSPECTOR) ",
            font=("Segoe UI", 10, "bold"),
            bg=self.COLOR_BG,
            fg="#0984e3",
            padx=10,
            pady=8
        )
        group.pack(fill=tk.X, pady=(0, 8))

        # Thông tin đỉnh
        self.lbl_vertex_info = tk.Label(
            group,
            text="Đỉnh v: Chưa chọn ô nào",
            font=("Segoe UI", 10, "bold"),
            bg=self.COLOR_BG,
            fg="#2d3436",
            anchor="w"
        )
        self.lbl_vertex_info.pack(fill=tk.X)

        self.lbl_degree_info = tk.Label(
            group,
            text="Bậc của đỉnh: deg(v) = 20 (8 hàng + 8 cột + 4 khối 3x3)",
            font=("Segoe UI", 9),
            bg=self.COLOR_BG,
            fg="#636e72",
            anchor="w"
        )
        self.lbl_degree_info.pack(fill=tk.X)

        self.lbl_sat_info = tk.Label(
            group,
            text="Bậc bão hòa (DSATUR): - / 9",
            font=("Segoe UI", 9, "bold"),
            bg=self.COLOR_BG,
            fg="#d63031",
            anchor="w"
        )
        self.lbl_sat_info.pack(fill=tk.X)

        self.lbl_colors_info = tk.Label(
            group,
            text="Miền màu khả dụng (MRV): -",
            font=("Segoe UI", 9),
            bg=self.COLOR_BG,
            fg="#009432",
            anchor="w"
        )
        self.lbl_colors_info.pack(fill=tk.X)

        self.lbl_status_info = tk.Label(
            group,
            text="Trạng thái: -",
            font=("Segoe UI", 9),
            bg=self.COLOR_BG,
            fg="#2f3640",
            anchor="w"
        )
        self.lbl_status_info.pack(fill=tk.X)

        # Cảnh báo xung đột thời gian thực (Game Validator)
        self.lbl_conflict_warn = tk.Label(
            group,
            text="Không có xung đột màu trên 20 đỉnh kề.",
            font=("Segoe UI", 9, "italic"),
            bg=self.COLOR_BG,
            fg="#009432",
            anchor="w",
            wraplength=420,
            justify=tk.LEFT
        )
        self.lbl_conflict_warn.pack(fill=tk.X, pady=(4, 0))

    def _setup_step_solver_panel(self, parent: tk.Widget) -> None:
        """Khung 2: Bảng trực quan hóa giải từng bước (Step-by-step DSATUR)."""
        group = tk.LabelFrame(
            parent,
            text=" 2. TRỰC QUAN HÓA TÔ MÀU (STEP-BY-STEP DSATUR) ",
            font=("Segoe UI", 10, "bold"),
            bg=self.COLOR_BG,
            fg="#6c5ce7",
            padx=10,
            pady=8
        )
        group.pack(fill=tk.X, pady=(0, 8))

        # Thanh trượt chỉnh tốc độ trễ (Delay Slider)
        speed_frame = tk.Frame(group, bg=self.COLOR_BG)
        speed_frame.pack(fill=tk.X, pady=(0, 6))

        tk.Label(
            speed_frame,
            text="Tốc độ trễ:",
            font=("Segoe UI", 9),
            bg=self.COLOR_BG
        ).pack(side=tk.LEFT)

        self.speed_slider = tk.Scale(
            speed_frame,
            from_=10,
            to=500,
            orient=tk.HORIZONTAL,
            bg=self.COLOR_BG,
            highlightthickness=0,
            length=180
        )
        self.speed_slider.set(80)  # Mặc định 80ms
        self.speed_slider.pack(side=tk.LEFT, padx=8)

        tk.Label(
            speed_frame,
            text="(ms/bước)",
            font=("Segoe UI", 8, "italic"),
            bg=self.COLOR_BG,
            fg="#636e72"
        ).pack(side=tk.LEFT)

        # Hàng nút điều khiển bước
        btn_step_frame = tk.Frame(group, bg=self.COLOR_BG)
        btn_step_frame.pack(fill=tk.X, pady=(0, 6))

        self.btn_auto = tk.Button(
            btn_step_frame,
            text="▶ Chạy tự động",
            font=("Segoe UI", 9, "bold"),
            bg="#0984e3",
            fg="white",
            relief=tk.FLAT,
            padx=10,
            pady=4,
            command=self.toggle_auto_solve
        )
        self.btn_auto.pack(side=tk.LEFT, padx=(0, 6))

        self.btn_next = tk.Button(
            btn_step_frame,
            text="⏭ Bước tiếp",
            font=("Segoe UI", 9),
            bg="#dfe6e9",
            fg="#2d3436",
            relief=tk.FLAT,
            padx=10,
            pady=4,
            command=self.step_forward
        )
        self.btn_next.pack(side=tk.LEFT, padx=(0, 6))

        self.btn_instant = tk.Button(
            btn_step_frame,
            text="⚡ Giải nhanh",
            font=("Segoe UI", 9),
            bg="#dfe6e9",
            fg="#2d3436",
            relief=tk.FLAT,
            padx=8,
            pady=4,
            command=self.solve_instantly
        )
        self.btn_instant.pack(side=tk.LEFT)

        # Thống kê số bước và số lần quay lui
        stats_frame = tk.Frame(group, bg=self.COLOR_BG)
        stats_frame.pack(fill=tk.X)

        self.lbl_stats = tk.Label(
            stats_frame,
            text="Số bước gán màu: 0  |  Số lần quay lui (Backtracks): 0",
            font=("Segoe UI", 9),
            bg=self.COLOR_BG,
            fg="#2d3436",
            anchor="w"
        )
        self.lbl_stats.pack(side=tk.LEFT)

    def _setup_control_panel(self, parent: tk.Widget) -> None:
        """Khung 3: Bảng điều khiển nạp đề, gợi ý và kiểm tra tính hợp lệ."""
        group = tk.LabelFrame(
            parent,
            text=" 3. BẢNG ĐIỀU KHIỂN & CHỨC NĂNG ",
            font=("Segoe UI", 10, "bold"),
            bg=self.COLOR_BG,
            fg="#2d3436",
            padx=10,
            pady=8
        )
        group.pack(fill=tk.BOTH, expand=True)

        # Hàng chọn đề mẫu 4 cấp độ
        sample_frame = tk.Frame(group, bg=self.COLOR_BG)
        sample_frame.pack(fill=tk.X, pady=(0, 6))

        tk.Label(
            sample_frame,
            text="Đề mẫu:",
            font=("Segoe UI", 9, "bold"),
            bg=self.COLOR_BG
        ).pack(side=tk.LEFT, padx=(0, 6))

        for level, filename in [
            ("Dễ", "sample_easy.txt"),
            ("Trung bình", "sample_medium.txt"),
            ("Khó", "sample_hard.txt"),
            ("Chuyên gia", "sample_expert.txt"),
        ]:
            btn = tk.Button(
                sample_frame,
                text=level,
                font=("Segoe UI", 8),
                bg="#f1f2f6",
                relief=tk.GROOVE,
                padx=6,
                pady=2,
                command=lambda f=filename: self.load_sample_puzzle(f)
            )
            btn.pack(side=tk.LEFT, padx=2)

        # Hàng nút công cụ nâng cao
        tools_frame = tk.Frame(group, bg=self.COLOR_BG)
        tools_frame.pack(fill=tk.X, pady=(0, 6))

        btn_open = tk.Button(
            tools_frame,
            text="📂 Mở file .txt",
            font=("Segoe UI", 9),
            bg="#f1f2f6",
            relief=tk.GROOVE,
            padx=8,
            pady=3,
            command=self.open_file_dialog
        )
        btn_open.pack(side=tk.LEFT, padx=(0, 4))

        btn_hint = tk.Button(
            tools_frame,
            text="💡 Gợi ý (Hint)",
            font=("Segoe UI", 9, "bold"),
            bg="#55efc4",
            fg="#2d3436",
            relief=tk.FLAT,
            padx=8,
            pady=3,
            command=self.trigger_hint
        )
        btn_hint.pack(side=tk.LEFT, padx=(0, 4))

        btn_check = tk.Button(
            tools_frame,
            text="🔍 Kiểm tra khả giải",
            font=("Segoe UI", 9),
            bg="#f1f2f6",
            relief=tk.GROOVE,
            padx=8,
            pady=3,
            command=self.check_solvability
        )
        btn_check.pack(side=tk.LEFT, padx=(0, 4))

        btn_reset = tk.Button(
            tools_frame,
            text="↺ Đặt lại",
            font=("Segoe UI", 9),
            bg="#f1f2f6",
            relief=tk.GROOVE,
            padx=8,
            pady=3,
            command=self.reset_puzzle
        )
        btn_reset.pack(side=tk.LEFT, padx=(0, 4))

        btn_clear = tk.Button(
            tools_frame,
            text="🗑 Xóa trắng",
            font=("Segoe UI", 9),
            bg="#ffeaa7",
            relief=tk.GROOVE,
            padx=8,
            pady=3,
            command=self.clear_board
        )
        btn_clear.pack(side=tk.LEFT)

        # Hộp thông báo nhật ký hoạt động
        self.txt_log = tk.Text(
            group,
            height=6,
            font=("Consolas", 8),
            bg="#ffffff",
            fg="#2f3640",
            relief=tk.SUNKEN,
            wrap=tk.WORD
        )
        self.txt_log.pack(fill=tk.BOTH, expand=True, pady=(6, 0))
        self.log_message("Chào mừng! Hệ thống đồ thị Sudoku đã nạp thành công 81 đỉnh, 810 cạnh.")

    # =========================================================================
    # SỰ KIỆN CHUỘT VÀ BÀN PHÍM (EVENT BINDINGS)
    # =========================================================================

    def _bind_events(self) -> None:
        """Gắn các sự kiện click chuột và phím bấm trên bàn cờ."""
        self.canvas.bind("<Button-1>", self._on_canvas_click)
        self.root.bind("<Key>", self._on_key_press)

    def _on_canvas_click(self, event: tk.Event) -> None:
        """Xử lý khi người dùng click chuột vào một ô trên bàn cờ."""
        x = event.x - self.BOARD_PADDING
        y = event.y - self.BOARD_PADDING

        if 0 <= x < self.CELL_SIZE * 9 and 0 <= y < self.CELL_SIZE * 9:
            col = x // self.CELL_SIZE
            row = y // self.CELL_SIZE
            vertex = SudokuGraph.coords_to_index(row, col)
            self.select_vertex(vertex)

    def _on_key_press(self, event: tk.Event) -> None:
        """Xử lý nhập số từ bàn phím hoặc phím điều hướng."""
        if self.selected_vertex is None:
            return

        v = self.selected_vertex
        r, c = SudokuGraph.index_to_coords(v)

        # Điều hướng bằng 4 phím mũi tên
        if event.keysym == "Up" and r > 0:
            self.select_vertex(SudokuGraph.coords_to_index(r - 1, c))
            return
        elif event.keysym == "Down" and r < 8:
            self.select_vertex(SudokuGraph.coords_to_index(r + 1, c))
            return
        elif event.keysym == "Left" and c > 0:
            self.select_vertex(SudokuGraph.coords_to_index(r, c - 1))
            return
        elif event.keysym == "Right" and c < 8:
            self.select_vertex(SudokuGraph.coords_to_index(r, c + 1))
            return

        # Không cho phép sửa ô tiền tô màu của đề bài
        if self.graph.is_precolored[v]:
            return

        # Nhập số từ 1 đến 9
        if event.char in "123456789":
            val = int(event.char)
            self.graph.colors[v] = val
            self.hint_vertex = None  # Xóa highlight gợi ý nếu người chơi đã đi
            self.render_board()
            self.update_inspector()

            # Kiểm tra xung đột thời gian thực trên 20 đỉnh kề
            conflicts = self.graph.find_conflicts(v)
            if conflicts:
                self.log_message(f"CẢNH BÁO: {conflicts[0]['message']}")
            else:
                self.log_message(f"Ô ({r+1}, {c+1}) [đỉnh {v}]: Gán màu {val} thành công.")

            # Kiểm tra nếu đã hoàn thành toàn bộ bàn cờ
            if self.graph.is_complete():
                messagebox.showinfo(
                    "CHÚC MỪNG!",
                    "Bàn cờ Sudoku đã được giải hoàn toàn chính xác theo luật tô màu đồ thị!"
                )
                self.log_message("XUẤT SẮC: Toàn bộ 81 đỉnh đã tô màu hợp lệ (không xung đột)!")

        # Xóa số bằng phím 0, Backspace hoặc Delete
        elif event.keysym in ("BackSpace", "Delete") or event.char == "0":
            self.graph.colors[v] = 0
            self.render_board()
            self.update_inspector()
            self.log_message(f"Ô ({r+1}, {c+1}) [đỉnh {v}]: Đã xóa màu (chưa tô).")

    def select_vertex(self, vertex: int) -> None:
        """Chọn một đỉnh v trên bàn cờ và cập nhật thông số kề."""
        self.selected_vertex = vertex
        self.render_board()
        self.update_inspector()

    # =========================================================================
    # VẼ BÀN CỜ 9X9 VÀ HIGHLIGHT ĐỒ THỊ (RENDER ENGINE)
    # =========================================================================

    def render_board(self) -> None:
        """
        Vẽ lại toàn bộ 81 ô bàn cờ trên Canvas:
        - Highlight ô được chọn.
        - Highlight 20 đỉnh kề N(v) của ô đang chọn (Tính năng trọng tâm của đồ án).
        - Tô màu cảnh báo các ô xung đột (Game Validator).
        - Hiển thị số với kiểu chữ phân biệt (tiền tô màu / người dùng điền).
        - Vẽ các đường kẻ lưới 3x3 đậm nhạt chuẩn mực.
        """
        self.canvas.delete("all")

        # Xác định tập 20 đỉnh kề nếu có ô đang chọn
        neighbors_set: Set[int] = set()
        if self.selected_vertex is not None:
            neighbors_set = set(self.graph.get_neighbors(self.selected_vertex))

        # Tìm tất cả đỉnh đang bị xung đột màu
        conflicts = self.graph.get_all_conflicts()
        conflict_vertices = set()
        for c in conflicts:
            conflict_vertices.add(c["u"])
            conflict_vertices.add(c["v"])

        pad = self.BOARD_PADDING
        sz = self.CELL_SIZE

        # 1. Vẽ nền của 81 ô
        for r in range(9):
            for c in range(9):
                v = SudokuGraph.coords_to_index(r, c)
                x1 = pad + c * sz
                y1 = pad + r * sz
                x2 = x1 + sz
                y2 = y1 + sz

                # Xác định màu nền ô theo thứ tự ưu tiên
                bg_color = self.COLOR_CELL_DEFAULT
                if v == self.selected_vertex:
                    bg_color = self.COLOR_CELL_SELECTED
                elif v == self.active_step_vertex:
                    bg_color = self.COLOR_CELL_ACTIVE
                elif v == self.hint_vertex:
                    bg_color = self.COLOR_CELL_HINT
                elif v in conflict_vertices:
                    bg_color = self.COLOR_CELL_CONFLICT
                elif v in neighbors_set:
                    bg_color = self.COLOR_CELL_NEIGHBOR

                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=bg_color,
                    outline="",
                    tags=f"cell_{v}"
                )

                # Vẽ giá trị số (màu đỉnh)
                val = self.graph.colors[v]
                if val != 0:
                    # Kiểu dáng chữ phân biệt
                    if v in conflict_vertices:
                        text_color = self.COLOR_TEXT_CONFLICT
                        font_spec = ("Segoe UI", 16, "bold")
                    elif self.graph.is_precolored[v]:
                        text_color = self.COLOR_TEXT_PRECOLORED
                        font_spec = ("Segoe UI", 16, "bold")
                    else:
                        text_color = self.COLOR_TEXT_USER
                        font_spec = ("Segoe UI", 16)

                    self.canvas.create_text(
                        (x1 + x2) // 2,
                        (y1 + y2) // 2,
                        text=str(val),
                        font=font_spec,
                        fill=text_color
                    )

        # 2. Vẽ đường kẻ lưới bàn cờ (đường mảnh cho ô, đường dày cho khối 3x3)
        for i in range(10):
            # Tọa độ đường ngang và dọc
            coord = pad + i * sz
            is_block_line = (i % 3 == 0)
            line_w = 3 if is_block_line else 1
            line_c = self.COLOR_LINE_THICK if is_block_line else self.COLOR_LINE_THIN

            # Đường kẻ ngang
            self.canvas.create_line(
                pad, coord, pad + 9 * sz, coord,
                fill=line_c, width=line_w
            )
            # Đường kẻ dọc
            self.canvas.create_line(
                coord, pad, coord, pad + 9 * sz,
                fill=line_c, width=line_w
            )

    # =========================================================================
    # THANH TRA ĐỒ THỊ & THÔNG BÁO (GRAPH INSPECTOR)
    # =========================================================================

    def update_inspector(self) -> None:
        """Cập nhật các chỉ số lý thuyết đồ thị lên bảng Thanh tra bên phải."""
        if self.selected_vertex is None:
            self.lbl_vertex_info.config(text="Đỉnh v: Chưa chọn ô nào trên bàn cờ")
            self.lbl_sat_info.config(text="Bậc bão hòa (DSATUR): - / 9")
            self.lbl_colors_info.config(text="Miền màu khả dụng (MRV): -")
            self.lbl_status_info.config(text="Trạng thái: -")
            self.lbl_conflict_warn.config(
                text="Hãy click chọn 1 ô để quan sát 20 đỉnh kề N(v) và bậc bão hòa.",
                fg="#636e72"
            )
            return

        v = self.selected_vertex
        r, c = SudokuGraph.index_to_coords(v)
        b = SudokuGraph.get_box_index(r, c)
        val = self.graph.colors[v]
        sat = self.graph.get_saturation_degree(v)
        avail = sorted(list(self.graph.get_available_colors(v)))

        # 1. Tọa độ và chỉ số đỉnh
        self.lbl_vertex_info.config(
            text=f"Đỉnh v = {v} (Hàng {r + 1}, Cột {c + 1}, Khối 3x3 số {b + 1})"
        )

        # 2. Bậc bão hòa DSATUR
        self.lbl_sat_info.config(
            text=f"Bậc bão hòa (DSATUR): {sat} / 9 (đã có {sat} màu khác nhau ở 20 đỉnh kề)"
        )

        # 3. Miền màu khả dụng MRV
        if val != 0:
            self.lbl_colors_info.config(text=f"Miền màu khả dụng (MRV): Ô đã mang màu {val}")
        else:
            avail_str = ", ".join(map(str, avail)) if avail else "Không có màu nào (Bế tắc!)"
            self.lbl_colors_info.config(
                text=f"Miền màu khả dụng (MRV): {len(avail)} màu [{avail_str}]"
            )

        # 4. Trạng thái đỉnh
        if self.graph.is_precolored[v]:
            status_text = f"Trạng thái: Ô tiền tô màu cố định của đề bài (Màu {val})"
        elif val != 0:
            status_text = f"Trạng thái: Ô do người chơi/thuật toán điền (Màu {val})"
        else:
            status_text = "Trạng thái: Ô trống chưa tô màu (Màu 0)"
        self.lbl_status_info.config(text=status_text)

        # 5. Kiểm tra xung đột thời gian thực trên 20 đỉnh kề
        conflicts = self.graph.find_conflicts(v)
        if conflicts:
            msg = f"⚠ XUNG ĐỘT: {conflicts[0]['message']}!"
            self.lbl_conflict_warn.config(text=msg, fg="#d63031")
        else:
            if val != 0:
                self.lbl_conflict_warn.config(
                    text="✓ Hợp lệ: Màu không trùng với bất kỳ đỉnh kề nào trong 20 đỉnh kề.",
                    fg="#009432"
                )
            else:
                self.lbl_conflict_warn.config(
                    text="Quan sát nền xanh nhạt trên bàn cờ: đó là đúng 20 đỉnh kề N(v) của ô này.",
                    fg="#0984e3"
                )

    def log_message(self, msg: str) -> None:
        """Ghi dòng nhật ký mới vào hộp Text log."""
        self.txt_log.insert(tk.END, f"• {msg}\n")
        self.txt_log.see(tk.END)

    # =========================================================================
    # THUẬT TOÁN GIẢI TỪNG BƯỚC (STEP-BY-STEP GENERATOR ENGINE)
    # =========================================================================

    def _create_solve_generator(self):
        """
        Tạo generator giải Sudoku bằng Backtracking kết hợp Heuristic DSATUR & MRV.
        Mỗi bước giải yield một hành động ('select', 'assign', 'backtrack', 'done')
        để giao diện Tkinter cập nhật đồ họa từng bước mà không làm đơ màn hình.
        """
        graph = self.graph

        def backtrack():
            uncolored = graph.get_uncolored_vertices()
            if not uncolored:
                yield ("done", None, None, "Đã hoàn thành toàn bộ bàn cờ!")
                return True

            # Chọn đỉnh theo Heuristic DSATUR: Bậc bão hòa cao nhất, miền màu hẹp nhất (MRV)
            candidates = []
            for v in uncolored:
                avail = sorted(list(graph.get_available_colors(v)))
                sat = graph.get_saturation_degree(v)
                candidates.append((v, sat, len(avail), avail))

            # Sắp xếp ưu tiên: ít màu khả dụng nhất (MRV nhỏ), bậc bão hòa lớn nhất
            best_v, best_sat, num_avail, avail_colors = min(
                candidates, key=lambda x: (x[2], -x[1])
            )

            # Bế tắc: không còn màu nào hợp lệ cho đỉnh này -> cần quay lui
            if num_avail == 0:
                return False

            r, c = SudokuGraph.index_to_coords(best_v)

            # Thử từng màu hợp lệ trong miền giá trị
            for color in avail_colors:
                graph.colors[best_v] = color
                yield ("assign", best_v, color, f"Gán màu {color} vào ô ({r+1}, {c+1}) [sat_deg={best_sat}]")

                sub_gen = backtrack()
                for step in sub_gen:
                    yield step
                    if step[0] == "done":
                        return True

                # Quay lui khi nhánh thử nghiệm thất bại
                graph.colors[best_v] = 0
                yield ("backtrack", best_v, color, f"Quay lui tại ô ({r+1}, {c+1}) [hủy màu {color}]")

            return False

        return backtrack()

    def step_forward(self) -> bool:
        """Thực hiện đúng 1 bước tiếp theo của thuật toán giải."""
        if self.step_generator is None:
            # Nếu đang có xung đột màu do người chơi điền sai, không thể giải
            if self.graph.get_all_conflicts():
                messagebox.showerror(
                    "Lỗi bàn cờ",
                    "Bàn cờ hiện tại đang có ô bị xung đột màu! Vui lòng xóa ô sai trước khi giải."
                )
                return False
            self.step_generator = self._create_solve_generator()
            self.stats_steps = 0
            self.stats_backtracks = 0

        try:
            action, v, val, desc = next(self.step_generator)
            self.stats_steps += 1

            if action == "assign":
                self.active_step_vertex = v
                self.select_vertex(v)
                self.log_message(desc)
            elif action == "backtrack":
                self.stats_backtracks += 1
                self.active_step_vertex = v
                self.select_vertex(v)
                self.log_message(desc)
            elif action == "done":
                self.active_step_vertex = None
                self.render_board()
                self.update_inspector()
                self.log_message(f"THÀNH CÔNG: {desc}")
                messagebox.showinfo("Hoàn tất", f"Đã giải thành công!\nSố bước duyệt: {self.stats_steps}\nSố lần quay lui: {self.stats_backtracks}")
                self.step_generator = None
                self.is_auto_running = False
                self.btn_auto.config(text="▶ Chạy tự động", bg="#0984e3")
                return False

            # Cập nhật thống kê
            self.lbl_stats.config(
                text=f"Số bước gán màu: {self.stats_steps}  |  Số lần quay lui (Backtracks): {self.stats_backtracks}"
            )
            self.render_board()
            self.update_inspector()
            return True

        except StopIteration:
            self.step_generator = None
            self.active_step_vertex = None
            self.render_board()
            self.log_message("Thuật toán kết thúc: Không tìm thấy thêm lời giải.")
            return False

    def toggle_auto_solve(self) -> None:
        """Bật/Tắt chế độ tự động giải từng bước có hoạt họa trễ (Animation loop)."""
        if self.is_auto_running:
            # Tạm dừng
            self.is_auto_running = False
            self.btn_auto.config(text="▶ Tiếp tục", bg="#0984e3")
            self.log_message("Đã tạm dừng quá trình giải.")
        else:
            # Bắt đầu chạy
            self.is_auto_running = True
            self.btn_auto.config(text="⏸ Tạm dừng", bg="#e17055")
            self.log_message("Bắt đầu tự động giải từng bước (Step-by-step)...")
            self._run_auto_step()

    def _run_auto_step(self) -> None:
        """Vòng lặp phi nghẽn (Non-blocking) sử dụng root.after để cập nhật GUI liên tục."""
        if not self.is_auto_running:
            return

        has_more = self.step_forward()
        if has_more and self.is_auto_running:
            delay_ms = self.speed_slider.get()
            self.root.after(delay_ms, self._run_auto_step)

    def solve_instantly(self) -> None:
        """Giải ngay lập tức mà không chờ hoạt họa (cho người dùng muốn kết quả tức thì)."""
        # Tạm dừng chạy tự động nếu đang chạy
        self.is_auto_running = False
        self.btn_auto.config(text="▶ Chạy tự động", bg="#0984e3")

        if self.graph.get_all_conflicts():
            messagebox.showerror("Lỗi", "Bàn cờ có xung đột màu! Vui lòng xóa ô vi phạm trước.")
            return

        # Khởi tạo generator mới và chạy đến hết
        gen = self._create_solve_generator()
        steps = 0
        backtracks = 0
        success = False

        for action, v, val, desc in gen:
            steps += 1
            if action == "backtrack":
                backtracks += 1
            elif action == "done":
                success = True
                break

        self.step_generator = None
        self.active_step_vertex = None
        self.render_board()
        self.update_inspector()

        if success:
            self.lbl_stats.config(
                text=f"Số bước gán màu: {steps}  |  Số lần quay lui (Backtracks): {backtracks}"
            )
            self.log_message(f"Giải hoàn tất trong {steps} bước duyệt ({backtracks} lần quay lui).")
            messagebox.showinfo("Thành công", f"Đã giải thành công trong {steps} bước!\nSố lần quay lui: {backtracks}")
        else:
            messagebox.showwarning("Bế tắc", "Không tìm thấy lời giải hợp lệ cho bàn cờ này.")

    # =========================================================================
    # CÁC CHỨC NĂNG HỖ TRỢ ĐỒ ÁN (HINT, SOLVABILITY, LOAD PUZZLES)
    # =========================================================================

    def trigger_hint(self) -> None:
        """Chức năng Gợi ý nước đi tiếp theo (Hint Engine theo DSATUR & MRV)."""
        hint = self.graph.get_hint()
        if not hint:
            messagebox.showinfo("Gợi ý", "Bàn cờ đã được điền kín hoặc không còn ô trống!")
            return

        v = hint["vertex"]
        self.hint_vertex = v
        self.select_vertex(v)

        reason = hint["reason"]
        suggested = hint.get("suggested_color")
        self.log_message(f"GỢI Ý ĐỒ THỊ: {reason}")
        messagebox.showinfo(
            "Gợi ý từ DSATUR Hint Engine",
            f"Vị trí gợi ý: Hàng {hint['row'] + 1}, Cột {hint['col'] + 1} (Đỉnh {v})\n"
            f"Màu đề xuất: {suggested}\n\n"
            f"Giải thích logic đồ thị:\n{reason}"
        )

    def check_solvability(self) -> None:
        """Chức năng Kiểm tra tính khả giải và số nghiệm (Solvability Checker)."""
        sol_info = self.graph.check_solvability()
        msg = (
            f"Trạng thái: {sol_info['status']}\n"
            f"Số lượng nghiệm: {sol_info['solutions_count']}\n\n"
            f"{sol_info['message']}"
        )
        self.log_message(f"SOLVABILITY CHECKER: {sol_info['status']} ({sol_info['solutions_count']} nghiệm)")
        messagebox.showinfo("Kiểm tra khả giải", msg)

    def _load_default_sample(self) -> None:
        """Nạp đề mẫu dễ mặc định từ file hoặc chuỗi dự phòng."""
        sample_path = os.path.join(PROJECT_ROOT, "Release", "puzzles", "sample_easy.txt")
        if os.path.exists(sample_path):
            try:
                self.graph = IOHandler.read_puzzle_from_file(sample_path)
                return
            except Exception:
                pass
        # Chuỗi đề dự phòng nếu không tìm thấy file
        backup_str = (
            "530070000600195000098000060800060003400803001700020006060000280000419005000080079"
        )
        self.graph.load_from_string(backup_str)

    def load_sample_puzzle(self, filename: str) -> None:
        """Nạp một bộ đề mẫu trong thư mục Release/puzzles/."""
        self._stop_simulation()
        puzzle_path = os.path.join(PROJECT_ROOT, "Release", "puzzles", filename)
        if not os.path.exists(puzzle_path):
            messagebox.showerror("Lỗi", f"Không tìm thấy file đề mẫu: {puzzle_path}")
            return

        try:
            self.graph = IOHandler.read_puzzle_from_file(puzzle_path)
            self.selected_vertex = None
            self.hint_vertex = None
            self.render_board()
            self.update_inspector()
            self.log_message(f"Đã nạp thành công bộ đề: {filename}")
        except Exception as e:
            messagebox.showerror("Lỗi nạp đề", f"Không thể nạp đề bài: {e}")

    def open_file_dialog(self) -> None:
        """Mở hộp thoại chọn file .txt bất kỳ trên máy."""
        self._stop_simulation()
        initial_dir = os.path.join(PROJECT_ROOT, "Release", "puzzles")
        file_path = filedialog.askopenfilename(
            initialdir=initial_dir if os.path.exists(initial_dir) else PROJECT_ROOT,
            title="Chọn tập tin đề bài Sudoku (.txt)",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if not file_path:
            return

        try:
            self.graph = IOHandler.read_puzzle_from_file(file_path)
            self.selected_vertex = None
            self.hint_vertex = None
            self.render_board()
            self.update_inspector()
            self.log_message(f"Đã nạp file đề: {os.path.basename(file_path)}")
        except Exception as e:
            messagebox.showerror("Lỗi đọc file", f"Không thể đọc file: {e}")

    def reset_puzzle(self) -> None:
        """Đặt lại bàn cờ về trạng thái đề bài ban đầu (chỉ giữ ô tiền tô màu)."""
        self._stop_simulation()
        self.graph.reset_to_precolored()
        self.hint_vertex = None
        self.render_board()
        self.update_inspector()
        self.log_message("Đã đặt lại bàn cờ về trạng thái đề bài ban đầu.")

    def clear_board(self) -> None:
        """Xóa trắng toàn bộ bàn cờ để người dùng tự nhập đề mới."""
        self._stop_simulation()
        self.graph.clear()
        self.selected_vertex = None
        self.hint_vertex = None
        self.render_board()
        self.update_inspector()
        self.log_message("Đã xóa trắng bàn cờ. Bạn có thể tự do nhập đề bài mới.")

    def _stop_simulation(self) -> None:
        """Dừng hoàn toàn tiến trình mô phỏng đang chạy."""
        self.is_auto_running = False
        self.step_generator = None
        self.active_step_vertex = None
        self.btn_auto.config(text="▶ Chạy tự động", bg="#0984e3")
        self.lbl_stats.config(text="Số bước gán màu: 0  |  Số lần quay lui (Backtracks): 0")


def main():
    """Khởi chạy ứng dụng GUI."""
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
