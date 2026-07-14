"""Freeze completed Top-1 CE tracker-ablation results into paper_results/raw."""

from __future__ import annotations

import json
import shutil
from pathlib import Path


WORKSPACE = Path(__file__).resolve().parents[2]
SOURCE_ROOT = WORKSPACE / "mmbeam-tracking" / "artifacts" / "v9_paper" / "top1ce_tracker_completion"
IMM_BASE_SOURCE_ROOT = (
    WORKSPACE
    / "mmbeam-tracking"
    / "artifacts"
    / "v9_paper"
    / "beam_management"
    / "final_test_9p9s_v7_training_latency_weather_tuned_tracker_bm_v2"
    / "loss_ablation"
    / "csi5ms"
)
IMM_RAIN_REFRESH_SOURCE_ROOT = (
    WORKSPACE / "mmbeam-tracking" / "artifacts" / "v9_paper" / "r9m010" / "loss_ablation" / "csi5ms"
)
DESTINATION_ROOT = WORKSPACE / "paper_results" / "raw" / "beam_management" / "v9" / "tracker_top1ce"
WEATHERS = ("clear_day", "rain_fog_day", "night")
TRACKERS = ("imm_bm_v2", "kf_cv_bm_v2", "kf_ct_bm_v2")


def main() -> None:
    comparison = SOURCE_ROOT / "tracker_ablation_comparison.json"
    manifest = SOURCE_ROOT / "final_manifest.json"
    if not comparison.is_file() or not manifest.is_file():
        raise FileNotFoundError(f"Incomplete completed tracker suite: {SOURCE_ROOT}")
    payload = json.loads(comparison.read_text(encoding="utf-8"))
    expected = {(weather, tracker) for weather in WEATHERS for tracker in TRACKERS}
    found = {(row["weather_id"], row["tracker"]) for row in payload["rows"]}
    if found != expected:
        raise RuntimeError(f"Unexpected completed tracker rows: {sorted(found)}")

    DESTINATION_ROOT.mkdir(parents=True, exist_ok=True)
    for name in ("tracker_ablation_comparison.json", "tracker_ablation_comparison.csv", "final_manifest.json"):
        shutil.copy2(SOURCE_ROOT / name, DESTINATION_ROOT / name)
    for weather in WEATHERS:
        for tracker in TRACKERS:
            if tracker == "imm_bm_v2":
                # Rain/fog was refreshed with the final margin=0.10 gate; clear and
                # night retain their completed V9 Top-1 CE runs.
                imm_root = IMM_RAIN_REFRESH_SOURCE_ROOT if weather == "rain_fog_day" else IMM_BASE_SOURCE_ROOT
                source = imm_root / weather / "top1_ce_cross_agent" / "summary.json"
            else:
                source = SOURCE_ROOT / "tracker_ablation" / "csi5ms" / weather / tracker / "summary.json"
            if not source.is_file():
                raise FileNotFoundError(source)
            destination = DESTINATION_ROOT / "run_summaries" / weather / tracker / "summary.json"
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
    (DESTINATION_ROOT / "raw_manifest.json").write_text(
        json.dumps(
            {
                "format": "paper_tracker_top1ce_raw_v1",
                "completed_suite": str(SOURCE_ROOT),
                "imm_summary_sources": {
                    "clear_day": str(IMM_BASE_SOURCE_ROOT),
                    "rain_fog_day": str(IMM_RAIN_REFRESH_SOURCE_ROOT),
                    "night": str(IMM_BASE_SOURCE_ROOT),
                },
                "detector": "v3_rt_anchor_beam_top1_ce_cross_agent",
                "trackers": list(TRACKERS),
                "weathers": list(WEATHERS),
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"[complete] {DESTINATION_ROOT}")


if __name__ == "__main__":
    main()
