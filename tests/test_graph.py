from app.graph import run_task
from app.llm import _sanitize_response


def test_sanitize_response_removes_repeated_noise():
    assert _sanitize_response("Rhodes@@@@@@@@@@@@@@@@@@@@@@@@@@@@") == "Rhodes"


def test_calendar_alert_task_builds_alert_message():
    result = run_task(
        task_name="calendar_alert",
        emails=[
            {"subject": "Customer update", "from": "ops@example.com", "snippet": "Need follow-up by noon"},
            {"subject": "Design review", "from": "design@example.com", "snippet": "Please review mockups"},
        ],
        today_events=[
            {"title": "Daily standup", "start": "2026-09-27T09:00:00Z", "end": "2026-09-27T09:30:00Z"},
        ],
    )

    assert result["status"] == "alert_created"
    assert "Daily standup" in result["alert_message"]
    assert "Customer update" in result["brief"] or "Design review" in result["brief"]


def test_email_brief_task_summarizes_new_emails():
    result = run_task(
        task_name="email_brief",
        emails=[
            {"subject": "Quarterly forecast", "from": "finance@example.com", "snippet": "Revenue is ahead of target"},
            {"subject": "Security notice", "from": "security@example.com", "snippet": "Patch required before Friday"},
        ],
        today_events=[],
    )

    assert result["status"] == "brief_ready"
    assert "Quarterly forecast" in result["brief"]
    assert "Security notice" in result["brief"]
