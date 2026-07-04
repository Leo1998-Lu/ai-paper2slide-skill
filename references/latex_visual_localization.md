# LaTeX visual localization guide

Use this reference when the user supplies a LaTeX source package or asks for accurate architecture/table/chart placement.

## Hard visual-source policy

Images placed in the final slide deck must only come from image assets contained in the user-provided LaTeX package. The package asset must be visible in `visual_source_manifest.json` through a resolved `\includegraphics` path or another explicit source path discovered from the LaTeX project.

Do not use:

- PDF page screenshots or crops.
- Figures copied from the web, project pages, repositories, or prior conversations.
- AI-generated images.
- Stock icons or decorative images.
- User-uploaded images that are not inside the LaTeX source package.
- Visually similar replacements.

If a figure is important but not resolvable from the LaTeX package, create a text/shape-based explanation and list the missing asset in the quality report.

## Source priority

1. `\includegraphics` assets inside figure environments, resolved inside the LaTeX package.
2. Converted versions of those same assets, e.g. PDF/EPS/SVG to high-resolution PNG, preserving the original manifest id.
3. Native LaTeX tables inside table environments, recreated as editable PowerPoint tables.
4. TikZ/PGF diagrams compiled from the LaTeX source, only if the compiled output is derived from files in the package.
5. Text/shape-based recreations from source text, explicitly marked as recreated.

PDF crops are not allowed as slide images under this skill's strict default policy.

## Manifest fields to preserve

For every important figure/table, keep:

- `id`: stable manifest id, e.g. `figure_003`.
- `type`: figure or table.
- `tex_file`, `start_line`, `end_line`.
- `label`: LaTeX label, if present.
- `caption`: normalized caption.
- `section`: nearest section heading.
- `includegraphics`: raw included paths.
- `resolved_assets`: actual source files found inside the LaTeX package.
- `status`: source-anchored, needs-review, parse-error.
- `notes`: ambiguity, unresolved assets, or source constraints.

For slide images, `resolved_assets` must be non-empty and `status` must be `source-anchored`.

## Mapping paper content to slides

Use labels and captions, not file names alone.

Good mapping examples:

- Method overview slide: choose the figure whose caption names the proposed architecture, framework, pipeline, overview, model, or method.
- Core module slide: choose the subfigure/caption mentioning the exact module name.
- Main results slide: choose the table caption mentioning main comparison, benchmark, state of the art, or overall performance.
- Ablation slide: choose the table/figure caption mentioning ablation, component analysis, sensitivity, scaling, or efficiency.
- Qualitative slide: choose the figure caption mentioning visualization, case study, examples, generated samples, reconstruction, or attention maps.

## Common ambiguity checks

If multiple figures look relevant:

1. Prefer the one explicitly labeled as overview/architecture for the method slide.
2. Prefer the one in the Method section over a teaser figure unless the teaser is clearer for a talk.
3. Prefer main comparison tables in Experiments or Results over appendix tables.
4. Prefer ablation tables with the proposed model components named in rows/columns.
5. Never use a figure from a different paper, previous task, or PDF screenshot.

## Table handling

For simple result tables:

- Recreate as editable PowerPoint tables from LaTeX source.
- Keep exact metric names, dataset names, and values.
- Bold the best result and underline the second-best only if the paper does so or the user requests it.
- Add a short callout for the main gain.

For complex tables:

- Prefer a simplified editable table with the most important rows/columns.
- If exact table appearance is necessary, use only a source-derived table image generated from the LaTeX package, not a PDF crop.
- Highlight only the relevant rows/columns.
- Consider splitting into two slides if readability suffers.
