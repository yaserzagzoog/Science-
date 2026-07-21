#!/usr/bin/env bash
#
# One-command setup for the NotebookLM MCP server used by this project.
# Based on: https://github.com/alfredang/notebooklm-mcp (community project —
# review its README and open issues before running).
#
# Usage:  ./scripts/setup-notebooklm-mcp.sh
#
set -euo pipefail

REPO_URL="https://github.com/alfredang/notebooklm-mcp.git"
TARGET_DIR="$(cd "$(dirname "$0")/.." && pwd)/tools/notebooklm-mcp"

echo "==> NotebookLM MCP setup"

# 1. uv is required (https://docs.astral.sh/uv/)
if ! command -v uv >/dev/null 2>&1; then
  echo "ERROR: 'uv' is not installed."
  echo "Install it first:  curl -LsSf https://astral.sh/uv/install.sh | sh"
  exit 1
fi

# 2. Clone (or update) the MCP server into tools/notebooklm-mcp
if [ -d "$TARGET_DIR/.git" ]; then
  echo "==> Updating existing clone in $TARGET_DIR"
  git -C "$TARGET_DIR" pull --ff-only
else
  echo "==> Cloning $REPO_URL into $TARGET_DIR"
  mkdir -p "$(dirname "$TARGET_DIR")"
  git clone "$REPO_URL" "$TARGET_DIR"
fi

# 3. Install dependencies
echo "==> Installing dependencies (uv sync)"
cd "$TARGET_DIR"
uv sync

# 4. Authenticate with Google / NotebookLM (opens a browser window — must be
#    run on your own machine, once).
echo
echo "==> Now log in to NotebookLM with your Google account:"
echo "    cd tools/notebooklm-mcp && uv run notebooklm login"
echo
echo "==> Then verify the server starts:"
echo "    uv run python server.py   (Ctrl+C to stop)"
echo
echo "==> Claude Code will auto-detect the server via .mcp.json in the repo root."
echo "    Or register it globally with:"
echo "    claude mcp add notebooklm -- uv --directory $TARGET_DIR run python server.py"
echo
echo "==> Test inside Claude Code with:  List my NotebookLM notebooks"
