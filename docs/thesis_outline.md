# 论文大纲

最后更新：2026-06-22

论文暂定题目：Multimodal Sensing-Assisted User Association and Tracking in Vehicular Networks

本文档是论文写作蓝图，由 `docs/work_brief.md` 推导和更新。大纲只记录当前采用的
论文结构、方法方案和叙述逻辑；方法不确定性、实验空缺和内部待办事项应维护在
`docs/work_brief.md` 中。后续撰写 `chapters/*.tex` 时，应把正文写成可供审稿的
正式英文论文文本，不在正文中保留 TODO、未完成口吻或代码库说明。

## Chapter 1: Introduction

本章目的：介绍车联网高移动场景下 beam management 的背景和问题，说明多模态感知
如何辅助车辆用户的波束选择、目标到用户关联和 tracking，并概括本文贡献。

叙述逻辑：先从 vehicular networks 和高频 V2I communication 的需求切入，再说明
传统 beam sweeping / CSI acquisition 在高移动、多目标和遮挡条件下的开销与不确定性，
最后引出 BS/SN 多视角摄像头和 BS 侧 ISAC point cloud 对 sensing-assisted beam
management 的价值。

### 1.1 Background

写作要点：

- 介绍 vehicular networks、V2I communication、connected mobility 和高频无线系统的需求。
- 说明车辆用户高速移动带来的 beam alignment、beam tracking 和 user association 难题。
- 说明传统 SSB/CSI-RS beam sweeping 和 CSI feedback 在动态道路场景中的开销。
- 引出道路侧基础设施同时具备通信与感知能力，例如 BS camera、distributed sensing nodes
  和 BS-side ISAC sensing。

### 1.2 Challenges

写作要点：

- 讨论 high mobility、rapidly changing link quality、blockage、measurement uncertainty
  和 multi-vehicle association ambiguity。
- 说明 sensing target 与 communication user identity 不天然一致，因此多目标场景下不仅要预测
  beam，还要解决 target-user association。
- 说明持续 full beam sweep 会带来额外开销，而完全依赖历史关联又可能造成 beam mismatch。
- 引出 tracking 对维持 user identity 和 beam selection 时间连续性的作用。

### 1.3 Research Objective

写作要点：

- 明确本文目标：利用 BS-centric multimodal distributed sensing，为车辆用户实现低开销、
  可追踪的 beam management。
- 说明本文核心任务包括 BEV-based vehicle detection、per-target beam power distribution /
  Top-K beam prediction、target-user association、IMM tracking 和系统级通信评估。
- 说明本文采用简化且可解释的 beam management、beam mismatch 和 ZF precoding 评估模型，
  而不是完整 5G NR protocol-stack simulation。

### 1.4 Contributions

写作要点：

- 贡献 1：提出 BS-centric multimodal distributed sensing-assisted beam management framework。
- 贡献 2：设计面向多车辆场景的 target-user association and tracking 流程。
- 贡献 3：构建多模态车联网仿真系统与系统级评估方法。
- 不写具体性能提升数值；定量结论只在 Chapter 5 结果完成后加入。

### 1.5 Thesis Organization

写作要点：

- 简要说明 Chapter 2--6 的内容。
- Chapter 2 梳理相关工作；Chapter 3 定义系统模型；Chapter 4 介绍方法；
  Chapter 5 描述仿真系统和实验评估；Chapter 6 总结和展望。

## Chapter 2: Background and Related Work

本章目的：梳理 sensing-assisted beam management、ISAC predictive beamforming、
BEV / cooperative perception、target-user association 和 tracking 相关研究，明确本文研究缺口。

叙述逻辑：先介绍车联网和 beam management 基础，再按 sensing modalities 与方法类型梳理已有工作，
随后引入分布式感知和 BEV 多模态融合，最后收束到本文的研究定位：多模态分布式 BEV 感知、
target-user association/tracking 和系统级仿真评估在一个闭环中结合。

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

### 2.5 Target-User Association and Tracking in Sensing-Assisted Communication

写作要点：

- 讨论 sensing target、detected vehicle、communication user/UE 之间的身份差异。
- 回顾 multi-candidate beam prediction、transmitter identification 和 object association-based tracking
  相关工作。
- 说明初始 beam spectrum 匹配与后续 tracking 结合的必要性。
- 引出本文的 SSB-based initial association + IMM tracking 方案。

### 2.6 Summary of Research Gap

写作要点：

- 总结已有工作分别覆盖 sensing-aided beam prediction、ISAC tracking/beamforming、BEV fusion、
  cooperative perception 和 multi-candidate identification。
- 指出本文拟连接的三个方面：BS/SN 分布式多视角 camera 与 BS-side ISAC point cloud 的 BEV 融合；
  sensing target 到 communication user 的初始关联和后续 tracking 维护；多模态仿真数据、
  beam labels 与 ZF-based communication metrics 的系统级评估闭环。
- gap 与 Chapter 1 的三条贡献对齐。

## Chapter 3: System Model and Problem Formulation

本章目的：定义道路侧车联网场景、BS/SN/vehicle/user 实体、多模态 sensing observations、
target-user association、tracking state，以及面向 beam management 与系统级评估的通信模型。

叙述逻辑：先定义网络和时间结构，再定义多模态感知观测，然后定义 sensing target、
communication user 和 tracking identity 之间的关系，随后统一给出通信与 beam management 模型，
最后形成本文的 problem formulation。

### 3.1 Network Scenario and Time Structure

写作要点：

- 定义道路场景、BS、distributed sensing nodes、vehicles/users。
- 每个 BS 以自身为中心选择周围 K 个 SN 形成协作感知区域。
- 每个 BS/SN 配置 4 个倾斜下视摄像头，BS 还具备 ISAC point cloud sensing。
- 定义 frame / time slot / decision epoch，并用符号化参数表示场景数量、K 和时间尺度。

### 3.2 Multimodal Sensing Observation Model

写作要点：

- 定义 camera modality：BS camera views 和 K 个 SN 的 camera views。
- 定义 ISAC modality：BS-side ISAC-like point cloud。
- 说明标定、同步和坐标系转换，尤其是如何进入 BEV coordinate frame。
- 定义 detected target 的 BEV 表示，如中心点、位置、尺寸和置信度。

### 3.3 Target-User Association and Tracking State

写作要点：

- 区分 sensing target identity、tracking identity 和 communication user identity。
- 定义 target-user association 变量或映射关系。
- 定义 tracking state：BEV position、velocity 和 motion mode probability。
- 采用 IMM filter 进行状态预测，并将 predicted tracks 与新一帧 BEV detections 关联。

### 3.4 Communication and Beam Management Model

写作要点：

- 定义 BS beam codebook、per-beam power distribution 和 Top-K candidate beams。
- 定义初始接入阶段的 SSB beam sweep power spectrum。
- 说明后续帧的 partial beam measurement / calibration signal 作为校准或恢复机制。
- 定义 beam training overhead。
- 定义 beam mismatch penalty 如何影响 CSI/PMI 或等效信道估计。
- 定义 ZF precoding 下的 effective SINR、spectral efficiency 和 overhead-adjusted throughput。
- 说明该通信模型是可解释的系统级模型，不等同于完整 5G NR 协议栈。

### 3.5 Problem Formulation

写作要点：

- 用自然语言和必要符号总结本文问题：给定多模态 sensing observations 和少量 communication measurements，
  输出 target detection、Top-K beams、target-user association、tracking states，并评估通信收益。
- 采用多目标表述：提高 Top-K beam coverage、association/tracking consistency 和 overhead-adjusted
  throughput，同时降低 beam training overhead。
- 避免把系统写成单一闭式优化问题；重点放在 sensing-assisted beam management workflow 和系统级评价。

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
- 配置一张 framework figure，突出 sensing-to-communication 的闭环。

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

### 4.4 Initial Target-User Association

写作要点：

- 初始接入阶段执行 SSB beam sweep，得到每个 communication user 的 beam power spectrum。
- 将 spectrum 与 detected target 的 predicted beam distribution 进行相似度匹配。
- 匹配代价结合 beam distribution distance、BEV spatial gating 和 detection confidence。
- 通过一对一 matching 建立 sensing target 与 communication user identity 的初始绑定。

### 4.5 IMM Tracking and Beam Maintenance

写作要点：

- IMM filter 维护多运动模型状态，典型模型包括 constant velocity、constant acceleration
  和 turning-motion model。
- 新一帧 BEV detections 与 predicted tracks 通过空间距离、运动一致性和 detection confidence 进行关联。
- Tracking state 用于维持 user identity，并辅助后续 beam selection。
- 当 tracking confidence 下降或 beam mismatch 风险增大时，触发 partial beam measurement 或 re-association。

### 4.6 Communication Interface and System-Level Evaluation

写作要点：

- Top-K beam prediction 传递到通信评估模块。
- 正确 Top-K 覆盖降低 beam training overhead。
- 错误 Top-K 引入 beam mismatch penalty，并影响 ZF SINR。
- 最终输出 spectral efficiency、user throughput、sum throughput 和 overhead-adjusted throughput。

### 4.7 Algorithm Summary and Complexity

写作要点：

- 给出初始接入和后续帧两种流程的伪代码。
- 分析主要计算开销：BEV fusion network、detection/beam heads、association、IMM update、
  communication evaluation。
- 讨论 online feasibility 时保持克制，不写未经测量的实时性能结论。

## Chapter 5: Multimodal Simulation System and Experimental Evaluation

本章目的：描述多模态车联网仿真系统，说明如何生成 camera observations、ISAC-like point clouds、
vehicle trajectories、beam labels 和 communication channels，并通过实验评估本文方法对 beam prediction、
association、tracking 和通信吞吐量的影响。

叙述逻辑：先介绍仿真系统和数据生成链路，再定义 baselines 和 metrics，然后展示主实验和消融实验，
最后讨论 limitations。独立 sensitivity / robustness section 不再设置，相关因素可作为 ablation
或 discussion 的一部分。

### 5.1 Multimodal Simulation System

写作要点：

- 介绍仿真链路：CARLA 道路交通和传感器数据生成，Blender/Mitsuba 逐帧场景重建，Sionna RT
  多径传播和信道生成。
- 将仿真系统描述为学术方法与数据生成框架，而不是代码库或脚本说明。
- 说明输出数据类型：camera images、ISAC-like point clouds、vehicle poses、trajectories、
  channel coefficients、path parameters 和 beam labels。
- 说明该系统服务于本文第三条贡献。

### 5.2 Scenario and Dataset Construction

写作要点：

- 描述道路场景、BS/SN 布局、车辆数量、车辆轨迹、天气/光照和帧率。
- 说明每个 BS/SN 的 camera placement 和 BS-side ISAC-like point cloud 生成方式。
- 说明 beam codebook、ray tracing frequency、antenna configuration 和 channel storage。
- 说明训练/验证/测试划分。

### 5.3 Baselines

写作要点：

- Communication-only full beam sweep。
- Communication-only partial sweep。
- Camera-only BEV beam prediction。
- ISAC-only beam prediction。
- Single-site sensing：仅服务 BS 传感器。
- No-tracking variant：逐帧独立检测和 beam prediction。
- Proposed multimodal distributed sensing-assisted framework。

### 5.4 Evaluation Metrics

写作要点：

- 感知指标：detection accuracy / mAP、BEV localization error。
- 关联与 tracking 指标：target-user association accuracy、tracking identity consistency、
  tracking prediction error。
- Beam management 指标：Top-1 accuracy、Top-K accuracy、beam power prediction error、
  beam training overhead reduction。
- 通信指标：effective SINR under ZF precoding、spectral efficiency、user throughput、
  sum throughput、overhead-adjusted throughput。

### 5.5 Main Results

写作要点：

- 结果待补：展示 proposed framework 相对 baselines 的主要结果。
- 结果分别覆盖 detection/beam prediction、association/tracking 和 communication performance。
- 定量结论必须由图表和实验数值支撑。

### 5.6 Ablation Studies

写作要点：

- 去除 ISAC point cloud，仅保留 camera modality。
- 去除 SN camera views，仅使用 BS 侧传感器。
- 改变协作 SN 数量 K。
- 去除 IMM tracking。
- 比较 full sweep、partial measurement 和 sensing-assisted Top-K beam selection。
- 可纳入 Top-K 取值、车辆密度、遮挡、感知噪声或 beam mismatch penalty 等少量鲁棒性因素。

### 5.7 Discussion

写作要点：

- 解释多模态分布式感知在哪些场景下更有优势。
- 讨论 target-user association 或 tracking 失败时对通信性能的影响。
- 说明仿真系统与真实 5G NR 协议栈之间的差距。
- 说明 limitations，例如仿真域偏差、传感器同步误差、beam mismatch 模型简化等。

## Chapter 6: Conclusion and Future Work

本章目的：总结本文完成的工作、实验支持的发现和主要限制，并提出未来扩展方向。

叙述逻辑：先回到研究问题，再概括三个贡献对应的完成内容，随后总结由实验支持的结论，
最后讨论 future work。结论章不引入正文没有证明的新 claim。

### 6.1 Conclusion

写作要点：

- 概括本文针对车联网 beam management 提出的多模态分布式感知框架。
- 概括 target-user association and tracking 流程。
- 概括多模态仿真系统和系统级评估方法。
- 结果待补：只总结 Chapter 5 已经支持的发现。

### 6.2 Limitations

写作要点：

- 说明仿真环境和真实部署之间可能存在 domain gap。
- 说明本文通信评估是简化模型，不是完整 5G NR stack。
- 说明 sensing noise、calibration error、missing modality、occlusion 和 tracking failure 对系统的潜在影响。

### 6.3 Future Work

写作要点：

- 扩展到更真实的多 BS / 多 SN 网络和更复杂道路拓扑。
- 引入更完善的 5G NR protocol-level simulation。
- 研究 missing modality、online adaptation、domain adaptation 和真实数据验证。
- 扩展到 cooperative multi-BS beam management 或 handover decision。
