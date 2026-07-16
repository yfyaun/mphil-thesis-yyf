# 最终论文结果包

本目录是论文使用的唯一正式结果包。`raw/` 保存冻结的机器可读输入，`tables/` 与 `figures/` 均可由 `scripts/` 从这些 raw 数据重新生成；不在此目录运行训练、RT 重建或 beam-management 仿真。

## 当前正文结果组织

1. **Learning detection 与 beam prediction：**
   - 表 1：不同模态/融合的 Overall 指标（AP@2m、Recall@2m、Beam Top-1/Top-4@2m、Top-4 power ratio）。
   - 表 2：相同指标的 Clear、Rain-Fog、Night 分天气结果。
   - 表 3、图 1–3：nearby node 数变化下的 AP@2m、Recall@2m 与 Beam Top-1/Top-4@2m。
2. **系统级 beam management：**
   - 表 4：三种天气下 SSB-guided CSI-RS refinement 的 \(K_{\mathrm{ref}}=4\) 与 \(K_{\mathrm{ref}}=12\) 设置，以及 DMSA-BM 的用户平均速率、CSI-RS 开销与 sensing use/fallback 结果。
   - 表 5、图 4–5：三天气等权宏平均、用户平均速率、CSI-RS overhead 与 hint/fallback 运行折中。
3. **Tracker：** 图 6 使用 test / clear-day / BS-NE 的 GT+1.0 m 位置噪声输入，直观对比 KF-CV、KF-CT、IMM 轨迹。**表 IV**（`table_06_tracker_macro_average.*`）报告固定 Top-1 CE detector、CSI 5 ms、四小区与 weather-specific gate 下三种 tracker 的跨天气等权宏平均用户有效速率和 sensing-use ratio。

Beam supervision 的 Power-KL + ranking、Power-KL only、Top-1 CE 对比是内部开发归档，不进入论文图表。论文主系统级 sensing 行固定使用 `v3_rt_anchor_beam_top1_ce_cross_agent` + IMM；其来源由 `metadata/manifest.json` 记录。

本文中“用户平均有效速率”定义为完整仿真时段内、全部 UE 的 time-average throughput：

\[
\bar R_{\mathrm{UE,eff}}=
\frac{1}{|\mathcal U|T}\sum_{u\in\mathcal U}\sum_t R_u(t)\Delta t
=\frac{\bar R_{\mathrm{sys}}}{|\mathcal U|}.
\]

其中 CSI-RS training、SSB/控制/CSI-RS 等非数据信号开销以及 UE 未被调度的时段均按零吞吐量计入。它不是 `mean_ue_rate_when_scheduled_bps` 的条件平均；后者不再用于论文表图。系统总速率与 outage 仍保留在 raw snapshot 中供补充分析。

## 生成命令

在工作区根目录执行：

```powershell
uv run --project mmbeam-tracking python paper_results/scripts/sync_top1ce_tracker_raw.py
uv run --project mmbeam-tracking python paper_results/scripts/prepare_tracker_gt_noise_test_visual.py
uv run --project mmbeam-tracking python paper_results/scripts/build_paper_assets.py --clean
```

第一条命令将已完成的 Top-1 CE tracker 端到端运行冻结至 `raw/beam_management/v9/tracker_top1ce/`。第二条命令仅在 `raw/tracking/visualizations/` 缺少 test-split GT-noise 图时生成该定性可视化；第三条命令会清空并重建本目录下的 `tables/`、`figures/`，同时清理旧的 `tracking/tables/` 与 `tracking/figures/`，但不会删除任何 `raw/` 数据或原始 `artifacts/`。

## 目录约定

```text
paper_results/
├─ raw/        # 冻结输入：learning、beam-management、tracking
├─ scripts/    # 可复现的资产导出脚本
├─ tables/     # 每张表的 CSV、Markdown、LaTeX
├─ figures/    # 论文图：PNG（320 dpi）及 PDF；轨迹图仅 PNG
└─ metadata/   # 本次导出的输入与协议追溯
```

核心通信数据的雨雾门限采用已授权的 test-tuned `min_association_margin=0.10` 操作点，写作中须表述为固定操作点结果，不能当作独立 held-out 泛化性能。
