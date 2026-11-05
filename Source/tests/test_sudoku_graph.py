"""
Bộ kiểm thử đơn vị (Unit Tests) cho Lớp SudokuGraph và IOHandler.
Phục vụ nghiệm thu kỹ thuật Thành viên 1 (Nhóm trưởng) theo kế hoạch đồ án.
Chỉ tiêu nghiệm thu:
1. Đồ thị đúng 81 đỉnh, 810 cạnh.
2. Mỗi đỉnh có chính xác 20 đỉnh kề (20-regular graph).
3. Bắt lỗi chính xác các đề bài vi phạm luật tiền tô màu (trùng hàng, trùng cột, trùng khối 3x3).
4. Tính đúng bậc bão hòa (Saturation Degree) và tập màu khả dụng.
5. Đọc/ghi file đề bài chính xác.
"""

import unittest
import os
import tempfile
from Source.core.graph import Graph
from Source.core.sudoku_graph import SudokuGraph, PrecoloringConflictError
from Source.core.io_handler import IOHandler


class TestSudokuGraphCore(unittest.TestCase):
    def setUp(self):
        self.graph = SudokuGraph()

    def test_vertex_and_edge_counts(self):
        """Kiểm tra số lượng đỉnh và cạnh của đồ thị Sudoku."""
        self.assertEqual(self.graph.num_vertices, 81, "Đồ thị phải có đúng 81 đỉnh.")
        self.assertEqual(self.graph.num_edges, 810, "Đồ thị phải có đúng 810 cạnh vô hướng.")

    def test_20_regular_property(self):
        """Kiểm tra tính chất chính quy bậc 20: mọi đỉnh v thuộc V đều có bậc đúng 20."""
        is_regular, degree = self.graph.is_regular()
        self.assertTrue(is_regular, "Đồ thị Sudoku phải là đồ thị chính quy.")
        self.assertEqual(degree, 20, "Bậc của mọi đỉnh trong đồ thị Sudoku phải đúng 20.")
        
        for v in range(81):
            neighbors = self.graph.get_neighbors(v)
            self.assertEqual(len(neighbors), 20, f"Đỉnh {v} phải có đúng 20 đỉnh kề.")
            self.assertEqual(len(set(neighbors)), 20, f"Đỉnh {v} có đỉnh kề bị trùng lặp.")
            self.assertNotIn(v, neighbors, f"Đỉnh {v} không được tự kề với chính nó (không có khuyên).")

    def test_neighbor_composition_corner_cell(self):
        """
        Kiểm tra chi tiết 20 đỉnh kề của ô góc trên-trái (0, 0) - đỉnh 0:
        - 8 đỉnh cùng hàng 0: (0, 1) đến (0, 8)
        - 8 đỉnh cùng cột 0: (1, 0) đến (8, 0)
        - 4 đỉnh cùng khối 3x3 nhưng khác hàng/cột: (1,1), (1,2), (2,1), (2,2)
        """
        v0 = 0
        neighbors = set(self.graph.get_neighbors(v0))
        
        expected_row = {SudokuGraph.coords_to_index(0, c) for c in range(1, 9)}
        expected_col = {SudokuGraph.coords_to_index(r, 0) for r in range(1, 9)}
        expected_box_only = {
            SudokuGraph.coords_to_index(1, 1),
            SudokuGraph.coords_to_index(1, 2),
            SudokuGraph.coords_to_index(2, 1),
            SudokuGraph.coords_to_index(2, 2)
        }
        
        all_expected = expected_row | expected_col | expected_box_only
        self.assertEqual(len(all_expected), 20)
        self.assertEqual(neighbors, all_expected)

    def test_adjacency_matrix_properties(self):
        """Kiểm tra ma trận kề 81x81: đối xứng qua đường chéo chính, đường chéo bằng 0, tổng hàng = 20."""
        matrix = self.graph.adjacency_matrix
        self.assertEqual(len(matrix), 81)
        for i in range(81):
            self.assertEqual(len(matrix[i]), 81)
            self.assertEqual(matrix[i][i], 0, f"Đường chéo tại ({i}, {i}) phải bằng 0.")
            self.assertEqual(sum(matrix[i]), 20, f"Tổng hàng {i} phải bằng 20.")
            for j in range(81):
                self.assertEqual(matrix[i][j], matrix[j][i], f"Ma trận kề phải đối xứng tại ({i}, {j}).")

    def test_valid_precoloring_loading(self):
        """Kiểm tra nạp đề bài hợp lệ từ chuỗi 81 ký tự chuẩn."""
        # Đề Sudoku kinh điển (dễ)
        puzzle = (
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
        self.graph.load_from_string(puzzle)
        self.assertEqual(self.graph.colors[0], 5)
        self.assertTrue(self.graph.is_precolored[0])
        self.assertEqual(self.graph.colors[2], 0)
        self.assertFalse(self.graph.is_precolored[2])

    def test_precoloring_conflict_row(self):
        """Kiểm tra bắt lỗi đề sai khi trùng màu trên cùng hàng."""
        # Hai số 5 trên cùng hàng 0 tại cột 0 và cột 1
        bad_puzzle = (
            "550070000" + "0" * 72
        )
        with self.assertRaises(PrecoloringConflictError) as context:
            self.graph.load_from_string(bad_puzzle)
        self.assertIn("HÀNG 1", str(context.exception))

    def test_precoloring_conflict_col(self):
        """Kiểm tra bắt lỗi đề sai khi trùng màu trên cùng cột."""
        # Hai số 5 trên cùng cột 0 tại hàng 0 và hàng 3 (khác khối 3x3)
        grid = [[0] * 9 for _ in range(9)]
        grid[0][0] = 5
        grid[3][0] = 5
        with self.assertRaises(PrecoloringConflictError) as context:
            self.graph.load_from_matrix(grid)
        self.assertIn("CỘT 1", str(context.exception))

    def test_precoloring_conflict_box(self):
        """Kiểm tra bắt lỗi đề sai khi trùng màu trong cùng khối 3x3 (khác hàng, khác cột)."""
        # Hai số 7 trong khối 3x3 đầu tiên tại (0, 1) và (1, 2)
        grid = [[0] * 9 for _ in range(9)]
        grid[0][1] = 7
        grid[1][2] = 7
        with self.assertRaises(PrecoloringConflictError) as context:
            self.graph.load_from_matrix(grid)
        self.assertIn("KHỐI 3x3", str(context.exception))

    def test_saturation_degree_and_available_colors(self):
        """Kiểm tra tính toán bậc bão hòa (DSATUR) và tập màu khả dụng (MRV)."""
        # Ô (0, 0) chưa tô, gán các đỉnh kề các màu khác nhau
        v0 = 0
        self.assertEqual(self.graph.get_saturation_degree(v0), 0)
        self.assertEqual(self.graph.get_available_colors(v0), set(range(1, 10)))

        # Tô màu 1 cho ô cùng hàng (0, 1) -> đỉnh 1
        self.graph.assign_color(1, 1)
        self.assertEqual(self.graph.get_saturation_degree(v0), 1)
        self.assertNotIn(1, self.graph.get_available_colors(v0))

        # Tô thêm màu 1 cho ô cùng cột (1, 0) -> đỉnh 9: bậc bão hòa không tăng vì cùng màu 1!
        self.graph.assign_color(9, 1)
        self.assertEqual(self.graph.get_saturation_degree(v0), 1)

        # Tô thêm màu 2 cho ô trong khối 3x3 (1, 1) -> đỉnh 10: bậc bão hòa tăng lên 2
        self.graph.assign_color(10, 2)
        self.assertEqual(self.graph.get_saturation_degree(v0), 2)
        self.assertEqual(self.graph.get_available_colors(v0), set(range(3, 10)))

    def test_io_handler_file_read_write(self):
        """Kiểm tra module IOHandler đọc và ghi file đề bài."""
        sample_str = (
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
        with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".txt") as tmp:
            tmp.write("# Test Sudoku Puzzle\n")
            tmp.write(sample_str + "\n")
            tmp_path = tmp.name

        try:
            loaded_graph = IOHandler.read_puzzle_from_file(tmp_path)
            self.assertEqual(loaded_graph.to_string(empty_char="0"), sample_str)

            out_path = tmp_path + ".out.txt"
            IOHandler.save_puzzle_to_file(loaded_graph, out_path, as_matrix=True)
            self.assertTrue(os.path.exists(out_path))

            reloaded_graph = IOHandler.read_puzzle_from_file(out_path)
            self.assertEqual(reloaded_graph.to_string(empty_char="0"), sample_str)
            if os.path.exists(out_path):
                os.remove(out_path)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)


if __name__ == "__main__":
    unittest.main()
