# grant-compliance-evidence-desk

Nonprofit operator surface for grant evidence, reporting posture, budget amendments, and deliverable readiness.

## What it shows

- a local-first Python + SQLite desk for nonprofit grant compliance and funder reporting posture
- modeled grants, funders, evidence packets, and reporting cycles that surface missing proof before reporting windows slip
- a crawlable static custom-domain surface published from the same desk output

## Product depth

Grant Compliance Evidence Desk turns funder reporting into a board-readable proof packet. It gives development, finance, program owners, and executive stakeholders one shared view of grant evidence before missing proof, budget amendments, deliverable drift, or reporting-window risk weakens funder trust.

The surface is designed for both non-technical and technical readers:

- leaders see which grants are exposed, who owns the next move, and what evidence is still missing
- operators see the workflow from grant lane to evidence gap to reporting posture
- technical reviewers see the data contract behind the desk: grants, funders, reporting cycles, evidence packets, and derived readiness marts
- GTM readers get a clear value story around proof reuse, reporting confidence, and reduced funder-risk drag

## What these repos have in common

This repo follows the Kinetic Gain control-plane pattern: convert a fragmented operating lane into a board-readable decision surface with risk, owner, proof, and next action in the same artifact.

- The public demo uses representative local data, not live funder, donor, beneficiary, credential, or production records.
- The page connects business impact with implementation proof so it does not read like a generic landing page.
- The generated site, JSON output, screenshots, tests, docs, and custom-domain rail all ship from the same repo.

## Operating workflow

1. Model the portfolio: load synthetic grants, funders, evidence packets, and reporting cycles into SQLite.
2. Score the risk: compute readiness, evidence gaps, deliverable pressure, and reporting posture in local marts.
3. Route the decision: publish a static evidence desk showing what to submit, repair, escalate, or hold.

## Routes

- `/`
- `/grant-lane/`
- `/evidence-gaps/`
- `/reporting-posture/`
- `/verification/`
- `/docs/`

## Local development

```powershell
python scripts\run_demo.py
python scripts\generate_site.py
```

## Validation

```powershell
python -m pytest
python scripts\smoke_check.py
python scripts\render_readme_assets.py
```

## Screenshots

![Overview proof](./screenshots/01-overview-proof.svg)
![Evidence gaps proof](./screenshots/02-evidence-gaps-proof.svg)
![Reporting posture proof](./screenshots/03-reporting-posture-proof.svg)

## Why this matters

This repo extends the nonprofit / foundation ops lane with a real operator primitive: grant evidence should not live as fragmented inbox follow-up between development, finance, and program teams. The desk keeps missing proof, amendment posture, and deliverable risk inspectable before funder trust degrades.

Kinetic Gain Embedded tie-back:

This surface shows how Kinetic Gain can package grant operations into a buyer-readable evidence workflow, with a direct path to hosted review lanes, paid templates, and embedded nonprofit reporting modules.

## Embedded tie-back

See [docs/KINETIC_GAIN_EMBEDDED.md](./docs/KINETIC_GAIN_EMBEDDED.md).

---

Part of the [Kinetic Gain Suite](https://suite.kineticgain.com/) operator portfolio · apex: [kineticgain.com](https://kineticgain.com) · live: [grants.kineticgain.com](https://grants.kineticgain.com/)
