"""Run Phase 3.1: feature matrix, rule expansion, validation, reports."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str]) -> int:
    print(f">>> {' '.join(cmd)}")
    return subprocess.call(cmd, cwd=ROOT)


def main() -> int:
    steps = [
        [sys.executable, "src/build_modelling_feature_matrix.py"],
        [sys.executable, "src/expand_scenarios.py"],
        [sys.executable, "src/validate_synthetic_scenarios.py"],
        [sys.executable, "src/validate_scenario_constraints.py"],
        [sys.executable, "src/validate_extractions.py"],
        [sys.executable, "src/generate_data_quality_report.py"],
    ]
    for cmd in steps:
        if run(cmd) != 0:
            print(f"Phase 3.1 failed at: {' '.join(cmd)}")
            return 1
    print("Phase 3.1 complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
