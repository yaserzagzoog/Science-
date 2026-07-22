---
name: notebooklm-sync
description: >
  One-prompt transfer of ALL science content in this repo (docs/*.md source
  packs, fine-structure.html research feed, index.html site list) into
  NotebookLM. Uses the notebooklm MCP server directly when it is connected;
  otherwise falls back automatically to the Google Drive bridge (NotebookLM
  imports Drive docs natively). Trigger whenever the user says
  "sync to NotebookLM", "transfer the science to NotebookLM",
  "push the repo to NotebookLM", "update my notebook",
  "/notebooklm-sync", or any variation of moving repo content into NotebookLM.
---

# NotebookLM Sync — transfer the repo's science to NotebookLM in one prompt

Target notebook: **Fine Structure α** (create it if the MCP path is available
and it does not exist).

## Step 1 — Inventory the science content

Build the list of content to transfer. Always include, when present:

- Every markdown file in `docs/` EXCEPT `NOTEBOOKLM_SETUP.md` (that is setup
  documentation, not science). Today this means
  `docs/FINE_STRUCTURE_ALPHA_SOURCES.md`; future digests and source packs in
  `docs/` are included automatically.
- All external URLs referenced in those markdown files and in
  `fine-structure.html` / `index.html` (arXiv, Quanta Magazine, etc.).
  Extract with a grep for `https?://` and deduplicate. Exclude
  github.com/tooling/setup links — only science sources go to the notebook.

## Step 2 — Choose the transfer path

Check with ToolSearch whether `notebooklm` MCP tools are connected
(query: "notebooklm").

### Path A — direct (notebooklm MCP connected, local session)

1. List notebooks; find **Fine Structure α** or create it.
2. Add each extracted URL as a **website source** (skip URLs already present
   in the notebook — list existing sources first).
3. Add each markdown document's full text as a **text source**, titled with
   the filename.
4. Report: sources added, sources skipped as duplicates, notebook total
   (free tier caps at 50 sources — warn if approaching the cap).

### Path B — Google Drive bridge (cloud session, MCP not available)

The community NotebookLM MCP server requires a one-time `notebooklm login`
on the user's own machine, so it can never run in a cloud session. Never
block on it. Instead:

1. Search Drive for the folder **"Fine Structure α — NotebookLM"**
   (`title = 'Fine Structure α — NotebookLM' and mimeType = 'application/vnd.google-apps.folder'`).
   Create it if missing.
2. For each markdown file in the inventory, create or update a Google Doc in
   that folder containing its full content (text/plain upload converts to a
   Google Doc). If a doc with the same title exists, create the new one with
   a date suffix rather than silently duplicating.
3. Create/refresh a Google Doc **"URL bulk-paste list"** with all extracted
   science URLs, one per line, for bulk import via NotebookLM's Website box.
4. Tell the user the finishing steps:
   - NotebookLM → **+ إضافة مصدر / Add source → Google Drive** → pick the
     content docs.
   - **Add source → Website** → paste the URL list (one per line, bulk
     paste works).
5. Remind them (once, briefly) that running
   `./scripts/setup-notebooklm-mcp.sh` + `uv run notebooklm login` locally
   unlocks Path A with zero manual steps.

## Step 3 — Report

End with a short summary: which path ran, what was transferred, direct links
(Drive folder / docs), and what — if anything — the user must click in
NotebookLM to finish.
