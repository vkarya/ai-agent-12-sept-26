from typing import Any, Dict, List, TypedDict


class EmailMessage(TypedDict, total=False):
    subject: str
    from_email: str
    sender: str
    snippet: str
    body: str
    received_at: str


class CalendarEvent(TypedDict, total=False):
    title: str
    start: str
    end: str
    location: str
    attendees: List[str]


class AgentState(TypedDict):
    task_name: str
    emails: List[Dict[str, Any]]
    today_events: List[Dict[str, Any]]
    alert_message: str
    brief: str
    status: str
