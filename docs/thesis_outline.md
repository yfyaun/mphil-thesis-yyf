# 论文大纲

最后更新：2026-06-22

论文暂定题目：Multimodal Sensing-Assisted User Association and Tracking in Vehicular Networks

本文档是论文写作蓝图，应基于 `docs/work_brief.md` 定期更新。后续撰写
`chapters/*.tex` 时，应优先依据本文档中的章节结构、写作要点、叙述逻辑、
证据需求和状态标记。

状态标记：

- `稳定`：内容已经足够明确，可以进入正式英文论文写作。
- `草稿`：可作为写作基础，但后续可能调整。
- `缺证据`：需要实验结果、文献引用、baseline、数值或更清晰的方法细节。
- `不稳定`：方法、系统模型、研究问题或贡献尚未定型，不应写成最终结论。

## Chapter 1: Introduction

本章目的：介绍车联网高移动场景下 beam management 的背景和问题，说明多模态感知
为什么可以辅助车辆用户的波束选择、目标到用户关联和 tracking，并概括本文的候选贡献。

叙述逻辑：先从 vehicular networks 和 mmWave/high-frequency communication 的应用需求切入，
再说明传统 beam sweeping / CSI acquisition 在高移动、多目标和遮挡条件下的开销与不确定性，
最后引出 BS/SN 多视角摄像头和 BS 侧 ISAC point cloud 对 sensing-assisted beam management
的潜在价值。

### 1.1 Background

写作要点：

- 介绍 vehicular networks、V2I communication、connected mobility 和未来高频无线系统的需求。
- 说明车辆用户高速移动会带来 beam alignment、beam tracking 和 user association 难题。
- 说明传统 SSB/CSI-RS beam sweeping 和 CSI feedback 在动态道路场景中的开销。
- 引出道路侧基础设施可以同时具备通信与感知能力，例如 BS camera、distributed sensing nodes
  和 BS-side ISAC sensing。

需要证据：

- 车辆网络、mmWave/THz beam management、beam sweeping overhead 的基础文献。
- vision/radar/LiDAR/ISAC sensing-assisted beam prediction 的代表文献。

当前状态：缺证据

### 1.2 Challenges

写作要点：

- 讨论 high mobility、rapidly changing link quality、blockage、measurement uncertainty
  和 multi-vehicle association ambiguity。
- 说明 sensing target 与 communication user identity 不天然一致，因此多目标场景下不仅要预测
  beam，还要解决 target-user association。
- 说明后续帧如果持续 full beam sweep，会带来额外开销；如果完全不测量，又可能造成 beam mismatch。
- 引出需要 tracking 来维持 user identity 和 beam selection 的时间连续性。

需要证据：

- 多目标 V2I beam prediction、transmitter identification、tracking-assisted beam prediction
  和 ISAC predictive beamforming 文献。

当前状态：缺证据

### 1.3 Research Objective

写作要点：

- 明确本文目标：利用 BS-centric multimodal distributed sensing，为车辆用户实现低开销、可追踪的
  beam management。
- 说明本文核心任务包括 BEV-based vehicle detection、per-target beam power distribution /
  Top-K beam prediction、target-user association、IMM tracking 和系统级通信评估。
- 说明本文不追求完整 5G NR stack 仿真，而采用简化且可解释的 beam management、beam mismatch
  和 ZF precoding 评估模型。

需要证据：

- 系统模型、算法流程和仿真系统实现需要进一步固定。

当前状态：草稿

### 1.4 Contributions

写作要点：

- 按 `docs/work_brief.md` 中的三条候选贡献撰写，不夸大为已验证结论。
- 贡献 1：BS-centric multimodal distributed sensing-assisted beam management framework。
- 贡献 2：target-user association and tracking 流程。
- 贡献 3：多模态车联网仿真系统与系统级评估方法。
- 不写具体性能提升数值，除非后续实验已经记录在 `docs/work_brief.md`。

需要证据：

- 完成文献差异分析，确认本文贡献相对已有工作的位置。
- 完成实验后，用结果支撑各贡献。

当前状态：缺证据

### 1.5 Thesis Organization

写作要点：

- 简要说明 Chapter 2--6 的内容。
- Chapter 2 梳理相关工作；Chapter 3 定义系统模型；Chapter 4 介绍方法；
  Chapter 5 描述仿真系统和实验评估；Chapter 6 总结和展望。

需要证据：

- 无特殊证据需求，待章节标题稳定后同步。

当前状态：稳定

## Chapter 2: Background and Related Work

本章目的：梳理 sensing-assisted beam management、ISAC predictive beamforming、
BEV / cooperative perception、target-user association 和 tracking 相关研究，明确本文的研究缺口。

叙述逻辑：先介绍车联网和 beam management 基础，再按 sensing modalities 与方法类型梳理已有工作，
随后引入分布式感知和 BEV 多模态融合，最后收束到本文要解决的 gap：多模态分布式 BEV 感知、
target-user association/tracking 和系统级仿真评估尚未在一个闭环中充分结合。

### 2.1 Vehicular Networks and Beam Management

写作要点：

- 回顾 V2I / vehicular networks 中高频通信的 beam alignment、beam selection、beam tracking
  和 handover 问题。
- 介绍 beam codebook、SSB beam sweeping、CSI/PMI acquisition 和 beam training overhead。
- 说明 beam management 与 spectral efficiency / throughput 的关系。

需要证据：

- mmWave / vehicular beam management 基础文献。
- 5G NR beam management 和 SSB/CSI-RS 相关参考。

当前状态：缺证据

### 2.2 Sensing-Aided Beam Prediction

写作要点：

- 按 sensing modality 组织：camera-based、position/GPS-aided、radar-aided、LiDAR-aided、
  multimodal sensing-aided beam prediction。
- 介绍 DeepSense 6G 系列工作、Top-K beam accuracy、beam power loss 和 overhead reduction
  等常用指标。
- 说明现有工作多关注 beam index prediction，对 sensing target 与 communication user identity
  的长期维护考虑不足。

需要证据：

- 已下载文献中的 vision-position、radar-aided、LiDAR-aided、camera-based multi-candidate、
  multimodal transformer 和 BEV-fusion beam prediction 论文。

当前状态：缺证据

### 2.3 ISAC Predictive Beamforming and Tracking

写作要点：

- 回顾 DFRC/ISAC 中利用 radar echo、historical channel 或 reflected signal samples 做车辆状态预测
  和 predictive beamforming 的工作。
- 介绍 EKF、Bayesian/message passing、CLSTM、Transformer 或 end-to-end predictive beamforming。
- 说明 ISAC 文献通常重视 channel/beamforming/rate 优化，但较少结合 camera-based multi-object
  perception 和 target-user association。

需要证据：

- Radar-assisted predictive beamforming、Bayesian predictive beamforming、ISAC extended target、
  learning-based predictive beamforming 等文献。

当前状态：缺证据

### 2.4 BEV Multimodal Fusion and Cooperative Perception

写作要点：

- 介绍 CenterNet / CenterTrack 对 point-based detection 和 tracking 的启发。
- 介绍 Lift-Splat-Shoot、BEVFusion 等 BEV 表征方法，说明 BEV 对多视角图像和点云融合的意义。
- 介绍 V2X cooperative perception，说明多节点协作感知对覆盖范围、遮挡和视角互补的帮助。
- 连接到本文 BS/SN 多视角 camera 与 BS-side ISAC point cloud 的 BEV 融合设计。

需要证据：

- CenterNet、CenterTrack、Lift-Splat-Shoot、BEVFusion、V2X-ViT 等文献。

当前状态：缺证据

### 2.5 Target-User Association and Tracking in Sensing-Assisted Communication

写作要点：

- 讨论 sensing target、detected vehicle、communication user/UE 之间的身份差异。
- 回顾 multi-candidate beam prediction、transmitter identification 和 object association-based tracking
  相关工作。
- 说明初始 beam spectrum 匹配与后续 tracking 结合的必要性。
- 引出本文的 SSB-based initial association + IMM tracking 方案。

需要证据：

- Multi-candidate camera-based beam prediction、distributed sensing-aided networks、tracking-by-detection
  和 IMM/filtering 相关文献。

当前状态：缺证据

### 2.6 Summary of Research Gap

写作要点：

- 总结已有工作分别覆盖了 sensing-aided beam prediction、ISAC tracking/beamforming、BEV fusion、
  cooperative perception 和 multi-candidate identification。
- 指出本文拟连接的缺口：
  - BS/SN 分布式多视角 camera 与 BS-side ISAC point cloud 在 BEV 中统一服务 beam management。
  - 从 sensing target 到 communication user 的初始关联和后续 tracking 维护。
  - 多模态仿真数据、beam labels、ZF-based communication metrics 的系统级评估闭环。
- gap 必须与 Chapter 1 的三条贡献对齐。

需要证据：

- 完成文献对比表后再写成正式正文。

当前状态：缺证据

## Chapter 3: System Model and Problem Formulation

本章目的：定义道路侧车联网场景、BS/SN/vehicle/user 实体、多模态 sensing observations、
communication beam measurements、target-user association、tracking state 和通信性能抽象。

叙述逻辑：先定义网络和时间结构，再定义感知与通信观测，然后定义 tracking 和 association 变量，
最后给出本文要解决的 beam management / system evaluation 问题。

### 3.1 Network Scenario and Time Structure

写作要点：

- 定义道路场景、BS、distributed sensing nodes、vehicles/users。
- 说明每个 BS 以自身为中心选择周围 K 个 SN 形成协作感知区域。
- 说明每个 BS/SN 配置 4 个倾斜下视摄像头，BS 还具备 ISAC point cloud sensing。
- 定义 frame / time slot / decision epoch。

需要证据：

- 需要确定最终仿真场景数量、BS/SN 布局、K 的默认值和时间尺度。

当前状态：草稿

### 3.2 Multimodal Sensing Observation Model

写作要点：

- 定义 camera modality：BS camera views 和 K 个 SN 的 camera views。
- 定义 ISAC modality：BS-side ISAC-like point cloud。
- 说明标定、同步和坐标系转换，尤其是如何进入 BEV coordinate frame。
- 定义 detected target 的 BEV 表示，如中心点、位置、尺寸、置信度等。

需要证据：

- 需要明确 BEV 坐标范围、分辨率、camera projection / point-cloud encoding 细节。

当前状态：不稳定

### 3.3 Communication and Beam Model

写作要点：

- 定义 BS beam codebook 和 per-beam power distribution。
- 定义 Top-K candidate beams。
- 定义初始接入阶段的 SSB beam sweep power spectrum。
- 说明后续帧的 partial beam measurement / calibration signal 只作为校准或恢复机制。

需要证据：

- 需要确定 codebook size、beam label 生成方式、SSB/measurement 抽象。

当前状态：不稳定

### 3.4 Target-User Association and Tracking State

写作要点：

- 区分 sensing target identity、tracking identity 和 communication user identity。
- 定义 target-user association 变量或映射关系。
- 定义 tracking state：BEV position、velocity、motion mode probability 等。
- 说明 IMM filter 的状态预测与 BEV detection association 的关系。

需要证据：

- 需要确定 association cost、matching constraints、IMM motion models 和失配恢复规则。

当前状态：不稳定

### 3.5 Communication Performance Abstraction

写作要点：

- 定义 beam training overhead。
- 定义 beam mismatch penalty 如何影响 CSI/PMI 或等效信道估计。
- 定义 ZF precoding 下的 effective SINR、spectral efficiency 和 overhead-adjusted throughput。
- 说明该模型是可解释的系统级抽象，不等同于完整 5G NR 协议栈。

需要证据：

- 需要固定 beam mismatch 到 SINR degradation 的数学形式。
- 需要确定 overhead accounting 的时间/资源单位。

当前状态：不稳定

### 3.6 Problem Statement

写作要点：

- 用自然语言和必要符号总结本文问题：给定多模态 sensing observations 和少量 communication measurements，
  输出 target detection、Top-K beams、target-user association、tracking states，并评估通信收益。
- 如果最终需要优化目标，可采用多目标表述：提高 Top-K beam accuracy 和 association/tracking accuracy，
  同时降低 beam training overhead 并提升 overhead-adjusted throughput。
- 避免在方法和实验未完全固定前写成过强的闭式优化问题。

需要证据：

- 需要在方法稳定后补充符号表和正式 formulation。

当前状态：草稿

## Chapter 4: Proposed Multimodal Sensing-Assisted Beam Management Framework

本章目的：介绍本文提出的 BS-centric multimodal distributed sensing-assisted beam management
框架，包括 BEV 多模态融合、目标检测、beam prediction、target-user association、IMM tracking
和通信评估接口。

叙述逻辑：先给整体框架图和数据流，再按模块说明 sensing input 如何变成 BEV features，
BEV features 如何产生 detections 和 per-target beam distribution，初始 SSB spectrum 如何建立用户关联，
后续 tracking 如何维持关联，最后说明算法流程和复杂度。

### 4.1 Framework Overview

写作要点：

- 给出整体模块：multimodal input construction、BEV fusion network、detection head、beam prediction head、
  initial target-user association、IMM tracking、communication evaluation。
- 说明以 BS 为中心输入自身传感器和周围 K 个 SN 数据。
- 说明输出包括 detected targets、Top-K beams、user identities、tracking states 和通信评估量。
- 建议配一张 framework figure。

需要证据：

- 需要最终系统框架图和模块接口。

当前状态：草稿

### 4.2 BEV-Based Multimodal Fusion

写作要点：

- 说明多视角 camera features 如何投影/编码到 BEV。
- 说明 BS-side ISAC point cloud 如何编码到 BEV。
- 说明多站点、多模态特征如何融合。
- 讨论时间同步、空间标定、传感器覆盖差异和 missing / noisy observations。

需要证据：

- 需要明确网络结构、输入尺寸、BEV grid、fusion strategy 和训练标签。

当前状态：不稳定

### 4.3 Vehicle Detection and Per-Target Beam Prediction

写作要点：

- 说明 CenterNet-like detection head 如何从 BEV feature map 输出 vehicle centers / attributes。
- 说明 beam prediction head 如何为每个 detected target 输出 per-beam power distribution。
- 说明 Top-K beams 如何从分布中选出。
- 说明 detection loss、beam distribution loss 和训练标签生成思路。

需要证据：

- 需要确定 loss function、beam label、正负样本匹配和 beam power normalization。

当前状态：不稳定

### 4.4 Initial Target-User Association

写作要点：

- 说明初始接入阶段执行 SSB beam sweep，得到每个 communication user 的 beam power spectrum。
- 说明如何将 spectrum 与 detected target 的 predicted beam distribution 进行相似度匹配。
- 可考虑 beam distribution similarity、BEV spatial prior、detection confidence 等匹配项。
- 说明匹配输出是 sensing target 与 communication user identity 的初始绑定。

需要证据：

- 需要确定 association cost、matching algorithm 和多用户冲突处理。

当前状态：不稳定

### 4.5 IMM Tracking and Beam Maintenance

写作要点：

- 说明 IMM filter 的运动模型组合和状态预测。
- 说明新一帧 BEV detections 与 predicted tracks 的 data association。
- 说明 tracking state 如何辅助后续 beam selection 和减少 full beam sweep。
- 说明何时触发 partial beam measurement 或 re-association。

需要证据：

- 需要确定 IMM 参数、gating threshold、association rule 和 failure recovery。

当前状态：不稳定

### 4.6 Communication Interface and System-Level Evaluation

写作要点：

- 说明 Top-K beam prediction 如何传递到通信评估模块。
- 说明正确 Top-K 覆盖如何降低 beam training overhead。
- 说明错误 Top-K 如何引入 beam mismatch penalty 并影响 ZF SINR。
- 说明最终输出 spectral efficiency、user throughput、sum throughput 和 overhead-adjusted throughput。

需要证据：

- 需要固定 ZF precoding 和 mismatch penalty 的数学模型。

当前状态：不稳定

### 4.7 Algorithm Summary and Complexity

写作要点：

- 方法稳定后给出伪代码，包含初始接入和后续帧两种流程。
- 分析主要计算开销：BEV fusion network、detection/beam heads、association、IMM update、
  communication evaluation。
- 讨论 online feasibility，但不夸大实时性能。

需要证据：

- 需要实现后统计模型复杂度、运行时间或至少给出理论复杂度。

当前状态：缺证据

## Chapter 5: Multimodal Simulation System and Experimental Evaluation

本章目的：描述多模态车联网仿真系统，说明如何生成 camera observations、ISAC-like point clouds、
vehicle trajectories、beam labels 和 communication channels，并通过实验评估本文方法对 beam prediction、
association、tracking 和通信吞吐量的影响。

叙述逻辑：先介绍仿真系统和数据生成链路，再定义 baselines 和 metrics，然后展示主实验、消融实验、
敏感性分析和系统级通信评估，最后诚实讨论 limitations。

### 5.1 Multimodal Simulation System

写作要点：

- 介绍仿真链路：CARLA 道路交通和传感器数据生成，Blender/Mitsuba 逐帧场景重建，Sionna RT
  多径传播和信道生成。
- 说明仿真系统如何参考 `Multi-modal-beam-twin` / `Multimodal-Wireless`。
- 说明输出数据类型：camera images、depth/LiDAR/radar 或 ISAC-like point clouds、vehicle poses、
  trajectories、scene YAML、channel coefficients、path parameters、beam labels。
- 说明该系统服务于本文第三条贡献。

需要证据：

- 需要确定最终复用/改造的仿真代码版本、场景配置和数据格式。

当前状态：草稿

### 5.2 Scenario and Dataset Construction

写作要点：

- 描述道路场景、BS/SN 布局、车辆数量、车辆轨迹、天气/光照和帧率。
- 说明每个 BS/SN 的 camera placement 和 BS-side ISAC-like point cloud 生成方式。
- 说明 beam codebook、ray tracing frequency、antenna configuration 和 channel storage。
- 说明训练/验证/测试划分。

需要证据：

- 需要最终数据集规模、场景数量、参数表和可复现配置。

当前状态：缺证据

### 5.3 Baselines

写作要点：

- Communication-only full beam sweep。
- Communication-only partial sweep。
- Camera-only BEV beam prediction。
- ISAC-only beam prediction。
- Single-site sensing：仅服务 BS 传感器。
- No-tracking variant：逐帧独立检测和 beam prediction。
- Proposed multimodal distributed sensing-assisted framework。

需要证据：

- 需要实现或明确每个 baseline 的公平输入、训练方式和评估设置。

当前状态：缺证据

### 5.4 Evaluation Metrics

写作要点：

- 感知指标：detection accuracy / mAP、BEV localization error。
- 关联与 tracking 指标：target-user association accuracy、tracking identity consistency、
  tracking prediction error。
- beam management 指标：Top-1 accuracy、Top-K accuracy、beam power prediction error、
  beam training overhead reduction。
- 通信指标：effective SINR under ZF precoding、spectral efficiency、user throughput、
  sum throughput、overhead-adjusted throughput。

需要证据：

- 需要确定每个 metric 的精确定义和计算脚本。

当前状态：草稿

### 5.5 Main Results

写作要点：

- 展示 proposed framework 相对 baselines 的主要结果。
- 结果应分别覆盖 detection/beam prediction、association/tracking 和 communication performance。
- 不在没有数据的情况下写性能提升结论。

需要证据：

- 需要完整实验结果、图表和统计分析。

当前状态：缺证据

### 5.6 Ablation Studies

写作要点：

- 去除 ISAC point cloud，仅保留 camera modality。
- 去除 SN camera views，仅使用 BS 侧传感器。
- 改变协作 SN 数量 K。
- 去除 IMM tracking。
- 比较 full sweep、partial measurement 和 sensing-assisted Top-K beam selection。

需要证据：

- 需要消融实验结果和原因分析。

当前状态：缺证据

### 5.7 Sensitivity and Robustness Analysis

写作要点：

- 分析 Top-K 中 K 的取值。
- 分析车辆密度、速度、遮挡、感知噪声、camera calibration / synchronization error。
- 分析 ISAC-like point cloud 稀疏度、beam codebook size 和 beam mismatch penalty 强度。

需要证据：

- 需要敏感性实验结果。

当前状态：缺证据

### 5.8 Discussion

写作要点：

- 解释在哪些场景下多模态分布式感知更有优势。
- 讨论 target-user association 或 tracking 失败时对通信性能的影响。
- 说明仿真系统与真实 5G NR 协议栈之间的差距。
- 诚实说明 limitations，例如仿真域偏差、传感器同步误差、beam mismatch 模型简化等。

需要证据：

- 需要基于实验结果形成具体讨论。

当前状态：缺证据

## Chapter 6: Conclusion and Future Work

本章目的：总结本文完成的工作、实验支持的发现和主要限制，并提出未来扩展方向。

叙述逻辑：先回到研究问题，再概括三个贡献对应的完成内容，随后总结由实验支持的结论，
最后讨论 future work。不得引入正文没有证明的新 claim。

### 6.1 Conclusion

写作要点：

- 概括本文针对车联网 beam management 提出的多模态分布式感知框架。
- 概括 target-user association and tracking 流程。
- 概括多模态仿真系统和系统级评估方法。
- 只总结实验已经支持的发现，不写未经验证的性能结论。

需要证据：

- 需要 Chapter 5 完成后才能正式写作。

当前状态：缺证据

### 6.2 Limitations

写作要点：

- 说明仿真环境和真实部署之间可能存在 domain gap。
- 说明本文通信评估是简化模型，不是完整 5G NR stack。
- 说明 sensing noise、calibration error、missing modality、occlusion 和 tracking failure 对系统的潜在影响。

需要证据：

- 需要实验和消融结果支撑具体限制。

当前状态：缺证据

### 6.3 Future Work

写作要点：

- 扩展到更真实的多 BS / 多 SN 网络和更复杂道路拓扑。
- 引入更完善的 5G NR protocol-level simulation。
- 研究 missing modality、online adaptation、domain adaptation 和真实数据验证。
- 扩展到 cooperative multi-BS beam management 或 handover decision。

需要证据：

- 不需要实验支撑，但应与正文 limitations 自然对应。

当前状态：草稿
