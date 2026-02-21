"""GitHub API client — authentication and HTTP helpers."""

import keyring
import requests

SERVICE = "pr-review-mcp"

GITHUB_TOKEN = None
REPO = None


# ── Secrets ──────────────────────────────────────────────

def get_secret(key: str) -> str:
    """Read a secret from the system keychain, prompting if missing."""
    value = keyring.get_password(SERVICE, key)
    if not value:
        print(f"\n[pr-review-mcp] {key} not found in keychain.")
        value = input(f"Enter {key}: ")
        if not value:
            raise ValueError(f"{key} cannot be empty")
        keyring.set_password(SERVICE, key, value)
        print(f"[pr-review-mcp] {key} saved to keychain.")
    return value


def init_secrets():
    """Load token and repo from keychain (prompt if missing)."""
    global GITHUB_TOKEN, REPO
    GITHUB_TOKEN = get_secret("GITHUB_TOKEN")
    REPO = get_secret("GITHUB_REPO")
    print(f"[pr-review-mcp] Ready, Connect MCP to CLAUDE!. Current Repo: {REPO}")


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
    return requests.get(url, headers=get_headers(), params=params)
