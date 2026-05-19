"""Tea production optimization model using Gurobi."""

from __future__ import annotations

from dataclasses import dataclass
import sys

try:
    import gurobipy as gp
    from gurobipy import GRB
except ImportError as exc:  # pragma: no cover - runtime guard
    raise SystemExit(
        "gurobipy is not installed. Install it with: pip install gurobipy"
    ) from exc


# ---------------------------------------------------------------------------
# Default inputs
# Edit these at the top when you want to change the scenario.
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ModelData:
    # Demand in finished dry tea (kg)
    D1: float = 20.0
    D2: float = 20.0

    # Fresh-to-dry conversion factor: kg fresh per 1 kg dry
    k: float = 4.5

    # Working hours and machine capacity per shift
    T1: float = 8.0
    T2: float = 8.0
    C1: float = 120.0
    C2: float = 100.0

    # Labor productivity per worker per shift (kg fresh)
    a1: float = 450.0
    a2: float = 410.0

    # Labor cost per worker per shift
    W_wage: float = 375_000.0

    # Electricity cost per kg fresh processed in each shift
    # These should be calibrated from the EVN tariff + machine power draw.
    e1: float = 1_250.0
    e2: float = 1_650.0

    # Sale prices per kg dry tea
    P1: float = 95_000.0
    P2: float = 37_000.0
    P3: float = 8_000.0

    # Yield loss coefficients
    rd_ca1_12: float = 0.02
    rd_ca1_23: float = 0.01
    rd_ca2_12: float = 0.08
    rd_ca2_23: float = 0.12


def ask_float(label: str, default: float) -> float:
    raw = input(f"{label} [{default}]: ").strip()
    return default if raw == "" else float(raw)


def ask_int(label: str, default: int) -> int:
    raw = input(f"{label} [{default}]: ").strip()
    return default if raw == "" else int(raw)


def get_model_data() -> ModelData:
    if not sys.stdin.isatty():
        return ModelData()

    print("Nhap D1, D2. Bo trong va Enter de dung gia tri mac dinh.")
    return ModelData(
        D1=ask_float("D1 - nhu cau loai 1 (kg kho)", ModelData.D1),
        D2=ask_float("D2 - nhu cau loai 2 (kg kho)", ModelData.D2),
    )


def build_model(data: ModelData) -> tuple[gp.Model, dict[str, gp.Var]]:
    m = gp.Model("tea_production_optimization")
    m.Params.OutputFlag = 1

    x1 = m.addVar(lb=0.0, name="x1")
    x2 = m.addVar(lb=0.0, name="x2")
    x3 = m.addVar(lb=0.0, name="x3")
    x4 = m.addVar(lb=0.0, name="x4")
    n1 = m.addVar(vtype=GRB.INTEGER, lb=0.0, name="n1")
    n2 = m.addVar(vtype=GRB.INTEGER, lb=0.0, name="n2")

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

    m.addConstr(x1 + x3 <= data.C1 * data.T1, name="machine_shift_1")
    m.addConstr(x2 + x4 <= data.C2 * data.T2, name="machine_shift_2")
    m.addConstr(x1 + x3 <= data.a1 * n1, name="labor_shift_1")
    m.addConstr(x2 + x4 <= data.a2 * n2, name="labor_shift_2")
    m.addConstr(q1 >= data.D1, name="demand_q1")
    m.addConstr(q2 >= data.D2, name="demand_q2")

    m.setObjective(profit, GRB.MAXIMIZE)

    vars_map = {
        "x1": x1,
        "x2": x2,
        "x3": x3,
        "x4": x4,
        "n1": n1,
        "n2": n2,
    }
    return m, vars_map


def print_solution(model: gp.Model, data: ModelData, vars_map: dict[str, gp.Var]) -> None:
    if model.Status == GRB.OPTIMAL:
        x1 = vars_map["x1"].X
        x2 = vars_map["x2"].X
        x3 = vars_map["x3"].X
        x4 = vars_map["x4"].X
        n1 = vars_map["n1"].X
        n2 = vars_map["n2"].X

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
        w_buy = x1 + x2 + x3 + x4

        print("\n=== Kết quả tối ưu ===")
        print("Biến quyết định:")
        print(f"  x1 = {x1:.4f} kg  -> chè tươi ca 1, luồng 1 (chủ đích loại 1)")
        print(f"  x2 = {x2:.4f} kg  -> chè tươi ca 2, luồng 1 (chủ đích loại 1)")
        print(f"  x3 = {x3:.4f} kg  -> chè tươi ca 1, luồng 2 (chủ đích loại 2)")
        print(f"  x4 = {x4:.4f} kg  -> chè tươi ca 2, luồng 2 (chủ đích loại 2)")
        print(f"  n1 = {n1:.0f}  -> số thợ ở ca 1")
        print(f"  n2 = {n2:.0f}  -> số thợ ở ca 2")

        print("\nTổng hợp sản lượng:")
        print(f"  W_buy = {w_buy:.4f} kg chè tươi cần mua/xử lý")
        print(f"  Q1 = {q1:.4f} kg chè khô loại 1 giao được")
        print(f"  Q2 = {q2:.4f} kg chè khô loại 2 giao được")
        print(f"  Q3 = {q3:.4f} kg chè khô loại 3 phát sinh")

        print("\nChi phí và doanh thu:")
        print(f"  Chi phí nhân công = {cost_labor:,.0f} VND")
        print(f"  Chi phí điện       = {cost_electric:,.0f} VND")
        print(f"  Doanh thu          = {revenue:,.0f} VND")
        print(f"  Lợi nhuận          = {profit:,.0f} VND")

        print("\nDiễn giải nhanh:")
        print("  - Mô hình chỉ dùng luồng loại 2 ở mức tối thiểu cần thiết để đạt Q2.")
        print("  - Nếu x3 và x4 bằng 0 thì luồng loại 2 không đáng dùng thêm với bộ số hiện tại.")
        print("  - Q1 và Q2 là sản lượng khô, nên so trực tiếp với D1 và D2.")
        print("  - x1..x4 là kg chè tươi, n1..n2 là số thợ.")
        return

    if model.Status == GRB.INFEASIBLE:
        print("Model is infeasible. Check demand, capacity, and labor inputs.")
        model.computeIIS()
        model.write("tea_model.ilp")
        print("IIS written to tea_model.ilp")
        return

    print(f"Model ended with status code: {model.Status}")


def main() -> None:
    data = get_model_data()
    model, vars_map = build_model(data)
    model.optimize()
    print_solution(model, data, vars_map)


if __name__ == "__main__":
    main()
