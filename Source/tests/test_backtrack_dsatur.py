import sys
import os
import time

# Thêm đường dẫn gốc dự án để import module
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from Source.core.sudoku_graph import SudokuGraph
from Source.algorithms.backtrack_dsatur import BacktrackDSATURSolver


def run_puzzle_tests():
    puzzle_files = [
        ("Dễ (Easy)", "Release/puzzles/sample_easy.txt"),
        ("Trung bình (Medium)", "Release/puzzles/sample_medium.txt"),
        ("Khó (Hard)", "Release/puzzles/sample_hard.txt"),
        ("Chuyên gia (Expert)", "Release/puzzles/sample_expert.txt"),
    ]

    print("=" * 75)
    print("KIỂM THỬ THUẬT TOÁN BACKTRACKING + FORWARD CHECKING + DSATUR (TV3)")
    print("=" * 75)

    for level_name, file_path in puzzle_files:
        if not os.path.exists(file_path):
            print(f"[CẢNH BÁO] Không tìm thấy file: {file_path}")
            continue

        # Lọc bỏ các dòng comment bắt đầu bằng '#' trước khi ghép chuỗi 81 ký tự
        with open(file_path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip() and not line.strip().startswith("#")]
            puzzle_str = "".join(lines)

        graph = SudokuGraph()
        graph.load_from_string(puzzle_str)

        solver = BacktrackDSATURSolver(graph, record_steps=False)
        start_time = time.perf_counter()
        result = solver.solve()
        elapsed_ms = (time.perf_counter() - start_time) * 1000

        status = "THÀNH CÔNG" if (result["solved"] and graph.is_complete()) else "THẤT BẠI"
        print(
            f"- {level_name:<20} | Trạng thái: {status:<10} | "
            f"Bước thử: {result['steps']:<5} | Quay lui: {result['backtracks']:<4} | "
            f"Thời gian: {elapsed_ms:.2f} ms"
        )

    print("=" * 75)


if __name__ == "__main__":
    run_puzzle_tests()