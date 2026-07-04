---
name: ai-paper2slide-skill
description: >-
  transform ai and scientific papers into conference-quality pptx slide decks and per-slide english speaker scripts. use when the user asks to convert a paper, pdf, arxiv manuscript, or latex source package into presentation slides for ai/ml venues such as neurips, icml, iclr, cvpr, acl, kdd, www, aaai, miccai, sigir, emnlp, or acm multimedia. this skill has two hard guarantees: slide images must only come from image assets included in the user-provided latex package, and every full paper-to-slide run must return at least two user-facing files by default: a powerpoint slide deck and a word document containing the english per-slide speaker script for an approximately 10-minute talk.
---

# AI Paper2Slide

## Non-negotiable guarantees

Use this skill to produce conference-quality presentations from AI/scientific papers while preserving strict visual provenance.

**Hard rule 1: LaTeX-only slide images.**  
Any bitmap/vector image placed into the slide deck must come from an image asset contained in the user-provided LaTeX source package and referenced, directly or indirectly, by that package. Do not use paper images from PDF screenshots, web search, prior conversations, memory, stock assets, generated images, or visually similar substitutes. Do not use user-provided images outside the LaTeX package as paper visuals. Logos or decorative images are also disallowed unless they are included in the LaTeX package or the user explicitly asks for non-paper branding and accepts that it is excluded from paper-visual provenance.

**Hard rule 2: Default two-file delivery.**  
Every full paper-to-slide request must return at least these two files by default:

1. `paper2slide_deck.pptx` — a 16:9 slide deck.
2. `paper2slide_speaker_script.docx` — an English per-slide speaker script, approximately 10 minutes total unless the user specifies another duration.

Also create `visual_source_manifest.json` and `paper2slide_quality_report.md` whenever possible, but never replace the PPTX or English DOCX with only markdown, outlines, screenshots, or a plan.

## Goal

Create a polished, top-tier-AI-conference presentation package from a research paper:

1. A `.pptx` slide deck with source-accurate architecture diagrams, result tables, ablations, and charts.
2. A `.docx` English speaker script, organized by slide, totaling approximately 10 minutes by default.
3. A visual source manifest that records where every important figure/table came from.
4. A quality report that verifies visual provenance, slide readability, and script timing.

## Inputs

Prefer these inputs, in order:

1. **Original LaTeX source archive** (`.zip`, `.tar`, `.tar.gz`) plus compiled paper PDF. This is required to place paper images in slides.
2. **Original LaTeX source archive only.** This is acceptable if the source compiles or contains enough assets and text to map figures/tables.
3. **Paper PDF only.** Use only for text understanding and slide planning. Do not place PDF-cropped paper images into the PPTX. Ask for the LaTeX package once when the requested deck needs figures or tables as images.
4. Optional venue, audience, talk length, preferred slide count, author names, target slide language, and user-selected figure/table labels.

If the user requests exact architecture/experiment visual placement and no LaTeX source is provided, ask for the source package once. If the user cannot provide it, continue only with text-based slides, editable shapes, or tables reconstructed from paper text, and record that no paper images were inserted because LaTeX assets were unavailable.

## Deliverables

Always produce these files when creating a full package:

- `paper2slide_deck.pptx`
- `paper2slide_speaker_script.docx`
- `visual_source_manifest.json`
- `paper2slide_quality_report.md`

The first two are mandatory user-facing deliverables. The manifest and quality report support verification and should be returned alongside them when available. Use descriptive names when the user supplies a paper title, but keep the same deliverable types.

## Workflow

### 1. Ingest and map the paper

When a LaTeX package is available:

1. Unpack the archive into a working directory.
2. Run `scripts/inspect_latex_assets.py` on the unpacked folder or archive.
3. Identify the main `.tex` file, section structure, figure environments, table environments, labels, captions, and `\includegraphics` source paths.
4. Build `visual_source_manifest.json` before drafting slides.
5. Mark each figure as slide-image-eligible only when it has at least one resolved asset path inside the LaTeX package.
6. Treat native LaTeX tables as source-anchored but not as slide images unless they are exported from the LaTeX source or recreated as editable slide tables.

When only a PDF is available:

1. Use the PDF for text extraction and paper understanding only.
2. Do not crop architecture figures, result tables, or qualitative examples from PDF pages into slides.
3. Use text-only summaries, editable schematic shapes, and editable tables if values can be extracted reliably.
4. Mark the quality report as `latex-source-missing` or `pdf-text-only-fallback`.

### 2. Enforce LaTeX-only visual provenance

For every image placed in the deck, verify all of the following:

- The image source appears in `visual_source_manifest.json`.
- The corresponding manifest entry has `status: source-anchored`.
- The manifest entry has a non-empty `resolved_assets` list.
- The resolved asset path is inside the user-provided LaTeX package.
- The slide visual map references the manifest `figure_id` or `table_id` used to create it.

Allowed slide visual sources:

1. Original image files referenced by `\includegraphics` and resolved inside the LaTeX package.
2. Converted versions of those original package assets, e.g. PDF/EPS/SVG converted to PNG at high resolution, with the original manifest ID preserved.
3. Native LaTeX tables recreated as editable PowerPoint tables using exact values from the source.
4. Diagrams redrawn with editable PowerPoint shapes only when the slide explicitly labels them as simplified/recreated and they are based on LaTeX source text, not external images.

Disallowed slide visual sources:

- PDF page crops or screenshots.
- Web images, stock images, icons, or screenshots.
- Images from previous conversations or memory.
- Images generated by an image model.
- User-uploaded images not included in the LaTeX package.
- Figures from other papers, repositories, blogs, or project pages.
- Placeholder diagrams that imply they are from the paper.

If a needed figure cannot be resolved from the LaTeX package, do not insert a substitute image. Instead, create a clean text/shape-based explanatory slide and list the unresolved figure in the quality report.

### 3. Plan a 10-minute AI-conference deck

Default to 11-13 slides. Use this structure unless the paper demands otherwise:

1. Title and one-sentence takeaway, 20-30 sec
2. Problem and motivation, 45-60 sec
3. Key insight / gap, 45 sec
4. Contributions, 45 sec
5. Method overview with source-anchored architecture figure if available, 75-90 sec
6. Core module 1, 60 sec
7. Core module 2 or training objective, 60 sec
8. Experimental setup / datasets / metrics, 60 sec
9. Main results, 75-90 sec
10. Ablation or scaling analysis, 60 sec
11. Qualitative / case study / visualization, 45-60 sec
12. Takeaways and limitations, 45 sec
13. Closing slide, 20-30 sec

If the target time differs, scale the number of slides and script timing proportionally.

### 4. Write slides in top-tier AI venue style

Follow `references/ai_conference_style_guide.md`.

Core rules:

- One message per slide.
- Use a strong slide headline that states the claim, not a generic section title.
- Keep body text sparse: usually 2-4 bullets, each under 12 words.
- Put the source-anchored architecture figure or result table at the visual center of the relevant slide when available.
- Use callout boxes to explain modules, losses, or result gains.
- Highlight only the numbers that support the slide claim.
- Prefer editable charts/tables when they are simple; use original LaTeX package assets when exact visual fidelity matters.
- Maintain consistent color coding across method, data, training, and results.

### 5. Generate the PowerPoint deck

When creating `.pptx`, follow the local slide-generation instructions available in the execution environment. Use a 16:9 widescreen deck.

Recommended slide design:

- White or very light background.
- Clean sans-serif typography.
- Large claim headline at top.
- Two-column layouts for motivation and experiments.
- Center-weighted architecture slides.
- Consistent footer with paper short title and slide number.
- Minimal decorative elements.
- No cluttered screenshots, low-resolution crops, unreadable tables, or non-LaTeX images.

### 6. Generate the English speaker script

Create `paper2slide_speaker_script.docx` with one section per slide. Follow `references/speaker_script_guide.md`.

Each slide script must include:

- Slide number and title.
- Target speaking time.
- 100-150 spoken English words for 60 seconds, scaled by timing.
- A natural transition to the next slide.
- Pronunciation-friendly descriptions of equations, model blocks, and metrics.

The total script should be approximately 10 minutes unless the user specifies another duration.

If the user requests Chinese, bilingual, or another language, still produce the default English script unless they explicitly request a different-only script. Additional language scripts may be returned as extra DOCX files, but the default `paper2slide_speaker_script.docx` remains English.

### 7. Validate before final delivery

Before returning files, create `paper2slide_quality_report.md` with:

- Confirmation that `paper2slide_deck.pptx` exists.
- Confirmation that `paper2slide_speaker_script.docx` exists and is in English.
- Slide count and total estimated speaking time.
- Visual source coverage: count of LaTeX-source images, recreated editable tables, and unresolved visuals.
- Confirmation that no PDF crops, web images, generated images, or non-LaTeX user images were inserted.
- Any missing LaTeX assets or unresolved references.
- Architecture slide verification: source path, caption, and label.
- Experiment slide verification: table/figure source path, caption, and label.
- Readability notes: minimum font size, dense slides, low-resolution images.

Run `scripts/validate_visual_sources.py --strict-latex-images` when a slide visual map is available.

## Important failure modes to avoid

- Do not use a wrong architecture figure because the paper has multiple model diagrams.
- Do not place an ablation table where the main result table is requested.
- Do not crop figures or tables from the PDF into the slide deck.
- Do not use images from the web, project pages, or previous conversations.
- Do not create only a markdown outline when the user asked for paper-to-slide output; return PPTX and English DOCX.
- Do not crop figure captions into slides unless the caption is intentionally used as evidence and comes from the LaTeX source.
- Do not overfill slides with paper paragraphs.
- Do not hallucinate metrics, datasets, baselines, or venue claims.
- Do not create a speech script that reads like the paper abstract; make it presentation-oriented.

## Included resources

- `scripts/inspect_latex_assets.py`: scan a LaTeX project/archive and produce a structured visual manifest.
- `scripts/validate_visual_sources.py`: check that a planned slide-to-visual mapping uses valid source-anchored figures/tables and can enforce LaTeX-only image policy.
- `references/latex_visual_localization.md`: detailed rules for exact figure/table localization and LaTeX-only image provenance.
- `references/ai_conference_style_guide.md`: slide design standards for AI top-conference talks.
- `references/speaker_script_guide.md`: timing and wording rules for the English script.
- `references/quality_checklist.md`: final pre-delivery checklist.
