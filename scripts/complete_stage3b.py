"""Run Phase 3B: tabular GAN/VAE pilot generation and validation."""

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
        [sys.executable, "src/generate_tabular_gan_pilot.py"],
        [sys.executable, "src/validate_synthetic_scenarios.py", "--gan"],
        [sys.executable, "src/validate_synthetic_scenarios.py", "--all"],
        [sys.executable, "src/compute_dri_scores.py", "--all-synthetic"],
    ]
    for cmd in steps:
        if run(cmd) != 0:
            return 1
    print("Phase 3B complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
