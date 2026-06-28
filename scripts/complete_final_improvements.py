"""Run final reviewer-readiness fixes (idempotent)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str]) -> int:
    print(f">>> {' '.join(cmd)}")
    return subprocess.call(cmd, cwd=ROOT)


def main() -> int:
    py = sys.executable
    steps = [
        [py, "scripts/complete_reviewer_improvements.py"],
        [py, "src/validate_extractions.py"],
        [py, "src/generate_data_quality_report.py"],
        [py, "-m", "pytest", "tests/", "-q"],
    ]
    for cmd in steps:
        if run(cmd) != 0:
            return 1
    print("Final reviewer improvements complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
