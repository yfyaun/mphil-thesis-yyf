# 工作说明

最后更新：2026-07-16

论文暂定题目：*Multimodal Sensing-Assisted User Association and Tracking in Vehicular Networks*

本文档是当前研究工作的事实源，用于界定论文的研究对象、已采用的方法、证据边界和后续实验要求。正式 LaTeX 正文须依据本文档及 `docs/thesis_outline.md` 撰写；不得把本文档中的内部确认事项、开发性结果或诊断性上界写成已经验证的论文结论。

## 1. 论文命题与研究边界

### 1.1 核心命题

本文研究多小区 V2I 场景中的多模态感知辅助波束管理。传统 SSB/CSI-RS 测量在高速移动、遮挡和天气变化下具有显著资源开销，且测得的 CSI 会随时间老化。道路侧基础设施能够同时提供相机和 ISAC 观测，但感知结果本身可能漏检、误检、失去连续身份，且不天然携带通信 UE 身份。

因此，本文采用以 target BS 为中心的 Distributed Multimodal Sensing-Assisted Beam Management (DMSA-BM) 框架：在统一的 target-BS-centered BEV 表达中，从服务 BS、邻近 sensing nodes (SNs) 的相机观测和 BS-local ISAC 点云中检测车辆，并预测其 CSI 波束类别后验分数；以不携带通信身份的感知轨迹为中介，在传统测量支持的初始接入或重关联阶段建立 UE--track binding；只有在绑定和当前观测均可靠时，才用感知提示压缩下一次 CSI-RS 测量候选集。否则，系统保留 SSB-guided CSI-RS refinement。

论文的目标不是将感知无条件替代传统波束管理，也不是只提高单帧 beam Top-1 分类率；目标是在统一资源模型下检验感知辅助候选集压缩在 effective rate、outage/failure risk 与 pilot overhead 之间的可验证权衡。

### 1.2 场景、数据与协议边界

- 数据来自既有 `mmbeam_town05_3weather_v1` 数据集；本文不生成 CARLA、Sionna RT、图像、点云或无线信道资产。
- 本文构建的是基于既有多模态数据资产的系统级 Multimodal V2I Simulator；它复现和比较 beam-management policy、测量事件、RZF 与资源记账，而不重新生成原始感知或信道资产。
- 场景包括 `clear_day`、`rain_fog_day` 和 `night` 三种天气。训练、验证和测试切分由数据集 manifest 显式定义。
- 单帧感知样本由 `(weather_id, frame_id, bs_id)` 标识，其中 `bs_id` 是 target BS；链路监督额外由 `ue_id` 标识，即 `(weather_id, frame_id, bs_id, ue_id)`。
- 单帧感知和初始轨迹均在 target-BS-centered Sionna BEV 局部坐标系中定义；该坐标系不是全局坐标系。
- 当前码本由 48 个 SSB 波束和 192 个 CSI 波束组成，每个 CSI 波束对应一个 SSB parent。码本、SSB/CSI-RS 周期和候选数必须在实验设置或表注中明确报告。
- RT 信道以相邻保存帧构成的约 100 ms segment 为基础：segment 内采用固定多径参数及 Doppler 相位演化，跨 segment 使用新的参考信道。本文可研究候选集、pilot 周期和 CSI aging 的相对影响，但不声称复现完整 NR 协议或 segment 内所有遮挡变化。
- 本文重点是每个 target BS 内的感知、轨迹维持和通信绑定。UE 切换到新的 serving cell 后重新绑定；当前版本不主张跨 BS 的全局统一轨迹 ID。

### 1.3 统一角色定义

| 术语 | 当前采用的含义 | 不应混同为 |
| --- | --- | --- |
| target BS | 构造局部 BEV、输出 detection 并服务 UE 的基站 | 全局融合中心 |
| sensing node (SN) | 为 target BS 提供邻近视觉观测的感知节点 | 独立服务小区 |
| perception detection / track | 未绑定通信身份的车辆观测或其时间连续轨迹 | 已识别的 UE |
| communication UE | 参与 SSB、CSI-RS 和下行传输的通信实体 | 感知网络输出类别 |
| UE--track binding | 由通信测量和感知证据建立的映射 | 由 ground truth 强行赋予的 ID |
| candidate beam | 下一次 CSI-RS 实测的候选集合 | 已确认的最优下行 beam |
| oracle / ground truth | 上界、诊断和正确性统计所用信息 | 正式决策输入 |

## 2. 研究问题、假设与贡献

### 2.1 核心科学问题

1. 多模态与跨节点观测能否在 target-BS-centered BEV 中同时支持车辆检测和条件 CSI 波束预测？
2. 以最强物理 beam 为 Top-1 标签训练的联合检测--波束预测网络，能否产生可用于候选 CSI-RS 测量的 target-level beam scores？
3. 感知轨迹 ID 的稳定性以及初始/重关联正确性如何影响 beam hint 能否持续服务正确 UE？
4. 在计入 SSB、CSI-RS、CSI aging、RZF、切换和 fallback 后，基于 association acceptance 的感知辅助能否形成可接受的 rate--overhead Pareto trade-off？

Chapter 1 将上述科学问题收束为两项方法挑战和一项验证要求。挑战一是条件变化下单站点、单模态的目标可观测性受限，对应分布式多模态感知与 beam prediction；挑战二是 sensing target 与 communication UE 之间存在身份歧义，对应 communication-measurement-assisted target-to-user association 与 IMM-based tracking。系统级 rate--overhead 评价不再单列为第三项挑战，而作为第三项研究目标，用于验证前两项方法能否在关联接受、current-observation requirement 与 conventional fallback 共同作用下形成可度量的通信收益。

### 2.2 研究假设

- **H1：信息互补。** 相机的语义和可见性信息、ISAC 的无线感知信息以及邻近节点的互补视角共同支持检测与 beam prediction；融合收益应同时由 detection 和 matched-beam 指标验证。
- **H2：Top-1 beam prediction supports candidate measurement.** strongest-beam cross-entropy 所学习的 192-way class posterior 可为 Top-\(K\) candidate measurement 与 measurement-assisted association 提供 score ordering；其候选价值应由 Beam Top-1/Top-\(K\) 与 Top-\(K\) power ratio 验证，而不将 posterior 解释为物理 CSI 功率分布。
- **H3：身份是系统中介变量。** 正确的位置和单帧 beam ranking 仍可能因 ID switch 或错误 binding 被交给错误 UE；因此 tracking 和 binding 是感知指标转化为通信指标的必要中间环节。
- **H4：关联接受后使用感知。** association cost、assignment margin 与 current-observation requirement 共同决定是否接受 UE--track binding；只有已接受且当前可观测的 binding 才能产生 sensing candidates，否则使用 conventional fallback。

### 2.3 当前采用的贡献表述

下列为方法与评估层面的拟贡献。只有在冻结 test 的同协议结果支持时，才能将其扩展为性能优越性结论。

1. 提出 distributed multimodal BEV perception framework，在 target-BS-centred BEV 中联合执行车辆检测与 beam prediction。该方法融合 target BS 与邻近 SN 的相机观测以及 BS-local ISAC 点云，以缓解单站点或单模态在遮挡、视场和环境变化下的目标可观测性限制；Top-1 classifier 输出 per-target CSI beam-class posterior，其排序用于 target-to-user association 与候选 CSI-RS 测量。
2. 构建 target-to-user association framework with IMM-based tracking，以处理物理 sensing target 与 communication UE 之间并非天然对应的问题。传统 SSB/CSI-RS 测量用于建立或恢复 UE--track binding，IMM multi-object tracking 维持感知目标的时序连续性；仅当 association 已接受且对应 track 当前可观测时，才使用 sensing-derived candidates，否则回退至 SSB-guided refinement。
3. 建立 multimodal V2I simulation and 5G NR-oriented beam-management evaluation framework，将多模态感知、时变 V2I 信道、communication measurement 与资源记账置于一致的评价链条中。该框架以 average effective user rate、CSI-RS overhead、sensing-use/fallback 和候选测量数刻画 perception-assisted policy 的通信后果，从而区分 beam-prediction accuracy 与实际系统收益。

## 3. 系统模型、算法接口与符号约定

### 3.1 多模态局部观测

对时刻 (t) 的 target BS (b)，多模态观测记为

\[
\mathcal{O}_{b,t}=\{\mathcal{I}_{b,t},\mathcal{I}_{\mathcal{N}_b,t},\mathcal{P}_{b,t}\},
\]

其中，\(\mathcal{I}_{b,t}\) 是 target BS 的多视角相机观测，\(\mathcal{I}_{\mathcal{N}_b,t}\) 是邻近 SN 的相机观测，\(\mathcal{P}_{b,t}\) 是 BS-local ISAC 点云。相机特征经地平面投影，点云特征经 BEV 编码；二者以及跨节点信息随后在同一 target-BS-centered BEV 平面融合。

BS-local ISAC 点云在 Chapter 3 中采用 monostatic radio-sensing abstraction 解释。BS 以已知 sensing symbol 和 sensing beam 发射探测信号，接收回波信道分解为 stationary roadside structures 形成的 static component 与 moving objects 形成的 dynamic component。dynamic component 进一步包含目标直接往返回波，以及目标参与、并附加一次环境镜面或漫反射的 secondary paths；其 delay、angle 和 Doppler 随目标运动变化。static component 可通过背景估计或 slow-time averaging 获取，并由常见 clutter suppression 去除。对剩余 target-related channel 进行 range--angle--Doppler processing，再以 CFAR 检测保留显著 resolution cells，最终将 range/angle 映射为 BS-local point cloud \(\mathcal P_{b,t}\)。该建模只阐明已有 ISAC 点云的物理来源，不将新 waveform、clutter-removal 或 CFAR 算法作为本文贡献。

设 \(\mathcal{J}_b=\{b\}\cup\mathcal{N}_b\)，相机特征先按节点组织并在 target-BS-centred BEV 中对齐。对 BEV cell \(\mathbf x\)，令 \(\mathbf f^{\mathrm{cam}}_{j\rightarrow b,t}(\mathbf x)\) 表示节点 \(j\) 的特征，\(m^{\mathrm{node}}_{j,t}(\mathbf x)\in\{0,1\}\) 表示该节点在该位置是否具有有效投影。正式方法将节点聚合表述为 **attention-based cross-node fusion**，其中 cross-node fusion 是模块功能，multi-head attention 是实现机制。以 target-BS feature 与有效节点均值共同构造 query，以各节点 feature 和相对几何编码构造 key/value。第 \(h\) 个 head 的权重可概括为

\[
e^{(h)}_{j,t}(\mathbf x)=
\frac{\mathbf q_h(\mathbf x)^{\mathsf T}\mathbf k_{j,h}(\mathbf x)}{\sqrt{d_h}}
b_h(\mathbf g_{j\rightarrow b}),\qquad
\alpha^{(h)}_{j,t}(\mathbf x)=
\frac{m^{\mathrm{node}}_{j,t}(\mathbf x)\exp(e^{(h)}_{j,t}(\mathbf x)/T_{\mathrm{node}})}
{\sum_{\ell\in\mathcal J_b}m^{\mathrm{node}}_{\ell,t}(\mathbf x)\exp(e^{(h)}_{\ell,t}(\mathbf x)/T_{\mathrm{node}})}.
\]

各 head 以 \(\sum_j\alpha^{(h)}_{j,t}\mathbf v_{j,h}\) 聚合不同节点，并通过 output projection、masked-mean residual 与 FFN refinement 得到 \(\mathbf F^{\mathrm{cam}}_{b,t}\)。该设计允许不同 BEV 位置依据目标 BS 上下文、节点相对位置和局部可见性选择互补视角，而不是对所有 SN 固定平均。

BS-local ISAC point cloud 被编码为 \(\mathbf F^{\mathrm{isac}}_{b,t}=\Phi_{\mathrm{pc}}(\mathcal P_{b,t})\)。正式方法进一步采用 **gated multimodal attention**。首先将 camera 与 ISAC features 投影到相同通道数，并构造

\[
\mathbf U_{b,t}=\left[
\widetilde{\mathbf F}^{\mathrm{cam}}_{b,t}\,\|\,
\widetilde{\mathbf F}^{\mathrm{isac}}_{b,t}\,\|\,
\left|\widetilde{\mathbf F}^{\mathrm{cam}}_{b,t}-
\widetilde{\mathbf F}^{\mathrm{isac}}_{b,t}\right|
\right].
\]

对模态 \(q\in\{\mathrm{cam},\mathrm{isac}\}\)，local gate 产生逐 cell logit \(\ell^{\mathrm{loc}}_{q,t}(\mathbf x)\)，global gate 从 \(\operatorname{GAP}(\mathbf U_{b,t})\) 产生 scene-level logit \(\ell^{\mathrm{glo}}_{q,t}\)。令 \(a_{q,t}\in\{0,1\}\) 为 modality availability mask，则

\[
\beta_{q,t}(\mathbf x)=
\frac{a_{q,t}\exp\!\left((\ell^{\mathrm{loc}}_{q,t}(\mathbf x)+\ell^{\mathrm{glo}}_{q,t})/T_{\mathrm{modal}}\right)}
{\sum_{q'}a_{q',t}\exp\!\left((\ell^{\mathrm{loc}}_{q',t}(\mathbf x)+\ell^{\mathrm{glo}}_{q',t})/T_{\mathrm{modal}}\right)},
\]

\[
\mathbf F^{(0)}_{b,t}(\mathbf x)=
\sum_q\beta_{q,t}(\mathbf x)\widetilde{\mathbf F}^{q}_{b,t}(\mathbf x),\qquad
\mathbf F_{b,t}=\sigma\!\left(\mathbf F^{(0)}_{b,t}+\Phi_{\mathrm{ref}}(\mathbf F^{(0)}_{b,t})\right).
\]

local attention 处理遮挡、点云稀疏性与空间位置相关的模态质量差异，global attention 响应整幅场景中的天气、照明和整体观测条件。天气标签不作为网络输入；权重通过 detection 与 beam-prediction objectives 端到端学习。\(m^{\mathrm{node}}\) 与 \(a_q\) 仅表示投影有效性或模态是否存在，不能解释为独立 reliability model。

联合网络输出两类空间量：车辆中心热图及尺度、朝向和速度等回归量；以及空间密集的 192 维 CSI beam-class logits。对与 detection 对齐的 BEV 位置采样并经 softmax 后，得到该感知目标的 beam-class posterior。训练和评估中可使用 link coordinate 进行监督采样，但该坐标和 UE identity 不作为网络前向输入。

若 \(\widehat{\mathbf r}_{i,t}\) 是检测中心、\(\widehat{\mathbf a}_{i,t}\) 是几何或运动属性、\(\widehat c_{i,t}\) 是检测置信度，则 target-level 输出写为

\[
d_{i,t}=(\widehat{\mathbf r}_{i,t},\widehat{\mathbf a}_{i,t},\widehat c_{i,t}),
\qquad
\mathbf p_{i,t}=\operatorname{softmax}\!\left(
\operatorname{Sample}(\mathbf P_{b,t},\widehat{\mathbf r}_{i,t})\right),
\]

其中 \(\mathbf P_{b,t}\) 是 dense 192-way beam-class logit map，\(\mathbf p_{i,t}\in[0,1]^{192}\) 是未绑定 physical target 的 CSI beam-class posterior。其 Top-\(K\) entries 作为后续候选测量和关联的 target-level score evidence，而非 UE-specific service-beam declaration 或物理功率分布估计。

### 3.2 Top-1 波束监督与候选集

对一个 BS--UE 链路的物理 CSI 功率向量 \(g\in\mathbb{R}_{+}^{192}\)，以 \(y^{\mathrm{beam}}\) 表示 strongest-beam class label，从而与 Chapter 3 中 CSI-RS 测量后确定的 service beam \(k^\star\) 区分。该标签定义为

\[
y^{\mathrm{beam}}=\arg\max_{k\in\{1,\ldots,192\}}g(k).
\]

网络在对应 BEV 位置输出 beam-class posterior \(p_\theta(k)\)，当前采用的 beam loss 为常见的 Top-1 cross-entropy：

\[
\mathcal{L}_{\mathrm{beam}}=-\log p_\theta(y^{\mathrm{beam}}).
\]

联合训练目标可概括为

\[
\mathcal{L}_{\mathrm{joint}}=
\lambda_{\mathrm{hm}}\mathcal{L}_{\mathrm{hm}}+
\lambda_{\mathrm{attr}}\mathcal{L}_{\mathrm{attr}}+
\lambda_{\mathrm{beam}}\mathcal{L}_{\mathrm{beam}},
\]

其中前两项分别监督 vehicle centre 与属性回归。Top-1 CE 是论文正式学习模型；Power-KL、KL+ranking 等历史对比仅作为内部开发归档，不进入论文方法或结果叙事。模型在推理时导出全部 192 个 beam-class scores，\(K_{\mathrm{scan}}\) 才表示已绑定 UE 实际发送 CSI-RS 测量的 beam 数，二者不能混同。

### 3.3 未绑定 detection 与多目标轨迹

感知输出描述当前 target BS 视角下的未绑定车辆观测，至少包含时间、BS、confidence、BEV 中心、尺寸、朝向、速度、坐标系以及按分数排序的 beam IDs/scores；其语义中不包含 `ue_id` 或 `track_id`。`diagnostic_gt_track_id` 只用于离线评估。

对每个 `(split, weather_id, bs_id)` 独立构造时序轨迹。CV Kalman filter、coordinated-turn (CT) EKF 和
IMM(CV+CT) 构成可比较的状态估计方案，并共享 innovation gating 与 Hungarian 一对一分配。CV 模型在
Cartesian 坐标中使用

\[
\mathbf{x}_t=[p_x,p_y,v_x,v_y]^{\mathsf T},\qquad
\mathbf{z}_t=[p_x,p_y]^{\mathsf T}.
\]

CT 模型使用 \([p_x,p_y,v,\psi,\omega]^{\mathsf T}\)，以速度、航向与转向角速度描述曲线运动；在
\(\omega\rightarrow0\) 时退化为直线运动。IMM 以 Markov model-transition probabilities 混合 CV 与 CT 的
初始 state/covariance，分别执行 KF/EKF prediction--update，再依据 measurement likelihood 更新 mode
probabilities 并融合状态。不同坐标的 state/covariance 在 mixing 与 fusion 时通过确定性 state transformation
及其 Jacobian 保持一致。

tracking 在本文中用于维持 beam hint 所属感知对象的时间连续性，而不是声称某一滤波器本身构成主要创新。匹配检测更新 track motion state、mode probability、confidence、observation history、beam-class posterior 和 hint age；未匹配轨迹可短时保留，但纯预测状态不生成正式 beam candidate。GT/noisy-GT 结果仅用于运动模型和数据关联的受控诊断，不能替代 predicted-detection 的端到端主结果。

### 3.4 测量辅助 UE--track binding

感知轨迹没有通信身份。在初始接入、切换到新 serving cell、已有 binding 失效或当前帧未观测时，系统执行 conventional SSB 与 CSI-RS refinement。令扫描为 communication UE \(u\) 选出的 CSI beam 为 \(b_u\)，当前 observed perception track \(i\) 的导出 beam-class posterior 为 \(p_i(k)\)，当前采用的 beam-posterior 关联代价为

\[
c(u,i)=\frac{-\log p_i(b_u)}{\log M_{\mathrm{CSI}}}.
\]

只有当 \(\varphi_b(b_u)\) 与当前 serving SSB 一致时，该 UE--track 配对才可行。系统在可行配对和未匹配虚拟列上执行 Hungarian assignment；高代价或低 margin 的配对被拒绝，并继续沿用 conventional scanning。该规则不使用 ground truth、不以预测位置反推码本的几何近似，也不以人工 UE ID 作为模型输入。

`beam_direction` 和 `beam_topk` 可作为 association ablation；正式叙事以 beam-posterior score、SSB-parent consistency、association cost threshold 与 assignment margin 为主。实验须分别报告 binding coverage、可诊断样本上的 accuracy 和 active accuracy，不能以单一百分比掩盖拒绝关联的比例。

### 3.5 关联接受门控、候选扫描与回退

已建立 binding \((weather_id,bs_id,ue_id)\mapsto track_id\) 后，系统保留 \(G_{u,t}\) 作为 candidate-use indicator，但不再为其引入独立的 reliability feature vector 或 threshold function。令 \(A_{u,r,t}\) 表示由 association cost threshold 与 assignment margin 决定的接受状态，则

\[
G_{u,t}=A_{u,r,t}\,\mathbf 1\!\left\{\pi_{b,t}(u)=r\in\mathcal R_{b,t}^{\mathrm{obs}}\right\}.
\]

accepted status 在两次 association event 之间随 binding 保持，并在 association 失效时置零。仅当已接受的 binding 对应当前 observed track 时使用感知候选；否则进行 conventional refinement。association confidence、detection/track confidence、hint age、observation count 和 beam-score mass 不再作为第二层 candidate-use gate 的输入。

若当前 observed detection 的前 \(K_{\max}\) 个 beam scores 为 \(s_1\geq\cdots\geq s_{K_{\max}}\)，自适应候选数可定义为

\[
k^*=\min\left\{k\in\{1,\ldots,K_{\max}\}\ \middle|\
\frac{\sum_{i=1}^{k}s_i}{\sum_{i=1}^{K_{\max}}s_i}\geq q\right\}.
\]

因此候选集宽度最小为 1，即仅测量 Top-1 预测波束。

该规则只决定 CSI-RS 测量集合大小；UE 在实测候选中按测得 SNR 选择 beam。正式 policy 仅使用当前 observed detection 的 beam Top-\(K\)，不将 KF/IMM 的纯预测位置映射为正式候选 beam；后者只保留为诊断性几何消融。

### 3.6 通信、CSI 获取与有效速率模型

在每个 beam-management cycle \(n\)，target BS 为
\(\mathcal U_b[n]\) 中的 VUE 进行下行传输。BS--VUE
信道采用随 RT reference channel 和 Doppler 演化的多径向量
\(\mathbf h_{b,u,n}=\sum_{\ell}\alpha_{b,u,\ell,n}e^{\mathrm j2\pi\nu_{b,u,\ell,n}t_n}
\mathbf a_b(\vartheta_{b,u,\ell,n})\) 表示。BS 采用一般线性 precoder 向 \(\mathcal U_b[n]\) 中的 VUE 发送多用户数据流；每个 VUE 的接收信号由目标流、其他 VUE 的 multi-user interference 与噪声组成，由此定义未扣除 beam-management overhead 的 downlink SINR 和 gross achievable rate。该部分不预设 beam selection 方法，也不提前引入 beam-conditioned effective channel。

为构造 precoder，BS 通过 CSI-RS codebook \(\mathcal F_b^{\mathrm{CSI}}=\{\mathbf f_{b,k}^{\mathrm{CSI}}\}_{k=1}^{192}\) 发送已知参考信号。VUE 在 beam \(k\) 下估计等效标量信道 \(h_{b,u,k,n}^{\mathrm{eq}}=\mathbf h_{b,u,n}^{\mathrm H}\mathbf f_{b,k}^{\mathrm{CSI}}\)，并由 reference-signal power、interference 与 noise 计算相应 CSI-RS quality/SINR。VUE 在实际测量的 candidate set 内选择 quality 最大的 beam，反馈 beam index、该 beam 下的 channel estimate 及相应 quality information；多用户预编码所需的 selected RF-beam coefficients 采用同一 beam-domain CSI 形式反馈。BS 汇总这些 beam-conditioned CSI 后构造 RF beam matrix 和 digital RZF precoder。本文不把完整 NR feedback payload 或逐 PRB/RE physical-resource mapping 作为研究对象，但所有对照必须共享同一 RT/Doppler、信道估计、RZF、功率和噪声配置。

SSB sweep 提供 coarse beam/serving-SSB evidence；CSI-RS 在实际 candidate set 上完成窄波束测量，实测
response 决定 service beam。已接受且当前可观测的 UE--track binding 才允许 beam-class posterior 缩减
CSI-RS candidate width；否则使用 conventional refinement。网络导出的 192-way posterior 不等于 192 次导频测量，实际测量开销仅由每个 event 的 \(K_e\) 决定。

资源预算采用

\[
\tau_{b,n}^{\mathrm{tot}}=\tau_{b,n}^{\mathrm{SSB}}+\tau_{b,n}^{\mathrm{CSI\text{-}RS}}
+\tau_{b,n}^{\mathrm{ctrl}}+\tau_{b,n}^{\mathrm{data}},
\]

上述资源项在正式系统模型中表示归一化的下行时频资源单元，而非逐 PRB/RE 的标准化 3GPP mapping；TDD 下行占比 \(\eta_{\mathrm{DL}}\) 独立建模。对 event set \(\mathcal E\)，dedicated-per-UE beam acquisition cost 写为

\[
\tau_{b,n}^{\mathrm{CSI\text{-}RS}}=
\sum_{e\in\mathcal E}
\left\lceil\frac{K_e}{M}\right\rceil\delta_{\mathrm{probe}},
\qquad
\eta_{b,n}^{\mathrm{data}}=
\frac{\tau_{b,n}^{\mathrm{data}}}{\tau_{b,n}^{\mathrm{tot}}},
\]

其中 \(K_e\) 是 event \(e\) 中所有 VUE 的实际候选 beam 总数，\(M\) 是可正交复用的 UE--beam measurement 数，\(\delta_{\mathrm{probe}}\) 是一次 acquisition 的归一化成本。令 \(\gamma_{b,u,n}^{\mathrm{RZF}}\) 表示真实 CSI-RS measurement、信道估计与 RZF 后的 SINR，则有效速率指标为

\[
R_{b,u,n}^{\mathrm{eff}}=
B_b\,\eta_b^{\mathrm{DL}}\,
\eta_{b,n}^{\mathrm{data}}
\log_2\!\left(1+\gamma_{b,u,n}^{\mathrm{RZF}}\right).
\]

当前 system-level data block 为 \(1\,\mathrm{ms}\)，其 measurement event、candidate decision 与资源预算与 \(0.125\,\mathrm{ms}\) physical reference 对齐；block 内保持 precoder，并以中点真实信道计算 post-RZF SINR。该具体时间配置属于 Chapter 5 的冻结实验协议，Chapter 3 仅使用归一化 overhead model，不逐项展开 slot/frame duration。该模型冻结的是 beam-management event 的 candidate/selected beam，而非整个 RT channel。以
\[
\overline R_b[N]=\frac{1}{N}\sum_{n=1}^{N}
\frac{1}{|\mathcal U_b[n]|}\sum_{u\in\mathcal U_b[n]}R_{b,u,n}^{\mathrm{eff}}
\]
定义 BS \(b\) 的 average effective user rate，并将其作为 Chapter 5 的系统级评价统计量。Chapter 3 不再把 sensing、association、candidate selection 与 precoding 强行写成一个联合优化问题；这些模块分别在 Chapter 4 给出算法，其共同通信后果通过 post-RZF SINR、CSI-RS overhead 与 \(R_{b,u,n}^{\mathrm{eff}}\) 体现。正式主表报告 average effective user rate、CSI-RS overhead、候选 beam 数、\(\eta_{b,n}^{\mathrm{data}}\) 与 sensing use/fallback；当前正式包不将 p05 rate 或 outage 作为主结果。

## 4. 算法整体框架

对每个 target BS、每个感知更新时刻，方法按以下顺序运行：

1. **观测对齐与 BEV 融合：** 收集 target BS 与邻近 SN 的多视角相机观测以及 BS-local ISAC 点云，依据 target-BS local calibration 映射至共享 BEV；采用节点聚合、跨节点注意力或模态门控等可比较融合机制形成联合特征。
2. **联合检测与 beam prediction：** 从共享 BEV 特征输出车辆 heatmap、几何/运动回归量和 dense 192-way CSI beam-class logits；在 detection 位置采样并经 softmax 得到未绑定 detection 及其 beam-class posterior。
3. **per-BS 多目标轨迹维护：** 采用 CV、CT 或 IMM 在相同 BS、天气和 split 的序列内预测轨迹；通过 gated Hungarian assignment 将当前 detections 与预测轨迹关联，更新 track state、confidence 和 hint age。
4. **初始/重关联 binding：** 在系统触发传统扫描时，将实测 CSI beam 与当前 observed tracks 的 beam-class posterior score 匹配；SSB-parent consistency 先筛除不可能配对，再以 Hungarian assignment 和拒绝门限建立或修复 UE--track binding。
5. **关联接受门控候选 CSI-RS：** 若 UE--track association 已通过 \(A_{u,r,t}\) 接受且对应 track 当前可观测，则从当前 observation 的 beam-class posterior 形成固定或自适应 \(K_{\mathrm{scan}}\) 候选；否则使用 conventional refinement。
6. **实测选择、RZF 与资源评价：** 在真正扫描的 CSI-RS candidates 内根据实测 SNR 选择 beam；在一致的 RT/Doppler、RZF、功率和归一化 \(\tau\) accounting 条件下计算 candidate recall、CSI-RS overhead、\(\eta_{b,n}^{\mathrm{data}}\)、sensing use/fallback 与 average effective user rate。

该算法的关键边界是：网络预测的对象始终是未绑定感知目标；通信身份只经由传统测量辅助的 binding 层进入；感知输出是缩小实测集合的 hint，而不是绕过测量直接确认下行最优 beam。

### 4.1 模块职责与信息接口

后续 Chapter 3--5 应以以下接口边界组织方法和实验，避免把诊断信息误写为正式决策输入。

| 模块 | 正式输入 | 正式输出 | 不得跨越的边界 |
| --- | --- | --- | --- |
| BEV 感知与联合预测 | target BS/SN 相机观测、BS-local ISAC 点云及标定信息 | 未绑定 detection、几何/运动属性、192-way beam-class posterior | 不输入 `ue_id`、link coordinate、ground-truth beam 或 oracle identity |
| 多目标 tracking | 同一 `(split, weather_id, bs_id)` 序列的未绑定 detections 与既有 track state | perception tracks、状态预测、track confidence 与 hint age | track 只维护感知对象身份；纯预测位置不产生正式 CSI-RS candidate |
| UE--track binding | 当前 observed tracks、传统 SSB/CSI-RS 测量、SSB-parent consistency | 已接受的 binding、margin/confidence 与拒绝/重关联状态 | ground truth 仅用于离线正确性统计，不能参与匹配代价或接受决策 |
| 关联接受门控与候选扫描 | association acceptance \(A_{u,r,t}\)、当前 observed track 及其 beam-class posterior | fixed/adaptive \(K_{\mathrm{scan}}\) candidates 或 conventional fallback | 不引入第二层 reliability features；prediction 只缩小实测集合，最终服务 beam 仍由实际 CSI-RS/SNR 测量决定 |
| PHY 与资源评价 | 实测候选、统一的 RT/Doppler、RZF、功率和归一化 \(\tau\) profile | candidate recall、CSI-RS overhead、sensing use/fallback 与 average effective user rate | 不从通信结果反向修改 test 阈值或把 oracle ceiling 作为正式方案 |

## 5. 实验设计与证据链

### 5.1 分层评价问题

| 层级 | 要回答的问题 | 主指标 | 不能单独推出的结论 |
| --- | --- | --- | --- |
| Detection | 是否发现可用车辆目标 | AP@2m、Recall@2m | 不能证明通信速率提升 |
| Beam prediction | Top-1 classifier 的候选排序是否保留有用 beam | matched Beam Top-1@2m、Top-4@2m、Top-4 power ratio | 不能证明 UE 已被正确绑定 |
| Cross-node sensing | 邻近节点是否补足局部场景观测 | 上述指标随 nearby-node count 的变化 | 不能将节点数增益直接等同于用户速率增益 |
| Tracking | 不同运动模型如何影响轨迹维护与端到端 policy | 定性轨迹、mean candidate beams、sensing use/fallback、handover count | 不能仅由受控轨迹图证明端到端身份优势 |
| Candidate selection and system | 更少 beam 的候选测量是否在资源代价下仍有收益 | mean effective user rate、CSI-RS overhead、SSB overhead、data fraction、sensing use、fallback | 不能反推任一感知模块在所有条件下最优 |

最终论文结果包以 detection-conditioned beam metrics、CSI-RS overhead、hint use/fallback 和用户平均有效速率构成证据链。当前包未单独导出 accepted binding accuracy 或 p05/outage 主表；因此正文不得以这些未导出指标形成定量结论。

### 5.2 公平比较与冻结规则

- `train` 仅用于训练，`val` 用于 checkpoint、tracking 参数和候选策略选择。正式结果包中的雨雾 gate 采用固定的 `min_association_margin=0.10` 操作点；该点由 test 调节，因此论文中只能表述为固定操作点结果，不能表述为独立 held-out 泛化性能。
- 每种天气分别统计；总体比例由原始分子/分母汇总，不对天气百分比简单平均。
- 除上述已记录的固定雨雾操作点外，不得使用 test rate、test binding accuracy 或 test candidate recall 调节阈值；任何后续 test-tuned 参数同样不能作为严格 held-out 主结论。
- 条件指标必须写出条件并同时报告 coverage，例如 `beam Recall@4 | matched detection within 2 m`。
- GT-ID、GT detection 和 oracle hint 仅作为 ceiling 或诊断；正式路径必须以 predicted detection、communication measurement 和非 GT association-acceptance result 为输入。

### 5.3 对照组

- Learning：Camera-only、ISAC-only、Local camera--ISAC fusion、Distributed mean fusion 和 Distributed multimodal attention (proposed)。
- Nearby-node study：Distributed fusion with learned gating、Distributed multimodal attention (proposed) 和 Distributed mean fusion，nearby-node count 从 0 至 5。Distributed multimodal attention 是正式主感知方案；Distributed fusion with learned gating 是对不同 SN 特征学习融合 gate 的对照方案。
- Beam learning：固定 Top-1 CE；Power-KL、KL-only 和 KL+ranking 仅保留为内部开发归档，不作为论文图表或结果。
- System：SSB-guided CSI-RS refinement 的 \(K_{\mathrm{ref}}=4\) 和 \(K_{\mathrm{ref}}=12\) 两个参数点，以及完整 DMSA-BM 方案；三者共享冻结的 resource profile。两个 refinement 设置属于同一 hierarchical beam-search baseline，不表述为两种独立算法；该 baseline 的 coarse-to-fine search 依据 Xiao et al. 的 hierarchical codebook 工作进行学术定位。
- Tracking：IMM、KF-CV 与 KF-CT；定性轨迹图采用 test / clear-day / BS-NE 的 GT+1.0 m 位置噪声输入，仅用于受控运动诊断；宏平均表使用相同的 Top-1 CE detector 与系统级 protocol。

主结果采用一套冻结 radio profile：48 SSB、100 ms SSB period、20 ms CSI-RS period、4-BS 场景，以及一致的 RT segment、功率、噪声、RZF 与归一化 \(\tau\) 资源抽象。SSB-guided CSI-RS refinement 以 \(K_{\mathrm{ref}}\in\{4,12\}\) 表示两个候选宽度；正式正文不将十二波束设置误写为全部位于单一 SSB parent 内。CSI-RS period、\(K_{\mathrm{ref}}\)、\(K_{\mathrm{scan}}\)、\(\delta_{\mathrm{probe}}\)/measurement multiplexing、单/多 BS 和 Doppler 可作为敏感性轴，而不应与全部上游模型形成全笛卡尔积。

### 5.4 正式结果包与论文呈现顺序

- 唯一正式定量来源为 paper_results/README.md 及其 figures、tables 子目录。论文 Chapter 5 按“数据与设置—评价方法—感知性能—通信性能—跟踪性能—讨论与边界”呈现，不将历史开发结果混入主表。
- 学习结果使用 table_01--table_03 与 fig_01--fig_03：总体与天气分层表首先说明不同融合方案在 AP、Recall、Top-1 和 Top-4 指标上不存在统一最优；随后用 fixed-model missing-node curves 表达 nearby-node availability 的影响，而非为每个节点数分别训练模型。
- 系统结果使用两张互补表格。table_04 在同一张表中按天气比较 DMSA-BM 与两个 SSB-guided refinement operating points，并在表末增加三天气等权宏平均；该表只保留 average effective user rate 与 CSI-RS overhead，避免与后续模态表重复。table_05 使用 Camera-only、ISAC-only、Local camera--ISAC fusion 与完整 DMSA-BM 的端到端结果，报告三天气等权平均的 effective user rate、CSI-RS overhead 与 sensing use，从通信层说明感知来源与分布式协作的作用。原 fig_04 与 fig_05 不再进入论文结果包。data fraction 是冻结资源 profile 的公共项，不作为 policy 独立优化的结果。
- 跟踪结果以 table_06 的 predicted-detection 系统指标呈现，必须避免以单一 rate 数值声称 IMM 普遍优于 KF-CV/KF-CT。fig_06 作为 GT 加 1.0 m 噪声下的受控轨迹诊断保留在正式结果包中，但不纳入当前 Chapter 5 的展示。

## 6. 当前进展与证据等级

### 6.1 已具备的研究与实验框架

- 已建立 manifest 驱动的 target-BS-centered 数据读取、相机/ISAC BEV 表达、基于 Top-1 CE 的联合 detection--beam prediction 及不同模态和节点融合的实验框架。
- 已建立未绑定 perception prediction、per-BS track state、传统测量辅助关联、current-detection beam Top-\(K\) candidate scanning、SSB-parent check、association-decision log、自适应 \(K\)、conventional fallback、RT/Doppler/RZF/归一化 \(\tau\) accounting 的端到端流程。
- 已具备 camera、ISAC、multimodal 与多节点融合；CV、CT、IMM；conventional、direction/top-\(K\)/association-gated 等可比较协议。论文正式 system-level sensing 行固定使用 `v3_rt_anchor_beam_top1_ce_cross_agent` 与 IMM。
- 正式模块接口遵守“learning output -> unbound detection；tracking -> perception track；beam management -> track state + communication measurement”的边界，避免直接传递训练网络内部状态。

### 6.2 已有定量证据

| 层级 | 已保存证据 | 可谨慎使用的表述 | 证据等级 |
| --- | --- | --- | --- |
| Top-1 CE multimodal learning | 正式结果包的 Distributed multimodal attention test：AP@2m 为 78.73\%，Recall@2m 为 81.51\%，Beam Top-1@2m 为 71.13\%，Beam Top-4@2m 为 94.13\%，Top-4 power ratio 为 97.01\% | 固定 Top-1 CE 检测器能够同时提供车辆检测和候选 beam 排序；Top-4 的候选价值需与 detection availability 一并解释 | 冻结正式结果包，`table_01_learning_modalities_overall` |
| 分天气 learning | Clear、Rain/Fog、Night 三种天气下，多模态 variants 的 AP@2m 均高于单模态 camera/ISAC；Distributed multimodal attention 在 Clear 下达到 81.92\% AP@2m 与 75.00\% Beam Top-1@2m | 模态与跨节点互补性随天气和指标而变化，不宜用单一总体指标宣称所有融合策略均最优 | 冻结正式结果包，table 02 |
| 跨节点互补 | Distributed multimodal attention 的节点数 test 中，AP@2m 从 0 节点的 38.59\% 升至 5 个邻近节点的 80.41\%；Beam Top-4@2m 从 91.58\% 升至 95.40\% | 更多邻近视角在该冻结协议下改善检测，并保持较高的 Top-4 候选覆盖 | 冻结正式结果包，`table_03_node_count_overall` |
| 核心系统比较 | 三天气等权宏平均下，DMSA-BM 的 mean effective user rate 为 146.332 Mbps，CSI-RS overhead 为 1.56\%，sensing use 为 54.35\%，fallback 为 45.65\%；SSB-guided refinement \((K_{\mathrm{ref}}=4)\) 的相应 rate/overhead 为 142.248 Mbps/1.90\% | 在该固定操作点和资源模型下，感知辅助以部分 fallback 换取较低 CSI-RS 开销与更高的用户平均有效速率 | 冻结正式结果包，`table_04_core_by_weather` 的 Macro average 行 |
| 感知方案端到端比较 | 三天气等权平均下，DMSA-BM、Local camera--ISAC fusion、ISAC-only 与 Camera-only 的 mean effective user rate 分别为 146.332、143.701、142.522 与 138.868 Mbps；相应 CSI-RS overhead 为 1.56\%、1.80\%、1.81\% 与 1.86\%，sensing use 为 54.35\%、58.28\%、49.03\% 与 47.93\% | 完整分布式多模态方案同时取得更高 average effective user rate 和更低 CSI-RS overhead；Local camera--ISAC 是三个简化输入方案中最接近完整方案的配置。sensing use 的高低不能单独推出速率收益 | `table_05_sensing_configuration_communication`；简化方案来自保存的 modality-ablation runs，DMSA-BM 采用正式 selected operating point |
| 条件化 system operation | DMSA-BM 的 sensing use 从 Clear 的 76.35\% 降至 Rain/Fog 的 56.65\% 和 Night 的 30.07\%，对应 fallback 为 23.65\%、43.35\% 和 69.93\% | association-acceptance rule 与 current-observation requirement 共同决定 sensing use 或 SSB-guided refinement fallback | 冻结正式结果包，table 04 |
| Tracker 宏平均比较 | Top-1 CE detector 下，IMM、KF-CV 和 KF-CT 的 mean effective user rate 分别为 146.332、146.373 和 145.880 Mbps | 三种 tracker 的端到端差异需要与 hint usage、fallback 和候选数共同解释；该表不支持将 IMM 表述为普遍最优 | 冻结正式结果包，`table_06_tracker_macro_average` |

### 6.3 当前必须保持的证据边界

- Chapter 4 的正式方法已改为 attention-based cross-node fusion 与 gated multimodal attention。当前保存的定量表格沿用此前结果包，在用户完成相应结果更新前，不得把其中数值直接归因于新的 gated multimodal attention 配置；Chapter 5 现有数值暂按用户要求保持不变。
- Power-KL、KL-only 和 KL+ranking 为内部开发归档，不进入论文图表、方法比较或性能主张；正式叙事固定为 Top-1 CE beam classifier。
- 不得将正式 Top-1 CE detector 的结果与历史 Power-KL、KL-only 或 KL+ranking 的开发结果混合；后者不进入论文图表、方法比较或性能主张。
- 不得将采用 `min_association_margin=0.10` 的雨雾 gate 表述为独立 held-out 泛化结论；它是正式结果包记录的固定 test-tuned 操作点。
- 不得宣称 IMM 在 predicted-detection 端到端路径上普遍优于 CV/CT；正式宏平均表中 KF-CV 的 user rate 略高于 IMM，比较应同时报告 hint usage、fallback、候选数和 handover。
- 正式系统结论须采用 `paper_results` 的 average effective user rate；历史 20 ms raw-RE profile 或短段结果不可混入主表。
- 当前正式结果包未单独导出 accepted binding accuracy、p05 rate 或 outage 主表。正文可将 sensing use/fallback 作为 association-to-policy 的 operational evidence，但不得据此虚构独立 association accuracy 或 lower-tail/outage 结论。

## 7. 内部待确认事项与后续实验

以下事项留在本文档中推进，不应以未完成口吻进入正式正文。

1. 更新并维护采用 gated multimodal attention 的 Top-1 CE final model checkpoint、输入输出、seed、原始分子/分母及其与正式结果包的追溯关系；不再将历史 Power-KL 或 ranking supervision 纳入论文模型比较。
2. 在相同 Top-1 CE predicted-detection outputs 上进一步诊断 CV/CT/IMM 的差异，并补充 association accuracy、track continuity 和按条件分层的错误统计；重点解释宏平均 user rate、hint/fallback 与候选数之间的关系。
3. 将 beam-posterior association、association cost threshold、assignment margin 和 adaptive \(K\) 的选择过程完整记录为可追溯操作点；对 test-tuned 参数保持审慎表述。
4. 在相同 RT manifest、归一化 \(\tau\) profile 和 PHY 参数下补充 oracle ceiling 或两阶段 fallback 的诊断，但不替代正式 DMSA-BM 主结果。
5. 研究 conservative candidate union、基于实际 pilot-SNR 的两阶段 fallback 或更稳健的初始/重关联，重点改善 night 与 rain/fog 条件下的 fallback 依赖。
6. 维护 final checkpoint、raw snapshot、原始统计、汇总指标、可视化和轻量 run manifest 的可追溯关系。

## 8. 术语与符号

| 概念 | 推荐术语或符号 | 说明 |
| --- | --- | --- |
| 完整主方案 | Distributed Multimodal Sensing-Assisted Beam Management (DMSA-BM) | 包含分布式多模态感知、IMM tracking、measurement-assisted target-to-user association 与 association-gated CSI-RS candidate selection |
| 主感知方案 | Distributed multimodal attention (proposed) | 采用 attention-based cross-node fusion 的正式感知网络 |
| 学习门控对照 | Distributed fusion with learned gating | 对不同 SN 特征学习融合 gate 的对照方案，不是正式主感知方案 |
| 通信基线 | SSB-guided CSI-RS refinement | coarse SSB measurement 后进行 CSI-RS refinement，以 \(K_{\mathrm{ref}}\) 表示候选宽度 |
| 多模态感知 | multimodal sensing | camera modality、ISAC modality 与跨节点观测共同构成 |
| 目标基站 | target base station (target BS) | 当前构造局部 BEV、输出 detection 并服务 UE 的 BS |
| 分布式感知节点 | sensing node (SN) | 向 target BS 提供邻近视觉观测，不独立提供通信服务 |
| 局部鸟瞰表征 | target-BS-centered BEV representation | 对齐多站点、多模态观测的局部空间表征 |
| 感知检测/轨迹 | perception detection / track | 不带 communication UE identity 的目标观测或轨迹 |
| UE--轨迹绑定 | UE--track binding | 通信测量与感知证据建立的身份映射 |
| CSI 波束预测后验 | CSI beam-class posterior | Top-1 CE classifier 对 192 个 CSI codebook beams 导出的 softmax scores；不解释为物理功率分布 |
| 波束后验关联 | beam-posterior association | 用预测 posterior 与扫描所得 CSI beam 的负对数似然完成 binding |
| \(K_{\mathrm{scan}}\) | CSI-RS scan budget | 已绑定 UE 实际进行 CSI-RS 测量的 beam 数 |
| 关联接受门控 | association-acceptance gate | 由 \(A_{u,r,t}\) 与 current-observation requirement 直接决定是否使用 sensing hint，不包含第二层 reliability features |
| 常规回退 | conventional fallback/refinement | association 未接受或对应 track 当前不可观测时沿用传统扫描 |
| 有效速率 | effective rate | 同时扣除 SSB、CSI-RS 与控制资源后的速率指标 |
| RZF | regularized zero-forcing (RZF) | 系统评价中的下行多用户预编码抽象 |
