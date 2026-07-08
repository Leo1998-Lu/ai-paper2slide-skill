import os
import json
import math
import urllib.request
import urllib.parse
from datetime import datetime, timezone
from collections import defaultdict

OWNER = os.environ.get("REPO_OWNER", "Leo1998-Lu")
REPO = os.environ.get("REPO_NAME", "ai-paper2slide-skill")
TOKEN = os.environ.get("GITHUB_TOKEN", "")

OUT_DIR = "assets"
SVG_PATH = os.path.join(OUT_DIR, "star-history.svg")
JSON_PATH = os.path.join(OUT_DIR, "star-history.json")


def fetch_stargazers(owner: str, repo: str):
    stars = []
    page = 1

    while True:
        url = (
            f"https://api.github.com/repos/"
            f"{urllib.parse.quote(owner)}/{urllib.parse.quote(repo)}"
            f"/stargazers?per_page=100&page={page}"
        )

        headers = {
            "Accept": "application/vnd.github.star+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "local-star-history-generator",
        }

        if TOKEN:
            headers["Authorization"] = f"Bearer {TOKEN}"

        req = urllib.request.Request(url, headers=headers)

        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))

        if not data:
            break

        for item in data:
            starred_at = item.get("starred_at")
            user = item.get("user", {}).get("login", "")
            if starred_at:
                stars.append({"user": user, "starred_at": starred_at})

        if len(data) < 100:
            break

        page += 1

    stars.sort(key=lambda x: x["starred_at"])
    return stars


def month_key(iso_time: str):
    dt = datetime.fromisoformat(iso_time.replace("Z", "+00:00"))
    return f"{dt.year}-{dt.month:02d}"


def build_monthly_series(stars):
    if not stars:
        now = datetime.now(timezone.utc)
        key = f"{now.year}-{now.month:02d}"
        return [(key, 0)]

    counts = defaultdict(int)
    for s in stars:
        counts[month_key(s["starred_at"])] += 1

    first = datetime.fromisoformat(stars[0]["starred_at"].replace("Z", "+00:00"))
    last = datetime.now(timezone.utc)

    months = []
    y, m = first.year, first.month
    while (y < last.year) or (y == last.year and m <= last.month):
        months.append(f"{y}-{m:02d}")
        m += 1
        if m == 13:
            y += 1
            m = 1

    total = 0
    series = []
    for k in months:
        total += counts[k]
        series.append((k, total))

    return series


def nice_max(value: int):
    if value <= 5:
        return 5
    magnitude = 10 ** int(math.log10(value))
    return math.ceil(value / magnitude) * magnitude


def generate_svg(series, total_stars):
    width = 900
    height = 460
    left = 72
    right = 32
    top = 48
    bottom = 72

    plot_w = width - left - right
    plot_h = height - top - bottom

    y_max = nice_max(max(v for _, v in series))
    n = len(series)

    def x_pos(i):
        if n == 1:
            return left + plot_w / 2
        return left + i * plot_w / (n - 1)

    def y_pos(v):
        return top + plot_h - (v / y_max) * plot_h

    points = [(x_pos(i), y_pos(v)) for i, (_, v) in enumerate(series)]

    line_points = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    area_points = (
        f"{left:.2f},{top + plot_h:.2f} "
        + line_points
        + f" {left + plot_w:.2f},{top + plot_h:.2f}"
    )

    y_ticks = 5
    y_grid = []
    for i in range(y_ticks + 1):
        val = round(y_max * i / y_ticks)
        y = y_pos(val)
        y_grid.append((val, y))

    label_indices = []
    if n <= 6:
        label_indices = list(range(n))
    else:
        for i in range(6):
            label_indices.append(round(i * (n - 1) / 5))
        label_indices = sorted(set(label_indices))

    last_x, last_y = points[-1]

    if total_stars == 0:
        empty_note = """
        <text x="450" y="230" text-anchor="middle" font-size="22" fill="#6b7280">
          No stars yet
        </text>
        <text x="450" y="260" text-anchor="middle" font-size="14" fill="#9ca3af">
          The chart will update automatically when the repository receives stars.
        </text>
        """
    else:
        empty_note = ""

    circles = ""
    if total_stars > 0:
        circles = f"""
        <circle cx="{last_x:.2f}" cy="{last_y:.2f}" r="5" fill="#2563eb"/>
        <text x="{last_x - 8:.2f}" y="{last_y - 14:.2f}" text-anchor="end" font-size="13" fill="#2563eb" font-weight="600">
          {total_stars} stars
        </text>
        """

    svg = f"""<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="{width}" height="{height}" rx="20" fill="#ffffff"/>
  <rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="19" stroke="#e5e7eb"/>

  <text x="{left}" y="30" font-family="Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="20" font-weight="700" fill="#111827">
    Star History
  </text>
  <text x="{width - right}" y="30" text-anchor="end" font-family="Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="13" fill="#6b7280">
    {OWNER}/{REPO}
  </text>

  <g font-family="Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif">
"""

    for val, y in y_grid:
        svg += f"""
    <line x1="{left}" y1="{y:.2f}" x2="{left + plot_w}" y2="{y:.2f}" stroke="#eef2f7"/>
    <text x="{left - 12}" y="{y + 4:.2f}" text-anchor="end" font-size="12" fill="#6b7280">{val}</text>
"""

    svg += f"""
    <line x1="{left}" y1="{top}" x2="{left}" y2="{top + plot_h}" stroke="#d1d5db"/>
    <line x1="{left}" y1="{top + plot_h}" x2="{left + plot_w}" y2="{top + plot_h}" stroke="#d1d5db"/>

    <polygon points="{area_points}" fill="#dbeafe" opacity="0.72"/>
    <polyline points="{line_points}" fill="none" stroke="#2563eb" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>

    {circles}
    {empty_note}
"""

    for idx in label_indices:
        k, _ = series[idx]
        x = x_pos(idx)
        svg += f"""
    <text x="{x:.2f}" y="{top + plot_h + 32}" text-anchor="middle" font-size="12" fill="#6b7280">{k}</text>
"""

    svg += f"""
    <text x="{left + plot_w / 2:.2f}" y="{height - 20}" text-anchor="middle" font-size="12" fill="#9ca3af">
      Generated from GitHub stargazer timestamps
    </text>
  </g>
</svg>
"""
    return svg


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    stars = fetch_stargazers(OWNER, REPO)
    series = build_monthly_series(stars)
    svg = generate_svg(series, len(stars))

    with open(SVG_PATH, "w", encoding="utf-8") as f:
        f.write(svg)

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(
            {
                "repository": f"{OWNER}/{REPO}",
                "total_stars": len(stars),
                "updated_at": datetime.now(timezone.utc).isoformat(),
                "stars": stars,
                "series": [{"month": k, "stars": v} for k, v in series],
            },
            f,
            indent=2,
            ensure_ascii=False,
        )

    print(f"Generated {SVG_PATH} with {len(stars)} stars.")


if __name__ == "__main__":
    main()
