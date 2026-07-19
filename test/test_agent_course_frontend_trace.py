from pathlib import Path


def test_frontend_exposes_route_trace_and_citation_panel():
    html = Path("static/index.html").read_text(encoding="utf-8")

    assert "route-pill" in html
    assert "trace-preview" in html
    assert "msg.route" in html
    assert "msg.trace" in html
