"""GitHub API client — authentication and HTTP helpers."""

import os
import re
import sys
import keyring
import requests

SERVICE = "pr-review-mcp"

GITHUB_TOKEN = None
REPO = None

# Regex: owner/repo, only ASCII letters, digits, hyphens, underscores, dots
_REPO_RE = re.compile(r"^[A-Za-z0-9._-]+/[A-Za-z0-9._-]+$")


# ── Validation ───────────────────────────────────────────

def _validate_token(value: str) -> str:
    """Validate and clean GitHub token."""
    value = value.strip()
    if not value:
        raise ValueError("GITHUB_TOKEN is empty")
    if not value.isascii():
        raise ValueError(
            "GITHUB_TOKEN contains non-ASCII characters. "
            "Make sure you copied the real token, not a placeholder."
        )
    return value


def _validate_repo(value: str) -> str:
    """Validate and clean GitHub repo (owner/repo format)."""
    value = value.strip()
    if not value:
        raise ValueError("GITHUB_REPO is empty")
    if not _REPO_RE.match(value):
        raise ValueError(
            f"GITHUB_REPO '{value}' is invalid. "
            "Expected format: owner/repo (e.g. octocat/Hello-World)"
        )
    return value


_VALIDATORS = {
    "GITHUB_TOKEN": _validate_token,
    "GITHUB_REPO": _validate_repo,
}


# ── Secrets ──────────────────────────────────────────────

def get_secret(key: str) -> str:
    """Read a secret from env, then keychain, then interactive prompt."""
    value = os.environ.get(key) or keyring.get_password(SERVICE, key)
    if not value:
        # Interactive input — only works in terminal, not in Claude Desktop
        if not sys.stdin.isatty():
            raise ValueError(
                f"{key} not found. Set it via environment variable or "
                "run 'python server.py' manually first to save it to keychain."
            )
        print(f"\n[pr-review-mcp] {key} not found in keychain.")
        value = input(f"Enter {key}: ")
        if not value:
            raise ValueError(f"{key} cannot be empty")
        keyring.set_password(SERVICE, key, value)
        print(f"[pr-review-mcp] {key} saved to keychain.")

    validate = _VALIDATORS.get(key)
    if validate:
        value = validate(value)
    return value


def init_secrets():
    """Load token and repo from keychain (prompt if missing)."""
    global GITHUB_TOKEN, REPO
    GITHUB_TOKEN = get_secret("GITHUB_TOKEN")
    REPO = get_secret("GITHUB_REPO")
    print(f"[pr-review-mcp] Ready. Repo: {REPO}")


def reset_secrets():
    """Delete all stored secrets from the keychain."""
    for key in ("GITHUB_TOKEN", "GITHUB_REPO"):
        try:
            keyring.delete_password(SERVICE, key)
            print(f"[pr-review-mcp] Deleted {key}")
        except keyring.errors.PasswordDeleteError:
            print(f"[pr-review-mcp] {key} not found")


# ── GitHub HTTP helpers ──────────────────────────────────

def get_headers() -> dict:
    return {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }


def github_get(path: str, **params) -> requests.Response:
    """GET request to the GitHub API. `path` is appended to the repo URL."""
    url = f"https://api.github.com/repos/{REPO}/{path}"
    resp = requests.get(url, headers=get_headers(), params=params)
    resp.encoding = "utf-8"
    return resp
