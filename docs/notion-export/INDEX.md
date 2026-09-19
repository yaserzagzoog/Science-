# Notion → NotebookLM Export Index
Exported 2026-07-22 from Yaser's Notion Knowledge Hub. Each file below is a
complete export of one Notion section, compiled as a single document so it
can be added to NotebookLM as ONE text source.

## Structure mapping (Notion section → export file → NotebookLM notebook)

| Notion section | Export file | Target notebook |
|---|---|---|
| ⚛️ Quantum Knowledge | `quantum-knowledge.md` | **Quantum Knowledge** |
| 🌿 Wellbeing+ Project | `wellbeing-project.md` | **Wellbeing+** |
| 🔬 Longevity Research | `longevity-research.md` | **Longevity Research** |
| 📁 Projects | `projects.md` | **Projects** |
| 🌌 Cosmology | `cosmology.md` | **Cosmology** |
| 🧵 String Theory | `string-theory.md` | **String Theory** |
| 🌀 Quantum Gravity | `quantum-gravity.md` | **Quantum Gravity** |
| 🔢 Fine Structure Research | `fine-structure.md` | **Fine Structure α** (existing, 48/50 — add as 1 text source) |
| Theoretical Physicists | `theoretical-physicists.md` | **Theoretical Physicists** (or add to Quantum Knowledge) |

## How to import (local Claude Code, one prompt)

In Claude Code on the machine with the saved NotebookLM login:

> Pull the latest repo. For each file in docs/notion-export/ (except INDEX.md),
> create the NotebookLM notebook named in docs/notion-export/INDEX.md if it does
> not exist, and add the file's full content as a single text source titled with
> the file's H1. For fine-structure.md, use the EXISTING "Fine Structure α"
> notebook. Skip any source that already exists with the same title.

Free-tier limits: 100 notebooks, 50 sources each — one text source per section
uses a tiny fraction of that.
