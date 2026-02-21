"""Simple file logger for error reporting and optional debug logging."""

import os
import traceback
from datetime import datetime
from pathlib import Path

LOG_PATH = Path(__file__).parent / "error_report.log"
DEBUG = os.environ.get("MCP_DEBUG", "").lower() in ("1", "true", "yes")


def log_error(tool_name: str, error: Exception) -> str:
    """Log an error with traceback and return a user-friendly message."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tb = traceback.format_exc()
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] [ERROR] [{tool_name}] {type(error).__name__}: {error}\n{tb}\n")
    return f"Error: {error} (see error_report.log for details)"


def log_debug(tool_name: str, message: str):
    """Log a debug message (only when MCP_DEBUG=1)."""
    if not DEBUG:
        return
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] [DEBUG] [{tool_name}] {message}\n")
