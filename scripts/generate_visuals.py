from __future__ import annotations

from pathlib import Path
from math import exp

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
ASSETS.mkdir(parents=True, exist_ok=True)

BG = "#ffffff"
TEXT = "#0f172a"
MUTED = "#475569"
BORDER = "#cbd5e1"
GRID = "#e2e8f0"
LEVELS = ["#94a3b8", "#60a5fa", "#34d399", "#fbbf24", "#a78bfa"]


def esc(text: str) -> str:
    return (text.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace('"', "&quot;"))


def write_svg(path: Path, width: int, height: int, body: str) -> None:
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img">
<rect width="100%" height="100%" fill="{BG}"/>
<style>
  text {{ font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; fill: {TEXT}; }}
  .muted {{ fill: {MUTED}; }}
  .title {{ font-weight: 700; }}
  .small {{ font-size: 13px; }}
  .label {{ font-size: 15px; font-weight: 600; }}
</style>
{body}
</svg>'''
    path.write_text(svg, encoding="utf-8")


def maturity_ladder() -> None:
    width, height = 1120, 600
    body = []
    body.append('<text x="560" y="46" text-anchor="middle" class="title" font-size="25">CMM software-process maturity</text>')
    body.append('<text x="560" y="74" text-anchor="middle" class="muted" font-size="14">From ad hoc execution to continuous improvement</text>')

    steps = [
        (1, "Initial", "Ad hoc", "Individual-dependent"),
        (2, "Repeatable", "Disciplined", "Project management"),
        (3, "Defined", "Standardized", "Organization-wide process"),
        (4, "Managed", "Measured", "Quantitative control"),
        (5, "Optimizing", "Improving", "Continuous learning"),
    ]
    x0, y0 = 90, 470
    step_w, step_h, rise = 180, 78, 82
    for idx, (n, name, tag, desc) in enumerate(steps):
        x = x0 + idx * step_w
        y = y0 - idx * rise
        body.append(f'<rect x="{x}" y="{y}" width="{step_w-14}" height="{step_h}" rx="15" fill="{LEVELS[idx]}" opacity="0.18" stroke="{LEVELS[idx]}" stroke-width="2"/>')
        body.append(f'<circle cx="{x+28}" cy="{y+27}" r="17" fill="{LEVELS[idx]}"/>')
        body.append(f'<text x="{x+28}" y="{y+33}" text-anchor="middle" font-size="14" font-weight="700" fill="#ffffff">{n}</text>')
        body.append(f'<text x="{x+55}" y="{y+26}" class="label">{esc(name)}</text>')
        body.append(f'<text x="{x+18}" y="{y+52}" class="small muted">{esc(tag)} · {esc(desc)}</text>')
        if idx < len(steps)-1:
            ax1 = x + step_w - 5
            ay1 = y + 35
            ax2 = x + step_w + 5
            ay2 = y - rise + 35
            body.append(f'<path d="M {ax1} {ay1} C {ax1+30} {ay1}, {ax2-30} {ay2}, {ax2} {ay2}" fill="none" stroke="{MUTED}" stroke-width="2" stroke-dasharray="5 5"/>')
            body.append(f'<path d="M {ax2-9} {ay2-5} L {ax2} {ay2} L {ax2-9} {ay2+5}" fill="none" stroke="{MUTED}" stroke-width="2"/>')

    body.append(f'<line x1="100" y1="548" x2="1010" y2="548" stroke="{BORDER}" stroke-width="2"/>')
    body.append(f'<text x="100" y="575" class="small muted">Lower predictability</text>')
    body.append(f'<text x="1010" y="575" text-anchor="end" class="small muted">Higher predictability, visibility and learning</text>')
    write_svg(ASSETS / "cmm-maturity-ladder.svg", width, height, "\n".join(body))


def gaussian_points(cx: float, cy: float, sx: float, sy: float, shift: float = 0.0) -> str:
    pts = []
    for p in range(101):
        t = -3 + p * 6 / 100
        x = cx + t * sx
        y = cy - exp(-0.5 * t * t) * sy + shift
        pts.append(f"{x:.1f},{y:.1f}")
    return " ".join(pts)


def process_capability() -> None:
    width, height = 1120, 760
    body = []
    body.append('<text x="560" y="42" text-anchor="middle" class="title" font-size="25">Process capability becomes more predictable with maturity</text>')
    body.append('<text x="560" y="69" text-anchor="middle" class="muted" font-size="14">Conceptual distributions — narrower variation and stronger target alignment at higher levels</text>')

    labels = [
        (1, "Initial", "Wide variation; targets are often missed"),
        (2, "Repeatable", "Plans become more realistic from prior experience"),
        (3, "Defined", "Standard processes reduce variation"),
        (4, "Managed", "Quantitative control further improves predictability"),
        (5, "Optimizing", "Feedback supports sustained improvement"),
    ]
    chart_x0, chart_x1 = 110, 665
    target_x = 535
    row_h = 126
    top = 105
    sigmas = [88, 74, 60, 49, 42]
    centers = [450, 472, 493, 510, 520]

    for r, (level, name, desc) in enumerate(labels):
        y = top + r * row_h
        base = y + 74
        body.append(f'<line x1="{chart_x0}" y1="{base}" x2="{chart_x1}" y2="{base}" stroke="{BORDER}"/>')
        body.append(f'<line x1="{target_x}" y1="{y+12}" x2="{target_x}" y2="{base}" stroke="{MUTED}" stroke-width="1.5" stroke-dasharray="4 4"/>')
        body.append(f'<text x="{target_x+7}" y="{y+24}" class="small muted">Target</text>')
        pts = gaussian_points(centers[r], base, sigmas[r]/3, 54)
        body.append(f'<polyline points="{pts}" fill="none" stroke="{LEVELS[r]}" stroke-width="3"/>')
        body.append(f'<text x="80" y="{y+44}" text-anchor="end" font-size="14" font-weight="700">L{level}</text>')
        body.append(f'<text x="705" y="{y+36}" class="label">{esc(name)}</text>')
        body.append(f'<text x="705" y="{y+60}" class="small muted">{esc(desc)}</text>')

    body.append(f'<text x="{(chart_x0+chart_x1)/2}" y="735" text-anchor="middle" class="small muted">Process result / schedule / cost performance →</text>')
    write_svg(ASSETS / "process-capability.svg", width, height, "\n".join(body))


def process_visibility() -> None:
    width, height = 1120, 520
    body = []
    body.append('<text x="560" y="42" text-anchor="middle" class="title" font-size="25">Management visibility increases as the process matures</text>')
    body.append('<text x="560" y="69" text-anchor="middle" class="muted" font-size="14">More standardization and measurement make progress, quality and problems easier to observe</text>')

    stages = [
        (1, "Initial", "Ad hoc", 0.20),
        (2, "Repeatable", "Plans & records", 0.38),
        (3, "Defined", "Standard process", 0.58),
        (4, "Managed", "Metrics & control", 0.79),
        (5, "Optimizing", "Feedback & learning", 0.96),
    ]
    x0, y0, bar_w, gap = 100, 165, 830, 58
    for idx, (lvl, name, desc, p) in enumerate(stages):
        y = y0 + idx * gap
        body.append(f'<text x="90" y="{y+20}" text-anchor="end" class="label">L{lvl}</text>')
        body.append(f'<rect x="{x0}" y="{y}" width="{bar_w}" height="30" rx="15" fill="#f1f5f9" stroke="{GRID}"/>')
        body.append(f'<rect x="{x0}" y="{y}" width="{bar_w*p:.0f}" height="30" rx="15" fill="{LEVELS[idx]}" opacity="0.82"/>')
        body.append(f'<text x="{x0+14}" y="{y+20}" font-size="13" font-weight="700">{esc(name)}</text>')
        body.append(f'<text x="{x0+bar_w+18}" y="{y+20}" class="small muted">{esc(desc)}</text>')

    body.append(f'<text x="{x0}" y="486" class="small muted">Low visibility</text>')
    body.append(f'<text x="{x0+bar_w}" y="486" text-anchor="end" class="small muted">High visibility</text>')
    body.append(f'<line x1="{x0}" y1="464" x2="{x0+bar_w}" y2="464" stroke="{BORDER}" stroke-width="2"/>')
    body.append(f'<path d="M {x0+bar_w-10} 459 L {x0+bar_w} 464 L {x0+bar_w-10} 469" fill="none" stroke="{BORDER}" stroke-width="2"/>')
    write_svg(ASSETS / "process-visibility.svg", width, height, "\n".join(body))


if __name__ == "__main__":
    maturity_ladder()
    process_capability()
    process_visibility()
    print("Generated:")
    for name in ["cmm-maturity-ladder.svg", "process-capability.svg", "process-visibility.svg"]:
        print(f"- {ASSETS / name}")
