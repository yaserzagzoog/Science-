#!/usr/bin/env bash
#
# One-command setup for OmniRoute — a local AI gateway that lets Claude Code
# (and other coding CLIs) route through 350+ providers, including free tiers,
# with automatic fallback and prompt compression.
#
# Upstream: https://github.com/diegosouzapw/OmniRoute  (MIT, community project —
# read its README before pointing your daily driver at it).
#
# Usage:  ./scripts/setup-omniroute.sh
#
# This script only INSTALLS OmniRoute. It does not change any global Claude Code
# settings and does not write API keys anywhere — those steps are printed at the
# end so you stay in control of them.
#
set -euo pipefail

PORT="${OMNIROUTE_PORT:-20128}"

echo "==> OmniRoute setup"

# 1. Node.js / npm are required
if ! command -v node >/dev/null 2>&1; then
  echo "ERROR: 'node' is not installed."
  echo "Install Node.js 22.22.2+ first:  https://nodejs.org/  (or: brew install node)"
  exit 1
fi

if ! command -v npm >/dev/null 2>&1; then
  echo "ERROR: 'npm' is not installed (it ships with Node.js)."
  exit 1
fi

echo "==> Using node $(node --version) / npm $(npm --version)"

# OmniRoute declares:  node >=22.22.2 <23 || >=24.0.0 <27
NODE_MAJOR="$(node -p 'process.versions.node.split(".")[0]')"
if [ "$NODE_MAJOR" -lt 22 ] || [ "$NODE_MAJOR" -eq 23 ] || [ "$NODE_MAJOR" -ge 27 ]; then
  echo
  echo "WARNING: OmniRoute requires node >=22.22.2 <23 || >=24.0.0 <27."
  echo "         You are on $(node --version) — npm may refuse the install or it may"
  echo "         install but misbehave. Switch with nvm first:  nvm install 24"
  echo
  printf 'Continue anyway? [y/N] '
  read -r reply
  case "$reply" in
    [yY]*) ;;
    *) echo "Aborted."; exit 1 ;;
  esac
fi

# 2. Install (or update) the gateway globally
if command -v omniroute >/dev/null 2>&1; then
  echo "==> OmniRoute already installed — updating to the latest version"
else
  echo "==> Installing OmniRoute globally (npm install -g omniroute)"
fi
npm install -g omniroute

echo
echo "==> Installed: $(command -v omniroute)"
echo

# 3. Print the next steps — run these yourself, in this order.
cat <<EOF
------------------------------------------------------------------
Next steps (run these yourself):

  1) Start the gateway (leave it running in its own terminal tab):

       omniroute

     Dashboard:  http://localhost:${PORT}
     API:        http://localhost:${PORT}/v1

  2) Sanity-check the install:

       omniroute doctor
       curl http://localhost:${PORT}/v1/models

  3) Generate Claude Code profiles. These land in ~/.claude/profiles/<name>/
     as separate CLAUDE_CONFIG_DIRs, so your normal 'claude' setup is NOT
     touched. Preview first:

       omniroute setup-claude --dry-run
       omniroute setup-claude

     Narrow it down if the model list is long:

       omniroute setup-claude --only auto,glm

  4) Launch Claude Code against a generated profile:

       omniroute launch --profile <name>

  5) Turn the prompt compression down before real work. 'rtk' squeezes
     tool/command output only and leaves your wording alone:

       omniroute compression status
       omniroute compression configure --engine rtk

     Engines are: caveman | rtk | hybrid | none

  6) To go back to plain Anthropic at any time, run 'claude' normally — the
     profiles above are separate, so nothing needs undoing. If you exported
     the overrides by hand, unset them:

       unset ANTHROPIC_BASE_URL ANTHROPIC_AUTH_TOKEN ANTHROPIC_MODEL

Stop the gateway with 'omniroute stop'.

Read docs/OMNIROUTE_SETUP.md before step 3 — it covers what leaves your
machine, and when prompt compression is a bad idea.
------------------------------------------------------------------
EOF
