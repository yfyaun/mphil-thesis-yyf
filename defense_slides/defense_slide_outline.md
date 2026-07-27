# MPhil Thesis Defense Slide Outline

## 1. Presentation Brief / 答辩整体定位

- **Working title**: *Multimodal Sensing-Assisted User Association and Tracking in Vehicular Networks*
- **Target duration**: approximately 35 minutes
- **Target length**: 28 slides, including four section-divider slides
- **Presentation language**: English
- **Outline annotations**: English slide copy with Chinese explanation
- **Intended audience**: an academic defense panel with expertise in wireless communications, signal processing, sensing, and machine learning, but not necessarily familiar with every implementation detail of this thesis
- **Communication job**: By the end, the panel should understand why sensing-assisted beam prediction is insufficient without target-to-user association, how DMSA-BM connects distributed multimodal perception to measured CSI-RS decisions, and what communication benefit is supported by the current evidence.

### Central takeaway / 核心结论

> Distributed multimodal sensing can reduce CSI-RS measurement overhead in dynamic V2I networks only when target-level beam predictions are associated with the intended communication user and remain supported by a current physical-target observation.

中文解释：整场答辩不应被组织成“我做了一个检测网络、一个 tracker、一个仿真器”的模块罗列，而应持续回答同一个问题：感知产生的 target-level beam prediction 如何安全、有效地转化为正确用户的通信收益。

### Narrative arc / 叙事主线

1. **Why the problem matters** — vehicular networks require reliable, low-latency V2I connectivity under high mobility and changing propagation conditions.
2. **Why V2I beam management is difficult** — narrow beams provide high-frequency gain but create a recurrent measurement-overhead problem.
3. **What sensing-assisted prediction can and cannot provide** — single-candidate formulations assume a known target, while multi-candidate formulations require user-specific side information to identify the intended transmitter.
4. **Why target-to-user association is required** — sensing observes physical targets, while communication serves VUE identities; uncertain target evidence cannot safely narrow a VUE's scan.
5. **How the proposed framework closes the loop** — distributed multimodal BEV perception for joint vehicle detection and beam prediction, measurement-assisted association with IMM tracking, and association-gated candidate measurement.
6. **What the evidence supports** — improved target observability and a rate–overhead benefit under the stated operating point, with explicit fallback and limitations.

### Recommended visual language / 建议视觉风格

- Follow the supplied institutional template with a white background, dark-olive top and bottom rules, an institutional-blue title, and the university logo at the upper right.
- Every slide, including section dividers, uses a fixed top title area. Titles should be formal noun phrases of approximately two to six words and should normally fit on one line.
- Keep the title descriptive rather than argumentative. The principal finding or takeaway should appear in the body of the slide, not in the title bar.
- Use black body text and blue outlined square bullets. Preserve generous white space and avoid dense card-based layouts that conflict with the template.
- Prefer one dominant message or evidence object per slide.
- Use thesis figures and regenerated result charts wherever possible. Avoid decorative stock imagery.
- Keep equations selective. Each method slide should show only the equation needed to explain the decision or information interface.
- Section-divider slides retain the same top title bar and place the section number plus one orienting sentence in the body area.
- Suggested typography for a 16:9 deck is 32–36 pt for the fixed title, 24–28 pt for body subheadings, and 20–24 pt for body copy.

中文解释：整体版式直接服从现有学校模板。顶部标题只承担“本页讲什么”的导航功能，不承担完整论证，因此不使用长句、问句或宣传式结论。原来标题中的判断性内容应移至正文首句、图表旁结论或页面底部 takeaway。除封面外，标题尽量控制在 2–6 个英文词，并保持单行。

## 2. Timing Plan / 时间分配

| Part | Slides | Suggested time |
| --- | --- | ---: |
| Opening, motivation, and contributions | 1–7 | 5.75 min |
| System and problem setting | 8–11 | 5.0 min |
| Proposed DMSA-BM methodology | 12–20 | 15.25 min |
| Experimental evaluation | 21–26 | 8.5 min |
| Conclusions and closing | 27–28 | 1.0 min |
| **Total** | **28** | **35.5 min** |

中文解释：方法部分约占 15 分钟，是答辩核心。背景和系统模型只保留理解算法所需的内容。实验部分优先展示能够直接支撑贡献的四类证据，不逐表复述论文全部数字。

---

## Slide 1 — MPhil Thesis Defense

### Visible title and text / 页面英文内容

**MPhil Thesis Defense**

*Multimodal Sensing-Assisted User Association and Tracking in Vehicular Networks*

Yifeng Yuan  
MPhil Thesis Defense  
Department / University  
Supervisor: [Name]  
[Defense Date]

### Purpose and speaking focus / 中文说明

保持极简。开场只用一句话定义研究对象，例如“this thesis studies how roadside sensing can reduce beam measurements without applying a prediction to the wrong user”。不要在标题页提前列贡献或结果。

### Layout / 排版建议

- Use **MPhil Thesis Defense** in the fixed top title area.
- Place the full thesis title as the dominant left-aligned text in the upper half of the body area.
- Candidate, supervisor, institution, and date in a compact block at the lower left.
- Optional faint background crop from the simulated roadside scene or BEV map on the right, with low contrast.

### Suggested time

0.5 min

---

## Slide 2 — Background

### Visible title and text / 页面英文内容

**Background**

**Connected mobility and intelligent transportation rely on reliable V2I connectivity.**

Vehicular networks connect moving vehicles, roadside infrastructure, and network services.

**Roadside operating conditions**  
High mobility · rapidly changing geometry · intermittent blockage

**Communication requirements**  
High data rate · low latency · reliable connectivity

### Purpose and speaking focus / 中文说明

先建立共同场景：本研究关注的是移动车辆、路侧基础设施与网络服务之间的 V2I 连通性，而不是从模型或传感器直接切入。说明车辆高速运动、几何关系变化与遮挡使得高数据率、低时延和可靠性需要同时满足。最后自然引出：高频 V2I 链路如何在这些条件下保持可靠连接？

### Layout / 排版建议

- Use one simplified roadside V2I scene as the dominant visual: moving vehicles, a roadside BS, and surrounding infrastructure.
- Place the three operating-condition labels near the road scene and the three communication requirements in a concise lower band.
- Avoid beam diagrams and NR signalling details on this page; those begin on the next slide.

### Suggested time

0.75 min

---

## Slide 3 — V2I Beam Management Problem

### Visible title and text / 页面英文内容

**V2I Beam Management Problem**

**High-frequency V2I links provide bandwidth, but require narrow directional beams.**

Vehicle motion, blockage, and path evolution quickly age beam information.

SSB access → CSI-RS candidate measurement → CSI feedback → data transmission

Wider and more frequent measurements improve alignment reliability, but consume time-frequency resources that could carry payload data.

**Beam management is a recurrent measurement decision.**  
Measurement reliability ↔ measurement overhead

### Purpose and speaking focus / 中文说明

从大背景收束到通信问题：高频段以窄波束提供阵列增益，但链路方向会随车辆运动和传播变化快速失效。强调 beam management 不是一次性的 beam-index classification，而是持续的测量与资源分配决策。最后一句引出：能否借助环境感知缩小待测候选集合？

### Layout / 排版建议

- Left: a moving vehicle and roadside BS with narrow beam directions.
- Centre: the concise SSB-to-data measurement chain.
- Bottom: a small resource bar contrasting "measurement" and "payload data". Avoid detailed NR timing values here.

### Suggested time

0.75 min

---

## Slide 4 — Sensing-Assisted Beam Prediction: Single-Candidate Scenario

### Visible title and text / 页面英文内容

**Sensing-Assisted Beam Prediction: Single-Candidate Scenario**

**Multimodal sensing can predict or rank beams for a known physical target.**

Camera · position · radar · LiDAR · multimodal sensing  
→ physical-scene observations  
→ predicted beam or Top-\(K\) beam candidates

**Single-candidate formulations**  
A specified or visually isolated target is treated as the intended communication user.

\[
\widehat{k}_{u,n}=\arg\max_k f_\theta(\mathcal O_n)_k
\]

**Role in beam management**  
Prediction narrows the CSI-RS search; measured CSI quality still selects the service beam.

Complementary modalities can improve target observability under changing illumination, weather, occlusion, and geometry.

### Purpose and speaking focus / 中文说明

先肯定已有工作的价值：视觉、位置、雷达、LiDAR 与多模态观测均可在 CSI-RS 测量前预测或排序候选波束。单候选设定将观测到的目标默认视为通信用户，因此输入是场景观测、输出是该已知用户的 beam posterior 或 Top-\(K\) 集合。强调多模态提供互补观测；它为不同光照、天气、遮挡和几何条件下的 target observability 提供潜力，而非在未给出证据时宣称无条件鲁棒。

可在讲稿或小号页脚中引用代表性方向：Alrabeiah et al. (vision), Demirhan and Alkhateeb (radar), Jiang et al. (LiDAR), and Charan et al. (single-candidate vision-position).

### Layout / 排版建议

- Use a short sensing-to-candidate flow across the top.
- Place the single-candidate identity assumption and the compact formulation in two aligned body blocks.
- Put the role of prediction and the observability message in a highlighted bottom statement. Keep citations as a small footer rather than a literature-review list.

### Suggested time

1.0 min

---

## Slide 5 — Sensing-Assisted Beam Prediction: Multi-Candidate Scenario

### Visible title and text / 页面英文内容

**Sensing-Assisted Beam Prediction: Multi-Candidate Scenario**

**When several vehicles are visible, prediction must first identify the intended transmitter.**

**User-conditioned formulation**

\[
\widehat{k}_{u,n}=\arg\max_k f_\theta(\mathcal O_n,\mathbf g_{u,n})_k
\]

\(\mathcal O_n\): scene-level sensing observations  
\(\mathbf g_{u,n}\): location or other user-specific side information

**Limitations of user-conditioned prediction**

- User location can be unavailable, inaccurate, stale, or misaligned with the sensing frame.
- One candidate decision is required for each VUE; the user-conditioned workload scales with the active-user set.
- A target-level beam ranking is not yet a verified user-specific service decision.

**The question is not only which beams are likely, but whose candidate list it is.**

### Purpose and speaking focus / 中文说明

代表性的多候选工作会在场景观测之外输入用户位置或其他通信侧辅助信息，以完成 transmitter identification。不要说“所有多用户方案都需要位置”，因为也存在利用先前接收功率等通信侧信息的方案；本页强调的是，这类 user-specific 输入在实际道路场景中可能不可得、不精确、过时，或无法直接与感知坐标对齐。这里的 workload 表述限定为 user-conditioned candidate decision，避免把可并行的批量推理错误表述为必然的墙钟线性增长。

可在讲稿或小号页脚中引用 Charan et al. (multi-candidate vision-position) 与 Imran et al. (distributed sensing with communication-side information)。

### Layout / 排版建议

- Use the user-conditioned formulation as the central visual object.
- Place the definitions of \(\mathcal O_n\) and \(\mathbf g_{u,n}\) directly below the equation.
- Use three concise limitation callouts in the lower half; the final unanswered question forms the bottom takeaway.

### Suggested time

1.0 min

---

## Slide 6 — Sensing-Target-to-User Association

### Visible title and text / 页面英文内容

**Sensing-Target-to-User Association**

**Sensing observes physical targets, whereas beam management serves VUE identities.**

**Sensing domain**  
Physical vehicles → detections → perception tracks → target-level beam posteriors

**Communication domain**  
VUE identities → SSB / CSI-RS measurements → user-specific downlink transmission

**Association question**  
Which observed target provides credible candidate beams for VUE \(u\)?

A visible vehicle may not be an active VUE. The intended VUE may be temporarily unobserved. Multiple targets may be plausible in the same scene.

**Uncertain target evidence must not reduce the CSI-RS scan for a VUE.**

### Purpose and speaking focus / 中文说明

这是整场答辩最重要的问题定义页。通过两个身份域解释 target-to-user association 为什么不是普通 beam prediction 的附属细节：可见车辆、active VUE 和 perception track 并非天然一一对应。本页只定义问题与安全边界，不解释 IMM、Hungarian matching 或回退算法；这些属于后续方案。

### Layout / 排版建议

- Use two horizontal lanes or two vertical columns for sensing and communication domains.
- Place several vehicle icons on the sensing side and anonymised VUE identifiers on the communication side.
- Use question-mark connectors in the centre. Do not draw confirmed mappings or algorithmic steps yet.

### Suggested time

1.0 min

---

## Slide 7 — Research Objectives and Contributions

### Visible title and text / 页面英文内容

**Research Objectives and Contributions**

**Research question**  
How can distributed multimodal sensing reduce CSI-RS measurement overhead while preserving user-specific V2I decisions?

1. **Distributed multimodal BEV perception for joint vehicle detection and beam prediction**  
   Multi-view cameras and BS-local ISAC sensing produce vehicle detections and per-target CSI beam posteriors.

2. **Measurement-assisted target-to-user association**  
   VUE-indexed beam measurements and IMM tracking establish and maintain credible UE–track pairs.

3. **NR-oriented end-to-end evaluation**  
   Sensing use and fallback are related to CSI-RS overhead and average effective user rate.

### Purpose and speaking focus / 中文说明

这一页才首次将 IMM tracking 作为解决 association 问题的方案组成，而非另一个背景问题。三项贡献分别回应：目标可观测性、感知—通信身份歧义，以及系统级通信价值。不要展开网络层细节；只说明每项贡献解决的缺口及其输出。

### Layout / 排版建议

- Put the research question in a short opening statement near the top of the body area.
- Use three numbered horizontal stages connected by a thin line.
- Keep each contribution to a bold phrase and no more than two lines of explanation. Use the blue accent only on “Perception”, “Association”, and “Evaluation”.

### Suggested time

0.75 min

---

## Slide 8 — System Model

### Visible title and text / 页面英文内容

**System Model**

**01**

What information is available to the BS, and how does a beam candidate affect user rate?

### Purpose and speaking focus / 中文说明

章节切分页。口头过渡应说明，在介绍算法前需要先定义三个接口，即 sensing observation、communication measurement 和 overhead-adjusted rate。

### Layout / 排版建议

- Use **System Model** in the fixed top title area and place a large **01** in the body.
- One short question near the bottom.
- No diagram or bullet list.

### Suggested time

0.25 min

---

## Slide 9 — Network Architecture and Information Domains

### Visible title and text / 页面英文内容

**Network Architecture and Information Domains**

**Local system**  A target BS makes all communication decisions; neighbouring nodes extend only its sensing coverage.

\[
\mathcal U_b[n]=\{\text{active VUEs served by target BS }b\},
\qquad \mathcal N_b=\{\text{sensing-only neighbouring nodes}\}
\]

| Communication domain | Sensing domain |
|---|---|
| Identified VUEs \(u\in\mathcal U_b[n]\) | Unlabelled physical targets observed in the local road scene |
| CSI reporting, beam decisions, and downlink transmission | Distributed camera views and BS-local radio sensing |

**Locality principle**  All observations are aligned in a target-BS-centred BEV frame.  A VUE entering another serving cell establishes a new local association; no global cross-BS identity is assumed.

### Purpose and speaking focus / 中文说明

使用总体网络图解释 BS、SN、VUE 与 physical target 的角色边界。先说明 BS \(b\) 是唯一服务和决策节点，SN 只提供互补相机视角；再用两栏对照明确 communication domain 中的 VUE ID 与 sensing domain 中无标签物理目标不是同一概念。这一页只建立“为什么 association 必须显式完成”的系统前提，不提前讲具体 association 算法。

### Layout / 排版建议

- Use the network architecture diagram as the central visual: target BS in the centre, VUEs connected by solid communication links, and SN cameras connected by dashed sensing links.
- Place the two-column domain comparison beneath or to the right of the diagram.
- Highlight the target-BS-centred BEV region with a faint boundary; put the compact set notation in a footer band.

### Suggested time

1.5 min

---

## Slide 10 — ISAC Sensing Model

### Visible title and text / 页面英文内容

**ISAC Sensing Model**

**Known ISAC transmission**

\[
\mathbf{x}^{\mathrm{sen}}_{b,n}[p,l]
=\sqrt{P^{\mathrm{sen}}_{b,n}}\,
\mathbf{f}^{\mathrm{sen}}_{b,n}[p,l]s^{\mathrm{sen}}_{b,n}[p,l]
\]

**Echo model**

\[
\mathbf{y}^{\mathrm{echo}}_{b,n}[p,l]
=\bigl(\mathbf{H}^{\mathrm{sta}}_b[p]
+\mathbf{H}^{\mathrm{dyn}}_{b,n}[p,l]\bigr)
\mathbf{x}^{\mathrm{sen}}_{b,n}[p,l]
+\mathbf{z}^{\mathrm{sen}}_{b,n}[p,l]
\]

\[
\widetilde{\mathbf H}_{b,n}
=\widehat{\mathbf H}^{\mathrm{echo}}_{b,n}-\widehat{\mathbf H}^{\mathrm{sta}}_b
\ \xrightarrow{\ \mathcal T_{\mathrm{RAD}}\ }\ 
Z_{b,n}(\rho,\theta,\nu),
\qquad
|Z_{b,n}|^2>\eta^{\mathrm{CFAR}}_{b,n}
\]

\[
\mathcal P_{b,n}
=\bigl\{(\mathbf q_{b,m,n},a_{b,m,n})\bigr\}_{m=1}^{N^{\mathrm{pc}}_{b,n}}
\]

**Output**  Static clutter is suppressed; retained range--angle--Doppler cells form the BS-local point cloud used by multimodal perception.

### Purpose and speaking focus / 中文说明

严格按原文的 ISAC 建模链条讲解：已知 sensing symbol 经 sensing beam 发射；回波由静态环境分量、车辆相关动态分量和噪声组成；静态背景估计后相减，进行 range--angle--Doppler 处理，再通过 CFAR 保留有效单元。最后解释 \(\mathcal P_{b,n}\) 的每一点包含位置及强度、Doppler 或置信度等属性，并作为 BS-local radio observation 输入后续 BEV 感知。

### Layout / 排版建议

- Use a left-to-right signal chain: known ISAC waveform → echo channel → background subtraction / RAD / CFAR → local point cloud.
- Place the transmit and echo equations above the first two stages; put the compact processing and point-cloud equations under the latter stages.
- Use distinct muted colours for \(\mathbf H^{\mathrm{sta}}\) and \(\mathbf H^{\mathrm{dyn}}\), explaining that only the dynamic component carries vehicle evidence after clutter suppression.

### Suggested time

1.75 min

---

## Slide 11 — Downlink Communication Model

### Visible title and text / 页面英文内容

**Downlink Communication Model**

**1. Multi-user downlink data**

\[
\mathbf{x}_{b,n}
=\sum_{u\in\mathcal U_b[n]}
\sqrt{P_{b,u,n}}\,\mathbf w_{b,u,n}s_{b,u,n}.
\]

**2. CSI-RS scan, measured-beam selection, and equivalent-channel feedback**

For a candidate set \(\mathcal C_{b,u,n}\) with \(|\mathcal C_{b,u,n}|=K\),

\[
y^{\mathrm{CSI}}_{b,u,k,n}[l]
=\sqrt{P^{\mathrm{CSI}}_{b,k,n}}
h^{\mathrm{eq}}_{b,u,k,n}c_{b,k,n}[l]+z^{\mathrm{CSI}}_{b,u,k,n}[l],
\qquad
h^{\mathrm{eq}}_{b,u,k,n}
=\mathbf h^{\mathrm H}_{b,u,n}\mathbf f^{\mathrm{CSI}}_{b,k},
\]

\[
k^{\star}_{b,u,n}
=\underset{k\in\mathcal C_{b,u,n}}{\arg\max}\;
\widehat\gamma^{\mathrm{CSI}}_{b,u,k,n},
\qquad
\widehat h^{\mathrm{eq}}_{b,u,k^{\star},n}
=\operatorname{Corr}\!\left(y^{\mathrm{CSI}}_{b,u,k^{\star},n},c_{b,k^{\star},n}\right).
\]

**3. Hybrid RZF construction**

\[
\mathbf F^{\mathrm{RF}}_b[n]
=\bigl[\mathbf f^{\mathrm{CSI}}_{b,k^{\star}_{b,u_1,n}},\ldots,
\mathbf f^{\mathrm{CSI}}_{b,k^{\star}_{b,u_{U_b[n]},n}}\bigr],
\]

\[
\mathbf V^{\mathrm{RZF}}_b[n]
=\left(\widehat{\mathbf H}^{\mathrm{eff}}_b[n]\right)^{\mathrm H}
\left(\widehat{\mathbf H}^{\mathrm{eff}}_b[n]
\left(\widehat{\mathbf H}^{\mathrm{eff}}_b[n]\right)^{\mathrm H}
+\lambda_b\mathbf I\right)^{-1}\mathbf D_b[n],
\qquad
\mathbf W^{\mathrm{RZF}}_b[n]
=\mathbf F^{\mathrm{RF}}_b[n]\mathbf V^{\mathrm{RZF}}_b[n].
\]

### Purpose and speaking focus / 中文说明

先建立通信侧的 multi-user downlink：\(\mathbf x_{b,n}\) 是所有本地 VUE 的叠加发送信号，\(\gamma_{b,u,n}\) 显式包含目标 VUE 的有效信号、其他 VUE 造成的干扰与噪声。随后说明 CSI-RS 不是预测标签，而是从单位范数 codebook 中的实际发射参考信号；VUE 对每个被测 beam 得到 beam-domain equivalent channel 和 \(\widehat\gamma^{\mathrm{CSI}}\)。强调本页的边界：sensing 不替代 CSI acquisition，也不直接给出 service beam。

### Layout / 排版建议

- Split the page horizontally: the upper half is the multi-user downlink signal and SINR; the lower half is the CSI-RS codebook, observation, and reported quality.
- A narrow right-hand arrow can show \(\mathbf h^{\mathrm H}\mathbf f^{\mathrm{CSI}}\rightarrow \widehat h^{\mathrm{eq}}\rightarrow\widehat\gamma^{\mathrm{CSI}}\).
- Keep the final boundary sentence in an accent-colour footer, as it is the bridge to the proposed method.

### Suggested time

1.75 min

---

## Slide 12 — Downlink Communication Model

### Visible title and text / 页面英文内容

**Downlink Communication Model**

**1. Precoded received signal**

\[
y_{b,u,n}
=\sqrt{P_{b,u,n}}\mathbf h^{\mathrm H}_{b,u,n}
\mathbf w^{\mathrm{RZF}}_{b,u,n}s_{b,u,n}
+\sum_{v\in\mathcal U_b[n]\setminus\{u\}}
\sqrt{P_{b,v,n}}\mathbf h^{\mathrm H}_{b,u,n}
\mathbf w^{\mathrm{RZF}}_{b,v,n}s_{b,v,n}
+z_{b,u,n}.
\]

**2. Post-RZF SINR and achievable rate**

\[
\gamma^{\mathrm{RZF}}_{b,u,n}
=\frac{P_{b,u,n}|\mathbf h^{\mathrm H}_{b,u,n}\mathbf w^{\mathrm{RZF}}_{b,u,n}|^2}
{\sum_{v\in\mathcal U_b[n]\setminus\{u\}}
P_{b,v,n}|\mathbf h^{\mathrm H}_{b,u,n}\mathbf w^{\mathrm{RZF}}_{b,v,n}|^2+\sigma^2_{b,u,n}},
\qquad
R^{\mathrm{DL}}_{b,u,n}
=B_b\eta_b^{\mathrm{DL}}\log_2\!\left(1+\gamma^{\mathrm{RZF}}_{b,u,n}\right).
\]

**3. Beam-management resources and effective rate**

\[
\tau_{b,n}^{\mathrm{tot}}
=\tau_{b,n}^{\mathrm{SSB}}
+\tau_{b,n}^{\mathrm{CSI\text{-}RS}}
+\tau_{b,n}^{\mathrm{ctrl}}
+\tau_{b,n}^{\mathrm{data}},
\]

\[
\tau_{b,n}^{\mathrm{CSI\text{-}RS}}
=\sum_{e\in\mathcal E_b[n]}
\left\lceil\frac{K_e}{M}\right\rceil\delta_{\mathrm{probe}},
\qquad
\eta_{b,n}^{\mathrm{data}}
=\frac{\tau_{b,n}^{\mathrm{data}}}{\tau_{b,n}^{\mathrm{tot}}},
\]

\[
R^{\mathrm{eff}}_{b,u,n}
=\eta^{\mathrm{data}}_{b,n}R^{\mathrm{DL}}_{b,u,n}
=\eta^{\mathrm{data}}_{b,n}B_b\eta_b^{\mathrm{DL}}
\log_2\!\left(1+\gamma^{\mathrm{RZF}}_{b,u,n}\right).
\]

### Purpose and speaking focus / 中文说明

说明 \(\mathcal C_{b,u,n}\) 不是最终 beam，而是 CSI-RS 需要测量的候选集；VUE 在候选集内按实测 \(\widehat\gamma^{\mathrm{CSI}}\) 选择 \(k^\star\)，所有 VUE 的选择共同构成 RF precoder，再由数字 RZF 处理多用户干扰。接着解释开销模型：一次 acquisition event 中测量越多的 beam，\(\tau^{\mathrm{CSI\text{-}RS}}\) 越大、可用于数据的 \(\eta^{\mathrm{data}}\) 越小。最后用 \(R^{\mathrm{eff}}\) 收束：候选集质量影响 \(\gamma^{\mathrm{RZF}}\)，候选集大小影响 \(\eta^{\mathrm{data}}\)，两者共同决定系统性能。

### Layout / 排版建议

- Top: a compact sequence, candidate set → measured best beam → RF precoder → digital RZF, with the first equation underneath.
- Bottom: place the CSI-RS overhead equation on the left and the effective-rate equation, visually dominant, on the right.
- Use two colour cues throughout: a beam-quality path ending at \(\gamma^{\mathrm{RZF}}\), and a resource-cost path ending at \(\eta^{\mathrm{data}}\); both meet at \(R^{\mathrm{eff}}\).

### Suggested time

1.75 min

---

## Slide 13 — Design Requirements

### Visible title and text / 页面英文内容

**Design Requirements**

**A sensing-assisted beam-management policy must satisfy three information boundaries.**

1. **Target-level prediction**  
   The network predicts beams for an observed physical target, not for a known VUE identity.

2. **Measurement-grounded association**  
   Communication evidence must establish which track belongs to each VUE.

3. **Measured service-beam selection**  
   Sensing narrows CSI-RS candidates; measured quality selects the service beam.

### Purpose and speaking focus / 中文说明

这是 system model 到 methodology 的桥梁。用三条边界解释算法设计原因，并明确排除 oracle UE identity、position-to-beam inversion 和 prediction-only service-beam decision。

### Layout / 排版建议

- One vertical sequence with three numbered statements.
- A narrow side rail labelled “No oracle identity / No direct service-beam declaration”.
- Avoid a complex diagram because the next section begins with the complete framework figure.

### Suggested time

1.5 min

---

## Slide 14 — Proposed Framework

### Visible title and text / 页面英文内容

**Proposed Framework**

**02**

How does unbound sensing evidence become a VUE-specific CSI-RS decision?

### Purpose and speaking focus / 中文说明

章节切分页。用一句话强调接下来的算法顺序严格遵循 information flow，而不是多个独立模块的拼接。

### Layout / 排版建议

- Use **Proposed Framework** in the fixed top title area and place a large **02** in the body.
- Use the accent colour on “DMSA-BM”.

### Suggested time

0.25 min

---

## Slide 15 — DMSA-BM Architecture

### Visible title and text / 页面英文内容

**DMSA-BM Architecture**

**Framework flow**  DMSA-BM converts multimodal observations into measured beam decisions in four stages.

1. Distributed multimodal perception and beam prediction
2. IMM-based multi-object tracking
3. Initial or renewed target-to-user association
4. Association-gated CSI-RS candidate selection

\[
\mathcal O_{b,n}
\rightarrow \{d_{b,i,n},\mathbf p_{b,i,n}\}_i
\rightarrow \mathcal R_{b,n}
\rightarrow \pi_{b,n}
\rightarrow \mathcal C_{b,u,n}
\]

### Purpose and speaking focus / 中文说明

使用 Chapter 4 的 overview figure 作为全页主体。逐步解释 network 输出什么、tracker 做什么、初始关联如何建立，以及候选集何时可缩减。之后每一页分别放大其中一个关键模块。

### Layout / 排版建议

- Full-width process diagram in the centre.
- Four short stage labels above or below the diagram.
- Put the compact mathematical flow in a thin footer band.

### Suggested time

1.5 min

---

## Slide 16 — Joint Detection and Beam Prediction: Distributed Sensor Image Encoding and Cross-Node Fusion

### Visible title and text / 页面英文内容

**Joint Detection and Beam Prediction**

**Distributed Sensor Image Encoding and Cross-Node Fusion**

Calibrated multiview cameras are lifted into one target-BS-centred BEV grid; masked attention selects complementary valid evidence at each BEV cell.

\[
\mathbf F^{\mathrm{cam}}_{j\rightarrow b,n}
=\Phi_{\mathrm{img}}\!\left(
\mathcal I_{j,n};\mathbf T_{j\rightarrow b}
\right)
\]

\[
\alpha_{j,h,n}(\mathbf x)
\propto
m^{\mathrm{node}}_{j,n}(\mathbf x)
\exp\!\left(
e_{j,h,n}(\mathbf x)/T_{\mathrm{node}}
\right)
\]

\[
\mathbf f^{\mathrm{cam}}_{b,n}(\mathbf x)
=\overline{\mathbf f}^{\mathrm{cam}}_{b,n}(\mathbf x)
+\rho_{\mathrm{att}}\mathbf W^O
\operatorname{Concat}_{h}
\left(\sum_{j\in\mathcal J_b}
\alpha_{j,h,n}(\mathbf x)\mathbf v_{j,h,n}(\mathbf x)\right)
\]

**Output**  Target-BS-centred camera BEV feature \(\mathbf F^{\mathrm{cam}}_{b,n}\).  \(m^{\mathrm{node}}=0\) excludes an invalid projection.

### Purpose and speaking focus / 中文说明

用一个被 target-BS camera 遮挡、但被邻近 SN 看见的车辆作为直观例子。先说明每个节点的多视角图像经标定后 lift 到 target-BS-centred BEV；再说明 attention 是逐 BEV cell 选择有效节点证据，而不是给整个节点设定固定权重。target-BS-conditioned query 保留 serving-link 视角，geometry-aware key 区分邻居位置，mask 只排除无效投影。

### Layout / 排版建议

- Use one left-to-right technical schematic: three roadside camera nodes → aligned per-node BEV patches → enlarged BEV-cell attention example → fused camera BEV.
- The enlarged cell should show target-BS occlusion, a valid neighbouring view with high attention weight, and one invalid projection with mask zero.
- Place the camera-lift and masked-attention equations beneath the schematic; do not use a text-card grid.

### Suggested time

2.0 min

---

## Slide 17 — Joint Detection and Beam Prediction: Multimodal BEV Feature Fusion

### Visible title and text / 页面英文内容

**Joint Detection and Beam Prediction**

**Multimodal BEV Feature Fusion**

The fused camera BEV and the BS-local ISAC point cloud are projected to a common BEV space and combined by local–global gated attention.

\[
\mathbf U_{b,n}
=
\left[
\widetilde{\mathbf F}^{\mathrm{cam}}_{b,n}
\,\|\,
\widetilde{\mathbf F}^{\mathrm{isac}}_{b,n}
\,\|\,
\left|
\widetilde{\mathbf F}^{\mathrm{cam}}_{b,n}
-\widetilde{\mathbf F}^{\mathrm{isac}}_{b,n}
\right|
\right]
\]

\[
\beta_{q,b,n}(\mathbf x)
=\operatorname{MaskedSoftmax}_{q}\!\left(
\ell^{\mathrm{loc}}_{q,b,n}(\mathbf x)
+\ell^{\mathrm{glo}}_{q,b,n}
\right)
\]

\[
\mathbf F_{b,n}
=\sigma\!\left(
\mathbf F^{\mathrm{modal},0}_{b,n}
+\Phi_{\mathrm{ref}}\!\left(
\mathbf F^{\mathrm{modal},0}_{b,n}
\right)\right)
\]

**Output**  Shared multimodal BEV feature \(\mathbf F_{b,n}\).  Availability masks exclude missing inputs only.

### Purpose and speaking focus / 中文说明

说明 camera BEV 提供语义和可见性，BS-local ISAC BEV 提供互补的局部几何与动态感知证据。先由共享通道投影和差异特征形成 \(\mathbf U_{b,n}\)，再由 local gate 适应遮挡、camera blind region 与 point-cloud sparsity，由 global gate 适应 scene-wide observation condition。不要说天气标签直接进入网络，也不要将 availability mask 解释成独立 reliability score。

### Layout / 排版建议

- Use a top-to-bottom fusion flow: fused camera BEV and ISAC BEV → common-channel projection and interaction \(\mathbf U\) → local/global gates → shared multimodal BEV.
- Illustrate local attention with a small spatial weight map and global attention with one scene-level scalar; avoid a second large process diagram.
- Keep the availability-mask boundary as a short footer under the final shared BEV map.

### Suggested time

2.0 min

---

## Slide 18 — Joint Detection and Beam Prediction: Network Output Definition

### Visible title and text / 页面英文内容

**Joint Detection and Beam Prediction**

**Network Output: Target Detections and Beam Rankings**

A single shared BEV representation is decoded into vehicle-centre, attribute, and dense beam-score maps.

\[
\left(
\mathbf H_{b,n},\mathbf A_{b,n},\mathbf P_{b,n}
\right)
=\Phi_{\mathrm{joint}}\!\left(\mathbf F_{b,n}\right)
\]

\[
d_{b,i,n}
=
\left(
\widehat{\mathbf r}_{b,i,n},
\widehat{\mathbf a}_{b,i,n},
\widehat c_{b,i,n}
\right),
\qquad
\mathbf p_{b,i,n}
=\operatorname{softmax}\!\left(
\operatorname{Sample}(\mathbf P_{b,n},\widehat{\mathbf r}_{b,i,n})
\right)
\]

- Each detected physical target exports a BEV centre, attributes, confidence, and a 192-way beam posterior.
- Training uses Top-1 cross-entropy with the strongest physical codebook beam; inference retains the full posterior for ranking.
- The output contains neither a VUE identity nor a final service-beam decision.

### Purpose and speaking focus / 中文说明

先用精简全网络图回顾前两页的 camera BEV、ISAC BEV、cross-node fusion 与 multimodal fusion 如何汇入 \(\mathbf F_{b,n}\)。随后明确 joint head 的三个 dense maps：centre heatmap \(\mathbf H\)、attribute map \(\mathbf A\) 与 192-way beam-logit map \(\mathbf P\)。local maximum 定义 physical target，beam logits 在该 decoded centre 采样后形成 target-level posterior。强调 link coordinate 仅用于训练监督采样，不是 forward input；Top-1 CE 也不代表网络输出 CSI-power distribution。

### Layout / 排版建议

- Left two thirds: a simplified complete architecture, from distributed cameras and BS-local ISAC through the two fusion stages to \(\mathbf F_{b,n}\) and the joint head.
- Right one third: one target example showing centre/attribute/confidence output and a 192-way posterior sampled at the decoded centre.
- Place the three output boundaries in a compact footer: target-indexed only; no VUE identity; no direct service-beam decision.

### Suggested time

1.75 min

---

## Slide 19 — IMM-Based Physical-Target Tracking

### Visible title and text / 页面英文内容

**IMM-Based Physical-Target Tracking**

**From target-level outputs to persistent, beam-aware physical tracks**

\[
\{(d_{b,i,n},\mathbf p_{b,i,n})\}_i
\quad\longrightarrow\quad
\mathcal R_{b,n}
\]

\[
\mathcal R^{\mathrm{obs}}_{b,n}
=
\left\{
r:\left(
\widehat{\mathbf x}_{r,n},\mathbf P_{r,n},
\mathbf p^{\mathrm{obs}}_{r,n}
\right)
\right\}
\]

\(i\): frame-specific detection index \(\;\cdot\;\)
\(r\): persistent physical-track ID

**CV model**  \(\mathbf x^{\mathrm{CV}}=[x,y,v_x,v_y]^{\mathsf T}\)

**CT model**  \(\mathbf x^{\mathrm{CT}}=[x,y,v,\psi,\omega]^{\mathsf T}\)

\[
\mu^{(\ell)}_{r,n}\propto
\Lambda^{(\ell)}_{r,i,n}\bar\mu^{(\ell)}_{r,n}
\]

**Key boundary**  IMM predicts motion continuity; gated one-to-one detection-to-track updates preserve the persistent track ID.  A track is not a VUE identity.

### Purpose and speaking focus / 中文说明

先把 Slide 18 的当前帧 detection index \(i\) 转换成跨帧持续的 physical-track ID \(r\)。被当前 detection 更新的 track 属于 \(\mathcal R^{\mathrm{obs}}_{b,n}\)，并获得当前 posterior \(\mathbf p^{\mathrm{obs}}_{r,n}\)，这是下一页唯一允许参与 UE association 的感知证据。IMM 以 CV/CT 分支预测和更新运动状态；真正抑制 ID 跳变的是“预测 + 门控 + detection-to-track 一对一更新”，不是 IMM 单独完成。predicted-only track 可保留状态，但不属于 \(\mathcal R^{\mathrm{obs}}_{b,n}\)，不能减少 CSI-RS 测量。

### Layout / 排版建议

- Add a thin input-to-output strip: Slide 18 output \(\{(d_i,\mathbf p_i)\}\) → prediction/gating/update → observed track card \(r\).
- Centre: compact CV/CT state pills and the proportional model-posterior relation; do not show full Kalman recursion.
- Bottom: use a simplified editable IMM mini-diagram, “Mix → CV/CT filtering → likelihood reweighting → fused track update”.  Avoid the ambiguous “Predictive Beamforming” / “Associated Measurement” labels in the existing PDF.
- Right-side track card lists persistent ID, state, uncertainty, and \(\mathbf p^{\mathrm{obs}}_{r,n}\).  End with the bold boundary sentence.

### Suggested time

1.75 min

---

## Slide 20 — Conventional Measurement for Track–VUE Association

### Visible title and text / 页面英文内容

**Conventional Measurement for Track–VUE Association**

**For each affected VUE, an SSB-guided CSI-RS scan creates VUE-indexed evidence for matching currently observed tracks.**

**Communication evidence**

Association event  →  affected VUE \(u\)  →  SSB sweep \(s_{b,u,n}\)

\[
\left|\mathcal C^{\mathrm{ref}}_{b,u,n}(K_{\mathrm{ref}})\right|=K_{\mathrm{ref}}
\]

CSI-RS scan \(k\in\mathcal C^{\mathrm{ref}}_{b,u,n}\)
→ \(\{\widehat\gamma^{\mathrm{CSI}}_{b,u,k,n}\}_k\)
→ reported beam evidence \(\kappa_{b,u,n}\)

**Track evidence from Slide 19**

\[
\mathcal R^{\mathrm{obs}}_{b,n}:\quad r\mapsto\mathbf p^{\mathrm{obs}}_{r,n}
\]

**Association output**

Feasible cost matrix  →  one-to-one matching with \(\emptyset\)
→ accepted \(\pi_{b,n}(u)=r\)  or  unmatched \(\pi_{b,n}(u)=\varnothing\)

### Purpose and speaking focus / 中文说明

这页只讲流程，不展开大段公式。对 initial access、serving-cell change 或 association support 丢失的 affected VUE，保留传统 SSB-guided fixed-width CSI-RS refinement。VUE 对固定大小 \(K_{\mathrm{ref}}\) 的候选集测量并反馈 CSI-RS quality，形成带 VUE identity 的 \(\kappa_{b,u,n}\)。同时，Slide 19 提供当前 observed tracks 及各自 posterior。两类证据在 cost matrix 中相遇：SSB-parent 不一致或非当前观测的 pair 直接不可行；其余 pair 参加含 unmatched option 的一对一 assignment。强调 CSI-RS quality 比单纯“power”更准确。

### Layout / 排版建议

- Use two coloured lanes that converge: blue communication lane (SSB + fixed-width CSI-RS scan) and green sensing-track lane (\(\mathcal R^{\mathrm{obs}}\) + \(\mathbf p^{\mathrm{obs}}\)).
- Centre: an editable 2-by-3 illustrative cost matrix with one green low-cost pair, grey infeasible cells, and a final \(\emptyset\) column.
- Right: assignment box followed by a small acceptance diamond; accepted mapping proceeds to Slide 21, while unmatched VUE remains on conventional refinement.
- Use native PowerPoint shapes and connectors, not a raster workflow image, so every label remains editable.

### Suggested time

1.75 min

---

## Slide 21 — Association Scoring and Candidate-Set Policy

### Visible title and text / 页面英文内容

**Association Scoring and Candidate-Set Policy**

**Only a confident, currently observed track–VUE mapping can reduce CSI-RS scanning.**

**1. Measurement-to-track compatibility**

\[
c^{\mathrm{assoc}}_{u,r,n}
=-\frac{\log\!\left(
p^{\mathrm{obs}}_{r,n}(\kappa_{b,u,n})+\epsilon
\right)}{\log M_{\mathrm{CSI}}}
\]

\[
(u,r)\in\mathcal E^{\mathrm{assoc}}_{b,n}
\iff
\varphi_b(\kappa_{b,u,n})=s_{b,u,n},\quad
r\in\mathcal R^{\mathrm{obs}}_{b,n}
\]

**2. Partial one-to-one association**

\[
\widehat\sigma
=
\underset{\sigma}{\arg\min}
\sum_{u\in\mathcal U_b^{\mathrm{evt}}[n]}
c^{\mathrm{assoc}}_{u,\sigma(u),n},
\qquad
\sigma(u)\in\mathcal R^{\mathrm{obs}}_{b,n}\cup\{\emptyset\}
\]

\[
A_{u,r,n}=\mathbf 1\!\left\{
c^{\mathrm{assoc}}_{u,r,n}\leq\tau_{\mathrm{assoc}},\
\Delta_{u,r,n}\geq\tau_{\mathrm{margin}}
\right\}
\]

**3. Association-gated CSI-RS candidates**

\[
\mathcal C_{b,u,n}=
\begin{cases}
\operatorname{TopK}_{K_{\mathrm{scan}}}
\left(\mathbf p^{\mathrm{obs}}_{\pi_{b,n}(u),n}\right),
& A_{u,r,n}=1,\ \pi_{b,n}(u)\in\mathcal R^{\mathrm{obs}}_{b,n},\\
\mathcal C^{\mathrm{ref}}_{b,u,n}(K_{\mathrm{ref}}),
& \text{otherwise}.
\end{cases}
\]

\[
k^\star_{b,u,n}
=\arg\max_{k\in\mathcal C_{b,u,n}}
\widehat\gamma^{\mathrm{CSI}}_{b,u,k,n}
\]

**Measurement safeguard**  The posterior ranks CSI-RS candidates; measured CSI-RS quality selects the service beam.

### Purpose and speaking focus / 中文说明

按照 Slide 20 的流程逐步给出计算。先用 \(\kappa_{b,u,n}\) 在 observed track posterior 中取值，构造较小为好的 compatibility cost；再由 SSB-parent consistency 和 current observation 形成 feasible matrix，求包含 \(\emptyset\) 的一对一 assignment；最后同时使用 cost threshold 与 margin threshold 接受或拒绝匹配。只有 accepted mapping 且 track 当前被观测到时，\(\mathbf p^{\mathrm{obs}}\) 才定义缩小后的 \(\operatorname{TopK}\) 测量集；否则使用传统 \(\mathcal C^{\mathrm{ref}}\)。结尾明确服务波束仍由实测 quality 的 argmax 选择。adaptive-width \(\zeta\) 作为扩展策略移至 appendix，避免打断主流程。

### Layout / 排版建议

- Use three top-to-bottom formula bands matching Slide 20’s three workflow stages.
- Put a small labelled cost matrix beside the first equation: green = low cost, grey = infeasible, last column = \(\emptyset\).  This is explanatory, not a separate algorithm diagram.
- Keep assignment and acceptance equations compact in the middle band; reserve the lower band for the candidate-set cases and final measured-beam equation.
- Finish with a distinct safeguard strip.  Do not include the adaptive-width variant on this main-path slide.

### Suggested time

2.0 min

---

## Slide 22 — Algorithm Summary

### Visible title and text / 页面英文内容

**Algorithm Summary**

**Key property**  The framework separates sensing computation from air-interface measurement cost.

**Per sensing epoch**

1. Construct distributed multimodal BEV features.
2. Decode detections and beam-class posteriors.
3. Predict, assign, and update physical-target tracks.
4. Reassociate only when an association event occurs.
5. Select sensing-derived or SSB-guided CSI-RS candidates.

**Scaling drivers**  
Views and BEV resolution · targets and tracks · assignment size · \(M_{\mathrm{CSI}}\) · \(K_{\mathrm{scan}}\)

### Purpose and speaking focus / 中文说明

快速总结算法，重点区分每个 sensing epoch 的 perception/tracking 与事件触发的 association。复杂度只说明 scaling driver，不做没有 profiling 支撑的实时延迟宣称。最后过渡到实验：上游 prediction 是否有用，最终要由 association-gated communication policy 验证。

### Layout / 排版建议

- Five-step horizontal process across the slide.
- A thin bottom band separates computational scaling from air-interface scan width.
- Avoid reproducing the full pseudocode environment.

### Suggested time

1.25 min

---

## Slide 23 — Experimental Evaluation

### Visible title and text / 页面英文内容

**Experimental Evaluation**

**03**

Does the complete decision chain improve communication performance after measurement cost is included?

### Purpose and speaking focus / 中文说明

章节切分页。过渡时强调实验不是只验证 beam accuracy，而是沿 detection、beam ranking、sensing use/fallback、overhead 和 effective rate 建立证据链。

### Layout / 排版建议

- Use **Experimental Evaluation** in the fixed top title area and place a large **03** in the body.
- Optional small line of metric names at the bottom, without numbers.

### Suggested time

0.25 min

---

## Slide 24 — Experimental Setup

### Visible title and text / 页面英文内容

**Experimental Setup**

**Evaluation principle**  A common multimodal and communication protocol links perception results to user rate.

- Four-BS roadside scenario under Clear, Rain/Fog, and Night conditions
- Target-BS and neighbouring-node cameras, BS-local ISAC point clouds, trajectories, and ray-traced channels
- 48 SSB beams and 192 CSI-RS beams
- 100 ms SSB periodicity and 20 ms CSI-RS periodicity
- Common Doppler, power, noise, RZF, and resource-accounting assumptions

**Evaluation chain**  
Detection → Beam ranking → Association-conditioned sensing use → CSI-RS overhead → Average effective user rate

### Purpose and speaking focus / 中文说明

说明 train/validation/test split 互斥，并明确 Rain/Fog association margin 0.10 是固定的 test-tuned operating point，因此结果只代表该操作点，不能宣称独立 held-out 泛化。强调系统结果来自同一 radio profile 下的公平比较。

### Layout / 排版建议

- Left two thirds: one representative scene montage with camera, BEV/point-cloud, and channel views.
- Right: concise protocol parameters.
- Bottom: one horizontal evaluation chain.

### Suggested time

1.5 min

---

## Slide 25 — Perception and Beam Prediction

### Visible title and text / 页面英文内容

**Perception and Beam Prediction**

**Main observation**  Distributed multimodal attention improves target availability without uniformly dominating every beam-ranking metric.

**Distributed multimodal attention**

- AP@2m: **78.73%**
- Recall@2m: **81.51%**
- Top-4 power ratio: **97.01%**

**Local camera–ISAC fusion**

- Beam Top-1@2m: **71.54%**
- Beam Top-4@2m: **94.66%**

**Interpretation**  
Better target observability and better beam ranking are related but not identical objectives.

### Purpose and speaking focus / 中文说明

使用总体结果表的简化版本或重新绘制的分组图。不要把五个方法和五个指标全部塞成原始宽表。口头补充 Rain/Fog 下 ISAC-only detection 优于 Camera-only，以及不同天气下模态互补性不同。核心结论是多模态/跨节点主要改善 target availability，但 beam ranking 仍需单独评价。

### Layout / 排版建议

- Dominant grouped bar chart or two aligned metric groups.
- A small interpretation sentence below the chart.
- Use blue to highlight the proposed method and dark gray to highlight the best local-fusion beam metrics.

### Suggested time

2.0 min

---

## Slide 26 — Cooperative Sensing Nodes

### Visible title and text / 页面英文内容

**Cooperative Sensing Nodes**

**Main observation**  Additional roadside viewpoints primarily improve detection and localisation.

Distributed multimodal attention with 0 → 5 nearby nodes

- AP@2m: **38.59% → 80.41%**
- Recall@2m: **52.34% → 83.15%**
- Beam Top-4@2m remains high and approaches saturation.

**Interpretation**  
Cross-node sensing first expands target observability; its effect on exact Top-1 ranking is more method dependent.

### Purpose and speaking focus / 中文说明

明确这些是 fixed-model missing-node robustness/coverage curves，不是针对每个节点数重新训练模型。优先展示 AP 和 Recall 曲线，beam curve 可作为小图或口头说明。

### Layout / 排版建议

- Large line chart occupying about 70% of the slide.
- Two large numeric callouts on the right.
- Small caption stating “fixed trained model; available nodes varied at test time”.

### Suggested time

1.25 min

---

## Slide 27 — Communication Performance

### Visible title and text / 页面英文内容

**Communication Performance**

**Main result**  DMSA-BM achieves a higher effective rate with lower CSI-RS overhead.

| Policy | Effective rate | CSI-RS overhead |
| --- | ---: | ---: |
| SSB-guided refinement, \(K_{\mathrm{ref}}=4\) | 142.248 Mbps | 1.90% |
| SSB-guided refinement, \(K_{\mathrm{ref}}=12\) | 115.890 Mbps | 5.71% |
| **DMSA-BM** | **146.332 Mbps** | **1.56%** |

**Condition-dependent operation**

- Sensing use: 76.35% in Clear, 56.65% in Rain/Fog, and 30.07% at Night
- The remaining cases retain SSB-guided refinement.

### Purpose and speaking focus / 中文说明

这是最核心的系统结果页。建议将三种 policy 画成 rate–overhead 平面上的三个点，而不是只放表格。说明 \(K_{\mathrm{ref}}=4\) 和 12 是同一 hierarchical baseline 的两个 operating points。强调 Night/Rain-Fog 下 fallback 增加是方案的一部分，而不是被隐藏的失败样本。

### Layout / 排版建议

- Left two thirds: scatter plot with overhead on the x-axis and effective rate on the y-axis.
- Right: three large per-condition sensing-use values and one fallback explanation.
- Keep the macro-average table as a small supporting object or replace it entirely with labelled chart points.

### Suggested time

2.0 min

---

## Slide 28 — Ablation and Tracking Results

### Visible title and text / 页面英文内容

**Ablation and Tracking Results**

**Main observation**  Local multimodal complementarity provides most of the gain, while distributed sensing improves the final operating point.

| Sensing configuration | Effective rate | CSI-RS overhead | Sensing use |
| --- | ---: | ---: | ---: |
| Camera-only | 138.868 Mbps | 1.86% | 47.93% |
| ISAC-only | 142.522 Mbps | 1.81% | 49.03% |
| Local camera–ISAC fusion | 143.701 Mbps | 1.80% | 58.28% |
| **DMSA-BM** | **146.332 Mbps** | **1.56%** | 54.35% |

**Tracker check**  
IMM 146.332 · KF-CV 146.373 · KF-CT 145.880 Mbps

### Purpose and speaking focus / 中文说明

解释 sensing use 更高并不自动意味着 rate 更高。Local fusion 的 sensing use 高于 DMSA-BM，但 rate 更低、overhead 更高。Tracker 数值非常接近，KF-CV 在该操作点略高于 IMM，因此不能以 rate 声称 IMM 普遍优越；IMM 的采用理由是多模型状态估计与 association maintenance，而不是当前表格证明其绝对性能最优。

### Layout / 排版建议

- Main area: four horizontal bars for effective rate, with overhead as small adjacent labels.
- Bottom strip: three tracker rate markers on a compressed axis to make their small separation visually honest.
- Avoid a dense five-column table in the final deck even though the exact values are listed here for authoring.

### Suggested time

1.5 min

---

## Slide 29 — Conclusion

### Visible title and text / 页面英文内容

**Conclusion**

**04**

What has been established, and what remains before deployment?

### Purpose and speaking focus / 中文说明

最后一个章节切分页。提醒评委接下来不是重复贡献名称，而是回答开场提出的问题并明确证据边界。

### Layout / 排版建议

- Use **Conclusion** in the fixed top title area and place a large **04** in the body.
- No result numbers; reserve them for the final synthesis slide.

### Suggested time

0.25 min

---

## Slide 30 — Conclusions and Future Work

### Visible title and text / 页面英文内容

**Conclusions and Future Work**

**Central conclusion**  Distributed sensing becomes useful for beam management only through a user-specific measurement interface.

**Established in this thesis**

- Distributed multimodal BEV perception jointly detects vehicles and ranks per-target CSI beams.
- IMM tracking preserves physical-target continuity without treating a track as a VUE identity.
- Beam measurements establish target-to-user associations, and only accepted, currently observed pairs reduce CSI-RS scanning.
- Under the stated operating point, DMSA-BM reaches **146.332 Mbps** with **1.56% CSI-RS overhead**.

**Next steps**  
Real-world validation · protocol-level NR evaluation · online/domain adaptation · cooperative multi-BS association and handover

**Questions and discussion**

### Purpose and speaking focus / 中文说明

回扣 Slide 2–3 的问题。最后一句口头总结建议为：“The central contribution is not sensing-only beam prediction, but a complete interface that determines when target-level sensing evidence is applicable to a communication user.” 随后停在本页进入答问，而不是使用只有 “Thank you” 的空白结束页。

### Layout / 排版建议

- Use **Conclusions and Future Work** in the fixed top title area.
- Place the central conclusion as the first body statement rather than enlarging it into a second title.
- Four concise findings in a single left-aligned column.
- One large rate/overhead result callout on the right.
- Future-work line and “Questions and discussion” at the bottom.

### Suggested time

0.75 min

---

## 3. Authoring Notes for the Next Stage / 后续制作注意事项

1. Reuse or redraw the Chapter 4 framework and IMM figures rather than reproducing dense LaTeX equations as screenshots.
2. Rebuild result visuals from `paper_results/tables` and `paper_results/figures` so that font size, colour, and emphasis are consistent across the deck.
3. Preserve the formal result boundary. The Rain/Fog association margin is a fixed test-tuned operating point, and accepted-association accuracy, lower-tail rate, and outage are not reported as primary results.
4. Do not claim universal IMM superiority. The current tracker table reports 146.332, 146.373, and 145.880 Mbps for IMM, KF-CV, and KF-CT, respectively.
5. Keep the proposed perception name consistent as **Distributed multimodal attention (proposed)** and the full system name as **Distributed Multimodal Sensing-Assisted Beam Management (DMSA-BM)**.
6. Use **SSB-guided CSI-RS refinement** for the communication baseline. \(K_{\mathrm{ref}}=4\) and 12 are two operating points of the same hierarchical baseline.
7. Reserve backup slides for detailed equations, full metric tables, ISAC echo modelling, IMM covariance recursion, and additional weather-stratified results. These backup slides are not included in the 28-slide main-deck count.
