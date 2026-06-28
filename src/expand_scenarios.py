"""Rule-based synthetic scenario expansion from GAN seed records (Phase 3.1)."""

from __future__ import annotations

import csv
import sys
from datetime import date
from itertools import product
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise RuntimeError("PyYAML required") from exc

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.validate_scenario_constraints import validate_scenario_row  # noqa: E402

DATA_DIR = ROOT / "data"
REPORTS_DIR = ROOT / "reports"
CONFIG_PATH = ROOT / "config" / "generative_augmentation_config.yaml"
MATRIX_PATH = DATA_DIR / "modelling_feature_matrix.csv"
SEED_PATH = DATA_DIR / "gan_seed_dataset.csv"
OUT_PATH = DATA_DIR / "synthetic_scenario_dataset.csv"

FEATURE_COLS = [
    "video_category_enc",
    "activity_group_enc",
    "workflow_stage_enc",
    "movement_pattern_enc",
    "operating_surface_enc",
    "congestion_level_enc",
    "reinforcement_complexity_enc",
    "access_condition_enc",
    "safety_condition_enc",
    "evidence_level_enc",
    "coding_confidence_enc",
    "manufacturer_name_enc",
    "comparison_robot_enc",
    "labour_count_visible",
    "robot_operator_count",
]

OUTPUT_HEADER = [
    "scenario_id",
    "is_synthetic",
    "generation_method",
    "source_seed_id",
    "scenario_family",
    "logical_validity",
    "constraint_violation_count",
    "synthetic_provenance",
    "generation_date",
    "record_origin",
    "pilot_only",
    "training_seed_count",
    "not_for_statistical_inference",
    "synthetic_generation_method",
    "generation_note",
] + FEATURE_COLS


def pilot_metadata(*, generation_method: str, note: str = "") -> dict[str, str]:
    return {
        "record_origin": "synthetic_pilot",
        "pilot_only": "yes",
        "training_seed_count": "14",
        "not_for_statistical_inference": "yes",
        "synthetic_generation_method": generation_method,
        "generation_note": note or "Pilot scenario for framework logic stress-test; not observed data",
    }

CONGESTION_FROM_ENC = {"1": "low", "2": "medium", "3": "high"}
ACCESS_FROM_ENC = {"1": "open", "2": "partially_restricted", "3": "congested"}


def load_config() -> dict:
    with CONFIG_PATH.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, header: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=header, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def fingerprint(row: dict[str, str]) -> tuple[str, ...]:
    return tuple(row.get(col, "") for col in FEATURE_COLS)


def allowed_access_for_congestion(cong_enc: str) -> list[str]:
    if cong_enc == "3":
        return ["2", "3"]
    if cong_enc == "1":
        return ["1", "2"]
    return ["1", "2", "3"]


def clamp_int(value: str, low: int, high: int) -> str:
    try:
        num = int(float(value or 0))
    except ValueError:
        num = 0
    return str(max(low, min(high, num)))


def scenario_family_for_seed(seed: dict[str, str]) -> str:
    if seed.get("video_category_enc") == "0":
        return "SF-MIVAN-SLAB-CYCLE"
    activity = seed.get("activity_group", "")
    if activity == "fresh_concrete_leveling":
        return "SF-ROBOT-FRESH-CONCRETE"
    if seed.get("workflow_stage_enc") == "3":
        return "SF-ROBOT-POST-CAST"
    return "SF-DEPLOYMENT-JOINT"


def row_for_validation(row: dict[str, str], config: dict) -> dict[str, str]:
    activity_map = {str(v): k for k, v in config["activity_group"].items()}
    enriched = dict(row)
    enriched["activity_group"] = activity_map.get(row.get("activity_group_enc", ""), "unknown")
    enriched["workflow_stage"] = {"1": "pre-pour", "2": "pour", "3": "post-cast"}.get(
        row.get("workflow_stage_enc", ""), "unknown"
    )
    enriched["operating_surface"] = {
        "1": "wet_concrete",
        "2": "pre_pour_slab",
        "3": "hardened_concrete",
    }.get(row.get("operating_surface_enc", ""), "unknown")
    enriched["congestion_level"] = CONGESTION_FROM_ENC.get(row.get("congestion_level_enc", ""), "")
    enriched["access_condition"] = ACCESS_FROM_ENC.get(row.get("access_condition_enc", ""), "")
    return enriched


def validate_feature_row(row: dict[str, str], config: dict, row_id: str) -> tuple[str, int]:
    result = validate_scenario_row(row_for_validation(row, config), config, row_id)
    violations = len(result.errors) + len(result.warnings)
    if result.errors:
        return "fail", violations
    if result.warnings:
        return "pass_with_warnings", violations
    return "pass", 0


def copy_features(matrix_row: dict[str, str]) -> dict[str, str]:
    return {col: matrix_row.get(col, "") for col in FEATURE_COLS}


def perturb_features(
    base: dict[str, str],
    *,
    cong_enc: str | None = None,
    access_enc: str | None = None,
    labour: str | None = None,
    robot_ops: str | None = None,
) -> dict[str, str]:
    row = dict(base)
    if cong_enc is not None:
        row["congestion_level_enc"] = cong_enc
    if access_enc is not None:
        row["access_condition_enc"] = access_enc
    elif cong_enc is not None:
        allowed = allowed_access_for_congestion(cong_enc)
        if row.get("access_condition_enc", "") not in allowed:
            row["access_condition_enc"] = allowed[0]
    if labour is not None:
        row["labour_count_visible"] = labour
    if robot_ops is not None:
        row["robot_operator_count"] = robot_ops
    return row


def single_seed_variants(matrix_row: dict[str, str], seed_meta: dict[str, str]) -> list[dict[str, str]]:
    base = copy_features(matrix_row)
    is_mivan = base["video_category_enc"] == "0"
    is_robot = base["video_category_enc"] == "1"
    base_cong = int(base["congestion_level_enc"] or "2")
    base_lab = int(base["labour_count_visible"] or "0")
    base_ops = int(base["robot_operator_count"] or "0")

    specs: list[dict] = []

    for delta in (-1, 0, 1):
        cong = str(max(1, min(3, base_cong + delta)))
        for access in allowed_access_for_congestion(cong):
            specs.append({"cong_enc": cong, "access_enc": access, "labour": None, "robot_ops": None})

    if is_mivan:
        for delta in (-1, 1):
            specs.append(
                {
                    "cong_enc": None,
                    "access_enc": None,
                    "labour": clamp_int(str(base_lab + delta), 2, 12),
                    "robot_ops": None,
                }
            )

    if is_robot:
        for ops in (0, 1, 2):
            if ops != base_ops:
                specs.append({"cong_enc": None, "access_enc": None, "labour": None, "robot_ops": str(ops)})

    variants: list[dict[str, str]] = []
    seen: set[tuple[str, ...]] = set()
    for spec in specs:
        row = perturb_features(
            base,
            cong_enc=spec["cong_enc"],
            access_enc=spec["access_enc"],
            labour=spec["labour"],
            robot_ops=spec["robot_ops"],
        )
        fp = fingerprint(row)
        if fp in seen:
            continue
        seen.add(fp)
        variants.append(row)
    return variants


def merge_joint_features(robot_row: dict[str, str], mivan_row: dict[str, str]) -> dict[str, str]:
    merged = copy_features(robot_row)
    merged["labour_count_visible"] = mivan_row.get("labour_count_visible", "0")
    merged["congestion_level_enc"] = mivan_row.get("congestion_level_enc", merged["congestion_level_enc"])
    merged["access_condition_enc"] = mivan_row.get("access_condition_enc", merged["access_condition_enc"])
    merged["reinforcement_complexity_enc"] = mivan_row.get(
        "reinforcement_complexity_enc", merged["reinforcement_complexity_enc"]
    )
    allowed = allowed_access_for_congestion(merged["congestion_level_enc"])
    if merged["access_condition_enc"] not in allowed:
        merged["access_condition_enc"] = allowed[0]
    return merged


def joint_variants(
    robot_row: dict[str, str],
    mivan_row: dict[str, str],
    robot_meta: dict[str, str],
    mivan_meta: dict[str, str],
) -> list[tuple[dict[str, str], str]]:
    if robot_row.get("workflow_stage_enc") != mivan_row.get("workflow_stage_enc"):
        return []

    base = merge_joint_features(robot_row, mivan_row)
    source = f"{mivan_meta['seed_id']}|{robot_meta['seed_id']}"
    variants: list[tuple[dict[str, str], str]] = []

    cong = int(base["congestion_level_enc"] or "2")
    for delta in (-1, 0, 1):
        new_cong = str(max(1, min(3, cong + delta)))
        for access in allowed_access_for_congestion(new_cong):
            row = perturb_features(base, cong_enc=new_cong, access_enc=access)
            variants.append((row, source))

    lab = int(mivan_row.get("labour_count_visible") or "0")
    for delta in (-1, 1):
        row = perturb_features(base, labour=clamp_int(str(lab + delta), 2, 12))
        variants.append((row, source))

    return variants


def select_diverse_candidates(candidates: list[dict[str, str]], target: int) -> list[dict[str, str]]:
    if len(candidates) <= target:
        return candidates

    selected: list[dict[str, str]] = []
    seen: set[tuple[str, ...]] = set()

    def pick(pool: list[dict[str, str]], count: int) -> None:
        for row in pool:
            if count <= 0 or len(selected) >= target:
                break
            fp = fingerprint(row)
            if fp in seen:
                continue
            seen.add(fp)
            selected.append(row)
            count -= 1

    joint = [c for c in candidates if c["scenario_family"] == "SF-DEPLOYMENT-JOINT"]
    bright = [c for c in candidates if c.get("manufacturer_name_enc") == "2"]
    mivan = [c for c in candidates if c["scenario_family"] == "SF-MIVAN-SLAB-CYCLE"]
    fresh = [c for c in candidates if c["scenario_family"] == "SF-ROBOT-FRESH-CONCRETE"]
    post = [c for c in candidates if c["scenario_family"] == "SF-ROBOT-POST-CAST"]

    pick(joint, 10)
    pick(bright, 4)
    pick(mivan, 16)
    pick(fresh, 12)
    pick(post, 10)

    for row in candidates:
        if len(selected) >= target:
            break
        fp = fingerprint(row)
        if fp not in seen:
            seen.add(fp)
            selected.append(row)

    return selected[:target]


def expand(
    target_count: int | None = None,
) -> dict:
    config = load_config()
    if target_count is None:
        target_count = int(config["augmentation_strategy"]["phases"]["phase_3a"]["target_synthetic_count"])

    matrix_rows = read_csv(MATRIX_PATH)
    seed_rows = read_csv(SEED_PATH)
    seed_by_id = {row["seed_id"]: row for row in seed_rows}
    matrix_by_id = {row["seed_id"]: row for row in matrix_rows}

    seed_fingerprints = {fingerprint(copy_features(matrix_by_id[sid])) for sid in matrix_by_id}

    generation_date = date.today().isoformat()
    candidates: list[dict[str, str]] = []
    seen_fps: set[tuple[str, ...]] = set()

    def try_add(
        features: dict[str, str],
        source_seed_id: str,
        scenario_family: str,
    ) -> None:
        fp = fingerprint(features)
        if fp in seed_fingerprints or fp in seen_fps:
            return
        temp_id = f"CAND-{len(candidates) + 1}"
        validity, violations = validate_feature_row(features, config, temp_id)
        if validity == "fail":
            return
        seen_fps.add(fp)
        candidates.append(
            {
                "is_synthetic": "yes",
                "generation_method": "rule_expanded",
                "source_seed_id": source_seed_id,
                "scenario_family": scenario_family,
                "logical_validity": validity,
                "constraint_violation_count": str(violations),
                "synthetic_provenance": "rule_expanded",
                "generation_date": generation_date,
                **pilot_metadata(generation_method="rule_expanded"),
                **features,
            }
        )

    for seed_id, matrix_row in matrix_by_id.items():
        seed_meta = seed_by_id[seed_id]
        family = scenario_family_for_seed(seed_meta)
        for features in single_seed_variants(matrix_row, seed_meta):
            try_add(features, seed_id, family)

    mivan_by_stage: dict[str, list[str]] = {}
    robot_by_stage: dict[str, list[str]] = {}
    for sid, row in matrix_by_id.items():
        stage = row.get("workflow_stage_enc", "")
        if row.get("video_category_enc") == "0":
            mivan_by_stage.setdefault(stage, []).append(sid)
        else:
            robot_by_stage.setdefault(stage, []).append(sid)

    for stage in set(mivan_by_stage) & set(robot_by_stage):
        for m_sid, r_sid in product(mivan_by_stage[stage], robot_by_stage[stage]):
            for features, source in joint_variants(
                matrix_by_id[r_sid],
                matrix_by_id[m_sid],
                seed_by_id[r_sid],
                seed_by_id[m_sid],
            ):
                try_add(features, source, "SF-DEPLOYMENT-JOINT")

    selected = select_diverse_candidates(candidates, target_count)
    for idx, row in enumerate(selected, start=1):
        row["scenario_id"] = f"SYN-{idx:03d}"

    write_csv(OUT_PATH, OUTPUT_HEADER, selected)
    write_expansion_report(selected, candidates, target_count, generation_date)

    return {
        "generated": len(selected),
        "candidates": len(candidates),
        "target": target_count,
    }


def write_expansion_report(
    selected: list[dict[str, str]],
    candidates: list[dict[str, str]],
    target: int,
    generation_date: str,
) -> None:
    errors = sum(1 for r in selected if r.get("logical_validity") == "fail")
    warnings = sum(1 for r in selected if r.get("logical_validity") == "pass_with_warnings")
    families: dict[str, int] = {}
    for row in selected:
        fam = row.get("scenario_family", "?")
        families[fam] = families.get(fam, 0) + 1

    lines = [
        "# Synthetic Scenario Expansion Report (Phase 3.1)",
        "",
        f"**Generated:** {generation_date} by `src/expand_scenarios.py`",
        "",
        "## Summary",
        "",
        f"- Target scenarios: {target}",
        f"- Valid candidates: {len(candidates)}",
        f"- Exported scenarios: {len(selected)}",
        f"- Failed validation (excluded): N/A (excluded at generation)",
        f"- Pass with warnings: {warnings}",
        f"- Constraint error rate: {errors / len(selected) * 100 if selected else 0:.1f}%",
        "",
        "## Scenario families",
        "",
    ]
    for fam, count in sorted(families.items()):
        lines.append(f"- {fam}: {count}")
    lines.extend(
        [
            "",
            "## Output",
            "",
            "- `data/synthetic_scenario_dataset.csv`",
            "",
            "## Research-safe note",
            "",
            "All rows are `is_synthetic=yes`, `generation_method=rule_expanded`. "
            "No duration or productivity fields generated.",
            "",
        ]
    )
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    (REPORTS_DIR / "synthetic_expansion_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    if not MATRIX_PATH.exists():
        print(f"Missing {MATRIX_PATH}; run build_modelling_feature_matrix.py first.")
        return 1
    result = expand()
    print(
        f"Phase 3.1 complete: {result['generated']} synthetic scenarios "
        f"({result['candidates']} valid candidates, target {result['target']})."
    )
    print(f"Output: {OUT_PATH}")
    print(f"Report: {REPORTS_DIR / 'synthetic_expansion_report.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
