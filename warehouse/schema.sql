CREATE TABLE funders (
  funder_id TEXT PRIMARY KEY,
  funder_name TEXT NOT NULL,
  grant_type TEXT NOT NULL
);

CREATE TABLE grants (
  grant_id TEXT PRIMARY KEY,
  funder_id TEXT NOT NULL REFERENCES funders(funder_id),
  grant_name TEXT NOT NULL,
  reporting_due_date TEXT NOT NULL,
  owner TEXT NOT NULL
);

CREATE TABLE evidence_packets (
  packet_id TEXT PRIMARY KEY,
  grant_id TEXT NOT NULL REFERENCES grants(grant_id),
  packet_name TEXT NOT NULL,
  status TEXT NOT NULL,
  reviewer_lane TEXT NOT NULL
);

CREATE TABLE reporting_cycles (
  cycle_id TEXT PRIMARY KEY,
  grant_id TEXT NOT NULL REFERENCES grants(grant_id),
  readiness_score INTEGER NOT NULL,
  evidence_gaps INTEGER NOT NULL,
  deliverable_risk INTEGER NOT NULL,
  amendment_needed INTEGER NOT NULL
);
