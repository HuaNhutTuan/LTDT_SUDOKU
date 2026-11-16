"""
Mô-đun cài đặt thuật toán Quay lui kết hợp Forward Checking và Heuristic DSATUR/MRV.
Phụ trách: Kiều Gia Bảo (Quay lui + DSATUR & Bộ sinh đề).
"""

from typing import Dict, List, Set, Tuple, Optional
from Source.core.sudoku_graph import SudokuGraph


class BacktrackDSATURSolver:
    """
    Bộ giải Sudoku bằng thuật toán Quay lui có định hướng (Backtracking)
    kết hợp Kiểm tra tiến (Forward Checking) và chọn đỉnh theo DSATUR / MRV.
    """

    def __init__(self, graph: SudokuGraph, record_steps: bool = False):
        self.graph = graph
        self.record_steps = record_steps  # Bật True khi chạy chế độ trực quan GUI
        
        # Các chỉ số thống kê phục vụ Benchmark (TV5)
        self.steps_count: int = 0         # Tổng số lần gán thử màu
        self.backtracks_count: int = 0    # Tổng số lần quay lui (ngõ cụt)
        self.history: List[Dict] = []     # Lưu vết từng bước cho GUI (TV4)

    def _init_domains(self) -> Optional[Dict[int, Set[int]]]:
        """
        Khởi tạo miền màu khả dụng (Domain) cho tất cả các đỉnh chưa tô.
        Trả về None nếu phát hiện đỉnh trống nào đó không còn màu hợp lệ ngay từ đầu.
        """
        domains: Dict[int, Set[int]] = {}
        for v in self.graph.get_uncolored_vertices():
            avail = self.graph.get_available_colors(v)
            if not avail:
                return None  # Bế tắc ngay từ đầu
            domains[v] = avail
        return domains

    def _select_next_vertex(self, domains: Dict[int, Set[int]]) -> int:
        """
        Chọn đỉnh chưa tô tiếp theo theo tiêu chuẩn kép DSATUR + MRV:
        1. Ưu tiên đỉnh có bậc bão hòa (Saturation Degree) LỚN NHẤT.
        2. Nếu bằng nhau, ưu tiên đỉnh có miền màu khả dụng (MRV) NHỎ NHẤT.
        """
        return max(
            domains.keys(),
            key=lambda v: (self.graph.get_saturation_degree(v), -len(domains[v]))
        )

    def _forward_check(
        self, vertex: int, color: int, domains: Dict[int, Set[int]]
    ) -> Tuple[bool, List[int]]:
        """
        Kiểm tra tiến (Forward Checking):
        Loại bỏ `color` khỏi miền màu khả dụng của các đỉnh kề chưa tô.
        Trả về (True, danh_sách_đỉnh_bị_xóa_màu) nếu hợp lệ.
        Trả về (False, danh_sách_đã_sửa) nếu có đỉnh kề bị rỗng miền màu -> Cắt tỉa ngay!
        """
        pruned_neighbors: List[int] = []
        for nbr in self.graph.adjacency_list[vertex]:
            if nbr in domains and color in domains[nbr]:
                domains[nbr].remove(color)
                pruned_neighbors.append(nbr)
                if len(domains[nbr]) == 0:
                    return False, pruned_neighbors  # Phát hiện ngõ cụt sớm!
        return True, pruned_neighbors

    def _restore_domains(
        self, color: int, pruned_neighbors: List[int], domains: Dict[int, Set[int]]
    ) -> None:
        """Khôi phục lại màu vào miền giá trị của các đỉnh kề khi quay lui."""
        for nbr in pruned_neighbors:
            domains[nbr].add(color)

    def solve(self) -> Dict:
        """
        Hàm thực thi chính giải đồ thị Sudoku.
        Trả về từ điển kết quả gồm trạng thái thành công và các chỉ số đo lường.
        """
        self.steps_count = 0
        self.backtracks_count = 0
        self.history.clear()

        domains = self._init_domains()
        if domains is None:
            return {
                "solved": False,
                "steps": 0,
                "backtracks": 0,
                "history": self.history
            }

        is_solved = self._backtrack(domains)
        return {
            "solved": is_solved,
            "steps": self.steps_count,
            "backtracks": self.backtracks_count,
            "history": self.history
        }

    def _backtrack(self, domains: Dict[int, Set[int]]) -> bool:
        # Điều kiện dừng: Không còn đỉnh nào chưa tô màu
        if not domains:
            return True

        # Bước 1: Chọn đỉnh tối ưu theo DSATUR / MRV
        v = self._select_next_vertex(domains)
        current_domain = sorted(list(domains[v]))
        del domains[v]  # Tạm đưa v ra khỏi tập đỉnh chưa tô

        # Bước 2: Thử lần lượt từng màu khả dụng
        for color in current_domain:
            self.steps_count += 1
            self.graph.assign_color(v, color)

            if self.record_steps:
                self.history.append({"action": "assign", "vertex": v, "color": color})

            # Bước 3: Kiểm tra tiến (Forward Checking)
            is_valid, pruned = self._forward_check(v, color, domains)
            if is_valid:
                if self._backtrack(domains):
                    return True

            # Bước 4: Cắt tỉa / Quay lui (Backtrack)
            self._restore_domains(color, pruned, domains)
            self.graph.unassign_color(v)
            self.backtracks_count += 1

            if self.record_steps:
                self.history.append({"action": "backtrack", "vertex": v, "color": 0})

        # Đưa đỉnh v trở lại danh sách chưa tô trước khi lùi về nhánh cha
        domains[v] = set(current_domain)
        return False