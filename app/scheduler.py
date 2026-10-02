from __future__ import annotations

from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from tzlocal import get_localzone

from app.connectors import fetch_emails, fetch_today_events
from app.graph import run_task

scheduler = BackgroundScheduler(timezone=str(get_localzone()))


def run_calendar_alert_job() -> None:
    emails = fetch_emails()
    events = fetch_today_events()
    response = run_task(task_name="calendar_alert", emails=emails, today_events=events)
    print(f"[9:00] Calendar alert job: {response}")


def run_email_brief_job() -> None:
    emails = fetch_emails()
    events = fetch_today_events()
    response = run_task(task_name="email_brief", emails=emails, today_events=events)
    print(f"[10:00] Email brief job: {response}")


def start_scheduler() -> None:
    scheduler.add_job(run_calendar_alert_job, "cron", hour=9, minute=0, id="calendar_alert_job")
    scheduler.add_job(run_email_brief_job, "cron", hour=10, minute=0, id="email_brief_job")
    scheduler.start()


def stop_scheduler() -> None:
    scheduler.shutdown()


if __name__ == "__main__":
    start_scheduler()
    print(f"Scheduler started at {datetime.now()}.")
