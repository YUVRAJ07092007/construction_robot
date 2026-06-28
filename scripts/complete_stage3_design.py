"""Run Stage 3 design baseline: feature matrix + constraint validation + design report."""

from __future__ import annotations

import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"


def run(cmd: list[str]) -> int:
    print(f">>> {' '.join(cmd)}")
    return subprocess.call(cmd, cwd=ROOT)


def write_design_report() -> None:
    matrix_path = ROOT / "data" / "modelling_feature_matrix.csv"
    seed_path = ROOT / "data" / "gan_seed_dataset.csv"
    lines = [
        "# Stage 3 Design Baseline Report",
        "",
        f"**Generated:** {date.today().isoformat()}",
        "",
        "Stage 3 generative augmentation is in **design phase**. No synthetic records generated.",
        "",
        "## Artifacts",
        "",
        f"- Design doc: `docs/generative_augmentation_design.md`",
        f"- Config: `config/generative_augmentation_config.yaml`",
        f"- Seeds: `{seed_path.name}`",
        f"- Feature matrix: `{matrix_path.name}`",
        "",
        "## Next step",
        "",
        "Human review of design → approve Phase 3.1 rule-based scenario expansion.",
        "",
        "See `docs/stage3_design_checklist.md`.",
        "",
    ]
    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS / "stage3_design_report.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {REPORTS / 'stage3_design_report.md'}")


def main() -> int:
    steps = [
        [sys.executable, "src/build_modelling_feature_matrix.py"],
        [sys.executable, "src/validate_scenario_constraints.py"],
    ]
    for cmd in steps:
        if run(cmd) != 0:
            return 1
    write_design_report()
    print("Stage 3 design baseline complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
