# Hodge Project

A Claude Code research workspace for a long-horizon study of Hodge theory and the Hodge Conjecture, run as a multi-agent pipeline whose outputs are verifiable artifacts — machine-checked Lean 4 proofs and pressure-tested research maps — never proof-shaped text.

## Layout

| Path | Purpose |
|---|---|
| `CLAUDE.md` | Project rules, workflow, and current state of the problem. Loaded automatically in every Claude Code session. |
| `hodge-roadmap.md` | The 4–5 year study roadmap with adversarially examined phase gates. |
| `PROGRESS.md` | Dated session log maintained by the orchestrator agent. |
| `.claude/agents/` | The agent council (see below). |

## The agent council

Claude Code discovers these automatically; invoke them by name or let the orchestrator route work.

- **orchestrator** — runs the full pipeline on a question, enforces the CLAUDE.md rules, writes the session report to `PROGRESS.md`.
- **alpha-arithmetic** — arithmetic geometry: cycle class maps, absolute Hodge classes, motives.
- **beta-condensed** — derived/categorical methods: semiregularity, obstruction theory.
- **gamma-physics** — mathematical physics: harmonic theory, positivity, SUSY QM intuition (analogies only, never proofs).
- **delta-spectral** — spectral theory: elliptic operators, hard Lefschetz, what spectral methods cannot see.
- **adversary** — blocking journal-referee review; nothing is recorded as a result without its SURVIVES verdict.
- **scout** — literature antecedent checks, citation verification, mathlib coverage audits.
- **lean-formalizer** — Track A driver: Lean 4 / mathlib formalization; the compiler is the arbiter.

## Workflow

```
question → alpha + beta + gamma + delta (parallel, independent)
         → adversary (blocking)
         → scout (antecedent check)
         → lean-formalizer (Track A candidates)
         → owner review
```

## Ground rules (abridged — see CLAUDE.md)

1. Every mathematical claim carries a provenance tag: ✓ proved here / ◐ known with citation / ⚠️ conjecture / ✗ open.
2. Nothing is called "new" without adversary survival **and** no literature antecedent **and** human expert review.
3. Lean is the arbiter for formalization work: if it doesn't compile, it isn't proved.
4. The Hodge Conjecture is open. Any output claiming otherwise is a pipeline error.
