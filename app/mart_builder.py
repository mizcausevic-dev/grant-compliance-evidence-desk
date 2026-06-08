# SPDX-License-Identifier: AGPL-3.0-or-later

from __future__ import annotations

import json
import sqlite3
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
WAREHOUSE = ROOT / "warehouse"


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    for script in [
        WAREHOUSE / "schema.sql",
        WAREHOUSE / "seed.sql",
        WAREHOUSE / "marts" / "mart_grant_readiness.sql",
        WAREHOUSE / "marts" / "mart_evidence_gaps.sql",
    ]:
        conn.executescript(script.read_text(encoding="utf-8"))
    return conn


def rows(conn: sqlite3.Connection, sql: str) -> list[dict[str, Any]]:
    return [dict(row) for row in conn.execute(sql).fetchall()]


def build_dashboard() -> dict[str, Any]:
    conn = connect()
    grant_rows = rows(
        conn,
        """
        SELECT *
        FROM mart_grant_readiness
        ORDER BY readiness_score DESC, deliverable_risk DESC, evidence_gaps DESC
        """,
    )
    evidence_rows = rows(conn, "SELECT * FROM mart_evidence_gaps")
    avg_readiness = round(sum(row["readiness_score"] for row in grant_rows) / len(grant_rows), 1)

    return {
        "generated_on": str(date.today()),
        "grant_count": len(grant_rows),
        "high_risk_grants": sum(1 for row in grant_rows if row["deliverable_risk"] >= 60),
        "missing_packets": sum(row["evidence_gaps"] for row in grant_rows),
        "avg_readiness": avg_readiness,
        "max_deliverable_risk": max(row["deliverable_risk"] for row in grant_rows),
        "grant_rows": grant_rows,
        "evidence_rows": evidence_rows,
    }


def status_badge(status: str) -> str:
    palette = {"green": "green", "yellow": "warn", "red": "bad"}
    tone = palette.get(status, "cyan")
    return f'<span class="status {tone}">{status.upper()}</span>'


def base_css() -> str:
    return """
    :root{
      --bg:#070a0f; --panel:#0b1220; --panel2:#0a1426;
      --line:rgba(120,255,170,.18); --line2:rgba(120,255,170,.10);
      --text:#e9f3ff; --muted:rgba(233,243,255,.72); --muted2:rgba(233,243,255,.55);
      --bert:#37ff8b; --bert2:#19c7ff; --warn:#ffcc66; --bad:#ff5c7a; --plum:#b88cff;
      --shadow:0 18px 60px rgba(0,0,0,.55);
      --mono:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,"Courier New",monospace;
      --sans:ui-sans-serif,system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;
    }
    *{box-sizing:border-box} html,body{height:100%}
    body{margin:0;font-family:var(--sans);color:var(--text);background:
      radial-gradient(1200px 600px at 20% -10%, rgba(55,255,139,.18), transparent 60%),
      radial-gradient(900px 520px at 90% 0%, rgba(25,199,255,.16), transparent 55%),
      radial-gradient(1000px 600px at 50% 110%, rgba(55,255,139,.10), transparent 60%),
      linear-gradient(180deg,#05070c 0%,#070a0f 35%,#05070c 100%);}
    .grid-bg{position:fixed;inset:0;pointer-events:none;opacity:.12;z-index:-1;background-image:
      linear-gradient(to right, rgba(55,255,139,.14) 1px, transparent 1px),
      linear-gradient(to bottom, rgba(55,255,139,.10) 1px, transparent 1px);
      background-size:46px 46px;mask-image: radial-gradient(900px 600px at 40% 10%, #000 60%, transparent 100%);}
    .wrap{max-width:1280px;margin:0 auto;padding:24px 22px 80px}
    .topbar{display:flex;justify-content:space-between;align-items:flex-start;gap:14px;border-bottom:1px solid var(--line2);padding-bottom:14px;margin-bottom:22px;font-family:var(--mono);font-size:11px;letter-spacing:.16em;color:var(--muted);text-transform:uppercase}
    .topbar .left{color:var(--bert)}
    .hero,.panel,.tablewrap{background:linear-gradient(180deg, rgba(11,18,32,.95), rgba(8,14,26,.92));border:1px solid var(--line);border-radius:22px;box-shadow:var(--shadow)}
    .herorow{display:grid;grid-template-columns:1.45fr .85fr;gap:18px} @media (max-width:1000px){.herorow{grid-template-columns:1fr}}
    .hero{padding:28px 28px 24px;border-top:2px solid var(--bert2)}
    .hero h1{font-size:64px;line-height:.95;margin:0 0 18px;font-weight:800;letter-spacing:-.5px}
    @media (max-width:700px){.hero h1{font-size:42px}}
    .hero p,.panel p{color:var(--muted);font-size:15px;line-height:1.55}
    .chiprow{display:flex;flex-wrap:wrap;gap:8px}
    .chip,.status,.notepill{font-family:var(--mono);font-size:11px;padding:7px 12px;border-radius:999px;border:1px solid var(--line);background:rgba(6,10,18,.4);color:var(--muted)}
    .side{display:flex;flex-direction:column;gap:14px}
    .panel{padding:18px}
    .panel .lbl,.section-note{font-family:var(--mono);font-size:10px;letter-spacing:.18em;text-transform:uppercase;color:var(--bert2)}
    .panel h3{margin:8px 0 6px;font-size:28px;line-height:1.02}
    .kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:12px} @media (max-width:900px){.kpis{grid-template-columns:repeat(2,1fr)}} @media (max-width:640px){.kpis{grid-template-columns:1fr}}
    .kpi,.card{border:1px solid var(--line);border-radius:16px;padding:16px;background:linear-gradient(180deg, rgba(11,18,32,.85), rgba(8,14,26,.65))}
    .kpi .v{font-family:var(--mono);font-size:28px;font-weight:700}
    .kpi .lbl{font-family:var(--mono);font-size:10px;letter-spacing:.18em;text-transform:uppercase;color:var(--muted);margin-top:6px}
    .kpi .h{font-size:12px;color:var(--muted);line-height:1.45;margin-top:8px}
    .green{color:var(--bert)} .cyan{color:var(--bert2)} .warn{color:var(--warn)} .plum{color:var(--plum)} .bad{color:var(--bad)}
    .section{margin-top:34px}
    .sh{display:flex;justify-content:space-between;align-items:baseline;gap:14px;padding-bottom:10px;border-bottom:1px solid var(--line2);margin-bottom:14px}
    .sh h2{margin:0;font-size:24px;font-weight:600}
    .sh .note{font-family:var(--mono);font-size:11px;color:var(--muted2);letter-spacing:.16em;text-transform:uppercase}
    .cards{display:grid;grid-template-columns:repeat(3,1fr);gap:14px} @media (max-width:1000px){.cards{grid-template-columns:1fr}}
    .card h3{margin:8px 0 8px;font-size:22px}
    .card .eyebrow{font-family:var(--mono);font-size:10px;letter-spacing:.18em;text-transform:uppercase;color:var(--bert)}
    table{width:100%;border-collapse:collapse} th,td{padding:13px 14px;text-align:left;font-size:13.5px;vertical-align:top}
    thead th{font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--muted2);border-bottom:1px solid var(--line);background:rgba(11,18,32,.5)}
    tbody td{color:var(--muted);border-bottom:1px solid var(--line2)} tbody tr:hover{background:rgba(55,255,139,.03)}
    .tablewrap{padding:0;overflow:hidden}
    .status{display:inline-block;padding:4px 9px;border-radius:6px;border:1px solid currentColor}
    .quote{margin-top:34px;border:1px solid rgba(55,255,139,.22);background:radial-gradient(700px 200px at 0% 0%, rgba(55,255,139,.10), transparent 60%),linear-gradient(180deg, rgba(11,18,32,.92), rgba(8,14,26,.88));border-radius:18px;padding:24px 26px}
    .quote .lbl{font-family:var(--mono);font-size:11px;color:var(--bert);letter-spacing:.22em;text-transform:uppercase}
    .quote .q{margin-top:12px;font-size:32px;line-height:1.25;font-weight:600;max-width:1000px}
    footer{margin-top:30px;padding-top:14px;border-top:1px dashed var(--line2);display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;font-family:var(--mono);font-size:11px;color:var(--muted2);letter-spacing:.08em}
    a{color:var(--bert2);text-decoration:none}
    """


def page(title: str, description: str, content: str, canonical: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <meta name="robots" content="index,follow">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{canonical}">
  <link rel="canonical" href="{canonical}">
  <style>{base_css()}</style>
</head>
<body>
  <div class="grid-bg"></div>
  <div class="wrap">{content}</div>
</body>
</html>"""


def overview_html(data: dict[str, Any]) -> str:
    readiness_rows = "".join(
        f"""
        <tr>
          <td><b>{row['grant_name']}</b><br><span class="section-note">{row['grant_id']} · {row['funder_name']}</span></td>
          <td>{row['readiness_score']}</td>
          <td>{row['evidence_gaps']}</td>
          <td>{row['deliverable_risk']}</td>
          <td>{status_badge(row['risk_status'])}</td>
        </tr>
        """
        for row in data["grant_rows"]
    )

    evidence_cards = "".join(
        f"""
        <div class="card">
          <div class="eyebrow">{row['grant_id']}</div>
          <h3>{row['grant_name']}</h3>
          <p>{row['next_gap']} still needs proof before the next funder-facing reporting cycle can close cleanly.</p>
          <p>{status_badge(row['risk_status'])}</p>
        </div>
        """
        for row in data["evidence_rows"]
    )

    return f"""
    <div class="topbar">
      <div class="left">grant evidence desk · nonprofit operator surface</div>
      <div class="right">
        <div>grants.kineticgain.com</div>
        <div>generated {data['generated_on']} · reporting and evidence posture</div>
      </div>
    </div>
    <div class="herorow">
      <section class="hero">
        <div class="chiprow">
          <span class="chip">Grant compliance</span>
          <span class="chip">evidence routing</span>
          <span class="chip">deliverable posture</span>
          <span class="chip">nonprofit ops</span>
        </div>
        <h1>Keep grant evidence, reporting cadence, and deliverable risk visible before funder trust starts to slip.</h1>
        <p>A nonprofit operator surface for grant managers, finance leads, and program owners who need evidence packets, reporting obligations, budget amendment readiness, and deliverable risk in one review-safe desk.</p>
        <div class="chiprow">
          <span class="notepill">/grant-lane/</span>
          <span class="notepill">/evidence-gaps/</span>
          <span class="notepill">/reporting-posture/</span>
        </div>
      </section>
      <aside class="side">
        <div class="panel">
          <div class="lbl">active grants</div>
          <h3 class="green">{data['grant_count']}</h3>
          <p>Current grant programs represented in the evidence and reporting desk.</p>
        </div>
        <div class="panel">
          <div class="lbl">avg readiness</div>
          <h3 class="cyan">{data['avg_readiness']}</h3>
          <p>Average readiness across the current funder reporting and compliance portfolio.</p>
        </div>
        <div class="panel">
          <div class="lbl">missing packets</div>
          <h3 class="warn">{data['missing_packets']}</h3>
          <p>Evidence packets still incomplete, draft, or waiting on policy or finance proof.</p>
        </div>
      </aside>
    </div>
    <section class="section">
      <div class="sh"><h2>Desk KPIs</h2><div class="note">nonprofit grant snapshot</div></div>
      <div class="kpis">
        <div class="kpi"><div class="v green">{data['grant_count']}</div><div class="lbl">tracked grants</div><div class="h">Funding lanes mapped into one evidence and reporting control surface.</div></div>
        <div class="kpi"><div class="v bad">{data['high_risk_grants']}</div><div class="lbl">high risk grants</div><div class="h">Programs most likely to slip on compliance, reporting, or amendment proof.</div></div>
        <div class="kpi"><div class="v plum">{data['missing_packets']}</div><div class="lbl">evidence gaps</div><div class="h">Packets still missing deliverable proof, budget notes, or board-ready narrative.</div></div>
        <div class="kpi"><div class="v warn">{data['max_deliverable_risk']}</div><div class="lbl">max deliverable risk</div><div class="h">Highest reporting and deliverable exposure across the active grant portfolio.</div></div>
      </div>
    </section>
    <section class="section">
      <div class="sh"><h2>Evidence gaps</h2><div class="note">what needs intervention</div></div>
      <div class="cards">{evidence_cards}</div>
    </section>
    <section class="section">
      <div class="sh"><h2>Grant readiness</h2><div class="note">desk output</div></div>
      <div class="tablewrap">
        <table>
          <thead><tr><th>Grant</th><th>Readiness</th><th>Evidence gaps</th><th>Deliverable risk</th><th>Status</th></tr></thead>
          <tbody>{readiness_rows}</tbody>
        </table>
      </div>
    </section>
    <section class="section">
      <div class="sh"><h2>Board questions this answers</h2><div class="note">funder exposure · budget · narrative</div></div>
      <div class="cards">
        <div class="card"><div class="eyebrow">exposure</div><h3>Which grants are most likely to miss a funder commitment?</h3><p>Deliverable risk, evidence gaps, and readiness scores show where funder trust is exposed before a late report, thin packet, or amendment surprise reaches leadership.</p></div>
        <div class="card"><div class="eyebrow">savings</div><h3>Where is evidence collection becoming duplicate work?</h3><p>The desk ties program metrics, finance notes, approvals, budget amendments, and deliverable proof together so grant teams do not rebuild the same packet every cycle.</p></div>
        <div class="card"><div class="eyebrow">investment</div><h3>Which reporting control should be strengthened first?</h3><p>High-risk grants show whether finance support, program instrumentation, approval tracking, or funder narrative production deserves the next operating investment.</p></div>
      </div>
    </section>
    <section class="section">
      <div class="sh"><h2>Evidence model</h2><div class="note">signal · proof · decision</div></div>
      <div class="tablewrap">
        <table>
          <thead><tr><th>Signal</th><th>Owner</th><th>Required proof</th><th>Decision supported</th></tr></thead>
          <tbody>
            <tr><td><b>Deliverable readiness</b></td><td>Grant Manager</td><td>Requirement, due date, source artifact, reviewer, submission posture</td><td>Submit, hold, or escalate funder packet</td></tr>
            <tr><td><b>Budget amendment pressure</b></td><td>Finance Lead</td><td>Variance note, board approval, funder communication, revised allocation</td><td>Approve amendment, reforecast, or contain spend</td></tr>
            <tr><td><b>Program metric support</b></td><td>Program Owner</td><td>Metric definition, cohort source, delivery note, evidence attachment</td><td>Use, qualify, or repair impact narrative</td></tr>
          </tbody>
        </table>
      </div>
    </section>
    <section class="quote">
      <div class="lbl">why this matters</div>
      <div class="q">Kinetic Gain Embedded tie-back: this repo proves the portfolio can ship nonprofit funding operator surfaces where grant evidence, reporting cycles, and amendment readiness stay inspectable in one place instead of fragmenting across finance, programs, and development.</div>
    </section>
    <footer>
      <span>grant-compliance-evidence-desk · Python evidence mart + static operator surface</span>
      <span><a href="/docs/">Docs</a> · <a href="/verification/">Verification</a></span>
    </footer>
    """


def generic_html(title: str, note: str, bullets: list[str]) -> str:
    items = "".join(f"<li>{bullet}</li>" for bullet in bullets)
    return f"""
    <div class="topbar">
      <div class="left">grant evidence desk · nonprofit workflow</div>
      <div class="right"><div>{title}</div></div>
    </div>
    <section class="hero">
      <div class="section-note">{note}</div>
      <h1>{title}</h1>
      <p>{" ".join(bullets)}</p>
      <ul style="color:var(--muted);line-height:1.8">{items}</ul>
      <p><a href="/">Return to overview</a></p>
    </section>
    """


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_site(out_dir: str | Path | None = None, domain: str = "grants.kineticgain.com") -> Path:
    data = build_dashboard()
    out = ROOT / "site" if out_dir is None else ROOT / Path(out_dir)
    out.mkdir(exist_ok=True)
    write(
        out / "index.html",
        page(
            "Grant Compliance Evidence Desk",
            "Nonprofit operator surface for grant evidence, reporting posture, budget amendments, and deliverable readiness.",
            overview_html(data),
            f"https://{domain}/",
        ),
    )
    write(
        out / "grant-lane" / "index.html",
        page(
            "Grant Lane",
            "Lane view for nonprofit grant readiness and owner posture.",
            generic_html(
                "Grant lane",
                "lane view",
                [
                    "Each grant lane keeps owner, funder, reporting cycle, and amendment posture visible.",
                    "The desk makes program, finance, and development dependencies readable at a glance.",
                    "This route keeps funder readiness tied to real evidence packets instead of status-only meetings.",
                ],
            ),
            f"https://{domain}/grant-lane/",
        ),
    )
    write(
        out / "evidence-gaps" / "index.html",
        page(
            "Evidence Gaps",
            "Evidence gap view for the grant compliance evidence desk.",
            generic_html(
                "Evidence gaps",
                "what is still missing",
                [
                    "Missing board approvals, budget amendments, attendance proof, and program metrics surface first.",
                    "The desk ties each gap back to the exact grant and next reporting commitment.",
                    "This keeps evidence follow-up operational instead of living in inbox residue.",
                ],
            ),
            f"https://{domain}/evidence-gaps/",
        ),
    )
    write(
        out / "reporting-posture" / "index.html",
        page(
            "Reporting Posture",
            "Reporting and deliverable posture view for nonprofit grant operations.",
            generic_html(
                "Reporting posture",
                "funder-facing readiness",
                [
                    "Deliverable risk and readiness stay visible before a funder report goes late or thin.",
                    "Program metrics, finance support, and compliance notes are treated as one operating layer.",
                    "The route proves the desk can explain grant posture to executives and auditors without overclaiming compliance.",
                ],
            ),
            f"https://{domain}/reporting-posture/",
        ),
    )
    write(
        out / "verification" / "index.html",
        page(
            "Verification",
            "Verification notes for the grant compliance evidence desk.",
            generic_html(
                "Verification",
                "release gate",
                [
                    "SQLite executes the schema, seed, and mart SQL scripts locally.",
                    "Python tests verify the dashboard summary, gap counts, and site output invariants.",
                    "A static Pages bundle publishes the resulting desk with robots, sitemap, and custom-domain support.",
                ],
            ),
            f"https://{domain}/verification/",
        ),
    )
    write(
        out / "docs" / "index.html",
        page(
            "Docs",
            "Documentation for the grant compliance evidence desk reference implementation.",
            generic_html(
                "Docs",
                "reference implementation",
                [
                    "This repo extends the nonprofit and evidence-routing lanes in the Kinetic Gain portfolio.",
                    "The desk is local-first, audit-readable, and designed to show how grants can be treated as operator workflows.",
                    "It proves the portfolio can ship nonprofit reporting surfaces as evidence systems, not only dashboards.",
                ],
            ),
            f"https://{domain}/docs/",
        ),
    )
    write(out / "api" / "dashboard.json", json.dumps(data, indent=2))
    write(out / "CNAME", domain + "\n")
    write(out / "robots.txt", f"User-agent: *\nAllow: /\nSitemap: https://{domain}/sitemap.xml\n")
    today = date.today().isoformat()
    write(
        out / "sitemap.xml",
        f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://{domain}/</loc><lastmod>{today}</lastmod></url>
  <url><loc>https://{domain}/grant-lane/</loc><lastmod>{today}</lastmod></url>
  <url><loc>https://{domain}/evidence-gaps/</loc><lastmod>{today}</lastmod></url>
  <url><loc>https://{domain}/reporting-posture/</loc><lastmod>{today}</lastmod></url>
  <url><loc>https://{domain}/verification/</loc><lastmod>{today}</lastmod></url>
  <url><loc>https://{domain}/docs/</loc><lastmod>{today}</lastmod></url>
</urlset>
""",
    )
    write(out / "404.html", (out / "index.html").read_text(encoding="utf-8"))
    return out
