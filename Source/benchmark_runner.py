"""
Chương trình thực thi kiểm thử Benchmark tự động (Benchmark Runner).
Phục vụ môn học: Lý thuyết đồ thị và Ứng dụng - Khoa CNTT, HCMUE.
Phụ trách: Thành viên 5 (Thực nghiệm, Kiểm thử & Media).

Chức năng:
- Đọc bộ 40 đề kiểm thử chuẩn từ Release/puzzles/benchmark_40.txt (10 Dễ, 10 Trung bình, 10 Khó, 10 Chuyên gia).
- Chạy đối sánh đồng thời 3 giải thuật:
    1. Welsh-Powell (Tham lam tĩnh theo bậc)
    2. DSATUR Pure (Brélaz 1979 - Tham lam động theo bậc bão hòa, không quay lui)
    3. Backtrack + DSATUR (Quay lui kết hợp Forward Checking và Heuristic DSATUR / MRV)
- Đo lường và thống kê chi tiết:
    + Thời gian thực thi (ms)
    + Số bước gán màu (Color Assignments)
    + Số lần quay lui (Backtracks)
    + Số đỉnh đã thăm (Vertices Visited)
    + Tỷ lệ giải thành công (%)
- Xuất dữ liệu thực nghiệm ra:
    + Release/benchmark_results.csv (phục vụ vẽ biểu đồ trên Excel / Python)
    + Release/benchmark_summary.json (lưu trữ chỉ số tổng hợp)
"""

import os
import sys
import time
from typing import List, Tuple

# Cấu hình encoding UTF-8 cho console để chạy hoàn hảo trên VS Code và Windows Terminal
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Thêm đường dẫn gốc để import module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Source.core.sudoku_graph import SudokuGraph
from Source.core.benchmark import BenchmarkEngine, BenchmarkMetrics


def parse_benchmark_file(file_path: str) -> List[Tuple[str, str, int, str]]:
    """
    Phân tích tệp benchmark_40.txt thành danh sách các bộ đề:
    Trả về List[(puzzle_id, difficulty, clues_count, puzzle_string)]
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Không tìm thấy tập tin benchmark: {file_path}")

    dataset: List[Tuple[str, str, int, str]] = []
    current_pid = ""
    current_clues = 0

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Bắt header đề: # EASY_01 | Clues: 36
            if line.startswith("#") and "|" in line:
                parts = line.lstrip("#").strip().split("|")
                if len(parts) >= 2:
                    current_pid = parts[0].strip()
                    clue_part = parts[1].strip()
                    if "Clues:" in clue_part:
                        try:
                            current_clues = int(clue_part.replace("Clues:", "").strip())
                        except ValueError:
                            current_clues = 0
                continue

            # Nếu dòng bắt đầu bằng '#' khác thì bỏ qua
            if line.startswith("#"):
                continue

            # Dòng chứa chuỗi đề 81 ký tự
            cleaned = "".join(ch for ch in line if ch.isdigit() or ch == ".")
            if len(cleaned) == 81:
                pid = current_pid or f"PUZZLE_{len(dataset)+1:02d}"
                clues = current_clues or sum(1 for c in cleaned if c != "0" and c != ".")
                
                # Xác định độ khó từ ID
                if pid.startswith("EASY"):
                    diff = "Easy"
                elif pid.startswith("MEDIUM"):
                    diff = "Medium"
                elif pid.startswith("HARD"):
                    diff = "Hard"
                elif pid.startswith("EXPERT"):
                    diff = "Expert"
                else:
                    diff = "Custom"

                dataset.append((pid, diff, clues, cleaned))
                current_pid = ""
                current_clues = 0

    return dataset


def print_banner():
    print("=" * 80)
    print("   KHOA CNTT - TRƯỜNG ĐẠI HỌC SƯ PHẠM TP. HỒ CHÍ MINH (HCMUE)")
    print("   ĐỒ ÁN LÝ THUYẾT ĐỒ THỊ: GIẢI TRÒ CHƠI SUDOKU BẰNG TÔ MÀU ĐỒ THỊ")
    print("   HỆ THỐNG THỰC NGHIỆM VÀ ĐỐI SÁNH HIỆU NĂNG BENCHMARK (40 ĐỀ CHUẨN)")
    print("   Phụ trách: Thành viên 5 (Thực nghiệm, Kiểm thử & Media)")
    print("=" * 80)


def print_summary_table(summary: dict):
    print("\n" + "=" * 80)
    print("            BẢNG TỔNG HỢP KẾT QUẢ ĐỐI SÁNH HIỆU NĂNG 3 GIẢI THUẬT")
    print("=" * 80)
    header = f"{'Thuật toán':<22} | {'Cấp độ':<8} | {'Số đề':<6} | {'Thành công':<11} | {'T.gian TB':<10} | {'Quay lui':<9} | {'Gán màu':<9}"
    print(header)
    print("-" * 80)

    for algo in ["Welsh-Powell", "DSATUR Pure", "Backtrack + DSATUR"]:
        if algo not in summary:
            continue
        for diff in ["Easy", "Medium", "Hard", "Expert"]:
            if diff not in summary[algo]:
                continue
            data = summary[algo][diff]
            sr_str = f"{data['solved_count']}/{data['total_puzzles']} ({data['success_rate_percent']}%)"
            t_str = f"{data['time_mean_ms']:.2f} ms"
            bt_str = f"{data['backtracks_mean']:.1f}"
            as_str = f"{data['assignments_mean']:.1f}"
            print(f"{algo:<22} | {diff:<8} | {data['total_puzzles']:<6} | {sr_str:<11} | {t_str:<10} | {bt_str:<9} | {as_str:<9}")
        print("-" * 80)


def main():
    print_banner()

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    benchmark_file = os.path.join(base_dir, "Release", "puzzles", "benchmark_40.txt")
    csv_output = os.path.join(base_dir, "Release", "benchmark_results.csv")
    json_output = os.path.join(base_dir, "Release", "benchmark_summary.json")

    print(f"\n[BƯỚC 1] Đọc tập dữ liệu Benchmark từ: {benchmark_file}")
    dataset = parse_benchmark_file(benchmark_file)
    print(f"-> Nạp thành công {len(dataset)} đề kiểm thử phân chia đều 4 cấp độ:")
    for diff in ["Easy", "Medium", "Hard", "Expert"]:
        count = sum(1 for _, d, _, _ in dataset if d == diff)
        print(f"   • Cấp độ {diff:<6}: {count} đề")

    print("\n[BƯỚC 2] Bắt đầu chạy thực nghiệm đối sánh 3 giải thuật trên toàn bộ 40 đề...")
    start_all = time.perf_counter()

    results: List[BenchmarkMetrics] = []
    total_tests = len(dataset) * 3
    current_test = 0

    algorithms = ["Welsh-Powell", "DSATUR Pure", "Backtrack + DSATUR"]

    for pid, diff, clues, p_str in dataset:
        g = SudokuGraph()
        g.load_from_string(p_str)
        for algo in algorithms:
            current_test += 1
            res = BenchmarkEngine.run_single(g, pid, diff, clues, algo)
            results.append(res)
            status_char = "✓" if res.is_solved else "✗"
            print(f"   [{current_test:03d}/{total_tests:03d}] {pid} ({diff:<6}) | {algo:<20} | {status_char} | {res.execution_time_ms:6.2f} ms | Backtracks: {res.backtracks:<5}")

    total_time = time.perf_counter() - start_all
    print(f"\n-> Hoàn tất 120 lượt chạy thực nghiệm trong {total_time:.2f} giây!")

    print("\n[BƯỚC 3] Tổng hợp và tính toán các chỉ số thống kê toán học:")
    summary = BenchmarkEngine.aggregate_summary(results)
    print_summary_table(summary)

    print("\n[BƯỚC 4] Xuất kết quả chi tiết ra tệp:")
    BenchmarkEngine.export_csv(results, csv_output)
    print(f"-> Đã lưu bảng dữ liệu chi tiết tại: {csv_output}")
    BenchmarkEngine.export_json(summary, json_output)
    print(f"-> Đã lưu bảng chỉ số tổng hợp JSON tại: {json_output}")

    print("\n" + "=" * 80)
    print("   CHÚC MỪNG: THÀNH VIÊN 5 ĐÃ HOÀN THÀNH XUẤT SẮC NHIỆM VỤ THỰC NGHIỆM!")
    print("   Dữ liệu đã sẵn sàng để vẽ biểu đồ và đưa vào Chương 4 Báo cáo Tiểu luận.")
    print("=" * 80)


if __name__ == "__main__":
    main()
