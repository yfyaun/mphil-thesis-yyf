# 工作说明

最后更新：2026-06-22

论文暂定题目：Multimodal Sensing-Assisted User Association and Tracking in Vehicular Networks

本文档是当前研究工作的事实源，用于记录“目前这项工作到底在做什么”。它可以
随着实验、算法设计和论文定位的变化持续更新。后续论文正文应依据本文档和
`docs/thesis_outline.md` 撰写，不应脱离本文档自行扩展未经确认的贡献或结论。

## 1. 研究背景与动机

本论文关注车联网场景下的多模态感知辅助通信问题。车辆用户在道路环境中高速移动，
其相对于基站的角度、距离和遮挡状态会快速变化，导致毫米波或高频通信中的波束管理、
用户关联和链路维护面临较大开销与不确定性。传统通信系统主要依赖 beam sweeping、
SSB/CSI-RS 测量和后续 CSI 反馈进行波束选择与预编码设计，但在高移动性场景下，完整
beam sweep 会消耗较多时频资源，且测量结果可能由于车辆运动、遮挡和环境变化而迅速失效。

道路侧基础设施通常具备较强的环境感知能力。例如，BS 可以配置多视角摄像头并通过
ISAC 双功能波形获得感知点云，分布式 sensing nodes 也可以通过多视角摄像头提供额外
空间观测。这些感知信息能够在通信测量之外提供车辆位置、运动状态、道路几何关系和
潜在遮挡信息。因此，本研究希望利用多模态分布式感知信息预测车辆用户的候选通信波束，
并通过目标检测、target-user association 和 tracking 降低后续 beam management 开销，
最终改善有效通信吞吐量。

本工作将多模态感知与通信过程耦合起来：感知网络负责从多视角图像和 ISAC 点云中识别
车辆目标并预测其 beam power distribution / Top-K beams；通信测量用于初始接入阶段
建立 sensing target 与通信 user identity 的关联；后续帧通过 tracking 维持该关联并
减少完整 beam sweep 的频率。论文中的通信性能评估采用简化但可解释的 5G beam
management 与 ZF precoding 抽象，而不追求完整 5G NR 协议栈仿真。

## 2. 关注的问题

本论文拟解决的问题是：在车联网场景中，如何利用 BS 与分布式 sensing nodes 的多模态
观测，为车辆用户进行低开销、可追踪的 beam management，并将 sensing-assisted beam
prediction 的准确性转化为通信系统层面的性能收益。

系统输入包括：

- BS 侧多视角摄像头图像。每个 BS 配置 4 个倾斜下视摄像头，用于覆盖道路区域。
- 分布式 sensing nodes 侧多视角摄像头图像。每个 SN 配置 4 个倾斜下视摄像头。
- BS 侧 ISAC sensing point cloud，由双功能通信-感知波形或等价 ISAC 感知过程获得。
- 通信侧 beam measurements，包括初始接入阶段的 SSB beam sweep power spectrum，以及
  后续必要时的少量 beam measurement / calibration signal。

系统输出包括：

- 道路场景中的车辆目标检测结果及其 BEV 空间位置。
- 每个 detected target 对应的 per-beam power distribution，并由此得到 Top-K candidate beams。
- sensing target 与通信 user identity 的关联关系。
- 每个已关联车辆用户的 tracking state，包括位置、速度和运动模型状态。
- 面向通信评估的 beam management 开销、有效 SINR、spectral efficiency 和 throughput。

决策过程按帧或时间槽运行。初始接入时，系统允许较完整的 SSB beam sweep，并将通信测量
与 sensing network 输出进行匹配，完成 target-user association。后续帧中，系统主要依赖
多模态感知和 tracking 预测维持用户状态，只在必要时进行少量 beam measurement，从而降低
beam training overhead。

本文关注的核心问题包括：

- 多模态分布式传感器如何在统一 BEV 表征中融合图像与 ISAC 点云。
- 如何从 BEV 特征中同时完成车辆目标检测和 per-target beam prediction。
- 如何利用初始 SSB beam sweep power spectrum 建立 target-user association。
- 如何利用 IMM tracking 在后续帧中维持用户身份并辅助 beam selection。
- Top-K beam prediction 的正确或错误如何影响后续 CSI/PMI 抽象、ZF precoding SINR 和
  最终吞吐量。

## 3. 核心创新点 / 贡献

以下贡献为当前论文的候选表述，后续应根据文献调研、系统实现和实验结果继续收敛。
贡献表述应保持克制，不在缺少实验支撑时给出具体性能提升结论。

1. 提出一种面向车联网波束管理的 BS-centric multimodal distributed sensing-assisted
   framework。该框架以服务 BS 为中心，融合 BS/SN 多视角摄像头与 BS 侧 ISAC point cloud，
   在统一 BEV 表征中进行车辆目标检测，并为每个 detected target 预测 per-beam power
   distribution / Top-K candidate beams。

2. 设计一种面向多车辆场景的 target-user association and tracking 流程。初始接入阶段
   利用 SSB beam sweep power spectrum 与感知网络预测的 per-target beam distribution
   建立 sensing target 与 communication user identity 的关联；后续帧通过 IMM tracking
   与 BEV detection association 维护用户身份和 beam selection 连续性，从而减少完整
   beam sweep 的使用频率。

3. 构建一种多模态车联网仿真系统与系统级评估方法。仿真系统参考 `Multi-modal-beam-twin`
   / `Multimodal-Wireless` 类流程，将 CARLA 道路交通与多传感器数据生成、Blender/Mitsuba
   场景重建、Sionna ray tracing 信道生成连接起来，形成 camera observations、ISAC-like
   point clouds、vehicle trajectories、beam power labels 和通信信道数据。基于该数据，
   系统级评估同时考虑 Top-K beam prediction、target-user association、tracking error、
   beam training overhead、beam mismatch penalty、ZF precoding SINR、spectral efficiency
   和 overhead-adjusted throughput。

## 4. 系统模型

### 4.1 网络实体与拓扑

考虑一个道路侧车联网场景，网络中包括多个 BS、若干分布式 sensing nodes，以及道路上
移动的车辆用户。BS 同时承担通信服务和感知信息采集任务；SN 不直接提供通信服务，主要
提供额外视觉感知覆盖。每个 BS 以自身为中心构建局部协作感知区域，并选取周围 K 个 SN
作为协作 sensing nodes。K 表示每个 BS 使用的邻近 SN 数量，可在实验中作为系统参数。

每个 BS 和 SN 均配备 4 个倾斜下视摄像头，用于从多个视角观测道路区域。BS 还通过 ISAC
能力获取局部感知点云。对于每个 BS，系统输入由该 BS 自身的 camera views、该 BS 的 ISAC
point cloud，以及周围 K 个 SN 的 camera views 组成。

### 4.2 车辆用户与目标模型

道路中的每个通信用户由一个车辆目标承载。感知系统首先在 BEV 空间中检测车辆目标，
得到目标位置、尺寸或中心点等表示；通信系统则通过 beam measurements 观测 user 与 BS
之间的波束响应。由于 sensing target identity 和 communication user identity 不天然
一致，系统需要在初始接入和后续跟踪过程中维护 target-user association。

### 4.3 通信与波束模型

每个 BS 配置一个离散 beam codebook。对车辆用户而言，不同 candidate beams 对应不同
接收功率或有效信道增益。感知神经网络为每个 detected target 输出一个 per-beam power
distribution，表示该目标在当前 BS codebook 下的 beam quality 估计。Top-K candidate
beams 由该分布中排名最高的 K 个 beam 得到。

初始接入阶段，BS 通过 SSB beam sweep 获得 user 的 beam power spectrum。该 spectrum
与 sensing network 为 detected targets 预测的 beam distribution 进行匹配，用于确定
哪个 sensing target 对应哪个 communication user。后续帧中，系统优先使用 sensing-assisted
Top-K beam prediction 与 tracking state 进行 beam management，仅在校准或失配恢复时使用
少量 beam measurement。

### 4.4 多模态感知模型

感知输入包含两类模态：

- Camera modality：来自 BS 与周围 K 个 SN 的多视角图像，每个站点包含 4 个倾斜下视摄像头。
- ISAC modality：来自 BS 的 sensing point cloud，由双功能波形或等价 ISAC 感知过程得到。

不同站点和模态的观测被投影或编码到统一 BEV 表征中。BEV 表征用于对齐不同摄像头视角、
不同 sensing node 的空间信息，以及 BS 侧 ISAC 点云。神经网络基于 BEV feature map 同时
执行车辆目标检测和 beam prediction。

### 4.5 Tracking 状态

对于已关联的车辆用户，系统维护 tracking state。状态至少包括 BEV 位置和速度，后续可以
扩展为加速度、航向角或运动模式概率。tracking module 采用 IMM filter，对不同车辆运动
模式进行融合预测。IMM 预测状态与后续帧的 BEV detection 进行 data association，以维持
车辆用户身份并辅助 beam prediction 的时间连续性。

### 4.6 通信性能抽象

本文采用简化通信模型评估 sensing-assisted beam management 对通信性能的影响。若 Top-K
beam prediction 覆盖真实有效 beam，则系统可以减少 beam sweep 开销，并将节省的资源用于
数据传输。若 Top-K beam prediction 错误，则后续 CSI/PMI 抽象会受到 beam mismatch 影响，
导致 ZF precoding 所使用的有效信道方向或增益不准确，从而降低 SINR。频谱效率可基于
ZF 后的 SINR 计算，吞吐量进一步考虑 beam training overhead 后得到。

## 5. 算法与整体流程框架

本论文采用一个以 BS 为中心的多模态感知辅助 beam management 框架。整体流程包括五个阶段。

### 5.1 多模态输入构建

对每个 BS，在每个时间帧收集以下输入：

- 该 BS 的 4 个 camera views。
- 周围 K 个 SN 的 camera views，每个 SN 包含 4 个摄像头。
- 该 BS 的 ISAC sensing point cloud。
- 初始接入或校准阶段可用的 communication beam measurements。

输入数据首先进行时间同步和空间标定，随后进入 BEV-based fusion network。

### 5.2 BEV 多模态融合与目标检测

Camera features 和 ISAC point-cloud features 被映射到统一 BEV 坐标系中。网络在 BEV
空间聚合不同站点和不同模态的信息，形成 BEV feature map。基于该 feature map，目标检测
head 采用类似 CenterNet 的结构输出车辆中心点、目标属性和置信度。

该设计使系统能够在统一空间中处理来自 BS 与分布式 SN 的多视角视觉信息，并结合 BS 侧
ISAC 点云提供的几何观测，从而增强车辆检测与定位能力。

### 5.3 Per-target Beam Prediction

在 BEV feature map 或 detected target features 上设置 beam prediction head。该 head
为每个 detected target 输出 per-beam power distribution，即该目标在当前 BS codebook 下
对应各个 beams 的预测质量。Top-K beams 由该分布排序获得，并作为后续 beam management
和通信评估的候选 beams。

采用 per-beam distribution 而不是只输出 hard Top-K，可以同时支持监督学习、Top-K accuracy
评估和 beam mismatch 对通信性能影响的建模。

### 5.4 Target-User Association

初始接入阶段，BS 对通信用户执行 SSB beam sweep，得到每个 user 的 beam power spectrum。
系统将该 spectrum 与每个 detected target 的 predicted beam distribution 进行相似度匹配，
建立 sensing target 与 communication user identity 的关联。匹配可以结合 beam distribution
相似度、BEV 空间先验和检测置信度。

完成初始关联后，每个车辆用户拥有统一的 sensing track identity 和 communication user
identity。该关联关系用于后续 tracking、beam prediction 和通信性能评估。

### 5.5 IMM Tracking 与后续帧维护

后续帧中，系统为每个已关联用户运行 IMM filter，预测其 BEV 位置和运动状态。新的 BEV
detections 到达后，系统根据 IMM predicted state 与 detection 之间的空间距离、运动一致性
和检测置信度进行 data association。关联成功的 track 更新状态并刷新 beam prediction；
关联失败或置信度降低时，可触发少量 beam measurement 或重新关联流程。

该机制使系统在不进行完整 beam sweep 的情况下维持 user identity，并利用时间连续性提高
beam selection 的稳定性。

### 5.6 通信性能评估流程

通信评估从 Top-K beam prediction 结果出发。若真实最优 beam 被包含在 Top-K candidate beams
中，则认为后续 CSI acquisition 或 PMI selection 可以在较小候选集合内进行，从而降低 beam
training overhead。若真实有效 beam 未被包含，则引入 beam mismatch penalty，用于刻画 CSI
方向或信道增益估计误差。随后在多用户 ZF precoding 模型下计算每个 user 的有效 SINR、
spectral efficiency 和 throughput。

总吞吐量同时考虑：

- 数据传输阶段的 spectral efficiency。
- beam training / measurement 占用的时频资源开销。
- Top-K beam prediction 错误导致的 SINR degradation。

## 6. 实验计划

### 6.1 仿真环境或数据来源

实验需要构建包含道路、BS、SN、车辆轨迹、camera observations、ISAC point clouds 和
communication beam labels 的仿真或数据生成环境。候选方案包括基于自动驾驶仿真平台生成
多视角视觉数据，并结合射线追踪或几何信道模型生成 beam power labels 和通信信道。
具体实现可参考 `Multi-modal-beam-twin` / `Multimodal-Wireless` 项目的仿真链路：使用
CARLA 定义道路交通场景并采集多传感器数据，使用 Blender/Mitsuba 进行逐帧场景重建，
再使用 Sionna RT 计算多径传播、信道系数和 beam-related labels。

数据应至少包含：

- 多 BS / 单 BS 局部服务区域设置。
- BS 与 SN 的空间位置、摄像头外参和视场设置。
- 车辆轨迹、位置、速度和目标框标注。
- BS 侧 ISAC point cloud。
- 每个车辆用户相对于服务 BS 的 beam power distribution 或最优 beam label。
- 可用于评估 ZF precoding 的信道或等效信道增益。

### 6.2 对比方法

计划设置以下 baselines：

- Communication-only full beam sweep：每次决策都依赖完整 beam sweep，作为高开销上界参考。
- Communication-only partial sweep：只扫描部分 beams，不使用 sensing 信息。
- Camera-only BEV beam prediction：仅使用 BS/SN 多视角图像，不使用 ISAC point cloud。
- ISAC-only beam prediction：仅使用 BS 侧 ISAC point cloud。
- Single-site sensing：仅使用服务 BS 的传感器，不使用周围 K 个 SN。
- No-tracking variant：逐帧独立检测与 beam prediction，不使用 IMM tracking。
- Proposed multimodal distributed sensing-assisted framework：使用 BS + K 个 SN 的 camera views、
  BS 侧 ISAC point cloud、target-user association 和 IMM tracking。

### 6.3 Evaluation Metrics

感知与 tracking 指标：

- detection accuracy / mAP。
- BEV localization error。
- tracking identity consistency。
- target-user association accuracy。
- tracking prediction error。

beam management 指标：

- Top-1 beam accuracy。
- Top-K beam accuracy。
- beam power prediction error。
- beam training overhead reduction。
- beam recovery / reassociation frequency。

通信性能指标：

- effective SINR under ZF precoding。
- spectral efficiency。
- user throughput。
- system sum throughput。
- overhead-adjusted throughput。

### 6.4 Ablation Studies

计划开展以下消融实验：

- 去除 ISAC point cloud，仅保留 camera modality。
- 去除 SN camera views，仅使用 BS 侧传感器。
- 改变协作 SN 数量 K。
- 去除 IMM tracking，比较逐帧独立关联的效果。
- 比较完整 beam sweep、partial beam measurement 和 sensing-assisted Top-K beam selection。
- 分析不同车辆密度、速度、遮挡强度和感知噪声下的性能变化。

### 6.5 Sensitivity Studies

计划分析以下因素对系统性能的影响：

- Top-K 中 K 的取值。
- BS/SN 传感器布局和视角覆盖。
- camera calibration / synchronization error。
- ISAC point cloud 稀疏度和噪声。
- 车辆速度和转向行为。
- beam codebook size。
- ZF precoding 中 beam mismatch penalty 的强度。

## 7. 当前证据

本节用于记录实验观察。只有当实验设置、指标和对比对象清楚时，观察才可以被
进一步转化为论文 claim。

| 日期 | 证据 / 观察 | 实验设置 | 指标 | 状态 |
| --- | --- | --- | --- | --- |
| 2026-06-21 | 完成论文仓库初始写作结构搭建。 | N/A | N/A | setup |
| 2026-06-21 | 明确初步研究方向：车联网场景下利用 BS/SN 多视角摄像头和 BS 侧 ISAC 点云进行 sensing-assisted beam management，覆盖目标检测、Top-K beam prediction、target-user association、IMM tracking 和简化 ZF 通信评估。 | Conceptual design | N/A | design draft |

## 8. 当前待补充部分

以下内容需要在文献调研、数据构建和实验推进后继续补充：

- 系统性文献调研与 related work 分类。
- 与已有 sensing-assisted beam management、ISAC-assisted communication、vehicular tracking
  和 user association 工作的差异。
- 具体数据集或仿真平台选择。
- BEV fusion network 的训练目标、损失函数和标签生成方式。
- Target-user association 的匹配代价函数和失败恢复机制。
- IMM filter 的运动模型组合与参数设置。
- Beam mismatch 对 CSI/PMI 抽象和 ZF SINR 的数学刻画。
- 主要贡献表述和实验支撑证据。

## 9. 术语与符号

当术语和符号稳定后，在此处维护统一写法。

| 概念 | 推荐术语或符号 | 说明 |
| --- | --- | --- |
| 多模态感知 | multimodal sensing | 由 camera modality 和 ISAC modality 共同构成 |
| 车联网 | vehicular networks | 本论文主要考虑道路侧基础设施辅助的车辆通信场景 |
| 基站 | base station (BS) | 通信服务节点，同时具备 camera 和 ISAC sensing 能力 |
| 分布式感知节点 | sensing node (SN) | 提供多视角 camera observations，不直接承担通信服务 |
| 多视角摄像头 | multiview cameras | 每个 BS/SN 配置 4 个倾斜下视摄像头 |
| ISAC 点云 | ISAC point cloud | BS 侧由双功能波形或等价 ISAC 感知过程获得的点云 |
| 鸟瞰图表征 | bird's-eye-view (BEV) representation | 用于对齐多站点、多模态观测的统一空间表征 |
| 用户关联 | user association | 通信 user 与 BS/beam 之间的服务关系；本文还涉及 sensing target 与 communication user identity 的关联 |
| 目标到用户关联 | target-user association | detected sensing target 与 communication user identity 之间的匹配 |
| 波束选择 | beam selection | 从 BS codebook 中选择服务车辆用户的 beam |
| Top-K 波束 | Top-K candidate beams | predicted beam distribution 中排名最高的 K 个 beams |
| 波束功率分布 | beam power distribution | 每个 detected target 对应不同 codebook beams 的预测质量或功率 |
| 跟踪状态 | tracking state | 车辆用户在 BEV 空间中的位置、速度和运动模式状态 |
| 交互多模型滤波器 | interacting multiple model (IMM) filter | 用于融合不同车辆运动模式并进行 tracking prediction |
| 零迫预编码 | zero-forcing (ZF) precoding | 通信性能评估中采用的多用户预编码抽象 |
| 频谱效率 | spectral efficiency | 基于 ZF 后有效 SINR 计算的通信指标 |
| 开销修正吞吐量 | overhead-adjusted throughput | 同时考虑数据传输效率和 beam training overhead 的吞吐量 |
