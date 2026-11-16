"""
Mô-đun cài đặt Thuật toán DSATUR (Degree of Saturation - Brélaz, 1979).
Phục vụ môn học: Lý thuyết đồ thị và Ứng dụng - Khoa CNTT, HCMUE.
Phụ trách: Thành viên 2 (Thuật toán Tham lam & DSATUR).

Tài liệu tham khảo:
[2] D. Brélaz, "New methods to color the vertices of a graph", Communications
    of the ACM, Vol. 22, No. 4, pp. 251-256, 1979.

Nguyên lý hoạt động của Heuristic DSATUR:
1. Định nghĩa Bậc bão hòa (Saturation Degree - sat_deg(v)):
   sat_deg(v) là số lượng màu KHÁC NHAU đã xuất hiện ở các đỉnh kề của v.
   sat_deg(v) = |{colors[u] | u in N(v), colors[u] != 0}|.
2. Chiến lược lựa chọn đỉnh động:
   - Luôn chọn đỉnh chưa tô có Bậc bão hòa LỚN NHẤT: max(sat_deg(v)).
     (Đỉnh chịu nhiều ràng buộc nhất, có nguy cơ bế tắc cao nhất nên cần giải quyết trước).
   - Quy tắc phá vỡ thế hòa (Tie-breaking):
     + Tiêu chí 1: Đỉnh có số đỉnh kề chưa tô lớn nhất (bậc trong đồ thị con chưa tô).
     + Tiêu chí 2: Đỉnh có miền giá trị khả dụng hẹp nhất (MRV - Minimum Remaining Values).
     + Tiêu chí 3: Đỉnh có chỉ số nhỏ nhất (v nhỏ hơn).
3. Gán màu:
   - Gán màu hợp lệ nhỏ nhất trong tập màu khả dụng {1..9}.
4. Cập nhật động:
   - Sau khi gán màu cho đỉnh u, lập tức cập nhật bậc bão hòa cho 20 đỉnh kề N(u).
5. Hiệu năng trên Sudoku:
   - Giải quyết tức thì và không cần quay lui trên hầu hết các đề Dễ và Trung bình.
   - Trên các đề Khó/Chuyên gia (ít clues), nếu tham lam thuần túy gặp bế tắc,
     thuật toán sẽ báo DEADLOCK (đặt tiền đề cho TV3 bổ sung cơ chế Backtracking).
"""

import time
from typing import List, Dict, Set, Tuple, Optional, Generator
from Source.core.sudoku_graph import SudokuGraph


class DSATURSolver:
    """
    Bộ giải Sudoku bằng Thuật toán DSATUR thuần túy (Heuristic bậc bão hòa động).
    Hỗ trợ cả chế độ giải siêu tốc lẫn chế độ chạy từng bước (Step-by-step)
    để TV4 tích hợp vào giao diện trực quan hóa.
    """

    def __init__(self, graph: SudokuGraph):
        """
        Khởi tạo bộ giải DSATUR.
        :param graph: Đối tượng SudokuGraph đại diện cho bàn cờ Sudoku 9x9.
        """
        self.graph: SudokuGraph = graph
        self.steps_history: List[Dict] = []
        self.execution_time_ms: float = 0.0

        # Mảng lưu trữ động tập các màu đã xuất hiện ở lân cận của mỗi đỉnh
        # neighbor_colors_set[v] = {màu của các đỉnh u in N(v)}
        self.neighbor_colors_set: List[Set[int]] = [set() for _ in range(self.graph.num_vertices)]
        self._init_dynamic_structures()

    def _init_dynamic_structures(self) -> None:
        """Khởi tạo cấu trúc theo dõi tập màu lân cận từ các đỉnh tiền tô màu ban đầu."""
        for v in range(self.graph.num_vertices):
            self.neighbor_colors_set[v] = {
                self.graph.colors[nbr]
                for nbr in self.graph.adjacency_list[v]
                if self.graph.colors[nbr] != 0
            }

    def get_saturation_degree(self, vertex: int) -> int:
        """Trả về bậc bão hòa hiện tại của đỉnh vertex trong O(1)."""
        return len(self.neighbor_colors_set[vertex])

    def get_all_saturations(self) -> List[int]:
        """Trả về danh sách bậc bão hòa của toàn bộ 81 đỉnh (phục vụ hiển thị UI)."""
        return [len(self.neighbor_colors_set[v]) for v in range(self.graph.num_vertices)]

    def get_uncolored_degree(self, vertex: int) -> int:
        """
        Tính số đỉnh kề chưa tô màu của vertex (Bậc trong đồ thị con chưa tô).
        Dùng làm tiêu chí phá vỡ thế hòa số 1 của Daniel Brélaz.
        """
        return sum(1 for nbr in self.graph.adjacency_list[vertex] if self.graph.colors[nbr] == 0)

    def select_next_vertex(self) -> Optional[int]:
        """
        Lựa chọn đỉnh tiếp theo để tô màu theo nguyên lý chuẩn của Brélaz (1979):
        1. Ưu tiên đỉnh chưa tô có Bậc bão hòa sat_deg lớn nhất.
        2. Tie-break 1: Đỉnh có số đỉnh kề chưa tô lớn nhất (uncolored degree).
        3. Tie-break 2: Đỉnh có miền giá trị khả dụng hẹp nhất (MRV).
        4. Tie-break 3: Chỉ số đỉnh nhỏ nhất.
        """
        uncolored = self.graph.get_uncolored_vertices()
        if not uncolored:
            return None

        def vertex_priority(v: int):
            sat = len(self.neighbor_colors_set[v])
            uncolored_deg = self.get_uncolored_degree(v)
            available_count = len(self.graph.PALETTE - self.neighbor_colors_set[v])
            # sat càng lớn càng ưu tiên; uncolored_deg càng lớn càng ưu tiên;
            # available_count càng nhỏ càng ưu tiên; v càng nhỏ càng ưu tiên.
            return (sat, uncolored_deg, -available_count, -v)

        return max(uncolored, key=vertex_priority)

    def _update_saturation_after_coloring(self, colored_vertex: int, color: int) -> None:
        """
        Cập nhật động bậc bão hòa cho 20 đỉnh kề của colored_vertex sau khi gán màu:
        Thêm color vào neighbor_colors_set của từng đỉnh kề chưa tô.
        Độ phức tạp O(deg(v)) = O(20) = O(1).
        """
        for nbr in self.graph.adjacency_list[colored_vertex]:
            self.neighbor_colors_set[nbr].add(color)

    def solve(self) -> Dict:
        """
        Thực hiện giải Sudoku bằng giải thuật DSATUR tham lam thuần túy.
        
        Trả về từ điển kết quả chứa:
        - status: "SUCCESS" nếu giải hoàn tất, "DEADLOCK" nếu gặp bế tắc, "INITIAL_CONFLICT" nếu đề sai.
        - execution_time_ms: Thời gian chạy tính bằng mili-giây.
        - total_steps: Số bước tô màu đã thực hiện.
        - colored_count: Số ô đã có màu trên bàn cờ.
        - remaining_uncolored: Số ô trống còn lại.
        - deadlock_info: Chi tiết ô bị bế tắc (nếu có).
        - steps: Toàn bộ nhật ký từng bước gán màu.
        """
        self.steps_history = []
        self._init_dynamic_structures()
        start_time = time.perf_counter()

        # Kiểm tra tính hợp lệ ban đầu
        conflicts = self.graph.get_all_conflicts()
        if conflicts:
            self.execution_time_ms = (time.perf_counter() - start_time) * 1000.0
            return {
                "status": "INITIAL_CONFLICT",
                "message": "Bàn cờ ban đầu có xung đột tiền tô màu vi phạm luật Sudoku.",
                "execution_time_ms": self.execution_time_ms,
                "total_steps": 0,
                "colored_count": sum(1 for c in self.graph.colors if c != 0),
                "remaining_uncolored": len(self.graph.get_uncolored_vertices()),
                "deadlock_info": None,
                "steps": []
            }

        deadlock_info = None
        step_idx = 0

        while True:
            # 1. Chọn đỉnh có bậc bão hòa lớn nhất
            v = self.select_next_vertex()
            if v is None:
                # Đã tô xong toàn bộ các đỉnh
                break

            step_idx += 1
            r, c = SudokuGraph.index_to_coords(v)
            sat_deg = self.get_saturation_degree(v)
            used_colors = self.neighbor_colors_set[v]
            available = self.graph.PALETTE - used_colors

            if not available:
                # Ngõ cụt: Bậc bão hòa = 9, không còn màu hợp lệ nào
                deadlock_info = {
                    "vertex": v,
                    "row": r,
                    "col": c,
                    "saturation_degree": sat_deg,
                    "uncolored_degree": self.get_uncolored_degree(v),
                    "used_colors_in_neighbors": sorted(list(used_colors)),
                    "step_failed": step_idx,
                    "reason": (
                        f"Tại bước {step_idx}, Heuristic DSATUR chọn ô ({r + 1}, {c + 1}) "
                        f"[đỉnh {v}] với Bậc bão hòa tối đại = {sat_deg}/9. "
                        f"Tất cả 9 màu đều đã bị 20 đỉnh kề chiếm dụng. "
                        f"Do DSATUR thuần túy là giải thuật tham lam một chiều (không quay lui), "
                        f"hệ thống ghi nhận trạng thái bế tắc (Deadlock)."
                    )
                }
                self.steps_history.append({
                    "step": step_idx,
                    "action": "DEADLOCK",
                    "vertex": v,
                    "row": r,
                    "col": c,
                    "saturation_degree": sat_deg,
                    "uncolored_degree": self.get_uncolored_degree(v),
                    "available_colors": [],
                    "assigned_color": None
                })
                break

            # 2. Gán màu nhỏ nhất hợp lệ (Greedy First-Fit)
            chosen_color = min(available)
            self.graph.assign_color(v, chosen_color)

            # 3. Cập nhật động bậc bão hòa cho 20 đỉnh kề
            self._update_saturation_after_coloring(v, chosen_color)

            # 4. Ghi nhận bước đi
            self.steps_history.append({
                "step": step_idx,
                "action": "ASSIGN",
                "vertex": v,
                "row": r,
                "col": c,
                "saturation_degree": sat_deg,
                "uncolored_degree": self.get_uncolored_degree(v),
                "available_colors": sorted(list(available)),
                "assigned_color": chosen_color
            })

        self.execution_time_ms = (time.perf_counter() - start_time) * 1000.0
        is_complete = self.graph.is_complete()

        status = "SUCCESS" if is_complete else "DEADLOCK"
        msg = (
            "Giải thành công bằng Heuristic DSATUR!"
            if is_complete
            else "DSATUR thuần túy gặp bế tắc (Cần kết hợp Backtracking của TV3)."
        )

        return {
            "status": status,
            "message": msg,
            "execution_time_ms": self.execution_time_ms,
            "total_steps": len(self.steps_history),
            "colored_count": sum(1 for c in self.graph.colors if c != 0),
            "remaining_uncolored": len(self.graph.get_uncolored_vertices()),
            "deadlock_info": deadlock_info,
            "steps": self.steps_history
        }

    def step_generator(self) -> Generator[Dict, None, None]:
        """
        Generator cho phép duyệt từng bước giải (dành riêng cho TV4 làm chế độ Step-by-step trên GUI).
        Mỗi lần next() sẽ trả về trạng thái của bước gán màu hiện tại.
        """
        self._init_dynamic_structures()
        step_idx = 0

        while True:
            v = self.select_next_vertex()
            if v is None:
                yield {
                    "step": step_idx,
                    "action": "FINISHED",
                    "vertex": None,
                    "is_complete": self.graph.is_complete()
                }
                break

            step_idx += 1
            r, c = SudokuGraph.index_to_coords(v)
            sat_deg = self.get_saturation_degree(v)
            used_colors = self.neighbor_colors_set[v]
            available = self.graph.PALETTE - used_colors

            if not available:
                yield {
                    "step": step_idx,
                    "action": "DEADLOCK",
                    "vertex": v,
                    "row": r,
                    "col": c,
                    "saturation_degree": sat_deg,
                    "uncolored_degree": self.get_uncolored_degree(v),
                    "available_colors": [],
                    "assigned_color": None
                }
                break

            chosen_color = min(available)
            self.graph.assign_color(v, chosen_color)
            self._update_saturation_after_coloring(v, chosen_color)

            yield {
                "step": step_idx,
                "action": "ASSIGN",
                "vertex": v,
                "row": r,
                "col": c,
                "saturation_degree": sat_deg,
                "uncolored_degree": self.get_uncolored_degree(v),
                "available_colors": sorted(list(available)),
                "assigned_color": chosen_color
            }
