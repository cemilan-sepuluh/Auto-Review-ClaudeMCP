#!/usr/bin/env python3
"""
Launcher for pr-review MCP server.
Forces UTF-8 encoding on Windows and logs crashes to error_report.log.
Use this as the entry point in Claude Desktop config instead of server.py.
"""

import os
import sys
import subprocess
import traceback
from pathlib import Path
from datetime import datetime

SCRIPT_DIR = Path(__file__).parent
SERVER_SCRIPT = SCRIPT_DIR / "server.py"
ERROR_LOG = SCRIPT_DIR / "error_report.log"


def log(message: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(ERROR_LOG, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] [launcher] {message}\n")


def main():
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"

    try:
        proc = subprocess.Popen(
            [sys.executable, str(SERVER_SCRIPT)] + sys.argv[1:],
            env=env,
            stdin=sys.stdin,
            stdout=sys.stdout,
            stderr=sys.stderr,
        )
        proc.wait()
        if proc.returncode != 0:
            log(f"Server exited with code {proc.returncode}")
        sys.exit(proc.returncode)
    except Exception as e:
        log(f"CRASH: {type(e).__name__}: {e}\n{traceback.format_exc()}")
        sys.exit(1)


if __name__ == "__main__":
    main()
