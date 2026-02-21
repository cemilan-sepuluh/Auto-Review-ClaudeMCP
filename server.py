#!/usr/bin/env python3
"""MCP server — exposes PR-review tools to Claude."""

import sys
from pathlib import Path
from mcp.server.fastmcp import FastMCP

from file_filter import should_include
import github_client

mcp = FastMCP("pr-review")


@mcp.tool()
def get_pr_diff(pr_number: int) -> str:
    """Fetch code diff from a GitHub Pull Request, skipping Unity binary/asset files."""
    resp = github_client.github_get(f"pulls/{pr_number}/files", per_page=100)

    if resp.status_code == 401:
        return "Error: GitHub token invalid or expired. Run: python server.py --reset"
    if resp.status_code == 404:
        return f"PR #{pr_number} not found in {github_client.REPO}"
    resp.raise_for_status()

    files = resp.json()
    included = []
    skipped = []

    for f in files:
        filename = f["filename"]
        if not should_include(filename):
            skipped.append(Path(filename).name)
            continue

        patch = f.get("patch")
        if not patch:
            skipped.append(Path(filename).name)
            continue

        included.append(f"## `{filename}` ({f['status']})\n```diff\n{patch}\n```")

    if not included:
        return f"PR #{pr_number}: no reviewable code files found. Skipped: {', '.join(skipped)}"

    result = f"# PR #{pr_number} — {github_client.REPO}\n\n"
    result += f"**Skipped (assets/binary):** {', '.join(skipped)}\n\n---\n\n"
    result += "\n\n".join(included)

    # Stats
    chars = len(result)
    tokens_approx = chars // 4
    diff_lines = sum(p.count("\n") for p in included)
    result += f"\n\n---\n**Stats:** {len(included)} files, {diff_lines} diff lines, ~{tokens_approx:,} tokens"

    return result


@mcp.tool()
def list_open_prs() -> str:
    """List open Pull Requests in the repository."""
    resp = github_client.github_get("pulls", state="open", per_page=20)

    if resp.status_code == 401:
        return "Error: GitHub token invalid or expired. Run: python server.py --reset"
    resp.raise_for_status()

    prs = resp.json()
    if not prs:
        return "No open PRs found."

    lines = [f"# Open PRs in {github_client.REPO}\n"]
    for pr in prs:
        lines.append(
            f"- **#{pr['number']}** {pr['title']} "
            f"— `{pr['user']['login']}` → `{pr['base']['ref']}`"
        )
    return "\n".join(lines)


if __name__ == "__main__":
    if "--reset" in sys.argv:
        github_client.reset_secrets()
    else:
        github_client.init_secrets()
        mcp.run()
