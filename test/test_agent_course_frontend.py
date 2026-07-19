from pathlib import Path


def test_frontend_uses_agent_course_branding():
    html = Path("static/index.html").read_text(encoding="utf-8")

    assert "StuckToShip" in html
    assert "从卡住到做出来" in html
    assert "stuck-card" in html
    assert "stucktoship_session_id" in html
    assert ("Agent " + "课程智能助教") not in html
    assert ("K" + "12 RAG 系统") not in html
