from __future__ import annotations

import html
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.mart_builder import build_dashboard


WIDTH = 1440
HEIGHT = 860


def wrap(text: str, width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if len(candidate) <= width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def text_block(x: int, y: int, text: str, size: int, width: int, fill: str = "#e9f3ff", weight: str = "400") -> str:
    lines = wrap(text, width)
    tspans = []
    for idx, line in enumerate(lines):
        dy = "0" if idx == 0 else f"{size + 8}"
        tspans.append(
            f'<tspan x="{x}" dy="{dy}">{html.escape(line)}</tspan>'
        )
    return (
        f'<text x="{x}" y="{y}" fill="{fill}" font-family="Segoe UI, Arial, sans-serif" '
        f'font-size="{size}" font-weight="{weight}">{"".join(tspans)}</text>'
    )


def frame(title: str, subtitle: str, body: list[str], footer: str) -> str:
    body_markup = []
    y = 270
    for line in body:
        body_markup.append(text_block(80, y, f"• {line}", 30, 64))
        y += 88
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">
  <defs>
    <linearGradient id="bg" x1="0" x2="1" y1="0" y2="1">
      <stop offset="0%" stop-color="#09101d"/>
      <stop offset="100%" stop-color="#0b1628"/>
    </linearGradient>
    <linearGradient id="line" x1="0" x2="1">
      <stop offset="0%" stop-color="#37ff8b"/>
      <stop offset="100%" stop-color="#19c7ff"/>
    </linearGradient>
  </defs>
  <rect width="{WIDTH}" height="{HEIGHT}" fill="url(#bg)"/>
  <rect x="26" y="26" width="{WIDTH-52}" height="{HEIGHT-52}" rx="24" fill="none" stroke="url(#line)" stroke-width="2"/>
  <text x="80" y="112" fill="#37ff8b" font-family="Segoe UI, Arial, sans-serif" font-size="20" font-weight="700">Grant Compliance Evidence Desk</text>
  {text_block(80, 188, title, 54, 30, weight="700")}
  {text_block(80, 235, subtitle, 24, 78, fill="#b9c9e6")}
  {''.join(body_markup)}
  <text x="80" y="{HEIGHT-70}" fill="#9eb1d1" font-family="Segoe UI, Arial, sans-serif" font-size="20">{html.escape(footer)}</text>
</svg>"""


def write_asset(path: Path, markup: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(markup, encoding="utf-8")


if __name__ == "__main__":
    data = build_dashboard()
    top_grant = data["grant_rows"][0]
    top_gap = data["evidence_rows"][0]
    screenshots = ROOT / "screenshots"

    write_asset(
        screenshots / "01-overview-proof.svg",
        frame(
            "Grant readiness at a glance.",
            "Active grants, missing evidence packets, and funder-facing deliverable risk stay visible in one control surface.",
            [
                f"{data['grant_count']} active grants with average readiness {data['avg_readiness']}.",
                f"{data['missing_packets']} missing packets still need proof before closeout.",
                f"{top_grant['grant_name']} is currently the highest-readiness lane for {top_grant['funder_name']}.",
            ],
            "Synthetic proof render for README packaging.",
        ),
    )

    write_asset(
        screenshots / "02-evidence-gaps-proof.svg",
        frame(
            "Evidence gaps that need follow-up first.",
            "The desk ties each missing packet or amendment to the exact grant and next reporting obligation.",
            [
                f"{top_gap['grant_name']} still needs: {top_gap['next_gap']}.",
                "Budget amendment notes, board approvals, and program metrics are treated as one operator workflow.",
                "Program, finance, and development can review the same evidence posture without spreadsheet drift.",
            ],
            "Synthetic proof render for README packaging.",
        ),
    )

    write_asset(
        screenshots / "03-reporting-posture-proof.svg",
        frame(
            "Reporting posture before funder trust slips.",
            "Deliverable risk, owner readiness, and evidence posture stay inspectable before the next reporting window closes.",
            [
                f"Max deliverable risk is {data['max_deliverable_risk']} across the current portfolio.",
                "High-risk grants surface before late reporting becomes an executive surprise.",
                "This lane is designed for hosted preview and embedded nonprofit reporting modules.",
            ],
            "Synthetic proof render for README packaging.",
        ),
    )

    print(screenshots)
