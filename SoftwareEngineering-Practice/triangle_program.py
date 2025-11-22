"""
Testable program for Basis Path Testing.
"""
from __future__ import annotations

from typing import Iterable


def classify_triangle(a: float, b: float, c: float) -> str:
    """Return a label for the triangle defined by sides a,b,c.
    Output labels:
    - INVALID_NONPOSITIVE: any side <= 0
    - INVALID_TRIANGLE_INEQUALITY: violates triangle inequality
    - EQUILATERAL
    - ISOSCELES
    - RIGHT_SCALENE
    - SCALENE
    """

    sides = (a, b, c)

    # Decision 1: guard against non-positive values
    if any(x <= 0 for x in sides):
        return "INVALID_NONPOSITIVE"

    x, y, z = sorted(sides)

    # Decision 2: triangle inequality
    if x + y <= z:
        return "INVALID_TRIANGLE_INEQUALITY"

    # Decision 3: equilateral
    if a == b == c:
        return "EQUILATERAL"

    # Decision 4: isosceles (non-equilateral because of previous check)
    is_iso = a == b or b == c or a == c

    # Decision 5: right triangle (Pythagoras)
    is_right = abs(x * x + y * y - z * z) < 1e-9

    if is_iso:
        return "ISOSCELES"

    if is_right:
        return "RIGHT_SCALENE"

    return "SCALENE"


def classify_batch(rows: Iterable[dict[str, str]]) -> list[tuple[str, str]]:
    """Classify each row read from CSV and return list of (case_id, label)."""
    results: list[tuple[str, str]] = []
    for row in rows:
        case_id = row["case_id"]
        a, b, c = (float(row["a"]), float(row["b"]), float(row["c"]))
        label = classify_triangle(a, b, c)
        results.append((case_id, label))
    return results


if __name__ == "__main__":
    import csv
    import pathlib

    data_path = pathlib.Path("data/input.csv")
    with data_path.open(newline="") as f:
        reader = csv.DictReader(f)
        batch_results = classify_batch(reader)

    for case_id, label in batch_results:
        print(f"{case_id}: {label}")
