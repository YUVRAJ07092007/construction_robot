"""Run Stage 2: GAN seed conversion, validation, and report regeneration."""

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
        [sys.executable, "src/convert_gan_seed.py"],
        [sys.executable, "src/validate_seed_dataset.py"],
        [sys.executable, "src/validate_extractions.py"],
        [sys.executable, "src/generate_data_quality_report.py"],
    ]
    for cmd in steps:
        code = run(cmd)
        if code != 0:
            print(f"Stage 2 failed at: {' '.join(cmd)}")
            return code
    print("Stage 2 complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
