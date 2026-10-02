from typing import Any, Dict, List, Optional

from langgraph.graph import END, StateGraph

from app.llm import generate_text
from app.models import AgentState


def _build_calendar_alert(emails: List[Dict[str, Any]], today_events: List[Dict[str, Any]]) -> str:
    if today_events:
        event_names = ", ".join(event.get("title", "Untitled event") for event in today_events[:3])
        base = f"Calendar alert: You have today's events scheduled at 9 AM: {event_names}."
    else:
        base = "Calendar alert: No meetings are scheduled for today."

    if emails:
        top_email_subjects = ", ".join(email.get("subject", "New email") for email in emails[:3])
        base += f" Prioritize these new messages: {top_email_subjects}."

    try:
        return generate_text(
            f"Refine this alert for a professional morning summary. Keep it concise and clear:\n\n{base}"
        )
    except Exception:
        return base


def _build_brief(emails: List[Dict[str, Any]]) -> str:
    if not emails:
        return "No new emails were found to summarize."

    summary_lines = [
        f"- {email.get('subject', 'Untitled email')} from {email.get('from_email') or email.get('sender') or 'Unknown sender'}: {email.get('snippet') or email.get('body') or 'No preview available.'}"
        for email in emails[:5]
    ]
    combined = "Key email brief:\n" + "\n".join(summary_lines)

    try:
        return generate_text(
            "Turn the following raw email summary into a polished brief for a morning digest:\n\n" + combined
        )
    except Exception:
        return combined


def read_emails_node(state: AgentState) -> AgentState:
    state["emails"] = state.get("emails") or []
    state["status"] = "emails_loaded"
    return state


def check_calendar_node(state: AgentState) -> AgentState:
    state["today_events"] = state.get("today_events") or []
    state["status"] = "calendar_checked"
    return state


def create_alert_node(state: AgentState) -> AgentState:
    state["alert_message"] = _build_calendar_alert(state.get("emails", []), state.get("today_events", []))
    state["brief"] = _build_brief(state.get("emails", []))
    state["status"] = "alert_created"
    return state


def create_brief_node(state: AgentState) -> AgentState:
    state["brief"] = _build_brief(state.get("emails", []))
    state["alert_message"] = _build_calendar_alert(state.get("emails", []), state.get("today_events", []))
    state["status"] = "brief_ready"
    return state


def route_task(state: AgentState) -> str:
    if state.get("task_name") == "calendar_alert":
        return "create_alert"
    return "create_brief"


def build_workflow() -> StateGraph:
    workflow = StateGraph(AgentState)
    workflow.add_node("read_emails", read_emails_node)
    workflow.add_node("check_calendar", check_calendar_node)
    workflow.add_node("create_alert", create_alert_node)
    workflow.add_node("create_brief", create_brief_node)

    workflow.set_entry_point("read_emails")
    workflow.add_edge("read_emails", "check_calendar")
    workflow.add_conditional_edges(
        "check_calendar",
        route_task,
        {
            "create_alert": "create_alert",
            "create_brief": "create_brief",
        },
    )
    workflow.add_edge("create_alert", END)
    workflow.add_edge("create_brief", END)
    return workflow


_graph = build_workflow().compile()


def run_task(task_name: str, emails: Optional[List[Dict[str, Any]]] = None, today_events: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    initial_state: AgentState = {
        "task_name": task_name,
        "emails": emails or [],
        "today_events": today_events or [],
        "alert_message": "",
        "brief": "",
        "status": "initialized",
    }
    result = _graph.invoke(initial_state)
    return {
        "status": result["status"],
        "alert_message": result.get("alert_message", ""),
        "brief": result.get("brief", ""),
        "emails": result.get("emails", []),
        "today_events": result.get("today_events", []),
    }
