"""Configuración de logging con rotación."""

from __future__ import annotations

import logging
import logging.handlers
from pathlib import Path

from tla.config import settings


def setup_logging() -> None:
    log_dir = settings.log_dir
    log_dir.mkdir(parents=True, exist_ok=True)

    level = getattr(logging, settings.log_level.upper(), logging.INFO)

    handler_file = logging.handlers.RotatingFileHandler(
        log_dir / "tla.log",
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=3,
        encoding="utf-8",
    )
    handler_file.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)s %(name)s — %(message)s")
    )

    handler_console = logging.StreamHandler()
    handler_console.setFormatter(logging.Formatter("%(levelname)s %(name)s — %(message)s"))

    root = logging.getLogger()
    root.setLevel(level)
    root.addHandler(handler_file)
    root.addHandler(handler_console)
