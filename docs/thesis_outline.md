# 论文大纲

最后更新：2026-07-12

论文暂定题目：Multimodal Sensing-Assisted User Association and Tracking in Vehicular Networks

本文档是论文写作蓝图，由 `docs/work_brief.md` 推导和更新。大纲只记录当前采用的
论文结构、方法方案和叙述逻辑；方法不确定性、实验空缺和内部待办事项应维护在
`docs/work_brief.md` 中。后续撰写 `chapters/*.tex` 时，应把正文写成可供审稿的
正式英文论文文本，不在正文中保留 TODO、未完成口吻或代码库说明。

## Chapter 1: Introduction

本章目的：从高频 V2I 波束对齐的测量负担出发，建立本文的两个核心动机。其一，多模态、
跨感知节点观测如何通过互补视角和几何信息，在遮挡、视场受限、天气和交通状态变化等条件下
提供更大范围且更可靠的环境表征；其二，感知到的车辆目标如何与通信 UE 建立并维持可验证的
对应关系，从而使 beam hint 真正服务于正确用户的 beam alignment。读者在本章结束时应理解，
本文研究的不是孤立的 beam classification，而是面向身份一致 beam alignment 的感知辅助候选
CSI-RS 测量机制。

叙述逻辑：先说明高频 V2I 的窄波束收益与 SSB/CSI-RS 测量开销之间的矛盾；继而从技术和
系统两个层面提出挑战：多模态/跨节点感知的空间互补性必须转化为可靠的 target-BS local
BEV 表征，而 sensing target 与 communication UE 的身份差异必须经由通信测量辅助的 association
显式处理。随后给出以 target BS 为中心的研究目标、范围和三项贡献，并用章节安排说明每一项
主张将如何由后续方法和实验支撑。

### 1.1 Background

写作要点：

- 从 connected mobility、V2I 和高频宽带通信的需求切入；窄波束带来阵列增益，也使链路依赖
  及时的 beam alignment、CSI acquisition 和 beam refinement。
- 说明车辆相对 BS 的几何、遮挡、散射路径和可见性会快速变化；天气、光照和道路交通同时
  改变通信状态与感知观测。强调“测量结果会老化”与“频繁扫描消耗资源”这两个并存事实。
- 用 SSB 完成初始接入、以 CSI-RS 执行细化/校准的抽象解释传统流程；说明缩小候选集可节省
  测量资源，但候选遗漏会传递为 CSI 失配、较低有效速率或更高 outage 风险。
- 引入道路侧相机、ISAC 与邻近 SN 的环境感知潜力：视觉信息刻画语义与可见性，ISAC 提供
  几何/无线感知线索，邻近节点扩展服务 BS 的可观察范围。此处只建立动机，不在引言展开
  具体融合结构。
- 文献定位可简述 camera-aided、radar-aided、LiDAR-aided 和 ISAC predictive beamforming；具体
  分类、代表方法和比较留给 Chapter 2。

### 1.2 Challenges

写作要点：

- **挑战一：多模态与跨节点感知的条件互补性。** 单一传感器或单一站点会受到视场、遮挡、
  光照、天气、点云稀疏度与空间覆盖范围限制。需要在 target-BS-centered BEV 中对齐 target BS
  相机、SN 相机和 BS-local ISAC 点云，使不同模态与节点的互补性能够服务于大范围车辆检测、
  定位和条件 beam-quality ranking，而非仅堆叠更多输入。
- **挑战二：sensing target-to-user association。** 感知系统输出的是道路中的物理目标，通信系统
  操作的是参与 SSB、CSI-RS 和下行传输的 UE。在多车场景中，正确的 detection 或 beam ranking
  若被分配给错误 UE，仍会造成错误 beam alignment。因此，target-to-user correspondence 是从
  环境感知走向实际通信收益的必要条件，也是相较于默认 UE 身份已知的 beam alignment 工作的
  关键区别。
- **挑战三：target-to-user correspondence 的时序保持。** 初始 association 之后，车辆运动、
  临时遮挡、漏检和近邻目标交汇会破坏 correspondence。应以多目标状态估计、gated data association
  和 measurement-assisted re-association 维持感知轨迹与 UE 之间的身份一致性；此机制的学术作用是
  保证 beam hint 的用户归属正确，而非把 tracking 本身表述为独立的通信身份识别器。
- **挑战四：感知提示的保守使用与系统收益。** 感知不应无条件取代通信测量。系统须根据
  association reliability、当前观测质量和 beam-distribution confidence 决定使用小候选集还是
  conventional fallback，并以 candidate recall、CSI-RS overhead、effective rate、p05 rate 和 outage
  共同评价实际 beam-alignment trade-off。
- 建议配置 Figure~1.1：以 target BS 为中心展示多模态/跨节点观测、未绑定 sensing target、
  target-to-user association、时序 correspondence maintenance、可靠度门控候选扫描与 conventional
  fallback；图中清楚区分 physical target identity、perception-track identity 与 communication UE identity。

### 1.3 Research Objective

写作要点：

- 明确总体目标：构建一个以 target BS 为局部协调点的 multimodal sensing-assisted beam-alignment
  framework，使分布式环境感知、目标到用户关联与系统级通信评价形成连续闭环；感知用于辅助
  beam management，而不绕过实际通信测量。
- 目标一对应 **Distributed Multimodal BEV Perception for Joint Vehicle Detection and Beam Prediction**：
  在统一局部 BEV 表征中融合 target-BS/SN 相机与 BS-local ISAC 点云，联合完成车辆检测和 per-target
  beam prediction，研究跨模态、跨节点观测为何能在可见性、遮挡和天气变化下提供互补信息。
- 目标二对应 **Target-to-User Association with IMM-Based Tracking**：解决 physical sensing target 与
  communication UE 并非天然对应的问题；以通信测量证据建立目标到用户关联，以 IMM-based tracking
  维持该关联的时序有效性，从而使 beam hint 服务于正确 UE。
- 目标三对应 **Multimodal V2I Simulator and 5G NR-Oriented Beam-Management Evaluation Framework**：
  基于既有多模态数据资产，在统一的 5G NR-oriented beam-management abstraction 下评价感知辅助方案
  对测量开销、链路可靠性和通信性能权衡的影响，而不以单帧 Top-\(K\) accuracy 代替系统层结论。
- 说明范围：研究聚焦每个 target BS 内的局部感知、target-to-user association 与 IMM-based tracking，
  不主张跨 BS global identity；ground truth 仅用于诊断或上界，正式决策依赖感知与通信侧可用信息。

### 1.4 Contributions

写作要点：

- 贡献 1：**Distributed Multimodal BEV Perception for Joint Vehicle Detection and Beam Prediction。**
  在 target-BS-centered BEV 中融合服务 BS、邻近 SN 的相机观测和 BS-local ISAC 点云，联合输出
  vehicle detections 与 192-way CSI beam-quality distribution；distribution/ranking learning 同时支持
  candidate ranking、置信度刻画和 association likelihood。
- 贡献 2：**Target-to-User Association with IMM-Based Tracking。** 以传统通信测量建立或恢复 sensing
  target 与 communication UE 的关联，以 IMM-based multi-object tracking 维持该关联的时序有效性；
  SSB-parent consistency、reliability gate 与 conventional fallback 使 beam hint 只用于可信用户对应关系。
- 贡献 3：**Multimodal V2I Simulator and 5G NR-Oriented Beam-Management Evaluation Framework。**
  基于既有多模态数据资产建立系统级 V2I simulator，在一致的 SSB/CSI-RS、码本、RZF、Doppler 和
  RE accounting 条件下，评价 candidate recall、pilot overhead、effective rate、p05 rate 与 outage。
- 贡献措辞保持为“提出/构建/建立”；不在 Introduction 写入未经冻结 test 支撑的定量收益或优越性。

### 1.5 Thesis Organization

写作要点：

- 简要说明 Chapter 2--6 的叙事分工，保持与实际章节文件和后续大纲同步。
- Chapter 2 从 sensing-aided beam prediction、ISAC predictive beamforming、BEV/cooperative perception
  与 sensing target-to-user association 四条线梳理相关工作，突出已有方法对 identity-consistent
  beam alignment 与资源感知系统评价的覆盖不足。
- Chapter 3 定义 target-BS local coordinate、观测、48/192 codebook、physical target/perception track/
  communication UE 三类身份、target-to-user correspondence、candidate set 和 resource accounting。
- Chapter 4 介绍分布式多模态 BEV perception、joint vehicle detection and beam prediction、IMM-based
  tracking、target-to-user association、reliability-gated candidate selection 与通信接口。
- Chapter 5 描述 Multimodal V2I Simulator、5G NR-oriented beam-management evaluation、条件分层对照
  和 association/tracking 指标；所有比较在一致的 measurement/resource profile 下进行。
- Chapter 6 总结由冻结证据支持的发现，说明局部 BS 范围、RT segment/PHY abstraction 与感知
  可靠性等限制，并讨论跨 BS correspondence、真实测量校准和更严格协议级评估等扩展。

## Chapter 2: Background and Related Work

本章目的：梳理 sensing-assisted beam prediction、ISAC predictive beamforming、BEV / cooperative
perception，以及 sensing target-to-user association 相关研究，明确多模态/跨节点互补性与
identity-consistent beam alignment 的研究缺口。

叙述逻辑：先介绍车联网和 beam management 基础，再按 sensing modalities 与方法类型梳理已有工作，
随后引入 BEV 多模态融合和分布式感知，最后收束到本文的研究定位：以跨节点 BEV 感知扩大条件化
观测能力，以 sensing target-to-user association 保证 beam hint 的正确 UE 归属，并以资源感知的
系统评价检验实际 beam alignment 影响。

### 2.1 Vehicular Networks and Beam Management

写作要点：

- 回顾 V2I / vehicular networks 中高频通信的 beam alignment、beam selection、beam tracking
  和 handover 问题。
- 介绍 beam codebook、SSB beam sweeping、CSI/PMI acquisition 和 beam training overhead。
- 说明 beam management 与 spectral efficiency / throughput 的关系。

### 2.2 Sensing-Aided Beam Prediction

写作要点：

- 按 sensing modality 组织已有工作：camera-based、position/GPS-aided、radar-aided、
  LiDAR-aided 和 multimodal sensing-aided beam prediction。
- 介绍 DeepSense 6G 系列工作、Top-K beam accuracy、beam power loss 和 overhead reduction
  等常用指标。
- 说明现有工作多关注 beam index prediction，而 sensing target 与 communication user identity
  的长期维护仍需要与 tracking 和 association 结合。

### 2.3 ISAC Predictive Beamforming and Tracking

写作要点：

- 回顾 DFRC/ISAC 中利用 radar echo、historical channel 或 reflected signal samples 做车辆状态预测
  和 predictive beamforming 的工作。
- 介绍 EKF、Bayesian/message passing、CLSTM、Transformer 或 end-to-end predictive beamforming。
- 说明 ISAC 文献通常重视 channel/beamforming/rate 优化，本文进一步结合 camera-based multi-object
  perception 和 target-user association。

### 2.4 BEV Multimodal Fusion and Cooperative Perception

写作要点：

- 介绍 CenterNet / CenterTrack 对 point-based detection 和 tracking 的启发。
- 介绍 Lift-Splat-Shoot、BEVFusion 等 BEV 表征方法，说明 BEV 对多视角图像和点云融合的意义。
- 介绍 V2X cooperative perception，说明多节点协作感知对覆盖范围、遮挡和视角互补的帮助。
- 连接到本文 BS/SN 多视角 camera 与 BS-side ISAC point cloud 的 BEV 融合设计。

### 2.5 Sensing Target-to-User Association and Identity-Consistent Beam Alignment

写作要点：

- 区分 physical sensing target、perception-track identity 和 communication UE identity；明确后两者的
  correspondence 不是由 detection 类别、位置标签或 ground truth 自动给定。
- 回顾 multi-candidate beam prediction、transmitter identification、multi-object data association 与
  state-estimation-based tracking 的相关思想，说明它们各自处理的身份边界。
- 将 sensing target-to-user association 定位为 identity-consistent beam alignment 的必要机制：只有
  beam hint 与正确 UE 对应，候选测量的节省才可能转化为该 UE 的通信收益。
- 说明本文采用 conventional-measurement-assisted initial/re-association、beam likelihood、
  SSB-parent consistency 和一对一 assignment；多目标状态估计只维持 correspondence 的时序一致性。

### 2.6 Summary of Research Gap

写作要点：

- 总结已有工作分别覆盖 sensing-aided beam prediction、ISAC predictive beamforming、BEV fusion、
  cooperative perception 和 multi-candidate identification。
- 从两条主线收束研究缺口：跨模态/跨节点观测如何在变化条件下形成可用的局部 BEV 表征；以及如何
  在不注入 oracle identity 的前提下建立 sensing target-to-user correspondence，使 beam ranking
  成为正确 UE 的候选测量提示。
- 指出仅报告 Top-\(K\) accuracy 的不足，并引出从 target-to-user association 到候选扫描、资源记账
  和 RZF effective-rate 的系统级证据链。gap 与 Chapter 1 的三项贡献对齐。

## Chapter 3: System Model and Problem Formulation

本章目的：定义道路侧车联网场景、target BS/SN/physical target/communication UE 实体、
target-BS-centered multimodal observations、sensing target-to-user correspondence、candidate
measurement 与资源记账模型，为 identity-consistent beam alignment 提供统一符号和边界。

叙述逻辑：先定义局部网络、时间尺度和坐标系，再定义多模态感知观测与未绑定 detection，随后
形式化三类身份及其 correspondence，最后定义 48/192 codebook、candidate measurement、reliability
decision 和资源模型，并形成多层输出而非单一闭式优化的 problem formulation。

### 3.1 Network Scenario and Time Structure

写作要点：

- 定义道路场景、BS、distributed sensing nodes、vehicles/users。
- 每个 target BS 以自身为中心选择周围 K 个 SN 形成局部协作感知区域。
- 定义 target-BS 和 SN 的相机观测、BS-local ISAC point cloud sensing，以及 target-BS-centered
  BEV local coordinate；不将该局部坐标解释为全局融合坐标。
- 定义 frame / time slot / decision epoch，并用符号化参数表示场景数量、K 和时间尺度。

### 3.2 Multimodal Sensing Observation Model

写作要点：

- 定义 camera modality：BS camera views 和 K 个 SN 的 camera views。
- 定义 ISAC modality：BS-side ISAC-like point cloud。
- 说明标定、同步和坐标系转换，尤其是如何进入 BEV coordinate frame。
- 定义 detected target 的 BEV 表示，如中心点、位置、尺寸和置信度。

### 3.3 Sensing Target-to-User Association and Correspondence State

写作要点：

- 区分 physical target、perception-track 和 communication UE 三类身份；定义 UE--track correspondence
  变量、binding coverage、accepted/rejected association 和 re-association event。
- 定义 perception-track 的状态、置信度、age 与运动模式；采用 CV、CT 或 IMM 等状态估计器，并用
  gated one-to-one data association 保持感知对象的时间连续性。
- 形式化 measurement-assisted association：初始接入、serving-cell 变化、binding 失效或当前未观测
  时执行 conventional measurement；由 beam likelihood、SSB-parent consistency 和拒绝规则产生
  UE--track correspondence。
- 强调 ground-truth identity 仅用于诊断/上界，不能进入正式 association decision；tracking 的作用是
  保持 correspondence，不是从感知特征直接识别 UE。

### 3.4 Codebook, Candidate Measurement, and Communication Resource Model

写作要点：

- 定义 48 SSB beams、192 CSI beams、SSB-parent relation、CSI power/quality distribution 和实际 CSI-RS
  candidate set；严格区分 \(K_{\mathrm{model}}\)、\(K_{\mathrm{bind}}\) 与 \(K_{\mathrm{scan}}\)。
- 定义 initial/re-association 的 conventional SSB/CSI-RS measurement，以及可靠 correspondence 下由
  当前 observed target 导出的 fixed/adaptive candidate measurement。
- 定义 reliability evidence、conventional fallback 与 candidate recall；明确感知只缩小实测集合，
  而最终服务 beam 由 CSI-RS/SNR 测量选择。
- 定义统一的 SSB、CSI-RS、control 和 data resource accounting，以及 RZF 下的 raw/effective rate、
  p05 rate 和 outage；说明该模型是系统级 abstraction，不等同完整 5G NR protocol stack。

### 3.5 Problem Formulation

写作要点：

- 用自然语言和必要符号总结本文问题：给定 target-BS-centered multimodal observations 和周期性
  communication measurements，输出未绑定 detection、beam-quality distribution、perception tracks、
  sensing target-to-user correspondence 和可靠度门控 CSI-RS candidates。
- 采用多目标表述：提高条件 beam-ranking quality、target-to-user association accuracy 与
  correspondence persistence，在保持 candidate recall、p05 rate 和 outage 可接受的前提下降低 CSI-RS
  resource overhead。
- 避免把系统写成单一闭式优化问题；重点呈现 identity-consistent beam-alignment workflow 及其分层评价。

## Chapter 4: Proposed Multimodal Sensing-Assisted Beam Management Framework

本章目的：介绍本文提出的 BS-centric multimodal and cross-node sensing-assisted beam-alignment
框架，包括局部 BEV 融合、联合 detection--beam-quality learning、未绑定多目标状态估计、
measurement-assisted sensing target-to-user association、可靠度门控候选测量和通信评估接口。

叙述逻辑：先给出感知身份与通信身份分离的整体数据流，再说明跨节点观测如何形成 BEV features、
如何输出未绑定 detections 和 CSI quality distributions；随后说明 conventional measurement 如何建立
target-to-user correspondence、状态估计如何保持其时序一致性，以及可靠度如何决定 candidate
measurement 或 fallback，最后总结算法与复杂度。

### 4.1 Framework Overview

写作要点：

- 给出整体模块：multimodal/cross-node input construction、BEV fusion、joint detection--beam-quality
  learning、unbound perception tracking、measurement-assisted target-to-user association、reliability-gated
  candidate measurement 与 communication evaluation。
- 说明以 BS 为中心输入自身传感器和周围 K 个 SN 数据。
- 明确输出包括未绑定 detected targets、beam-quality distributions、perception tracks、accepted
  UE--track correspondences、CSI-RS candidates 或 fallback，以及通信评估量。
- 配置一张 framework figure，突出 physical target、perception-track 与 communication UE identity 的
  分层边界，以及感知提示只缩小实测集合的闭环。

### 4.2 BEV-Based Multimodal Fusion

写作要点：

- 多视角 camera features 通过几何投影或 lift-splat-style view transformation 进入 BEV。
- BS-side ISAC point cloud 通过点云编码器映射到同一 BEV grid。
- 多站点、多模态特征在 BEV 空间中融合，形成服务 BS 的局部场景表征。
- 讨论时间同步、空间标定、传感器覆盖差异和 missing / noisy observations 的处理方式。

### 4.3 Vehicle Detection and Per-Target Beam Prediction

写作要点：

- CenterNet-like detection head 从 BEV feature map 输出 vehicle centers、target attributes 和 confidence。
- Beam prediction head 为每个 detected target 输出 per-beam power distribution。
- Top-K beams 从 predicted beam distribution 中排序得到。
- 训练目标由 detection loss、target attribute regression loss 和 beam distribution regression/classification
  loss 组成。

### 4.4 Measurement-Assisted Sensing Target-to-User Association

写作要点：

- 初始接入、serving-cell 变化或 binding 失效时执行 conventional SSB/CSI-RS measurement，得到
  communication UE 的实测 beam evidence。
- 将实测 CSI beam 与当前 observed perception track 的 beam likelihood 匹配；SSB-parent consistency
  用于筛除不可行对应关系，Hungarian assignment 在可行配对与未匹配选项上执行一对一求解。
- association acceptance 同时考虑 beam likelihood、margin 和非 GT reliability evidence；高代价或
  模糊配对不建立 correspondence，并保留 conventional refinement。
- 明确该模块解决 sensing target-to-user correspondence，而不是由感知网络直接预测 UE identity。

### 4.5 Track-Assisted Target-to-User Correspondence Maintenance

写作要点：

- CV Kalman filter、CT EKF 和 IMM(CV+CT) 等可比较状态估计器维护 per-BS perception-track state；
  运动模型用于预测物理目标状态，而非产生通信身份。
- 新一帧 BEV detections 与 predicted tracks 通过空间创新、运动一致性、detection confidence 和可选的
  beam-distribution consistency 进行 gated one-to-one association。
- 已接受的 UE--track correspondence 随 matched track 更新而持续；未观测、失配或低置信度状态会
  增加 hint age，并触发 conventional measurement 或 re-association。
- 正式候选只来自当前 observed target 的 quality distribution；纯 track prediction 是 correspondence
  maintenance 的状态信息，不替代当前 CSI-RS candidate evidence。

### 4.6 Communication Interface and System-Level Evaluation

写作要点：

- 对于可靠且当前 observed 的 correspondence，quality distribution 导出 fixed/adaptive \(K_{\mathrm{scan}}\)
  candidate set；其他 UE 使用 conventional refinement。
- UE 在实际扫描 candidate 上选择 beam，因此 candidate coverage、association correctness 和 fallback
  rate 共同决定是否能够减少 CSI-RS resources 而不损害 beam alignment。
- 在统一 RT/Doppler、RZF、调度、功率和 RE accounting 下报告 raw/effective rate、p05 rate、outage、
  candidate recall 与 CSI-RS overhead；不把 Top-\(K\) accuracy 直接等同通信收益。

### 4.7 Algorithm Summary and Complexity

写作要点：

- 给出 conventional-measurement-assisted association 与后续可靠度门控维护两种流程的伪代码。
- 分析主要计算开销：跨节点 BEV fusion、detection/beam heads、target-to-user assignment、
  multi-object state update、candidate measurement 与通信 evaluation。
- 讨论 online feasibility 时保持克制，不写未经测量的实时性能结论。

## Chapter 5: Multimodal V2I Simulator and 5G NR-Oriented Beam-Management Evaluation

本章目的：基于既有 `mmbeam_town05_3weather_v1` 多模态数据资产，构建系统级 Multimodal V2I
Simulator 与 5G NR-oriented beam-management evaluation framework。重点不是重新生成数据资产，而是
在统一的样本、坐标、码本、天气、切分、measurement event、RZF 和 resource accounting 条件下比较
不同 beam-management policy。

叙述逻辑：先给出数据与协议边界，再按多模态/跨节点互补性、beam-quality ranking、target-to-user
association 与 correspondence maintenance、candidate scanning 和系统性能的因果顺序报告结果，最后用
条件、coverage 和 fallback 指标解释收益、失效和限制。

### 5.1 Multimodal V2I Simulator, Dataset, and Frozen Evaluation Protocol

写作要点：

- 说明既有数据集、`clear_day`、`rain_fog_day`、`night` 三种天气、manifest-defined train/validation/
  test split，以及 `(weather_id, frame_id, bs_id)` 与 `(weather_id, frame_id, bs_id, ue_id)` 两类样本。
- 说明 simulator 如何将多模态观测、轨迹、码本质量标签和 RT/Doppler segment 组织为 target-BS-centered
  beam-management episodes；该 simulator 复用既有数据资产，不声称重新生成感知或信道场景。
- 定义 target-BS-centered Sionna BEV local coordinate、4-BS 场景、target BS/SN 角色与 48 SSB/
  192 CSI codebook；明确每个 CSI beam 的 SSB parent。
- 说明一致的 RT segment、Doppler、功率、噪声、调度、RZF、SSB/CSI-RS period 和 raw-RE accounting。
- 明确 val 用于 checkpoint、association/gate threshold 和 candidate policy 选择，test 用于冻结方案的
  held-out evaluation；天气统计应保留原始分子/分母。

### 5.2 Comparison Methods and Controlled Factors

写作要点：

- 感知对照：camera-only、ISAC-only、multimodal；单站点、node mean、gated fusion 和 cross-agent
  attention，以隔离模态与跨节点互补性。
- Beam supervision 对照：strongest-beam CE、KL-only、KL+ranking，比较 matched Recall@\(K\)、power
  retention 与 calibration，而不是只比较 Top-1。
- correspondence 对照：无感知、beam direction、beam top-\(K\)、beam-likelihood association；CV、CT
  和 IMM 的状态估计对照应在相同 predicted detections 上进行。
- 系统对照：conventional 4/12-beam refinement、GT ceiling、fixed/adaptive sensing candidates + fallback；
  oracle/GT 仅作诊断或上界，不能替代正式输入。

### 5.3 Layered Metrics and Evidence Discipline

写作要点：

- 感知层报告 mAP、AP@distance、precision/recall、center L2 与 availability，并按天气、可见性、遮挡
  或节点覆盖条件分层，以检验多模态/跨节点互补性。
- Beam-quality 层报告 matched Recall@\(K\)、power ratio、NLL/ECE/Brier 和 coverage；所有条件指标同时
  给出匹配样本比例，避免忽略 detection availability。
- correspondence 层报告 target-to-user binding coverage、diagnostic accuracy、active accuracy、loss/rebind、
  ID switches、fragmentation、track availability 和 fallback reason，区分初始 association 与时序保持。
- 系统层同时报告 candidate recall、hint usage/fallback、CSI-RS overhead、raw/effective rate、p05 rate、
  outage 与必要时的 fairness/handover 指标；不得用均值速率或 Top-\(K\) accuracy 单独推出系统收益。

### 5.4 Results: Multimodal Complementarity and Beam-Quality Learning

写作要点：

- 先比较 camera、ISAC、multimodal 与单/多节点融合，说明检测与 beam ranking 在不同天气、覆盖和
  遮挡条件下的关系；检测最优与 beam-ranking 最优可能不同，应分别呈现。
- 再比较 strongest-beam CE、KL-only 与 KL+ranking，检验 CSI quality distribution 是否提供更好的
  candidate recall、power retention 和 calibration。
- 所有定量结论必须使用冻结协议、图表和原始统计支持；val 结果仅用于模型选择或诊断，不能替代
  held-out 主结论。

### 5.5 Results: Target-to-User Association and Correspondence Maintenance

写作要点：

- 报告 conventional-measurement-assisted association 如何在多目标场景中建立 sensing target-to-user
  correspondence，并将 acceptance、rejection 与 fallback 分开统计。
- 比较 CV、CT 与 IMM 等状态估计器在 GT/noisy-GT 诊断和 predicted-detection 正式路径中的差异；
  明确受控诊断不能替代端到端结论。
- 通过错误案例或时间线解释 missed detection、相似 beam likelihood、交汇目标、track fragmentation
  与 re-association 如何影响 identity-consistent beam alignment。

### 5.6 Results: Reliability-Gated Candidate Scanning and System Trade-off

写作要点：

- 在相同 measurement/resource profile 下比较 conventional、oracle ceiling 与 sensing-assisted fixed/
  adaptive candidates + fallback，报告 candidate recall、CSI-RS overhead、effective rate、p05 rate 与 outage。
- 分析 \(K_{\mathrm{scan}}\)、CSI-RS period、conventional refinement width、SSB accounting 和 Doppler
  的敏感性，重点呈现 rate--overhead Pareto 而非预设净速率增益。
- 将 system outcome 回溯到上游的 beam quality、association correctness、correspondence persistence 和
  hint usage，区分“beam 本身不准”“提示给错 UE”“候选过窄”和“节省资源但速率受损”等原因。

### 5.7 Discussion and Limitations

写作要点：

- 讨论多模态/跨节点感知在何种可见性、遮挡和天气条件下最具互补价值，以及何时 reliability gate
  应更保守地采用 conventional fallback。
- 讨论 target-to-user association 或 correspondence 失败对实际 beam alignment 的传播机制，避免将
  sensing accuracy 与 communication gain 简化为一一对应关系。
- 说明局部 target-BS 范围、约 100 ms RT segment、感知同步/校准误差和 RZF/resource abstraction 的
  边界；不将该系统评价解释为完整 5G NR deployment performance。

## Chapter 6: Conclusion and Future Work

本章目的：总结本文完成的工作、实验支持的发现和主要限制，并提出未来扩展方向。

叙述逻辑：先回到研究问题，再概括三项贡献对应的完成内容，随后总结由实验支持的结论，
最后讨论 future work。结论章不引入正文没有证明的新 claim。

### 6.1 Conclusion

写作要点：

- 概括本文针对车联网 beam alignment 提出的多模态、跨节点感知框架及其条件互补性证据。
- 概括 measurement-assisted sensing target-to-user association 与 correspondence maintenance 如何使
  beam hint 服务于正确 UE。
- 概括 Multimodal V2I Simulator 与 5G NR-oriented beam-management evaluation framework，以及其由
  perception 到 resource-aware effective rate 的系统级评价方法。
- 只总结 Chapter 5 在冻结协议下支持的发现，不引入正文未验证的比较性结论。

### 6.2 Limitations

写作要点：

- 说明既有数据集与真实部署之间可能存在 domain gap，以及局部 target-BS scope 的限制。
- 说明本文通信评估是 RZF/resource abstraction，不是完整 5G NR stack。
- 说明 sensing noise、calibration error、missing modality、occlusion、association ambiguity 和
  correspondence failure 对系统的潜在影响。

### 6.3 Future Work

写作要点：

- 扩展到跨 BS target-to-user correspondence、协同多 BS beam alignment 与 handover decision。
- 引入更完善的 5G NR protocol-level simulation 和共享 CSI-RS measurement 模型。
- 研究 missing modality、online adaptation、domain adaptation、measurement calibration 和真实数据验证。
- 研究更稳健的 association confidence、两阶段 fallback 和动态候选策略，以改善 rate--outage 边界。
