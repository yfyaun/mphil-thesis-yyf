# 多模态感知辅助波束管理相关文献快速扫描

最后更新：2026-06-22

本文档用于支撑后续撰写 `docs/work_brief.md` 中的“核心创新点 / 贡献”部分。当前版本是快速扫描笔记，
不是最终 related work 章节。每篇论文均已下载 PDF 到本文件夹，文件名见各条目。

## 0. 检索与筛选原则

- 主题优先级：sensing-assisted beam prediction / beam tracking、ISAC predictive beamforming、
  target-user association、tracking、BEV multimodal fusion、distributed / cooperative perception。
- 来源优先级：IEEE 高质量期刊会议、arXiv 预印本、作者主页或学校仓储开放 PDF。
- 不使用付费墙绕过方式；IEEE 论文若有 arXiv 或作者开放版，则保存开放 PDF。
- 当前 30 篇大致分为三组：
  - 感知辅助 beam prediction / beam management：1--18。
  - BEV、CenterNet、V2X cooperative perception 与 tracking 基础方法：19--22、30。
  - ISAC / DFRC predictive beamforming 与通信性能建模：23--29。

## 1. 文献快速总结

### 1. Alrabeiah et al., "Millimeter Wave Base Stations with Cameras: Vision-Aided Beam and Blockage Prediction", IEEE VTC-Spring 2020

- PDF：`01_Alrabeiah2020_Vision_Aided_Beam_Blockage_Prediction.pdf`
- 链接：https://arxiv.org/abs/1911.06255
- 内容：较早提出利用 BS 侧 RGB camera 辅助 mmWave beam prediction 和 blockage prediction。核心思想是用视觉信息和 sub-6 GHz channel 等侧信息直接预测 mmWave beam 或遮挡状态，从而减少 beam sweeping。
- 对本论文的启发：证明 camera 可以作为 beam management 的外部感知源，适合作为视觉辅助通信的早期代表工作。
- 局限/可衔接点：主要是 BS 侧单点视觉和 beam/blockage 分类，不涉及分布式多视角 sensing nodes、BEV 空间融合、target-user association 和 tracking 维护。

### 2. Xu et al., "Computer Vision Aided mmWave Beam Alignment in V2X Communications", IEEE TWC 2023

- PDF：`02_Xu2023_Computer_Vision_Aided_mmWave_Beam_Alignment_V2X.pdf`
- 链接：https://arxiv.org/abs/2207.11409
- 内容：利用车载或环境视觉信息提取动态车辆的尺寸、位置等信息，用 DNN 推断 beam pair，并引入 beam coherence time prediction 来决定何时重新对齐波束。
- 对本论文的启发：说明视觉可用于预测 beam alignment 和 alignment 周期，和本论文降低 beam management 开销的动机一致。
- 局限/可衔接点：侧重视觉辅助 beam pair 和 BCT，未把多站点感知、ISAC 点云、目标到用户关联和通信吞吐量开销模型放在同一个框架中。

### 3. Charan et al., "Vision-Position Multi-Modal Beam Prediction Using Real Millimeter Wave Datasets", IEEE WCNC 2022

- PDF：`03_Charan2022_Vision_Position_Multimodal_Beam_Prediction.pdf`
- 链接：https://arxiv.org/abs/2111.07574
- 内容：使用真实 V2I 数据中的 camera 和 GPS/position 信息进行 mmWave beam prediction，是 DeepSense 6G 系列早期代表工作。
- 对本论文的启发：提供真实数据集上 vision-position multimodal beam prediction 的评估口径，如 Top-1 / Top-3 accuracy。
- 局限/可衔接点：主要处理视觉和位置双模态，目标识别、用户身份关联和后续 tracking 不是核心；也没有考虑 BS/SN 分布式多视角感知。

### 4. Demirhan and Alkhateeb, "Radar Aided 6G Beam Prediction", IEEE WCNC 2022

- PDF：`04_Demirhan2022_Radar_Aided_6G_Beam_Prediction.pdf`
- 链接：https://arxiv.org/abs/2111.09676
- 内容：利用 radar observation 进行 6G/mmWave beam prediction，在 DeepSense 6G 实测数据上展示 radar sensing 降低 beam training overhead 的潜力。
- 对本论文的启发：与本论文的 ISAC point cloud / radar-like sensing 模态直接相关，可作为“非视觉感知辅助 beam prediction”的代表。
- 局限/可衔接点：关注 radar 单模态，不涉及 camera + ISAC point cloud 的 BEV 融合，也不处理多目标场景下的 target-user association。

### 5. Jiang et al., "LiDAR Aided Future Beam Prediction in Real-World Millimeter Wave V2I Communications", IEEE WCL 2022

- PDF：`05_Jiang2022_LiDAR_Aided_Future_Beam_Prediction.pdf`
- 链接：https://arxiv.org/abs/2203.05548
- 内容：基于 LiDAR 数据预测当前和未来 beam，在真实 V2I 数据中证明几何深度信息对 future beam prediction / tracking 有帮助。
- 对本论文的启发：说明几何点云类模态对 beam prediction 和 tracking 任务非常关键，可支撑引入 BS 侧 ISAC point cloud。
- 局限/可衔接点：使用 LiDAR 而非通信系统自身的 ISAC sensing；主要是单站点几何感知，未扩展到 distributed SN camera 和通信身份关联。

### 6. Alkhateeb et al., "DeepSense 6G: A Large-Scale Real-World Multi-Modal Sensing and Communication Dataset", IEEE Communications Magazine 2023

- PDF：`06_Alkhateeb2023_DeepSense6G_Dataset.pdf`
- 链接：https://arxiv.org/abs/2211.09769
- 内容：介绍 DeepSense 6G 数据集，包含同步的 mmWave communication、camera、GPS、LiDAR、radar 等数据，支持多模态感知与通信研究。
- 对本论文的启发：为实验设计提供重要参照，包括多模态数据组织、beam labels、真实道路场景和 evaluation protocols。
- 局限/可衔接点：数据集文章本身不提出完整算法；本论文若自行构建仿真/数据，也可对标其同步多模态通信感知数据结构。

### 7. Charan et al., "Multi-Modal Beam Prediction Challenge 2022: Towards Generalization", arXiv 2022

- PDF：`07_Charan2022_Multimodal_Beam_Prediction_Challenge.pdf`
- 链接：https://arxiv.org/abs/2209.07519
- 内容：围绕 DeepSense 6G 组织多模态 beam prediction challenge，强调跨地点、跨时间、跨场景的泛化能力。
- 对本论文的启发：提供 beam prediction 泛化评估和 baseline 设计思路，提醒不能只在单一场景报告 Top-K accuracy。
- 局限/可衔接点：challenge 更关注 generalization benchmark，未形成面向 target-user association、tracking 和 5G/ZF 吞吐量的完整系统链路。

### 8. Charan et al., "Camera Based mmWave Beam Prediction: Towards Multi-Candidate Real-World Scenarios", arXiv 2023

- PDF：`08_Charan2023_Camera_Based_mmWave_Beam_Prediction_MultiCandidate.pdf`
- 链接：https://arxiv.org/abs/2308.06868
- 内容：将 camera-based beam prediction 推进到 multi-candidate / multi-object V2I 场景，并提出 transmitter identification，用于从多个视觉候选目标中找到通信用户。
- 对本论文的启发：这是 target-user association 方向最接近的文献之一。它说明 beam power / visual target matching 是多目标 beam prediction 的关键。
- 局限/可衔接点：主要使用 camera 和 position，关联过程仍较依赖图像级目标语义；本论文可以进一步引入 BEV 多模态融合、ISAC 点云和 IMM tracking。

### 9. Imran et al., "Environment Semantic Communication: Enabling Distributed Sensing Aided Networks", arXiv 2024 / IEEE ICC Workshops

- PDF：`09_Imran2024_Environment_Semantic_Communication_Distributed_Sensing_Aided_Networks.pdf`
- 链接：https://arxiv.org/abs/2402.14766
- 内容：提出 distributed sensing nodes，每个节点用 RGB camera 抽取 environment semantics，再将语义而非原始图像传给 BS 做 beam prediction。论文包含 transmitter identification 和 object association based tracking。
- 对本论文的启发：与“BS + 周围 K 个 SN”的分布式感知设定高度相关，也是本论文 distributed sensing 设计的重要直接参照。
- 局限/可衔接点：主要是 RGB camera semantics，如 bounding box / mask；没有将 BS 侧 ISAC point cloud 与多视角 camera 在 BEV 空间统一融合，也没有做 ZF/throughput 级通信评估。

### 10. Tian et al., "Multimodal Transformers for Wireless Communications: A Case Study in Beam Prediction", arXiv / ITU Journal 2023

- PDF：`10_Tian2023_Multimodal_Transformers_Beam_Prediction.pdf`
- 链接：https://arxiv.org/abs/2309.11811
- 内容：使用 image、point cloud、radar raw data、GPS 等多模态序列，并通过 transformer 学习跨模态和时间依赖，用于 beam prediction。
- 对本论文的启发：说明 transformer-style fusion 是多模态 beam prediction 的常见强 baseline；也提供多模态预处理和数据增强方法。
- 局限/可衔接点：多为 feature-level fusion，没有显式以 BEV 空间维护几何一致性；没有覆盖 sensing target 到 communication user 的长期身份维护。

### 11. Ghassemi et al., "Multi-Modal Transformer and Reinforcement Learning-Based Beam Management", IEEE Networking Letters 2024

- PDF：`11_Ghassemi2024_MMT_RL_Beam_Management.pdf`
- 链接：https://arxiv.org/abs/2410.19859
- 内容：两阶段 beam management：先用 multi-modal transformer 预测 beam group，再用 reinforcement learning 在组内快速决策，以提升 beam prediction accuracy 和 system throughput。
- 对本论文的启发：将多模态感知与 throughput/decision-making 联系起来，可作为通信性能评估和 beam decision baseline。
- 局限/可衔接点：不强调多目标检测、target-user association 或 IMM tracking；多模态表示也不是以 BS/SN 分布式 BEV 融合为中心。

### 12. Farzanullah et al., "Beam Selection in ISAC using Contextual Bandit with Multi-modal Transformer and Transfer Learning", IEEE ICC Workshops 2025 / arXiv

- PDF：`12_Farzanullah2025_Contextual_Bandit_MMT_ISAC_Beam_Selection.pdf`
- 链接：https://arxiv.org/abs/2503.08937
- 内容：结合 ISAC sensing data、multi-modal transformer、multi-agent contextual bandit 和 transfer learning 做 beam selection，并用 spectral efficiency regret 评估。
- 对本论文的启发：提供“感知输入 -> beam decision -> spectral efficiency”链路的参考，尤其适合作为通信性能指标和在线决策方法的对照。
- 局限/可衔接点：主要是 bandit/RL 决策框架，不处理 BEV 目标检测、target-user association 和多帧 tracking 误差如何影响通信。

### 13. Park et al., "Resource-Efficient Beam Prediction in mmWave Communications with Multimodal Realistic Simulation Framework", arXiv 2025

- PDF：`13_Park2025_Resource_Efficient_Beam_Prediction_CRKD.pdf`
- 链接：https://arxiv.org/abs/2504.05187
- 内容：构建 CARLA + MATLAB 的 multimodal realistic simulation framework，并用 cross-modal relational knowledge distillation 将多模态 teacher 知识蒸馏到 radar-only student。
- 对本论文的启发：为自建仿真环境提供很直接的参考：自动驾驶仿真生成 sensing 数据，通信/beam labels 由信道仿真生成。
- 局限/可衔接点：重点是模型压缩和 radar-only 部署，不是 BS/SN 多视角 camera + ISAC 点云的协作感知，也不强调 target-user identity maintenance。

### 14. Ma et al., "Knowledge Distillation for Lightweight Multimodal Sensing-Aided mmWave Beam Tracking", arXiv 2026

- PDF：`14_Ma2026_KD_Lightweight_Multimodal_Beam_Tracking.pdf`
- 链接：https://arxiv.org/abs/2604.16708
- 内容：使用 camera 和 radar 历史观测，通过 CNN-GRU teacher 预测当前和未来 beam，再用 knowledge distillation 训练轻量 student。
- 对本论文的启发：与“后续帧减少 sweep、依赖 sensing-assisted tracking / beam tracking”高度相关，可作为 long-term beam tracking 文献。
- 局限/可衔接点：关注轻量化和序列预测，没有显式处理多传感器 BEV 空间检测、target-user association 或通信层 ZF precoding penalty。

### 15. Zeng et al., "A BEV-Fusion Based Framework for Sequential Multi-Modal Beam Prediction in mmWave Systems", arXiv 2026

- PDF：`15_Zeng2026_BEV_Fusion_Sequential_Multimodal_Beam_Prediction.pdf`
- 链接：https://arxiv.org/abs/2604.05668
- 内容：将 camera、LiDAR、radar、GPS 融合到 shared BEV representation，并用 temporal transformer 聚合序列观测做 beam prediction。
- 对本论文的启发：这是与本论文 BEV-based multimodal beam prediction 最接近的近期工作之一，可作为必须重点对比的技术路线。
- 局限/可衔接点：虽然使用 BEV，但没有专门面向 BS + K 个 SN 的分布式 camera 节点和 BS 侧 ISAC point cloud；也没有把初始 SSB 关联、IMM tracking 和 ZF throughput 统一建模。

### 16. Orimogunje et al., "Occlusion-Aware Multimodal Beam Prediction and Pose Estimation for mmWave V2I", arXiv 2026

- PDF：`16_Orimogunje2026_Occlusion_Aware_Multimodal_Beam_Prediction_Pose.pdf`
- 链接：https://arxiv.org/abs/2603.25799
- 内容：融合 RGB、LiDAR、radar range-angle map、GNSS 和短期 mmWave power history，同时预测 beam、blockage probability 和 2D position。
- 对本论文的启发：说明将 beam prediction、pose estimation、blockage / occlusion awareness 放在 multi-task framework 中是可行的。
- 局限/可衔接点：关注 occlusion-aware multi-task prediction，不强调 distributed SN camera，target-user association 也不是主线。

### 17. Wen et al., "AMBER: An Adaptive Multimodal Mask Transformer for Beam Prediction with Missing Modalities", arXiv 2025

- PDF：`17_Wen2025_AMBER_Missing_Modality_Beam_Prediction.pdf`
- 链接：https://arxiv.org/abs/2512.11331
- 内容：提出 missing-modality-aware mask transformer，处理 camera、LiDAR、radar、GPS 等模态缺失情况下的 robust beam prediction。
- 对本论文的启发：提醒真实系统中的 camera 遮挡、点云稀疏、同步失败等问题会影响多模态融合；可作为 robustness / missing sensor baseline。
- 局限/可衔接点：侧重缺失模态鲁棒性，不解决多目标身份关联、IMM tracking 和通信级吞吐量建模。

### 18. Mollah et al., "Multi-Modal Sensing and Fusion in mmWave Beamforming for Connected Vehicles: A Transformer Based Framework", arXiv 2026

- PDF：`18_Mollah2026_Multimodal_Sensing_Fusion_mmWave_Beamforming_Connected_Vehicles.pdf`
- 链接：https://arxiv.org/abs/2602.13606
- 内容：针对 connected vehicles 的 V2I/V2V beamforming，使用多模态 sensing 和 cross-modal attention 预测 Top-K beams，并报告 power loss、latency 和 beam searching overhead。
- 对本论文的启发：提供 Top-K beams、power loss、latency/overhead 等评估指标，和本论文的通信性能口径接近。
- 局限/可衔接点：不是以 BEV 目标检测和 target-user association 为核心，也没有使用 BS/SN 分布式感知拓扑。

### 19. Zhou et al., "Objects as Points", arXiv 2019

- PDF：`19_Zhou2019_CenterNet_Objects_As_Points.pdf`
- 链接：https://arxiv.org/abs/1904.07850
- 内容：提出 CenterNet，将目标表示为中心点，通过 keypoint estimation 检测中心并回归尺寸、3D 位置、姿态等属性。
- 对本论文的启发：适合作为 BEV feature map 上目标检测 head 的基础思想；在 BEV 上预测车辆中心点与 beam head 可自然共享特征。
- 局限/可衔接点：这是视觉检测基础方法，不涉及通信 beam prediction；本论文需要把 CenterNet-style detection 与 beam power distribution prediction 联合起来。

### 20. Philion and Fidler, "Lift, Splat, Shoot", ECCV 2020 / arXiv

- PDF：`20_Philion2020_Lift_Splat_Shoot_BEV_Multicamera.pdf`
- 链接：https://arxiv.org/abs/2008.05711
- 内容：将任意 camera rig 的图像特征 lift 到 3D frustum，再 splat 到 BEV grid，用于自动驾驶中的 BEV 表征学习。
- 对本论文的启发：为 BS/SN 多视角 camera 映射到 BEV 空间提供基础方法参考。
- 局限/可衔接点：主要服务自动驾驶感知任务，不处理通信 beam labels、ISAC 点云和用户身份关联。

### 21. Liu et al., "BEVFusion: Multi-Task Multi-Sensor Fusion with Unified BEV Representation", arXiv 2022

- PDF：`21_Liu2022_BEVFusion_Multitask_Multisensor_Fusion.pdf`
- 链接：https://arxiv.org/abs/2205.13542
- 内容：在统一 BEV 空间中融合 camera 和 LiDAR features，强调 BEV fusion 可同时保留几何与语义信息，并支持多任务感知。
- 对本论文的启发：支撑“camera + point cloud 在 BEV 中统一融合”的主干设计；本论文可将 LiDAR 替换/类比为 BS 侧 ISAC point cloud。
- 局限/可衔接点：不涉及通信 beam prediction；本论文要把 BEV 感知特征和 beam power distribution / Top-K beam head 连接起来。

### 22. Xu et al., "V2X-ViT: Vehicle-to-Everything Cooperative Perception with Vision Transformer", ECCV 2022 / arXiv

- PDF：`22_Xu2022_V2X_ViT_Cooperative_Perception.pdf`
- 链接：https://arxiv.org/abs/2203.10638
- 内容：面向 V2X cooperative perception，使用 transformer 融合多智能体/基础设施感知信息，处理异步、pose error 和异构 agent。
- 对本论文的启发：为 BS + distributed SN 的协作感知提供 V2X cooperative perception 参考，尤其是多节点信息融合与鲁棒性问题。
- 局限/可衔接点：该工作目标是自动驾驶 3D detection，不含 communication beam prediction 或 target-user association。

### 23. Liu et al., "Learning-Based Predictive Beamforming for Integrated Sensing and Communication in Vehicular Networks", IEEE JSAC 2022

- PDF：`23_Liu2022_Learning_Based_Predictive_Beamforming_ISAC_Vehicular.pdf`
- 链接：https://arxiv.org/abs/2108.11540
- 内容：在 ISAC V2I 网络中，用历史 channel 和 HCL-Net 预测下一时隙 beamforming matrix，并在 sensing CRLB 约束下最大化 sum-rate。
- 对本论文的启发：提供 ISAC + predictive beamforming + sum-rate objective 的高质量基准，是通信性能建模的重要参考。
- 局限/可衔接点：输入主要是历史 channel，而非多模态 camera/point cloud；没有处理 sensing target detection 和 communication user identity mapping。

### 24. Liu et al., "Deep CLSTM for Predictive Beamforming in ISAC-Enabled Vehicular Networks", arXiv 2022

- PDF：`24_Liu2022_Deep_CLSTM_Predictive_Beamforming_ISAC.pdf`
- 链接：https://arxiv.org/abs/2209.12368
- 内容：针对 ISAC-enabled vehicular networks 的 channel prediction / predictive beamforming 问题，使用 convolutional LSTM 处理时空依赖。
- 对本论文的启发：说明 sequence modeling 对高移动性预测很重要，可为本论文的 tracking-assisted beam prediction 提供 temporal baseline。
- 局限/可衔接点：仍偏 channel/beamforming 预测，不涉及外部多模态感知、BEV detection 和多目标用户关联。

### 25. Yuan et al., "Bayesian Predictive Beamforming for Vehicular Networks", IEEE TWC 2021

- PDF：`25_Yuan2021_Bayesian_Predictive_Beamforming_Vehicular.pdf`
- 链接：https://arxiv.org/abs/2005.07698
- 内容：利用 DFRC echo 估计和预测车辆运动参数，通过 Bayesian / message passing 实现低开销 beamforming。
- 对本论文的启发：与“ISAC sensing -> tracking/prediction -> beamforming”链路高度相关，可为 IMM/EKF 类 tracking 设计提供理论背景。
- 局限/可衔接点：方法主要基于 radar-communication echo 和概率图，不使用 camera / BEV / deep multimodal detection。

### 26. Liu et al., "Radar-Assisted Predictive Beamforming for Vehicular Links: Communication Served by Sensing", IEEE TWC 2020

- PDF：`26_Liu2020_Radar_Assisted_Predictive_Beamforming_Vehicular.pdf`
- 链接：https://arxiv.org/abs/2001.09306
- 内容：提出 radar-assisted predictive beamforming，利用 RSU 的 radar sensing 估计车辆运动状态并辅助 V2I beam tracking，同时考虑 sensing-communication power allocation tradeoff。
- 对本论文的启发：是 sensing-assisted communication 的核心早期代表，可支撑“通信由感知服务”的研究动机。
- 局限/可衔接点：不涉及多模态 perception，也没有 camera-based target identification；本论文可以把 radar/ISAC tracking 与视觉 BEV 检测融合。

### 27. Du et al., "Integrated Sensing and Communications for V2I Networks: Dynamic Predictive Beamforming for Extended Vehicle Targets", IEEE TWC 2023

- PDF：`27_Du2023_ISAC_V2I_Dynamic_Predictive_Beamforming_Extended_Targets.pdf`
- 链接：https://arxiv.org/abs/2111.10152
- 内容：指出车辆是 extended target，简单指向车辆中心可能无法覆盖通信 receiver；提出动态 beamwidth / two-stage ISAC-communication scheme 和 EKF tracking。
- 对本论文的启发：提示车辆几何形状、receiver 位置和 beam width 都会影响 beam management，支撑本论文从检测目标到通信用户关联的必要性。
- 局限/可衔接点：基于 ISAC echo 和 EKF，不考虑多视角 camera、distributed SN 或 neural BEV beam distribution prediction。

### 28. Yao et al., "Joint Sensing and Communications for DRL-Based Beam Management in 6G", IEEE GLOBECOM 2022

- PDF：`28_Yao2022_Joint_Sensing_Communications_DRL_Beam_Management.pdf`
- 链接：https://arxiv.org/abs/2208.01880
- 内容：在位置不确定条件下，利用 vision-aided sensing 和 DRL 做 beam management / resource allocation。
- 对本论文的启发：提供 joint sensing and communication beam management 的 DRL baseline，以及在通信层处理不确定性的方法。
- 局限/可衔接点：侧重 RL 资源分配和位置不确定性，不解决多模态 BEV detection、target-user association 和 tracking continuity。

### 29. Wang and Wong, "Deep Learning for ISAC-Enabled End-to-End Predictive Beamforming in Vehicular Networks", IEEE ICC 2023

- PDF：`29_Wang2023_ISAC_End_to_End_Predictive_Beamforming.pdf`
- 链接：https://people.ece.ubc.ca/vincentw/C/WW-ICC-2023.pdf
- 内容：直接从 reflected signal samples 到 beamforming vector，避免显式估计车辆状态参数，并用 unsupervised objective 最大化 achievable rate。
- 对本论文的启发：提供 end-to-end ISAC predictive beamforming 的参考，说明不必总是显式恢复完整 channel/state 才能做通信优化。
- 局限/可衔接点：不是多模态外部感知框架，也没有处理视觉目标识别和 target-user association。

### 30. Zhou et al., "Tracking Objects as Points", ECCV 2020 / arXiv

- PDF：`30_Zhou2020_CenterTrack_Tracking_Objects_As_Points.pdf`
- 链接：https://arxiv.org/abs/2004.01177
- 内容：提出 CenterTrack，用 point-based detection 和 displacement prediction 同时进行目标检测与 tracking，简化 tracking-by-detection pipeline。
- 对本论文的启发：可为 BEV detection 后的目标追踪和 detection-to-track association 提供基础思路，与 IMM tracking 可形成对照或互补。
- 局限/可衔接点：是视觉多目标跟踪方法，不包含通信 user identity、SSB beam spectrum association 或 beam prediction。

## 2. 对本论文贡献撰写的支撑线索

### 2.1 已有工作的主要覆盖范围

- 单模态或少数模态 sensing-aided beam prediction 已较成熟：camera、GPS、radar、LiDAR 均已有代表工作。
- DeepSense 6G 系列工作已经把真实多模态 sensing + mmWave beam labels 推到较系统的 benchmark 层面。
- 近年工作开始关注 transformer、missing modality、knowledge distillation、BEV fusion、Top-K beam prediction 和 overhead / latency metrics。
- ISAC predictive beamforming 文献通常从 radar echo / historical channel / reflected signal 出发，关注 beamforming matrix、sum-rate、CRLB 或 sensing-communication tradeoff。
- 自动驾驶 BEV 和 V2X cooperative perception 文献提供了多视角、多节点、多模态融合的成熟方法，但通常不考虑通信 beam management。

### 2.2 与本论文方案最接近的已有方向

- 分布式 sensing：Imran et al. 已经使用 distributed RGB sensing nodes 做 beam prediction，并包含 transmitter identification / object tracking。
- 多候选用户：Charan et al. 处理 multi-candidate camera-based beam prediction，并提出 transmitter identification。
- BEV 多模态 beam prediction：Zeng et al. 已经将 camera/LiDAR/radar/GPS 融合到 BEV 用于 sequential beam prediction。
- ISAC tracking / predictive beamforming：Yuan、Liu、Du 等工作已经证明 DFRC/ISAC echo 可用于车辆状态预测和 beamforming。

### 2.3 可发展为本论文“候选贡献”的方向

以下只是基于当前扫描得到的候选贡献角度，后续需要结合更细文献调研和实验结果再正式写入 `work_brief.md`。

1. **分布式多视角 camera 与 BS 侧 ISAC point cloud 的 BEV 统一融合。**  
   已有 distributed sensing 工作多用 RGB semantics，已有 BEV beam prediction 多为 co-located 多模态输入。本论文可以强调以每个 BS 为中心，联合服务 BS 的 camera/ISAC point cloud 与周围 K 个 SN 的 multiview cameras，在 BEV 中形成面向 beam management 的统一感知表示。

2. **从 sensing target 到 communication user 的可追踪关联链路。**  
   多数 beam prediction 工作假设 user identity 或位置标签可用；multi-candidate 文献开始处理 transmitter identification，但后续长期 tracking 和少量 beam calibration 尚不充分。本论文可把 SSB beam power spectrum 初始关联、BEV detection association 和 IMM tracking 组织成完整 target-user association pipeline。

3. **检测、beam distribution prediction、tracking 和通信性能的端到端系统评估。**  
   许多文献只报告 Top-K accuracy 或 beam power loss；ISAC beamforming 文献则常从 channel / echo 直接优化 rate。本论文可以把 Top-K beam 正确率、beam training overhead、beam mismatch 对 CSI/PMI/ZF SINR 的影响和 throughput 放入同一评估链路，突出“感知预测错误如何传导到通信吞吐量”。

4. **面向低开销 beam management 的多帧运行机制。**  
   初始帧使用 SSB sweep 完成 user identity anchoring，后续帧主要依赖 IMM tracking 和 sensing-assisted Top-K prediction，只在置信度不足或关联失败时使用少量 beam measurement。这比每帧完整 sweep 更贴近协议开销问题，也比纯逐帧 beam prediction 更系统。

## 3. 后续建议

- 将本文件中的 30 篇文献整理进 `mythesis.bib`，并为每篇设置稳定 citation key。
- 下一步可把 `docs/thesis_outline.md` 的 Chapter 2 按以下类别重组：
  - sensing-aided beam prediction；
  - ISAC predictive beamforming and beam tracking；
  - distributed / cooperative perception；
  - target-user association and tracking；
  - research gap summary。
- 在写核心贡献前，需要进一步确认实验设置能支撑哪些 claim，尤其是：
  - BEV distributed fusion 是否显著优于 single-site / camera-only / ISAC-only；
  - SSB-based target-user association 是否优于仅基于位置/视觉的关联；
  - IMM tracking 是否能减少 beam measurement 频率并维持 Top-K accuracy；
  - ZF throughput 模型是否能清楚反映 beam mismatch penalty。
