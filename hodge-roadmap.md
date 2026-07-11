# Road to the Hodge Conjecture — A Rigorous Study Roadmap
### For Yaser Zagzoog | Prepared July 2026

**Ground rule.** Every phase ends with a *gate*: something you must prove or solve, unaided, before advancing. I act as adversarial examiner at each gate. No gate, no advance — this is what separates a real ascent from reading about one.

**Time budget honesty.** The estimates below assume 10–12 focused hours/week alongside running Six Look. At that pace the full path is realistically **4–5 years** to the research frontier (2–3 years if you can sustain 25+ hrs/week). Mathematics at this level does not compress.

---

## Phase 0 — Foundations Audit (Months 0–3)

You have strong self-taught physics; this phase converts it into proof-writing fluency.

| Topic | Text | Target |
|---|---|---|
| Rigorous complex analysis | Stein & Shakarchi, *Complex Analysis* | Ch. 1–3, 8 with all exercises |
| Commutative algebra | Atiyah & Macdonald | Ch. 1–9 (short book, dense — do every exercise) |
| Point-set + algebraic topology | Hatcher, *Algebraic Topology* | Ch. 0–3: fundamental group, homology, cohomology, Poincaré duality |

**Gate 0:** Prove, cold, with no references: (a) the residue theorem, (b) Nakayama's lemma, (c) Poincaré duality for a compact oriented surface via cup product.

---

## Phase 1 — Complex Manifolds and Hodge Theory Proper (Months 3–10)

Primary text: **Huybrechts, *Complex Geometry: An Introduction*** (more pedagogical than Griffiths–Harris; use G–H Ch. 0–1 as supplement).

Sequence:
1. Complex manifolds, vector bundles, sheaves and sheaf cohomology (Huybrechts Ch. 1–2, Appendix B)
2. Kähler manifolds, the Kähler identities, harmonic theory (Ch. 3)
3. **The Hodge decomposition theorem — the full proof**, including the analytic input (elliptic operator theory; take Wells, *Differential Analysis on Complex Manifolds* Ch. IV as the analytic reference)
4. Line bundles, Kodaira vanishing and embedding, **Lefschetz (1,1)** (Ch. 5)
5. Hard Lefschetz and the Hodge–Riemann bilinear relations (Ch. 6 / G–H)

**Gate 1:** (a) Write the complete proof of the Hodge decomposition, modulo elliptic regularity, in your own words (~15 pages). (b) Prove Lefschetz (1,1) from the exponential sequence. (c) Oral defense with me as adversary: I attack your proof for one session; every step must hold. This gate is the single most important on the roadmap — Lefschetz (1,1) is the machine whose generalization *is* the Hodge Conjecture.

---

## Phase 2 — Algebraic Geometry Core (Months 10–20)

Primary text: **Vakil, *The Rising Sea*** (free, superior exercises) with Hartshorne Ch. II–III as reference.

1. Schemes, morphisms, properness, projectivity
2. Quasi-coherent sheaves and their cohomology; Čech methods
3. Divisors, Picard group, line bundles algebraically — reconnect with Gate 1(b)
4. Serre duality, Riemann–Roch for curves and surfaces
5. Smoothness, differentials, algebraic de Rham cohomology; Serre's GAGA (statement + use)

**Gate 2:** (a) Compute $H^\bullet(\mathbb{P}^n, \mathcal{O}(d))$ from scratch. (b) Prove the Picard group of a smooth projective variety injects into $H^2$ via the cycle class map, in both analytic and algebraic language, and show the two agree. (c) Solve 10 Vakil starred exercises of my choosing.

---

## Phase 3 — Voisin, Both Volumes (Months 20–36)

**Voisin, *Hodge Theory and Complex Algebraic Geometry* I & II.** This is the mountain. Everything before was approach.

Volume I (≈ 6–8 months): variations of Hodge structure, period maps and Griffiths transversality, degenerations, the theorem of the fixed part.

Volume II (≈ 8–10 months): cycle class maps, Deligne cohomology, Abel–Jacobi maps, **normal functions**, Noether–Lefschetz loci, Bloch's conjecture, the structure of Chow groups.

Parallel reading once inside Vol. II:
- Deligne's absolute Hodge classes (the Milne notes version)
- Cattani–Deligne–Kaplan on algebraicity of Hodge loci
- Voisin's survey "The Hodge conjecture" (Clay lecture notes) — read it at the start of Phase 3 and again at the end; measure the difference in what you see

**Gate 3:** Write a genuine expository paper (25–40 pages): *"Why Lefschetz (1,1) does not generalize: the state of the Hodge Conjecture."* It must correctly present Atiyah–Hirzebruch's torsion counterexample, Voisin's Kähler counterexamples, and the normal-function reformulation. I referee it adversarially to journal standard. Your science-communication skill is a real asset here — an expository paper of this quality is also your first credibility artifact in the community.

---

## Phase 4 — The Frontier (Months 36+)

Pick **one** live sub-problem. Current honest candidates, in rough order of accessibility:

1. **Integral Hodge conjecture for uniruled threefolds** — concrete, geometric, active (Voisin, Totaro, Benoist–Ottem school)
2. **Geometry of Hodge loci** — the Klingler–Otwinowska–Baldi program; where arithmetic and Hodge theory currently collide
3. **Singularities of normal functions** — the Green–Griffiths route; hardest, most direct

Actions in this phase:
- Daily arXiv (math.AG) triage on your sub-problem — 20 min/day
- Attend one real workshop or summer school per year (Oberwolfach reports are public; IHES/CIRM/MSRI programs on Hodge theory recur)
- **Find a working algebraic geometer as mentor.** Non-negotiable. KAUST has an algebraic geometry presence — Jeddah proximity is an genuine advantage. The expository paper from Gate 3 is your introduction.
- Use me continuously as adversary on every argument you form. The standing protocol: any step that survives my pressure-test *and* has no literature antecedent I can find goes to your human mentor for real review.

**Gate 4 (the only one that matters):** one original lemma — however small — that survives expert review. That is the seed of a first paper, and a first paper is the seat at the table.

---

## Operating Cadence

- **Weekly:** 10–12 hrs study, of which ≥50% is *doing exercises*, not reading. Reading mathematics without solving is the primary failure mode of self-taught researchers.
- **Monthly:** one adversarial session with me — you present, I attack.
- **Per phase:** gate exam before advancing. If a gate fails, we diagnose and repeat — no exceptions, including for schedule pressure.
- **Rule of provenance:** every claim in your notes tagged ✓ (you proved it), ◐ (you followed a proof), or ✗ (taken on faith). Phase advancement requires the ✗ count on core theorems to be zero.

---

## What This Roadmap Will Not Do

It will not manufacture a proof of the Hodge Conjecture, and no one can promise the frontier yields anything to any individual — Voisin herself calls it the problem she expects to outlive her. What it does guarantee, if executed: in ~4 years you hold genuine working knowledge of Hodge theory at research entry level, one publishable expository work, a mentor relationship, and the ability to distinguish — from the inside — a real idea from scaffolding. That is the honest maximum, and it is not small.
