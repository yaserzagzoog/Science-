# Project memory workflow — NotebookLM

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

## If the MCP server is unavailable

Fall back to the manual workflow: produce the memory-update note as plain
text for the user to paste into NotebookLM themselves. Never block work on
the MCP connection.
