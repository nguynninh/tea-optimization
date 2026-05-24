"""Compare a manual planning heuristic against the true optimal plan."""

from __future__ import annotations

from math import ceil
import sys

from src.solver import ModelData, Solution, evaluate_solution, load_model_data, solve_exact


def configure_console() -> None:
    """Prefer UTF-8 console output for local demos."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")


def heuristic_solution(data: ModelData) -> Solution:
    """Simple manual rule that always satisfies demand."""
    x1 = data.D1 * data.k / (1.0 - data.rd_ca1_12)
    x2 = 0.0

    q2_gap = max(0.0, data.D2 - (x1 * data.rd_ca1_12) / data.k)
    x3 = q2_gap * data.k / (1.0 - data.rd_ca1_23)
    x4 = 0.0

    n1 = ceil((x1 + x3) / data.a1)
    n2 = 0
    return evaluate_solution(x1, x2, x3, x4, n1, n2, data, solver_name="manual-heuristic")


def print_detailed_analysis(label: str, solution: Solution, data: ModelData) -> None:
    print(f"\n{'=' * 70}")
    print(label)
    print(f"{'=' * 70}")
    print(f"\nPhương pháp: {solution.solver_name}")
    print("\nBiến quyết định:")
    print(f"  x1 (ca ngay, Loai 1) = {solution.x1:8.1f} kg")
    print(f"  x2 (ca toi,  Loai 1) = {solution.x2:8.1f} kg")
    print(f"  x3 (ca ngay, Loai 2) = {solution.x3:8.1f} kg")
    print(f"  x4 (ca toi,  Loai 2) = {solution.x4:8.1f} kg")
    print(f"  n1 (tho ca ngay)     = {solution.n1:8d} nguoi")
    print(f"  n2 (tho ca toi)      = {solution.n2:8d} nguoi")

    print("\nSản lượng đầu ra:")
    print(f"  Q1 (Loai 1) = {solution.q1:8.2f} kg (nhu cau: {data.D1:.0f} kg)")
    print(f"  Q2 (Loai 2) = {solution.q2:8.2f} kg (nhu cau: {data.D2:.0f} kg)")
    print(f"  Q3 (Loai 3) = {solution.q3:8.2f} kg")

    print("\nChi phí và doanh thu:")
    print(f"  Chi phi nhan cong = {solution.cost_labor:12,.0f} VND")
    print(f"  Chi phi dien      = {solution.cost_electric:12,.0f} VND")
    print(f"  Doanh thu         = {solution.revenue:12,.0f} VND")
    print(f"  Loi nhuan         = {solution.profit:12,.0f} VND")

    margin = (solution.profit / solution.revenue) * 100 if solution.revenue else 0.0
    print(f"  Profit margin     = {margin:6.1f}%")


def main() -> None:
    configure_console()
    data = load_model_data()
    heuristic = heuristic_solution(data)
    optimal = solve_exact(data)

    print("\n" + "=" * 70)
    print("PHÂN TÍCH HEURISTIC VS OPTIMAL")
    print("=" * 70)
    print("\nNguồn tham số: data/baseline_scenario.json")

    print_detailed_analysis("HEURISTIC (quy tắc thủ công)", heuristic, data)
    print_detailed_analysis("OPTIMAL (nghiệm tối ưu)", optimal, data)

    print(f"\n{'=' * 70}")
    print("SO SÁNH")
    print(f"{'=' * 70}")
    print(f"\n{'Chi so':<28} | {'HEURISTIC':>16} | {'OPTIMAL':>16}")
    print("-" * 70)
    print(f"{'Loi nhuan (VND)':<28} | {heuristic.profit:>16,.0f} | {optimal.profit:>16,.0f}")
    print(f"{'Chi phi tong (VND)':<28} | {(heuristic.cost_labor + heuristic.cost_electric):>16,.0f} | {(optimal.cost_labor + optimal.cost_electric):>16,.0f}")
    print(f"{'Tong nhan cong':<28} | {(heuristic.n1 + heuristic.n2):>16d} | {(optimal.n1 + optimal.n2):>16d}")
    print(f"{'Tong che tuoi (kg)':<28} | {heuristic.w_buy:>16.1f} | {optimal.w_buy:>16.1f}")
    print(f"{'Q1 (kg)':<28} | {heuristic.q1:>16.2f} | {optimal.q1:>16.2f}")
    print(f"{'Q2 (kg)':<28} | {heuristic.q2:>16.2f} | {optimal.q2:>16.2f}")

    profit_delta = optimal.profit - heuristic.profit
    improvement = (profit_delta / heuristic.profit) * 100 if heuristic.profit else 0.0
    print(f"\nChenh lech loi nhuan: {profit_delta:,.0f} VND/ngay")
    print(f"Muc cai thien loi nhuan cua toi uu so voi heuristic: {improvement:+.3f}%")


if __name__ == "__main__":
    main()
