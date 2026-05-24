"""Shared model data structures and exact solver utilities."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from itertools import combinations, product
import json
from pathlib import Path
from typing import Iterable


BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_DATA_PATH = BASE_DIR / "data" / "baseline_scenario.json"


@dataclass(frozen=True)
class ModelData:
    """Input parameters for the tea production optimization model."""

    D1: float = 40.0
    D2: float = 50.0
    k: float = 4.5
    T1: float = 8.0
    T2: float = 8.0
    C1: float = 80.0
    C2: float = 65.0
    a1: float = 400.0
    a2: float = 350.0
    W_wage: float = 250_000.0
    e1: float = 150.0
    e2: float = 350.0
    P1: float = 130_000.0
    P2: float = 45_000.0
    P3: float = 9_000.0
    rd_ca1_12: float = 0.02
    rd_ca1_23: float = 0.01
    rd_ca2_12: float = 0.08
    rd_ca2_23: float = 0.12


@dataclass(frozen=True)
class Solution:
    """Optimization result."""

    x1: float
    x2: float
    x3: float
    x4: float
    n1: int
    n2: int
    q1: float
    q2: float
    q3: float
    revenue: float
    cost_labor: float
    cost_electric: float
    profit: float
    w_buy: float
    solver_name: str


def load_model_data(path: str | Path | None = None) -> ModelData:
    """Load model parameters from a JSON file."""
    target = Path(path) if path else DEFAULT_DATA_PATH
    with target.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    return ModelData(**payload)


def save_model_data(path: str | Path, data: ModelData) -> None:
    """Persist model parameters to JSON."""
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8") as handle:
        json.dump(asdict(data), handle, indent=2, ensure_ascii=False)


def compute_outputs(x1: float, x2: float, x3: float, x4: float, data: ModelData) -> tuple[float, float, float]:
    """Compute dry tea outputs from fresh tea inputs."""
    q1 = ((1.0 - data.rd_ca1_12) * x1 + (1.0 - data.rd_ca2_12) * x2) / data.k
    q2 = (
        data.rd_ca1_12 * x1
        + (1.0 - data.rd_ca1_23) * x3
        + data.rd_ca2_12 * x2
        + (1.0 - data.rd_ca2_23) * x4
    ) / data.k
    q3 = (data.rd_ca1_23 * x3 + data.rd_ca2_23 * x4) / data.k
    return q1, q2, q3


def evaluate_solution(x1: float, x2: float, x3: float, x4: float, n1: int, n2: int, data: ModelData, solver_name: str) -> Solution:
    """Evaluate revenue, costs, and profit for a plan."""
    q1, q2, q3 = compute_outputs(x1, x2, x3, x4, data)
    cost_labor = data.W_wage * (n1 + n2)
    cost_electric = data.e1 * (x1 + x3) + data.e2 * (x2 + x4)
    revenue = data.P1 * q1 + data.P2 * q2 + data.P3 * q3
    profit = revenue - cost_labor - cost_electric
    return Solution(
        x1=x1,
        x2=x2,
        x3=x3,
        x4=x4,
        n1=n1,
        n2=n2,
        q1=q1,
        q2=q2,
        q3=q3,
        revenue=revenue,
        cost_labor=cost_labor,
        cost_electric=cost_electric,
        profit=profit,
        w_buy=x1 + x2 + x3 + x4,
        solver_name=solver_name,
    )


def is_feasible_plan(x1: float, x2: float, x3: float, x4: float, n1: int, n2: int, data: ModelData, tolerance: float = 1e-6) -> bool:
    """Check whether a plan satisfies all constraints."""
    if min(x1, x2, x3, x4) < -tolerance:
        return False
    if n1 < 0 or n2 < 0:
        return False
    if x1 + x3 > data.C1 * data.T1 + tolerance:
        return False
    if x2 + x4 > data.C2 * data.T2 + tolerance:
        return False
    if x1 + x3 > data.a1 * n1 + tolerance:
        return False
    if x2 + x4 > data.a2 * n2 + tolerance:
        return False
    q1, q2, _ = compute_outputs(x1, x2, x3, x4, data)
    if abs(q1 - data.D1) > tolerance:
        return False
    if abs(q2 - data.D2) > tolerance:
        return False
    return True


def solve_exact(data: ModelData) -> Solution:
    """Solve the mixed-integer linear model without external dependencies."""
    max_n1 = int((data.C1 * data.T1 + data.a1 - 1) // data.a1) + 1
    max_n2 = int((data.C2 * data.T2 + data.a2 - 1) // data.a2) + 1
    best: Solution | None = None
    for n1, n2 in product(range(max_n1 + 1), range(max_n2 + 1)):
        candidate = _solve_continuous_subproblem(data, n1, n2)
        if candidate is None:
            continue
        if best is None or candidate.profit > best.profit + 1e-6:
            best = candidate
    if best is None:
        raise ValueError("No feasible solution for the provided scenario.")
    return best


def _solve_continuous_subproblem(data: ModelData, n1: int, n2: int) -> Solution | None:
    cap1 = min(data.C1 * data.T1, data.a1 * n1)
    cap2 = min(data.C2 * data.T2, data.a2 * n2)
    constraints = list(_build_equality_candidates(data, cap1, cap2))
    best: Solution | None = None

    for selected in combinations(range(len(constraints)), 4):
        matrix = [constraints[index][0] for index in selected]
        rhs = [constraints[index][1] for index in selected]
        point = _solve_linear_system(matrix, rhs)
        if point is None:
            continue
        x1, x2, x3, x4 = point
        if not is_feasible_plan(x1, x2, x3, x4, n1, n2, data):
            continue
        candidate = evaluate_solution(x1, x2, x3, x4, n1, n2, data, solver_name="exact-enumeration")
        if best is None or candidate.profit > best.profit + 1e-6:
            best = candidate
    return best


def _build_equality_candidates(data: ModelData, cap1: float, cap2: float) -> Iterable[tuple[list[float], float]]:
    yield [1.0, 0.0, 1.0, 0.0], cap1
    yield [0.0, 1.0, 0.0, 1.0], cap2
    yield [(1.0 - data.rd_ca1_12) / data.k, (1.0 - data.rd_ca2_12) / data.k, 0.0, 0.0], data.D1
    yield [data.rd_ca1_12 / data.k, data.rd_ca2_12 / data.k, (1.0 - data.rd_ca1_23) / data.k, (1.0 - data.rd_ca2_23) / data.k], data.D2
    yield [1.0, 0.0, 0.0, 0.0], 0.0
    yield [0.0, 1.0, 0.0, 0.0], 0.0
    yield [0.0, 0.0, 1.0, 0.0], 0.0
    yield [0.0, 0.0, 0.0, 1.0], 0.0


def _solve_linear_system(matrix: list[list[float]], rhs: list[float], tolerance: float = 1e-9) -> list[float] | None:
    augmented = [row[:] + [value] for row, value in zip(matrix, rhs)]
    size = len(augmented)

    for pivot_index in range(size):
        pivot_row = max(range(pivot_index, size), key=lambda row_index: abs(augmented[row_index][pivot_index]))
        if abs(augmented[pivot_row][pivot_index]) < tolerance:
            return None
        augmented[pivot_index], augmented[pivot_row] = augmented[pivot_row], augmented[pivot_index]

        pivot = augmented[pivot_index][pivot_index]
        for column_index in range(pivot_index, size + 1):
            augmented[pivot_index][column_index] /= pivot

        for row_index in range(size):
            if row_index == pivot_index:
                continue
            factor = augmented[row_index][pivot_index]
            if abs(factor) < tolerance:
                continue
            for column_index in range(pivot_index, size + 1):
                augmented[row_index][column_index] -= factor * augmented[pivot_index][column_index]

    return [row[-1] if abs(row[-1]) > tolerance else 0.0 for row in augmented]
