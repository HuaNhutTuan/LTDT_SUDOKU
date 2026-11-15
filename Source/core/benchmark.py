"""
Mô-đun Benchmark & Performance Tracker - Đo lường và đánh giá hiệu năng giải thuật.
Phục vụ môn học: Lý thuyết đồ thị và Ứng dụng - Khoa CNTT, HCMUE.
Phụ trách: Thành viên 5 (Thực nghiệm, Kiểm thử & Media).

Các chỉ số đo lường cốt lõi:
1. Thời gian thực thi (Execution Time): tính bằng mili-giây (ms) với độ phân giải nano-giây qua time.perf_counter().
2. Số bước gán màu (Color Assignments): tổng số lần một đỉnh được gán màu hợp lệ.
3. Số đỉnh đã duyệt (Vertices Visited): số lần thuật toán thăm/kiểm tra một đỉnh trong quá trình tìm kiếm.
4. Số lần quay lui (Backtracks): số lần thuật toán phải hủy màu và thử nhánh khác do rơi vào nhánh cụt.
5. Tỷ lệ giải thành công (Success Rate): % số đề giải ra nghiệm hợp lệ mà không bế tắc hoặc vượt quá 9 màu.
6. Sắc số đạt được (Chromatic Number chi(G)): kiểm tra nghiệm có đúng 9 màu C = {1..9}.
"""

import time
import csv
import json
import os
from dataclasses import dataclass, asdict
from typing import List, Dict, Tuple, Optional, Set
from .sudoku_graph import SudokuGraph


@dataclass
class BenchmarkMetrics:
    """Lớp lưu trữ kết quả đo lường cho một lượt giải đề bài."""
    puzzle_id: str
    difficulty: str
    clues_count: int
    algorithm: str
    execution_time_ms: float
    vertices_visited: int
    color_assignments: int
    backtracks: int
    is_solved: bool
    is_valid: bool
    chromatic_number: int
    error_message: str = ""

    def to_dict(self) -> Dict:
        return asdict(self)


class WelshPowellSolver:
    """
    Thuật toán Welsh-Powell (1967) mở rộng cho bài toán Pre-coloring Extension.
    - Cơ chế: Sắp xếp các đỉnh chưa tô theo thứ tự giảm dần của bậc ràng buộc
      (ở đây là số đỉnh kề đã có màu hoặc số đỉnh kề tự do). Sau đó duyệt tuần tự
      và gán tham lam màu hợp lệ nhỏ nhất trong {1..9}.
    - Vai trò đối chứng: Chứng minh giới hạn của thuật toán tham lam tĩnh trên đồ thị
      chính quy bậc 20 (20-regular) khi có tiền tô màu (dễ dẫn đến Deadlock vì thiếu 9 màu).
    """

    @staticmethod
    def solve(graph: SudokuGraph, puzzle_id: str = "P", difficulty: str = "N/A", clues_count: int = 0) -> BenchmarkMetrics:
        g = graph.clone()
        start_time = time.perf_counter()
        
        # Lấy các đỉnh chưa tô
        uncolored = [v for v in range(SudokuGraph.NUM_VERTICES) if g.colors[v] == 0]
        # Sắp xếp các đỉnh theo số đỉnh kề đã có màu giảm dần (mức độ ràng buộc tĩnh)
        uncolored.sort(key=lambda v: len([nbr for nbr in g.get_neighbors(v) if g.colors[nbr] != 0]), reverse=True)
        
        visited = 0
        assignments = 0
        backtracks = 0
        error_msg = ""
        is_solved = False

        for v in uncolored:
            visited += 1
            available = g.get_available_colors(v)
            if not available:
                error_msg = f"Deadlock tại đỉnh {v}: không còn màu hợp lệ trong tập {{1..9}}."
                break
            # Gán màu nhỏ nhất khả dụng
            chosen_color = min(available)
            g.assign_color(v, chosen_color)
            assignments += 1

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        is_solved = (error_msg == "") and g.is_complete()
        is_valid = is_solved and (len(g.get_all_conflicts()) == 0)
        chromatic_num = len(set(g.colors)) if is_solved else 0

        return BenchmarkMetrics(
            puzzle_id=puzzle_id,
            difficulty=difficulty,
            clues_count=clues_count,
            algorithm="Welsh-Powell",
            execution_time_ms=round(elapsed_ms, 3),
            vertices_visited=visited,
            color_assignments=assignments,
            backtracks=backtracks,
            is_solved=is_solved,
            is_valid=is_valid,
            chromatic_number=chromatic_num,
            error_message=error_msg
        )


class DSATURPureSolver:
    """
    Thuật toán DSATUR thuần túy (Brélaz, 1979 - Không dùng quay lui).
    - Cơ chế: Tại mỗi bước, chọn đỉnh chưa tô có BẬC BÃO HÒA lớn nhất (saturation degree);
      nếu có nhiều đỉnh bằng nhau, ưu tiên đỉnh có số đỉnh kề chưa tô lớn nhất.
      Sau đó gán tham lam màu hợp lệ nhỏ nhất khả dụng.
    - Vai trò đối chứng: Minh họa sự vượt trội của Heuristic bão hòa động so với Welsh-Powell,
      giải quyết tốt các đề Dễ nhưng vẫn có khả năng bế tắc ở đề Khó/Chuyên gia nếu không quay lui.
    """

    @staticmethod
    def solve(graph: SudokuGraph, puzzle_id: str = "P", difficulty: str = "N/A", clues_count: int = 0) -> BenchmarkMetrics:
        g = graph.clone()
        start_time = time.perf_counter()

        uncolored = set(v for v in range(SudokuGraph.NUM_VERTICES) if g.colors[v] == 0)
        visited = 0
        assignments = 0
        backtracks = 0
        error_msg = ""

        while uncolored:
            visited += 1
            best_v = None
            max_sat = -1
            max_uncolored_deg = -1

            # Tìm đỉnh có bậc bão hòa lớn nhất
            for v in uncolored:
                sat = g.get_saturation_degree(v)
                uncolored_deg = len([nbr for nbr in g.get_neighbors(v) if g.colors[nbr] == 0])
                if sat > max_sat or (sat == max_sat and uncolored_deg > max_uncolored_deg):
                    max_sat = sat
                    max_uncolored_deg = uncolored_deg
                    best_v = v

            available = g.get_available_colors(best_v)
            if not available:
                error_msg = f"Deadlock tại đỉnh {best_v} (bậc bão hòa {max_sat}): 0 màu khả dụng."
                break

            chosen_color = min(available)
            g.assign_color(best_v, chosen_color)
            assignments += 1
            uncolored.remove(best_v)

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        is_solved = (error_msg == "") and g.is_complete()
        is_valid = is_solved and (len(g.get_all_conflicts()) == 0)
        chromatic_num = len(set(g.colors)) if is_solved else 0

        return BenchmarkMetrics(
            puzzle_id=puzzle_id,
            difficulty=difficulty,
            clues_count=clues_count,
            algorithm="DSATUR Pure",
            execution_time_ms=round(elapsed_ms, 3),
            vertices_visited=visited,
            color_assignments=assignments,
            backtracks=backtracks,
            is_solved=is_solved,
            is_valid=is_valid,
            chromatic_number=chromatic_num,
            error_message=error_msg
        )


class BacktrackDSATURSolver:
    """
    Thuật toán Backtracking kết hợp Forward Checking và Heuristic DSATUR / MRV.
    - Cơ chế: Định hướng tìm kiếm bằng cách luôn chọn ô có miền màu khả dụng nhỏ nhất (MRV)
      hoặc bậc bão hòa lớn nhất; cắt tỉa nhánh ngay khi phát hiện ô láng giềng bị triệt tiêu màu.
    - Vai trò chính: Thuật toán toàn vẹn, cam kết tìm ra lời giải chính xác 100% cho mọi đề hợp lệ
      với số lần quay lui và thời gian thực thi tối ưu nhất.
    """

    @staticmethod
    def solve(graph: SudokuGraph, puzzle_id: str = "P", difficulty: str = "N/A", clues_count: int = 0) -> BenchmarkMetrics:
        g = graph.clone()
        adj = g.adjacency_list
        working_colors = list(g.colors)
        palette = SudokuGraph.PALETTE

        visited = 0
        assignments = 0
        backtracks = 0
        start_time = time.perf_counter()

        def backtrack() -> bool:
            nonlocal visited, assignments, backtracks
            visited += 1

            # Áp dụng chiến lược MRV (Minimum Remaining Values - tương đương DSATUR)
            best_v = -1
            best_avail = None
            min_avail_count = 10

            for v in range(SudokuGraph.NUM_VERTICES):
                if working_colors[v] == 0:
                    used = {working_colors[nbr] for nbr in adj[v] if working_colors[nbr] != 0}
                    avail = palette - used
                    cnt = len(avail)
                    if cnt == 0:
                        # Cắt tỉa tiến (Forward Checking): Có ô bị bế tắc, nhánh này vô nghiệm
                        return False
                    if cnt < min_avail_count:
                        min_avail_count = cnt
                        best_v = v
                        best_avail = avail
                        if cnt == 1:
                            break  # Tối ưu: Nếu chỉ còn 1 màu duy nhất thì chốt ngay

            if best_v == -1:
                return True  # Toàn bộ 81 đỉnh đã được tô màu hợp lệ

            for c in sorted(best_avail):
                working_colors[best_v] = c
                assignments += 1
                if backtrack():
                    return True
                working_colors[best_v] = 0
                backtracks += 1

            return False

        is_solved = backtrack()
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        # Áp dụng nghiệm vào đồ thị
        if is_solved:
            for v in range(SudokuGraph.NUM_VERTICES):
                g.colors[v] = working_colors[v]

        is_valid = is_solved and (len(g.get_all_conflicts()) == 0) and g.is_complete()
        chromatic_num = len(set(working_colors)) if is_solved else 0

        return BenchmarkMetrics(
            puzzle_id=puzzle_id,
            difficulty=difficulty,
            clues_count=clues_count,
            algorithm="Backtrack + DSATUR",
            execution_time_ms=round(elapsed_ms, 3),
            vertices_visited=visited,
            color_assignments=assignments,
            backtracks=backtracks,
            is_solved=is_solved,
            is_valid=is_valid,
            chromatic_number=chromatic_num,
            error_message="" if is_solved else "Không tìm thấy lời giải hợp lệ."
        )


class BenchmarkEngine:
    """
    Bộ động cơ thực thi kiểm thử và tổng hợp số liệu thực nghiệm.
    """

    SOLVERS = {
        "Welsh-Powell": WelshPowellSolver.solve,
        "DSATUR Pure": DSATURPureSolver.solve,
        "Backtrack + DSATUR": BacktrackDSATURSolver.solve
    }

    @classmethod
    def run_single(cls, graph: SudokuGraph, puzzle_id: str, difficulty: str, clues_count: int, algorithm_name: str) -> BenchmarkMetrics:
        if algorithm_name not in cls.SOLVERS:
            raise ValueError(f"Thuật toán không hỗ trợ: {algorithm_name}")
        return cls.SOLVERS[algorithm_name](graph, puzzle_id, difficulty, clues_count)

    @classmethod
    def run_full_benchmark(cls, dataset: List[Tuple[str, str, int, str]], algorithms: Optional[List[str]] = None) -> List[BenchmarkMetrics]:
        """
        Chạy toàn bộ tập dữ liệu đề kiểm thử trên các thuật toán được chỉ định.
        dataset format: List of (puzzle_id, difficulty, clues_count, puzzle_string)
        """
        if algorithms is None:
            algorithms = list(cls.SOLVERS.keys())

        results: List[BenchmarkMetrics] = []
        for pid, diff, clues, p_str in dataset:
            g = SudokuGraph()
            g.load_from_string(p_str)
            for algo in algorithms:
                res = cls.run_single(g, pid, diff, clues, algo)
                results.append(res)

        return results

    @staticmethod
    def aggregate_summary(results: List[BenchmarkMetrics]) -> Dict:
        """
        Tính toán các chỉ số thống kê (Mean, Min, Max, Tỷ lệ thành công)
        phân nhóm theo Thuật toán và Cấp độ khó.
        """
        grouped: Dict[Tuple[str, str], List[BenchmarkMetrics]] = {}
        for r in results:
            key = (r.algorithm, r.difficulty)
            grouped.setdefault(key, []).append(r)

        summary: Dict[str, Dict] = {}
        for (algo, diff), metrics_list in grouped.items():
            total = len(metrics_list)
            solved = sum(1 for m in metrics_list if m.is_solved)
            success_rate = (solved / total * 100.0) if total > 0 else 0.0

            times = [m.execution_time_ms for m in metrics_list]
            assignments = [m.color_assignments for m in metrics_list]
            backtracks = [m.backtracks for m in metrics_list]
            visited = [m.vertices_visited for m in metrics_list]

            if algo not in summary:
                summary[algo] = {}

            summary[algo][diff] = {
                "total_puzzles": total,
                "solved_count": solved,
                "success_rate_percent": round(success_rate, 1),
                "time_mean_ms": round(sum(times) / total, 3),
                "time_min_ms": round(min(times), 3),
                "time_max_ms": round(max(times), 3),
                "assignments_mean": round(sum(assignments) / total, 1),
                "backtracks_mean": round(sum(backtracks) / total, 1),
                "visited_mean": round(sum(visited) / total, 1)
            }

        return summary

    @staticmethod
    def export_csv(results: List[BenchmarkMetrics], file_path: str) -> None:
        """Xuất toàn bộ kết quả chi tiết ra tệp CSV."""
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
        fieldnames = [
            "puzzle_id", "difficulty", "clues_count", "algorithm",
            "execution_time_ms", "vertices_visited", "color_assignments",
            "backtracks", "is_solved", "is_valid", "chromatic_number", "error_message"
        ]
        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for r in results:
                writer.writerow(r.to_dict())

    @staticmethod
    def export_json(summary: Dict, file_path: str) -> None:
        """Xuất bảng tổng hợp thống kê ra tệp JSON."""
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
