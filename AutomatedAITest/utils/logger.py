"""Logging utilities for the AutomatedAITest package."""
from __future__ import annotations

import logging
from logging import Logger
from pathlib import Path
from typing import Optional


_LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


def _resolve_level(level_name: str) -> int:
    """Resolve a logging level from a string representation."""
    normalized = level_name.upper()
    if normalized == "TRACE":
        # Custom trace level below DEBUG for verbose gRPC tracing if required.
        logging.addLevelName(5, "TRACE")
        return 5
    return getattr(logging, normalized, logging.INFO)


def setup_logging(level: str, log_file: Path, logger_name: str = "AutomatedAITest") -> Logger:
    """Configure application wide logging.

    Parameters
    ----------
    level:
        String representation of the desired log level (e.g. "INFO", "DEBUG").
    log_file:
        Destination file path for log entries. Parent folders are created if
        required.
    logger_name:
        Name of the logger instance to create or retrieve.

    Returns
    -------
    Logger
        Configured :class:`logging.Logger` instance with both console and file
        handlers installed.
    """
    resolved_level = _resolve_level(level)
    logger = logging.getLogger(logger_name)
    logger.setLevel(resolved_level)

    # Prevent duplicate handlers when running multiple instances or tests.
    if logger.handlers:
        return logger

    log_file_path = log_file.expanduser().resolve()
    log_file_path.parent.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter(_LOG_FORMAT)

    file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
    file_handler.setLevel(resolved_level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(resolved_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    logger.debug("Logging initialised at level %s -> %s", level, resolved_level)
    return logger


def update_log_level(logger: Logger, level: Optional[str]) -> None:
    """Update the logger level at runtime if a new level is provided."""
    if level is None:
        return
    resolved_level = _resolve_level(level)
    logger.setLevel(resolved_level)
    for handler in logger.handlers:
        handler.setLevel(resolved_level)
    logger.debug("Logger level updated dynamically to %s", level)
