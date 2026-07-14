# 论文大纲

最后更新：2026-07-14

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
  定位和条件 beam prediction，而非仅堆叠更多输入。
- **挑战二：target-to-user association 及其时序维持。** 感知系统输出的是道路中的物理目标，通信
  系统操作的是参与 SSB、CSI-RS 和下行传输的 UE。在多车场景中，正确的 detection 或 beam ranking
  若被分配给错误 UE，仍会造成错误 beam alignment。初始 association 还会因车辆运动、临时遮挡、
  漏检和近邻目标交汇而失效。因此，需要以 communication measurement 为锚点建立 association，并由
  多目标状态估计、gated data association 和 measurement-assisted re-association 维持其时序有效性；
  tracking 的作用是维护用户归属，而非从感知特征直接识别 UE。
- **挑战三：association-aware candidate reduction 与系统评价。** 感知不应无条件取代通信测量。系统
  须根据 association reliability、当前观测质量和 beam-class posterior confidence 决定使用小候选集还是
  conventional fallback，并以 candidate recall、CSI-RS overhead、sensing use/fallback 和 all-UE effective
  rate 共同评价错误 association、re-association 和 fallback 对实际 beam-alignment trade-off 的影响。
- 建议配置 Figure~1.1：以 target BS 为中心展示多模态/跨节点观测、未绑定 sensing target、
  target-to-user association、时序 association maintenance、可靠度门控候选扫描与 conventional
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
  vehicle detections 与 192-way CSI beam-class posterior；以 strongest-beam Top-1 cross-entropy 训练，
  posterior 的排序用于 candidate measurement 与 association，而不表述为物理 CSI 功率分布。
- 贡献 2：**Target-to-User Association with IMM-Based Tracking。** 以传统通信测量建立或恢复 sensing
  target 与 communication UE 的关联，以 IMM-based multi-object tracking 维持该关联的时序有效性；
  可靠度评估确保 beam hint 仅用于可信的 user association，并在关联不可靠时回退至 conventional
  refinement。
- 贡献 3：**Multimodal V2I Simulator and 5G NR-Oriented Beam-Management Evaluation Framework。**
  基于既有多模态数据资产建立系统级 V2I simulator，在一致的 5G NR-oriented measurement 与资源模型下，
  评价 CSI-RS overhead、sensing use/fallback、effective user rate 与跟踪相关的运行指标，并将感知结果
  连接至实际测量候选和资源约束下的通信后果。
- 贡献措辞保持为“提出/构建/建立”；不在 Introduction 写入未经冻结 test 支撑的定量收益或优越性。

### 1.5 Thesis Organization

写作要点：

- 简要说明 Chapter 2--6 的叙事分工，保持与实际章节文件和后续大纲同步。
- Chapter 2 按问题链条综述：高移动性 V2I 的 beam alignment 负担、sensing-assisted beam
  prediction、V2X 分布式协作感知，以及 multi-candidate 场景中的 target-to-user association。该章在
  association 语境下讨论 tracking 与面向最终用户 rate--overhead 的系统评价，而非按本文贡献并列罗列文献。
- Chapter 3 依次定义局部 V2I network architecture、distributed multimodal sensing model、NR-oriented
  communication and beam-management procedure，以及连接 sensing、association 与 rate--resource
  performance 的 problem formulation。
- Chapter 4 介绍分布式多模态 BEV perception、joint vehicle detection and beam prediction、IMM-based
  tracking、target-to-user association、reliability-gated candidate selection 与通信接口。
- Chapter 5 说明多模态 V2I 数据如何构成评测样本，定义冻结协议和指标，并依次报告多模态感知、
  可靠性门控波束管理与跟踪结果；所有比较在一致的 measurement/resource profile 下进行。
- Chapter 6 总结由冻结证据支持的发现，说明局部 BS 范围、RT segment/PHY abstraction 与感知
  可靠性等限制，并讨论跨 BS association、真实测量校准和更严格协议级评估等扩展。

## Chapter 2: Background and Related Work

本章目的：从 sensing-assisted beam management 的问题本身出发综述相关工作，而非以本文的贡献
作为文献分类。重点说明高移动性 V2I 为何面临 beam alignment 负担，环境感知如何辅助缩小候选
beam 空间，分布式协作感知如何改善道路场景可观测性，以及为何多车场景最终必须处理从 physical
target 到 communication UE 的 association。

叙述逻辑：本章沿“通信决策--感知证据--场景可观测性--用户级归属--系统后果”的链条展开。先说明
传统 beam alignment 在移动性和遮挡下的测量负担；随后回顾 sensing-assisted beam prediction 的输入、
输出和假设；再讨论 V2X distributed cooperative perception 为何能补足单节点观测的局限。最后以
multi-candidate 场景为中心，将 target-to-user association、multi-object tracking 和 association-aware
beam-management evaluation 收束为同一用户级问题，并据此定位本文。

### 2.1 Beam Alignment in High-Mobility V2I Networks

写作要点：

- **Conventional Beam Alignment。** 回顾高频 V2I 的 directional transmission、initial access、beam
  training、CSI acquisition 与 beam refinement，说明 exhaustive/hierarchical search 和 measurement-based
  refinement 的作用与局限。强调最终 service beam 仍须由通信侧测量确认；预测的合理角色是缩小候选
  集合，而非绕过通信决策。
- **Beam Tracking in Dynamic V2I Environments。** 从 vehicle motion、blockage、nearby users 和 CSI aging
  的时序影响出发，分别综述 radar/DFRC state prediction、EKF-based dynamic beamforming、historical-channel
  sequence models 和 end-to-end predictive beamforming。对每项代表工作说明其输入、预测对象与通信
  目标，并指出其通常默认 tracked target 与 communication link 已对应。
- 以 candidate coverage、measurement overhead、recovery frequency 和 effective communication performance
  为线索，引出仅凭单帧最强 beam 分类不足以评价 beam-management policy。

### 2.2 Sensing-Assisted Beam Prediction

写作要点：

- **Vision- and Geometry-Aided Beam Prediction。** 分别讲述 camera-based beam/blockage prediction、
  vision-aided beam pair and coherence-time prediction、radar-aided beam prediction 与 LiDAR-aided future
  beam prediction 的输入和输出，说明语义、位置与几何线索如何缩小 beam search space。
- **Multimodal Beam-Prediction Models。** 围绕模型与任务形式组织文献：vision--position fusion、
  transformer-based cross-modal fusion、BEV-temporal transformer、occlusion-aware multi-task learning、
  missing-modality modelling、cross-modal attention、knowledge distillation，以及 RL/contextual-bandit
  decision models。对每项工作说明其融合输入、预测目标和评价口径；DeepSense 6G 与其 challenge 作为
  同步多模态数据和泛化评测资源分别说明。
- 比较 strongest-beam classification 与由 class posterior 导出的 ranked Top-\(K\) prediction；说明 Top-1
  CE 的 192-way scores 如何形成 candidate set，并强调它们不是物理 CSI power distribution。
- 指出多数工作仍以已知位置、已经配对的 sensing sample--link 或单一目标为前提。多车道路场景中，
  一个正确的 target-level ranking 尚不能说明它会被用于正确的 UE。

### 2.3 Distributed Cooperative Perception in V2X Networks

写作要点：

- **Cooperative Perception in V2X Networks。** 从单节点相机或单一传感器的视场、遮挡、天气、稀疏
  几何和异步观测局限出发，分别综述 multi-agent feature fusion 与 distributed sensing-aided networking，
  说明 pose error、time synchronisation、communication cost、environment semantics 与 cross-node fusion
  的处理方式。
- **BEV Representation for Cooperative Perception。** 说明 camera-to-BEV view transformation、camera--
  point-cloud BEV fusion 和 point-based target representation 的代表工作；BEV 为多视角图像、BS-local
  geometric sensing 与 cross-node observations 提供共享道路平面接口，也允许 detection 与 beam-related
  inference 利用同一 target-level scene context。不得将自动驾驶 detection 的性能直接等同于通信收益。
- 收束到通信相关缺口：现有分布式感知通常服务于驾驶感知任务，现有 multimodal beam prediction 也
  往往不显式组织分布式观察和未绑定车辆目标；因此仍需要将更完整的场景证据连接至用户级 beam
  management。

### 2.4 Target-to-User Association in Multi-Candidate V2I Scenarios

写作要点：

- **Target ambiguity。** 明确 physical sensing target、perception track 和 communication UE 的语义
  区别。在多车、相近方位、暂时漏检或遮挡情形下，per-target beam prediction 不会天然给出 UE identity；
  若 beam hint 被错误归属，即使其自身 ranking 正确，也不能改善正确用户的 beam alignment。
- **Association and tracking。** 综述 multi-candidate beam prediction、transmitter identification、
  geometric/object association、tracking-by-detection 以及 Kalman/EKF/IMM state estimation。区分它们
  对目标发现、一次关联和时序状态维持的作用；将 conventional communication measurement 定位为 UE--track
  association 的通信侧锚点，而 IMM-based tracking 用于维持关联的时序有效性，不把 tracking 写成视觉
  UE recognition。
- **Association-aware evaluation。** 将 tracking/association 的文献讨论自然延伸至 beam-management
  consequences。除 detection、beam Top-\(K\) 和 association accuracy 外，还须通过 candidate recall、
  re-association/fallback frequency、CSI-RS overhead、effective rate、lower-tail rate 和 outage 刻画错误
  关联与恢复测量如何传导到最终用户性能；数据集和 system-level simulator 是支撑该评价链的手段，
  不作为与前述问题并列的文献类别。

### 2.5 Research Gaps and Thesis Positioning

写作要点：

- 连续总结：sensing-assisted beam prediction 已证明环境证据可压缩候选 beam 空间；distributed
  cooperative perception 提供了提升道路场景可观测性的基础；multi-candidate 场景则暴露出 physical
  target 与 communication UE 之间的身份接口；association 的可靠性最终必须在资源约束下通过用户
  性能验证。
- 归纳三项相互衔接的研究缺口：缺少面向通信的分布式多模态 target-level scene representation；
  缺少由通信侧证据锚定、并能在运动和观测中断下维持的 target-to-user association；缺少贯通 target
  availability、beam ranking、association quality、measurement overhead 与 effective user rate 的评价
  链条。
- 据此克制定位本文：以 target-BS-centered multimodal BEV perception 生成未绑定 target-level beam
  evidence，以 measurement-assisted association 和 IMM-based tracking 维持其用户归属，并在统一资源
  abstraction 下评价所得 beam-management policy。章节结尾过渡至 Chapter 3 的系统模型与问题定义。

## Chapter 3: System Model and Problem Formulation

本章目的：以通信系统建模为主线，定义局部 V2I 网络、分布式多模态观测和 resource-aware
downlink communication model。章节先由信道、下行信号、RZF precoding 和 SINR 建立每个 VUE 的
achievable-rate 模型，再说明 SSB/CSI-RS beam management 与 sensing-assisted candidate selection 如何
改变资源开销和有效信道，最后在因果信息约束下将系统表述为长期 all-UE average-rate maximisation。

叙述逻辑：先定义 target BS、sensing nodes 与 VUE 的网络关系；随后给出 camera 和 BS-local ISAC
point cloud 的观测模型，并以简洁回波信道、静态 clutter removal 与 point-cloud extraction 说明 ISAC
点云的物理来源；接着以信道、信号、SINR、SSB/CSI-RS measurement、RZF precoding 和资源开销建立
通信模型；最后以 association-constrained candidate selection 为约束，给出长期平均用户速率目标。
该章不展开 BEV fusion、network loss、Hungarian implementation 或 IMM filter recursion，这些算法细节留给
Chapter 4。

### 3.1 Network Architecture

写作要点：

- 定义 BS 集合、target BS、为其服务的 VUE 集合和邻近 sensing-node 集合；SN 只提供感知信息，
  不独立承担下行服务。
- 说明论文以 target BS 为局部决策点；每个 serving cell 内独立维护 target-to-user association，
  VUE 切换至新 serving cell 后重新建立局部 association，不假设全局跨 BS track identity。
- 仅简洁说明相机与 ISAC 观测经标定表达于 target-BS-centered local BEV frame；坐标变换与 feature
  construction 不作为本节重点。

### 3.2 Multimodal and Distributed Sensing Model

写作要点：

- 以 \(\mathcal{O}_{b,n}=\{\mathcal{I}_{b,n},\mathcal{I}_{\mathcal{N}_b,n},\mathcal{P}_{b,n}\}\) 定义
  sensing epoch \(n\) 可用的 target-BS cameras、SN cameras 和 BS-local ISAC point cloud；说明 epoch
  由 sensor period 产生，并与后续 NR slot interval 对齐。

#### 3.2.1 Camera Observations

- 定义 target BS 与各 SN 的多视角 image set；已知 calibration 将每个 view 投影/表达至 target-BS local
  frame。
- 强调相机观测提供语义、可见性与跨视角空间覆盖；不在本节指定 camera encoder 或 BEV fusion algorithm。

#### 3.2.2 ISAC Point-Cloud Model

- 定义 BS 发射已知 probing/communication waveform 后的 echo observation：回波 channel 包括 static-clutter
  component 与 dynamic-target components，并加入噪声。
- 由 \(\widehat{\mathbf H}^{\mathrm{echo}}=\mathbf Y^{\mathrm{echo}}\mathbf S^{\dagger}\) 给出等效 echo-channel
  estimate；经 static clutter removal 得到 dynamic component，再由 delay--angle--Doppler/target extraction
  operator 得到 \(\mathcal P_{b,n}\)。
- 明确该关系只解释 ISAC point cloud 的物理语义；论文使用既有多模态资产的 point cloud，不将完整 ISAC
  waveform processing 或 point-cloud generation 作为研究对象。

### 3.3 Communication Model

写作要点：

#### 3.3.1 Downlink Signal and Channel Model

- 定义 target BS 到 VUE 的多径、Doppler-aware channel vector，以 ray-tracing reference channel 与
  segment 内演化为物理来源；不展开无线信道生成实现。
- 对 \(\mathcal U_b^{\mathrm{sch}}[n]\) 给出多用户下行接收信号：目标流、残余 multi-user interference
  和噪声共同定义 \(\gamma_{b,u,n}\)。service-beam measurement 与 CSI feedback 后的 effective channel
  进入 digital precoder。

#### 3.3.2 Beam Management and Precoding

- 定义 NR-oriented time hierarchy：\(T_{\mathrm{frame}}=10\) ms、随 numerology 变化的
  \(T_{\mathrm{slot}}\)，以及 sensing period、SSB periodicity 与 CSI-RS periodicity。具体数值由 Chapter 5
  的 frozen radio profile 给出，本章仅定义其关系和通信角色。
- 定义 48-beam SSB codebook、192-beam CSI codebook、CSI-to-SSB parent relation 与物理 beam gain
  \(g_{b,u,n}(k)=|\mathbf h_{b,u,n}^{\mathrm H}\mathbf f_{b,k}^{\mathrm{CSI}}|^2\)。最强物理 beam 提供
  Top-1 label，但不作为在线决策输入。
- conventional SSB/CSI-RS procedure 用于 coarse identification、initial/re-association 和 refinement。
  只有可靠且当前 observed 的 association 才以 posterior 缩小 CSI-RS candidate set；service beam 始终由
  measured candidate response 选择。RZF 由 measured effective-channel estimates 构成，给出 post-RZF SINR。

#### 3.3.3 Resource Overhead and Effective Rate

- 定义 \(\tau_{b,n}^{\mathrm{tot}}=\tau_{b,n}^{\mathrm{SSB}}+
  \tau_{b,n}^{\mathrm{CSI\text{-}RS}}+\tau_{b,n}^{\mathrm{ctrl}}+
  \tau_{b,n}^{\mathrm{data}}\)，并以每个 acquisition event 的 \(K_e\)、measurement multiplexing
  \(M\) 与 \(\delta_{\mathrm{probe}}\) 表示 CSI-RS overhead。
- 以 scheduling indicator、downlink fraction、data resource fraction 和 post-RZF SINR 定义
  \(R_{b,u,n}^{\mathrm{ach}}\)。未调度的 active VUE rate 计为零，因此后续使用 all-UE time-average，
  而非 scheduled-user conditional rate。

### 3.4 Problem Formulation

写作要点：将 Chapter 3 的系统问题写为因果、受约束的长期速率最大化，而不是将训练 loss 或单帧
beam Top-\(K\) accuracy 误写为通信优化目标。感知网络和 IMM 的具体训练/递推留在 Chapter 4；本节只
规定它们能够向通信决策提供哪些非 oracle 信息。

#### 3.4.1 Association-Constrained Candidate Selection

- 将 multimodal observation 映射为未绑定 detections 与 192-way beam-class posterior；定义当前 observed
  track 集合以及 partial one-to-one mapping
  \(\pi_{b,n}:\mathcal U_b[n]\rightarrow\mathcal R_{b,n}^{\mathrm{obs}}\cup\{\varnothing\}\)。
- 对 initial/re-association event，使用 measured CSI beam 与 track posterior 构造 normalised negative-log
  matching cost；SSB-parent consistency 限定可行 pair，assignment 保留 unmatched choice。
- 定义 candidate-use decision \(G_{u,n}\)：只有当前 observed 且 accepted 的 association 才使用
  \(\operatorname{TopK}_{K_{\mathrm{scan}}}(\mathbf p_{\pi_{b,n}(u),n})\)；否则使用
  \(\mathcal C_{b,u,n}^{\mathrm{conv}}\)。纯 track prediction 不产生正式候选 beam。

#### 3.4.2 Long-Term Average-Rate Maximisation

- 定义 \(\overline R_b[N]=N^{-1}\sum_n|\mathcal U_b[n]|^{-1}\sum_u
  R_{b,u,n}^{\mathrm{ach}}\)，明确其包含未调度 VUE 的零速率。
- 以 \(\liminf_{N\to\infty}\overline R_b[N]\) 为目标，联合表述 association、candidate set、precoder 和
  scheduling decisions；约束包括 candidate policy、measured-beam service selection、resource budget 和
  per-cycle transmit-power budget。
- 强调决策只能使用 cycle \(n\) 可得的 sensing posterior、track state 与 communication measurements；
  不输入 oracle identity、未测量 beam gain 或 future channel。Chapter 4 随后给出满足这些接口约束的
  BEV learning、IMM tracking 和 association/candidate algorithm。

## Chapter 4: Proposed Sensing-Assisted Beam Management Framework

本章目的：在 Chapter 3 的系统接口上，给出由分布式多模态 BEV 表征、联合车辆检测与 Top-1 CSI
beam prediction、未绑定多目标轨迹、measurement-assisted target-to-user association 和
reliability-aware candidate selection 组成的完整算法。章节聚焦每个模块为何需要、交换何种信息，
以及这些设计如何避免把 oracle UE identity 或未实测 beam 写入决策路径。

叙述逻辑：先界定 target-level sensing evidence 与 UE-level communication decision 的边界；随后说明
多节点、多模态观测如何形成 BEV feature，并由共享空间表征同时支持 detection 和 Top-1 beam-class
prediction；接着以 track maintenance 维持 physical target 的时序连续性，以 conventional measurement
建立或恢复 UE--track association；最后用 reliability decision 将可靠的 posterior scores 转化为有限 CSI-RS
candidate set，否则回退 conventional refinement。该顺序将学习、身份接口与通信决策串为一条完整算法链。

### 4.1 Framework Architecture

写作要点：

- 按照一个 sensing epoch 的先后顺序，以非复杂数学语言交代四步数据流：多模态网络首先输出未绑定车辆
  detections 及每个目标的 CSI beam-class posterior；IMM tracker 将连续 detections 维护为 physical
  target tracks；在 initial access、new serving cell 或失效恢复时，conventional SSB/CSI-RS measurement
  与 track-level beam-posterior score 共同建立 UE--track association；reliability decision 决定采用 sensing
  candidates 还是 conventional refinement。
- 明确神经网络输出的是目标位置、属性/置信度和 192-way beam-class posterior，而非 UE identity、物理
  CSI power distribution 或 service beam。IMM tracker 只维持物理目标的时序状态和观测连续性，不直接赋予通信身份。
- 清楚说明初始关联的证据链：communication-side measurement 给出 UE-indexed beam evidence，当前可观测
  track 的 predicted posterior score 提供 target-side evidence；二者在 SSB parent consistency 和一对一
  assignment 约束下匹配。测量所得候选中的最佳 CSI-RS beam 才成为 service beam。
- 为 overview figure 配套叙述，突出 sensing evidence、track state、communication measurement 与
  reliability-aware candidate decision 的边界；GT/oracle 仅连接诊断和评估支路。可保留一行简洁流程
  \(\mathcal O_{b,t}\rightarrow\{d_{i,t},\mathbf p_{i,t}\}\rightarrow\mathcal R_{b,t}
  \rightarrow\pi_{b,t}\rightarrow\mathcal C_{b,u,t}\)，不在本节展开关联代价或优化公式。

### 4.2 Distributed Multimodal BEV Perception and Beam Prediction

写作要点：本节将多模态、跨节点 BEV 表征与联合 detection--Top-1 beam prediction 作为一个连续的
perception-and-learning pipeline 叙述：先说明何以形成共享空间表征，再说明该表征如何以统一的目标级接口
输出位置、属性和 beam-class posterior，最后给出 strongest-beam Top-1 cross-entropy supervision。

#### 4.2.1 Multimodal BEV Representation

- 定义 \(\mathcal J_b=\{b\}\cup\mathcal N_b\)，将 target-BS/SN image features 经标定投影或 lift 至
  target-BS-centred BEV，并将 BS-local ISAC point cloud 编码到同一平面。
- 以 \(\Phi_{\mathrm{node}}\) 和 \(\Phi_{\mathrm{modal}}\) 表示节点聚合与模态融合；将 node mean、cross-agent
  attention、modal gating 等定位为可比较实现，而非把具体卷积、体素或 tensor layout 写为算法创新。
- 说明共享 BEV 的设计动机：SN 提供遮挡/视场互补，target BS 保持与 serving link 的几何关系，ISAC 提供
  与视觉互补的局部几何证据。availability/confidence mask 处理 missing、noisy 或不同覆盖条件的输入，
  但不将同步和标定误差的工程补偿写成本章重点。

#### 4.2.2 Joint Detection and Beam Prediction

- 定义 \(d_{i,t}=(\widehat{\mathbf r}_{i,t},\widehat{\mathbf a}_{i,t},\widehat c_{i,t})\) 与
  \(\mathbf p_{i,t}=\operatorname{softmax}(\operatorname{Sample}(\mathbf P_{b,t},\widehat{\mathbf r}_{i,t}))\)；说明属性可包括
  size、heading 与 velocity，具体 head design 不影响本章的接口表述。
- 从共享 BEV feature 同时产生 vehicle-centre heatmap、属性回归与 dense 192-way CSI beam-class logits；在
  decoded detection centre 采样得到 \((d_{i,t},\mathbf p_{i,t})\)，从而使 detection 和 beam prediction
  在同一 target-level spatial interface 上对齐。
- 以 heatmap/attribute terms 与 beam term 组成 joint loss，说明共用 BEV context 使物体可见性与 link
  quality 共同约束目标表示。
- 明确 link coordinate 只在训练/评估中选择监督采样位置；UE identity、ground-truth beam 和 link
  coordinate 不作为前向输入。因此 \(\mathbf p_{i,t}\) 是未绑定 physical target 的 beam-class posterior，
  而不是 service-beam declaration 或物理 CSI power distribution。

#### 4.2.3 Top-1 Beam Classification

- 以物理 CSI gain 最大的 beam \(k^\star=\arg\max_k g(k)\) 作为 strongest-beam label，并以
  \(\mathcal L_{\mathrm{beam}}=-\log p_\theta(k^\star)\) 进行标准 Top-1 cross-entropy training。
- 将模型输出定位为 192-way beam-class posterior：其 Top-\(K\) 排序可用于 candidate measurement 与
  association score，但不解释为 CSI power distribution、calibrated power estimate 或直接 precoder。
- 明确模型为全部 192 beams 导出 scores，而 \(K_{\mathrm{scan}}\) 才是实际 CSI-RS measurement budget；
  candidate recall 和 Top-\(K\) power ratio 是评价指标，不是额外监督项。

### 4.3 IMM-Based Multi-Object Tracking

写作要点：本节作为独立的 sensing-domain temporal-estimation module，说明 IMM 如何在不引入 UE
identity 的条件下，为每个 physical target 提供连续、可量化不确定性的轨迹状态。先分别建立 CV 与
coordinated-turn (CT) 模型，再以完整的 IMM mixing、model-conditioned filtering、mode-probability update 和
state fusion 递推说明两种运动假设如何协作；最后给出 detection-to-track assignment 及 track management。

#### 4.3.1 Motion Models

- 分别定义 CV linear Kalman model 的 Cartesian state
  \([p_x,p_y,v_x,v_y]^{\mathsf T}\)、state-transition matrix、position measurement model 与 process/measurement
  noise；它描述短时近似匀速运动。
- 采用 \([p_x,p_y,v,\psi,\omega]^{\mathsf T}\) 建立 CT nonlinear state evolution，给出由速度、heading 和
  turn rate 导出的弧线位置更新，以及 \(\omega\rightarrow0\) 时的 CV limit；以 EKF Jacobian 完成 CT model
  的局部线性化。说明该模型适用于车辆转弯或曲线行驶。
- 说明两种状态坐标之间的 deterministic transformation，用于在 IMM mixing 和最终输出时保持概率与协方差的
  一致性；不将运动模型解释为 communication UE identification。

#### 4.3.2 IMM Filtering and Track Management

- 对 Markov transition probability、mixing probability、mixed initial state/covariance、CV prediction、CT EKF
  prediction、measurement innovation、Kalman gain、model likelihood、posterior mode probability 与 fused state/
  covariance 逐步给出数学递推。强调 IMM 的优势是依据观测自适应地调节直行与转弯模型权重，而非预先固定车辆
  的运动类别。
- 对每个 `(split, weather, target BS)` 独立维护 tracks。以 predicted position/covariance 的 innovation gate
  先排除不可能 pair，再以 Hungarian assignment 处理 detection--track one-to-one correspondence。
- 匹配检测更新运动状态、mode probability、track confidence、observation history、当前 beam-class posterior
  与 hint age。未匹配轨迹可以暂时保留，但其纯预测状态不生成正式 beam candidate；该边界使 tracking 的角色
  保持为 temporal continuity，而非替代通信测量。

### 4.4 Measurement-Assisted Target-to-User Association

写作要点：本节将 communication-side beam measurement 与 4.2 的 target-level beam-class posterior 连接为
一个明确的 UE--track matching problem，并在同一节内说明何时可以安全地将匹配结果用于 CSI-RS candidate
reduction。可靠度是 association-to-candidate interface 的判断条件，而非额外独立贡献模块。

#### 4.4.1 Initial Association from Beam Measurements

- 在 initial access、new serving cell、binding failure 或 sensing evidence 不可靠时执行 conventional
  SSB/CSI-RS measurement。重申 4.2 导出的 \(\mathbf p_{r,n}\) 是当前 observed physical track 对各 CSI beam
  的 classifier posterior score；将 UE \(u\) 的 conventional measured beam
  \(\kappa_{b,u,n}\) 代入 \(p_{r,n}(\cdot)\)，以 normalised negative log posterior score 建立
  \(c^{\mathrm{bind}}_{u,r,n}\)。
- 定义 SSB-parent consistency 和 current-observation requirement 所构成的 feasible edge set。随后在带 dummy
  unmatched columns 的 cost matrix 上使用 Hungarian assignment，给出 partial mapping
  \(\pi_{b,n}:\mathcal U_b[n]\rightarrow\mathcal R_{b,n}\cup\{\varnothing\}\)。以 cost threshold 和
  assignment margin 拒绝不明确配对，而非强制每个 UE 都绑定一个 track。
- 强调该步骤不使用 GT、几何反推 beam 或感知直接识别 UE；beam direction 与 beam top-\(K\) 只作为
  association ablations。

#### 4.4.2 Reliability-Aware Candidate Selection

写作要点：

- 将 accepted association、current observed detection 与 non-GT reliability evidence 共同定义为 candidate-use
  event。可靠度输入包括 binding confidence、assignment margin、current detection/track confidence、hint age、
  SSB-parent consistency、observation count 与 beam-score mass。
- 只有 accepted binding 对应当前 observed detection 且 \(G_{u,t}=1\) 时，才从
  \(\mathbf p_{\pi_{b,t}(u),t}\) 导出 sensing candidates；否则采用 conventional refinement。纯 track
  prediction 不可替代当前观测。
- 给出 fixed-\(K_{\mathrm{scan}}\) 与 score-mass adaptive-\(K_{\mathrm{scan}}\) 规则；后者以累计分数达到
  阈值 \(q\) 且不小于 \(K_{\min}\) 的最小 \(k\) 为 measurement width。
- 重申 beam-class posterior 只缩小实际 CSI-RS scan；UE 在 measured candidate set 内按 SNR 选择 service
  beam。该接口随后交由 Chapter 5 的 RZF/resource evaluation。

### 4.5 Algorithm Summary and Complexity

写作要点：

- 给出逐 sensing epoch 的伪代码：BEV representation、joint inference、IMM prediction/update、event-driven
  association/reassociation、candidate-use reliability test、candidate/fallback decision 与 measured-beam interface。
- 清楚区分 association event 与普通 maintenance epoch，避免误写成每帧均需 full scan 或每帧均可使用
  sensing hint。
- 分析主要项：BEV feature construction、192-way target-level prediction、track/detection assignment、UE--track
  assignment 与 candidate measurement width；Hungarian assignment 对相应候选规模呈三次复杂度。
- 不作未经 profiling 支持的 real-time latency claim；复杂度讨论仅说明算法规模如何随 sensor views、
  target/tracks、UEs 和 \(K_{\mathrm{scan}}\) 变化。

## Chapter 5: Multimodal V2I Dataset Construction and Experimental Evaluation

本章目的：基于既有多模态数据资产构造面向目标 BS 的 V2I 评测样本和 beam-management episodes，并在统一的 5G NR-oriented measurement/resource profile 下，报告从目标检测与波束预测到可靠性门控候选测量、再到 all-UE effective rate 的完整结果链。重点是复用既有感知和链路资产进行一致的系统评价，而非重新生成原始图像、点云或无线信道。

叙事逻辑：先界定多模态 V2I 数据如何组织为可复现的训练、验证和测试样本；随后定义只服务于正式结果的指标与冻结协议；再依次报告多模态/分布式感知、可靠性门控波束管理和跟踪模块的结果。这样的顺序将上游的可观测性和候选质量与下游的测量开销和有效吞吐率直接连接，同时避免把单一 Top-K 指标误作系统收益。

### 5.1 Multimodal V2I Dataset Construction

#### 5.1.1 Multimodal Simulation and Data Generation

- 说明本章使用既有 mmbeam_town05_3weather_v1 多模态数据资产。系统级评测器将同步的相机观测、BS-local ISAC 点云、车辆/链路标签、轨迹片段和码本信息组织为 target-BS-centred episode；它不重新生成 CARLA、射线追踪、图像、点云或信道资产。
- 说明每一个 sensing sample 由 weather_id、frame_id 和 bs_id 标识，链路监督样本另含 ue_id。感知输入进入 Chapter 4 的 BEV 网络；测试阶段的 detector、track 和 association 输出则与既有链路演化和资源记账接口相连。
- 给出 48-beam SSB codebook、192-beam CSI codebook 及其 parent relation 的作用：预测的 192-way beam-class posterior 用于排序、关联和 CSI-RS 候选缩减，而非直接宣告服务波束。

#### 5.1.2 Scenario Definition and Dataset Splits

- 定义四 BS 道路场景、target BS 与 neighbouring sensing nodes 的角色，以及 clear_day、rain_fog_day、night 三种条件；所有结果均在 manifest 定义的 train/validation/test split 上组织。
- 说明局部 BEV 和 local service region 的边界：每个 target BS 独立维护 sensing targets、tracks 和 target-to-user associations，不将本章结果表述为跨 BS 全局身份管理。
- 给出冻结 radio profile：100 ms SSB periodicity、20 ms CSI-RS periodicity、每个 SSB parent 的四波束 conventional refinement、一致的 RT segment、Doppler、功率、噪声、调度、RZF 和归一化资源记账。雨雾条件使用 min_association_margin=0.10 的固定 test-tuned operation point，应表述为本结果包的运行配置，而非独立的 held-out 泛化结论。

### 5.2 Evaluation Metrics and Protocol

#### 5.2.1 Detection and Beam-Prediction Metrics

- 定义 AP@2m 与 Recall@2m，用于同时刻画 detection precision 和 target availability。
- 对与参考目标匹配的检测，报告 Beam Top-1@2m、Beam Top-4@2m 和 Top-4 power ratio。前两者评价 strongest-beam class ranking，最后一项评价候选集捕获的链路能量；它们不是网络输出的功率校准声明。
- 以 camera-only、ISAC-only、single-station multimodal、mean-gated multimodal、node-mean fusion 和 cross-agent multimodal 作为同一任务上的已报告方案，在本节描述其输入/融合差异，不单设 Baselines 一节。

#### 5.2.2 System-Level Metrics

- 给出 all-UE time-average effective throughput 的定义：用户速率包含 SSB、control、CSI-RS 和未被调度时段的资源影响；因此不同 candidate policies 在相同冻结 profile 下可直接比较。
- 同时报出 CSI-RS overhead、sensing-use ratio、conventional-fallback ratio 和平均 measured candidate count。sensing use/fallback 是 association-to-policy 的运行证据，不替代未单独导出的 binding accuracy。
- 对 tracker 比较，报告系统级 rate、overhead、sensing/fallback、candidate count 和 handover；受控轨迹图仅用于展示运动估计行为，不能替代端到端比较。
- 正式系统结果比较 conventional four-beam refinement、conventional twelve-beam refinement 与 perception-assisted policy。所有 policy 使用同一 measurement/resource profile；不引入 GT/oracle ceiling 作为正式运行方案。

### 5.3 Results: Multimodal Perception and Beam Prediction

#### 5.3.1 Modality and Fusion Results

- 以 Table 5.1 总体比较六类感知/融合方案，以 Table 5.2 按天气分层。叙述应先指出不同指标并不存在统一最优方案：cross-agent multimodal 的 AP@2m 为 78.73%，mean-gated multimodal 的 Recall@2m 和 Top-4 power ratio 分别为 81.90% 和 97.13%，而 single-station multimodal 的 Beam Top-1@2m 为 71.54%。
- 结合三种天气解释互补性而非只报告平均值。例如 clear_day 下 cross-agent multimodal 的 AP@2m 为 81.92% 和 Top-1 为 75.00%；rain_fog_day 下 ISAC-only 的 AP@2m 高于 camera-only，而多模态方案保持更高的整体 detection/候选质量；night 条件也显示相机与 ISAC 的条件性差异。
- 结论限定为：多模态和跨节点信息改善的维度取决于环境和评价指标，因而系统接口应保留 ranking、可靠性和 fallback，而不从单一 detection 或 Top-1 数值直接推断用户收益。

#### 5.3.2 Value of Nearby Sensing Nodes

- 以 Figures 5.1--5.3 报告在固定模型下可用 nearby nodes 数从 0 到 5 的变化，明确这些是 missing-node robustness/coverage curves，不是为每个节点数量分别重训练的容量比较。
- 报告 cross-agent attention 的 AP@2m 由 38.59% 增至 80.41%，Recall@2m 由 52.34% 增至 83.15%；Beam Top-4@2m 在较少节点时已较高、随后趋于饱和。将此解释为额外视角首先改善目标可见性和定位，而不同融合方式对 beam Top-1 的影响不必与 detection 完全同序。
- 对照 cross-agent+gated、cross-agent attention 与 node-masked 的趋势，说明可用节点和融合机制的共同作用；避免宣称某一方案在所有 detection 和 beam 指标上均占优。

### 5.4 Results: Reliability-Gated Beam Management

#### 5.4.1 Results Across Weather Conditions

- 使用 Table 5.4 和 Figure 5.4 对比三种天气下的 effective user rate、CSI-RS overhead、sensing use 和 fallback。clear_day 中 perception-assisted policy 的平均 rate 为 155.453，相对 conventional four-beam 的 151.367 与 twelve-beam 的 127.033，CSI-RS overhead 为 1.39%。
- 同时报告条件差异：rain_fog_day 的 sensing use 为 56.65%、fallback 为 43.35%；night 的 sensing use 进一步降为 30.07%、fallback 为 69.93%。说明 gate 在证据较弱时转向 conventional refinement，而非把预测候选无条件用于 UE。
- 强调 per-weather 数字是冻结运行点下的 policy consequence；不把 sensing-use ratio 表述为单独的 association accuracy。

#### 5.4.2 Macro-Average Resource and Rate Trade-off

- 使用 Figure 5.5 汇总宏平均：perception-assisted policy 的 effective user rate 为 146.332，CSI-RS overhead 为 1.56%，而 conventional four-beam 与 twelve-beam 分别为 142.248/1.90% 和 115.890/5.71%。
- 将 54.35% sensing use 与 45.65% fallback 解释为可靠性门控下的混合运行状态。公共的 data-fraction 项来自冻结的数据侧资源配置，因此不应被解读为另一项由 policy 单独优化的结果。
- 以 rate--measurement trade-off 收束本节：预测只在当前检测和 target-to-user association 可信时缩小 CSI-RS 候选集；最终 service beam 仍在实际测量候选中确定。

### 5.5 Results: Tracking under the Frozen Protocol

#### 5.5.1 Controlled Trajectory Diagnosis

- 使用 Figure 5.6 展示 test/clear-day/BS-NE 条件下、以 GT 加 1.0 m 位置噪声作为输入的 KF-CV、KF-CT 与 IMM 轨迹。图的作用是直观展示运动模型如何平滑和处理转弯片段。
- 明确这是隔离 detection/association error 的受控诊断，不据此作端到端吞吐率或 tracker superiority 结论。

#### 5.5.2 End-to-End Tracker Comparison

- 以 Table 5.6 在同一 Top-1 CE detector 和冻结协议下报告三种 tracker 的宏平均系统指标。IMM 的 rate/overhead/use/fallback 为 146.332/1.56%/54.35%/45.65%，KF-CV 为 146.373/1.56%/53.80%/46.20%，KF-CT 为 145.880/1.57%/52.26%/47.74%。
- 说明这组数值的差异较小，且 KF-CV 的 rate 略高于 IMM；因此不将 IMM 表述为由 effective rate 证明的普遍最优 tracker。IMM 的方法定位是为 association maintenance 提供多运动模型状态估计，系统结果应与候选数和 fallback 一并解读。

### 5.6 Discussion and Limitations

- 综合讨论：多模态和 nearby-node information 主要改变目标可见性与候选 ranking；可靠性门控将这种上游信息转化为有条件的 CSI-RS 节省，并在不可靠时保留 conventional fallback。
- 说明正式结果没有独立 accepted-binding accuracy、p05 rate 或 outage 主表，因而本章只以 sensing use/fallback 和 all-UE effective throughput 说明 association 的运行后果，不延伸为未测量的用户级结论。
- 重申边界：结果针对局部 target-BS service region、既有数据资产、约 100 ms RT segments 和 RZF/resource abstraction；它们不等同于完整 5G NR protocol-stack 或真实部署性能。
## Chapter 6: Conclusion and Future Work

本章目的：总结本文完成的工作、实验支持的发现和主要限制，并提出未来扩展方向。

叙述逻辑：先回到研究问题，再概括三项贡献对应的完成内容，随后总结由实验支持的结论，
最后讨论 future work。结论章不引入正文没有证明的新 claim。

### 6.1 Conclusion

写作要点：

- 概括本文针对车联网 beam alignment 提出的多模态、跨节点感知框架及其条件互补性证据。
- 概括 measurement-assisted sensing target-to-user association 与 association maintenance 如何使
  beam hint 服务于正确 UE。
- 概括 Multimodal V2I Simulator 与 5G NR-oriented beam-management evaluation framework，以及其由
  perception 到 resource-aware effective rate 的系统级评价方法。
- 只总结 Chapter 5 在冻结协议下支持的发现，不引入正文未验证的比较性结论。

### 6.2 Limitations

写作要点：

- 说明既有数据集与真实部署之间可能存在 domain gap，以及局部 target-BS scope 的限制。
- 说明本文通信评估是 RZF/resource abstraction，不是完整 5G NR stack。
- 说明 sensing noise、calibration error、missing modality、occlusion、association ambiguity 和
  association failure 对系统的潜在影响。

### 6.3 Future Work

写作要点：

- 扩展到跨 BS target-to-user association、协同多 BS beam alignment 与 handover decision。
- 引入更完善的 5G NR protocol-level simulation 和共享 CSI-RS measurement 模型。
- 研究 online adaptation、domain adaptation、measurement calibration 和真实数据验证。
- 研究更稳健的 association confidence、两阶段 fallback 和动态候选策略，以改善 rate--outage 边界。
