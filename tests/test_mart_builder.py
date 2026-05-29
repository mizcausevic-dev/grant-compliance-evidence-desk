from app.mart_builder import build_dashboard, write_site


def test_dashboard_summary() -> None:
    dashboard = build_dashboard()
    assert dashboard["grant_count"] == 4
    assert dashboard["high_risk_grants"] == 2
    assert dashboard["missing_packets"] >= 4
    assert dashboard["max_deliverable_risk"] >= 60


def test_site_generation(tmp_path) -> None:
    out = write_site(out_dir := "site")
    assert out.name == "site"
