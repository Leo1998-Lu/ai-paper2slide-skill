#!/usr/bin/env python3
"""Inspect a LaTeX paper project and produce a visual source manifest.

The script is intentionally lightweight and dependency-minimal so a future
ChatGPT runtime can use it before building a slide deck. It scans .tex files,
finds figure/table environments, captures labels/captions/includegraphics
paths, resolves likely asset files, and writes JSON.

Usage:
  python scripts/inspect_latex_assets.py /path/to/latex_project --output visual_source_manifest.json
  python scripts/inspect_latex_assets.py paper_source.zip --output visual_source_manifest.json
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import tarfile
import tempfile
import zipfile
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

GRAPHIC_EXTS = [".pdf", ".png", ".jpg", ".jpeg", ".eps", ".svg", ".tif", ".tiff"]

BEGIN_ENV_RE = re.compile(r"\\begin\{(?P<env>figure\*?|table\*?)\}")
END_ENV_RE = re.compile(r"\\end\{(?P<env>figure\*?|table\*?)\}")
CAPTION_RE = re.compile(r"\\caption(?:\[[^\]]*\])?\{", re.DOTALL)
LABEL_RE = re.compile(r"\\label\{([^{}]+)\}")
INCLUDEGRAPHICS_RE = re.compile(
    r"\\includegraphics(?:\s*\[[^\]]*\])?\s*\{([^{}]+)\}", re.DOTALL
)
SECTION_RE = re.compile(r"\\(section|subsection|subsubsection)\*?\{([^{}]+)\}")
INPUT_RE = re.compile(r"\\(?:input|include)\{([^{}]+)\}")
DOCUMENTCLASS_RE = re.compile(r"\\documentclass")
BEGIN_DOCUMENT_RE = re.compile(r"\\begin\{document\}")


@dataclass
class VisualRecord:
    id: str
    type: str
    tex_file: str
    start_line: int
    end_line: int
    label: Optional[str]
    caption: Optional[str]
    section: Optional[str]
    includegraphics: List[str]
    resolved_assets: List[str]
    status: str
    slide_image_allowed: bool
    notes: List[str]


def strip_latex_comments(text: str) -> str:
    lines = []
    for line in text.splitlines():
        # Remove unescaped % comments.
        out = []
        escaped = False
        for ch in line:
            if ch == "\\" and not escaped:
                escaped = True
                out.append(ch)
                continue
            if ch == "%" and not escaped:
                break
            out.append(ch)
            escaped = False
        lines.append("".join(out))
    return "\n".join(lines)


def clean_latex_inline(text: str) -> str:
    text = re.sub(r"\\[a-zA-Z]+\*?(?:\[[^\]]*\])?", "", text)
    text = text.replace("{", "").replace("}", "")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_braced(text: str, open_brace_index: int) -> Tuple[str, int]:
    """Return content inside a balanced {...} starting at an opening brace."""
    depth = 0
    chars: List[str] = []
    for i in range(open_brace_index, len(text)):
        ch = text[i]
        if ch == "{" and (i == 0 or text[i - 1] != "\\"):
            depth += 1
            if depth == 1:
                continue
        elif ch == "}" and (i == 0 or text[i - 1] != "\\"):
            depth -= 1
            if depth == 0:
                return "".join(chars), i + 1
        if depth >= 1:
            chars.append(ch)
    return "".join(chars), len(text)


def extract_caption(env_text: str) -> Optional[str]:
    match = CAPTION_RE.search(env_text)
    if not match:
        return None
    content, _ = extract_braced(env_text, match.end() - 1)
    return clean_latex_inline(content)


def find_tex_files(root: Path) -> List[Path]:
    return sorted(p for p in root.rglob("*.tex") if p.is_file())


def score_main_tex(path: Path, text: str) -> int:
    score = 0
    if DOCUMENTCLASS_RE.search(text):
        score += 10
    if BEGIN_DOCUMENT_RE.search(text):
        score += 10
    if "\\title" in text:
        score += 2
    if "\\maketitle" in text:
        score += 2
    if path.name.lower() in {"main.tex", "paper.tex", "ms.tex", "manuscript.tex"}:
        score += 3
    return score


def detect_main_tex(root: Path, tex_files: List[Path]) -> Optional[Path]:
    scored = []
    for p in tex_files:
        try:
            text = p.read_text(errors="ignore")
        except Exception:
            continue
        scored.append((score_main_tex(p, text), p))
    if not scored:
        return None
    scored.sort(key=lambda x: (x[0], -len(str(x[1]))), reverse=True)
    return scored[0][1]


def current_section_at(lines: List[str], line_idx: int) -> Optional[str]:
    current = None
    for i in range(0, min(line_idx + 1, len(lines))):
        m = SECTION_RE.search(lines[i])
        if m:
            current = clean_latex_inline(m.group(2))
    return current


def resolve_graphic(root: Path, tex_dir: Path, graphic_path: str) -> List[str]:
    raw = graphic_path.strip()
    candidates: List[Path] = []
    base_paths = [tex_dir / raw, root / raw]
    for base in base_paths:
        if base.suffix:
            candidates.append(base)
        else:
            candidates.extend(base.with_suffix(ext) for ext in GRAPHIC_EXTS)
    # Also search by basename as fallback.
    basename = Path(raw).name
    if basename:
        for p in root.rglob(basename + "*"):
            if p.suffix.lower() in GRAPHIC_EXTS:
                candidates.append(p)
    out = []
    seen = set()
    for c in candidates:
        try:
            rp = c.resolve()
        except Exception:
            continue
        if rp.exists() and rp.is_file() and str(rp) not in seen:
            seen.add(str(rp))
            out.append(os.path.relpath(rp, root))
    return out


def line_number_for_offset(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def extract_envs_from_tex(root: Path, tex_file: Path, counters: Dict[str, int]) -> List[VisualRecord]:
    raw = tex_file.read_text(errors="ignore")
    text = strip_latex_comments(raw)
    lines = text.splitlines()
    records: List[VisualRecord] = []
    pos = 0
    while True:
        start_match = BEGIN_ENV_RE.search(text, pos)
        if not start_match:
            break
        env = start_match.group("env")
        end_match = re.search(r"\\end\{" + re.escape(env) + r"\}", text[start_match.end():])
        if not end_match:
            pos = start_match.end()
            continue
        env_start = start_match.start()
        env_end = start_match.end() + end_match.end()
        env_text = text[env_start:env_end]
        start_line = line_number_for_offset(text, env_start)
        end_line = line_number_for_offset(text, env_end)
        visual_type = "figure" if env.startswith("figure") else "table"
        counters[visual_type] = counters.get(visual_type, 0) + 1
        vid = f"{visual_type}_{counters[visual_type]:03d}"
        labels = LABEL_RE.findall(env_text)
        graphics = [g.strip() for g in INCLUDEGRAPHICS_RE.findall(env_text)]
        resolved = []
        for g in graphics:
            resolved.extend(resolve_graphic(root, tex_file.parent, g))
        notes = []
        if visual_type == "figure" and not graphics:
            notes.append("figure environment has no includegraphics; may be tikz, subfile, or algorithmic figure")
        if graphics and not resolved:
            notes.append("includegraphics paths were found but no source asset resolved")
        status = "source-anchored" if (visual_type == "table" or resolved) else "needs-review"
        slide_image_allowed = bool(visual_type == "figure" and resolved and status == "source-anchored")
        section = current_section_at(lines, max(start_line - 1, 0))
        records.append(
            VisualRecord(
                id=vid,
                type=visual_type,
                tex_file=os.path.relpath(tex_file, root),
                start_line=start_line,
                end_line=end_line,
                label=labels[0] if labels else None,
                caption=extract_caption(env_text),
                section=section,
                includegraphics=graphics,
                resolved_assets=sorted(set(resolved)),
                status=status,
                slide_image_allowed=slide_image_allowed,
                notes=notes,
            )
        )
        pos = env_end
    return records


def unpack_if_archive(input_path: Path, workdir: Path) -> Path:
    if input_path.is_dir():
        return input_path
    suffixes = "".join(input_path.suffixes).lower()
    out = workdir / "source"
    out.mkdir(parents=True, exist_ok=True)
    if input_path.suffix.lower() == ".zip":
        with zipfile.ZipFile(input_path) as zf:
            zf.extractall(out)
        return out
    if suffixes.endswith(".tar.gz") or input_path.suffix.lower() == ".tar":
        with tarfile.open(input_path) as tf:
            tf.extractall(out)
        return out
    raise ValueError(f"Unsupported input: {input_path}. Provide a directory, .zip, .tar, or .tar.gz")


def build_manifest(source_root: Path) -> Dict[str, object]:
    tex_files = find_tex_files(source_root)
    main_tex = detect_main_tex(source_root, tex_files)
    counters: Dict[str, int] = {}
    visuals: List[VisualRecord] = []
    for tex in tex_files:
        try:
            visuals.extend(extract_envs_from_tex(source_root, tex, counters))
        except Exception as exc:
            visuals.append(
                VisualRecord(
                    id=f"parse_error_{len(visuals)+1:03d}",
                    type="parse_error",
                    tex_file=os.path.relpath(tex, source_root),
                    start_line=0,
                    end_line=0,
                    label=None,
                    caption=None,
                    section=None,
                    includegraphics=[],
                    resolved_assets=[],
                    status="parse-error",
                    slide_image_allowed=False,
                    notes=[str(exc)],
                )
            )
    sections = []
    for tex in tex_files:
        text = strip_latex_comments(tex.read_text(errors="ignore"))
        for m in SECTION_RE.finditer(text):
            sections.append(
                {
                    "level": m.group(1),
                    "title": clean_latex_inline(m.group(2)),
                    "tex_file": os.path.relpath(tex, source_root),
                    "line": line_number_for_offset(text, m.start()),
                }
            )
    return {
        "schema": "ai-paper2slide-visual-manifest-v1",
        "source_root": str(source_root),
        "main_tex": os.path.relpath(main_tex, source_root) if main_tex else None,
        "tex_file_count": len(tex_files),
        "sections": sections,
        "visuals": [asdict(v) for v in visuals],
        "summary": {
            "figures": sum(1 for v in visuals if v.type == "figure"),
            "tables": sum(1 for v in visuals if v.type == "table"),
            "source_anchored": sum(1 for v in visuals if v.status == "source-anchored"),
            "needs_review": sum(1 for v in visuals if v.status != "source-anchored"),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a LaTeX visual source manifest for paper-to-slide generation.")
    parser.add_argument("input", help="LaTeX project directory or source archive (.zip/.tar/.tar.gz)")
    parser.add_argument("--output", "-o", default="visual_source_manifest.json", help="Output JSON path")
    args = parser.parse_args()

    input_path = Path(args.input).expanduser().resolve()
    output_path = Path(args.output).expanduser().resolve()

    with tempfile.TemporaryDirectory(prefix="paper2slide_latex_") as tmp:
        root = unpack_if_archive(input_path, Path(tmp))
        manifest = build_manifest(root.resolve())
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
        print(json.dumps(manifest["summary"], indent=2))
        print(f"wrote {output_path}")


if __name__ == "__main__":
    main()
