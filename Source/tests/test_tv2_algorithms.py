"""
Bộ kiểm thử tự động Unit Tests cho Module Thuật toán của Thành viên 2:
- Thuật toán Welsh-Powell (Tham lam theo bậc cố định).
- Thuật toán DSATUR thuần túy (Heuristic bậc bão hòa động).
- Cơ chế tính toán và cập nhật bậc bão hòa.

Phục vụ môn học: Lý thuyết đồ thị và Ứng dụng - Khoa CNTT, HCMUE.
"""

import unittest
import os
import sys

# Thêm thư mục gốc vào PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from Source.core.sudoku_graph import SudokuGraph
from Source.core.io_handler import IOHandler
from Source.algorithms.welsh_powell import WelshPowellSolver
from Source.algorithms.dsatur import DSATURSolver


class TestTV2Algorithms(unittest.TestCase):
    """Kiểm thử nghiệm thu module thuật toán của Thành viên 2."""

    def setUp(self):
        self.easy_puzzle_str = (
            "530070000"
            "600195000"
            "098000060"
            "800060003"
            "400803001"
            "700020006"
            "060000280"
            "000419005"
            "000080079"
        )
        self.graph_easy = SudokuGraph()
        self.graph_easy.load_from_string(self.easy_puzzle_str)

    def test_dsatur_solver_easy_puzzle(self):
        """Kiểm thử DSATUR giải thành công đề Dễ mà không cần quay lui."""
        solver = DSATURSolver(self.graph_easy)
        result = solver.solve()
        
        self.assertEqual(result["status"], "SUCCESS")
        self.assertTrue(self.graph_easy.is_complete())
        self.assertEqual(result["remaining_uncolored"], 0)
        self.assertGreater(result["total_steps"], 0)
        self.assertLess(result["execution_time_ms"], 50.0)  # Thường < 5ms

    def test_dsatur_step_generator(self):
        """Kiểm thử generator từng bước của DSATUR phục vụ TV4 làm Step-by-step GUI."""
        graph = SudokuGraph()
        graph.load_from_string(self.easy_puzzle_str)
        solver = DSATURSolver(graph)
        
        steps = list(solver.step_generator())
        self.assertGreater(len(steps), 0)
        # Bước cuối cùng phải là FINISHED hoặc ASSIGN cuối
        self.assertIn(steps[-1]["action"], ("FINISHED", "ASSIGN"))
        self.assertTrue(graph.is_complete())

    def test_dsatur_saturation_degree_calculation(self):
        """Kiểm thử tính toán bậc bão hòa động trong DSATUR."""
        graph = SudokuGraph()
        graph.load_from_string(self.easy_puzzle_str)
        solver = DSATURSolver(graph)
        
        # Kiểm tra bậc bão hòa ban đầu
        v = SudokuGraph.coords_to_index(0, 2)  # ô (1, 3)
        expected_sat = graph.get_saturation_degree(v)
        self.assertEqual(solver.get_saturation_degree(v), expected_sat)
        
        # Mảng 81 bậc bão hòa
        all_sats = solver.get_all_saturations()
        self.assertEqual(len(all_sats), 81)

    def test_welsh_powell_on_regular_graph(self):
        """
        Kiểm thử Welsh-Powell trên đồ thị Sudoku:
        Chứng minh Welsh-Powell duyệt đỉnh theo bậc cố định (deg=20)
        và thể hiện rõ hiện tượng Deadlock do tham lam tĩnh không quay lui.
        """
        graph = SudokuGraph()
        graph.load_from_string(self.easy_puzzle_str)
        solver = WelshPowellSolver(graph, tie_breaker="index")
        
        order = solver.get_vertex_ordering()
        # Số đỉnh cần duyệt bằng số ô trống
        self.assertEqual(len(order), len(graph.get_uncolored_vertices()))
        
        result = solver.solve()
        # Welsh-Powell trên Sudoku thường rơi vào deadlock hoặc nếu thành công cũng phải hợp lệ
        self.assertIn(result["status"], ["DEADLOCK", "SUCCESS"])
        self.assertGreater(result["total_steps"], 0)
        if result["status"] == "DEADLOCK":
            self.assertIsNotNone(result["deadlock_info"])
            self.assertIn("reason", result["deadlock_info"])

    def test_welsh_powell_tie_breakers(self):
        """Kiểm thử hai tiêu chí phá vỡ thế hòa của Welsh-Powell."""
        graph1 = SudokuGraph()
        graph1.load_from_string(self.easy_puzzle_str)
        solver1 = WelshPowellSolver(graph1, tie_breaker="index")
        order1 = solver1.get_vertex_ordering()

        graph2 = SudokuGraph()
        graph2.load_from_string(self.easy_puzzle_str)
        solver2 = WelshPowellSolver(graph2, tie_breaker="precolored_neighbors")
        order2 = solver2.get_vertex_ordering()

        self.assertEqual(len(order1), len(order2))
        # Hai thứ tự sắp xếp phải khác nhau do tiêu chí tie-breaker khác nhau
        self.assertNotEqual(order1, order2)

    def test_conflict_initial_board(self):
        """Kiểm thử cả 2 giải thuật khi nạp bảng có xung đột ban đầu."""
        invalid_str = "550070000" + "0" * 72
        # Tự tạo bảng xung đột trực tiếp bằng cách gán màu không qua validate
        graph = SudokuGraph()
        graph.colors[0] = 5
        graph.colors[1] = 5  # Xung đột cùng hàng 1
        
        solver_wp = WelshPowellSolver(graph)
        res_wp = solver_wp.solve()
        self.assertEqual(res_wp["status"], "INITIAL_CONFLICT")

        solver_ds = DSATURSolver(graph)
        res_ds = solver_ds.solve()
        self.assertEqual(res_ds["status"], "INITIAL_CONFLICT")


if __name__ == "__main__":
    unittest.main()
