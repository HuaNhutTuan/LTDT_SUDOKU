"""
Mô-đun SudokuGraph - Mô hình hóa trò chơi Sudoku 9x9 dưới dạng Đồ thị vô hướng.
Phục vụ môn học: Lý thuyết đồ thị và Ứng dụng - Khoa CNTT, HCMUE.
Phụ trách: Thành viên 1 (Nhóm trưởng - Kiến trúc & Đồ thị).

Bản chất toán học:
- Tập đỉnh V: Gồm đúng 81 đỉnh (chỉ số 0..80), ánh xạ 1-1 với tọa độ (hàng r, cột c) theo quy tắc:
    v = r * 9 + c  <==>  r = v // 9, c = v % 9  (r, c thuộc {0..8})
- Tập cạnh E: Gồm đúng 810 cạnh vô hướng thể hiện các ràng buộc loại trừ lẫn nhau:
    Hai đỉnh u(r1, c1) và v(r2, c2) kề nhau (có cạnh nối) khi và chỉ khi:
    (r1 == r2) hoặc (c1 == c2) hoặc (r1 // 3 == r2 // 3 và c1 // 3 == c2 // 3).
- Bậc của mỗi đỉnh deg(v) = 20 với mọi v thuộc V (8 cùng hàng + 8 cùng cột + 4 cùng ô vuông 3x3).
  Do đó đồ thị Sudoku là Đồ thị chính quy bậc 20 (20-regular graph).
- Tổng số cạnh: |E| = (81 * 20) / 2 = 810 cạnh.
- Bài toán giải Sudoku tương đương với Bài toán Mở rộng tiền tô màu (Pre-coloring Extension)
  trên đồ thị G với k = 9 màu C = {1, 2, 3, 4, 5, 6, 7, 8, 9}.
"""

from typing import List, Set, Tuple, Optional, Dict
from copy import deepcopy
from .graph import Graph


class PrecoloringConflictError(Exception):
    """Ngoại lệ ném ra khi bảng tiền tô màu (đề bài ban đầu) vi phạm luật Sudoku."""
    pass


class SudokuGraph(Graph):
    """
    Lớp biểu diễn đồ thị Sudoku chuẩn 9x9 kế thừa từ Graph tổng quát.
    Quản lý 81 đỉnh, 810 cạnh, trạng thái tô màu, bậc bão hòa và các ràng buộc.
    """

    NUM_VERTICES = 81
    NUM_EDGES = 810
    DEGREE = 20
    PALETTE = set(range(1, 10))  # Tập 9 màu: {1, 2, 3, 4, 5, 6, 7, 8, 9}

    def __init__(self):
        super().__init__(self.NUM_VERTICES)
        
        # Mảng lưu màu hiện tại của 81 đỉnh (0: chưa tô màu, 1..9: đã gán màu)
        self.colors: List[int] = [0] * self.NUM_VERTICES
        
        # Đánh dấu các đỉnh được gán màu cố định từ đề bài ban đầu (Precolored)
        self.is_precolored: List[bool] = [False] * self.NUM_VERTICES
        
        # Xây dựng tự động 810 cạnh theo luật Sudoku
        self._build_sudoku_edges()
        
        # Xác thực kiểm tra tính chính quy 20-regular và số cạnh 810
        self._validate_graph_topology()

    # =========================================================================
    # PHẦN 1: MÔ HÌNH HÓA ĐỒ THỊ VÀ XÂY DỰNG CẠNH (81 đỉnh, 810 cạnh)
    # =========================================================================

    @staticmethod
    def coords_to_index(row: int, col: int) -> int:
        """Chuyển đổi tọa độ (hàng, cột) sang chỉ số đỉnh v thuộc [0..80]."""
        if not (0 <= row < 9 and 0 <= col < 9):
            raise IndexError(f"Tọa độ (hàng={row}, cột={col}) không hợp lệ trên bàn cờ 9x9.")
        return row * 9 + col

    @staticmethod
    def index_to_coords(vertex: int) -> Tuple[int, int]:
        """Chuyển đổi chỉ số đỉnh v thuộc [0..80] sang tọa độ (hàng, cột)."""
        if not (0 <= vertex < 81):
            raise IndexError(f"Chỉ số đỉnh {vertex} phải nằm trong miền [0..80].")
        return vertex // 9, vertex % 9

    @staticmethod
    def get_box_index(row: int, col: int) -> int:
        """Xác định chỉ số khối 3x3 [0..8] dựa trên tọa độ (hàng, cột)."""
        return (row // 3) * 3 + (col // 3)

    def _build_sudoku_edges(self) -> None:
        """
        Tự động nối các cạnh vô hướng giữa 81 đỉnh thỏa mãn luật Sudoku:
        Cùng hàng HOẶC cùng cột HOẶC cùng khối 3x3.
        """
        for u in range(self.NUM_VERTICES):
            r1, c1 = self.index_to_coords(u)
            b1 = self.get_box_index(r1, c1)

            for v in range(u + 1, self.NUM_VERTICES):
                r2, c2 = self.index_to_coords(v)
                b2 = self.get_box_index(r2, c2)

                # Nối cạnh nếu thuộc cùng hàng, cùng cột hoặc cùng khối 3x3
                if (r1 == r2) or (c1 == c2) or (b1 == b2):
                    self.add_edge(u, v)

    def _validate_graph_topology(self) -> None:
        """
        Nghiệm thu kiến trúc đồ thị: Đảm bảo đồ thị có đúng 81 đỉnh, 810 cạnh
        và mỗi đỉnh có đúng 20 đỉnh kề (20-regular graph).
        """
        assert self.num_vertices == self.NUM_VERTICES, f"Lỗi: Số đỉnh là {self.num_vertices}, kỳ vọng 81."
        assert self.num_edges == self.NUM_EDGES, f"Lỗi: Số cạnh là {self.num_edges}, kỳ vọng 810."
        for v in range(self.NUM_VERTICES):
            deg = self.get_degree(v)
            assert deg == self.DEGREE, f"Lỗi: Đỉnh {v} có bậc {deg}, kỳ vọng đúng 20."

    def get_row_neighbors(self, vertex: int) -> List[int]:
        """Lấy 8 đỉnh kề cùng hàng với đỉnh vertex."""
        r, c = self.index_to_coords(vertex)
        return [self.coords_to_index(r, col) for col in range(9) if col != c]

    def get_col_neighbors(self, vertex: int) -> List[int]:
        """Lấy 8 đỉnh kề cùng cột với đỉnh vertex."""
        r, c = self.index_to_coords(vertex)
        return [self.coords_to_index(row, c) for row in range(9) if row != r]

    def get_box_neighbors(self, vertex: int) -> List[int]:
        """Lấy 8 đỉnh cùng khối 3x3 với đỉnh vertex (trong đó có 4 đỉnh không cùng hàng/cột)."""
        r, c = self.index_to_coords(vertex)
        start_r, start_c = (r // 3) * 3, (c // 3) * 3
        neighbors = []
        for i in range(3):
            for j in range(3):
                cur_r, cur_c = start_r + i, start_c + j
                if cur_r != r or cur_c != c:
                    neighbors.append(self.coords_to_index(cur_r, cur_c))
        return neighbors

    # =========================================================================
    # PHẦN 2: THAO TÁC TÔ MÀU & TÍNH TOÁN BẬC BÃO HÒA (DSATUR)
    # =========================================================================

    def is_safe(self, vertex: int, color: int) -> bool:
        """
        Kiểm tra tính an toàn (hợp lệ) khi gán màu `color` cho đỉnh `vertex`:
        Màu phải nằm trong {1..9} và không có đỉnh kề nào của `vertex` đang mang màu này.
        """
        if color not in self.PALETTE:
            return False
        for neighbor in self.adjacency_list[vertex]:
            if self.colors[neighbor] == color:
                return False
        return True

    def assign_color(self, vertex: int, color: int, as_precolored: bool = False) -> bool:
        """
        Gán màu cho một đỉnh. Trả về True nếu gán thành công, False nếu màu xung đột.
        """
        if color not in self.PALETTE and color != 0:
            raise ValueError(f"Màu {color} không hợp lệ. Miền màu cho phép là 1..9 (hoặc 0 để xóa màu).")
        
        if color == 0:
            self.unassign_color(vertex)
            return True

        if not self.is_safe(vertex, color):
            return False

        self.colors[vertex] = color
        if as_precolored:
            self.is_precolored[vertex] = True
        return True

    def unassign_color(self, vertex: int) -> None:
        """Hủy gán màu của một đỉnh (trả về trạng thái chưa tô 0). Dùng cho thuật toán quay lui."""
        if not self.is_precolored[vertex]:
            self.colors[vertex] = 0

    def get_saturation_degree(self, vertex: int) -> int:
        """
        Tính bậc bão hòa (Saturation Degree - Brélaz) của đỉnh `vertex`:
        Được định nghĩa là số lượng màu KHÁC NHAU xuất hiện ở các đỉnh kề đã được tô.
        """
        neighbor_colors = {self.colors[nbr] for nbr in self.adjacency_list[vertex] if self.colors[nbr] != 0}
        return len(neighbor_colors)

    def get_available_colors(self, vertex: int) -> Set[int]:
        r"""
        Trả về tập các màu khả dụng trong {1..9} có thể gán an toàn cho đỉnh `vertex`.
        Miền giá trị khả dụng (Domain / Minimum Remaining Values - MRV) = PALETTE \ {màu của các đỉnh kề}.
        """
        if self.colors[vertex] != 0:
            return set()
        used_colors = {self.colors[nbr] for nbr in self.adjacency_list[vertex] if self.colors[nbr] != 0}
        return self.PALETTE - used_colors

    def get_uncolored_vertices(self) -> List[int]:
        """Trả về danh sách tất cả các đỉnh chưa được tô màu."""
        return [v for v in range(self.NUM_VERTICES) if self.colors[v] == 0]

    def is_complete(self) -> bool:
        """Kiểm tra xem toàn bộ 81 đỉnh đã được gán màu hợp lệ chưa (không còn ô trống và không xung đột)."""
        for v in range(self.NUM_VERTICES):
            if self.colors[v] == 0:
                return False
            for nbr in self.adjacency_list[v]:
                if self.colors[v] == self.colors[nbr]:
                    return False
        return True

    # =========================================================================
    # PHẦN 3: NẠP ĐỀ, KIỂM TRA TÍNH HỢP LỆ TIỀN TÔ MÀU (PRE-COLORING VALIDATION)
    # =========================================================================

    def clear(self) -> None:
        """Xóa trắng toàn bộ bảng cờ và trạng thái tiền tô màu."""
        self.colors = [0] * self.NUM_VERTICES
        self.is_precolored = [False] * self.NUM_VERTICES

    def reset_to_precolored(self) -> None:
        """Đặt lại đồ thị về trạng thái đề bài ban đầu (xóa các ô giải, chỉ giữ ô tiền tô màu)."""
        for v in range(self.NUM_VERTICES):
            if not self.is_precolored[v]:
                self.colors[v] = 0

    def load_from_matrix(self, matrix: List[List[int]]) -> None:
        """
        Nạp đề bài Sudoku từ ma trận 9x9.
        Các giá trị từ 1 đến 9 là các đỉnh tiền tô màu (precolored), 0 là ô trống.
        Tự động gọi hàm kiểm tra tính hợp lệ tiền tô màu `validate_precoloring()`.
        """
        if len(matrix) != 9 or any(len(row) != 9 for row in matrix):
            raise ValueError("Kích thước ma trận đề bài không hợp lệ, phải đúng kích thước 9x9.")

        self.clear()
        temp_colors = [0] * self.NUM_VERTICES
        temp_precolored = [False] * self.NUM_VERTICES

        for r in range(9):
            for c in range(9):
                val = matrix[r][c]
                if not (0 <= val <= 9):
                    raise ValueError(f"Giá trị ô ({r}, {c}) = {val} không hợp lệ. Chỉ chấp nhận các số từ 0 đến 9.")
                idx = self.coords_to_index(r, c)
                if val != 0:
                    temp_colors[idx] = val
                    temp_precolored[idx] = True

        self.colors = temp_colors
        self.is_precolored = temp_precolored

        # Kiểm tra tính hợp lệ của đề bài ban đầu
        self.validate_precoloring()

    def load_from_string(self, grid_str: str) -> None:
        """
        Nạp đề bài từ chuỗi 81 ký tự (dùng chữ số 1-9 cho ô có số, và '0' hoặc '.' cho ô trống).
        Bỏ qua các ký tự khoảng trắng hoặc xuống dòng.
        """
        filtered = [ch for ch in grid_str if ch.isdigit() or ch == '.']
        if len(filtered) != 81:
            raise ValueError(f"Chuỗi đề bài phải chứa đúng 81 ký tự hợp lệ, nhận được {len(filtered)} ký tự.")

        matrix = []
        for r in range(9):
            row = []
            for c in range(9):
                ch = filtered[r * 9 + c]
                val = 0 if ch in ('.', '0') else int(ch)
                row.append(val)
            matrix.append(row)

        self.load_from_matrix(matrix)

    def validate_precoloring(self) -> None:
        """
        Kiểm tra tính hợp lệ của bài toán Mở rộng tiền tô màu (Pre-coloring Extension).
        Nếu phát hiện hai đỉnh tiền tô màu kề nhau có cùng màu, lập tức ném ra ngoại lệ
        PrecoloringConflictError kèm thông tin vị trí xung đột chi tiết.
        """
        for u in range(self.NUM_VERTICES):
            c_u = self.colors[u]
            if c_u == 0:
                continue

            r1, c1 = self.index_to_coords(u)
            for v in self.adjacency_list[u]:
                if u < v and self.colors[v] == c_u:
                    r2, c2 = self.index_to_coords(v)
                    # Xác định kiểu xung đột
                    reason = ""
                    if r1 == r2:
                        reason = f"Cùng HÀNG {r1 + 1} (cột {c1 + 1} và {c2 + 1})"
                    elif c1 == c2:
                        reason = f"Cùng CỘT {c1 + 1} (hàng {r1 + 1} và {r2 + 1})"
                    else:
                        box = self.get_box_index(r1, c1) + 1
                        reason = f"Cùng KHỐI 3x3 số {box} (ô ({r1 + 1},{c1 + 1}) và ({r2 + 1},{c2 + 1}))"
                    
                    raise PrecoloringConflictError(
                        f"Xung đột tiền tô màu: Màu {c_u} bị trùng giữa 2 đỉnh kề nhau: {reason}."
                    )

    # =========================================================================
    # PHẦN 4: TIỆN ÍCH XUẤT BẢNG VÀ CHUYỂN ĐỔI DỮ LIỆU
    # =========================================================================

    def to_matrix(self) -> List[List[int]]:
        """Xuất trạng thái đồ thị hiện tại thành ma trận 2 chiều 9x9."""
        return [[self.colors[self.coords_to_index(r, c)] for c in range(9)] for r in range(9)]

    def to_string(self, empty_char: str = ".") -> str:
        """Xuất trạng thái hiện tại thành chuỗi 81 ký tự."""
        chars = []
        for v in range(self.NUM_VERTICES):
            c = self.colors[v]
            chars.append(str(c) if c != 0 else empty_char)
        return "".join(chars)

    def display(self, title: str = "BÀN CỜ SUDOKU") -> None:
        """In bàn cờ Sudoku trực quan ra console với các đường ngăn cách khối 3x3."""
        print(f"\n--- {title} ---")
        line_sep = "+-------+-------+-------+"
        for r in range(9):
            if r % 3 == 0:
                print(line_sep)
            row_str = "| "
            for c in range(9):
                idx = self.coords_to_index(r, c)
                val = self.colors[idx]
                val_str = str(val) if val != 0 else "."
                row_str += val_str + " "
                if (c + 1) % 3 == 0:
                    row_str += "| "
            print(row_str)
        print(line_sep)

    def clone(self) -> 'SudokuGraph':
        """Tạo bản sao sâu (deep copy) của trạng thái đồ thị hiện tại."""
        new_graph = SudokuGraph()
        new_graph.colors = list(self.colors)
        new_graph.is_precolored = list(self.is_precolored)
        return new_graph
