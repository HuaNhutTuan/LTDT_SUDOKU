"""
Mô-đun IOHandler - Đọc và ghi đề bài / kết quả Sudoku từ tệp tin.
Phục vụ môn học: Lý thuyết đồ thị và Ứng dụng - Khoa CNTT, HCMUE.
Phụ trách: Thành viên 1 (Nhóm trưởng - Kiến trúc & Đồ thị).
"""

import os
from typing import List, Optional
from .sudoku_graph import SudokuGraph


class IOHandler:
    """
    Lớp xử lý tập tin đầu vào / đầu ra cho trò chơi Sudoku.
    Hỗ trợ các định dạng tập tin chuẩn phổ biến trong nghiên cứu và thi đấu:
    - Định dạng ma trận 9x9 (các số cách nhau bởi khoảng trắng hoặc viết liền).
    - Định dạng chuỗi đơn 81 ký tự (dùng '0' hoặc '.' cho ô trống).
    - Định dạng tập tin chứa nhiều đề kiểm thử (Benchmark dataset: mỗi dòng 1 đề).
    """

    @staticmethod
    def read_puzzle_from_file(file_path: str) -> SudokuGraph:
        """
        Đọc một đề bài Sudoku từ tệp tin .txt và nạp vào đối tượng SudokuGraph.
        Tự động bỏ qua các dòng ghi chú bắt đầu bằng dấu '#'.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Không tìm thấy tập tin đề bài: {file_path}")

        raw_chars: List[str] = []
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                # Lọc ra các ký tự hợp lệ (số 0-9 hoặc dấu chấm)
                for ch in line:
                    if ch.isdigit() or ch == ".":
                        raw_chars.append(ch)

        if len(raw_chars) < 81:
            raise ValueError(
                f"Tập tin {file_path} không đủ 81 ô giá trị (chỉ tìm thấy {len(raw_chars)} ký tự hợp lệ)."
            )

        puzzle_str = "".join(raw_chars[:81])
        graph = SudokuGraph()
        graph.load_from_string(puzzle_str)
        return graph

    @staticmethod
    def read_multiple_puzzles(file_path: str) -> List[SudokuGraph]:
        """
        Đọc danh sách nhiều đề bài từ một tệp dataset (phục vụ kiểm thử Benchmark của TV5).
        Mỗi đề bài nằm trên một dòng (chuỗi 81 ký tự) hoặc các khối cách nhau.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Không tìm thấy tập tin dataset: {file_path}")

        graphs: List[SudokuGraph] = []
        with open(file_path, "r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, start=1):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                filtered = [ch for ch in line if ch.isdigit() or ch == "."]
                if len(filtered) == 81:
                    g = SudokuGraph()
                    try:
                        g.load_from_string("".join(filtered))
                        graphs.append(g)
                    except Exception as e:
                        print(f"Cảnh báo: Bỏ qua dòng {line_no} do lỗi đề bài: {e}")

        return graphs

    @staticmethod
    def save_puzzle_to_file(
        graph: SudokuGraph,
        file_path: str,
        as_matrix: bool = True,
        metadata: Optional[str] = None,
    ) -> None:
        """
        Ghi bảng Sudoku (đề bài hoặc lời giải) ra tệp tin text.
        Nếu as_matrix=True, lưu định dạng ma trận 9x9 trực quan.
        Nếu as_matrix=False, lưu dưới dạng chuỗi 81 ký tự.
        """
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            if metadata:
                f.write(f"# {metadata}\n")

            if as_matrix:
                matrix = graph.to_matrix()
                for row in matrix:
                    row_str = " ".join(str(val) for val in row)
                    f.write(row_str + "\n")
            else:
                f.write(graph.to_string(empty_char="0") + "\n")
