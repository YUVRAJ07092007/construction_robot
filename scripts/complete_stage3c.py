"""Run Phase 3C: DRI framework scoring and validation."""

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
        [sys.executable, "src/compute_dri_scores.py"],
        [sys.executable, "src/validate_dri_scores.py"],
    ]
    for cmd in steps:
        if run(cmd) != 0:
            return 1
    print("Phase 3C complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
