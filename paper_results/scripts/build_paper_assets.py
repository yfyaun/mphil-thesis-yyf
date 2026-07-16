"""Regenerate all current paper figures and tables from paper_results/raw.

The script deliberately reads the frozen raw snapshot only. It does not access
training checkpoints, run beam-management simulations, or regenerate learning
evaluations. Use ``prepare_tracker_gt_noise_test_visual.py`` once to place the
requested test-split qualitative tracker visual in ``raw/tracking``.
"""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D


PAPER_ROOT = Path(__file__).resolve().parents[1]
RAW_ROOT = PAPER_ROOT / "raw"
TABLE_ROOT = PAPER_ROOT / "tables"
FIGURE_ROOT = PAPER_ROOT / "figures"
METADATA_ROOT = PAPER_ROOT / "metadata"
LEGACY_TRACKING_ROOT = PAPER_ROOT / "tracking"
WEATHERS = ("clear_day", "rain_fog_day", "night")
WEATHER_LABELS = {"clear_day": "Clear", "rain_fog_day": "Rain/Fog", "night": "Night"}
CONDITION_LABELS = {
    "conventional_4beam": "SSB-guided refinement (K = 4)",
    "conventional_12beam": "SSB-guided refinement (K = 12)",
    "sensing_imm": "DMSA-BM",
}
TRACKER_LABELS = {
    "imm_bm_v2": "IMM",
    "kf_cv_bm_v2": "KF-CV",
    "kf_ct_bm_v2": "KF-CT",
}
SENSING_CONFIGURATION_LABELS = {
    "camera_only": "Camera-only",
    "isac_only": "ISAC-only",
    "single_station_multimodal": "Local camera--ISAC fusion",
}
LEARNING_METHODS = (
    ("Camera-only", "v3_rt_anchor_modalities_camera_concat_power_kl_ranking"),
    ("ISAC-only", "v3_rt_anchor_modalities_isac_concat_power_kl_ranking"),
    ("Local camera--ISAC fusion", "v3_rt_anchor_modalities_multimodal_mean_concat_power_kl_ranking"),
    ("Distributed mean fusion", "v3_rt_anchor_node_fusion_multimodal_node_mean_power_kl_ranking"),
    ("Distributed multimodal attention (proposed)", "v3_rt_anchor_beam_top1_ce_cross_agent"),
)
NODE_FUSION_LABELS = {
    "Cross-agent + gated fusion": "Distributed fusion with learned gating",
    "Cross-agent attention": "Distributed multimodal attention (proposed)",
    "Node masked mean": "Distributed mean fusion",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build paper tables and figures from frozen raw results.")
    parser.add_argument("--clean", action="store_true", help="Remove prior paper tables/figures before export.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    _validate_inputs()
    if args.clean:
        _clean_outputs()
    TABLE_ROOT.mkdir(parents=True, exist_ok=True)
    FIGURE_ROOT.mkdir(parents=True, exist_ok=True)
    METADATA_ROOT.mkdir(parents=True, exist_ok=True)

    learning_summary = _read_json(RAW_ROOT / "learning" / "v3_rt_anchor_paper_test" / "summary.json")
    node_summary = _read_json(RAW_ROOT / "learning" / "v3_rt_anchor_node_fusion_sn_count_test" / "summary.json")
    core_summary = _read_json(RAW_ROOT / "beam_management" / "v9" / "core_comparison.json")
    modality_summary = _read_json(
        RAW_ROOT / "beam_management" / "v9" / "modality_ablation_comparison.json"
    )
    tracker_summary = _read_json(
        RAW_ROOT / "beam_management" / "v9" / "tracker_top1ce" / "tracker_ablation_comparison.json"
    )
    core_user_counts = _load_core_unique_ue_counts()
    modality_user_counts = _load_modality_unique_ue_counts()
    tracker_user_counts = _load_tracker_unique_ue_counts()

    _export_learning_tables(learning_summary)
    _export_node_count_table_and_figures(node_summary)
    _export_core_table(core_summary, core_user_counts)
    _export_sensing_configuration_table(
        core_summary,
        core_user_counts,
        modality_summary,
        modality_user_counts,
    )
    _export_tracker_table(tracker_summary, tracker_user_counts)
    _copy_tracker_visual()
    _write_manifest()
    print(json.dumps({"status": "complete", "tables": str(TABLE_ROOT), "figures": str(FIGURE_ROOT)}, ensure_ascii=False))


def _validate_inputs() -> None:
    required = (
        RAW_ROOT / "learning" / "v3_rt_anchor_paper_test" / "summary.json",
        RAW_ROOT / "learning" / "v3_rt_anchor_node_fusion_sn_count_test" / "summary.json",
        RAW_ROOT / "beam_management" / "v9" / "core_comparison.json",
        RAW_ROOT / "beam_management" / "v9" / "modality_ablation_comparison.json",
        RAW_ROOT / "beam_management" / "v9" / "tracker_top1ce" / "tracker_ablation_comparison.json",
        RAW_ROOT / "tracking" / "visualizations" / "test_clear_day_bs_ne_three_trackers_noise_1_0m.png",
    )
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise FileNotFoundError(
            "Missing frozen raw inputs. Run prepare_tracker_gt_noise_test_visual.py once for the tracker image: "
            + "; ".join(missing)
        )


def _load_core_unique_ue_counts() -> dict[tuple[str, str], int]:
    """Read the simulated UE population for the selected core rows.

    The paper sensing row is the existing Top-1 CE + IMM loss-ablation run;
    conventional rows originate from the core group.  The rain/fog Top-1 CE
    summary has the same 32 UE population as its refreshed selected result, so
    it supplies the denominator while ``core_comparison.json`` supplies the
    selected, gate-refreshed numerator.
    """
    root = RAW_ROOT / "beam_management" / "v9" / "run_summaries"
    counts: dict[tuple[str, str], int] = {}
    for weather in WEATHERS:
        for condition in CONDITION_LABELS:
            group, name = (
                ("loss_ablation", "top1_ce_cross_agent")
                if condition == "sensing_imm"
                else ("core", condition)
            )
            summary = _read_json(root / group / "csi5ms" / weather / name / "summary.json")
            count = int(summary["unique_ue_count"])
            if count <= 0:
                raise ValueError(f"Invalid unique_ue_count for {weather}/{condition}: {count}")
            counts[(weather, condition)] = count
    return counts


def _load_tracker_unique_ue_counts() -> dict[tuple[str, str], int]:
    root = RAW_ROOT / "beam_management" / "v9" / "tracker_top1ce" / "run_summaries"
    counts: dict[tuple[str, str], int] = {}
    for weather in WEATHERS:
        for tracker in TRACKER_LABELS:
            summary = _read_json(root / weather / tracker / "summary.json")
            count = int(summary["unique_ue_count"])
            if count <= 0:
                raise ValueError(f"Invalid unique_ue_count for {weather}/{tracker}: {count}")
            counts[(weather, tracker)] = count
    return counts


def _load_modality_unique_ue_counts() -> dict[tuple[str, str], int]:
    root = RAW_ROOT / "beam_management" / "v9" / "run_summaries" / "modality_ablation" / "csi5ms"
    counts: dict[tuple[str, str], int] = {}
    for weather in WEATHERS:
        for detector in SENSING_CONFIGURATION_LABELS:
            summary = _read_json(root / weather / detector / "summary.json")
            count = int(summary["unique_ue_count"])
            if count <= 0:
                raise ValueError(f"Invalid unique_ue_count for {weather}/{detector}: {count}")
            counts[(weather, detector)] = count
    return counts


def _clean_outputs() -> None:
    # The requested reset applies to the official output folders and the
    # previous nested tracking paper tables/figures. Raw data and scripts stay intact.
    for path in (TABLE_ROOT, FIGURE_ROOT, LEGACY_TRACKING_ROOT / "tables", LEGACY_TRACKING_ROOT / "figures"):
        resolved = path.resolve()
        if PAPER_ROOT.resolve() not in resolved.parents:
            raise RuntimeError(f"Refusing to clean outside paper_results: {resolved}")
        if path.exists():
            shutil.rmtree(path)


def _read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _export_learning_tables(summary: dict[str, Any]) -> None:
    overall = {row["experiment"]: row for row in summary["overall_results"]}
    weather = {
        (row["experiment"], _row_weather(row)): row
        for row in summary["weather_results"]
    }
    headers = ["Method", "AP@2m (%)", "Recall@2m (%)", "Beam Top-1@2m (%)", "Beam Top-4@2m (%)", "Top-4 power ratio (%)"]
    overall_rows = [_learning_table_row(label, overall[experiment]) for label, experiment in LEARNING_METHODS]
    _write_table("table_01_learning_modalities_overall", headers, overall_rows)

    weather_rows: list[list[str]] = []
    for weather_id in WEATHERS:
        for label, experiment in LEARNING_METHODS:
            weather_rows.append([WEATHER_LABELS[weather_id], *_learning_table_row(label, weather[(experiment, weather_id)])])
    _write_table("table_02_learning_modalities_by_weather", ["Weather", *headers], weather_rows)


def _row_weather(row: dict[str, Any]) -> str:
    if row.get("weather_id"):
        return str(row["weather_id"])
    weather_ids = row.get("weather_ids", [])
    if len(weather_ids) == 1:
        return str(weather_ids[0])
    raise ValueError(f"Weather-specific learning row lacks a unique weather identifier: {row.get('experiment')}")


def _learning_table_row(label: str, row: dict[str, Any]) -> list[str]:
    recall = float(row["det_match_count"]) / float(row["det_num_gt"])
    return [
        label,
        _pct(row["det_ap_dist_2_0m"]),
        _pct(recall),
        _pct(row["beam_top1_dist_2_0m"]),
        _pct(row["beam_top4_dist_2_0m"]),
        _pct(row["beam_pred_top4_power_ratio"]),
    ]


def _export_node_count_table_and_figures(summary: dict[str, Any]) -> None:
    records: list[dict[str, Any]] = []
    for result in summary["results"]:
        raw_label = str(result["label"])
        label = NODE_FUSION_LABELS.get(raw_label, raw_label)
        evaluations = result["evaluation"]["results"]
        for raw_count, payload in evaluations.items():
            metrics = payload["overall"]["metrics"]
            records.append(
                {
                    "label": label,
                    "node_count": int(raw_count),
                    "ap": float(metrics["det_ap_dist_2_0m"]),
                    "recall": float(metrics["det_match_count"]) / float(metrics["det_num_gt"]),
                    "top1": float(metrics["beam_top1_dist_2_0m"]),
                    "top4": float(metrics["beam_top4_dist_2_0m"]),
                }
            )
    records.sort(key=lambda row: (row["label"], row["node_count"]))
    _write_table(
        "table_03_node_count_overall",
        ["Fusion method", "Nearby node count", "AP@2m (%)", "Recall@2m (%)", "Beam Top-1@2m (%)", "Beam Top-4@2m (%)"],
        [[row["label"], str(row["node_count"]), _pct(row["ap"]), _pct(row["recall"]), _pct(row["top1"]), _pct(row["top4"])] for row in records],
    )
    styles = (("#1f77b4", "o"), ("#ff7f0e", "s"), ("#2ca02c", "^"))
    labels = list(dict.fromkeys(row["label"] for row in records))
    _plot_node_metric(records, labels, styles, summary["sn_counts"], "ap", "AP@2m (%)", "fig_01_node_count_ap")
    _plot_node_metric(records, labels, styles, summary["sn_counts"], "recall", "Recall@2m (%)", "fig_02_node_count_recall")
    _plot_node_beam_metrics(records, labels, styles, summary["sn_counts"])


def _plot_node_metric(
    records: list[dict[str, Any]],
    labels: list[str],
    styles: tuple[tuple[str, str], ...],
    node_counts: list[int],
    metric_key: str,
    ylabel: str,
    stem: str,
) -> None:
    fig, ax = plt.subplots(figsize=(6.5, 3.9), constrained_layout=True)
    for index, label in enumerate(labels):
        color, marker = styles[index % len(styles)]
        series = [row for row in records if row["label"] == label]
        ax.plot(
            [row["node_count"] for row in series],
            [100 * row[metric_key] for row in series],
            marker=marker,
            color=color,
            linewidth=1.9,
            label=label,
        )
    ax.set_xlabel("Nearby node count")
    ax.set_ylabel(ylabel)
    ax.set_xticks(node_counts)
    ax.set_ylim(0, 100)
    ax.grid(axis="y", alpha=0.25)
    ax.legend(fontsize=8, frameon=False, ncol=1)
    _save_figure(fig, stem)


def _plot_node_beam_metrics(
    records: list[dict[str, Any]],
    labels: list[str],
    styles: tuple[tuple[str, str], ...],
    node_counts: list[int],
) -> None:
    fig, ax = plt.subplots(figsize=(6.8, 4.0), constrained_layout=True)
    for index, label in enumerate(labels):
        color, marker = styles[index % len(styles)]
        series = [row for row in records if row["label"] == label]
        x = [row["node_count"] for row in series]
        ax.plot(x, [100 * row["top1"] for row in series], marker=marker, color=color, linewidth=1.9, linestyle="-")
        ax.plot(x, [100 * row["top4"] for row in series], marker=marker, color=color, linewidth=1.9, linestyle="--")
    method_handles = [
        Line2D([0], [0], color=color, marker=marker, linewidth=1.9, label=label)
        for label, (color, marker) in zip(labels, styles, strict=True)
    ]
    metric_handles = [
        Line2D([0], [0], color="#333333", linewidth=1.9, linestyle="-", label="Beam Top-1@2m"),
        Line2D([0], [0], color="#333333", linewidth=1.9, linestyle="--", label="Beam Top-4@2m"),
    ]
    methods_legend = ax.legend(handles=method_handles, title="Fusion method", loc="lower right", frameon=False, fontsize=7.7, title_fontsize=8)
    ax.add_artist(methods_legend)
    ax.legend(handles=metric_handles, title="Metric", loc="lower left", frameon=False, fontsize=7.7, title_fontsize=8)
    ax.set_xlabel("Nearby node count")
    ax.set_ylabel("Beam metric (%)")
    ax.set_xticks(node_counts)
    ax.set_ylim(0, 100)
    ax.grid(axis="y", alpha=0.25)
    _save_figure(fig, "fig_03_node_count_beam")


def _export_core_table(
    summary: dict[str, Any],
    unique_ue_counts: dict[tuple[str, str], int],
) -> None:
    rows = summary["rows"]
    by_key: dict[tuple[str, str], dict[str, Any]] = {}
    for row in rows:
        key = (row["weather_id"], row["condition"])
        selected = dict(row)
        selected["mean_effective_user_rate_bps"] = float(row["mean_system_rate_bps"]) / unique_ue_counts[key]
        selected["unique_ue_count"] = unique_ue_counts[key]
        by_key[key] = selected
    headers = ["Weather", "Scheme", "Mean effective user rate (Mbps)", "CSI-RS overhead (%)"]
    detail_rows: list[list[str]] = []
    for weather in WEATHERS:
        for condition in CONDITION_LABELS:
            detail_rows.append(_core_table_row(WEATHER_LABELS[weather], CONDITION_LABELS[condition], by_key[(weather, condition)]))

    aggregate_by_condition = {row["condition"]: dict(row) for row in summary["aggregates"]}
    for condition, aggregate in aggregate_by_condition.items():
        selected_rows = [by_key[(weather, condition)] for weather in WEATHERS]
        aggregate["mean_effective_user_rate_bps"] = float(
            np.mean([row["mean_effective_user_rate_bps"] for row in selected_rows])
        )
        aggregate["unique_ue_count"] = int(round(np.mean([row["unique_ue_count"] for row in selected_rows])))
    detail_rows.extend(
        _core_table_row("Macro average", CONDITION_LABELS[condition], aggregate_by_condition[condition])
        for condition in CONDITION_LABELS
    )
    _write_table("table_04_core_by_weather", headers, detail_rows)


def _core_table_row(weather: str, scheme: str, row: dict[str, Any]) -> list[str]:
    return [
        weather,
        scheme,
        _num(float(row["mean_effective_user_rate_bps"]) / 1e6),
        _pct(row["mean_csi_overhead"]),
    ]


def _export_sensing_configuration_table(
    core_summary: dict[str, Any],
    core_user_counts: dict[tuple[str, str], int],
    modality_summary: dict[str, Any],
    modality_user_counts: dict[tuple[str, str], int],
) -> None:
    headers = ["Sensing configuration", "Mean effective user rate (Mbps)", "CSI-RS overhead (%)", "Sensing use (%)"]
    modality_by_key = {
        (row["weather_id"], row["detector"]): row
        for row in modality_summary["rows"]
        if row["detector"] in SENSING_CONFIGURATION_LABELS
    }
    table_rows: list[list[str]] = []
    for detector, label in SENSING_CONFIGURATION_LABELS.items():
        rows = [modality_by_key[(weather, detector)] for weather in WEATHERS]
        rates = [
            float(row["mean_system_rate_bps"]) / modality_user_counts[(weather, detector)]
            for weather, row in zip(WEATHERS, rows)
        ]
        table_rows.append(
            [
                label,
                _num(float(np.mean(rates)) / 1e6),
                _pct(float(np.mean([float(row["mean_csi_overhead"]) for row in rows]))),
                _pct(float(np.mean([float(row["sensing_hint_usage_fraction"]) for row in rows]))),
            ]
        )

    core_rows = {
        row["weather_id"]: row
        for row in core_summary["rows"]
        if row["condition"] == "sensing_imm"
    }
    core_rates = [
        float(core_rows[weather]["mean_system_rate_bps"]) / core_user_counts[(weather, "sensing_imm")]
        for weather in WEATHERS
    ]
    table_rows.append(
        [
            "DMSA-BM",
            _num(float(np.mean(core_rates)) / 1e6),
            _pct(float(np.mean([float(core_rows[weather]["mean_csi_overhead"]) for weather in WEATHERS]))),
            _pct(float(np.mean([float(core_rows[weather]["sensing_hint_usage_fraction"]) for weather in WEATHERS]))),
        ]
    )
    _write_table("table_05_sensing_configuration_communication", headers, table_rows)


def _export_tracker_table(
    summary: dict[str, Any],
    unique_ue_counts: dict[tuple[str, str], int],
) -> None:
    rows = summary["rows"]
    by_tracker: dict[str, list[dict[str, Any]]] = {tracker: [] for tracker in TRACKER_LABELS}
    for row in rows:
        key = (row["weather_id"], row["tracker"])
        selected = dict(row)
        selected["mean_effective_user_rate_bps"] = float(row["mean_system_rate_bps"]) / unique_ue_counts[key]
        by_tracker[row["tracker"]].append(selected)
    if any(len(rows) != len(WEATHERS) for rows in by_tracker.values()):
        raise ValueError("Tracker table requires one completed Top-1 CE result per tracker and weather")
    headers = ["Tracker", "Mean effective user rate (Mbps)", "Sensing use (%)"]
    table_rows: list[list[str]] = []
    for tracker, label in TRACKER_LABELS.items():
        values = by_tracker[tracker]
        table_rows.append(
            [
                label,
                _num(float(np.mean([row["mean_effective_user_rate_bps"] for row in values])) / 1e6),
                _pct(float(np.mean([row["sensing_hint_usage_fraction"] for row in values]))),
            ]
        )
    _write_table("table_06_tracker_macro_average", headers, table_rows)


def _copy_tracker_visual() -> None:
    source = RAW_ROOT / "tracking" / "visualizations" / "test_clear_day_bs_ne_three_trackers_noise_1_0m.png"
    destination = FIGURE_ROOT / "fig_06_tracker_gt_noise_test.png"
    shutil.copy2(source, destination)


def _write_manifest() -> None:
    manifest = {
        "format": "paper_results_asset_export_v2",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "raw_inputs": [
            "raw/learning/v3_rt_anchor_paper_test/summary.json",
            "raw/learning/v3_rt_anchor_node_fusion_sn_count_test/summary.json",
            "raw/beam_management/v9/core_comparison.json",
            "raw/beam_management/v9/modality_ablation_comparison.json",
            "raw/beam_management/v9/tracker_top1ce/tracker_ablation_comparison.json",
            "raw/tracking/visualizations/test_clear_day_bs_ne_three_trackers_noise_1_0m.png",
        ],
        "paper_core_primary_detector": "v3_rt_anchor_beam_top1_ce_cross_agent",
        "paper_user_rate_metric": "mean_system_rate_bps / unique_ue_count",
        "paper_user_rate_definition": "All-UE time-average effective throughput; CSI-RS training, non-data overhead, and unscheduled intervals contribute zero throughput.",
        "excluded_from_paper": ["beam-supervision ablation", "historical end-to-end tracker ablation"],
        "generated_tables": sorted(path.name for path in TABLE_ROOT.glob("*")),
        "generated_figures": sorted(path.name for path in FIGURE_ROOT.glob("*")),
    }
    path = METADATA_ROOT / "manifest.json"
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _write_table(stem: str, headers: list[str], rows: list[list[str]]) -> None:
    with (TABLE_ROOT / f"{stem}.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(headers)
        writer.writerows(rows)
    markdown_lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    markdown_lines.extend("| " + " | ".join(_markdown_cell(cell) for cell in row) + " |" for row in rows)
    (TABLE_ROOT / f"{stem}.md").write_text("\n".join(markdown_lines) + "\n", encoding="utf-8")
    alignment = "l" + "r" * (len(headers) - 1)
    latex = [f"\\begin{{tabular}}{{{alignment}}}", "\\toprule", " & ".join(_latex_cell(cell) for cell in headers) + " \\\\", "\\midrule"]
    latex.extend(" & ".join(_latex_cell(cell) for cell in row) + " \\\\" for row in rows)
    latex.extend(["\\bottomrule", "\\end{tabular}"])
    (TABLE_ROOT / f"{stem}.tex").write_text("\n".join(latex) + "\n", encoding="utf-8")


def _save_figure(fig: plt.Figure, stem: str) -> None:
    fig.savefig(FIGURE_ROOT / f"{stem}.png", dpi=320, bbox_inches="tight")
    fig.savefig(FIGURE_ROOT / f"{stem}.pdf", bbox_inches="tight")
    plt.close(fig)


def _pct(value: float) -> str:
    return f"{100 * float(value):.2f}"


def _pct_or_dash(value: Any) -> str:
    return "—" if value is None else _pct(float(value))


def _num(value: float) -> str:
    return f"{value:.3f}"


def _markdown_cell(value: str) -> str:
    return str(value).replace("|", "\\|")


def _latex_cell(value: str) -> str:
    return str(value).replace("_", "\\_").replace("%", "\\%").replace("&", "\\&")


if __name__ == "__main__":
    main()
