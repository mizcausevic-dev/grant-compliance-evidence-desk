CREATE VIEW mart_grant_readiness AS
SELECT
  g.grant_id,
  f.funder_name,
  f.grant_type,
  g.grant_name,
  g.reporting_due_date,
  g.owner,
  rc.readiness_score,
  rc.evidence_gaps,
  rc.deliverable_risk,
  rc.amendment_needed,
  COUNT(ep.packet_id) AS packet_count,
  SUM(CASE WHEN ep.status = 'complete' THEN 1 ELSE 0 END) AS complete_packets,
  SUM(CASE WHEN ep.status IN ('blocked', 'draft') THEN 1 ELSE 0 END) AS blocked_or_draft_packets,
  CASE
    WHEN rc.deliverable_risk >= 60 THEN 'red'
    WHEN rc.deliverable_risk >= 40 THEN 'yellow'
    ELSE 'green'
  END AS risk_status
FROM grants g
JOIN funders f ON f.funder_id = g.funder_id
JOIN reporting_cycles rc ON rc.grant_id = g.grant_id
LEFT JOIN evidence_packets ep ON ep.grant_id = g.grant_id
GROUP BY
  g.grant_id,
  f.funder_name,
  f.grant_type,
  g.grant_name,
  g.reporting_due_date,
  g.owner,
  rc.readiness_score,
  rc.evidence_gaps,
  rc.deliverable_risk,
  rc.amendment_needed;
