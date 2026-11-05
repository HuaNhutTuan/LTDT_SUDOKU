"""
Mô-đun biểu diễn đồ thị tổng quát G = (V, E).
Phục vụ môn học: Lý thuyết đồ thị và Ứng dụng - Khoa CNTT, HCMUE.
Phụ trách: Thành viên 1 (Nhóm trưởng - Kiến trúc & Đồ thị).
"""

from typing import List, Set, Tuple, Dict


class Graph:
    """
    Lớp biểu diễn đồ thị vô hướng tổng quát G = (V, E).
    Hỗ trợ đồng thời cả hai cấu trúc lưu trữ cơ bản:
    1. Danh sách kề (Adjacency List): Tối ưu cho việc duyệt các đỉnh kề và cập nhật bậc bão hòa.
    2. Ma trận kề (Adjacency Matrix): Tối ưu cho việc kiểm tra xung đột trực tiếp giữa 2 đỉnh trong O(1).
    """

    def __init__(self, num_vertices: int):
        if num_vertices <= 0:
            raise ValueError("Số lượng đỉnh của đồ thị phải là số nguyên dương.")
        self.num_vertices: int = num_vertices
        self.num_edges: int = 0
        
        # Danh sách kề: mỗi đỉnh liên kết với một tập hợp các đỉnh kề
        self.adjacency_list: List[List[int]] = [[] for _ in range(num_vertices)]
        self._adj_set: List[Set[int]] = [set() for _ in range(num_vertices)]
        
        # Ma trận kề: kích thước num_vertices x num_vertices
        self.adjacency_matrix: List[List[int]] = [[0] * num_vertices for _ in range(num_vertices)]

    def add_edge(self, u: int, v: int) -> bool:
        """
        Thêm một cạnh vô hướng giữa đỉnh u và đỉnh v.
        Trả về True nếu cạnh mới được thêm thành công, False nếu cạnh đã tồn tại hoặc u == v.
        """
        if u < 0 or u >= self.num_vertices or v < 0 or v >= self.num_vertices:
            raise IndexError(f"Chỉ số đỉnh không hợp lệ: u={u}, v={v}. Miền hợp lệ: [0, {self.num_vertices - 1}]")
        
        if u == v:
            return False  # Đồ thị đơn, không chứa khuyên
            
        if v in self._adj_set[u]:
            return False  # Cạnh đã tồn tại (không xét đa cạnh)

        # Cập nhật danh sách kề (song phương vì là đồ thị vô hướng)
        self.adjacency_list[u].append(v)
        self.adjacency_list[v].append(u)
        self._adj_set[u].add(v)
        self._adj_set[v].add(u)

        # Cập nhật ma trận kề
        self.adjacency_matrix[u][v] = 1
        self.adjacency_matrix[v][u] = 1

        self.num_edges += 1
        return True

    def has_edge(self, u: int, v: int) -> bool:
        """
        Kiểm tra hai đỉnh u và v có cạnh nối trực tiếp hay không trong O(1).
        """
        if 0 <= u < self.num_vertices and 0 <= v < self.num_vertices:
            return self.adjacency_matrix[u][v] == 1
        return False

    def get_neighbors(self, v: int) -> List[int]:
        """
        Lấy danh sách tất cả các đỉnh kề N(v) của đỉnh v.
        """
        if 0 <= v < self.num_vertices:
            return self.adjacency_list[v]
        raise IndexError(f"Chỉ số đỉnh {v} nằm ngoài phạm vi [0, {self.num_vertices - 1}].")

    def get_degree(self, v: int) -> int:
        """
        Trả về bậc deg(v) của đỉnh v (số lượng đỉnh kề trực tiếp).
        """
        if 0 <= v < self.num_vertices:
            return len(self.adjacency_list[v])
        raise IndexError(f"Chỉ số đỉnh {v} nằm ngoài phạm vi [0, {self.num_vertices - 1}].")

    def get_all_edges(self) -> List[Tuple[int, int]]:
        """
        Trả về danh sách tất cả các cạnh vô hướng (u, v) với quy ước u < v.
        """
        edges: List[Tuple[int, int]] = []
        for u in range(self.num_vertices):
            for v in self.adjacency_list[u]:
                if u < v:
                    edges.append((u, v))
        return edges

    def is_regular(self) -> Tuple[bool, int]:
        """
        Kiểm tra xem đồ thị có phải là đồ thị chính quy (k-regular) hay không.
        Trả về (True, k) nếu đồ thị chính quy bậc k, ngược lại trả về (False, -1).
        """
        if self.num_vertices == 0:
            return True, 0
        first_degree = self.get_degree(0)
        for v in range(1, self.num_vertices):
            if self.get_degree(v) != first_degree:
                return False, -1
        return True, first_degree
