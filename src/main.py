"""Tea production optimization entrypoints."""

from __future__ import annotations

from dataclasses import fields
from pathlib import Path
import argparse
import sys

from src.solver import ModelData, Solution, evaluate_solution, load_model_data, solve_exact

try:  # pragma: no cover - optional dependency
    import gurobipy as gp
    from gurobipy import GRB
except ImportError:  # pragma: no cover - optional dependency
    gp = None
    GRB = None


def configure_console() -> None:
    """Prefer UTF-8 output for local terminal demos."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")


def ask_float(label: str, default: float) -> float:
    try:
        raw = input(f"{label} [{default}]: ").strip()
    except EOFError:
        return default
    return default if raw == "" else float(raw)


def get_model_data(data_path: str | Path | None) -> ModelData:
    data = load_model_data(data_path)
    if not sys.stdin.isatty():
        return data

    print("Nhap gia tri moi neu can. Bo trong va Enter de giu du lieu tu file JSON.")
    overrides: dict[str, float] = {}
    for field in fields(ModelData):
        current = getattr(data, field.name)
        overrides[field.name] = ask_float(field.name, current)
    return ModelData(**overrides)


def solve_with_gurobi(data: ModelData) -> Solution:
    if gp is None or GRB is None:
        raise RuntimeError("gurobipy is not installed.")

    model = gp.Model("tea_production_optimization")
    model.Params.OutputFlag = 0

    x1 = model.addVar(lb=0.0, name="x1")
    x2 = model.addVar(lb=0.0, name="x2")
    x3 = model.addVar(lb=0.0, name="x3")
    x4 = model.addVar(lb=0.0, name="x4")
    n1 = model.addVar(vtype=GRB.INTEGER, lb=0.0, name="n1")
    n2 = model.addVar(vtype=GRB.INTEGER, lb=0.0, name="n2")

    q1 = ((1.0 - data.rd_ca1_12) * x1 + (1.0 - data.rd_ca2_12) * x2) / data.k
    q2 = (
        data.rd_ca1_12 * x1
        + (1.0 - data.rd_ca1_23) * x3
        + data.rd_ca2_12 * x2
        + (1.0 - data.rd_ca2_23) * x4
    ) / data.k
    q3 = (data.rd_ca1_23 * x3 + data.rd_ca2_23 * x4) / data.k

    cost_labor = data.W_wage * (n1 + n2)
    cost_electric = data.e1 * (x1 + x3) + data.e2 * (x2 + x4)
    revenue = data.P1 * q1 + data.P2 * q2 + data.P3 * q3
    profit = revenue - cost_labor - cost_electric

    model.addConstr(x1 + x3 <= data.C1 * data.T1, name="machine_shift_1")
    model.addConstr(x2 + x4 <= data.C2 * data.T2, name="machine_shift_2")
    model.addConstr(x1 + x3 <= data.a1 * n1, name="labor_shift_1")
    model.addConstr(x2 + x4 <= data.a2 * n2, name="labor_shift_2")
    model.addConstr(q1 == data.D1, name="demand_q1")
    model.addConstr(q2 == data.D2, name="demand_q2")
    model.setObjective(profit, GRB.MAXIMIZE)
    model.optimize()

    if model.Status != GRB.OPTIMAL:
        raise RuntimeError(f"Gurobi ended with status code {model.Status}.")

    return evaluate_solution(x1.X, x2.X, x3.X, x4.X, round(n1.X), round(n2.X), data, solver_name="gurobi")


def solve_model(data: ModelData, solver: str) -> Solution:
    if solver == "exact":
        return solve_exact(data)
    if solver == "gurobi":
        return solve_with_gurobi(data)
    if solver == "auto":
        if gp is not None and GRB is not None:
            return solve_with_gurobi(data)
        return solve_exact(data)
    raise ValueError(f"Unsupported solver: {solver}")


def print_solution(solution: Solution) -> None:
    print("\n=== KẾT QUẢ TỐI ƯU ===")
    print(f"Solver su dung: {solution.solver_name}")
    print("Biến quyết định:")
    print(f"  x1 = {solution.x1:.4f} kg -> che tuoi ca 1, luong 1")
    print(f"  x2 = {solution.x2:.4f} kg -> che tuoi ca 2, luong 1")
    print(f"  x3 = {solution.x3:.4f} kg -> che tuoi ca 1, luong 2")
    print(f"  x4 = {solution.x4:.4f} kg -> che tuoi ca 2, luong 2")
    print(f"  n1 = {solution.n1:d} nguoi")
    print(f"  n2 = {solution.n2:d} nguoi")

    print("\nTổng hợp sản lượng:")
    print(f"  W_buy = {solution.w_buy:.4f} kg che tuoi")
    print(f"  Q1 = {solution.q1:.4f} kg che kho loai 1")
    print(f"  Q2 = {solution.q2:.4f} kg che kho loai 2")
    print(f"  Q3 = {solution.q3:.4f} kg che kho loai 3")

    print("\nChi phí và doanh thu:")
    print(f"  Chi phi nhan cong = {solution.cost_labor:,.0f} VND")
    print(f"  Chi phi dien      = {solution.cost_electric:,.0f} VND")
    print(f"  Doanh thu         = {solution.revenue:,.0f} VND")
    print(f"  Loi nhuan         = {solution.profit:,.0f} VND")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Solve the tea production optimization model.")
    parser.add_argument("--data", default=None, help="Path to a JSON scenario file.")
    parser.add_argument(
        "--solver",
        choices=["auto", "gurobi", "exact"],
        default="auto",
        help="Choose Gurobi when available or the built-in exact solver.",
    )
    return parser.parse_args()


def main() -> None:
    configure_console()
    args = parse_args()
    data = get_model_data(args.data)
    solution = solve_model(data, args.solver)
    print_solution(solution)


if __name__ == "__main__":
    main()
