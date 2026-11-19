"""
Kiểm thử tự động cho mô-đun PuzzleGenerator (Bộ sinh đề Sudoku đối xứng tâm có nghiệm duy nhất).
"""

import unittest
from Source.core.sudoku_graph import SudokuGraph
from Source.core.puzzle_generator import PuzzleGenerator


class TestPuzzleGenerator(unittest.TestCase):
    def test_generate_full_board(self):
        """Kiểm tra sinh bảng hoàn chỉnh 81 ô không vi phạm xung đột."""
        full_board = PuzzleGenerator.generate_full_board()
        self.assertTrue(full_board.is_complete())
        self.assertEqual(len(full_board.get_all_conflicts()), 0)
        self.assertEqual(len(full_board.get_uncolored_vertices()), 0)

    def test_generate_easy_puzzle(self):
        """Kiểm tra sinh đề Dễ có nghiệm duy nhất và số clues phù hợp."""
        puzzle = PuzzleGenerator.generate(difficulty="easy", max_attempts=2)
        clues_count = sum(1 for c in puzzle.colors if c != 0)
        self.assertGreaterEqual(clues_count, 32)
        self.assertLessEqual(clues_count, 45)
        # Kiểm tra tính duy nhất của nghiệm
        sols = puzzle.count_solutions(max_solutions=2)
        self.assertEqual(sols, 1, "Đề bài sinh ra phải có duy nhất đúng 1 nghiệm!")

    def test_central_symmetry(self):
        """Kiểm tra tính đối xứng tâm của các ô được điền và ô trống."""
        puzzle = PuzzleGenerator.generate(difficulty="easy", max_attempts=2)
        for v in range(40):
            v_sym = 80 - v
            is_filled_v = (puzzle.colors[v] != 0)
            is_filled_sym = (puzzle.colors[v_sym] != 0)
            self.assertEqual(
                is_filled_v,
                is_filled_sym,
                f"Đỉnh {v} và đỉnh đối xứng {v_sym} phải cùng trạng thái (đối xứng tâm 180 độ)!"
            )


if __name__ == "__main__":
    unittest.main()
