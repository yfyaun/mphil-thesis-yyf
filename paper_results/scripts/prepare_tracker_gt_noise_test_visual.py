"""Create the requested test-split GT-noise tracker visualization.

This is a qualitative plot only. It does not run learning inference or the
beam-management PHY simulation: GT detections receive a fixed 1.0 m position
noise realization and are passed through the three existing tracker configs.
The resulting PNG is stored with the paper raw snapshot so the main paper-asset
builder can copy it without rerunning tracking.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


WORKSPACE = Path(__file__).resolve().parents[2]
TRACKING_ROOT = WORKSPACE / "mmbeam-tracking"
OUTPUT = (
    WORKSPACE
    / "paper_results"
    / "raw"
    / "tracking"
    / "visualizations"
    / "test_clear_day_bs_ne_three_trackers_noise_1_0m.png"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prepare the GT-noise test tracker figure for paper export.")
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if OUTPUT.is_file() and not args.force:
        print(f"[skip] {OUTPUT}")
        return
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    command = [
        sys.executable,
        "scripts/visualize_tracks.py",
        "--split",
        "test",
        "--weather-id",
        "clear_day",
        "--bs-id",
        "bs_ne",
        "--max-frames",
        "100",
        "--position-noise-std-m",
        "1.0",
        "--seed",
        "2026",
        "--tracker-configs",
        (
            "KF-CV=configs/tracker/kf_cv_beam_management_v2.yaml,"
            "KF-CT=configs/tracker/kf_ct_beam_management_v2.yaml,"
            "IMM=configs/tracker/imm_cv_ct_beam_management_v2.yaml"
        ),
        "--title",
        "GT detections + 1.0 m position noise (test, clear day, BS NE)",
        "--output",
        str(OUTPUT),
    ]
    subprocess.run(command, cwd=TRACKING_ROOT, check=True)
    if not OUTPUT.is_file():
        raise RuntimeError(f"Tracker visualization was not written: {OUTPUT}")
    print(f"[complete] {OUTPUT}")


if __name__ == "__main__":
    main()
