#!/usr/bin/env python3
"""Validate that a slide visual map references valid LaTeX manifest entries.

Expected map JSON format:
{
  "slides": [
    {"slide": 5, "title": "Method overview", "visual_refs": ["figure_003", "table_001"]}
  ]
}

Strict mode enforces the AI Paper2Slide policy that slide images must come only
from resolved assets inside the user-provided LaTeX package. In strict mode:
- every referenced id must exist in the manifest;
- figure references must be source-anchored and have resolved_assets;
- pdf-crop, generated-image, external, web, memory, and user-asset statuses fail;
- table references are allowed when source-anchored because they can be recreated
  as editable slide tables from LaTeX source.

The script writes a compact quality report in Markdown.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List, Set

DISALLOWED_STATUSES = {
    "pdf-crop",
    "pdf-derived",
    "pdf-fallback",
    "external",
    "web",
    "generated-image",
    "memory",
    "user-asset",
    "needs-review",
    "parse-error",
}


def load_json(path: Path) -> Dict:
    return json.loads(path.read_text(encoding="utf-8"))


def normalized_refs(slide: Dict) -> List[str]:
    refs = slide.get("visual_refs", []) or []
    out: List[str] = []
    for ref in refs:
        if isinstance(ref, str):
            out.append(ref)
        elif isinstance(ref, dict) and "id" in ref:
            out.append(str(ref["id"]))
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate slide-to-visual references against a LaTeX source manifest.")
    parser.add_argument("manifest", help="visual_source_manifest.json")
    parser.add_argument("slide_map", help="slide_visual_map.json")
    parser.add_argument("--output", "-o", default="paper2slide_quality_report.md")
    parser.add_argument(
        "--strict-latex-images",
        action="store_true",
        help="Enforce that all figure images are source-anchored LaTeX package assets and reject PDF/external/generated images.",
    )
    args = parser.parse_args()

    manifest = load_json(Path(args.manifest))
    slide_map = load_json(Path(args.slide_map))
    visuals = {v["id"]: v for v in manifest.get("visuals", []) if "id" in v}
    valid_ids: Set[str] = set(visuals)
    missing: List[str] = []
    strict_failures: List[str] = []
    used: Set[str] = set()

    lines: List[str] = ["# Paper2Slide Quality Report", ""]
    lines.append("## Visual reference validation")
    lines.append("")
    lines.append(f"- Strict LaTeX-only image mode: {'enabled' if args.strict_latex_images else 'disabled'}")

    for slide in slide_map.get("slides", []):
        refs = normalized_refs(slide)
        slide_no = slide.get("slide", "unknown")
        for ref in refs:
            used.add(ref)
            if ref not in valid_ids:
                missing.append(f"slide {slide_no}: {ref}")
                continue
            if args.strict_latex_images:
                v = visuals[ref]
                vtype = v.get("type")
                status = v.get("status")
                assets = v.get("resolved_assets", []) or []
                if status in DISALLOWED_STATUSES:
                    strict_failures.append(f"slide {slide_no}: {ref} has disallowed status `{status}`")
                if vtype == "figure" and status != "source-anchored":
                    strict_failures.append(f"slide {slide_no}: {ref} is a figure but is not source-anchored")
                if vtype == "figure" and not assets:
                    strict_failures.append(f"slide {slide_no}: {ref} is a figure without resolved LaTeX package assets")
                if vtype not in {"figure", "table"}:
                    strict_failures.append(f"slide {slide_no}: {ref} has unsupported visual type `{vtype}`")

    lines.append(f"- Manifest visuals: {len(valid_ids)}")
    lines.append(f"- Visual references used in slides: {len(used)}")
    lines.append(f"- Missing references: {len(missing)}")
    lines.append(f"- Strict provenance failures: {len(strict_failures)}")

    if missing:
        lines.append("")
        lines.append("### Missing or unresolved references")
        for item in missing:
            lines.append(f"- {item}")

    if strict_failures:
        lines.append("")
        lines.append("### LaTeX-only image policy failures")
        for item in strict_failures:
            lines.append(f"- {item}")

    lines.append("")
    lines.append("## Used visual details")
    for ref in sorted(used):
        v = visuals.get(ref)
        if not v:
            continue
        cap = (v.get("caption") or "").strip()
        if len(cap) > 180:
            cap = cap[:177] + "..."
        assets = v.get("resolved_assets", []) or []
        asset_text = ", ".join(assets[:3]) if assets else "none"
        lines.append(
            f"- `{ref}`: {v.get('type')} | `{v.get('label')}` | {v.get('status')} | assets: {asset_text} | {cap}"
        )

    lines.append("")
    lines.append("## Mandatory output check")
    lines.append("- Default package must include `paper2slide_deck.pptx`.")
    lines.append("- Default package must include `paper2slide_speaker_script.docx` in English.")

    Path(args.output).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {args.output}")
    if missing or strict_failures:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
