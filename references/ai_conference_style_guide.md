# AI conference slide style guide

Use this reference for NeurIPS, ICML, ICLR, CVPR, ACL, KDD, WWW, AAAI, MICCAI, ACM MM, and similar venues.

## Overall look

- Aspect ratio: 16:9 widescreen.
- Background: white or near-white.
- Typography: modern sans-serif; large, readable text.
- Visual language: flat vector elements, thin borders, rounded rectangles, restrained shadows.
- Palette: one primary accent plus muted secondary colors. Use color to encode meaning, not decoration.
- Slide density: readable from the back of a conference room.

## Slide hierarchy

Each slide should have:

1. A claim headline at the top.
2. One dominant visual or one dominant comparison.
3. Small supporting text.
4. A takeaway/callout when useful.

Avoid generic titles such as “Method”, “Experiments”, or “Results”. Prefer claim titles:

- “A unified block mixes sequential and multi-field features.”
- “Source-anchored visual tokens prevent architecture mismatch.”
- “Ablations show both modules are necessary.”

## Recommended layouts

### Motivation
Two columns:

- Left: problem/friction in current methods.
- Right: what the proposed method changes.

### Method overview
Center the architecture figure. Add 3-5 callouts around the figure:

- Input representation.
- Core module.
- Training objective.
- Prediction head.
- Efficiency or scaling property.

### Module detail
Use zoom-in layout:

- Left: cropped or simplified module visual.
- Right: short explanation and equation if needed.
- Bottom: why this module matters.

### Experimental setup
Use compact cards:

- Dataset(s).
- Baselines.
- Metrics.
- Split/protocol.

### Main results
Use a table or bar chart with a single highlighted message:

- Highlight proposed model row.
- Add a callout arrow for the most important gain.
- Avoid showing every appendix metric.

### Ablation/scaling
Use a small table or chart. Focus on one comparison:

- Full model vs. removal variants.
- Performance vs. model size/compute/data.
- Robustness vs. missing inputs or domain shift.

### Conclusion
Use three takeaway cards:

- What was introduced.
- What improved.
- Why the result matters.

## Readability rules

- Minimum font size: 18 pt for body, 24 pt preferred.
- Headline: 32-44 pt.
- Keep bullets short: under 12 words where possible.
- Avoid more than 6 objects competing for attention.
- Do not place raw paper paragraphs on slides.
- Do not use screenshots of dense tables unless cropped and highlighted.

## AI-paper content priorities

For AI papers, the deck should make these clear:

1. Task and problem setting.
2. Why existing methods fail.
3. Core technical novelty.
4. Model architecture and data flow.
5. Training objective or inference algorithm.
6. Experimental protocol and baselines.
7. Main quantitative gains.
8. Ablation evidence.
9. Qualitative or diagnostic evidence.
10. Limitations and future directions.
