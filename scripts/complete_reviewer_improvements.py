"""Run full reviewer-improvement pipeline (idempotent)."""

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
        [py, "scripts/apply_reviewer_schema_v2.py"],
        [py, "scripts/patch_synthetic_pilot_metadata.py"],
        [py, "src/validate_extractions.py"],
        [py, "scripts/check_file_formatting.py"],
        [py, "src/generate_data_quality_report.py"],
        [py, "src/dri_weight_sensitivity.py"],
    ]
    for cmd in steps:
        if run(cmd) != 0:
            return 1
    print("Reviewer improvements complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
