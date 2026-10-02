from __future__ import annotations

import re
from typing import Any, Dict, Optional

import requests

from app.config import settings


def _sanitize_response(text: str) -> str:
    cleaned = re.sub(r"(@{3,}|#\s*\d+|\s{2,})", " ", text).strip()
    cleaned = re.sub(r"(\s*\.){3,}", ".", cleaned)
    cleaned = re.sub(r"([A-Za-z]+)\1{2,}", r"\1", cleaned)
    cleaned = re.sub(r"[@#_]{3,}", " ", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


def _is_probably_noise(text: str) -> bool:
    if not text:
        return True

    compact = re.sub(r"\s+", "", text)
    if len(compact) < 12:
        return True
    if re.search(r"(?:[A-Za-z])\1{3,}", compact):
        return True
    if re.search(r"[@#_]{4,}", text):
        return True
    if re.fullmatch(r"[A-Za-z]+", compact):
        return len(compact) < 20
    return False


def generate_text(prompt: str, model: Optional[str] = None) -> str:
    """Generate text using the local Ollama endpoint."""
    base_url = (settings.ollama_base_url or "http://localhost:11434").rstrip("/")
    candidates = [model, settings.ollama_model, "llama3.2:latest", "llama3.1:latest"]

    last_error = None
    for candidate in candidates:
        if not candidate:
            continue
        try:
            response = requests.post(
                f"{base_url}/api/generate",
                json={
                    "model": candidate,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.1,
                        "num_predict": 64,
                        "repeat_penalty": 1.1,
                        "top_p": 0.9,
                    },
                },
                timeout=60,
            )
            if response.status_code >= 400:
                last_error = response.text
                continue
            payload: Dict[str, Any] = response.json()
            text = _sanitize_response(str(payload.get("response", "")))
            if text and not _is_probably_noise(text):
                return text
            last_error = "Ollama returned unusable output"
        except requests.RequestException as exc:
            last_error = str(exc)
            continue

    if last_error:
        raise RuntimeError(f"Ollama request failed: {last_error}")
    return ""
