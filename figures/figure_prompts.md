# Figure Plan and Generation Prompts for Chapters 1--4

This plan is derived from the current Chapters 1--4.  It follows the thesis
argument rather than adding decorative artwork:

\[
\text{distributed multimodal observations}
\rightarrow
\text{unbound target-level beam evidence}
\rightarrow
\text{UE--track association}
\rightarrow
\text{CSI-RS candidate measurement}
\rightarrow
\text{VUE-level communication performance}.
\]

The recommended figures clarify a relationship that is hard to recover from
text or equations alone: the difference between a physical target and a VUE,
the sensing--communication interface, or a multi-stage algorithm.  Figures
1.1, 3.1, 3.2, 4.1, 4.2, 4.4, and 4.5 are highest priority.  Figures 2.1 and
4.3 should be retained when the page budget permits.

## Global visual language

### Style

- Use clean vector-like academic diagrams on a white or very light-grey
  background.  Avoid photorealistic scenes, 3D rendering, gradients, neon
  colours, decorative textures, and dense dashboard-like panels.
- Use left-to-right composition for pipelines and top-to-bottom composition for
  timing or decision trees.  Use generous whitespace.
- Use rounded rectangles for algorithms, thin arrows for data flow, dashed
  arrows for fallback or optional paths, and a diamond only for a genuine
  decision gate.
- Generated images should contain no equations and very little text.  Add exact
  labels and mathematical symbols in vector editing software or LaTeX after
  generation, since image models are unreliable for small typesetting.

### Palette and icon rules

| Semantic object | Suggested appearance |
|---|---|
| Target BS and radio-side procedure | navy or clear blue |
| Neighbouring sensing node | teal |
| Camera observation / visual feature | muted green |
| BS-local ISAC point cloud / geometric feature | violet |
| Physical target or perception track | neutral charcoal |
| Communication VUE / measured link | orange |
| Reliable sensing-assisted path | blue-green |
| Conventional fallback / rejected association | restrained red or grey |

Topology figures may use simple original-colour icons for a roadside BS, camera,
vehicle, point cloud, and radio beam.  Algorithm figures should remain
schematic.

### Technical facts that every figure must preserve

- Neighbouring SNs provide sensing observations only; they do not serve VUEs.
- The scope is a target-BS-centred local service region; do not imply a global
  cross-BS identity tracker.
- Perception outputs physical targets and tracks, not UE identities.
- Prediction ranks CSI-RS candidates.  The final service beam is always chosen
  from actually measured CSI-RS beams.
- A predicted-only track cannot initiate a reduced scan.  A current observation
  and a reliable accepted association are both required.
- Downlink evaluation uses RZF, not ZF.
- The ISAC point cloud is an available BS-local observation.  Do not imply that
  this thesis develops a raw ISAC waveform/radar pipeline, a CARLA data
  generation pipeline, or a full 5G NR protocol stack.

## Figure 1.1 --- Motivation: scene observation to user-specific beam management

- **Priority:** Essential
- **Insertion point:** Chapter 1, after the final paragraph of Background and
  before Challenges.
- **Filename:** *figures/ch1_motivation_sensing_to_vue.pdf*
- **Purpose:** Establish the whole thesis problem before the three challenges.
  In particular, show why a target-level beam ranking becomes useful only after
  it is attached to the intended VUE.
- **Suggested caption:** *Distributed multimodal sensing narrows the CSI-RS
  measurement set only after target-level beam evidence is associated with the
  intended VUE; the final service beam remains measurement-selected.*
- **Composition:** One roadside scene develops through four stages: distributed
  sensing; local BEV targets with beam-distribution glyphs; ambiguity between
  nearby physical tracks and a VUE measurement; CSI-RS candidates, measurement,
  service-beam selection, and rate.  Include a dashed fallback route for an
  unreliable association.
- **Generation prompt:**

  > Create a wide, clean vector-style academic illustration for a wireless
  > communications thesis.  On a white background, show a roadside V2I scene
  > evolving left to right into a user-specific beam-management decision.  Left:
  > one roadside target base station in navy blue, two smaller neighbouring
  > sensing nodes in teal, several moving vehicles on a simple road, compact
  > camera field-of-view cones, a sparse violet ISAC point cloud, and one
  > occlusion object.  The target base station emits narrow radio beams;
  > sensing nodes do not emit service beams.  Middle-left: a small bird's-eye
  > view grid with several unlabelled vehicle targets in charcoal and a compact
  > ranked beam-distribution glyph beside each target.  Middle-right: show two
  > nearby perception tracks but one orange communication VUE measurement.
  > Use a measurement-anchored link to select the correct track; show a muted
  > red dashed alternative mismatch.  Right: a short CSI-RS candidate list, a
  > measurement probe, one selected service beam, and a restrained effective
  > rate icon.  Include a dashed fallback path from an unreliable association
  > to conventional refinement.  Use flat vector shapes, minimal text,
  > navy-teal-violet-orange-charcoal palette, no gradients, no photorealism, no
  > tiny labels, no equations, and generous whitespace.  Aspect ratio 16:9.

## Figure 2.1 --- Related-work chain and thesis positioning

- **Priority:** Useful
- **Insertion point:** Chapter 2, after the opening paragraph and before Beam
  Alignment in High-Mobility V2I Networks.
- **Filename:** *figures/ch2_related_work_chain.pdf*
- **Purpose:** Give the literature review a problem-driven map matching Sections
  2.1--2.4, then lead naturally to the three gaps in Section 2.5.
- **Suggested caption:** *Problem-driven organisation of the related work and
  the resulting research gaps addressed in this thesis.*
- **Composition:** Four horizontal stages: directional V2I alignment/tracking;
  sensing-assisted beam prediction; distributed cooperative perception;
  target-to-user association and association-aware evaluation.  At the right,
  collect the three research gaps: distributed target-level sensing evidence,
  measurement-anchored UE--track association, and rate--overhead evaluation
  after association.
- **Generation prompt:**

  > Design a restrained horizontal academic taxonomy diagram for a thesis
  > related-work chapter on sensing-assisted V2I beam management.  Use four
  > large left-to-right stages connected by arrows: directional beam alignment
  > and tracking; sensing-assisted beam prediction; distributed cooperative
  > perception; target-to-user association with communication-aware evaluation.
  > Give each stage one simple line icon: radio beam, sensor, multi-node
  > bird's-eye-view map, and VUE-to-track link.  At the far right, show three
  > compact research-gap cards leading to one thesis-positioning card.  Leave
  > blank label areas for later typesetting rather than generating small text.
  > Use navy, teal, charcoal, and a restrained orange accent; white background;
  > thin connectors; flat vector style; no gradients, no decorative images, no
  > equations, and no crowded literature logos.  Aspect ratio 16:9.

## Figure 3.1 --- Target-BS-centred network and sensing topology

- **Priority:** Essential
- **Insertion point:** Chapter 3, after the third paragraph of Network
  Architecture and before Multimodal and Distributed Sensing Model.
- **Filename:** *figures/ch3_network_sensing_topology.pdf*
- **Purpose:** Defines the local service scope and prevents the mistaken
  interpretation that distributed sensing implies distributed serving-cell
  control.
- **Suggested caption:** *Target-BS-centred local V2I architecture:
  neighbouring sensing nodes provide complementary camera observations, whereas
  the target BS alone performs VUE-specific beam management and owns the local
  ISAC point cloud.*
- **Composition:** A top-down local service region with target BS, neighbouring
  SNs, physical vehicles, a subset of active VUEs, camera arrows converging at
  target-BS BEV fusion, and a local point cloud at only the BS.  Only target BS
  emits SSB/CSI-RS/downlink beams.
- **Generation prompt:**

  > Create a top-down vector-style system topology for an academic V2I
  > communications thesis.  Show a simple multi-lane road inside one clearly
  > bounded local service region.  Place one target base station in navy blue at
  > the roadside; it has compact camera icons, a violet local ISAC point-cloud
  > icon, and narrow blue downlink radio beams to orange active vehicle UEs.
  > Place two or three neighbouring sensing nodes in teal around the road; each
  > has cameras and sends only green observation arrows toward the target
  > base-station BEV fusion point.  Do not draw service beams from sensing
  > nodes.  Show several charcoal physical vehicles, with only some marked as
  > orange VUEs.  Include one partially occluded vehicle.  Add a small
  > bird's-eye-view grid inset at the target BS receiving camera and point-cloud
  > inputs.  Use clean flat icons, thin arrows, sparse labels or blank label
  > placeholders, navy-teal-violet-orange-charcoal palette, white background,
  > no gradients, no photorealism, and no global cross-cell identity links.
  > Aspect ratio 16:9.

## Figure 3.2 --- NR-oriented timing and beam-management procedure

- **Priority:** Essential
- **Insertion point:** Chapter 3, after the final paragraph of Timing and
  Measurements and before Beam Selection and Precoding.
- **Filename:** *figures/ch3_beam_management_timing.pdf*
- **Purpose:** Explains the sensor/radio time relation and makes clear that
  sensing reduces only the CSI-RS candidate measurement step.
- **Suggested caption:** *NR-oriented sensing-assisted beam-management
  procedure.  SSB and CSI-RS measurements anchor or recover association, while
  reliable current sensing evidence restricts only the CSI-RS candidate set.*
- **Composition:** Two aligned timelines.  Upper: frame/slot background, SSB
  sweep, CSI-RS candidates, VUE feedback, effective CSI, RZF precoding, data.
  Lower: observation, BEV target/beam distribution, track update.  A decision
  diamond routes reliable current association to Top-\(K_{\mathrm{scan}}\);
  otherwise it selects conventional refinement.  Both paths merge before
  measured service-beam selection.
- **Generation prompt:**

  > Produce a precise, clean academic timeline diagram for an NR-oriented
  > sensing-assisted beam-management procedure in V2I.  Use two horizontally
  > aligned timelines on a white background.  Upper radio timeline: a lightly
  > shaded radio frame and slot grid, then a coarse SSB sweep, CSI-RS candidate
  > measurement, VUE feedback, effective CSI, RZF precoding, and data
  > transmission.  Lower sensing timeline: multimodal observation, BEV target
  > detections with beam-quality distributions, and multi-object track update.
  > Connect the timelines at an initial-access or reassociation event, where SSB
  > and CSI-RS measurements establish a UE-to-track association.  At a later
  > maintenance epoch, show one decision diamond for current reliable
  > association: a blue-green path selects a short Top-K CSI-RS candidate list;
  > a muted red or grey path selects conventional refinement.  Both paths merge
  > before a measured service-beam selection block.  Use flat vector elements,
  > navy and teal for normal flow, orange for VUE feedback, violet for sensing
  > geometry, sparse large text placeholders only, no protocol-stack details,
  > and no gradients.  Aspect ratio 16:9.

## Figure 4.1 --- Overall framework and information boundaries

- **Priority:** Essential
- **Insertion point:** Chapter 4, in Framework Architecture, after the
  introductory paragraph and before the four-stage enumeration.
- **Filename:** *figures/ch4_framework_overview.pdf*
- **Purpose:** Central method figure.  It should be the reference for the
  reader while progressing through Sections 4.2--4.4.
- **Suggested caption:** *Overview of the proposed sensing-assisted
  beam-management framework.  Perception and tracking retain unbound
  physical-target evidence; conventional measurements establish a VUE--track
  association before reliable sensing-derived CSI-RS candidates are used.*
- **Composition:** Five stages: inputs; BEV fusion plus joint outputs; CV/CT IMM
  physical tracking; event-triggered measurement and association; reliability
  gate, candidate/fallback, actual CSI-RS measurement, service beam, RZF/data.
  Visually group stages 1--3 as sensing and 4--5 as communication.
- **Generation prompt:**

  > Create the central overview diagram for a communications thesis method
  > called distributed multimodal sensing-assisted beam management.  Use a
  > clean left-to-right flat vector pipeline on a white background with five
  > major stages.  Stage 1: target-base-station multiview cameras, neighbouring
  > sensing-node cameras, and one local ISAC point cloud.  Stage 2: calibrated
  > bird's-eye-view fusion followed by joint vehicle detection and a per-target
  > 192-way beam-quality distribution glyph.  Stage 3: a CV and CT two-branch
  > IMM tracker producing physical tracks only; visually separate tracks from
  > UE identities.  Stage 4: event-triggered conventional SSB and CSI-RS
  > measurements feeding a one-to-one UE-to-track association block with an
  > unmatched option.  Stage 5: reliability gate; reliable current association
  > leads to a short CSI-RS candidate set, otherwise conventional-refinement
  > fallback; both paths use actual CSI-RS measurement before measured
  > service-beam selection, RZF precoding, and data-rate evaluation.  Group
  > stages 1--3 as sensing and stages 4--5 as communication.  Use navy for
  > radio blocks, teal/green for cameras, violet for ISAC, charcoal for physical
  > tracks, orange for VUEs, and dashed muted-red fallback arrows.  Use simple
  > icons, thin connectors, large blank label areas, no equations, no
  > photorealism, no gradients, and no tiny text.  Aspect ratio 16:9.

## Figure 4.2 --- Distributed multimodal BEV perception and joint outputs

- **Priority:** Essential
- **Insertion point:** Chapter 4, at the end of Multimodal BEV Representation,
  immediately before Joint Detection and Beam-Quality Prediction.
- **Filename:** *figures/ch4_bev_fusion_joint_prediction.pdf*
- **Purpose:** Shows why distributed camera views and the BS-local point cloud
  fuse before target-level decoding, and why one BEV feature map serves two
  outputs.
- **Suggested caption:** *Distributed visual observations and the BS-local ISAC
  point cloud are aligned in a target-BS-centred BEV representation, from which
  joint vehicle detection and per-target beam-quality prediction are decoded.*
- **Generation prompt:**

  > Draw a clean neural-architecture-style academic figure showing distributed
  > multimodal BEV perception for V2I beam prediction.  On the left, show
  > several small camera-view icons from a target base station and neighbouring
  > sensing nodes.  Transform them into aligned bird's-eye-view feature tiles,
  > then aggregate the node features with small availability-mask symbols.  In
  > parallel, show a sparse violet point cloud from the target base station
  > encoded into the same BEV grid.  Merge the visual and geometric BEV features
  > into one shared square BEV feature map.  Split this map into two output
  > heads: a vehicle-centre heatmap plus target attributes, and a dense
  > 192-channel beam-score map.  At two detected vehicle centres, sample the
  > beam-score map and show two different compact ranked-distribution glyphs.
  > Make it visually clear that outputs are physical targets, not UE identities.
  > Use flat vector blocks, teal/green for cameras, violet for point cloud, navy
  > for fusion and heads, charcoal for targets, white background, minimal label
  > placeholders, no equations, no gradients, and no photorealism.  Aspect ratio
  > 16:9.

## Figure 4.3 --- Distributional beam supervision for candidate ranking

- **Priority:** Useful
- **Insertion point:** Chapter 4, in Distributional Beam Supervision, after
  the paragraph introducing the soft target distribution and before the complete
  joint loss.
- **Filename:** *figures/ch4_distributional_beam_supervision.pdf*
- **Purpose:** The loss equations are visually dense; this comparison explains
  why a distribution is more useful than only a strongest-beam label.
- **Suggested caption:** *Distributional beam supervision preserves the
  relative quality of multiple CSI beams, supporting candidate ranking and a
  confidence-aware measurement decision.*
- **Generation prompt:**

  > Create a compact vector-style explanatory diagram for distributional
  > beam-quality supervision in a wireless communications thesis.  Compare a
  > physical CSI beam-power profile with a predicted per-target beam-quality
  > distribution.  Use two rows of small abstract ranked bar charts, not
  > literal 192 individual bars.  Transform the physical profile into a soft
  > target distribution, then connect target and prediction to two simple loss
  > blocks: distribution matching and ranking consistency.  On the right, show
  > a short Top-K candidate list retaining several near-optimal beams, contrasted
  > with a subtle one-hot strongest-beam icon that discards alternatives.  Use
  > navy for model output, violet for physical quality, orange only for selected
  > candidates, white background, flat academic infographic style, no equations,
  > no tiny generated text, and no gradients.  Aspect ratio 3:2.

## Figure 4.4 --- IMM-based multi-object tracking

- **Priority:** Recommended
- **Insertion point:** Chapter 4, after the introductory paragraph of IMM-Based
  Multi-Object Tracking and before Motion Models.
- **Filename:** *figures/ch4_imm_tracking.pdf*
- **Purpose:** Separates the role of IMM tracking from UE association before the
  reader encounters the detailed CV/CT and filtering recursions.
- **Suggested caption:** *IMM-based tracking maintains unbound physical-target
  states by combining constant-velocity and coordinated-turn hypotheses with
  gated detection--track assignment.*
- **Generation prompt:**

  > Create a clean loop-style flow diagram for IMM-based multi-object tracking
  > in a vehicular sensing thesis.  Start with previous physical tracks in a
  > bird's-eye-view coordinate frame.  Split each track into a constant-velocity
  > branch and a coordinated-turn branch, with small probability weights and a
  > mixing block.  Show predicted states with uncertainty ellipses.  Feed current
  > BEV vehicle detections into an innovation-gating block, then a small
  > one-to-one Hungarian assignment matrix.  Merge matched detections into
  > updated physical tracks carrying position, velocity, confidence, observation
  > history, and a beam-distribution glyph.  Show an unmatched track continuing
  > as a grey prediction, with a prohibition icon indicating that prediction
  > alone cannot create a formal reduced CSI-RS candidate.  Do not show UE
  > identities.  Use charcoal for tracks, navy for filter blocks, teal for
  > detections, violet for uncertainty, grey for unmatched predictions, flat
  > vector style, white background, no equations, no gradients, and sparse text
  > placeholders.  Aspect ratio 16:9.

## Figure 4.5 --- Measurement-assisted association and reliable candidate policy

- **Priority:** Essential
- **Insertion point:** Chapter 4, after the opening paragraph of
  Measurement-Assisted Target-to-User Association and before Initial Association
  from Beam Measurements.
- **Filename:** *figures/ch4_association_and_candidate_policy.pdf*
- **Purpose:** The most distinctive method figure.  It demonstrates that
  association is communication-anchored and that a predicted distribution never
  directly selects a service beam.
- **Suggested caption:** *Conventional SSB/CSI-RS measurements anchor
  one-to-one UE--track association; only an accepted, currently observed,
  reliable association permits sensing-derived CSI-RS candidates.*
- **Composition:** A top association panel and a bottom candidate-policy panel.
  The first maps VUE beam measurements and track distributions through
  SSB-parent feasibility, beam-likelihood costs, Hungarian assignment, and an
  unmatched option.  The second maps acceptance and reliability evidence to
  Top-\(K_{\mathrm{scan}}\) or conventional refinement; both paths join at
  actual CSI-RS measurement and measured service-beam selection.
- **Generation prompt:**

  > Design a two-panel top-to-bottom academic flow diagram for
  > measurement-assisted target-to-user association in a multi-vehicle V2I
  > network.  Top panel: orange communication VUEs provide conventional
  > measurements, represented by one serving SSB glyph and one measured CSI-RS
  > beam glyph.  Several charcoal currently observed perception tracks provide
  > predicted beam-quality-distribution glyphs.  Connect them through an
  > SSB-parent consistency filter and a compact bipartite cost matrix with a
  > Hungarian one-to-one assignment block and a dummy unmatched option.  Show
  > accepted links in blue-green and ambiguous or rejected links as muted red
  > dashed links.  Bottom panel: an accepted UE-to-track link enters a
  > reliability gate checking current observation, association confidence, hint
  > age, and beam-score concentration.  The yes branch gives a short Top-K
  > CSI-RS candidate list; the no branch gives conventional refinement.  Both
  > branches join at actual CSI-RS measurement and measured service-beam
  > selection.  Make clear that a neural distribution does not directly select
  > the service beam.  Use flat vector shapes, navy radio blocks, orange VUEs,
  > charcoal tracks, violet distributions, blue-green reliable path, muted-red
  > fallback, white background, no formulas, no gradients, and no tiny text.
  > Aspect ratio 4:3.

## Deliberately omitted or deferred figures

- **No separate Chapter 1 contributions graphic.** Figure 1.1 already expresses
  the three contributions as one causal chain.  Another contribution diagram
  would repeat Figure 4.1.
- **No separate Chapter 3 problem-formulation flowchart.** The formal
  interfaces are visualised operationally in Figures 4.1 and 4.5; another
  rendering at the end of Chapter 3 would be redundant.
- **No full 5G NR frame-structure drawing.** The thesis uses an NR-oriented
  resource abstraction, not a standard-compliant full-stack simulation.  Figure
  3.2 should show timing and measurement relations only.
- **No raw ISAC signal-processing chain.** The point cloud is an available
  BS-local observation.  A detailed delay--Doppler or waveform-receiver figure
  would suggest an unclaimed contribution.

## Practical production order

1. Figure 3.1 establishes the visual vocabulary.
2. Figure 1.1 reuses the roadside-scene assets.
3. Figure 4.1 is the central framework figure.
4. Figure 4.5 explains the distinctive association contribution.
5. Figure 3.2 clarifies protocol timing.
6. Figure 4.2 and Figure 4.4 explain the two main sensing-side modules.
7. Add Figures 2.1 and 4.3 when page budget permits.

Before inserting a figure, convert it to vector PDF where possible; replace
generated labels with proofread thesis terminology; and ensure the caption
states the figure's claim without repeating the surrounding prose.
