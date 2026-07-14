# Tracker 正式数据报告

本目录保存与 V9 beam-management tracker 消融**参数完全一致**的纯追踪评估结果。它使用 V3 主模型 `v3_rt_anchor_beam_power_kl_ranking_cross_agent` 的未绑定 detection JSONL，在 held-out `test` split 上比较 IMM、KF-CT 与 KF-CV；不重新训练 detection，也不重新运行 beam-management PHY 仿真。

## 评估协议

- 数据范围：三种天气（clear day、rain/fog、night）× 四个 BS，共 12 条 sequence；每条 100 个已保存帧（10 FPS）。
- 坐标系：target-BS-centered Sionna BEV；检测 score 阈值为 0.05；GT/track 使用 2 m 欧氏距离匈牙利匹配。
- tracker 参数：`raw/tracker_configs/` 中保存的 `*_beam_management_v2.yaml`，也是 V9 的 `IMM / KF-CT / KF-CV` tracker 消融所用配置。
- 指标聚合：所有计数先跨 sequence 求和；precision、recall、MOTA、ID-maintenance 与平均位置误差随后以对应的全局分母计算。`ID switches / 1k GT observations` 仅用于跨天气归一化展示。

## 核心结果

IMM 的纯追踪指标整体最优：MOTA 50.94%、ID-maintenance 96.46%、precision/recall 74.86%/81.02%，共 324 次 ID switch。相对 KF-CT（MOTA 48.70%、325 switches）与 KF-CV（MOTA 48.16%、354 switches），优势一致但幅度适中。

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
