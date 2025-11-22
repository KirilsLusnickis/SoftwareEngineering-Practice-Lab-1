"""Testing harness that demonstrates Basis Path Testing for `triangle_program.py`.

Steps performed:
1. Read input test vectors from data/input.csv.
2. Compute actual labels via classify_triangle.
3. Write actual outputs to results/actual.csv.
4. Compare against expected labels (data/expected.csv).
5. Produce a human-friendly report in results/report.txt and print a summary.

Independent paths (derived from cyclomatic complexity V(G)=5 decisions + 1 = 6):
P1 invalid because a side is non-positive.
P2 invalid because triangle inequality fails.
P3 equilateral triangle.
P4 isosceles (but not equilateral).
P5 right, non-isosceles triangle.
P6 scalene, non-right triangle.
"""
from __future__ import annotations

import csv
import pathlib
from typing import Dict, Tuple

from triangle_program import classify_batch

INPUT_FILE = pathlib.Path("data/input.csv")
EXPECTED_FILE = pathlib.Path("data/expected.csv")
ACTUAL_FILE = pathlib.Path("results/actual.csv")
REPORT_FILE = pathlib.Path("results/report.txt")


def load_expected() -> Dict[str, str]:
    expected: Dict[str, str] = {}
    with EXPECTED_FILE.open(newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            expected[row["case_id"]] = row["expected"]
    return expected


def write_actual(results: list[Tuple[str, str]]) -> None:
    ACTUAL_FILE.parent.mkdir(parents=True, exist_ok=True)
    with ACTUAL_FILE.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["case_id", "actual"])
        writer.writerows(results)


def compare(results: list[Tuple[str, str]], expected: Dict[str, str]) -> Tuple[int, list[str]]:
    mismatches: list[str] = []
    for case_id, actual in results:
        exp = expected.get(case_id, "<missing>")
        if actual != exp:
            mismatches.append(f"{case_id}: expected {exp}, got {actual}")
    return len(mismatches), mismatches


def write_report(total: int, failures: int, mismatches: list[str]) -> None:
    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with REPORT_FILE.open("w") as f:
        f.write(f"Total cases: {total}\n")
        f.write(f"Failures: {failures}\n")
        if mismatches:
            f.write("\nMismatch details:\n")
            for line in mismatches:
                f.write(f"- {line}\n")


def main() -> None:
    with INPUT_FILE.open(newline="") as f:
        rows = list(csv.DictReader(f))

    expected = load_expected()
    results = classify_batch(rows)
    write_actual(results)

    failures, mismatches = compare(results, expected)
    write_report(total=len(results), failures=failures, mismatches=mismatches)

    print(f"Ran {len(results)} test cases; failures: {failures}")
    if mismatches:
        print("Mismatches:")
        for line in mismatches:
            print(f"  {line}")
    else:
        print("All basis paths passed.")


if __name__ == "__main__":
    main()
