"""Configuración de la app — carga .env y resuelve defaults por SO."""

from __future__ import annotations

import sys
from pathlib import Path

from dotenv import load_dotenv
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

_DEFAULT_DATA_ROOT = Path.home() / "Documents" / "TLA"
_DEFAULT_DB_PATH = (
    Path.home() / "AppData" / "Local" / "tla" / "tla.db"
    if sys.platform == "win32"
    else Path.home() / ".local" / "share" / "tla" / "tla.db"
)
_DEFAULT_LOG_DIR = (
    Path.home() / "AppData" / "Local" / "tla" / "logs"
    if sys.platform == "win32"
    else Path.home() / ".local" / "share" / "tla" / "logs"
)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="TLA_", case_sensitive=False)

    # Server
    host: str = "127.0.0.1"
    port: int = 8080

    # Paths
    data_root: Path = _DEFAULT_DATA_ROOT
    db_path: Path = _DEFAULT_DB_PATH
    log_dir: Path = _DEFAULT_LOG_DIR

    # Paths derivados de data_root (se resuelven post-init)
    reports_import_dir: Path | None = None
    stats_dir: Path | None = None
    stats_history_dir: Path | None = None

    # LLM
    llm_provider: str = "none"
    llm_model: str = ""
    anthropic_api_key: str = ""
    openai_api_key: str = ""
    ollama_host: str = "http://localhost:11434"

    # Sesión
    session_timeout_min: int = 30
    log_level: str = "INFO"
    locale: str = "es"

    # Red y rescan
    rescan_on_startup: bool = True
    network_timeout_sec: int = 10
    network_retry_count: int = 2

    # UI
    theme: str = "auto"

    def model_post_init(self, __context: object) -> None:
        if self.reports_import_dir is None:
            self.reports_import_dir = self.data_root / "_import"
        if self.stats_dir is None:
            self.stats_dir = self.data_root / "_stats"
        if self.stats_history_dir is None:
            self.stats_history_dir = self.stats_dir / "history"

    @field_validator("theme")
    @classmethod
    def validate_theme(cls, v: str) -> str:
        allowed = {"auto", "light", "dark"}
        if v not in allowed:
            raise ValueError(f"theme must be one of {allowed}")
        return v

    @field_validator("llm_provider")
    @classmethod
    def validate_llm_provider(cls, v: str) -> str:
        allowed = {"none", "anthropic", "openai", "ollama"}
        if v not in allowed:
            raise ValueError(f"llm_provider must be one of {allowed}")
        return v


settings = Settings()
