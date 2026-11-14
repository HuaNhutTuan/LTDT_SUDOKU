"""
Chương trình chính (Entry point) kiểm thử và chạy thử nghiệm lõi đồ thị SudokuGraph.
Phụ trách: Hứa Nhựt Tuấn - Nhóm trưởng (Thành viên 1: Kiến trúc & Đồ thị).
Môn học: Lý thuyết đồ thị và Ứng dụng - Khoa CNTT, HCMUE.
"""

import sys
import os

# Thêm đường dẫn gốc để import module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Source.core.sudoku_graph import SudokuGraph, PrecoloringConflictError
from Source.core.io_handler import IOHandler
from Source.algorithms.welsh_powell import WelshPowellSolver
from Source.algorithms.dsatur import DSATURSolver


def print_banner():
    print("=" * 70)
    print("    ĐỒ ÁN LÝ THUYẾT ĐỒ THỊ VÀ ỨNG DỤNG - KHOA CNTT, HCMUE")
    print("    ĐỀ TÀI: GIẢI TRÒ CHƠI SUDOKU BẰNG THUẬT TOÁN TÔ MÀU ĐỒ THỊ")
    print("    MODULE CỐT LÕI: SudokuGraph (81 đỉnh, 810 cạnh, 20-regular)")
    print("    Phụ trách: Thành viên 1 - Nhóm trưởng (Kiến trúc & Đồ thị)")
    print("=" * 70)


def demonstrate_graph_core():
    print_banner()

    print("\n[BƯỚC 1] KHỞI TẠO ĐỒ THỊ SUDOKU G = (V, E)")
    graph = SudokuGraph()
    print(f"+ Tổng số đỉnh |V|: {graph.num_vertices} (kỳ vọng: 81)")
    print(f"+ Tổng số cạnh vô hướng |E|: {graph.num_edges} (kỳ vọng: 810)")
    
    is_reg, deg = graph.is_regular()
    print(f"+ Đồ thị chính quy: {is_reg} (Bậc mọi đỉnh k = {deg}, kỳ vọng: 20)")

    # Khảo sát chi tiết đỉnh 0 (ô hàng 0, cột 0)
    v0 = 0
    nbrs = graph.get_neighbors(v0)
    r_nbrs = graph.get_row_neighbors(v0)
    c_nbrs = graph.get_col_neighbors(v0)
    b_nbrs = graph.get_box_neighbors(v0)
    print(f"\n[BƯỚC 2] KHẢO SÁT CHI TIẾT ĐỈNH 0 (Tọa độ hàng 0, cột 0):")
    print(f"  - 8 đỉnh kề cùng hàng: {r_nbrs}")
    print(f"  - 8 đỉnh kề cùng cột: {c_nbrs}")
    print(f"  - 8 đỉnh trong khối 3x3: {b_nbrs}")
    print(f"  - Tổng hợp 20 đỉnh kề duy nhất N(0): {nbrs}")
    print(f"  => Tổng số đỉnh kề: {len(nbrs)} đỉnh.")

    print("\n[BƯỚC 3] NẠP ĐỀ BÀI SUDOKU TIỀN TÔ MÀU MẪU (PRE-COLORING EXTENSION):")
    sample_puzzle = (
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
    graph.load_from_string(sample_puzzle)
    graph.display("ĐỀ BÀI SUDOKU BAN ĐẦU")
    
    precolored_count = sum(1 for p in graph.is_precolored if p)
    print(f"+ Số ô tiền tô màu (đề bài cho sẵn): {precolored_count} ô")
    print(f"+ Số ô chưa tô cần giải: {81 - precolored_count} ô")

    # Kiểm tra bậc bão hòa tại một số ô trống
    empty_indices = graph.get_uncolored_vertices()[:5]
    print("\n[BƯỚC 4] BẬC BÃO HÒA (DSATUR) & TẬP MÀU KHẢ DỤNG TẠI CÁC Ô TRỐNG ĐẦU TIÊN:")
    for v in empty_indices:
        r, c = SudokuGraph.index_to_coords(v)
        sat = graph.get_saturation_degree(v)
        avail = sorted(list(graph.get_available_colors(v)))
        print(f"  - Ô ({r + 1}, {c + 1}) [đỉnh {v:2d}]: Bậc bão hòa = {sat}, Màu khả dụng = {avail}")

    print("\n[BƯỚC 5] THỬ NGHIỆM BẮT LỖI ĐỀ BÀI VI PHẠM LUẬT TIỀN TÔ MÀU:")
    invalid_puzzle = "550070000" + "0" * 72  # Trùng hai số 5 ở hàng 1
    try:
        test_graph = SudokuGraph()
        test_graph.load_from_string(invalid_puzzle)
    except PrecoloringConflictError as err:
        print(f"  [ĐÃ BẮT LỖI THÀNH CÔNG] Ngoại lệ: {err}")

    print("\n[BƯỚC 6] KIỂM TRA TÍNH KHẢ GIẢI VÀ SỐ NGHIỆM (SOLVABILITY CHECKER):")
    solvability = graph.check_solvability()
    print(f"  + Trạng thái: {solvability['status']}")
    print(f"  + Số lượng nghiệm tìm được: {solvability['solutions_count']}")
    print(f"  + Thông điệp: {solvability['message']}")

    print("\n[BƯỚC 7] GỢI Ý NƯỚC ĐI TIẾP THEO (HINT ENGINE THEO HEURISTIC DSATUR & MRV):")
    hint = graph.get_hint()
    if hint:
        print(f"  + Ô gợi ý: Hàng {hint['row'] + 1}, Cột {hint['col'] + 1} (Đỉnh {hint['vertex']})")
        print(f"  + Bậc bão hòa sat_deg: {hint['sat_degree']}/9")
        print(f"  + Màu gợi ý: {hint['suggested_color']}")
        print(f"  + Miền màu khả dụng: {hint['available_colors']}")
        print(f"  + Lời giải thích logic đồ thị: {hint['reason']}")

    print("\n[BƯỚC 8] KIỂM TRA XUNG ĐỘT THỜI GIAN THỰC (GAME VALIDATOR):")
    # Giả lập người chơi thử điền sai màu 5 vào ô (0, 2)
    fake_v = SudokuGraph.coords_to_index(0, 2)
    graph.colors[fake_v] = 5
    conflicts = graph.find_conflicts(fake_v)
    print(f"  + Người chơi nhập thử số 5 vào ô (1, 3)...")
    print(f"  + Phát hiện {len(conflicts)} xung đột trên 20 đỉnh kề:")
    for c in conflicts:
        print(f"    - {c['message']}")
    graph.colors[fake_v] = 0  # Hoàn tác

    print("\n" + "=" * 70)
    print("    MODULE THUẬT TOÁN: THÀNH VIÊN 2 (WELSH-POWELL & DSATUR)")
    print("=" * 70)

    # 1. Thử nghiệm Welsh-Powell trên bản sao
    wp_graph = graph.clone()
    wp_solver = WelshPowellSolver(wp_graph, tie_breaker="index")
    wp_result = wp_solver.solve()
    print(f"\n[THỬ NGHIỆM 1] THUẬT TOÁN WELSH-POWELL (Tham lam theo bậc cố định):")
    print(f"  + Trạng thái: {wp_result['status']}")
    print(f"  + Thời gian chạy: {wp_result['execution_time_ms']:.3f} ms")
    print(f"  + Tổng số bước gán: {wp_result['total_steps']}")
    print(f"  + Số ô tô thành công: {wp_result['colored_count']}/81 ô")
    if wp_result["deadlock_info"]:
        print(f"  + Lý do bế tắc (Deadlock): {wp_result['deadlock_info']['reason']}")

    # 2. Thử nghiệm DSATUR thuần túy trên bản sao
    ds_graph = graph.clone()
    ds_solver = DSATURSolver(ds_graph)
    ds_result = ds_solver.solve()
    print(f"\n[THỬ NGHIỆM 2] THUẬT TOÁN DSATUR (Heuristic bậc bão hòa động):")
    print(f"  + Trạng thái: {ds_result['status']}")
    print(f"  + Thời gian chạy: {ds_result['execution_time_ms']:.3f} ms")
    print(f"  + Tổng số bước gán: {ds_result['total_steps']}")
    print(f"  + Số ô tô thành công: {ds_result['colored_count']}/81 ô")
    print(f"  + Thông điệp: {ds_result['message']}")
    if ds_result["status"] == "SUCCESS":
        ds_graph.display("KẾT QUẢ GIẢI BẰNG DSATUR")

    print("\n" + "=" * 70)
    print("  KẾT LUẬN: Đã hoàn thiện nghiệm thu 100% nhiệm vụ Thành viên 2!")
    print("  - Lớp WelshPowellSolver & DSATURSolver trong Source.algorithms.")
    print("  - Cơ chế tính và cập nhật Bậc bão hòa động O(1) qua 20 đỉnh kề.")
    print("  - Đã sẵn sàng phục vụ TV3 (Backtracking), TV4 (GUI) và TV5 (Benchmark).")
    print("=" * 70)


if __name__ == "__main__":
    demonstrate_graph_core()
