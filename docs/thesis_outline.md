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
- **挑战二：target-to-user association 及其时序维持。** 感知系统输出的是道路中的物理目标，通信
  系统操作的是参与 SSB、CSI-RS 和下行传输的 UE。在多车场景中，正确的 detection 或 beam ranking
  若被分配给错误 UE，仍会造成错误 beam alignment。初始 association 还会因车辆运动、临时遮挡、
  漏检和近邻目标交汇而失效。因此，需要以 communication measurement 为锚点建立 association，并由
  多目标状态估计、gated data association 和 measurement-assisted re-association 维持其时序有效性；
  tracking 的作用是维护用户归属，而非从感知特征直接识别 UE。
- **挑战三：association-aware candidate reduction 与系统评价。** 感知不应无条件取代通信测量。系统
  须根据 association reliability、当前观测质量和 beam-distribution confidence 决定使用小候选集还是
  conventional fallback，并以 candidate recall、CSI-RS overhead、effective rate、p05 rate 和 outage
  共同评价错误 association、re-association 和 fallback 对实际 beam-alignment trade-off 的影响。
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
  vehicle detections 与 192-way CSI beam-quality distribution；distribution/ranking learning 同时支持
  candidate ranking、置信度刻画和 association likelihood。
- 贡献 2：**Target-to-User Association with IMM-Based Tracking。** 以传统通信测量建立或恢复 sensing
  target 与 communication UE 的关联，以 IMM-based multi-object tracking 维持该关联的时序有效性；
  可靠度评估确保 beam hint 仅用于可信的 user association，并在关联不可靠时回退至 conventional
  refinement。
- 贡献 3：**Multimodal V2I Simulator and 5G NR-Oriented Beam-Management Evaluation Framework。**
  基于既有多模态数据资产建立系统级 V2I simulator，在一致的 5G NR-oriented measurement 与资源模型下，
  评价 candidate recall、pilot overhead、effective rate、p05 rate 与 outage。
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
- Chapter 5 描述 Multimodal V2I Simulator、5G NR-oriented beam-management evaluation、条件分层对照
  和 association/tracking 指标；所有比较在一致的 measurement/resource profile 下进行。
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
- 比较 single-beam classification、ranked Top-\(K\) prediction 与 beam-quality/power distribution 三类
  输出；说明排序或分布输出更适合 candidate selection、置信度刻画和后续通信测量决策。
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

本章目的：以通信系统建模为主线，定义局部 V2I 网络、分布式多模态观测、NR-oriented beam
management procedure 及其与 association 的接口。章节先说明 BS 如何通过 SSB、CSI-RS、CSI feedback
和 precoding 服务 VUE，再说明 sensing 如何只作为 candidate measurement 的辅助信息，最后将 sensing
quality、target-to-user association 与 effective communication performance 组织为耦合但非单一标量的
问题表述。

叙述逻辑：先定义 target BS、sensing nodes 与 VUE 的网络关系；随后给出 camera 和 BS-local ISAC
point cloud 的观测模型，并以简洁回波信道、静态 clutter removal 与 point-cloud extraction 说明 ISAC
点云的物理来源；接着定义 NR-oriented timing、SSB/CSI-RS measurement、CSI feedback、RZF precoding
和资源开销；最后按 sensing output、target-to-user association/tracking、rate/resource objectives 三个
层次给出 problem formulation。该章不展开 BEV fusion、network loss、Hungarian implementation 或 IMM
filter recursion，这些算法细节留给 Chapter 4。

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

### 3.3 Communication and Beam Management

写作要点：

#### 3.3.1 Timing and Measurements

- 定义 NR-oriented time hierarchy：\(T_{\mathrm{frame}}=10\) ms、随 numerology 变化的 \(T_{\mathrm{slot}}\)，
  以及 sensing period、SSB periodicity 与 CSI-RS periodicity。具体数值在 Chapter 5 的 frozen radio profile
  中给出，本章仅定义其关系和资源角色。
- 描述 conventional procedure：SSB sweep 用于 initial access/coarse beam identification；CSI-RS 在候选
  CSI beams 上测量，VUE feedback 支持 channel estimation 与 downlink precoding。
- 说明 initial access、handover、association failure 和 sensing unreliability 触发 conventional measurement；
  已可靠关联时可使用 sensing candidate 以减少 CSI-RS measurement width。

#### 3.3.2 Beam Selection and Precoding

- 定义 48-beam SSB codebook、192-beam CSI codebook 与 CSI-to-SSB parent relation；给出 BS--VUE link 的
  per-CSI-beam quality \(g_{b,u,n}(k)\)。
- 严格区分 \(K_{\mathrm{model}}\)、\(K_{\mathrm{bind}}\) 与 \(K_{\mathrm{scan}}\)：它们分别对应 exported
  prediction、association likelihood 和实际 CSI-RS scan budget。
- 定义 VUE 在实测 candidate set 内选择 CSI beam、反馈 CSI，并由 target BS 以 estimated effective channel
  形成 RZF precoder。明确 sensing prediction 不直接指定 service beam。

### 3.4 Problem Formulation

写作要点：

- 开篇说明本文不采用无法反映 protocol events 的单一加权优化；而是定义 sensing、association 和
  communication 三个耦合目标及其依赖关系。

#### 3.4.1 Sensing and Beam Prediction

- 将 multimodal observation 映射为未绑定 detections 与每个 target 的 CSI beam-quality distribution；
  detection 不含 UE identity，distribution 表达 192 CSI beams 的 ranking/likelihood。
- 将 sensing-level objective 表述为 target detection quality 与条件 beam-ranking quality；loss function
  和 network training 留到 Chapter 4。

#### 3.4.2 Association and Tracking

- 定义 persistent mapping \(\pi_{b,n}:\mathcal U_b[n]\rightarrow\mathcal R_b[n]\cup\{\varnothing\}\)，
  其中 \(\mathcal R_b[n]\) 是 perception tracks，空映射表示拒绝 association 或需要 recovery。
- 对 initial/re-association event，使用 measured CSI beam 与 track beam likelihood 构造 cost；SSB-parent
  consistency 定义可行 pair，Hungarian assignment 连同 unmatched option 构成 one-to-one association。
- 用 accepted-association correctness/coverage 说明目标不是强制每个 VUE 绑定，而是提高被接受 association
  的正确概率。IMM 仅维护 track state 与 association persistence；不以视觉特征直接识别 UE。

#### 3.4.3 Rate and Resource Objectives

- 定义 reliability gate 和 candidate policy：可靠且当前 observed association 使用 \(K_{\mathrm{scan}}\)
  sensing candidates；否则使用 conventional refinement。纯 track prediction 不产生正式候选 beam。
- 以实际 CSI-RS measurement 选出的 beam 和 feedback 构造 RZF SINR、raw/effective rate；资源因子涵盖
  SSB、CSI-RS、control 与 data allocation。
- 用 rate--overhead evaluation vector 而非单一标量总结系统目标：detection/beam ranking、accepted
  association accuracy、candidate recall、CSI-RS overhead、effective rate、p05 rate 和 outage。章节结尾
  过渡到 Chapter 4 的具体 BEV fusion、joint learning、IMM update 与 association/gating algorithm。

## Chapter 4: Proposed Multimodal Sensing-Assisted Beam Management Framework

本章目的：介绍本文提出的 BS-centric multimodal and cross-node sensing-assisted beam-alignment
框架，包括局部 BEV 融合、联合 detection--beam-quality learning、未绑定多目标状态估计、
measurement-assisted sensing target-to-user association、可靠度门控候选测量和通信评估接口。

叙述逻辑：先给出感知身份与通信身份分离的整体数据流，再说明跨节点观测如何形成 BEV features、
如何输出未绑定 detections 和 CSI quality distributions；随后说明 conventional measurement 如何建立
target-to-user association、状态估计如何保持其时序一致性，以及可靠度如何决定 candidate
measurement 或 fallback，最后总结算法与复杂度。

### 4.1 Framework Overview

写作要点：

- 给出整体模块：multimodal/cross-node input construction、BEV fusion、joint detection--beam-quality
  learning、unbound perception tracking、measurement-assisted target-to-user association、reliability-gated
  candidate measurement 与 communication evaluation。
- 说明以 BS 为中心输入自身传感器和周围 K 个 SN 数据。
- 明确输出包括未绑定 detected targets、beam-quality distributions、perception tracks、accepted
  UE--track associations、CSI-RS candidates 或 fallback，以及通信评估量。
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
  模糊配对不建立 association，并保留 conventional refinement。
- 明确该模块解决 sensing target-to-user association，而不是由感知网络直接预测 UE identity。

### 4.5 Track-Assisted Association Maintenance

写作要点：

- CV Kalman filter、CT EKF 和 IMM(CV+CT) 等可比较状态估计器维护 per-BS perception-track state；
  运动模型用于预测物理目标状态，而非产生通信身份。
- 新一帧 BEV detections 与 predicted tracks 通过空间创新、运动一致性、detection confidence 和可选的
  beam-distribution consistency 进行 gated one-to-one association。
- 已接受的 UE--track association 随 matched track 更新而持续；未观测、失配或低置信度状态会
  增加 hint age，并触发 conventional measurement 或 re-association。
- 正式候选只来自当前 observed target 的 quality distribution；纯 track prediction 是 association
  maintenance 的状态信息，不替代当前 CSI-RS candidate evidence。

### 4.6 Communication Interface and System-Level Evaluation

写作要点：

- 对于可靠且当前 observed 的 association，quality distribution 导出 fixed/adaptive \(K_{\mathrm{scan}}\)
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

叙述逻辑：先给出数据与协议边界，再按多模态/跨节点互补性、beam-quality ranking、multi-candidate
target-to-user association 及其 tracking、candidate scanning 和系统性能的因果顺序报告结果。评价应显式
追踪 association error、re-association 与 fallback 如何传导到 CSI-RS overhead 和最终用户 rate，最后用
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
- association 对照：无感知、beam direction、beam top-\(K\)、beam-likelihood association；CV、CT
  和 IMM 的状态估计对照应在相同 predicted detections 上进行。
- 系统对照：conventional 4/12-beam refinement、GT ceiling、fixed/adaptive sensing candidates + fallback；
  oracle/GT 仅作诊断或上界，不能替代正式输入。

### 5.3 Layered Metrics and Evidence Discipline

写作要点：

- 感知层报告 mAP、AP@distance、precision/recall、center L2 与 availability，并按天气、可见性、遮挡
  或节点覆盖条件分层，以检验多模态/跨节点互补性。
- Beam-quality 层报告 matched Recall@\(K\)、power ratio、NLL/ECE/Brier 和 coverage；所有条件指标同时
  给出匹配样本比例，避免忽略 detection availability。
- association 层报告 target-to-user binding coverage、diagnostic accuracy、active accuracy、loss/rebind、
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

### 5.5 Results: Target-to-User Association and Tracking

写作要点：

- 报告 conventional-measurement-assisted association 如何在多目标场景中建立 sensing target-to-user
  association，并将 acceptance、rejection 与 fallback 分开统计。
- 比较 CV、CT 与 IMM 等状态估计器在 GT/noisy-GT 诊断和 predicted-detection 正式路径中的差异；
  明确受控诊断不能替代端到端结论。
- 通过错误案例或时间线解释 missed detection、相似 beam likelihood、交汇目标、track fragmentation
  与 re-association 如何影响 identity-consistent beam alignment，并与后续 candidate measurement 和
  fallback 的系统后果相连接。

### 5.6 Results: Reliability-Gated Candidate Scanning and System Trade-off

写作要点：

- 在相同 measurement/resource profile 下比较 conventional、oracle ceiling 与 sensing-assisted fixed/
  adaptive candidates + fallback，报告 candidate recall、CSI-RS overhead、effective rate、p05 rate 与 outage。
- 分析 \(K_{\mathrm{scan}}\)、CSI-RS period、conventional refinement width、SSB accounting 和 Doppler
  的敏感性，重点呈现 rate--overhead Pareto 而非预设净速率增益。
- 将 system outcome 回溯到上游的 beam quality、association correctness、association persistence 和
  hint usage，区分“beam 本身不准”“提示给错 UE”“候选过窄”和“节省资源但速率受损”等原因。

### 5.7 Discussion and Limitations

写作要点：

- 讨论多模态/跨节点感知在何种可见性、遮挡和天气条件下最具互补价值，以及何时 reliability gate
  应更保守地采用 conventional fallback。
- 讨论 target-to-user association 失败对实际 beam alignment 的传播机制，避免将
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
- 研究 missing modality、online adaptation、domain adaptation、measurement calibration 和真实数据验证。
- 研究更稳健的 association confidence、两阶段 fallback 和动态候选策略，以改善 rate--outage 边界。
