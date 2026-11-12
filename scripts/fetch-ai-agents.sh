#!/usr/bin/env bash
# Fetch the AI-agent submodules under ai-agents/.
#   ./scripts/fetch-ai-agents.sh                  all repos
#   ./scripts/fetch-ai-agents.sh <category>       e.g. 03-memory-knowledge
#   ./scripts/fetch-ai-agents.sh <category/repo>  e.g. 01-agent-frameworks/langgraph
#   ./scripts/fetch-ai-agents.sh --update         update all to latest upstream
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

if [ "${1:-}" = "--update" ]; then
  git submodule update --init --remote --depth 1 -- ai-agents
  exit 0
fi

target="ai-agents${1:+/$1}"
git config -f .gitmodules --get-regexp path | cut -d" " -f2 | grep -q "^$target" \
  || { echo "No such submodule path: $target" >&2; exit 1; }
git submodule update --init --depth 1 -- "$target"
