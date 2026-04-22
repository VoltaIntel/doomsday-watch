"""Structured JSON logging for DoomsdayWatch.

Writes one JSON object per line to both stderr and a rotating daily file at
data/logs/pipeline-YYYY-MM-DD.log. Rotation policy: one file per day, keep
the last 30 days.
"""
from __future__ import annotations

import json
import logging
import os
import sys
from datetime import datetime, timezone
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

_LOG_DIR = Path("data/logs")
_LOGGER_NAME = "doomsdaywatch"


class _JsonFormatter(logging.Formatter):
    """Render records as compact JSON lines."""

    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "ts": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(
                timespec="milliseconds"
            ).replace("+00:00", "Z"),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }
        if record.exc_info:
            payload["exc"] = self.formatException(record.exc_info)
        # Attach any extra key=value pairs the caller passed via `extra=`.
        reserved = set(logging.LogRecord(
            "", 0, "", 0, "", None, None
        ).__dict__.keys()) | {"message", "asctime", "exc_info", "exc_text", "stack_info"}
        for k, v in record.__dict__.items():
            if k in reserved:
                continue
            try:
                json.dumps(v)
                payload[k] = v
            except TypeError:
                payload[k] = repr(v)
        return json.dumps(payload, ensure_ascii=False)


def get_logger() -> logging.Logger:
    """Return a singleton pipeline logger, configuring handlers on first call."""
    logger = logging.getLogger(_LOGGER_NAME)
    if getattr(logger, "_doomsday_configured", False):
        return logger
    logger.setLevel(logging.INFO)
    logger.propagate = False
    formatter = _JsonFormatter()

    stderr_h = logging.StreamHandler(sys.stderr)
    stderr_h.setFormatter(formatter)
    logger.addHandler(stderr_h)

    try:
        _LOG_DIR.mkdir(parents=True, exist_ok=True)
        log_path = _LOG_DIR / "pipeline.log"
        file_h = TimedRotatingFileHandler(
            log_path, when="midnight", backupCount=30, utc=True, encoding="utf-8"
        )
        file_h.setFormatter(formatter)
        logger.addHandler(file_h)
    except OSError as exc:
        logger.warning("log_dir_setup_failed", extra={"err": repr(exc)})

    logger._doomsday_configured = True  # type: ignore[attr-defined]
    return logger
