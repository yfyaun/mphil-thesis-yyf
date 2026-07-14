"""Build the dedicated tracker report from frozen V3-detection test results.

The report deliberately uses the three ``*_beam_management_v2`` tracker
configurations that feed the V9 beam-management ablation.  It reads only the
completed tracking metric contracts; it neither re-runs a tracker nor loads
training tensors or heavy dataset assets.
"""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
from typing import Any, Iterable

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SCRIPT_PATH = Path(__file__).resolve()
WORKSPACE_ROOT = SCRIPT_PATH.parents[3]
TRACKING_ROOT = WORKSPACE_ROOT / "mmbeam-tracking"
SOURCE_ROOT = (
    TRACKING_ROOT
    / "artifacts"
    / "v8_paper"
    / "tracking_metrics"
    / "primary_detector_test_bm_v2_matched"
)
TRACKER_ORDER = ("imm_bm_v2", "ct_bm_v2", "cv_bm_v2")
TRACKER_LABELS = {
    "imm_bm_v2": "IMM (CV+CT)",
    "ct_bm_v2": "KF-CT",
    "cv_bm_v2": "KF-CV",
}
TRACKER_CONFIGS = {
    "imm_bm_v2": "configs/tracker/imm_cv_ct_beam_management_v2.yaml",
    "ct_bm_v2": "configs/tracker/kf_ct_beam_management_v2.yaml",
    "cv_bm_v2": "configs/tracker/kf_cv_beam_management_v2.yaml",
}
WEATHER_ORDER = ("clear_day", "rain_fog_day", "night")
WEATHER_LABELS = {
    "clear_day": "Clear",
    "rain_fog_day": "Rain/Fog",
    "night": "Night",
}
COLORS = {
    "IMM (CV+CT)": "#F58518",
    "KF-CT": "#54A24B",
    "KF-CV": "#4C78A8",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build paper_results/tracking from frozen tracking metrics.")
    parser.add_argument("--output-dir", default=str(WORKSPACE_ROOT / "paper_results" / "tracking"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_root = Path(args.output_dir).resolve()
    _validate_sources()
    for name in ("raw", "tables", "figures", "scripts"):
        (output_root / name).mkdir(parents=True, exist_ok=True)

    comparison = _read_json(SOURCE_ROOT / "comparison.json")
    sequences = {name: _read_jsonl(SOURCE_ROOT / name / "sequence_metrics.jsonl") for name in TRACKER_ORDER}
    aggregate_rows = _aggregate_rows(comparison, sequences)
    weather_rows = _weather_rows(sequences)
    delta_rows = _delta_rows(aggregate_rows, baseline="KF-CV")

    _copy_raw_contracts(output_root)
    _write_table_bundle(output_root / "tables", "t1_tracker_aggregate_test", aggregate_rows)
    _write_table_bundle(output_root / "tables", "t2_tracker_by_weather_test", weather_rows)
    _write_table_bundle(output_root / "tables", "t3_tracker_delta_vs_kf_cv", delta_rows)
    _plot_aggregate_quality(output_root / "figures", aggregate_rows)
    _plot_weather_quality(output_root / "figures", weather_rows)

    manifest = {
        "format": "mmbeam_tracker_paper_results_v1",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "source_root": str(SOURCE_ROOT),
        "detector": comparison["input"]["detections"],
        "protocol": {
            "split": comparison["input"]["splits"],
            "weather_ids": comparison["input"]["weather_ids"],
            "bs_ids": comparison["input"]["bs_ids"],
            "sequence_count": comparison["input"]["sequence_count"],
            "match_distance_m": comparison["input"]["match_distance_m"],
            "tracker_configs": TRACKER_CONFIGS,
        },
        "source_sha256": _source_hashes(),
        "tables": [
            "t1_tracker_aggregate_test",
            "t2_tracker_by_weather_test",
            "t3_tracker_delta_vs_kf_cv",
        ],
        "figures": ["fig_t1_tracker_aggregate_quality", "fig_t2_tracker_weather_quality"],
    }
    _write_json(output_root / "raw" / "report_manifest.json", manifest)
    _write_json(
        output_root / "raw" / "report_summary.json",
        {"aggregate_rows": aggregate_rows, "weather_rows": weather_rows, "delta_rows": delta_rows},
    )
    _write_readme(output_root, aggregate_rows)
    _copy_builder(output_root)
    print(f"[done] {output_root}")


def _validate_sources() -> None:
    required = [SOURCE_ROOT / "comparison.json", SOURCE_ROOT / "comparison.csv"]
    for tracker in TRACKER_ORDER:
        required.extend(
            [
                SOURCE_ROOT / tracker / "aggregate_metrics.json",
                SOURCE_ROOT / tracker / "sequence_metrics.jsonl",
                TRACKING_ROOT / TRACKER_CONFIGS[tracker],
            ]
        )
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise FileNotFoundError("Missing frozen tracker result contracts:\n" + "\n".join(missing))


def _aggregate_rows(
    comparison: dict[str, Any], sequences: dict[str, list[dict[str, Any]]]
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for tracker in TRACKER_ORDER:
        metric = comparison["algorithms"][tracker]["aggregate"]
        rows.append(
            {
                "tracker": TRACKER_LABELS[tracker],
                "tracker_config": TRACKER_CONFIGS[tracker],
                "sequences": int(metric["sequence_count"]),
                "frames": sum(int(item["frame_count"]) for item in sequences[tracker]),
                "gt_observations": int(metric["gt_object_count"]),
                "matched_observations": int(metric["match_count"]),
                "mota_percent": _percent(metric["mota"]),
                "id_maintenance_percent": _percent(metric["id_maintenance_rate"]),
                "precision_percent": _percent(metric["precision"]),
                "recall_percent": _percent(metric["recall"]),
                "mean_center_error_m": _round(metric["mean_center_error_m"]),
                "id_switches": int(metric["id_switch_count"]),
                "fragmentations": int(metric["fragmentation_count"]),
                "mostly_tracked_gt": int(metric["mostly_tracked_count"]),
                "mostly_lost_gt": int(metric["mostly_lost_count"]),
                "produced_tracks": int(metric["track_count"]),
            }
        )
    return rows


def _weather_rows(sequences: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for weather in WEATHER_ORDER:
        for tracker in TRACKER_ORDER:
            selected = [item for item in sequences[tracker] if item["weather_id"] == weather]
            if len(selected) != 4:
                raise ValueError(f"Expected four BS sequences for {tracker} / {weather}, got {len(selected)}")
            metric = _aggregate_metrics(selected)
            rows.append(
                {
                    "weather": WEATHER_LABELS[weather],
                    "tracker": TRACKER_LABELS[tracker],
                    "sequences": int(metric["sequence_count"]),
                    "gt_observations": int(metric["gt_object_count"]),
                    "mota_percent": _percent(metric["mota"]),
                    "id_maintenance_percent": _percent(metric["id_maintenance_rate"]),
                    "precision_percent": _percent(metric["precision"]),
                    "recall_percent": _percent(metric["recall"]),
                    "mean_center_error_m": _round(metric["mean_center_error_m"]),
                    "id_switches": int(metric["id_switch_count"]),
                    "fragmentations": int(metric["fragmentation_count"]),
                    "id_switches_per_1k_gt": _round(1000.0 * metric["id_switch_count"] / metric["gt_object_count"]),
                }
            )
    return rows


def _aggregate_metrics(metrics: Iterable[dict[str, Any]]) -> dict[str, float]:
    values = list(metrics)
    sum_keys = (
        "gt_object_count",
        "gt_track_count",
        "tracker_output_count",
        "match_count",
        "track_count",
        "false_positive_count",
        "false_negative_count",
        "id_switch_count",
        "fragmentation_count",
        "mostly_tracked_count",
        "mostly_lost_count",
        "center_error_sum",
    )
    totals = {key: sum(float(item[key]) for item in values) for key in sum_keys}
    match = max(totals["match_count"], 1.0)
    gt = max(totals["gt_object_count"], 1.0)
    tracker_outputs = max(totals["tracker_output_count"], 1.0)
    totals.update(
        {
            "sequence_count": float(len(values)),
            "id_maintenance_rate": 1.0 - totals["id_switch_count"] / match,
            "precision": totals["match_count"] / tracker_outputs,
            "recall": totals["match_count"] / gt,
            "mota": 1.0 - (totals["false_negative_count"] + totals["false_positive_count"] + totals["id_switch_count"]) / gt,
            "mean_center_error_m": totals["center_error_sum"] / match,
        }
    )
    return totals


def _delta_rows(rows: list[dict[str, Any]], baseline: str) -> list[dict[str, Any]]:
    baseline_row = next(row for row in rows if row["tracker"] == baseline)
    result: list[dict[str, Any]] = []
    for row in rows:
        result.append(
            {
                "tracker": row["tracker"],
                "baseline": baseline,
                "mota_delta_pp": _round(row["mota_percent"] - baseline_row["mota_percent"]),
                "id_maintenance_delta_pp": _round(row["id_maintenance_percent"] - baseline_row["id_maintenance_percent"]),
                "precision_delta_pp": _round(row["precision_percent"] - baseline_row["precision_percent"]),
                "recall_delta_pp": _round(row["recall_percent"] - baseline_row["recall_percent"]),
                "center_error_delta_m": _round(row["mean_center_error_m"] - baseline_row["mean_center_error_m"]),
                "id_switch_delta": row["id_switches"] - baseline_row["id_switches"],
                "fragmentation_delta": row["fragmentations"] - baseline_row["fragmentations"],
            }
        )
    return result


def _copy_raw_contracts(output_root: Path) -> None:
    raw = output_root / "raw"
    _copy_file(SOURCE_ROOT / "comparison.json", raw / "comparison.json")
    _copy_file(SOURCE_ROOT / "comparison.csv", raw / "comparison.csv")
    for tracker in TRACKER_ORDER:
        _copy_file(SOURCE_ROOT / tracker / "aggregate_metrics.json", raw / tracker / "aggregate_metrics.json")
        _copy_file(SOURCE_ROOT / tracker / "sequence_metrics.jsonl", raw / tracker / "sequence_metrics.jsonl")
        _copy_file(TRACKING_ROOT / TRACKER_CONFIGS[tracker], raw / "tracker_configs" / Path(TRACKER_CONFIGS[tracker]).name)


def _plot_aggregate_quality(directory: Path, rows: list[dict[str, Any]]) -> None:
    metrics = (
        ("MOTA (%)", "mota_percent"),
        ("ID maintenance (%)", "id_maintenance_percent"),
        ("Precision / Recall (%)", None),
    )
    figure, axes = plt.subplots(1, 3, figsize=(11.2, 3.5), constrained_layout=True)
    labels = [row["tracker"] for row in rows]
    colors = [COLORS[label] for label in labels]
    for axis, (title, field) in zip(axes, metrics):
        if field is not None:
            axis.bar(labels, [row[field] for row in rows], color=colors)
            axis.set_ylim(0.0, 100.0)
        else:
            x = list(range(len(rows)))
            width = 0.36
            axis.bar([value - width / 2 for value in x], [row["precision_percent"] for row in rows], width, label="Precision", color="#4C78A8")
            axis.bar([value + width / 2 for value in x], [row["recall_percent"] for row in rows], width, label="Recall", color="#54A24B")
            axis.set(xticks=x, xticklabels=labels, ylim=(0.0, 100.0))
            axis.legend(frameon=False, fontsize=8)
        axis.set_title(title)
        axis.tick_params(axis="x", rotation=13)
        axis.grid(axis="y", alpha=0.25)
    _save_figure(figure, directory / "fig_t1_tracker_aggregate_quality")


def _plot_weather_quality(directory: Path, rows: list[dict[str, Any]]) -> None:
    figure, axes = plt.subplots(1, 2, figsize=(10.5, 3.6), constrained_layout=True)
    x = list(range(len(WEATHER_ORDER)))
    width = 0.22
    for index, tracker in enumerate(TRACKER_ORDER):
        label = TRACKER_LABELS[tracker]
        selected = [row for row in rows if row["tracker"] == label]
        values = {row["weather"]: row for row in selected}
        offset = (index - 1) * width
        axes[0].bar(
            [value + offset for value in x],
            [values[WEATHER_LABELS[weather]]["mota_percent"] for weather in WEATHER_ORDER],
            width,
            label=label,
            color=COLORS[label],
        )
        axes[1].bar(
            [value + offset for value in x],
            [values[WEATHER_LABELS[weather]]["id_switches_per_1k_gt"] for weather in WEATHER_ORDER],
            width,
            label=label,
            color=COLORS[label],
        )
    weather_labels = [WEATHER_LABELS[weather] for weather in WEATHER_ORDER]
    axes[0].set(xticks=x, xticklabels=weather_labels, ylabel="MOTA (%)", ylim=(0.0, 100.0), title="Tracking accuracy by weather")
    axes[1].set(xticks=x, xticklabels=weather_labels, ylabel="ID switches / 1k GT observations", title="ID continuity burden by weather")
    for axis in axes:
        axis.grid(axis="y", alpha=0.25)
    axes[0].legend(frameon=False, fontsize=8)
    _save_figure(figure, directory / "fig_t2_tracker_weather_quality")


def _write_table_bundle(directory: Path, name: str, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"No rows for {name}")
    directory.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0])
    with (directory / f"{name}.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    (directory / f"{name}.md").write_text(_markdown_table(fields, rows), encoding="utf-8")
    (directory / f"{name}.tex").write_text(_latex_table(fields, rows), encoding="utf-8")


def _markdown_table(fields: list[str], rows: list[dict[str, Any]]) -> str:
    header = "| " + " | ".join(fields) + " |\n"
    divider = "| " + " | ".join("---" for _ in fields) + " |\n"
    body = "".join("| " + " | ".join(_format_value(row[field]) for field in fields) + " |\n" for row in rows)
    return header + divider + body


def _latex_table(fields: list[str], rows: list[dict[str, Any]]) -> str:
    def escape(value: str) -> str:
        return value.replace("_", "\\_").replace("%", "\\%")

    lines = ["\\begin{tabular}{" + "l" * len(fields) + "}", "\\toprule"]
    lines.append(" & ".join(escape(field) for field in fields) + " \\\\")
    lines.append("\\midrule")
    for row in rows:
        lines.append(" & ".join(escape(_format_value(row[field])) for field in fields) + " \\\\")
    lines.extend(["\\bottomrule", "\\end{tabular}", ""])
    return "\n".join(lines)


def _write_readme(output_root: Path, rows: list[dict[str, Any]]) -> None:
    imm = next(row for row in rows if row["tracker"] == "IMM (CV+CT)")
    ct = next(row for row in rows if row["tracker"] == "KF-CT")
    cv = next(row for row in rows if row["tracker"] == "KF-CV")
    content = f"""# Tracker 正式数据报告

本目录保存与 V9 beam-management tracker 消融**参数完全一致**的纯追踪评估结果。它使用 V3 主模型 `v3_rt_anchor_beam_power_kl_ranking_cross_agent` 的未绑定 detection JSONL，在 held-out `test` split 上比较 IMM、KF-CT 与 KF-CV；不重新训练 detection，也不重新运行 beam-management PHY 仿真。

## 评估协议

- 数据范围：三种天气（clear day、rain/fog、night）× 四个 BS，共 12 条 sequence；每条 100 个已保存帧（10 FPS）。
- 坐标系：target-BS-centered Sionna BEV；检测 score 阈值为 0.05；GT/track 使用 2 m 欧氏距离匈牙利匹配。
- tracker 参数：`raw/tracker_configs/` 中保存的 `*_beam_management_v2.yaml`，也是 V9 的 `IMM / KF-CT / KF-CV` tracker 消融所用配置。
- 指标聚合：所有计数先跨 sequence 求和；precision、recall、MOTA、ID-maintenance 与平均位置误差随后以对应的全局分母计算。`ID switches / 1k GT observations` 仅用于跨天气归一化展示。

## 核心结果

IMM 的纯追踪指标整体最优：MOTA {imm['mota_percent']:.2f}%、ID-maintenance {imm['id_maintenance_percent']:.2f}%、precision/recall {imm['precision_percent']:.2f}%/{imm['recall_percent']:.2f}%，共 {imm['id_switches']} 次 ID switch。相对 KF-CT（MOTA {ct['mota_percent']:.2f}%、{ct['id_switches']} switches）与 KF-CV（MOTA {cv['mota_percent']:.2f}%、{cv['id_switches']} switches），优势一致但幅度适中。

这份报告应与 `../tables/table_06_end_to_end_tracker.*` 区分解读：前者衡量 detection-to-track 的位置匹配与 ID 连续性；后者是含 confidence fallback 的端到端系统速率。由于当前 beam hint 使用已关联 detection 的本帧 beam prediction，且低可靠度事件会回退 conventional，纯追踪优势不会线性地转换成同等幅度的系统速率差距。

## 目录

- `raw/`：冻结的 comparison、每 tracker 的 aggregate/sequence 原始指标、参数 YAML、报告 manifest 与可机器读取汇总。
- `tables/`：CSV、Markdown、LaTeX 三种格式的总体结果、按天气结果、相对 KF-CV 差值。
- `figures/`：320 dpi PNG 与矢量 PDF；`fig_t1` 为总体准确度，`fig_t2` 为三天气的 MOTA 与归一化 ID-switch 负担。
- `scripts/build_tracking_paper_results.py`：仅从上述冻结源结果重建本目录；不会执行新的追踪实验。

## 重建

从工作区根目录运行：

```powershell
uv run --project mmbeam-tracking python paper_results/tracking/scripts/build_tracking_paper_results.py
```
"""
    (output_root / "README.md").write_text(content, encoding="utf-8")


def _copy_builder(output_root: Path) -> None:
    destination = output_root / "scripts" / SCRIPT_PATH.name
    if destination.resolve() != SCRIPT_PATH:
        _copy_file(SCRIPT_PATH, destination)


def _source_hashes() -> dict[str, str]:
    files = [SOURCE_ROOT / "comparison.json"]
    for tracker in TRACKER_ORDER:
        files.extend([SOURCE_ROOT / tracker / "aggregate_metrics.json", SOURCE_ROOT / tracker / "sequence_metrics.jsonl"])
    return {str(path.relative_to(SOURCE_ROOT)): _sha256(path) for path in files}


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _copy_file(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def _save_figure(figure: plt.Figure, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(path.with_suffix(".png"), dpi=320, bbox_inches="tight")
    figure.savefig(path.with_suffix(".pdf"), bbox_inches="tight")
    plt.close(figure)


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _round(value: float, digits: int = 4) -> float:
    return round(float(value), digits)


def _percent(value: float) -> float:
    return _round(100.0 * float(value))


def _format_value(value: Any) -> str:
    if isinstance(value, float):
        return f"{value:.4f}"
    return str(value)


if __name__ == "__main__":
    main()
