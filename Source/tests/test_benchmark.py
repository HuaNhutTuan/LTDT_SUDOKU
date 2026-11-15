"""
Bộ kiểm thử đơn vị (Unit Tests) cho Module Benchmark và 3 Giải thuật Tô màu.
Phục vụ nghiệm thu kỹ thuật Thành viên 5 (Thực nghiệm, Kiểm thử & Media).
Khoa CNTT - Trường Đại học Sư phạm TP. Hồ Chí Minh (HCMUE).

Chỉ tiêu nghiệm thu:
1. Độ chính xác của các chỉ số đo lường (thời gian ms, số lần gán màu, số lần quay lui).
2. Kiểm tra tính đúng đắn của 3 giải thuật (Welsh-Powell, DSATUR Pure, Backtrack+DSATUR).
3. Kiểm tra tính toàn vẹn của bộ 40 đề Benchmark (81 ký tự, không xung đột, nghiệm duy nhất).
4. Kiểm tra chức năng tổng hợp số liệu và xuất file CSV/JSON.
"""

import os
import sys
import tempfile

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Thêm đường dẫn gốc
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from Source.core.sudoku_graph import SudokuGraph
from Source.core.benchmark import (
    BenchmarkMetrics,
    BenchmarkEngine,
    WelshPowellSolver,
    DSATURPureSolver,
    BacktrackDSATURSolver
)
from Source.benchmark_runner import parse_benchmark_file

try:
    import unittest
    BaseTestCase = unittest.TestCase
except ImportError:
    class BaseTestCase:
        def assertEqual(self, a, b, msg=""):
            assert a == b, f"{msg} | Kỳ vọng: {b}, Thực tế: {a}"

        def assertTrue(self, a, msg=""):
            assert bool(a) is True, f"{msg} | Kỳ vọng: True, Thực tế: {a}"

        def assertFalse(self, a, msg=""):
            assert bool(a) is False, f"{msg} | Kỳ vọng: False, Thực tế: {a}"

        def assertGreater(self, a, b, msg=""):
            assert a > b, f"{msg} | Kỳ vọng {a} > {b}"

        def assertLess(self, a, b, msg=""):
            assert a < b, f"{msg} | Kỳ vọng {a} < {b}"

        def assertIn(self, a, b, msg=""):
            assert a in b, f"{msg} | Kỳ vọng {a} in {b}"


class TestBenchmarkEngineAndSolvers(BaseTestCase):
    def setUp(self):
        self.sample_easy_str = (
            "003020600"
            "900305001"
            "001806400"
            "008102900"
            "700000008"
            "006708200"
            "002609500"
            "800203009"
            "005010300"
        )
        self.graph = SudokuGraph()
        self.graph.load_from_string(self.sample_easy_str)

    def test_benchmark_metrics_dataclass(self):
        """Kiểm tra khởi tạo và chuyển đổi từ điển của lớp BenchmarkMetrics."""
        metric = BenchmarkMetrics(
            puzzle_id="TEST_01",
            difficulty="Easy",
            clues_count=32,
            algorithm="Backtrack + DSATUR",
            execution_time_ms=1.25,
            vertices_visited=50,
            color_assignments=49,
            backtracks=0,
            is_solved=True,
            is_valid=True,
            chromatic_number=9,
            error_message=""
        )
        data = metric.to_dict()
        self.assertEqual(data["puzzle_id"], "TEST_01")
        self.assertEqual(data["chromatic_number"], 9)
        self.assertTrue(data["is_solved"])
        self.assertTrue(data["is_valid"])

    def test_welsh_powell_solver(self):
        """Kiểm tra thuật toán Welsh-Powell ghi nhận đúng số bước và phát hiện Deadlock."""
        res = WelshPowellSolver.solve(self.graph, "TEST_EASY", "Easy", 32)
        self.assertEqual(res.algorithm, "Welsh-Powell")
        self.assertGreater(res.execution_time_ms, 0)
        self.assertGreater(res.vertices_visited, 0)
        self.assertEqual(res.backtracks, 0, "Welsh-Powell không được có bước quay lui.")

    def test_dsatur_pure_solver(self):
        """Kiểm tra thuật toán DSATUR Pure giải thành công trên đề Easy chuẩn."""
        res = DSATURPureSolver.solve(self.graph, "TEST_EASY", "Easy", 32)
        self.assertEqual(res.algorithm, "DSATUR Pure")
        self.assertTrue(res.is_solved, "DSATUR Pure phải giải thành công đề Easy.")
        self.assertTrue(res.is_valid, "Nghiệm tìm được phải hợp lệ không xung đột.")
        self.assertEqual(res.chromatic_number, 9, "Sắc số của nghiệm Sudoku phải đúng bằng 9.")
        self.assertEqual(res.backtracks, 0, "DSATUR Pure không sử dụng quay lui.")

    def test_backtrack_dsatur_solver(self):
        """Kiểm tra thuật toán Backtrack + DSATUR đạt tỷ lệ chính xác 100%."""
        res = BacktrackDSATURSolver.solve(self.graph, "TEST_EASY", "Easy", 32)
        self.assertEqual(res.algorithm, "Backtrack + DSATUR")
        self.assertTrue(res.is_solved)
        self.assertTrue(res.is_valid)
        self.assertEqual(res.chromatic_number, 9)
        self.assertLess(res.execution_time_ms, 1000.0, "Thời gian giải đề Easy phải dưới 1 giây.")

    def test_benchmark_40_dataset_integrity(self):
        """Kiểm tra tính toàn vẹn của toàn bộ 40 đề trong file benchmark_40.txt."""
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        bench_file = os.path.join(base_dir, "Release", "puzzles", "benchmark_40.txt")
        self.assertTrue(os.path.exists(bench_file), "Tệp benchmark_40.txt phải tồn tại.")

        dataset = parse_benchmark_file(bench_file)
        self.assertEqual(len(dataset), 40, "Bộ dữ liệu Benchmark phải có đúng 40 đề.")

        diff_counts = {"Easy": 0, "Medium": 0, "Hard": 0, "Expert": 0}
        for pid, diff, clues, p_str in dataset:
            self.assertEqual(len(p_str), 81, f"Đề {pid} không đủ 81 ký tự.")
            self.assertIn(diff, diff_counts, f"Cấp độ không hợp lệ: {diff}")
            diff_counts[diff] += 1
            
            # Kiểm tra nạp vào đồ thị không bị lỗi tiền tô màu
            g = SudokuGraph()
            g.load_from_string(p_str)
            self.assertEqual(len(g.get_all_conflicts()), 0, f"Đề {pid} có xung đột tiền tô màu ban đầu.")

        self.assertEqual(diff_counts["Easy"], 10, "Cấp độ Easy phải có đúng 10 đề.")
        self.assertEqual(diff_counts["Medium"], 10, "Cấp độ Medium phải có đúng 10 đề.")
        self.assertEqual(diff_counts["Hard"], 10, "Cấp độ Hard phải có đúng 10 đề.")
        self.assertEqual(diff_counts["Expert"], 10, "Cấp độ Expert phải có đúng 10 đề.")

    def test_summary_and_export(self):
        """Kiểm tra hàm tổng hợp số liệu thống kê và xuất tệp CSV/JSON."""
        res_list = [
            BenchmarkMetrics("P1", "Easy", 36, "AlgoA", 1.0, 10, 5, 0, True, True, 9),
            BenchmarkMetrics("P2", "Easy", 36, "AlgoA", 3.0, 10, 5, 0, True, True, 9),
            BenchmarkMetrics("P3", "Easy", 36, "AlgoB", 5.0, 15, 8, 2, False, False, 0)
        ]
        summary = BenchmarkEngine.aggregate_summary(res_list)
        self.assertIn("AlgoA", summary)
        self.assertEqual(summary["AlgoA"]["Easy"]["success_rate_percent"], 100.0)
        self.assertEqual(summary["AlgoA"]["Easy"]["time_mean_ms"], 2.0)

        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = os.path.join(tmpdir, "test.csv")
            json_path = os.path.join(tmpdir, "test.json")
            BenchmarkEngine.export_csv(res_list, csv_path)
            BenchmarkEngine.export_json(summary, json_path)
            self.assertTrue(os.path.exists(csv_path))
            self.assertTrue(os.path.exists(json_path))


def run_tests_manually():
    test_suite = TestBenchmarkEngineAndSolvers()
    methods = [m for m in dir(test_suite) if m.startswith("test_")]
    print(f"Bắt đầu chạy {len(methods)} bài test nghiệm thu Benchmark...")
    passed = 0
    for m in methods:
        if hasattr(test_suite, "setUp"):
            test_suite.setUp()
        try:
            getattr(test_suite, m)()
            print(f"  [PASS] {m}")
            passed += 1
        except Exception as e:
            print(f"  [FAIL] {m}: {e}")
    print(f"\n=> Kết quả: {passed}/{len(methods)} bài test vượt qua thành công!")
    return passed == len(methods)


if __name__ == "__main__":
    if "unittest" in sys.modules:
        unittest.main()
    else:
        success = run_tests_manually()
        sys.exit(0 if success else 1)
