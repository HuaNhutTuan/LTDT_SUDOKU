"""
Mô-đun Bộ sinh đề Sudoku tự động (Game Generator) theo nguyên lý Đối xứng tâm
và cam kết đúng một nghiệm duy nhất (Unique Solution).
Phụ trách: Thành viên 3 (Kiều Gia Bảo) kết hợp Nhóm trưởng (Hứa Nhựt Tuấn).
"""

import random
from typing import Dict, List, Optional, Set, Tuple
from Source.core.sudoku_graph import SudokuGraph


class PuzzleGenerator:
    """
    Bộ sinh đề Sudoku 4 cấp độ khó:
    - Dễ (Easy): 36 - 40 clues (mặc định 38)
    - Trung bình (Medium): 32 - 35 clues (mặc định 33)
    - Khó (Hard): 26 - 31 clues (mặc định 28)
    - Chuyên gia (Expert): 22 - 25 clues (mặc định 24)

    Quy trình sinh đề:
    1. Sinh một bảng giải hoàn chỉnh hợp lệ ngẫu nhiên bằng BacktrackDSATUR xáo trộn màu.
    2. Tạo danh sách các cặp đỉnh đối xứng tâm 180 độ: (r, c) và (8-r, 8-c).
    3. Xáo trộn ngẫu nhiên thứ tự các cặp đỉnh.
    4. Thử đục lỗ từng cặp đỉnh và kiểm tra nghiệm bằng SudokuGraph.count_solutions(max_solutions=2).
       - Nếu số nghiệm == 1: chấp nhận đục lỗ (giảm số clue).
       - Nếu số nghiệm > 1: khôi phục lại giá trị của cặp đỉnh.
    5. Dừng lại khi số clue đạt ngưỡng mục tiêu của cấp độ yêu cầu.
    """

    # Định mức số clues (ô cho sẵn) chuẩn mực theo từng cấp độ
    DIFFICULTY_CLUES: Dict[str, Tuple[int, int]] = {
        "easy": (36, 40),
        "medium": (32, 35),
        "hard": (26, 31),
        "expert": (22, 25),
    }

    @classmethod
    def generate_full_board(cls) -> SudokuGraph:
        """
        Sinh một bảng Sudoku hoàn chỉnh ngẫu nhiên thỏa mãn 100% luật tô màu đồ thị.
        Áp dụng thuật toán Quay lui kết hợp Heuristic MRV và xáo trộn ngẫu nhiên bảng màu.
        """
        graph = SudokuGraph()
        working_colors = [0] * 81
        adj = graph.adjacency_list
        palette = list(range(1, 10))

        def fill_board() -> bool:
            # Tìm ô chưa tô có ít màu khả dụng nhất (MRV)
            best_v = -1
            best_avail: List[int] = []
            min_count = 10

            for v in range(81):
                if working_colors[v] == 0:
                    used = {working_colors[nbr] for nbr in adj[v] if working_colors[nbr] != 0}
                    avail = [c for c in palette if c not in used]
                    cnt = len(avail)
                    if cnt == 0:
                        return False
                    if cnt < min_count:
                        min_count = cnt
                        best_v = v
                        best_avail = avail
                        if cnt == 1:
                            break

            if best_v == -1:
                return True  # Đã điền kín bảng

            # Xáo trộn thứ tự màu thử nghiệm để tạo tính ngẫu nhiên phong phú
            random.shuffle(best_avail)

            for color in best_avail:
                working_colors[best_v] = color
                if fill_board():
                    return True
                working_colors[best_v] = 0

            return False

        # Điền ngẫu nhiên 3 khối chéo độc lập (0, 4, 8) để tăng tốc độ sinh và tăng độ phân tán
        for box_idx in (0, 4, 8):
            start_r = (box_idx // 3) * 3
            start_c = (box_idx % 3) * 3
            shuffled = list(palette)
            random.shuffle(shuffled)
            idx = 0
            for r in range(start_r, start_r + 3):
                for c in range(start_c, start_c + 3):
                    v = SudokuGraph.coords_to_index(r, c)
                    working_colors[v] = shuffled[idx]
                    idx += 1

        fill_board()

        for v in range(81):
            graph.colors[v] = working_colors[v]

        return graph

    @classmethod
    def generate(cls, difficulty: str = "easy", max_attempts: int = 5) -> SudokuGraph:
        """
        Sinh một bài toán Sudoku theo cấp độ khó với tính chất đối xứng tâm 180 độ
        và cam kết đúng một nghiệm duy nhất.

        :param difficulty: "easy", "medium", "hard", hoặc "expert"
        :param max_attempts: Số lần thử lại tối đa nếu chưa đạt số clues mục tiêu
        :return: Đối tượng SudokuGraph đã được nạp đề bài (is_precolored được thiết lập đúng)
        """
        diff = difficulty.lower().strip()
        if diff not in cls.DIFFICULTY_CLUES:
            diff = "easy"

        target_min, target_max = cls.DIFFICULTY_CLUES[diff]
        target_clues = (target_min + target_max) // 2

        best_graph: Optional[SudokuGraph] = None
        min_clues_reached = 82

        for attempt in range(max_attempts):
            full_board = cls.generate_full_board()
            puzzle_graph = full_board.clone()

            # Tạo danh sách các cặp đỉnh đối xứng tâm: (v, 80 - v)
            # Với r, c thì đối xứng là (8-r, 8-c) -> v_sym = (8-r)*9 + (8-c) = 80 - (r*9+c) = 80 - v
            pairs: List[Tuple[int, int]] = []
            center_v = 40  # Tọa độ (4, 4), tự đối xứng với chính nó

            for v in range(40):
                pairs.append((v, 80 - v))

            # Xáo trộn thứ tự các cặp đỉnh để đục lỗ ngẫu nhiên
            random.shuffle(pairs)
            # Thêm đỉnh trung tâm vào vị trí ngẫu nhiên
            pairs.insert(random.randint(0, len(pairs)), (center_v, center_v))

            current_clues = 81

            for v1, v2 in pairs:
                if current_clues <= target_clues:
                    break

                val1 = puzzle_graph.colors[v1]
                val2 = puzzle_graph.colors[v2]

                # Tạm thời xóa số
                puzzle_graph.colors[v1] = 0
                if v1 != v2:
                    puzzle_graph.colors[v2] = 0

                # Kiểm tra số lượng nghiệm
                sols = puzzle_graph.count_solutions(max_solutions=2)

                if sols == 1:
                    # Chấp nhận xóa: Nghiệm vẫn duy nhất
                    current_clues -= 1 if v1 == v2 else 2
                else:
                    # Khôi phục lại vì dẫn đến đa nghiệm (>1) hoặc vô nghiệm (0)
                    puzzle_graph.colors[v1] = val1
                    if v1 != v2:
                        puzzle_graph.colors[v2] = val2

            if current_clues <= target_max:
                # Đạt yêu cầu cấp độ
                cls._mark_precolored(puzzle_graph)
                return puzzle_graph

            if current_clues < min_clues_reached:
                min_clues_reached = current_clues
                best_graph = puzzle_graph.clone()

        if best_graph is not None:
            cls._mark_precolored(best_graph)
            return best_graph

        # Trường hợp dự phòng khẩn cấp
        fallback = cls.generate_full_board()
        cls._mark_precolored(fallback)
        return fallback

    @staticmethod
    def _mark_precolored(graph: SudokuGraph) -> None:
        """Đánh dấu các đỉnh có số là đỉnh tiền tô màu cố định của đề bài."""
        for v in range(81):
            if graph.colors[v] != 0:
                graph.is_precolored[v] = True
            else:
                graph.is_precolored[v] = False
