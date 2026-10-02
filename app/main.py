from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field

from app.graph import run_task

app = FastAPI(title="AI Agent Orchestrator", version="1.0.0")


class TriggerRequest(BaseModel):
    task_name: str = Field(..., description="calendar_alert or email_brief")
    emails: Optional[List[Dict[str, Any]]] = None
    today_events: Optional[List[Dict[str, Any]]] = None


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/tasks/run")
def run_trigger(request: TriggerRequest) -> Dict[str, Any]:
    return run_task(
        task_name=request.task_name,
        emails=request.emails,
        today_events=request.today_events,
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
