# Paper2Slide quality checklist

Use this before returning final deliverables.

## Mandatory deliverables

- [ ] `paper2slide_deck.pptx` exists.
- [ ] `paper2slide_speaker_script.docx` exists.
- [ ] The speaker script is in English by default.
- [ ] The PPTX and English DOCX are both returned to the user.
- [ ] `visual_source_manifest.json` exists when LaTeX source is available.
- [ ] `paper2slide_quality_report.md` exists.

## LaTeX-only image provenance

- [ ] Every image inserted into the PPTX comes from the user-provided LaTeX package.
- [ ] Every slide image references a valid `figure_id` or `table_id` in `visual_source_manifest.json`.
- [ ] Every inserted figure image has `status: source-anchored` and non-empty `resolved_assets`.
- [ ] No PDF screenshot or page crop is used as a slide image.
- [ ] No web image, generated image, stock icon, previous-conversation image, or external user image is used.
- [ ] Unresolved architecture/result figures are reported instead of being substituted.
- [ ] Converted images preserve a pointer to the original LaTeX package asset.

## Source accuracy

- [ ] The architecture slide uses the correct source figure.
- [ ] Every experiment table/chart is traceable to a LaTeX caption, label, table environment, or resolved package asset.
- [ ] Main results and ablation results are not swapped.
- [ ] All metric values shown on slides match the paper.
- [ ] Any recreated table is based on source text and exact values.

## Deck quality

- [ ] The deck is 16:9.
- [ ] Slide count matches the target duration.
- [ ] Each slide has one main claim.
- [ ] Body text is sparse and readable.
- [ ] Architecture/result slides have clear visual hierarchy.
- [ ] Dense tables are simplified or split for readability.
- [ ] Color coding is consistent.
- [ ] Footer and slide numbers are consistent.

## Speaker script

- [ ] Each slide has target timing.
- [ ] Total speaking time is approximately 10 minutes unless specified otherwise.
- [ ] The script explains visuals naturally.
- [ ] Transitions are included.
- [ ] Claims are supported by the paper.
- [ ] The script does not introduce results or claims absent from the paper.

## Final package

- [ ] File names are clear and user-friendly.
- [ ] The quality report explicitly confirms LaTeX-only image compliance.
- [ ] Known limitations are stated honestly.
