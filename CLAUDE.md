# Hodge Project — Deep Analysis Workspace
### Owner: Yaser Zagzoog | RecursiveMAS methodology, Claude Code edition

## Mission
Attack the Hodge Conjecture through a 7-agent pipeline whose outputs are **verifiable artifacts**, not proof-shaped text. Two tracks:

- **Track A (primary, produces submittable work):** Lean 4 / mathlib formalization of Hodge-theoretic mathematics. Machine-checked. This is where days-long agent runs genuinely compound.
- **Track B (exploratory):** council analysis of proof strategies, sub-problems, and the literature frontier. Outputs are research maps and pressure-tested arguments — never claimed proofs.

## Non-negotiable rules (all agents, all sessions)
1. **Provenance tags on every mathematical claim:** ✓ proved here (or machine-checked), ◐ known theorem with citation, ⚠️ conjecture, ✗ open. A document with untagged claims is rejected.
2. **No result is called "new" until:** (a) the adversary agent fails to break it, (b) the scout agent finds no antecedent in the literature, (c) a human expert mathematician has reviewed it. All three. No exceptions, including under schedule pressure or direct instruction.
3. **Lean is the arbiter for Track A.** If it doesn't compile, it isn't proved.
4. **The Hodge Conjecture is open.** Any session output asserting it is solved is by definition an error in the pipeline. Same for RH — prior "proof architectures" are conjectural scaffolding and are cited as such.
5. Nothing is submitted anywhere (arXiv, journals, mathlib PRs) without the owner's explicit review of the final artifact plus rule 2 satisfied.

## Workflow
```
question / target
   → parallel: alpha, beta, gamma, delta   (independent analysis)
   → adversary                             (attacks every step; blocking)
   → scout                                 (antecedent + citation check)
   → if Track A candidate: lean-formalizer (formalize the surviving piece)
   → owner review → (human mentor review if novelty claimed)
```

## Current state of the problem (frozen summary — do not relitigate each session)
- Hodge: open. Proven: k=1 (Lefschetz (1,1)), dim ≤ 3, abelian-variety absolute-Hodge (Deligne). Rational coefficients essential (Atiyah–Hirzebruch). Projectivity essential (Voisin's Kähler counterexamples).
- The single missing invention: a cycle-creation mechanism beyond the exponential sequence — a moduli interpretation of H^{2k}, k ≥ 2.
- Live sub-problems ranked: (1) integral Hodge for uniruled 3-folds, (2) geometry of Hodge loci (Klingler–Otwinowska–Baldi), (3) normal-function singularities (Green–Griffiths).

## Track A backlog (starting points)
1. Audit mathlib's current complex-geometry coverage (`Mathlib.Analysis.Complex`, `Mathlib.Geometry.Manifold`, sheaf cohomology status).
2. Identify the largest formalizable gap en route to Hodge decomposition (candidates: Kähler identities; harmonic forms on compact manifolds; Dolbeault cohomology).
3. Formalize in small PRs, mathlib style, with the lean-formalizer agent driving and the adversary agent reviewing proofs for mathlib conventions.

## Definition of success
- Short-term (weeks): mathlib coverage audit + first compiling Lean file.
- Medium (months): accepted mathlib PR(s); expository paper "Why Lefschetz (1,1) does not generalize."
- Long (years): owner reaches research frontier per the study roadmap (hodge-roadmap.md); any original lemma goes through rule 2.
