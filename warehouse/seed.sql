INSERT INTO funders (funder_id, funder_name, grant_type) VALUES
  ('FDN-ALPHA', 'North Harbor Foundation', 'program'),
  ('FDN-BETA', 'State Arts Trust', 'capital'),
  ('FDN-GAMMA', 'Civic Futures Fund', 'innovation'),
  ('FDN-DELTA', 'Community Relief Alliance', 'restricted');

INSERT INTO grants (grant_id, funder_id, grant_name, reporting_due_date, owner) VALUES
  ('GR-101', 'FDN-ALPHA', 'Youth workforce bridge grant', '2026-06-10', 'program-ops'),
  ('GR-208', 'FDN-BETA', 'Mobile classroom equipment award', '2026-06-18', 'development'),
  ('GR-314', 'FDN-GAMMA', 'Community health navigator pilot', '2026-06-21', 'impact-analytics'),
  ('GR-427', 'FDN-DELTA', 'Emergency pantry expansion support', '2026-06-28', 'finance-compliance');

INSERT INTO evidence_packets (packet_id, grant_id, packet_name, status, reviewer_lane) VALUES
  ('PK-101A', 'GR-101', 'Outcome metrics narrative', 'complete', 'program'),
  ('PK-101B', 'GR-101', 'Budget variance memo', 'blocked', 'finance'),
  ('PK-208A', 'GR-208', 'Vendor receipt bundle', 'draft', 'operations'),
  ('PK-208B', 'GR-208', 'Board approval excerpt', 'complete', 'executive'),
  ('PK-314A', 'GR-314', 'Participant cohort evidence', 'review', 'impact'),
  ('PK-314B', 'GR-314', 'Subrecipient monitoring notes', 'blocked', 'compliance'),
  ('PK-427A', 'GR-427', 'Relief distribution log', 'complete', 'program'),
  ('PK-427B', 'GR-427', 'Restricted-funds amendment note', 'draft', 'finance');

INSERT INTO reporting_cycles (cycle_id, grant_id, readiness_score, evidence_gaps, deliverable_risk, amendment_needed) VALUES
  ('CY-101', 'GR-101', 78, 1, 63, 1),
  ('CY-208', 'GR-208', 84, 1, 41, 0),
  ('CY-314', 'GR-314', 71, 2, 69, 1),
  ('CY-427', 'GR-427', 76, 1, 54, 1);
