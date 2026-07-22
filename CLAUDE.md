# Project memory workflow — NotebookLM

## One-prompt sync

To transfer all science content in this repo to NotebookLM, use the
`notebooklm-sync` skill (`.claude/skills/notebooklm-sync/SKILL.md`) — trigger
it with `/notebooklm-sync` or "sync the science to NotebookLM". It uses the
notebooklm MCP server directly when connected, and falls back to the Google
Drive bridge (folder "Fine Structure α — NotebookLM") in cloud sessions.

This project uses NotebookLM as its external long-term memory, connected via
the `notebooklm` MCP server configured in `.mcp.json` (see
`docs/NOTEBOOKLM_SETUP.md` for setup).

Division of labor: **NotebookLM stores knowledge and sources; Claude thinks,
writes, plans, and builds.**

## At the start of a work session

If the `notebooklm` MCP tools are available, query the project notebook for
previous decisions, important constraints, and unresolved questions, and load
only the context needed for the current task before making changes.

## At the end of a significant work session

Offer the user a "memory update" note they can paste into the project
notebook, containing:

- what changed today
- final decisions
- exact wording of important rules
- files or sources to add
- next action list

## Gmail as a memory source

The user's Gmail is connected to Claude as a connector. When asked to bring
email into project memory: search Gmail for the relevant threads, summarize
them into a memory note (decisions, dates, amounts, commitments, open
questions, next actions), and — if the `notebooklm` MCP tools are available —
add the note to the project notebook; otherwise hand the note to the user to
paste into NotebookLM. Always let the user review email-derived notes before
they are stored, since email may contain sensitive personal data.

## If the MCP server is unavailable

Fall back to the manual workflow: produce the memory-update note as plain
text for the user to paste into NotebookLM themselves. Never block work on
the MCP connection.
