"""Phase 3B: Tabular CTGAN/TVAE pilot on modelling feature matrix."""

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

from src.expand_scenarios import (  # noqa: E402
    FEATURE_COLS,
    OUTPUT_HEADER,
    allowed_access_for_congestion,
    fingerprint,
    pilot_metadata,
    read_csv,
    validate_feature_row,
    write_csv,
)
from src.validate_scenario_constraints import validate_scenario_row  # noqa: E402

DATA_DIR = ROOT / "data"
REPORTS_DIR = ROOT / "reports"
PILOT_CONFIG = ROOT / "config" / "tabular_gan_pilot_config.yaml"
GEN_CONFIG = ROOT / "config" / "generative_augmentation_config.yaml"
MATRIX_PATH = DATA_DIR / "modelling_feature_matrix.csv"
SEED_PATH = DATA_DIR / "gan_seed_dataset.csv"
RULE_PATH = DATA_DIR / "synthetic_scenario_dataset.csv"


def load_yaml(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def load_training_frame():
    import pandas as pd

    df = pd.read_csv(MATRIX_PATH)
    return df[[c for c in FEATURE_COLS if c in df.columns]]


def build_synthesizer(model_name: str, train_df, epochs: int, batch_size: int, verbose: bool):
    from sdv.metadata import Metadata
    from sdv.single_table import CTGANSynthesizer, TVAESynthesizer

    metadata = Metadata.detect_from_dataframe(train_df)
    if model_name == "tvae":
        return TVAESynthesizer(metadata, epochs=epochs, batch_size=batch_size, verbose=verbose)
    return CTGANSynthesizer(metadata, epochs=epochs, batch_size=batch_size, verbose=verbose)


def clamp_column(name: str, value, ranges: dict) -> str:
    bounds = ranges.get(name, [0, 99])
    low, high = int(bounds[0]), int(bounds[1])
    try:
        num = int(round(float(value)))
    except (TypeError, ValueError):
        num = low
    return str(max(low, min(high, num)))


def discretize_sample(row: dict, ranges: dict) -> dict[str, str]:
    out = {col: clamp_column(col, row.get(col, 0), ranges) for col in FEATURE_COLS}
    cong = out["congestion_level_enc"]
    allowed = allowed_access_for_congestion(cong)
    if out["access_condition_enc"] not in allowed:
        out["access_condition_enc"] = allowed[0]
    if out["video_category_enc"] == "0":
        out["robot_operator_count"] = "0"
        if int(out["labour_count_visible"]) < 2:
            out["labour_count_visible"] = "2"
    else:
        if int(out["labour_count_visible"]) > 0 and int(out["labour_count_visible"]) < 12:
            pass
        elif out["video_category_enc"] == "1" and int(out["labour_count_visible"]) > 8:
            out["labour_count_visible"] = "0"
    return out


def scenario_family_from_features(features: dict[str, str]) -> str:
    video_cat = features.get("video_category_enc", "")
    activity = features.get("activity_group_enc", "")
    workflow = features.get("workflow_stage_enc", "")
    if video_cat == "0":
        return "SF-MIVAN-SLAB-CYCLE"
    if activity == "4":
        return "SF-ROBOT-FRESH-CONCRETE"
    if workflow == "3":
        return "SF-ROBOT-POST-CAST"
    return "SF-DEPLOYMENT-JOINT"


def validate_gan_row(features: dict[str, str], gen_config: dict, row_id: str) -> tuple[bool, int, str]:
    validity, violations = validate_feature_row(features, gen_config, row_id)
    if validity == "fail":
        return False, violations, validity
    partial = validate_scenario_row(
        {
            "activity_group_enc": features["activity_group_enc"],
            "workflow_stage_enc": features["workflow_stage_enc"],
            "operating_surface_enc": features["operating_surface_enc"],
            "congestion_level_enc": features["congestion_level_enc"],
            "access_condition_enc": features["access_condition_enc"],
        },
        gen_config,
        row_id,
    )
    if partial.errors:
        return False, violations + len(partial.errors), "fail"
    return True, violations + len(partial.warnings), validity


def seed_fingerprints() -> set[tuple[str, ...]]:
    matrix = read_csv(MATRIX_PATH)
    return {fingerprint({c: r.get(c, "") for c in FEATURE_COLS}) for r in matrix}


def select_diverse(candidates: list[dict[str, str]], target: int) -> list[dict[str, str]]:
    if len(candidates) <= target:
        return candidates
    selected: list[dict[str, str]] = []
    seen: set[tuple[str, ...]] = set()
    buckets = {
        "SF-MIVAN-SLAB-CYCLE": [],
        "SF-ROBOT-FRESH-CONCRETE": [],
        "SF-ROBOT-POST-CAST": [],
        "SF-DEPLOYMENT-JOINT": [],
    }
    for row in candidates:
        buckets[row["scenario_family"]].append(row)

    def pick(pool: list[dict[str, str]], n: int) -> None:
        for row in pool:
            if n <= 0 or len(selected) >= target:
                break
            fp = fingerprint({c: row.get(c, "") for c in FEATURE_COLS})
            if fp in seen:
                continue
            seen.add(fp)
            selected.append(row)
            n -= 1

    pick(buckets["SF-ROBOT-FRESH-CONCRETE"], 14)
    pick(buckets["SF-DEPLOYMENT-JOINT"], 10)
    pick(buckets["SF-MIVAN-SLAB-CYCLE"], 14)
    pick(buckets["SF-ROBOT-POST-CAST"], 8)
    bright = [r for r in candidates if r.get("manufacturer_name_enc") == "2"]
    pick(bright, 4)

    for row in candidates:
        if len(selected) >= target:
            break
        fp = fingerprint({c: row.get(c, "") for c in FEATURE_COLS})
        if fp not in seen:
            seen.add(fp)
            selected.append(row)
    return selected[:target]


def generate_candidates(train_df, pilot_config: dict, model_used: str):
    model_cfg = pilot_config["model"]
    gen_cfg = pilot_config["generation"]
    synthesizer = build_synthesizer(
        model_used,
        train_df,
        epochs=int(model_cfg["epochs"]),
        batch_size=int(model_cfg["batch_size"]),
        verbose=bool(model_cfg.get("verbose", False)),
    )
    synthesizer.fit(train_df)
    sample = synthesizer.sample(num_rows=int(gen_cfg["candidate_pool"]))
    return sample


def run_pilot() -> dict:
    pilot_config = load_yaml(PILOT_CONFIG)
    gen_config = load_yaml(GEN_CONFIG)
    ranges = pilot_config["column_ranges"]
    target = int(pilot_config["generation"]["target_export"])
    generation_date = date.today().isoformat()
    seed_fps = seed_fingerprints()

    train_df = load_training_frame()
    model_used = pilot_config["model"]["primary"]
    try:
        raw_samples = generate_candidates(train_df, pilot_config, model_used)
    except Exception as exc:
        model_used = pilot_config["model"]["fallback"]
        raw_samples = generate_candidates(train_df, pilot_config, model_used)
        fallback_reason = str(exc)
    else:
        fallback_reason = ""

    method_tag = (
        pilot_config["output"]["generation_method_ctgan"]
        if model_used == "ctgan"
        else pilot_config["output"]["generation_method_tvae"]
    )

    candidates: list[dict[str, str]] = []
    rejected = 0
    for idx, row in raw_samples.iterrows():
        features = discretize_sample(row.to_dict(), ranges)
        fp = fingerprint(features)
        if fp in seed_fps:
            rejected += 1
            continue
        temp_id = f"GANC-{idx}"
        ok, violations, validity = validate_gan_row(features, gen_config, temp_id)
        if not ok:
            rejected += 1
            continue
        family = scenario_family_from_features(features)
        candidates.append(
            {
                "is_synthetic": "yes",
                "generation_method": method_tag,
                "source_seed_id": "gan_pilot_training_set",
                "scenario_family": family,
                "logical_validity": validity,
                "constraint_violation_count": str(violations),
                "synthetic_provenance": pilot_config["output"]["synthetic_provenance"],
                "generation_date": generation_date,
                **pilot_metadata(
                    generation_method=method_tag,
                    note=f"TVAE/CTGAN pilot from n=14 seeds; {model_used} model",
                ),
                **features,
            }
        )

    selected = select_diverse(candidates, target)
    for i, row in enumerate(selected, start=1):
        row["scenario_id"] = f"SYN-GAN-{i:03d}"

    gan_path = DATA_DIR / pilot_config["output"]["gan_dataset"]
    write_csv(gan_path, OUTPUT_HEADER, selected)

    combined: list[dict[str, str]] = []
    if RULE_PATH.exists():
        combined.extend(read_csv(RULE_PATH))
    combined.extend(selected)
    combined_path = DATA_DIR / pilot_config["output"]["combined_dataset"]
    write_csv(combined_path, OUTPUT_HEADER, combined)

    write_report(
        model_used=model_used,
        fallback_reason=fallback_reason,
        target=target,
        pool=len(raw_samples),
        valid_candidates=len(candidates),
        exported=len(selected),
        rejected=rejected,
        generation_date=generation_date,
        selected=selected,
    )

    return {
        "model": model_used,
        "exported": len(selected),
        "valid_candidates": len(candidates),
        "rejected": rejected,
        "combined_total": len(combined),
    }


def write_report(
    *,
    model_used: str,
    fallback_reason: str,
    target: int,
    pool: int,
    valid_candidates: int,
    exported: int,
    rejected: int,
    generation_date: str,
    selected: list[dict[str, str]],
) -> None:
    families: dict[str, int] = {}
    for row in selected:
        fam = row.get("scenario_family", "?")
        families[fam] = families.get(fam, 0) + 1

    lines = [
        "# Tabular GAN/VAE Pilot Report (Phase 3B)",
        "",
        f"**Generated:** {generation_date} by `src/generate_tabular_gan_pilot.py`",
        "",
        f"- Model used: **{model_used.upper()}**",
        f"- Training rows: 14 (modelling_feature_matrix.csv)",
        f"- Candidate pool sampled: {pool}",
        f"- Valid after constraint filter: {valid_candidates}",
        f"- Rejected: {rejected}",
        f"- Exported GAN scenarios: {exported} (target {target})",
        "",
    ]
    if fallback_reason:
        lines.extend([f"- Primary model failed; fallback used. Reason: {fallback_reason}", ""])
    lines.append("## Scenario families (GAN export)")
    lines.append("")
    for fam, count in sorted(families.items()):
        lines.append(f"- {fam}: {count}")
    lines.extend([
        "",
        "## Outputs",
        "",
        "- `data/synthetic_scenario_dataset_gan.csv`",
        "- `data/synthetic_scenario_dataset_all.csv` (50 rule + 50 GAN)",
        "",
        "## Research-safe note",
        "",
        "Pilot trained on n=14 seeds. Outputs are post-filtered synthetic scenarios, "
        "not field-validated performance data.",
        "",
    ])
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    (REPORTS_DIR / "tabular_gan_pilot_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    if not MATRIX_PATH.exists():
        print(f"Missing {MATRIX_PATH}")
        return 1
    try:
        import pandas  # noqa: F401
        import sdv  # noqa: F401
    except ImportError:
        print("Phase 3B requires: pip install -r requirements-gan-pilot.txt")
        return 1

    result = run_pilot()
    print(
        f"Phase 3B complete ({result['model']}): {result['exported']} GAN scenarios, "
        f"{result['combined_total']} combined."
    )
    print(f"Report: {REPORTS_DIR / 'tabular_gan_pilot_report.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
