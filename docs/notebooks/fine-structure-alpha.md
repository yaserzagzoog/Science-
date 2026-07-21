# NotebookLM notebook package — "Fine Structure α"

> Status: prepared automatically in a cloud session on 2026-07-21.
> The NotebookLM MCP server is installed under `tools/notebooklm-mcp/`, but no
> authentication was available in the cloud container (`NOTEBOOKLM_AUTH_JSON`
> was not set and no `storage_state.json` exists), so this package follows the
> manual fallback workflow from `CLAUDE.md`: everything below is paste-ready.

## Step 1 — Create the notebook

In [NotebookLM](https://notebooklm.google/), create a new notebook named:

```
Fine Structure α
```

(Or, once the MCP auth works on your machine:
`cd tools/notebooklm-mcp && uv run notebooklm create "Fine Structure α"`.)

## Step 2 — Add these sources (URL sources)

Curated on 2026-07-21 — latest arXiv papers and Quanta Magazine articles on
the fine structure constant.

### arXiv

| Source | Why it earns a slot |
|---|---|
| [arXiv:2512.14441 — A sub-ppm upper limit on the cosmological variations of the fine structure constant α](https://arxiv.org/abs/2512.14441) (Dec 2025) | The newest observational constraint: quasar-absorption analysis pushing cosmological α-variation below one part per million. |
| [arXiv:2506.18328 — The fine structure constant: a review of measurement results and possible space-time variations](https://arxiv.org/abs/2506.18328) (Jun 2025, Bronnikov et al.) | The best single review of the field: laboratory measurements, astrophysical/cosmological bounds, and theory of possible α variation in one place. |
| [arXiv:2410.07281 — Fundamental constants: from measurement to the universe, a window on gravitation and cosmology](https://arxiv.org/abs/2410.07281) (Oct 2024) | Puts α in the wider context of all fundamental constants, gravitation, and cosmology. |
| [arXiv:2409.03787 — CODATA Recommended Values of the Fundamental Physical Constants: 2022](https://arxiv.org/abs/2409.03787) (Sep 2024) | The authoritative reference value: α⁻¹ = 137.035999… and the electron g−2 / atom-interferometry determinations behind it. |
| [arXiv:2404.03123 — Constraints on the spacetime variation of the fine-structure constant using DESI emission-line galaxies](https://arxiv.org/abs/2404.03123) (Apr 2024) | Modern large-survey (DESI) approach to testing whether α varies across the sky and over cosmic time. |

### Quanta Magazine

| Source | Why it earns a slot |
|---|---|
| [The First Nuclear Clock Will Test if Fundamental Constants Change](https://www.quantamagazine.org/the-first-nuclear-clock-will-test-if-fundamental-constants-change-20240904/) (Sep 2024) | The thorium-229 nuclear clock — the most sensitive coming probe of α drift. |
| [Physicists Nail Down the 'Magic Number' That Shapes the Universe](https://www.quantamagazine.org/physicists-measure-the-magic-fine-structure-constant-20201202/) (Dec 2020) | The canonical narrative article on α ≈ 1/137: the 81-parts-per-trillion rubidium measurement, Feynman's "magic number", and why α's value matters for chemistry and life. |
| [Ultra-Accurate Clocks Lead Search for New Laws of Physics](https://www.quantamagazine.org/ultra-accurate-clocks-lead-search-for-new-laws-of-physics-20180416/) (Apr 2018) | How comparing independent atomic clocks turns timekeeping into a laboratory test of α variation and new physics. |

## Step 3 — Founding memory note (paste as a text source)

Paste the block below into the notebook as a text source titled
**"Project Memory Summary — founding note"**:

```text
PROJECT MEMORY SUMMARY — Fine Structure α (founding note, 2026-07-21)

PURPOSE
This notebook is the external long-term memory for the fine-structure-constant
strand of Yaser Zagzoog's Science project (GitHub: yaserzagzoog/science-).
Division of labor: NotebookLM stores knowledge and sources; Claude thinks,
writes, plans, and builds.

WHAT CHANGED TODAY
- The NotebookLM MCP server (alfredang/notebooklm-mcp) was installed into the
  repo at tools/notebooklm-mcp via scripts/setup-notebooklm-mcp.sh.
- This notebook, "Fine Structure α", was founded with 5 arXiv papers and
  3 Quanta Magazine articles as its initial sources (see source list).
- The repo already serves an "α Research Feed" page (fine-structure.html) and
  runs a daily 9 AM fine-structure digest skill that saves articles to the
  "Fine Structure" section in Notion.

FINAL DECISIONS
- NotebookLM = memory and sources; Claude = reasoning and execution.
- One notebook per topic strand; this one is only for the fine structure
  constant α, its measurement, its possible variation, and its connections to
  QED, quantum gravity, and the other fundamental constants.
- Cloud sessions cannot log in to Google, so MCP authentication must be done
  once on Yaser's own machine (uv run notebooklm login) or by exporting
  NOTEBOOKLM_AUTH_JSON into the cloud environment's variables.

EXACT WORDING OF IMPORTANT RULES
- "NotebookLM stores knowledge and sources; Claude thinks, writes, plans, and
  builds."
- "Never block work on the MCP connection." (If MCP is down, produce
  paste-ready memory notes instead.)
- "Always let the user review email-derived notes before they are stored."

KEY FACTS TO REMEMBER
- α ≈ 1/137.035999… (dimensionless); it sets the strength of the
  electromagnetic interaction.
- Best laboratory determinations come from electron g−2 plus QED, and from
  Rb/Cs atom-interferometry recoil measurements (CODATA 2022).
- Current best cosmological bounds put any variation of α below ~1 ppm
  (arXiv:2512.14441); the thorium-229 nuclear clock is the next big probe.

NEXT ACTIONS
1. Yaser: run `uv run notebooklm login` locally (or set NOTEBOOKLM_AUTH_JSON
   in the cloud environment) so future sessions can write to this notebook
   automatically.
2. Add the 8 founding sources listed in the package file to this notebook.
3. At the end of each significant session, append a dated memory-update note
   (what changed, decisions, rules, sources to add, next actions).
4. Consider wiring the daily fine-structure digest output into this notebook
   as an additional recurring source.
```
