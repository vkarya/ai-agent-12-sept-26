import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    app_env: str = os.getenv("APP_ENV", "dev")
    app_port: int = int(os.getenv("APP_PORT", "8000"))
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama3.2:latest")
    email_provider_url: str = os.getenv("EMAIL_PROVIDER_URL", "http://mail-provider.internal")
    calendar_provider_url: str = os.getenv("CALENDAR_PROVIDER_URL", "http://calendar-provider.internal")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    scheduler_timezone: str = os.getenv("SCHEDULER_TIMEZONE", "UTC")


settings = Settings()
