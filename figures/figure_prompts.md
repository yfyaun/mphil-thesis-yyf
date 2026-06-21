# Figure Prompt Plan

This file records draft prompts for thesis figures. The prompts are intentionally
method-oriented and should be refined after the implementation and experiments
are fixed.

## Figure 1.1: Research Motivation and Overall Problem

- Target chapter: Chapter 1, Introduction
- Purpose: Motivate why vehicular beam management can benefit from multimodal
  sensing.
- Prompt: Draw a clean academic system illustration for a roadside vehicular
  network. Show one serving base station with a beam codebook, several moving
  vehicles on a road, blockage objects, and time-varying narrow beams. Add
  roadside sensing nodes with cameras. Use arrows to show that sensing
  observations assist beam selection, target-user association, and tracking.
  Keep the style suitable for an engineering thesis, with restrained colors and
  clear labels.

## Figure 2.1: Taxonomy of Related Work

- Target chapter: Chapter 2, Background and Related Work
- Purpose: Organize the literature categories used in the related-work chapter.
- Prompt: Create a structured taxonomy diagram for related work on
  sensing-assisted beam management in vehicular networks. Use five branches:
  communication-only beam management, sensing-aided beam prediction,
  ISAC predictive beamforming, BEV multimodal fusion and cooperative perception,
  and target-user association with tracking. End with a highlighted research
  gap: closed-loop multimodal sensing, association, tracking, and system-level
  communication evaluation.

## Figure 3.1: BS-Centric Network and Sensor Topology

- Target chapter: Chapter 3, System Model and Problem Formulation
- Purpose: Define the system entities and observation scope.
- Prompt: Draw a top-down road scenario. Place one serving BS at the roadside
  and K neighboring sensing nodes around its coverage area. Each BS and sensing
  node has four tilted downward cameras. The BS also has an ISAC sensing module
  producing a local point cloud. Show vehicles as communication users and
  sensing targets. Highlight the BS-centric cooperative sensing region and
  distinguish camera observations, ISAC point cloud, and communication beams.

## Figure 3.2: Time Structure and Association State

- Target chapter: Chapter 3, System Model and Problem Formulation
- Purpose: Show how initial access and subsequent tracking frames differ.
- Prompt: Create a timeline figure with an initial access stage followed by
  multiple subsequent frames. In the initial stage, show SSB beam sweep, beam
  power spectrum, and target-user association. In later frames, show multimodal
  sensing, BEV detection, IMM prediction, data association, Top-K beam update,
  and optional partial beam measurement for recovery. Use compact symbols and
  avoid clutter.

## Figure 4.1: Proposed Framework Overview

- Target chapter: Chapter 4, Proposed Framework
- Purpose: Present the main processing pipeline.
- Prompt: Draw a block diagram for the proposed multimodal sensing-assisted
  beam management framework. Inputs: BS multiview cameras, K sensing-node
  multiview cameras, BS-side ISAC point cloud, and occasional communication
  beam measurements. Middle modules: calibration and synchronization, BEV
  multimodal fusion, CenterNet-like detection head, per-target beam prediction
  head, initial target-user association, IMM tracking, and communication
  evaluation. Outputs: detected vehicles, Top-K candidate beams, user identity
  association, tracking states, ZF SINR, spectral efficiency, and
  overhead-adjusted throughput.

## Figure 4.2: BEV Multimodal Fusion and Detection Heads

- Target chapter: Chapter 4, Proposed Framework
- Purpose: Explain how distributed cameras and ISAC point clouds are aligned.
- Prompt: Create an architecture diagram showing image features from multiple
  cameras being lifted or projected into a shared bird's-eye-view grid, and
  ISAC point-cloud features being encoded into the same BEV grid. Show feature
  fusion, a BEV feature map, a CenterNet-like detection head for vehicle
  centers, and a beam prediction head that outputs a per-beam power distribution
  for each detected target.

## Figure 4.3: Target-User Association and IMM Tracking Workflow

- Target chapter: Chapter 4, Proposed Framework
- Purpose: Clarify the identity-maintenance mechanism.
- Prompt: Draw a two-stage workflow. Stage 1: match detected sensing targets
  with communication users by comparing predicted per-target beam distributions
  with measured SSB beam power spectra. Stage 2: maintain the association with
  an IMM tracker, where predicted states are matched to new BEV detections and
  beam predictions are refreshed. Include failure handling through partial beam
  measurement or re-association.

## Figure 4.4: Communication Evaluation Abstraction

- Target chapter: Chapter 4, Proposed Framework
- Purpose: Explain how beam prediction accuracy affects throughput.
- Prompt: Draw a causal flow diagram from Top-K beam prediction to communication
  performance. If the true effective beam is inside Top-K, show reduced beam
  training overhead and accurate CSI or PMI acquisition. If not, show beam
  mismatch penalty, degraded effective channel estimate, lower ZF SINR, lower
  spectral efficiency, and lower overhead-adjusted throughput. Keep it as an
  abstraction rather than a full 5G protocol stack.

## Figure 5.1: Multimodal Simulation System Pipeline

- Target chapter: Chapter 5, Simulation System and Experimental Evaluation
- Purpose: Support the simulation-system contribution.
- Prompt: Draw a pipeline from CARLA traffic scenario generation to sensor data
  export, frame-wise scene reconstruction in Blender or Mitsuba, Sionna ray
  tracing, channel and beam-label generation, and final dataset assembly. Show
  outputs including camera images, ISAC-like point clouds, vehicle trajectories,
  beam power labels, channel coefficients, and evaluation metadata.

## Figure 5.2: Evaluation Matrix

- Target chapter: Chapter 5, Simulation System and Experimental Evaluation
- Purpose: Summarize baselines, metrics, and ablation studies.
- Prompt: Create a compact matrix diagram. Rows are evaluation dimensions:
  perception, association and tracking, beam management, and communication
  performance. Columns are baselines and variants: full sweep, partial sweep,
  camera-only, ISAC-only, single-site sensing, no tracking, and the proposed
  multimodal distributed framework. Place representative metrics in each row,
  such as mAP, localization error, association accuracy, Top-K beam accuracy,
  ZF SINR, spectral efficiency, and overhead-adjusted throughput.

