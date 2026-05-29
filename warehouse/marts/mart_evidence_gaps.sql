CREATE VIEW mart_evidence_gaps AS
SELECT
  grant_id,
  grant_name,
  funder_name,
  reporting_due_date,
  evidence_gaps,
  deliverable_risk,
  amendment_needed,
  risk_status,
  CASE
    WHEN amendment_needed = 1 THEN 'Budget amendment and restricted-funds narrative'
    WHEN evidence_gaps >= 2 THEN 'Program proof bundle and subrecipient support'
    ELSE 'Final board-ready evidence memo'
  END AS next_gap
FROM mart_grant_readiness
ORDER BY deliverable_risk DESC, evidence_gaps DESC, readiness_score ASC;
