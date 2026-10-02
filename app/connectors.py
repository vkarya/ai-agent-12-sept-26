from __future__ import annotations

import os
from typing import Any, Dict, List


MOCK_EMAILS: List[Dict[str, Any]] = [
    {
        "subject": "Follow-up on onboarding",
        "from_email": "ops@example.com",
        "snippet": "We need final sign-off before launch.",
    },
    {
        "subject": "Customer issue update",
        "from_email": "support@example.com",
        "snippet": "The incident review has been scheduled for tomorrow.",
    },
    {
        "subject": "Security patch reminder",
        "from_email": "security@example.com",
        "snippet": "Please apply the critical vulnerability patch before 5 PM today.",
    },
]


MOCK_TODAY_EVENTS: List[Dict[str, Any]] = [
    {
        "title": "Daily standup",
        "start": "2026-09-28T09:00:00Z",
        "end": "2026-09-28T09:30:00Z",
    },
    {
        "title": "Client demo",
        "start": "2026-09-28T15:00:00Z",
        "end": "2026-09-28T16:00:00Z",
    },
]


def fetch_emails() -> List[Dict[str, Any]]:
    """Use mocked email data by default for local demos.

    Real integration example (kept commented for later use):
    - Google Gmail API or Microsoft Graph API
    - OAuth token from secret manager
    - Filter only unread/new messages
    """
    if os.getenv("USE_MOCK_DATA", "true").lower() == "true":
        return [dict(email) for email in MOCK_EMAILS]

    # Example real call:
    # import requests
    # token = os.getenv("EMAIL_PROVIDER_TOKEN", "")
    # response = requests.get(
    #     "https://graph.microsoft.com/v1.0/me/messages?$filter=isRead eq false",
    #     headers={"Authorization": f"Bearer {token}"},
    #     timeout=30,
    # )
    # response.raise_for_status()
    # data = response.json()
    # return [{
    #     "subject": item.get("subject", "No subject"),
    #     "from_email": item.get("from", {}).get("emailAddress", {}).get("address", "unknown"),
    #     "snippet": item.get("bodyPreview", ""),
    # } for item in data.get("value", [])]

    return [dict(email) for email in MOCK_EMAILS]


def fetch_today_events() -> List[Dict[str, Any]]:
    """Use mocked calendar data by default for local demos.

    Real integration example (kept commented for later use):
    - Google Calendar API or Microsoft Graph calendar API
    - Timezone normalization for today
    """
    if os.getenv("USE_MOCK_DATA", "true").lower() == "true":
        return [dict(event) for event in MOCK_TODAY_EVENTS]

    # Example real call:
    # import requests
    # token = os.getenv("CALENDAR_PROVIDER_TOKEN", "")
    # response = requests.get(
    #     "https://graph.microsoft.com/v1.0/me/calendar/events",
    #     headers={"Authorization": f"Bearer {token}"},
    #     params={"startDateTime": "2026-09-28T00:00:00Z", "endDateTime": "2026-09-28T23:59:59Z"},
    #     timeout=30,
    # )
    # response.raise_for_status()
    # data = response.json()
    # return [{
    #     "title": item.get("subject", "Untitled event"),
    #     "start": item.get("start", {}).get("dateTime"),
    #     "end": item.get("end", {}).get("dateTime"),
    # } for item in data.get("value", [])]

    return [dict(event) for event in MOCK_TODAY_EVENTS]
