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
import json
import datetime
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
from typing import Optional, Set, List, Tuple

# Thêm đường dẫn gốc để import các mô-đun trong Source.core
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(CURRENT_DIR))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from Source.core.sudoku_graph import SudokuGraph, PrecoloringConflictError
from Source.core.io_handler import IOHandler
from Source.core.puzzle_generator import PuzzleGenerator


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

        # Kho 40 bản đồ mẫu theo 4 cấp độ (10 bản đồ mỗi cấp)
        self.curated_puzzles = self._load_curated_40_puzzles()

        # Nạp đề mẫu ban đầu
        self._load_default_sample()

        # Dựng các thành phần giao diện
        self._setup_ui()
        self._on_level_changed()

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

        # Hàng 1: Sinh đề tự động theo 4 cấp độ (Game Generator - Chức năng thực tế 1)
        gen_frame = tk.Frame(group, bg=self.COLOR_BG)
        gen_frame.pack(fill=tk.X, pady=(0, 6))

        tk.Label(
            gen_frame,
            text="🎲 Sinh đề mới:",
            font=("Segoe UI", 9, "bold"),
            bg=self.COLOR_BG,
            fg="#0984e3"
        ).pack(side=tk.LEFT, padx=(0, 6))

        for level_code, level_name, bg_color in [
            ("easy", "Dễ", "#dff9fb"),
            ("medium", "Trung bình", "#c7ecee"),
            ("hard", "Khó", "#ffeaa7"),
            ("expert", "Chuyên gia", "#ffcccc"),
        ]:
            btn = tk.Button(
                gen_frame,
                text=level_name,
                font=("Segoe UI", 8, "bold"),
                bg=bg_color,
                relief=tk.GROOVE,
                padx=6,
                pady=2,
                command=lambda d=level_code: self.generate_puzzle(d)
            )
            btn.pack(side=tk.LEFT, padx=2)

        # Hàng 2: Kho 40 bản đồ mẫu theo 4 cấp độ (10 bản đồ mỗi cấp độ)
        sample_frame = tk.Frame(group, bg=self.COLOR_BG)
        sample_frame.pack(fill=tk.X, pady=(0, 6))

        tk.Label(
            sample_frame,
            text="📚 Bản đồ:",
            font=("Segoe UI", 9, "bold"),
            bg=self.COLOR_BG,
            fg="#2d3436"
        ).pack(side=tk.LEFT, padx=(0, 4))

        # Combobox chọn Cấp độ
        self.cbo_level = ttk.Combobox(
            sample_frame,
            values=["Dễ (10 đề)", "Trung bình (10 đề)", "Khó (10 đề)", "Chuyên gia (10 đề)"],
            state="readonly",
            width=14,
            font=("Segoe UI", 8)
        )
        self.cbo_level.current(0)
        self.cbo_level.pack(side=tk.LEFT, padx=1)
        self.cbo_level.bind("<<ComboboxSelected>>", self._on_level_changed)

        # Combobox chọn Bản đồ (1..10)
        self.cbo_board = ttk.Combobox(
            sample_frame,
            values=[f"Bản đồ #{i+1}" for i in range(10)],
            state="readonly",
            width=12,
            font=("Segoe UI", 8)
        )
        self.cbo_board.current(0)
        self.cbo_board.pack(side=tk.LEFT, padx=1)

        # Nút nạp bản đồ
        btn_load_board = tk.Button(
            sample_frame,
            text="▶ Nạp",
            font=("Segoe UI", 8, "bold"),
            bg="#0984e3",
            fg="white",
            relief=tk.FLAT,
            padx=5,
            pady=1,
            command=self.load_selected_curated_puzzle
        )
        btn_load_board.pack(side=tk.LEFT, padx=1)

        # Nút Đề trước / Đề sau
        btn_prev = tk.Button(
            sample_frame,
            text="◀",
            font=("Segoe UI", 8),
            bg="#f1f2f6",
            relief=tk.GROOVE,
            padx=3,
            pady=1,
            command=lambda: self.navigate_curated_puzzle(-1)
        )
        btn_prev.pack(side=tk.LEFT, padx=1)

        btn_next = tk.Button(
            sample_frame,
            text="▶",
            font=("Segoe UI", 8),
            bg="#f1f2f6",
            relief=tk.GROOVE,
            padx=3,
            pady=1,
            command=lambda: self.navigate_curated_puzzle(1)
        )
        btn_next.pack(side=tk.LEFT, padx=1)

        # Nút mở thư viện 40 bản đồ
        btn_all_boards = tk.Button(
            sample_frame,
            text="Kho 40 đề",
            font=("Segoe UI", 8),
            bg="#dfe6e9",
            relief=tk.GROOVE,
            padx=4,
            pady=1,
            command=self.open_all_curated_puzzles_dialog
        )
        btn_all_boards.pack(side=tk.LEFT, padx=2)

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

        # Hàng nút Bàn cờ tự tạo & Bàn cờ đã lưu
        custom_frame = tk.Frame(group, bg=self.COLOR_BG)
        custom_frame.pack(fill=tk.X, pady=(0, 6))

        tk.Label(
            custom_frame,
            text="✍️ Tự tạo đề:",
            font=("Segoe UI", 9, "bold"),
            bg=self.COLOR_BG,
            fg="#0984e3"
        ).pack(side=tk.LEFT, padx=(0, 4))

        btn_new_blank = tk.Button(
            custom_frame,
            text="📝 Nhập bàn cờ trống",
            font=("Segoe UI", 8, "bold"),
            bg="#dff9fb",
            relief=tk.GROOVE,
            padx=5,
            pady=2,
            command=self.clear_board
        )
        btn_new_blank.pack(side=tk.LEFT, padx=2)

        btn_lock_puzzle = tk.Button(
            custom_frame,
            text="🔒 Khóa làm đề",
            font=("Segoe UI", 8),
            bg="#f1f2f6",
            relief=tk.GROOVE,
            padx=5,
            pady=2,
            command=self.lock_as_puzzle
        )
        btn_lock_puzzle.pack(side=tk.LEFT, padx=2)

        btn_save_puzzle = tk.Button(
            custom_frame,
            text="💾 Lưu bàn cờ",
            font=("Segoe UI", 8, "bold"),
            bg="#55efc4",
            fg="#2d3436",
            relief=tk.FLAT,
            padx=6,
            pady=2,
            command=self.save_custom_board
        )
        btn_save_puzzle.pack(side=tk.LEFT, padx=2)

        btn_saved_list = tk.Button(
            custom_frame,
            text="📁 Bàn cờ đã lưu",
            font=("Segoe UI", 8, "bold"),
            bg="#6c5ce7",
            fg="white",
            relief=tk.FLAT,
            padx=7,
            pady=2,
            command=self.open_saved_puzzles_dialog
        )
        btn_saved_list.pack(side=tk.LEFT, padx=2)

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

    def generate_puzzle(self, difficulty: str) -> None:
        """
        Chức năng Tạo trò chơi tự động (Game Generator):
        Sinh đề Sudoku ngẫu nhiên theo nguyên lý đối xứng tâm 180 độ
        và cam kết đúng duy nhất 1 nghiệm (Unique Solution).
        """
        self._stop_simulation()
        diff_names = {
            "easy": "DỄ (36-40 clues)",
            "medium": "TRUNG BÌNH (32-35 clues)",
            "hard": "KHÓ (26-31 clues)",
            "expert": "CHUYÊN GIA (22-25 clues)"
        }
        name = diff_names.get(difficulty, difficulty.upper())
        self.log_message(f"GAME GENERATOR: Đang khởi tạo ngẫu nhiên đề bài {name}...")

        try:
            self.graph = PuzzleGenerator.generate(difficulty=difficulty)
            self.selected_vertex = None
            self.active_step_vertex = None
            self.hint_vertex = None

            clues_count = sum(1 for c in self.graph.colors if c != 0)
            self.render_board()
            self.update_inspector()
            self.lbl_status_info.config(
                text=f"Trạng thái: Đã sinh đề mới ({name}) | Số clues: {clues_count}",
                fg="#0984e3"
            )
            self.log_message(
                f"TẠO ĐỀ THÀNH CÔNG: Cấp độ {name} gồm {clues_count} clues đối xứng tâm, nghiệm duy nhất!"
            )
            messagebox.showinfo(
                "Tạo đề Sudoku thành công",
                f"Đã sinh thành công đề bài cấp độ {name}!\n"
                f"- Số lượng clues ban đầu: {clues_count}\n"
                f"- Quy cách: Đối xứng tâm 180 độ\n"
                f"- Tính khả giải: Cam kết đúng 1 nghiệm duy nhất."
            )
        except Exception as e:
            messagebox.showerror("Lỗi sinh đề", f"Không thể sinh đề bài: {e}")

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

    def _load_curated_40_puzzles(self) -> dict:
        """Nạp danh sách 40 bản đồ mẫu theo 4 cấp độ (10 bản đồ mỗi cấp)."""
        json_path = os.path.join(PROJECT_ROOT, "Release", "puzzles", "curated_40_puzzles.json")
        if os.path.exists(json_path):
            try:
                with open(json_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"Lỗi đọc curated_40_puzzles.json: {e}")

        # Dự phòng đọc từ 4 file easy_10.txt, medium_10.txt, ...
        data = {"easy": [], "medium": [], "hard": [], "expert": []}
        files = {
            "easy": "easy_10.txt",
            "medium": "medium_10.txt",
            "hard": "hard_10.txt",
            "expert": "expert_10.txt"
        }
        for lvl, fname in files.items():
            fpath = os.path.join(PROJECT_ROOT, "Release", "puzzles", fname)
            if os.path.exists(fpath):
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        cur_id = ""
                        clues = 0
                        for line in f:
                            line = line.strip()
                            if line.startswith("#") and "Clues:" in line:
                                parts = line.split("-")
                                cur_id = parts[0].replace("#", "").strip()
                                clues = int(parts[1].split(":")[1].strip())
                            elif line and not line.startswith("#"):
                                data[lvl].append({"id": cur_id, "clues": clues, "string": line})
                except Exception:
                    pass
        return data

    def _get_active_curated_level_key(self) -> str:
        """Lấy mã cấp độ (easy, medium, hard, expert) từ combobox cấp độ."""
        idx = self.cbo_level.current()
        mapping = ["easy", "medium", "hard", "expert"]
        return mapping[idx] if 0 <= idx < len(mapping) else "easy"

    def _on_level_changed(self, event=None) -> None:
        """Cập nhật danh sách bản đồ khi người dùng đổi cấp độ trên Combobox."""
        if not hasattr(self, "cbo_board"):
            return
        lvl_key = self._get_active_curated_level_key()
        boards = self.curated_puzzles.get(lvl_key, [])
        options = [f"Bản đồ #{i+1} ({b.get('clues', '?')} clues)" for i, b in enumerate(boards)]
        if not options:
            options = [f"Bản đồ #{i+1}" for i in range(10)]
        self.cbo_board["values"] = options
        self.cbo_board.current(0)

    def load_selected_curated_puzzle(self) -> None:
        """Nạp bản đồ đã chọn trong combobox cấp độ và bản đồ."""
        self._stop_simulation()
        lvl_key = self._get_active_curated_level_key()
        boards = self.curated_puzzles.get(lvl_key, [])
        idx = self.cbo_board.current()
        if idx < 0 or idx >= len(boards):
            idx = 0

        p = boards[idx]
        self.graph.load_from_string(p["string"])
        self.selected_vertex = None
        self.hint_vertex = None
        self.render_board()
        self.update_inspector()

        lvl_names = {"easy": "Dễ", "medium": "Trung bình", "hard": "Khó", "expert": "Chuyên gia"}
        lName = lvl_names.get(lvl_key, lvl_key.capitalize())
        self.log_message(f"Đã nạp Bản đồ #{idx+1}/10 cấp độ {lName} ({p.get('clues', 0)} clues, nghiệm duy nhất).")

    def navigate_curated_puzzle(self, delta: int) -> None:
        """Chuyển sang bản đồ trước (-1) hoặc bản đồ tiếp theo (+1) trong cấp độ hiện tại."""
        lvl_key = self._get_active_curated_level_key()
        boards = self.curated_puzzles.get(lvl_key, [])
        if not boards:
            return
        cur_idx = self.cbo_board.current()
        next_idx = (cur_idx + delta) % len(boards)
        self.cbo_board.current(next_idx)
        self.load_selected_curated_puzzle()

    def open_all_curated_puzzles_dialog(self) -> None:
        """Mở cửa sổ duyệt danh sách toàn bộ 40 bản đồ tuyển chọn theo 4 cấp độ."""
        self._stop_simulation()
        top = tk.Toplevel(self.root)
        top.title("HCMUE - Kho 40 Bản đồ Sudoku Tuyển chọn (10 đề / cấp độ)")
        top.geometry("720x460")
        top.minsize(620, 360)
        top.configure(bg=self.COLOR_BG)
        top.transient(self.root)
        top.grab_set()

        # Tiêu đề
        lbl_head = tk.Label(
            top,
            text="📚 KHO 40 BẢN ĐỒ SUDOKU TUYỂN CHỌN THEO 4 CẤP ĐỘ",
            font=("Segoe UI", 11, "bold"),
            bg=self.COLOR_BG,
            fg="#2f3640"
        )
        lbl_head.pack(anchor="w", padx=15, pady=(12, 6))

        # Khung lọc cấp độ
        filter_frame = tk.Frame(top, bg=self.COLOR_BG)
        filter_frame.pack(fill=tk.X, padx=15, pady=(0, 6))

        tk.Label(filter_frame, text="Lọc cấp độ:", font=("Segoe UI", 9, "bold"), bg=self.COLOR_BG).pack(side=tk.LEFT, padx=(0, 6))

        level_var = tk.StringVar(value="all")
        for code, name in [("all", "Tất cả (40 đề)"), ("easy", "🟢 Dễ (10)"), ("medium", "🟡 Trung bình (10)"), ("hard", "🟠 Khó (10)"), ("expert", "🔴 Chuyên gia (10)")]:
            rb = tk.Radiobutton(
                filter_frame,
                text=name,
                value=code,
                variable=level_var,
                bg=self.COLOR_BG,
                font=("Segoe UI", 8),
                command=lambda: populate_tree()
            )
            rb.pack(side=tk.LEFT, padx=3)

        # Bảng hiển thị
        table_frame = tk.Frame(top, bg=self.COLOR_BG)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=4)

        columns = ("id", "level", "name", "clues", "sol")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=13)
        tree.heading("id", text="Mã đề")
        tree.heading("level", text="Cấp độ")
        tree.heading("name", text="Tên bản đồ")
        tree.heading("clues", text="Số clues")
        tree.heading("sol", text="Tính khả giải")

        tree.column("id", width=80, anchor="center")
        tree.column("level", width=100, anchor="center")
        tree.column("name", width=160)
        tree.column("clues", width=80, anchor="center")
        tree.column("sol", width=160, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        level_display = {"easy": "🟢 Dễ", "medium": "🟡 Trung bình", "hard": "🟠 Khó", "expert": "🔴 Chuyên gia"}

        def populate_tree():
            for item in tree.get_children():
                tree.delete(item)
            selected_lvl = level_var.get()
            for lvl_key in ["easy", "medium", "hard", "expert"]:
                if selected_lvl != "all" and selected_lvl != lvl_key:
                    continue
                boards = self.curated_puzzles.get(lvl_key, [])
                for i, b in enumerate(boards):
                    tree.insert(
                        "",
                        tk.END,
                        iid=f"{lvl_key}_{i}",
                        values=(
                            b.get("id", f"#{i+1}"),
                            level_display.get(lvl_key, lvl_key),
                            f"Bản đồ #{i+1} ({lvl_key})",
                            f"{b.get('clues', 0)} / 81",
                            "✔ 1 nghiệm duy nhất"
                        )
                    )

        populate_tree()

        # Thanh nút thao tác
        btn_bar = tk.Frame(top, bg=self.COLOR_BG, pady=10)
        btn_bar.pack(fill=tk.X, padx=15)

        def on_load_click():
            sel = tree.selection()
            if not sel:
                messagebox.showwarning("Chọn bản đồ", "Vui lòng click chọn 1 bản đồ trong bảng!", parent=top)
                return
            key = sel[0]
            lvl_key, idx_str = key.split("_")
            idx = int(idx_str)
            p = self.curated_puzzles[lvl_key][idx]

            self.graph.load_from_string(p["string"])
            self.selected_vertex = None
            self.hint_vertex = None
            self.render_board()
            self.update_inspector()

            mapping = {"easy": 0, "medium": 1, "hard": 2, "expert": 3}
            if lvl_key in mapping:
                self.cbo_level.current(mapping[lvl_key])
                self._on_level_changed()
                self.cbo_board.current(idx)

            lName = level_display.get(lvl_key, lvl_key)
            self.log_message(f"Đã nạp {lName} - Bản đồ #{idx+1} ({p.get('clues', 0)} clues) từ Kho 40 đề.")
            top.destroy()

        def on_copy_click():
            sel = tree.selection()
            if not sel:
                messagebox.showwarning("Chọn bản đồ", "Vui lòng click chọn 1 bản đồ trong bảng!", parent=top)
                return
            key = sel[0]
            lvl_key, idx_str = key.split("_")
            p = self.curated_puzzles[lvl_key][int(idx_str)]
            self.root.clipboard_clear()
            self.root.clipboard_append(p["string"])
            messagebox.showinfo("Đã sao chép", f"Đã sao chép mã 81 số của bản đồ {p.get('id', '')}!", parent=top)

        btn_load = tk.Button(
            btn_bar,
            text="▶ Nạp bản đồ này",
            font=("Segoe UI", 9, "bold"),
            bg="#0984e3",
            fg="white",
            relief=tk.FLAT,
            padx=10,
            pady=4,
            command=on_load_click
        )
        btn_load.pack(side=tk.LEFT, padx=(0, 6))

        btn_copy = tk.Button(
            btn_bar,
            text="📋 Sao chép mã 81 số",
            font=("Segoe UI", 9),
            bg="#f1f2f6",
            relief=tk.GROOVE,
            padx=8,
            pady=4,
            command=on_copy_click
        )
        btn_copy.pack(side=tk.LEFT, padx=(0, 6))

        btn_close = tk.Button(
            btn_bar,
            text="Đóng",
            font=("Segoe UI", 9),
            bg="#dfe6e9",
            relief=tk.FLAT,
            padx=10,
            pady=4,
            command=top.destroy
        )
        btn_close.pack(side=tk.RIGHT)

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
        """Xóa trắng toàn bộ bàn cờ để người dùng tự do nhập đề bài mới."""
        self._stop_simulation()
        self.graph.clear()
        self.selected_vertex = 0
        self.hint_vertex = None
        self.render_board()
        self.update_inspector()
        self.log_message("ĐÃ BẬT CHẾ ĐỘ NHẬP BÀN CỜ TRỐNG: Hãy click vào các ô và gõ phím số [1..9] để tự tạo đề bài.")

    def lock_as_puzzle(self) -> None:
        """Khóa các số đã nhập trên bàn cờ làm đề bài chính thức (tiền tô màu cố định)."""
        clues = sum(1 for c in self.graph.colors if c != 0)
        if clues == 0:
            messagebox.showwarning("Cảnh báo", "Bàn cờ đang trống! Vui lòng nhập các con số trước khi khóa làm đề.")
            return

        conflicts = self.graph.get_all_conflicts()
        if conflicts:
            messagebox.showerror(
                "Xung đột",
                f"Bàn cờ có {len(conflicts)} cặp ô bị trùng màu! Vui lòng xóa hoặc sửa các ô vi phạm trước khi khóa làm đề."
            )
            return

        for v in range(self.graph.num_vertices):
            self.graph.is_precolored[v] = (self.graph.colors[v] != 0)

        self.render_board()
        self.update_inspector()
        self.log_message(f"Đã cố định {clues} số vừa nhập thành đề bài chính thức (tiền tô màu).")
        messagebox.showinfo(
            "Khóa đề thành công",
            f"Đã khóa thành công {clues} số làm đề bài chính thức!\nBây giờ bạn có thể bắt đầu giải, chạy thuật toán hoặc xem gợi ý."
        )

    def _get_saved_puzzles_path(self) -> str:
        """Đường dẫn tệp lưu trữ danh sách bàn cờ tự tạo."""
        puzzles_dir = os.path.join(PROJECT_ROOT, "Release", "puzzles")
        os.makedirs(puzzles_dir, exist_ok=True)
        return os.path.join(puzzles_dir, "saved_custom_puzzles.json")

    def _load_saved_puzzles(self) -> list:
        """Nạp danh sách bàn cờ đã lưu từ tệp JSON."""
        path = self._get_saved_puzzles_path()
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        return data
            except Exception as e:
                self.log_message(f"Không thể đọc file bàn cờ đã lưu: {e}")

        # Danh sách mặc định ban đầu nếu tệp chưa có
        defaults = [
            {
                "id": "board_sample_easy",
                "name": "Đề Mẫu 1: Dễ Nhập Môn",
                "created_at": "2026-11-19 09:00",
                "string": "530070000600195000098000060800060003400803001700020006060000280000419005000080079",
                "clues_count": 30,
                "solutions_count": 1
            },
            {
                "id": "board_sample_medium",
                "name": "Đề Mẫu 2: Đối Xứng Hoa Cúc",
                "created_at": "2026-11-19 09:00",
                "string": "000000010400000000020000000000050407008000300001090000300400200050100000000806000",
                "clues_count": 22,
                "solutions_count": 1
            },
            {
                "id": "board_sample_17",
                "name": "Đề Mẫu 3: Độc Đáo 17 Số",
                "created_at": "2026-11-19 09:00",
                "string": "000000012000000003002300400001800005060070800000009000008500000900040500470006000",
                "clues_count": 17,
                "solutions_count": 1
            }
        ]
        self._save_saved_puzzles(defaults)
        return defaults

    def _save_saved_puzzles(self, puzzles: list) -> None:
        """Ghi danh sách bàn cờ vào tệp JSON."""
        path = self._get_saved_puzzles_path()
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(puzzles, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.log_message(f"Lỗi khi ghi tệp bàn cờ đã lưu: {e}")

    def save_custom_board(self) -> None:
        """Lưu bàn cờ hiện tại vào Mục Bàn cờ đã lưu."""
        clues = sum(1 for c in self.graph.colors if c != 0)
        if clues == 0:
            messagebox.showwarning("Cảnh báo", "Bàn cờ đang trống! Vui lòng nhập các số trước khi lưu.")
            return

        conflicts = self.graph.get_all_conflicts()
        if conflicts:
            messagebox.showerror(
                "Xung đột",
                f"Bàn cờ có {len(conflicts)} cặp ô bị trùng màu! Vui lòng sửa lại trước khi lưu."
            )
            return

        saved_list = self._load_saved_puzzles()
        default_name = f"Bàn cờ tự tạo #{len(saved_list) + 1}"
        name = simpledialog.askstring(
            "Lưu bàn cờ",
            "Nhập tên gợi nhớ cho bàn cờ tự tạo:",
            initialvalue=default_name,
            parent=self.root
        )
        if not name or not name.strip():
            return

        name = name.strip()
        board_str = "".join(str(c) if c != 0 else "." for c in self.graph.colors)
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        # Kiểm tra nhanh số nghiệm
        sol_info = self.graph.check_solvability()
        sols_count = sol_info.get("solutions_count", 1)

        new_item = {
            "id": f"board_{int(datetime.datetime.now().timestamp())}",
            "name": name,
            "created_at": now_str,
            "string": board_str,
            "clues_count": clues,
            "solutions_count": sols_count
        }

        saved_list.insert(0, new_item)
        self._save_saved_puzzles(saved_list)
        self.log_message(f"Đã lưu thành công bàn cờ '{name}' ({clues} số) vào Mục Bàn cờ đã lưu.")
        messagebox.showinfo(
            "Lưu thành công",
            f"Đã lưu thành công bàn cờ '{name}' vào Mục Bàn cờ đã lưu!\n"
            f"- Số clues: {clues}/81\n"
            f"- Thẩm định khả giải: {sol_info.get('status', 'Khả giải')} ({sols_count} nghiệm)\n\n"
            f"Bạn có thể mở nút '📁 Bàn cờ đã lưu' để xem lại bất cứ lúc nào."
        )

    def open_saved_puzzles_dialog(self) -> None:
        """Mở cửa sổ quản lý và chọn các bàn cờ đã lưu."""
        self._stop_simulation()
        saved_list = self._load_saved_puzzles()

        top = tk.Toplevel(self.root)
        top.title("HCMUE - Mục Bàn cờ Sudoku đã lưu")
        top.geometry("680x440")
        top.minsize(580, 350)
        top.configure(bg=self.COLOR_BG)
        top.transient(self.root)
        top.grab_set()

        # Tiêu đề
        lbl_head = tk.Label(
            top,
            text="📁 DANH SÁCH BÀN CỜ ĐÃ LƯU & TỰ TẠO",
            font=("Segoe UI", 11, "bold"),
            bg=self.COLOR_BG,
            fg="#2f3640"
        )
        lbl_head.pack(anchor="w", padx=15, pady=(12, 6))

        # Khung bảng dữ liệu
        table_frame = tk.Frame(top, bg=self.COLOR_BG)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=4)

        columns = ("name", "clues", "sols", "date")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)
        tree.heading("name", text="Tên bàn cờ")
        tree.heading("clues", text="Số clues")
        tree.heading("sols", text="Số nghiệm")
        tree.heading("date", text="Ngày lưu")

        tree.column("name", width=250)
        tree.column("clues", width=80, anchor="center")
        tree.column("sols", width=120, anchor="center")
        tree.column("date", width=140, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)

        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        def refresh_tree():
            for item in tree.get_children():
                tree.delete(item)
            nonlocal saved_list
            saved_list = self._load_saved_puzzles()
            for b in saved_list:
                sols_str = "1 nghiệm duy nhất ✔" if b.get("solutions_count") == 1 else (
                    "0 nghiệm (Bế tắc) 🛑" if b.get("solutions_count") == 0 else f"{b.get('solutions_count', '>1')} nghiệm"
                )
                tree.insert(
                    "",
                    tk.END,
                    iid=b["id"],
                    values=(b["name"], f"{b.get('clues_count', 0)} / 81", sols_str, b.get("created_at", ""))
                )

        refresh_tree()

        # Nút chức năng phía dưới
        btn_bar = tk.Frame(top, bg=self.COLOR_BG, pady=10)
        btn_bar.pack(fill=tk.X, padx=15)

        def on_play_selected():
            sel = tree.selection()
            if not sel:
                messagebox.showwarning("Chọn bàn cờ", "Vui lòng click chọn 1 bàn cờ trong danh sách!", parent=top)
                return
            board_id = sel[0]
            board = next((b for b in saved_list if b["id"] == board_id), None)
            if not board:
                return

            self.graph.load_from_string(board["string"])
            self.selected_vertex = None
            self.hint_vertex = None
            self.render_board()
            self.update_inspector()
            self.log_message(f"Đã nạp bàn cờ đã lưu: '{board['name']}' ({board.get('clues_count', 0)} clues) để giải.")
            top.destroy()

        def on_edit_selected():
            sel = tree.selection()
            if not sel:
                messagebox.showwarning("Chọn bàn cờ", "Vui lòng click chọn 1 bàn cờ trong danh sách!", parent=top)
                return
            board_id = sel[0]
            board = next((b for b in saved_list if b["id"] == board_id), None)
            if not board:
                return

            clean = board["string"].replace(".", "0")
            self.graph.clear()
            for i, ch in enumerate(clean):
                if i < 81 and ch in "123456789":
                    self.graph.colors[i] = int(ch)
            self.selected_vertex = 0
            self.hint_vertex = None
            self.render_board()
            self.update_inspector()
            self.log_message(f"Đang mở bàn cờ '{board['name']}' trên lưới trống để chỉnh sửa số đề bài.")
            top.destroy()

        def on_copy_selected():
            sel = tree.selection()
            if not sel:
                messagebox.showwarning("Chọn bàn cờ", "Vui lòng click chọn 1 bàn cờ trong danh sách!", parent=top)
                return
            board_id = sel[0]
            board = next((b for b in saved_list if b["id"] == board_id), None)
            if not board:
                return
            self.root.clipboard_clear()
            self.root.clipboard_append(board["string"])
            messagebox.showinfo("Đã sao chép", f"Đã sao chép mã 81 số của '{board['name']}' vào clipboard!", parent=top)

        def on_delete_selected():
            sel = tree.selection()
            if not sel:
                messagebox.showwarning("Chọn bàn cờ", "Vui lòng click chọn 1 bàn cờ trong danh sách!", parent=top)
                return
            board_id = sel[0]
            board = next((b for b in saved_list if b["id"] == board_id), None)
            if not board:
                return
            if messagebox.askyesno("Xác nhận xóa", f"Bạn có chắc muốn xóa bàn cờ '{board['name']}' khỏi danh sách?", parent=top):
                next_list = [b for b in saved_list if b["id"] != board_id]
                self._save_saved_puzzles(next_list)
                refresh_tree()
                self.log_message(f"Đã xóa bàn cờ '{board['name']}' khỏi mục đã lưu.")

        btn_play = tk.Button(
            btn_bar,
            text="▶ Nạp để giải / chơi",
            font=("Segoe UI", 9, "bold"),
            bg="#0984e3",
            fg="white",
            relief=tk.FLAT,
            padx=10,
            pady=4,
            command=on_play_selected
        )
        btn_play.pack(side=tk.LEFT, padx=(0, 6))

        btn_edit = tk.Button(
            btn_bar,
            text="✏️ Sửa trên lưới trống",
            font=("Segoe UI", 9),
            bg="#f1f2f6",
            relief=tk.GROOVE,
            padx=8,
            pady=4,
            command=on_edit_selected
        )
        btn_edit.pack(side=tk.LEFT, padx=(0, 6))

        btn_copy = tk.Button(
            btn_bar,
            text="📋 Sao chép mã 81 số",
            font=("Segoe UI", 9),
            bg="#f1f2f6",
            relief=tk.GROOVE,
            padx=8,
            pady=4,
            command=on_copy_selected
        )
        btn_copy.pack(side=tk.LEFT, padx=(0, 6))

        btn_del = tk.Button(
            btn_bar,
            text="🗑 Xóa",
            font=("Segoe UI", 9),
            bg="#ff7675",
            fg="white",
            relief=tk.FLAT,
            padx=8,
            pady=4,
            command=on_delete_selected
        )
        btn_del.pack(side=tk.LEFT, padx=(0, 6))

        btn_close = tk.Button(
            btn_bar,
            text="Đóng",
            font=("Segoe UI", 9),
            bg="#dfe6e9",
            relief=tk.FLAT,
            padx=10,
            pady=4,
            command=top.destroy
        )
        btn_close.pack(side=tk.RIGHT)

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
