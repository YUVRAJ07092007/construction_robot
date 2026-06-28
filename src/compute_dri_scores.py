"""Compute Deployment Readiness Index (DRI) scores — Phase 3C framework demonstration."""

from __future__ import annotations

import csv
import sys
from datetime import date
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise RuntimeError("PyYAML required") from exc

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

CONFIG_PATH = ROOT / "config" / "dri_framework_config.yaml"
GEN_CONFIG_PATH = ROOT / "config" / "generative_augmentation_config.yaml"
SEED_PATH = ROOT / "data" / "gan_seed_dataset.csv"
SYNTH_PATH = ROOT / "data" / "synthetic_scenario_dataset.csv"
GAN_SYNTH_PATH = ROOT / "data" / "synthetic_scenario_dataset_gan.csv"
OUT_PATH = ROOT / "data" / "dri_scored_scenarios.csv"

OUTPUT_HEADER = [
    "record_id",
    "record_type",
    "source_table",
    "scenario_family",
    "dri_applicable",
    "sci_only",
    "dri_access_score",
    "dri_workflow_score",
    "dri_coexistence_score",
    "dri_surface_score",
    "dri_evidence_score",
    "dri_total_score",
    "sci_total_score",
    "dri_band",
    "dri_rank",
    "score_provenance",
    "scoring_date",
]


def load_yaml(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, header: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=header, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def parse_int(value: str, default: int = 0) -> int:
    try:
        return int(float(value or default))
    except ValueError:
        return default


def clamp_score(value: float) -> int:
    return int(max(0, min(100, round(value))))


def score_access(cong_enc: str, access_enc: str) -> int:
    cong = parse_int(cong_enc, 2)
    acc = parse_int(access_enc, 2)
    if cong == 0:
        cong = 2
    if acc == 0:
        acc = 2
    raw = 100 - (cong - 1) * 28 - (acc - 1) * 18
    return clamp_score(raw)


def score_workflow(activity_enc: str, workflow_enc: str, dri_config: dict) -> int:
    expected = dri_config["activity_workflow_map"].get(activity_enc, [])
    if not expected:
        return 50
    if workflow_enc in expected:
        return 100
    return 25


def score_coexistence(
    labour: str,
    robot_ops: str,
    video_cat_enc: str,
    cong_enc: str,
) -> int:
    if video_cat_enc != "1":
        return 0
    ops = parse_int(robot_ops, 0)
    lab = parse_int(labour, 0)
    cong = parse_int(cong_enc, 2)

    ops_score = 70 if ops >= 1 else 40 if ops == 0 else 50
    if lab == 0:
        lab_score = 85
    elif lab <= 6:
        lab_score = 90
    elif lab <= 10:
        lab_score = 65
    else:
        lab_score = 40

    cong_penalty = max(0, (cong - 1) * 12)
    return clamp_score(ops_score * 0.45 + lab_score * 0.45 - cong_penalty * 0.1)


def score_surface(activity_enc: str, surface_enc: str, dri_config: dict) -> int:
    fresh_acts = set(dri_config["fresh_concrete_activity_enc"])
    post_acts = set(dri_config["post_cast_activity_enc"])
    wet = set(dri_config["wet_surface_enc"])
    hard = set(dri_config["hardened_surface_enc"])

    if activity_enc in fresh_acts:
        return 100 if surface_enc in wet else 20 if surface_enc != "0" else 50
    if activity_enc in post_acts:
        return 100 if surface_enc in hard else 20 if surface_enc != "0" else 50
    if surface_enc == "0":
        return 75
    return 80


def score_evidence(evidence_enc: str, confidence_enc: str) -> int:
    ev = parse_int(evidence_enc, 2)
    conf = parse_int(confidence_enc, 2)
    ev_pts = 100 if ev == 1 else 70
    conf_pts = {1: 60, 2: 80, 3: 100}.get(conf, 70)
    return clamp_score(ev_pts * 0.5 + conf_pts * 0.5)


def weighted_total(scores: dict[str, int], weights: dict[str, float]) -> int:
    total = sum(scores[dim] * weights[dim] for dim in weights)
    return clamp_score(total)


def classify_band(score: int | None, bands: dict) -> str:
    if score is None:
        return "not_applicable"
    if score <= bands["low"][1]:
        return "low"
    if score <= bands["medium"][1]:
        return "medium"
    return "high"


def record_type_from_seed(seed: dict[str, str]) -> tuple[str, str, bool, bool]:
    video_cat = seed.get("video_category_enc", "")
    activity = seed.get("activity_group", "")
    if video_cat == "1":
        if activity == "fresh_concrete_leveling":
            family = "SF-ROBOT-FRESH-CONCRETE"
        elif seed.get("workflow_stage_enc") == "3":
            family = "SF-ROBOT-POST-CAST"
        else:
            family = "SF-DEPLOYMENT-JOINT"
        return "robot_seed", family, True, False
    return "mivan_seed", "SF-MIVAN-SLAB-CYCLE", False, True


def record_type_from_synthetic(syn: dict[str, str]) -> tuple[str, str, bool, bool]:
    family = syn.get("scenario_family", "")
    video_cat = syn.get("video_category_enc", "")
    if family == "SF-DEPLOYMENT-JOINT":
        return "joint_synthetic", family, True, False
    if video_cat == "1":
        return "robot_synthetic", family, True, False
    return "mivan_synthetic", family, False, True


def feature_row_from_seed(seed: dict[str, str]) -> dict[str, str]:
    return {
        "video_category_enc": seed.get("video_category_enc", ""),
        "activity_group_enc": str(
            load_yaml(GEN_CONFIG_PATH)["activity_group"].get(seed.get("activity_group", ""), 0)
        ),
        "workflow_stage_enc": seed.get("workflow_stage_enc", ""),
        "operating_surface_enc": seed.get("operating_surface_enc", ""),
        "congestion_level_enc": seed.get("congestion_level_enc", ""),
        "access_condition_enc": seed.get("access_condition_enc", ""),
        "evidence_level_enc": seed.get("evidence_level_enc", ""),
        "coding_confidence_enc": seed.get("coding_confidence_enc", ""),
        "labour_count_visible": seed.get("labour_count_visible", "0") or "0",
        "robot_operator_count": seed.get("robot_operator_count", "0") or "0",
    }


def score_record(
    features: dict[str, str],
    *,
    dri_applicable: bool,
    sci_only: bool,
    dri_config: dict,
    scoring_date: str,
    record_id: str,
    record_type: str,
    source_table: str,
    scenario_family: str,
) -> dict[str, str]:
    access = score_access(features["congestion_level_enc"], features["access_condition_enc"])
    workflow = score_workflow(
        features["activity_group_enc"],
        features["workflow_stage_enc"],
        dri_config,
    )
    coexistence = score_coexistence(
        features["labour_count_visible"],
        features["robot_operator_count"],
        features["video_category_enc"],
        features["congestion_level_enc"],
    )
    surface = score_surface(
        features["activity_group_enc"],
        features["operating_surface_enc"],
        dri_config,
    )
    evidence = score_evidence(
        features["evidence_level_enc"],
        features["coding_confidence_enc"],
    )

    dim_weights = {k: v["weight"] for k, v in dri_config["dimensions"].items()}
    dim_scores = {
        "work_zone_access": access,
        "workflow_fit": workflow,
        "human_robot_coexistence": coexistence,
        "surface_task_alignment": surface,
        "evidence_confidence": evidence,
    }

    dri_total: int | None = None
    sci_total: int | None = None

    if dri_applicable:
        dri_total = weighted_total(dim_scores, dim_weights)
    if sci_only:
        sci_weights = {k: v["weight"] for k, v in dri_config["sci_dimensions"].items()}
        sci_total = weighted_total(
            {"work_zone_access": access, "workflow_fit": workflow},
            sci_weights,
        )

    band = classify_band(dri_total if dri_applicable else sci_total, dri_config["bands"])
    if not dri_applicable and sci_only:
        band = classify_band(sci_total, dri_config["bands"])

    return {
        "record_id": record_id,
        "record_type": record_type,
        "source_table": source_table,
        "scenario_family": scenario_family,
        "dri_applicable": "yes" if dri_applicable else "no",
        "sci_only": "yes" if sci_only and not dri_applicable else "no",
        "dri_access_score": str(access),
        "dri_workflow_score": str(workflow),
        "dri_coexistence_score": str(coexistence),
        "dri_surface_score": str(surface),
        "dri_evidence_score": str(evidence),
        "dri_total_score": str(dri_total) if dri_total is not None else "",
        "sci_total_score": str(sci_total) if sci_total is not None else "",
        "dri_band": band if dri_applicable or sci_only else "not_applicable",
        "dri_rank": "",
        "score_provenance": dri_config["output"]["score_provenance"],
        "scoring_date": scoring_date,
    }


def assign_ranks(rows: list[dict[str, str]]) -> None:
    applicable = [r for r in rows if r.get("dri_applicable") == "yes" and r.get("dri_total_score")]
    applicable.sort(key=lambda r: int(r["dri_total_score"]), reverse=True)
    for rank, row in enumerate(applicable, start=1):
        row["dri_rank"] = str(rank)


def load_synthetic_rows(use_all: bool) -> list[dict[str, str]]:
    rows = read_csv(SYNTH_PATH) if SYNTH_PATH.exists() else []
    if use_all and GAN_SYNTH_PATH.exists():
        rows = rows + read_csv(GAN_SYNTH_PATH)
    return rows


def compute_all(*, use_all_synthetic: bool = False) -> dict:
    dri_config = load_yaml(CONFIG_PATH)
    scoring_date = date.today().isoformat()
    scored: list[dict[str, str]] = []

    for seed in read_csv(SEED_PATH):
        features = feature_row_from_seed(seed)
        rtype, family, dri_ok, sci = record_type_from_seed(seed)
        scored.append(
            score_record(
                features,
                dri_applicable=dri_ok,
                sci_only=sci,
                dri_config=dri_config,
                scoring_date=scoring_date,
                record_id=seed["seed_id"],
                record_type=rtype,
                source_table="gan_seed_dataset",
                scenario_family=family,
            )
        )

    for syn in load_synthetic_rows(use_all_synthetic):
        features = {k: syn.get(k, "") for k in [
            "video_category_enc", "activity_group_enc", "workflow_stage_enc",
            "operating_surface_enc", "congestion_level_enc", "access_condition_enc",
            "evidence_level_enc", "coding_confidence_enc",
            "labour_count_visible", "robot_operator_count",
        ]}
        rtype, family, dri_ok, sci = record_type_from_synthetic(syn)
        source = "synthetic_scenario_dataset_gan" if syn.get("generation_method", "").startswith("tabular") else "synthetic_scenario_dataset"
        scored.append(
            score_record(
                features,
                dri_applicable=dri_ok,
                sci_only=sci,
                dri_config=dri_config,
                scoring_date=scoring_date,
                record_id=syn["scenario_id"],
                record_type=rtype,
                source_table=source,
                scenario_family=family,
            )
        )

    assign_ranks(scored)
    write_csv(OUT_PATH, OUTPUT_HEADER, scored)
    write_report(scored, scoring_date)
    return {"scored_count": len(scored), "dri_applicable": sum(1 for r in scored if r["dri_applicable"] == "yes")}


def write_report(rows: list[dict[str, str]], scoring_date: str) -> None:
    applicable = [r for r in rows if r.get("dri_applicable") == "yes"]
    bands = {}
    for r in applicable:
        b = r.get("dri_band", "?")
        bands[b] = bands.get(b, 0) + 1

    lines = [
        "# DRI Scoring Report (Phase 3C Framework)",
        "",
        f"**Generated:** {scoring_date} by `src/compute_dri_scores.py`",
        "",
        "> Scenario-relative framework demonstration. **Not field-validated.**",
        "",
        "## Summary",
        "",
        f"- Total records scored: {len(rows)}",
        f"- Full DRI applicable: {len(applicable)}",
        f"- SCI-only (Mivan context): {sum(1 for r in rows if r.get('sci_only') == 'yes')}",
        "",
        "## DRI band distribution (applicable records)",
        "",
    ]
    for band, count in sorted(bands.items()):
        lines.append(f"- {band}: {count}")
    lines.extend([
        "",
        "## Top 5 DRI-ranked scenarios",
        "",
        "| rank | record_id | type | DRI | band |",
        "|------|-----------|------|-----|------|",
    ])
    top = sorted(applicable, key=lambda r: int(r["dri_rank"] or 999))[:5]
    for r in top:
        lines.append(
            f"| {r['dri_rank']} | {r['record_id']} | {r['record_type']} | "
            f"{r['dri_total_score']} | {r['dri_band']} |"
        )
    lines.extend([
        "",
        "## Output",
        "",
        "- `data/dri_scored_scenarios.csv`",
        "",
    ])
    report_path = ROOT / "reports" / "dri_scoring_report.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--all-synthetic",
        action="store_true",
        help="Include GAN pilot scenarios in DRI scoring",
    )
    args = parser.parse_args()

    if not SEED_PATH.exists() or not SYNTH_PATH.exists():
        print("Missing seed or synthetic dataset.")
        return 1
    result = compute_all(use_all_synthetic=args.all_synthetic)
    print(f"Phase 3C DRI scoring complete: {result['scored_count']} records ({result['dri_applicable']} full DRI).")
    print(f"Output: {OUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
