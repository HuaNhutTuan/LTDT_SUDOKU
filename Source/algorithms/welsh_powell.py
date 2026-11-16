"""
Mô-đun cài đặt Thuật toán Welsh-Powell (Tham lam theo bậc cố định).
Phục vụ môn học: Lý thuyết đồ thị và Ứng dụng - Khoa CNTT, HCMUE.
Phụ trách: Thành viên 2 (Thuật toán Tham lam & DSATUR).

Tài liệu tham khảo:
[3] D. J. A. Welsh and M. B. Powell, "An upper bound for the chromatic number of
    a graph and its application to timetabling problems", The Computer Journal,
    Vol. 10, No. 1, pp. 85-86, 1967.

Nguyên lý và phân tích trên Đồ thị Sudoku:
1. Thuật toán Welsh-Powell sắp xếp các đỉnh theo thứ tự giảm dần của bậc:
   deg(v_1) >= deg(v_2) >= ... >= deg(v_n).
2. Tuy nhiên, đồ thị Sudoku là đồ thị chính quy bậc 20 (20-regular graph), tức là:
   deg(v) = 20 với mọi v thuộc V.
   Do đó, tiêu chí sắp xếp bậc bị thoái hóa hoàn toàn (tất cả 81 đỉnh có bậc như nhau).
3. Khi áp dụng cho bài toán Mở rộng tiền tô màu (Pre-coloring Extension), thuật toán
   gán màu tham lam theo thứ tự cố định. Do không có cơ chế quay lui (Backtracking),
   thuật toán rất dễ rơi vào tình trạng bế tắc (Deadlock - không còn màu hợp lệ nào
   trong tập {1..9}) hoặc buộc phải dùng màu thứ 10 trở lên.
4. Thuật toán này đóng vai trò đối chứng mẫu mực chứng minh hạn chế của tham lam tĩnh.
"""

import time
from typing import List, Dict, Set, Tuple, Optional
from Source.core.sudoku_graph import SudokuGraph


class WelshPowellSolver:
    """
    Bộ giải Sudoku sử dụng thuật toán tô màu Welsh-Powell thuần túy (Tham lam theo bậc).
    Hỗ trợ ghi nhận vết từng bước (Step-by-step trace) phục vụ trực quan hóa (TV4)
    và đo đạc chỉ số thực nghiệm (TV5).
    """

    def __init__(self, graph: SudokuGraph, tie_breaker: str = "index"):
        """
        Khởi tạo bộ giải Welsh-Powell.
        :param graph: Đối tượng SudokuGraph chứa trạng thái bàn cờ ban đầu.
        :param tie_breaker: Tiêu chí phá vỡ thế hòa khi các đỉnh cùng bậc 20:
                           - "index": Theo chỉ số đỉnh tăng dần 0..80.
                           - "precolored_neighbors": Ưu tiên đỉnh có nhiều lân cận đã có màu.
        """
        self.graph: SudokuGraph = graph
        self.tie_breaker: str = tie_breaker
        self.steps_history: List[Dict] = []
        self.execution_time_ms: float = 0.0

    def get_vertex_ordering(self) -> List[int]:
        """
        Xác định thứ tự duyệt đỉnh của Welsh-Powell.
        Lấy danh sách các đỉnh chưa tô và sắp xếp theo:
        1. Bậc giảm dần (trong Sudoku mọi đỉnh đều có deg = 20).
        2. Tiêu chí phá vỡ thế hòa (tie_breaker).
        """
        uncolored = self.graph.get_uncolored_vertices()

        if self.tie_breaker == "precolored_neighbors":
            # Tiêu chí phụ: Đỉnh có nhiều đỉnh kề đã tô màu hơn sẽ được duyệt trước
            def sort_key(v: int):
                colored_nbrs = sum(1 for nbr in self.graph.get_neighbors(v) if self.graph.colors[nbr] != 0)
                return (self.graph.get_degree(v), colored_nbrs, -v)
            return sorted(uncolored, key=sort_key, reverse=True)
        else:
            # Sắp xếp theo bậc giảm dần, tie-break theo chỉ số tăng dần
            return sorted(uncolored, key=lambda v: (-self.graph.get_degree(v), v))

    def solve(self) -> Dict:
        """
        Thực hiện giải Sudoku bằng thuật toán Welsh-Powell.
        
        Trả về từ điển kết quả chứa:
        - status: "SUCCESS" nếu tô kín 81 đỉnh bằng 9 màu, hoặc "DEADLOCK" nếu thất bại.
        - execution_time_ms: Thời gian chạy tính bằng mili-giây.
        - total_steps: Tổng số bước gán màu đã thực hiện.
        - colored_count: Số ô đã được tô màu thành công.
        - remaining_uncolored: Số ô còn trống chưa thể gán màu.
        - deadlock_info: Thông tin chi tiết đỉnh bị bế tắc (nếu thất bại).
        - steps: Danh sách các bước để phục vụ trực quan hóa.
        """
        self.steps_history = []
        start_time = time.perf_counter()

        # Kiểm tra tính hợp lệ của trạng thái tiền tô màu ban đầu
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

        # 1. Xác định thứ tự duyệt đỉnh theo nguyên lý Welsh-Powell
        vertex_order = self.get_vertex_ordering()
        deadlock_info = None

        # 2. Duyệt tuần tự từng đỉnh theo thứ tự đã sắp và gán màu nhỏ nhất hợp lệ
        for step_idx, v in enumerate(vertex_order, start=1):
            r, c = SudokuGraph.index_to_coords(v)
            available = self.graph.get_available_colors(v)
            sat_deg = self.graph.get_saturation_degree(v)

            if not available:
                # Ngõ cụt (Deadlock): Cả 9 màu đều đã bị 20 đỉnh kề chiếm giữ!
                used_colors = sorted(list(self.graph.PALETTE - available))
                deadlock_info = {
                    "vertex": v,
                    "row": r,
                    "col": c,
                    "degree": self.graph.get_degree(v),
                    "saturation_degree": sat_deg,
                    "used_colors_in_neighbors": used_colors,
                    "step_failed": step_idx,
                    "reason": (
                        f"Tại bước {step_idx}, ô ({r + 1}, {c + 1}) [đỉnh {v}] có Bậc bão hòa = {sat_deg}/9. "
                        f"Toàn bộ 9 màu đều đã xuất hiện ở 20 đỉnh kề lân cận. "
                        f"Thuật toán Welsh-Powell tham lam tĩnh không có cơ chế quay lui nên rơi vào bế tắc."
                    )
                }
                self.steps_history.append({
                    "step": step_idx,
                    "action": "DEADLOCK",
                    "vertex": v,
                    "row": r,
                    "col": c,
                    "degree": self.graph.get_degree(v),
                    "saturation_degree": sat_deg,
                    "available_colors": [],
                    "assigned_color": None
                })
                break

            # Chọn màu nhỏ nhất khả dụng trong tập {1..9} (Quy tắc Greedy First-Fit)
            chosen_color = min(available)
            self.graph.assign_color(v, chosen_color)

            self.steps_history.append({
                "step": step_idx,
                "action": "ASSIGN",
                "vertex": v,
                "row": r,
                "col": c,
                "degree": self.graph.get_degree(v),
                "saturation_degree": sat_deg,
                "available_colors": sorted(list(available)),
                "assigned_color": chosen_color
            })

        self.execution_time_ms = (time.perf_counter() - start_time) * 1000.0
        is_complete = self.graph.is_complete()

        status = "SUCCESS" if is_complete else "DEADLOCK"
        msg = (
            "Giải thành công bằng Welsh-Powell!"
            if is_complete
            else "Welsh-Powell thất bại do rơi vào bế tắc (Deadlock) của tham lam tĩnh."
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
