"""Regenerate CSV templates from current data headers."""

from __future__ import annotations

import csv
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
TEMPLATES = DATA / "templates"

TEMPLATE_MAP = {
    "video_metadata_template.csv": "video_metadata.csv",
    "video_segments_template.csv": "video_segments.csv",
    "robot_video_observations_template.csv": "robot_video_observations.csv",
    "mivan_video_observations_template.csv": "mivan_video_observations.csv",
    "manufacturer_specs_template.csv": "manufacturer_specs.csv",
    "cleaned_video_dataset_template.csv": "cleaned_video_dataset.csv",
}


def main() -> None:
    TEMPLATES.mkdir(parents=True, exist_ok=True)
    for template_name, source_name in TEMPLATE_MAP.items():
        source = DATA / source_name
        dest = TEMPLATES / template_name
        with source.open(newline="", encoding="utf-8") as handle:
            reader = csv.reader(handle)
            header = next(reader)
        with dest.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(header)
        print(f"Wrote {dest}")


if __name__ == "__main__":
    main()
