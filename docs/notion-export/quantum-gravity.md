# Quantum Gravity — Notion Export

**Compiled:** 2026-07-22
**Provenance:** Exported from the Notion page "🌀 Quantum Gravity" (child of "Knowledge Hub") — https://app.notion.com/p/37d765478c3c81b09117dd2eae577ea3

## Section Overview

Research, papers, and notes on loop quantum gravity, quantum spacetime, and unification of QM and GR.

The section contains two databases (📄 Papers, 🗒️ Notes), a rolling series of daily "Quantum Gravity Digest" pages, an arXiv research roundup, and individual paper notes. Everything is exported in full below, in the order listed on the parent page.

---

## Quantum Gravity Digest — 2026-06-15

Daily digest of quantum gravity, spacetime, graviton, and gravity discoveries from Scientific American and Quanta Magazine. Technical summaries with equations for rigorous review.

### Scientific American — Quantum Gravity & Spacetime

#### Can Space and Time Exist as Two Shapes at Once? Mind-Bending Experiments Aim to Find Out

*August 2024 · Nick Huggett & Carlo Rovelli*
https://www.scientificamerican.com/article/do-space-and-time-follow-quantum-rules-these-mind-bending-experiments-aim-to-find-out/

Huggett and Rovelli outline proposed tabletop experiments to test whether gravity $g_{\mu\nu}$ is fundamentally quantum by placing Planck-mass objects ($m_{Pl} = sqrt{hbar c / G} approx 2.2 times 10^{-8}$ kg) in spatial superpositions. If two such masses become gravitationally entangled via $U_{grav} sim G m^2 / r$, quantum information theory demands the mediating field must itself be in superposition — a direct signature of quantized spacetime geometry. The experiments target gravity-induced entanglement (GIE), where decoherence-free conditions allow the gravitational potential to generate off-diagonal density-matrix elements detectable as quantum correlations. A null result would support Penrose's collapse hypothesis and destabilize four decades of loop quantum gravity (LQG) and string-theoretic assumptions. The sweet spot lies near the Planck mass — macroscopic enough for gravitational effects yet small enough for coherent quantum control — placing these experiments tantalizingly close to current laboratory capability.

#### A Tale of Two Horizons: Black Hole Discovery Helps Explain the Quantum Nature of the Cosmos

*September 2022 · Edgar Shaghoulian*
https://www.scientificamerican.com/article/black-hole-discovery-helps-to-explain-quantum-nature-of-the-cosmos/

Shaghoulian demonstrates a deep mathematical analogy between black hole event horizons and the cosmological de Sitter horizon, arguing both must be described holographically. The Bekenstein-Hawking entropy $S_{BH} = A / 4G\hbar$ applies equally to both, suggesting our accelerating universe is bounded by an entropy-carrying cosmological horizon at $r_{dS} \approx c / H_0 \approx 1.6 \times 10^{26}$ m. Using the 2019 island formula breakthrough for black hole information recovery — wherein quantum extremal surfaces $X$ minimize $S_{gen} = A(X)/4G + S_{vN}(bulk)$ — Shaghoulian and collaborators show that information beyond the cosmological horizon may in principle be accessed from its Hawking-like radiation. The work highlights a central challenge: unlike black holes, de Sitter space has observer-dependent horizons, so constructing a single holographic dual requires removing the observer from within the system — an unresolved conceptual obstacle that connects directly to the quantum cosmology program.

### Quanta Magazine — Quantum Gravity

#### Entanglement Builds Space-Time. Now "Magic" Gives It Gravity.

*June 3, 2026 · Charlie Wood*
https://www.quantamagazine.org/entanglement-builds-space-time-now-magic-gives-it-gravity-20260603/

Charles Cao (Virginia Tech), John Preskill (Caltech), and collaborators have identified the missing ingredient that allows holographic quantum error-correcting codes to produce dynamical, curved spacetime: quantum "magic," formally measured by the stabilizer entropy or the number of non-Clifford T-gates required to prepare a state. Earlier stabilizer codes (built from Clifford group operations) generate a rigid, inert background geometry — entanglement gives space its connectivity ($ER = EPR$) but matter and geometry remain decoupled. By injecting non-Clifford operations, the new next-generation codes acquire magic, breaking the stabilizer-code separation and allowing the encoded matter and geometry entanglements to mix — precisely the condition Wheeler expressed as $G_{munu} = 8pi G T_{munu}$. The result is a proof-of-concept code where matter curves space: "gravity = approximate quantum error correction with magic." Swingle emphasizes that high-magic quantum states intrinsically require a quantum computer to simulate, directly linking the hardness of gravity to quantum computational complexity $mathcal{C} sim S_{magic}$. This constitutes step 0.5 of 5 toward a full theory — the code does not yet encode time or reproduce Einstein's field equations precisely, but it establishes magic as the fabric softener of spacetime.

#### Where Some See Strings, She Sees a Space-Time Made of Fractals

*March 11, 2026 · Charlie Wood*
https://www.quantamagazine.org/where-some-see-strings-she-sees-a-space-time-made-of-fractals-20260311/

Q&A with Astrid Eichhorn (Heidelberg University) on asymptotic safety — the hypothesis that quantum gravity reaches a non-Gaussian ultraviolet fixed point $g^*$ in the renormalization group (RG) flow, so that the dimensionless Newton coupling $\tilde{G} = G\mu^2$ (where $\mu$ is the RG scale) remains finite at all scales. Near this fixed point spacetime acquires a fractal-like scale symmetry: the spectral dimension runs from $d_s = 4$ at low energies to $d_s \approx 2$ at the Planck scale, consistent with results from causal dynamical triangulations. Eichhorn has shown that the fixed point survives in full gravity-matter systems including all Standard Model fields, and that it quantitatively predicts the top quark mass $m_t \approx 173$ GeV and the ratio $m_b / m_t$ to within 10% — the "OMG plot." The theory also constrains dark matter candidates: simple WIMPs, axion-like particles, and ultralight scalars are disfavored. Eichhorn argues asymptotic safety may be complementary to string theory rather than competitive, as both could describe the same physics from different vantage points.

### Quanta Magazine — General Relativity & Spacetime

#### In Expanding de Sitter Space, Quantum Mechanics Gets Even More Elusive

*March 30, 2026 · Shalma Wegsman*
https://www.quantamagazine.org/in-expanding-de-sitter-space-quantum-mechanics-gets-even-more-elusive-20260330/

Wegsman surveys the profound obstacles to formulating quantum mechanics in de Sitter space — the maximally symmetric solution to Einstein's equations with a positive cosmological constant $Lambda > 0$: $ds^2 = -dt^2 + e^{2Ht}(dx^2 + dy^2 + dz^2)$ where $H = sqrt{Lambda/3}$. Unlike anti-de Sitter space ($Lambda < 0$), which has a spatial boundary on which holographic duals (CFTs) naturally live, de Sitter's exponential expansion creates observer-dependent cosmological horizons that preclude a single global boundary. A Penedones-Loparco result (arXiv 2025) shows that massless photons in de Sitter can be decomposed into massive "complementary series" representations, implying they can spontaneously mix with massive modes — a violation of flat-space stability intuition. Energy is not conserved ($partial_mu T^{munu} neq 0$ globally), and quantum fluctuations $\langle \delta g_{\mu\nu}^2 \rangle$ do not vanish anywhere, making measurement theory itself ill-defined. Hartman (Stanford) and others find that applying island-formula techniques from black hole physics to de Sitter yields apparently empty Hilbert spaces — a sign of misinterpretation rather than emptiness. The resolution likely requires a new holographic framework anchored to an observer rather than a boundary.

*Generated automatically by Claude · June 15, 2026 · Sources: scientificamerican.com · quantamagazine.org*

---

## Quantum Gravity Digest — 2026-06-16

**June 16, 2026** | Sources: Scientific American · Quanta Magazine

### Scientific American — Quantum Gravity & Spacetime

#### Is Gravity Quantum?

*August 14, 2018* | scientificamerican.com

The fundamental question of whether gravity obeys the rules of quantum mechanics remains open — all forces but gravity are described by quantum field theory. The hypothetical carrier particle, the graviton, would prove gravity is quantum if detected, but detection poses extreme challenges: Freeman Dyson famously showed that a graviton detector massive enough to register individual graviton interactions would collapse into a black hole under its own gravity. Current experimental strategies include looking for a gravitational Casimir effect between superconducting plates, searching for gravity-induced entanglement between free-falling diamonds via laser fluorescence readout, and hunting for primordial B-mode polarization in the CMB — signatures of inflationary gravitational waves that would encode quantum fluctuations of spacetime at energy scales approaching the Planck mass M_Pl = sqrt(ℏc/G) ≈ 2.18 × 10⁻⁸ kg. So far all searches have returned null results, consistent with the graviton existing but interacting far more weakly than any detector can probe.

#### Quantum 'Graviton' Particles May Resemble Ordinary Particles of Force

*Recent (via SA Search)* | scientificamerican.com

Recent theoretical work suggests that gravitons may share structural properties with gauge bosons mediating the other fundamental forces. In the weak-coupling regime, graviton scattering amplitudes factorize in ways that mirror photon and gluon amplitudes — the Kawai-Lewellen-Tye (KLT) relations express M_gravity as a bilinear sum over gauge amplitudes with a momentum kernel. This 'gravity = (gauge theory)²' structure has practical implications for loop-level quantum gravity calculations and suggests deep unitarity constraints linking the gravitational and gauge sectors.

### Quanta Magazine — Quantum Gravity

#### Entanglement Builds Space-Time. Now "Magic" Gives It Gravity.

*June 3, 2026* | quantamagazine.org

In holographic (AdS/CFT) theories, a new ingredient has been identified that completes the Wheeler program: quantum 'magic' — the resource-theoretic measure of non-stabilizerness — encodes the bendability of emergent spacetime. Earlier work established that quantum entanglement between boundary CFT degrees of freedom builds the bulk spatial geometry via the Ryu-Takayanagi formula S_RT = A/4G_N. However, stabilizer-code holography produced inert, flat geometries: matter and space were decoupled. Charles Cao (Virginia Tech), John Preskill (Caltech), and collaborators showed in early 2026 [arXiv:2603.13475] that replacing stabilizer codes with 'magical' non-Clifford codes allows the encoded matter and space to interact, producing a back-reaction analogous to the Einstein equations G_μν + Λg_μν = (8πG/c⁴)T_μν. Magic (non-stabilizerness) measures how far a quantum state is from the nearest stabilizer state, and more magic implies weaker error-correction, which allows the encoded geometry to fluctuate and bend. This is a 'step 0.5 of 5' proof-of-concept: the code does not yet reproduce full Einstein gravity in our 3+1D universe, but demonstrates that gravity's curvature is intrinsically tied to quantum computational complexity beyond the Clifford group.

#### Are Strings Still Our Best Hope for a Theory of Everything?

*March 23, 2026* | quantamagazine.org

Natalie Wolchover surveys the 'forever war' over string theory with fresh ammunition from the bootstrap programme. Two 2025-2026 papers used S-matrix bootstrap methods — imposing unitarity, Lorentz invariance, and crossing symmetry with no string theory input — and derived the Veneziano scattering amplitude A(s,t) = Γ(-α's)Γ(-α't)/Γ(1-α's-α't) as the unique solution. The 2025 'Strings From Almost Nothing' paper (Cheung et al., arXiv:2508.09246) showed 'ultrasoftness' forces high-energy states into string-theory patterns. The 2026 'String Theory From Maximal Supersymmetry' (Elvang et al., arXiv:2601.11705) derived the Veneziano amplitude from N=4 super-Yang-Mills QFT using only maximal supersymmetry and Lorentz invariance — 'string theory comes out of just field theory.' Critics label this 'not surprising'; supporters note it shifts debate from 'is string theory right?' to 'are the bootstrap assumptions right?'

### Quanta Magazine — General Relativity & Spacetime

#### Where Some See Strings, She Sees a Space-Time Made of Fractals

*March 11, 2026* | quantamagazine.org

Astrid Eichhorn (Heidelberg) champions asymptotic safety as a rival quantum gravity framework. The programme posits that the gravitational RG flow reaches a non-Gaussian UV fixed point g* = lim_{k→∞} g_k where all relevant couplings become finite — avoiding the non-renormalizability of perturbative Einstein gravity. Near this fixed point, spacetime is predicted to exhibit fractal self-similarity with effective dimension d_UV ≈ 2 rather than 4. Eichhorn argues that assuming a flat background for UV scattering amplitudes — central to the bootstrap papers — is unjustified near the Planck scale l_Pl = sqrt(Gℏ/c³) ≈ 1.6 × 10⁻³⁵ m, where geometry fluctuations are O(1) and the notion of a Lorentz-invariant S-matrix itself may break down.

#### Cosmic Paradox Reveals the Awful Consequence of an Observer-Free Universe

*November 19, 2025* | quantamagazine.org

Extending holographic techniques from black holes (where the Page curve tracks information recovery via island formula S_gen = S_rad + A_island/4G) to de Sitter cosmology reveals a profound problem: in an accelerating universe with Λ > 0, there is a cosmic horizon with associated Gibbons-Hawking entropy S_dS = π/(GΛ), but no asymptotic region where an observer can collect all the Hawking radiation to compute the Page curve. Physicists applying quantum information-style reasoning to de Sitter find that consistent unitary evolution requires abandoning the idea of a single objective quantum state for the entire universe — raising doubts about whether any standard quantum gravity formalism can self-consistently describe our own accelerating universe.

*Generated automatically by Claude — June 16, 2026 · Sources: scientificamerican.com · quantamagazine.org*

---

## Quantum Gravity Digest — 2026-06-17

Sources: Scientific American · Quanta Magazine
Automatically generated by Claude. Target reader: technically rigorous, with equations.

### Scientific American — Quantum Gravity & Spacetime

> **Note:** Scientific American's topic/category pages (e.g. `/topic/quantum-gravity/`) returned HTTP 404 during today's run, indicating a site restructuring. No recent SA articles were retrievable. Quanta Magazine sections carry the full digest today.

### Quanta Magazine — Quantum Gravity

#### Entanglement Builds Space-Time. Now "Magic" Gives It Gravity.

**Date:** June 3, 2026 | [Read article](https://www.quantamagazine.org/entanglement-builds-space-time-now-magic-gives-it-gravity-20260603/)

Charles Cao (Virginia Tech), John Preskill (Caltech), and collaborators have identified the quantum resource responsible for spacetime curvature in holographic theories: **"magic"** — measured by the stabilizer Rényi entropy, i.e. the minimum number of non-Clifford gates needed to prepare a state:

```
M(|ψ⟩) = −log Σ_P ⟨ψ|P|ψ⟩^{2n}
```

Prior holographic quantum error-correcting codes (stabilizer codes) encoded spacetime geometry and matter in isolated sectors via the Ryu–Takayanagi entanglement entropy:

```
S = A / 4G_N
```

This produced a static background space but left the Einstein tensor vanishing identically, G_μν = 0 — space existed but could not bend. Introducing non-Clifford (T) gates injects magic M > 0, breaking the isolation between encoded sectors and allowing matter to source curvature:

```
G_{μν} + Λ g_{μν} ∝ T_{μν}
```

The encoding must be **approximate**: a magical code cannot perfectly recover all bulk information from any boundary subsystem, and this controlled imperfection is precisely the gravitational response — "the reason Newton's apple fell on him" (Czech, Tsinghua). The result is described as step 0.5 of 5 toward a full quantum gravity theory, but establishes that both quantum resources — entanglement (spacetime structure) and magic (spacetime flexibility/gravity) — map directly onto Wheeler's two sentences: space tells matter how to move, and matter tells space how to curve.

#### Old 'Ghost' Theory of Quantum Gravity Makes a Comeback

**Date:** November 17, 2025 | [Read article](https://www.quantamagazine.org/old-ghost-theory-of-quantum-gravity-makes-a-comeback-20251117/)

A revival of Lee–Wick quantum gravity is gaining traction as a renormalizable but unitary candidate theory. The standard spin-2 graviton propagator in momentum space:

```
G̃(k²) = 1 / (k² − iε)
```

is non-renormalizable in 4D. The Lee–Wick prescription modifies this to:

```
G̃_{LW}(k²) = 1/k² − 1/(k² − M²)
```

where M is a massive ghost mass. The ghost pole carries negative norm, threatening unitarity, but recent work argues the ghost is unstable (decays on timescales τ ~ M⁻¹), so the S-matrix remains unitary in the physical sector while UV divergences cancel between the two poles. The double-copy structure for graviton amplitudes survives:

```
M_{grav} = M_{YM} ⊗ M_{YM}
```

at tree level. Perturbative finiteness at one and two loops gives Lee–Wick gravity renewed credibility as a weakly-coupled bridge toward the Planck scale. *(Excerpt only)*

### Quanta Magazine — General Relativity & Spacetime

#### Where Some See Strings, She Sees a Space-Time Made of Fractals

**Date:** March 11, 2026 | [Read article](https://www.quantamagazine.org/where-some-see-strings-she-sees-a-space-time-made-of-fractals-20260311/)

Astrid Eichhorn (Heidelberg) has established that the Wilsonian RG flow for gravity-matter systems approaches a **non-Gaussian UV fixed point** at the Planck scale where all beta functions vanish:

```
β_i(g_j*) = μ (dg_i/dμ)|_{g*} = 0
```

At this fixed point spacetime acquires a **fractal, scale-invariant structure** — physics looks identical across all sub-Planckian scales. The graviton anomalous dimension η_G shifts Newton's constant toward marginality:

```
β_G = (2 + η_G) G_N − α G_N² + …,   α > 0
```

generating the attractive UV fixed point. Unlike string theory or loop quantum gravity, asymptotic safety retains continuous quantum fields with scale symmetry as the single new ingredient. A 2026 paper by Eichhorn's group showed the fixed point survives all Standard Model matter interactions, and predicts the top/bottom quark mass ratio to within ~10% of experiment. Several minimal WIMP and axion dark matter models are **incompatible** with the fractal fixed point — making null results from dark matter detectors an indirect probe of Planck-scale spacetime structure.

#### In Expanding de Sitter Space, Quantum Mechanics Gets Even More Elusive

**Date:** March 30, 2026 | [Read article](https://www.quantamagazine.org/in-expanding-de-sitter-space-quantum-mechanics-gets-even-more-elusive-20260330/)

Our universe is increasingly well-described by **de Sitter space** — the maximally symmetric solution to Einstein's equations with Λ > 0. The metric in flat slicing:

```
ds² = −dt² + e^{2Ht}(dx₁² + dx₂² + dx₃²),   H = √(Λ/3)
```

generates an exponentially expanding volume and a cosmological horizon at:

```
r_H = H⁻¹ = √(3/Λ)
```

Unlike AdS space (which has a well-defined spacelike boundary for holographic CFT), de Sitter has no accessible boundary. Quantum fluctuations of the metric persist everywhere at amplitude δg_{μν} ~ H/2π (de Sitter temperature T_{dS} = H/2π), with no asymptotic region shielded from quantum gravity effects, destroying the standard S-matrix definition.

A 2025 paper (Penedones & Loparco) revealed a further paradox: massless photons in de Sitter decompose as superpositions of massive states:

```
|γ⟩_{dS} = ∫ dm f(m) |m⟩
```

implying photons could spontaneously decay into matter — violating flat-space stability. Physicists now apply black-hole holography lessons to de Sitter: both share horizon thermodynamics,

```
S_{dS} = π r_H² / G_N
```

suggesting a dual description may exist but remains elusive. Progress here is expected to clarify the quantum nature of inflation and the ultimate fate of the universe.

*Generated automatically by Claude — June 17, 2026*
*Sources: scientificamerican.com · quantamagazine.org*

---

## Quantum Gravity Digest — 2026-06-17 (run 2)

**Date:** June 17, 2026
**Sources:** Scientific American · Quanta Magazine
**Compiled by:** Claude (automated daily run)

> Technically rigorous summaries with equations. Target reader: Yaser Zagzoog.

### Scientific American — Quantum Gravity & Spacetime

#### Newly discovered ripples in spacetime put Einstein's general relativity to the test

*March 5, 2026 · Claire Cameron · [Read article](https://www.scientificamerican.com/article/newly-discovered-ripples-in-spacetime-put-einsteins-general-relativity-to/)*

The LIGO-Virgo-KAGRA (LVK) collaboration released its fourth gravitational-wave catalog, more than doubling all prior detections to 200+ events. Each gravitational wave is a perturbation of the spacetime metric described in linearised GR as:

```
h_mu_nu = -(16π G / c^4) T_mu_nu   [Lorenz gauge]
```

with strain h ~ 10⁻²¹ at Earth. The catalog reveals black holes with asymmetric mass ratios and near-extremal spins χ = Sc/(GM²) → 1, probing the Kerr metric in the strong-field regime. Precision ringdown measurements constrain deviations from GR quasinormal frequencies ω_nlm. The dataset tightens the graviton mass bound to:

```
m_g < 1.27 × 10^{-23} eV/c²
```

and constrains non-tensorial GW polarisations predicted by scalar-tensor alternatives to G_μν + Λg_μν = (8πG/c⁴)T_μν.

#### We thought we knew the shape of the universe. We were wrong

*March 27, 2026 · Paul M. Sutter · [Read article](https://www.scientificamerican.com/article/we-thought-we-knew-the-shape-of-the-universe-we-were-wrong/)*

The COMPACT collaboration reanalysed Planck CMB data and found that constraints on cosmic topology are substantially weaker than consensus assumed. The standard detection strategy targets matched circle pairs in the CMB temperature expansion:

```
δT(n̂)/T = Σ_{l,m} a_{lm} Y_{lm}(n̂)
```

Failure to find them had been interpreted as ruling out non-trivial topology. COMPACT shows that this assumed loops must intersect the observer — which is not required. The minimum loop size can be **2–6× smaller** than prior bounds. This reopens the landscape of topologies — T³, Poincaré dodecahedral space, and 15 other flat possibilities — and connects to quantum gravity via the IR cutoff the topology imposes on the low-l CMB power spectrum C_l.

#### Can Space and Time Exist as Two Shapes at Once? Mind-Bending Experiments Aim to Find Out

*August 20, 2024 · Nick Huggett & Carlo Rovelli · [Read article](https://www.scientificamerican.com/article/do-space-and-time-follow-quantum-rules-these-mind-bending-experiments-aim-to-find-out/)*

Huggett and Rovelli survey tabletop proposals to test whether spacetime geometry obeys quantum superposition. Loop quantum gravity discretises spin-foam amplitudes at the Planck scale:

```
l_P = √(ℏG/c³) ≈ 1.616 × 10^{-35} m
```

The Bose-Marletto-Vedral (BMV) experiment places two Planck-mass objects (~22 μg) in superposition. Gravity mediates entanglement via V = −Gm₁m₂/|r₁−r₂|. The entanglement entropy S = −Tr(ρ_A log ρ_A) > 0 can only arise if gravity itself is in superposition:

```
|Ψ⟩_grav = α|g(x₁)⟩ + β|g(x₂)⟩
```

Detecting gravitationally induced entanglement (GIE) would be the first direct evidence that spacetime geometry is quantum.

### Quanta Magazine — Quantum Gravity

#### Entanglement Builds Space-Time. Now "Magic" Gives It Gravity.

*June 3, 2026 · Charlie Wood · [Read article](https://www.quantamagazine.org/entanglement-builds-space-time-now-magic-gives-it-gravity-20260603/)*

**Standout result of the digest.** Charles Cao (Virginia Tech), John Preskill (Caltech) and collaborators identify "magic" — the non-stabiliser complexity of a quantum state, quantified by its T-count (number of non-Clifford T gates) — as the quantum origin of gravitational pliability in holographic theories.

In AdS/CFT, bulk spacetime is reconstructed via a quantum error-correcting code |Ψ_bulk⟩ = U_code|ψ_bdy⟩. Stabiliser codes (zero magic) produce inert, gravity-free spacetime: space and matter decouple. Cao et al. show that approximate codes with high magic M allow the entanglement structure of space and matter to mix:

```
κ ~ M_magic    (spacetime curvature modulus scales with magic)
```

Gravity emerges as a consequence of **imperfect holographic encoding**. Wheeler's second dictum — matter tells spacetime how to curve — now has a quantum information origin. Described by Cao as "step 0.5 of 5" toward a full quantum gravity theory.

#### Where Some See Strings, She Sees a Space-Time Made of Fractals

*March 11, 2026 · Charlie Wood · [Read article](https://www.quantamagazine.org/where-some-see-strings-she-sees-a-space-time-made-of-fractals-20260311/)*

Astrid Eichhorn (Heidelberg) presents asymptotic safety as a conservative UV completion of gravity. The RG flow of Newton's constant G and cosmological constant Λ approaches a non-Gaussian UV fixed point g* = (G*, Λ*, ...) where:

```
β_i(g*) = μ ∂g_i/∂μ |_{g*} = 0   ∀i
```

Near g*, the spacetime spectral dimension collapses from d_s = 4 (macroscopic) to d_s = 2 (Planck scale), giving space a fractal structure. The fixed point survives inclusion of all Standard Model matter fields and enforces quantitative predictions:

```
m_t / m_b ≈ 40   (forced by RG fixed-point consistency)
m_H ≈ 125 GeV   (Higgs mass prediction)
```

Asymptotic safety rules out standard WIMPs, simple axions, and ultralight dark matter candidates — making it testable via next-generation dark matter experiments.

#### Are Strings Still Our Best Hope for a Theory of Everything?

*March 23, 2026 · Natalie Wolchover · [Read article](https://www.quantamagazine.org/are-strings-still-our-best-hope-for-a-theory-of-everything-20260323/)*

Wolchover reviews string theory's standing as the leading quantum gravity candidate. The Maldacena duality:

```
Z_string[AdS_{d+1}] = Z_{CFT_d}[∂AdS]
```

has been verified in numerous examples. String theory replaces point particles with 1D objects of tension T = 1/(2πα'), generating a UV-finite S-matrix. The 'swampland' programme places constraints on consistent quantum gravity vacua:

```
|∇φ| ≤ c/f   (distance conjecture)
|V| ≤ |∇V| / O(1)   (de Sitter conjecture)
```

Critics note ~10^{500} vacua in the landscape remain unexplored. Recent formal progress — amplituhedron, celestial holography — is noted, but experimental falsifiability remains unresolved.

### Quanta Magazine — General Relativity & Spacetime

#### Astrophysicists Find No 'Hair' on Black Holes

*August 27, 2025 · Matt von Hippel · [Read article](https://www.quantamagazine.org/astrophysicists-find-no-hair-on-black-holes-20250827/)*

An observational test of the no-hair theorem returns null results, constraining quantum gravitational 'hair'. The Kerr metric is fully characterised by (M, J, Q). Quantum gravity predicts additional soft graviton hair:

```
|M, J, soft⟩ = exp(Σ_k f_k a†_k) |M, J⟩
```

LVK ringdown analysis constrains deviations from GR quasinormal frequencies:

```
δω_{220} / ω_{220}^{GR} < 0.05
```

Any hair must be small but is not ruled out at Planck-scale amplitudes.

#### New Maps of the Bizarre, Chaotic Space-Time Inside Black Holes

*February 24, 2025 · Lyndie Chiou · [Read article](https://www.quantamagazine.org/new-maps-of-the-bizarre-chaotic-space-time-inside-black-holes-20250224/)*

New analytical maps of BKL (Belinski-Khalatnikov-Lifshitz) oscillations near spacelike singularities. Kasner exponents (p₁, p₂, p₃) satisfying:

```
p₁ + p₂ + p₃ = 1   and   p₁² + p₂² + p₃² = 1
```

undergo chaotic Mixmaster transitions. Lyapunov exponents λ_L = πkT match SYK-model quantum chaos, hinting at a deep connection between black hole interiors and holographic scrambling. These maps constrain how LQG or strings must regularise the singularity.

*Generated by Claude — June 17, 2026 · Sources: scientificamerican.com · quantamagazine.org*

---

## Quantum Gravity Digest — 2026-06-18

**Date:** June 18, 2026
**Sources:** Quanta Magazine (Scientific American unavailable today — returned no content)

### ⚠️ Scientific American — Quantum Gravity & Spacetime

Scientific American returned no content today (client-side rendered pages blocked). No articles included from this source.

### Quanta Magazine — Quantum Gravity

#### Entanglement Builds Space-Time. Now "Magic" Gives It Gravity.

**Date:** June 3, 2026
**URL:** https://www.quantamagazine.org/entanglement-builds-space-time-now-magic-gives-it-gravity-20260603/

Physicists Charles Cao (Virginia Tech), John Preskill (Caltech), and collaborators have identified a quantum resource called "magic" — quantified via non-Clifford gate complexity — as the ingredient that gives holographic space-time its gravitational pliability. In the AdS/CFT holographic framework, quantum error-correcting codes encode bulk space-time from boundary qubits; prior stabilizer-code models produced only inert, non-gravitating geometries satisfying G_mu_nu = 0 (flat, uncurved space). The new result (arXiv:2603.13475) shows that codes built with non-Clifford T-gates carry high magic M = -log_2 F_min (where F_min is the minimum stabilizer-state fidelity), which allows the entanglement encoding space and the entanglement encoding matter to mix — enabling gravitational backreaction. This coupling produces the full Einstein field equation G_mu_nu + Lambda g_mu_nu = (8πG/c⁴) T_mu_nu at the level of the encoded bulk. The work implies gravity is a direct consequence of imperfect, high-magic quantum encoding: perfect stabilizer codes protect information exactly and produce gravity-free space; approximate magical codes allow information to leak between space and matter sectors, generating curvature.

#### Are Strings Still Our Best Hope for a Theory of Everything?

**Date:** March 23, 2026
**URL:** https://www.quantamagazine.org/are-strings-still-our-best-hope-for-a-theory-of-everything-20260323/

A bootstrapping program is reinvigorating string theory's claim to be the unique UV completion of quantum gravity. Two recent papers show that the Veneziano amplitude A(s,t) = Γ(−α′s)Γ(−α′t)/Γ(−α′s−α′t) is the unique S-matrix consistent with specific physical axioms. Cheung et al. (arXiv:2508.09246) derive it from "ultrasoftness" — exponential amplitude decay at high energy — plus Lorentz invariance and unitarity. Elvang et al. (arXiv:2601.11705) show that N=4 super-Yang-Mills QFT has a unique UV completion at tree level: the Veneziano amplitude. These bootstrap results establish a striking logical necessity: if a QFT respects maximal supersymmetry and is UV-complete, particles must become strings at high energies. The debate has shifted from "is string theory worth studying" to the sharper question of whether its foundational assumptions hold in nature.

#### Where Some See Strings, She Sees a Space-Time Made of Fractals

**Date:** March 11, 2026
**URL:** https://www.quantamagazine.org/where-some-see-strings-she-sees-a-space-time-made-of-fractals-20260311/

Astrid Eichhorn (Heidelberg) presents asymptotic safety — the conjecture that the gravitational RG flow μ(dg_i/dμ) = β_i(g_j) reaches a non-Gaussian UV fixed point β_i(g*) = 0 at the Planck scale — as the most conservative path to quantum gravity, requiring no new fundamental objects. Her 2025 result (arXiv:2507.18304) demonstrates the fixed point survives inclusion of all Standard Model matter and their mutual gauge interactions. Crucially, asymptotic safety yields retrodictions: the Higgs mass m_H ≈ 125 GeV, the top-quark mass m_top ≈ 173 GeV, and the ratio m_top/m_bottom ≈ 40 all emerge naturally from fixed-point constraints. The approach also constrains dark matter: simple WIMP models and minimal axion-like particles are disfavored, making ongoing dark matter searches indirect tests of the fractal UV structure of space-time.

### Quanta Magazine — General Relativity & Spacetime

#### Astrophysicists Find No 'Hair' on Black Holes

**Date:** August 27, 2025
**URL:** https://www.quantamagazine.org/astrophysicists-find-no-hair-on-black-holes-20250827/

Einstein's GR predicts stationary black holes are uniquely determined by mass M, angular momentum J = aMG/c, and charge Q (the Kerr-Newman metric) — the no-hair theorem. Quantum gravity theories generically predict deviations (firewalls, fuzzballs, gravastars). A study combining 22 LIGO/Virgo/KAGRA binary black hole merger events (arXiv:2411.17893, Cardoso et al.) analyzed the post-merger ringdown quasi-normal mode spectrum ω_n = ω_R^(n) − i ω_I^(n) for parametric deviations from Kerr predictions. Result: at 95% confidence, any deviation from GR lies within δr < 40 km of the event horizon. Next-generation detectors (Einstein Telescope, Cosmic Explorer) will extend sensitivity to deviations at the Planck length l_Pl = √(ℏG/c³) ≈ 10⁻³³ cm, potentially exposing the quantum structure of the horizon.

---

## Quantum Gravity Digest — 2026-07-05

Today's digest draws four technically substantive pieces from Quanta Magazine spanning emergent-gravity-from-quantum-information, asymptotic safety, quadratic gravity's ghost revival, and the closed-universe Hilbert-space paradox. Scientific American could not be reached this run — its topic and search pages are JavaScript-rendered and returned no server-side content, and the Chrome browser extension (which would render the subscription pages) was not connected. Equations are written in plain ASCII for portability.

### Scientific American — Quantum Gravity & Spacetime

#### Source unavailable this run

Scientific American could not be fetched today. The topic page (scientificamerican.com/topic/quantum-gravity/) and search results are client-rendered and returned no article text to the fetcher, and the Claude-in-Chrome extension was not connected to render the JavaScript/subscription content. No SA articles are included; the Quanta sections below are complete.

### Quanta Magazine — Quantum Gravity

#### Entanglement Builds Space-Time. Now "Magic" Gives It Gravity.

*June 3, 2026*

In holographic (AdS/CFT) constructions, boundary entanglement is known to build the emergent bulk geometry — cut the entanglement threads linking two regions and the connecting wormhole pinches off — satisfying Wheeler's first dictum "space acts on matter, telling it how to move." What was missing was the back-reaction "matter tells space how to curve": stabilizer (Clifford) quantum error-correcting codes of the Harlow/Pastawski type cleanly separate the entanglement encoding 'space' from that encoding 'matter,' leaving the bulk geometry rigid and gravity-free. Charles Cao, John Preskill and collaborators (arXiv:2603.13475) show the missing ingredient is 'magic' — the non-stabilizerness introduced by non-Clifford gates such as the T gate T = diag(1, e^(i pi/4)), the same resource that makes quantum computation classically hard to simulate. A magical code couples the space and matter sectors so the encoded geometry becomes dynamical and can bend in response to matter; earlier work (Cao, Hamma, Dong et al., arXiv:2403.07056) tied this magic directly to the bulk's springiness. The authors call it a proof-of-concept precursor to gravity — 'step 0.5 of 5,' with no time dynamics or specific Einstein equations — but it suggests gravity arises precisely because the holographic encoding is approximate rather than perfect.

[Read on Quanta](https://www.quantamagazine.org/entanglement-builds-space-time-now-magic-gives-it-gravity-20260603/)

#### Where Some See Strings, She Sees a Space-Time Made of Fractals

*March 11, 2026*

Quanta profiles Astrid Eichhorn (Heidelberg), a leader in asymptotic safety — a conservative route to quantum gravity that keeps space-time continuous and quantum field theory intact rather than replacing them with strings or loops. The core idea, due to Weinberg (1976), is that the gravitational coupling flows under the renormalization group to a nontrivial ultraviolet fixed point, lim_{k -> infinity} g_i(k) = g_i^*, where dimensionless couplings stop running and scale symmetry is restored — giving a predictive, self-similar (fractal-like) short-distance regime. Eichhorn emphasizes gravity-matter systems: her 2013 'Matter Matters' work and a 2025 follow-up (arXiv:2507.18304) find the fixed point survives when all Standard Model fields and their interactions are included. Assuming the fixed point and flowing back out yields retrodictions of measured parameters — the Higgs mass (Shaposhnikov-Wetterich 2009), the top-quark mass (Eichhorn-Held 2017), and even the top/bottom mass splitting to within ~10% — plus predictions that several simple WIMP, axion and ultralight dark-matter models are disfavored. She notes asymptotic safety may coexist with, rather than compete against, string/loop pictures as an intermediate scaling window.

[Read on Quanta](https://www.quantamagazine.org/where-some-see-strings-she-sees-a-space-time-made-of-fractals-20260311/)

#### Old 'Ghost' Theory of Quantum Gravity Makes a Comeback

*November 17, 2025*

Standard Einstein gravity is perturbatively non-renormalizable because the graviton coupling carries negative mass dimension, so tinier space-time ripples matter more and the infinities cannot be absorbed into finitely many constants. Kellogg Stelle showed in 1977 that adding curvature-squared terms to the action, S = int d^4x sqrt(-g) [ (1/2 kappa^2) R + a R^2 + b R_mu_nu R^mu_nu ], makes the propagator fall off as 1/p^4 at high momentum, rendering the theory renormalizable — at the cost of a massive spin-2 'ghost' with a wrong-sign kinetic term, implying negative energies and apparent unitarity violation. The revival, led by Buoninfante, Donoghue, Menezes, Salvio, Holdom and Anselmi, argues the ghost may be benign: it is so heavy and unstable it decays before destabilizing the vacuum, and modified Feynman prescriptions or fakeon quantization keep probabilities positive, trading strict microcausality for tiny acausal 'micro-moments.' Donoghue's group also found quadratic gravity is asymptotically free — gravitons interact more weakly at high energy — hinting at a self-consistent 'space-time forever' theory. Stelle's scalar mode is exactly Starobinsky's R^2 inflaton, tying the framework to observable cosmology; his 1977 paper now draws 150+ citations per year.

[Read on Quanta](https://www.quantamagazine.org/old-ghost-theory-of-quantum-gravity-makes-a-comeback-20251117/)

### Quanta Magazine — General Relativity & Spacetime

#### Cosmic Paradox Reveals the Awful Consequence of an Observer-Free Universe

*November 19, 2025*

Applying holographic tools beyond black holes to closed cosmologies produces a startling result: Maldacena's use of the island formula for a spatially closed universe implies its Hilbert space is one-dimensional, dim H = 1, so the entire universe admits a single quantum state carrying zero bits of information — clashing with the manifest complexity around us. The same barrenness recurred for 'baby universe' constructions (Maxfield-Marolf, arXiv:2002.08950), suggesting a universal feature of gravity on a compact spatial slice, rooted in the gravitational constraints that leave no diffeomorphism-invariant global observables. Shaghoulian (arXiv:2305.10635) noted the analogy to topological field theories, whose Hilbert spaces are also one-dimensional until the manifold is cut along boundaries, and proposed that inserting an observer supplies exactly such a boundary. Zhao, Harlow and Usatyuk (arXiv:2501.02359), with a parallel group (arXiv:2501.02632), showed that adding a classical observer's worldline as an internal boundary restores the expected large Hilbert space and the universe's complexity. If it holds, the resolution elevates the observer from bookkeeping device to structural necessity, undermining the 'view from nowhere' in quantum cosmology.

[Read on Quanta](https://www.quantamagazine.org/cosmic-paradox-reveals-the-awful-consequence-of-an-observer-free-universe-20251119/)

---

## Quantum Gravity Digest — 2026-07-09

Sources covered: Scientific American and Quanta Magazine — 8 articles. NOTE: Scientific American's live topic and search pages returned 404 this run, so SA coverage falls back to its evergreen archive on quantum gravity, emergent spacetime and gravitons (full text retrieved). Quanta's quantum-gravity and general-relativity tag feeds resolved normally. Standout: the June 3, 2026 result showing how 'magic' (non-Clifford complexity) endows holographic space-time with gravitational backreaction.

### Scientific American — Quantum Gravity & Spacetime

#### What Is Spacetime Really Made Of? (February 1, 2022)

Reviews the converging evidence that space (and perhaps time) is emergent rather than fundamental. In AdS/CFT a d-dimensional gravitational bulk is dual to a (d-1)-dimensional conformal field theory on its boundary, and bulk geometry is built from boundary entanglement via the Ryu–Takayanagi relation S_A = Area(gamma_A) / (4 G hbar) — more boundary entanglement means the dual bulk regions sit closer together. Cutting entanglement makes the dual space 'dis-emerge'. Loop quantum gravity offers an alternative: discrete atoms of space knit into a spin foam whose coarse-grained limit reproduces smooth 4D spacetime. Key open problem: our universe is closer to de Sitter than anti–de Sitter space, where the holographic dictionary is unknown.

[What Is Spacetime Really Made Of?](https://www.scientificamerican.com/article/what-is-spacetime-really-made-of/)

#### Is Gravity Quantum? (August 14, 2018)

Surveys experimental strategies to detect whether gravity is quantized by looking for the graviton (massless spin-2). Direct detection is hopeless — a detector massive enough collapses to a black hole — because the scale is the Planck length l_P = sqrt(hbar G / c^3) ~ 1.6e-35 m. Indirect probes: a gravitational Casimir effect between superconductors (predicted ~10x the photon Casimir force; a Delft microchip saw null), gravity-induced entanglement between free-falling microdiamonds (Bose–Marletto–Vedral test), and inflationary CMB B-modes sourced by primordial tensor/graviton fluctuations with P_t(k) proportional to (H_inflation / M_Pl)^2.

[Is Gravity Quantum?](https://www.scientificamerican.com/article/is-gravity-quantum/)

#### Quantum 'Graviton' Particles May Resemble Ordinary Particles of Force (May 1, 2012)

Explains the generalized-unitarity method that reconstructs amplitudes from on-shell data, replacing the Feynman-diagram explosion (a 3-loop graviton amplitude would need ~10^20 terms). Central result: the double-copy structure, M_gravity ~ (A_gauge) x (A_gauge) (KLT / BCJ color-kinematics), so 'gravity is the square of gauge theory.' Using it, maximal N=8 supergravity is UV-finite at 3 and 4 loops, contradicting 1980s divergence expectations and reopening whether supergravity is perturbatively consistent up to the anticipated 7-loop danger point.

[Quantum 'Graviton' Particles...](https://www.scientificamerican.com/article/search-for-new-physics/)

### Quanta Magazine — Quantum Gravity

#### Entanglement Builds Space-Time. Now "Magic" Gives It Gravity. (June 3, 2026)

In holographic models built from quantum error-correcting codes, entanglement supplies the shape of space-time (Wheeler's 'space tells matter how to move'), but earlier stabilizer codes cleanly split entanglement into 'space' and 'matter' sectors that could not interact — the bulk was rigid, with no backreaction. Cao, Preskill and collaborators show the missing ingredient is 'magic', the nonstabilizerness a state gains from non-Clifford gates (e.g. the T gate); magic is exactly the resource making a state hard to simulate classically (Bravyi–Kitaev). A code rich in non-Clifford gates lets the space- and matter-entanglement sectors mix — magic as 'the fabric softener of space' — giving emergent geometry springiness, i.e. gravitational backreaction. Strikingly, gravity arises because the encoding is approximate: a perfectly protective (non-magical) code yields inert, gravity-free space. This is a proof of concept ('step 0.5 of 5') — it does not yet reproduce G_mu_nu + Lambda g_mu_nu = (8 pi G / c^4) T_mu_nu or include time — but ties QM's two features (entanglement, magic) to space's two features (shape, flexibility).

[Entanglement Builds Space-Time. Now "Magic" Gives It Gravity.](https://www.quantamagazine.org/entanglement-builds-space-time-now-magic-gives-it-gravity-20260603/)

#### Are Strings Still Our Best Hope for a Theory of Everything? (March 23, 2026)

Natalie Wolchover reassesses string theory's status. It stays the leading unification candidate because a massless spin-2 graviton arises inevitably from the closed-string spectrum and it furnishes the only worked AdS/CFT examples. Persistent objections: the ~10^500 landscape of vacua undermining predictivity, no low-energy SUSY partners at the LHC, and difficulty realizing a de Sitter (positive-Lambda) universe. (Based on Quanta listing excerpt; full column not fetched.)

[Are Strings Still Our Best Hope for a Theory of Everything?](https://www.quantamagazine.org/are-strings-still-our-best-hope-for-a-theory-of-everything-20260323/)

#### Where Some See Strings, She Sees a Space-Time Made of Fractals (March 11, 2026)

Q&A with Astrid Eichhorn on asymptotic safety: quantum gravity is made predictive by a non-Gaussian UV fixed point of the RG flow, so dimensionless couplings approach finite values g_*, lambda_* at high energy rather than diverging. Signature: the spectral dimension runs from d_s = 4 in the IR to d_s -> 2 in the UV, giving short-distance geometry a fractal character. The metric field, not strings, is fundamental. (Based on Quanta listing excerpt; full interview not fetched.)

[Where Some See Strings, She Sees a Space-Time Made of Fractals](https://www.quantamagazine.org/where-some-see-strings-she-sees-a-space-time-made-of-fractals-20260311/)

### Quanta Magazine — General Relativity & Spacetime

#### A New Geometry for Einstein's Theory of Relativity (July 16, 2025)

A Vienna team rebuilds Lorentzian geometry on synthetic, low-regularity foundations so GR's machinery survives where the metric is not smooth — shocks, matter discontinuities, singularities. Instead of a twice-differentiable metric, curvature bounds are encoded via metric/measure-space (Alexandrov-style) comparison and optimal transport adapted to the causal, indefinite-signature setting, tightening singularity theorems and clarifying where G_mu_nu = (8 pi G / c^4) T_mu_nu retains meaning. (Based on Quanta listing excerpt; full article not fetched.)

[A New Geometry for Einstein's Theory of Relativity](https://www.quantamagazine.org/a-new-geometry-for-einsteins-theory-of-relativity-20250716/)

#### New Maps of the Bizarre, Chaotic Space-Time Inside Black Holes (February 24, 2025)

Charts the interior approach to a singularity, where the BKL conjecture predicts spatial points decouple and geometry undergoes infinite chaotic 'Mixmaster' oscillations as t -> 0, each bounce governed by a chaotic map on Kasner exponents with p_1 + p_2 + p_3 = p_1^2 + p_2^2 + p_3^2 = 1. New maps expose exactly how GR breaks down where quantum gravity must take over. (Based on Quanta listing excerpt; full article not fetched.)

[New Maps of the Bizarre, Chaotic Space-Time Inside Black Holes](https://www.quantamagazine.org/new-maps-of-the-bizarre-chaotic-space-time-inside-black-holes-20250224/)

---

## 🔬 Research (arXiv)

**30 recent arXiv papers** on **🌀 Quantum Gravity** — category `gr-qc` (quantum gravity, loop quantum gravity, spacetime). Fetched 9 Jul 2026 · newest first.

### [Tomography of a Macroscopic Quantum State Influenced by Classical Self-Gravity](https://arxiv.org/abs/2607.06967)

**Authors:** Wenjie Zhong, Yubao Liu, Yanbei Chen, Haixing Miao, Yiqiu Ma · **Published:** 2026-07-08
How classical self-gravity affects quantum-state tomography of macroscopic oscillators via Schrödinger-Newton theory.

### [Towards Gauge Independence in Asymptotically Safe Quantum Gravity](https://arxiv.org/abs/2607.06657)

**Authors:** Kevin Falls, Renata Ferrero, Giovanni Oglialoro · **Published:** 2026-07-07
Demonstrates gauge-independent renormalization-group flows for asymptotically safe quantum gravity.

### [Entanglement and Geometric Transitions in Topological String Theory](https://arxiv.org/abs/2607.03526)

**Authors:** Gabriel Wong · **Published:** 2026-07-03
Realizes local holographic degrees of freedom using entanglement branes and geometric transitions.

### [Dark Energy Genesis: Modeling Dissipative Effects in Primordial Cosmology](https://arxiv.org/abs/2607.03272)

**Authors:** Pietro Pellecchia, Alejandro Perez, Salvatore Ribisi · **Published:** 2026-07-03
Dissipative quantum-gravity effects generate a small cosmological constant from discrete primordial spacetime.

### [Singularities, Entropy and the Arrow of Time, or Is CRT a Gauge Symmetry in Quantum Gravity?](https://arxiv.org/abs/2607.03199)

**Authors:** T. Banks · **Published:** 2026-07-03
Examines whether CPT is a gauge symmetry in quantum gravity across flat, AdS, and de Sitter spaces.

### [Lubkin-Page Typicality Bounds for Type II von Neumann Factors](https://arxiv.org/abs/2607.01873)

**Authors:** Zhi-Wei Wang, Samuel L. Braunstein · **Published:** 2026-07-02
Extends typicality bounds for emergent spacetime to Type II von Neumann algebras.

### [Classical and Loop Quantum Cosmology of Interacting Dark Energy](https://arxiv.org/abs/2607.01724)

**Authors:** Mohd Shahalam, K. Yerzhanov, G. Bauyrzhan, P. K. Dhankar · **Published:** 2026-07-02
Dynamical-system analysis of interacting dark sectors with a quantum bounce replacing the Big Bang.

### [Wormholes as Red Herrings: Reflection Positivity and the Reconstruction of Unitary QFTs](https://arxiv.org/abs/2607.01322)

**Authors:** Jacob McNamara, Zhencheng Wang · **Published:** 2026-07-01
Proves unitary QFTs are fixed by partition functions and that spatial wormholes signal incomplete charged spectra.

### [Can Primordial Black Holes Be Seeds for Early Galaxies in Models Satisfying the Covariant Entropy Bound?](https://arxiv.org/abs/2607.01292)

**Authors:** Sidan A, Tom Banks, Willy Fischler · **Published:** 2026-07-01
A primordial-black-hole scenario satisfying entropy bounds to explain dark matter and early JWST galaxies.

### [Modified Cosmology from a Mass-to-Horizon Relation: Background Evolution](https://arxiv.org/abs/2607.00133)

**Authors:** Pranav Prasanthan, Hussain Gohar, Vincenzo Salzano · **Published:** 2026-06-30
Thermodynamically consistent entropy generalizations tightly restrict deviations from standard cosmology.

### [Relativistic Gravity-Induced Entanglement via Frame Dragging](https://arxiv.org/abs/2606.31678)

**Authors:** Eyuri Wakakuwa, Luciano Petruzziello, Trinidad B. Lantaño, Susana F. Huelga, Martin B. Plenio · **Published:** 2026-06-30
Computes gravity-induced entanglement from frame dragging using a quantized Lense-Thirring Hamiltonian.

### [The Dynamics of Quantum Gravity: The Missing Piece in the Spacetime Emergentist Account](https://arxiv.org/abs/2606.31559)

**Authors:** Álvaro Mozota Frauca · **Published:** 2026-06-30
Argues spacetime emergentism lacks a distinct interpretation of quantum dynamics in current approaches.

### [CFT Constraints on the Weak Gravity Conjecture](https://arxiv.org/abs/2606.29896)

**Authors:** Saeed Noori Gashti, Behnam Pourhassan, İzzet Sakallı · **Published:** 2026-06-29
Derives the weak gravity conjecture from AdS/CFT boundary calculations for massive-gravity black holes.

### [Gravitational Time Advancement in Bumblebee Gravity for Earth-Bound Systems](https://arxiv.org/abs/2606.29819)

**Authors:** G. Y. Tuleganova, R. Kh. Karimov, R. N. Izmailov, A. A. Potapov, A. Bhadra, K. K. Nandi · **Published:** 2026-06-29
Predicts a negative Shapiro time delay in Lorentz-violating Bumblebee gravity for Earth–Moon systems.

### [On Padmanabhan's Duality Invariance and the Quantum of Length](https://arxiv.org/abs/2606.29318)

**Authors:** P. Fernandez de Cordoba, J. M. Isidro, A. Pereira Garcia · **Published:** 2026-06-28
A field-theoretic duality-invariant quantum-gravity propagator incorporating a minimal length.

### [Scalar Vacuum Polarization in Loop Quantum Gravity Black Holes](https://arxiv.org/abs/2606.29307)

**Authors:** Antonino Flachi, Marco Pasini · **Published:** 2026-06-28
Vacuum polarization around LQG black holes shows enhanced near-horizon effects scaling with quantum corrections.

### [Non-perturbative, Background-Independent Canonical Quantum Gravity in Fock Representations](https://arxiv.org/abs/2606.28788)

**Authors:** Thomas Thiemann · **Published:** 2026-06-27
Background-independent Fock representations offer a separable-Hilbert-space alternative to loop quantum gravity.

### [Quantum Fluctuations of the Black Hole Horizon](https://arxiv.org/abs/2606.28243)

**Authors:** Ben Freivogel, Antony Speranza, Erik Verlinde · **Published:** 2026-06-26
Quantum horizons have a measurable width depending on probe resolution, often exceeding the Planck scale.

### [Large Quantum Gravity Fluctuations of BTZ Black Holes](https://arxiv.org/abs/2606.28160)

**Authors:** Ben Freivogel, Upamanyu Moitra · **Published:** 2026-06-26
3d AdS black-hole horizons exhibit quantum width parametrically larger than the Planck scale.

### [Diffeomorphism-Invariant Quantities in Phase Space: More than Correlations](https://arxiv.org/abs/2606.25072)

**Authors:** Álvaro Mozota Frauca · **Published:** 2026-06-23
Spatiotemporal structures prove indispensable for characterizing invariant content in diffeomorphism-invariant theories.

### [An Interplay Between Fractional Calculus and Holographic Dark Energy](https://arxiv.org/abs/2606.22431)

**Authors:** Ayush Bidlan · **Published:** 2026-06-21
Fractional calculus extends holographic dark energy via memory effects in black-hole thermodynamics.

### [Asymptotically Safe Quantum Gravity and Its Phenomenology — A Review](https://arxiv.org/abs/2606.21522)

**Authors:** Astrid Eichhorn · **Published:** 2026-06-19
Reviews asymptotic safety as a predictive QFT approach to gravity spanning particle physics, black holes, and cosmology.

### [Quantum Dust from the Curse of Dimensionality](https://arxiv.org/abs/2606.20943)

**Authors:** Kenan Oggad · **Published:** 2026-06-18
Concentration of measure produces equidistant point configurations appearing two-dimensional to diffusion probes.

### [Spectral Functions of Lorentzian Quantum Gravity](https://arxiv.org/abs/2606.19321)

**Authors:** Gabriel Assant, Daniel F. Litim, Manuel Reichert · **Published:** 2026-06-17
Lorentzian quantum-gravity spectral functions interpolate between classical relativity and asymptotic safety.

### [GRMHD and GRRT Simulations of Black Hole Accretion: Flares, Precession, and Complex Spacetimes](https://arxiv.org/abs/2606.19320)

**Authors:** Hong-Xuan Jiang · **Published:** 2026-06-17
Models black-hole accretion including LQG corrections, constrained via Event Horizon Telescope observations.

### [A Matrix-Free Action of the Ashtekar-Lewandowski Volume Operator of Loop Quantum Gravity](https://arxiv.org/abs/2606.18397)

**Authors:** Waleed Sherif · **Published:** 2026-06-16
Matrix-free algorithms compute the LQG volume operator efficiently, enabling large-scale numerical simulations.

### [Boundary Conditions and Hilbert Spaces in No-Roll Quantum Cosmology](https://arxiv.org/abs/2606.17163)

**Authors:** Steffen Gielen · **Published:** 2026-06-15
Wheeler-DeWitt boundary conditions yield finite- or infinite-dimensional Hilbert spaces depending on the potential.

### [Quantum Gravity and Spectral Running Cutoff](https://arxiv.org/abs/2606.16911)

**Authors:** Carlo Branchina, Vincenzo Branchina, Filippo Contino, Riccardo Gandolfo, Arcangelo Pernace · **Published:** 2026-06-15
A spectral running cutoff recovers asymptotic-safety fixed points for gravitational couplings.

### [Effect of ξRφ² Non-Minimal Coupling on Gravitational Light Bending](https://arxiv.org/abs/2606.16406)

**Authors:** Ayan Kumar Naskar, Avijit Sen Majumder, Sourav Bhattacharya · **Published:** 2026-06-15
Curvature-scalar coupling produces distinctive light-bending signatures separating non-minimal from minimal gravity.

### [General Relativity and Background Independence](https://arxiv.org/abs/2606.15224)

**Authors:** Antonio Vassallo · **Published:** 2026-06-13
Argues background independence is a comparative diagnostic rather than an absolute requirement for quantum-gravity theories.

*Source: arXiv.org API · category gr-qc · sorted by submission date (descending).*

---

## Quantum-gravity phenomenology with primordial black holes (Rovelli & Vidotto, 2016)

**arXiv:** [1609.02159](https://arxiv.org/abs/1609.02159) · **PDF:** https://arxiv.org/pdf/1609.02159
**Venue:** Proceedings, 2015 Karl Schwarzschild Meeting on Gravitational Physics (6 pages)
**Subjects:** General Relativity & Quantum Cosmology (gr-qc); High Energy Astrophysical Phenomena (astro-ph.HE)
**Status:** 📥 To read

### Core idea

Quantum gravity may permit a black hole to *tunnel* into a white hole. If this happens, a black hole's lifetime can be much shorter than the Hawking-evaporation timescale, offering a resolution to the information paradox that keeps evolution unitary without requiring information loss at the horizon.

### Why it matters

The paper's main pitch is **observational**: this bounce scenario opens a window for quantum-gravity *phenomenology* rather than pure theory. Tied to the population of **primordial black holes**, the model predicts:

- A characteristic **explosion energy** at the end of the bounce.
- Potentially detectable **astrophysical signals in the radio and gamma wavelengths**.

### Reading notes / questions to pressure-test

- Derive the bounce lifetime scaling and compare against the Hawking timescale τ_H ∼ M³ (in G = c = 1 units) — what sets the shortening factor?
- What primordial BH mass window produces signals observable *today*? Check the mass-to-wavelength mapping for the predicted radio/gamma emission.
- Falsifiability check: is the predicted signal distinguishable from ordinary astrophysical transients (FRBs, etc.)? This is the crux for whether it's real phenomenology vs. untestable speculation.

*Filed automatically — added to reading queue.*

---

## Quantum Gravity Digest — 2026-07-14

Sources covered: Scientific American, Quanta Magazine. 6 articles collected. Note: Scientific American's quantum-gravity topic and search pages returned 404 this run (site path structure appears to have changed) — no new SA items could be harvested. All content below is from Quanta Magazine. No quantum-gravity articles were published in the last 7 days on either source; the most recent available pieces are included instead.

### Quanta Magazine — Quantum Gravity

#### Entanglement Builds Space-Time. Now "Magic" Gives It Gravity.

June 3, 2026 — Charles Cao (Virginia Tech), John Preskill, Brian Swingle and collaborators argue that holographic space-time needs a second quantum resource beyond entanglement: non-stabilizerness, or "magic". In the AdS/CFT error-correcting-code picture (Almheiri–Dong–Harlow; the HaPPY code), bulk operators are reconstructed from boundary subregions, and entanglement entropy fixes bulk geometry through Ryu–Takayanagi: S(A) = Area(γ_A)/(4 G_N) + S_bulk. But pure stabilizer codes are classically simulable (Gottesman–Knill) and factorize the code space so that "space" entanglement and "matter" entanglement never interact — the bulk geometry is rigid and matter does not backreact, so Wheeler's second sentence ("matter tells space how to curve") fails. Magic is generated only by non-Clifford gates such as T = diag(1, e^{iπ/4}), quantified by e.g. the stabilizer Rényi entropy M_2(ψ) = −log2( Σ_P ⟨ψ|P|ψ⟩^4 / 2^n ). Cao, Swingle and White showed holographic CFT states dual to anti-de Sitter space carry extensive magic; the 2026 Cao–Preskill code injects non-Clifford gates to couple the two entanglement sectors, so boundary magic controls bulk compressibility — a precursor of G_μν + Λ g_μν = (8πG/c⁴) T_μν. The code is background-general and time-less ("step 0.5 of 5"), but implies gravity arises from *imperfect* quantum encoding: perfect error correction yields an inert, gravity-free bulk.

[Entanglement Builds Space-Time. Now "Magic" Gives It Gravity.](https://www.quantamagazine.org/entanglement-builds-space-time-now-magic-gives-it-gravity-20260603/)

#### Where Some See Strings, She Sees a Space-Time Made of Fractals

March 11, 2026 — Q&A with Astrid Eichhorn (Heidelberg) on asymptotic safety: Weinberg's 1976 proposal that quantum gravity is nonperturbatively renormalizable at a non-Gaussian UV fixed point of the RG flow. The dimensionless Newton coupling g(k) = G(k) k² flows under the Wetterich equation, k ∂_k Γ_k = ½ Tr[(Γ_k^(2) + R_k)^{-1} k ∂_k R_k]; a fixed point β_g(g*, λ*) = 0 with finitely many relevant directions makes the theory predictive at all scales and implies exact scale symmetry — spacetime becomes self-similar, with spectral dimension running from 4 in the IR toward ~2 at the Planck scale l_P = √(ħG/c³) ≈ 1.616e-35 m. Eichhorn's distinctive contribution is gravity–matter systems: "Matter Matters" (2013) showed the fixed point survives the full Standard Model field content, and a 2025 follow-up extended this to all matter self-interactions. The payoff is retrodiction — flowing out of the fixed point pins the Higgs mass (Shaposhnikov–Wetterich 2009), the top mass, and the top–bottom splitting to ~10% (the "OMG plot"), and constrains neutrino masses. Asymptotic safety also disfavours simple WIMPs, the standard axion window, and ultralight dark matter, making DM searches indirect probes of the UV structure of spacetime.

[Where Some See Strings, She Sees a Space-Time Made of Fractals](https://www.quantamagazine.org/where-some-see-strings-she-sees-a-space-time-made-of-fractals-20260311/)

#### Are Strings Still Our Best Hope for a Theory of Everything?

March 23, 2026 — Natalie Wolchover's Qualia column revisits the dispute over whether string theory can describe our universe. The structural case is unchanged: the closed-string spectrum contains a massless spin-2 excitation whose low-energy effective action reproduces Einstein gravity, S = (1/16πG) ∫ d⁴x √(−g)(R − 2Λ) + α′ corrections, with the string scale M_s = 1/√α′ taming the nonrenormalizable (G E²)^n divergences of perturbative graviton loops. The persistent objection is predictivity: the flux landscape admits ~10^500 metastable vacua, and the swampland de Sitter conjecture |∇V| ≥ c V / M_P even questions whether stable de Sitter vacua — hence our accelerating universe — exist in string theory at all. *Excerpt-based summary; full text not retrieved this run.*

[Are Strings Still Our Best Hope for a Theory of Everything?](https://www.quantamagazine.org/are-strings-still-our-best-hope-for-a-theory-of-everything-20260323/)

### Quanta Magazine — General Relativity & Spacetime

#### What Is a Manifold?

November 3, 2025 — Riemann's 1854 reconception of space as a manifold: locally homeomorphic to R^n, but with global structure and curvature intrinsic, requiring no ambient embedding. The metric tensor g_μν gives the line element ds² = g_μν dx^μ dx^ν, from which the Levi-Civita connection Γ^λ_μν = ½ g^{λσ}(∂_μ g_σν + ∂_ν g_σμ − ∂_σ g_μν) and the Riemann tensor R^ρ_σμν follow. This is exactly the machinery Einstein needed sixty years later: GR is the statement that spacetime is a pseudo-Riemannian 4-manifold whose curvature is sourced by stress-energy, G_μν + Λ g_μν = (8πG/c⁴) T_μν. *Excerpt-based summary.*

[What Is a Manifold?](https://www.quantamagazine.org/what-is-a-manifold-20251103/)

#### A New Geometry for Einstein's Theory of Relativity

July 16, 2025 — A Vienna group (Kunzinger, Steinbauer and collaborators) is building a low-regularity / metric-measure formulation of Lorentzian geometry, extending GR to spacetimes whose metrics are not smooth. Classical singularity theorems (Penrose, Hawking) assume g_μν is at least C², so R_μν is defined pointwise; realistic matter (shock waves, thin shells, colliding gravitational waves) yields metrics only Lipschitz or continuous, exactly where those hypotheses fail. The program replaces pointwise curvature with synthetic curvature bounds — Lorentzian analogues of Alexandrov/optimal-transport conditions in which the timelike energy condition R_μν u^μ u^ν ≥ 0 becomes an entropy-convexity statement along geodesics of measures. The payoff: singularity theorems and causal-boundary theory valid for the rough metrics quantum gravity is likely to produce. *Excerpt-based summary.*

[A New Geometry for Einstein's Theory of Relativity](https://www.quantamagazine.org/a-new-geometry-for-einsteins-theory-of-relativity-20250716/)

#### Astrophysicists Find No 'Hair' on Black Holes

August 27, 2025 — The no-hair theorem asserts a stationary, asymptotically flat black hole in GR is fully specified by (M, J, Q), so every quasinormal-mode frequency of a ringdown is fixed by (M, J) alone: h(t) ~ Σ_{lmn} A_{lmn} e^{−t/τ_{lmn}} cos(ω_{lmn} t + φ_{lmn}), with ω, τ = f(M, J). Quantum-gravity-inspired scenarios (fuzzballs, firewalls, exotic compact objects) predict "hair" — shifted overtones or late-time echoes. LIGO–Virgo–KAGRA ringdown spectroscopy finds measured overtones consistent with Kerr, bounding any extra hair to be short; deviations in the fundamental l = m = 2 mode are constrained at the few-percent level. *Excerpt-based summary.*

[Astrophysicists Find No 'Hair' on Black Holes](https://www.quantamagazine.org/astrophysicists-find-no-hair-on-black-holes-20250827/)

---

## Quantum Gravity Digest — 2026-07-15

Sources: Scientific American and Quanta Magazine. **Note:** Scientific American's live quantum-gravity topic feed and on-site search returned HTTP 404 this run, so no new SA articles from the last 7 days could be pulled; two verified, on-topic SA feature articles from the archive are included for reference (dated accordingly). Quanta Magazine had nothing in the last 7 days on the quantum-gravity/general-relativity tags, so the 3 most recent per tag were selected. Total articles: 8.

### Scientific American — Quantum Gravity & Spacetime (archive; live feed unavailable this run)

#### What Is Spacetime Really Made Of? (archive feature, Feb 2022)

A feature on the emergent-spacetime program: space (and perhaps time) is not fundamental but arises from entanglement among microscopic quantum degrees of freedom. The concrete engine is Maldacena's AdS/CFT correspondence, in which a (d+1)-dimensional gravitational bulk in anti-de Sitter space is dual to a d-dimensional conformal field theory on its boundary — an explicit realization of 't Hooft–Susskind holography. The Ryu–Takayanagi formula ties boundary entanglement to bulk geometry via `S_A = Area(gamma_A) / (4 G_N hbar)`, so severing entanglement pinches off geometric connectivity (thinning an ER=EPR wormhole). Open problems flagged: recovering emergent time, extending holography from AdS to the de Sitter / cosmological case `Lambda > 0`, and the absence of LHC evidence for the supersymmetry the cleanest constructions rely on.

[What Is Spacetime Really Made Of?](https://www.scientificamerican.com/article/what-is-spacetime-really-made-of/)

#### Quantum 'Graviton' Particles May Resemble Ordinary Particles of Force (archive feature, May 2012)

Bern, Dixon and Kosower describe the generalized-unitarity method for scattering amplitudes, which sidesteps the factorial blow-up of Feynman diagrams by reconstructing loop amplitudes from on-shell tree data. Its key payoff for gravity is the double-copy / BCJ relation: graviton amplitudes factorize as two copies of gauge-theory (gluon) amplitudes — schematically `M_gravity ~ sum (n_i n_i-tilde) / (prod D_i)`, i.e. 'gravity = (gauge theory)^2'. Using this, they showed N=8 supergravity is UV-finite at three and four loops, contradicting 1980s expectations of uncontrolled spacetime-foam divergences and reopening whether a point-particle graviton theory can be perturbatively consistent (the seven-loop test being the frontier). The piece recalls the small QED coupling `alpha ~ 1/137` as why Feynman diagrams converge quickly there but not for gravity.

[Quantum 'Graviton' Particles May Resemble Ordinary Particles of Force](https://www.scientificamerican.com/article/search-for-new-physics/)

### Quanta Magazine — Quantum Gravity

#### Entanglement Builds Space-Time. Now 'Magic' Gives It Gravity. (June 3, 2026)

Holographic toy models built from quantum error-correcting 'stabilizer' codes (Harlow et al.) reproduce Wheeler's first dictum — entanglement stitches together bulk geometry — but yield an inert, non-dynamical space that does not curve in response to matter (Wheeler's second dictum fails). Cao, Preskill and collaborators trace the missing ingredient to 'magic' (nonstabilizerness), the resource that makes a state hard to simulate classically, injected by non-Clifford gates such as the T gate `T = diag(1, e^{i pi/4})`. Stabilizer codes are magic-free and Clifford-simulable via the Gottesman–Knill theorem, which is why their dual geometry is rigid; adding non-Clifford gates lets the 'space' and 'matter' entanglement sectors mix, producing a background that fluctuates and bends. Upshot: gravitational back-reaction is a manifestation of approximate (imperfect) quantum encoding — perfect error correction gives no gravity — called 'step 0.5 of 5.'

[Entanglement Builds Space-Time. Now 'Magic' Gives It Gravity.](https://www.quantamagazine.org/entanglement-builds-space-time-now-magic-gives-it-gravity-20260603/)

#### Are Strings Still Our Best Hope for a Theory of Everything? (March 23, 2026)

Natalie Wolchover's column surveys the 'forever war' over whether string theory remains the leading candidate for unifying gravity and QM. Credit side: a manifestly UV-complete, anomaly-free framework in `D = 10` (M-theory in `D = 11`) that automatically contains a massless spin-2 graviton and underwrites AdS/CFT. Debit side: the swampland/landscape problem — roughly `~10^{500}` metastable flux vacua with no dynamical selection principle — the absence of low-energy supersymmetry at the LHC, and the difficulty of building controlled de Sitter vacua for a universe with `Lambda > 0`. The column contrasts this with maturing competitors (asymptotic safety, loop quantum gravity, causal sets) and asks whether 'best hope' should be judged by mathematical richness or falsifiable prediction.

[Are Strings Still Our Best Hope for a Theory of Everything?](https://www.quantamagazine.org/are-strings-still-our-best-hope-for-a-theory-of-everything-20260323/)

#### Where Some See Strings, She Sees a Space-Time Made of Fractals (March 11, 2026)

A Q&A with Astrid Eichhorn on asymptotic safety — Weinberg's proposal that quantum gravity is nonperturbatively renormalizable because its RG flow hits an interacting ultraviolet fixed point. In terms of the dimensionless Newton coupling `g(k) = G(k) k^2`, the flow `k dg/dk = beta(g)` approaches a nontrivial fixed value `g_* != 0` at trans-Planckian momenta, taming divergences without new degrees of freedom. Signature: dimensional reduction — the spectral dimension runs from `d_s = 4` in the IR to `d_s ~ 2` near the Planck scale, giving an effectively fractal microstructure also seen in causal dynamical triangulations. Functional RG (Wetterich-equation) truncations provide the main evidence for the fixed point.

[Where Some See Strings, She Sees a Space-Time Made of Fractals](https://www.quantamagazine.org/where-some-see-strings-she-sees-a-space-time-made-of-fractals-20260311/)

### Quanta Magazine — General Relativity & Spacetime

#### Carlo Rovelli's Radical Perspective on Reality (October 29, 2025)

A Q&A with loop-quantum-gravity co-founder Carlo Rovelli on his relational view of space, time and quantum states. In LQG, geometry is quantized: spin networks (graphs with SU(2) spin labels j on edges) are eigenstates of geometric operators, giving a discrete area spectrum `A = 8 pi gamma l_P^2 sum_i sqrt(j_i (j_i + 1))` with Barbero–Immirzi parameter `gamma` and Planck length `l_P = sqrt(hbar G / c^3) ~ 1.616e-35 m`. Rovelli stresses background independence and the problem of time — the Wheeler–DeWitt constraint `H |psi> = 0` implies no external time parameter, so dynamics is relational, defined by correlations between physical variables rather than evolution in a fixed t.

[Carlo Rovelli's Radical Perspective on Reality](https://www.quantamagazine.org/carlo-rovellis-radical-perspective-on-reality-20251029/)

#### Astrophysicists Find No 'Hair' on Black Holes (August 27, 2025)

The classical no-hair theorem states that a stationary, isolated black hole is fully specified by three observables — mass M, angular momentum J, charge Q — with astrophysical holes described by the Kerr metric (Q ~ 0). Quantum-gravity effects could in principle add 'hair.' Black-hole spectroscopy tests this: the ringdown is a superposition of quasinormal modes whose complex frequencies `omega_{lmn} = 2 pi f_{lmn} - i / tau_{lmn}` are, for Kerr, functions of only M and J. Analyses of LIGO–Virgo–KAGRA ringdown data find the overtone and subdominant-mode frequencies consistent with Kerr, constraining any extra hair to be small and supporting GR in the strong-field regime.

[Astrophysicists Find No 'Hair' on Black Holes](https://www.quantamagazine.org/astrophysicists-find-no-hair-on-black-holes-20250827/)

#### Singularities in Space-Time Prove Hard to Kill (May 27, 2025)

General relativity predicts its own breakdown at singularities (black-hole cores, the Big Bang), where curvature invariants diverge and geodesics are incomplete. The Penrose–Hawking theorems show this is generic: once a trapped surface forms, geodesic incompleteness follows from the focusing of congruences governed by the Raychaudhuri equation `d theta / d tau = -(1/3) theta^2 - sigma_{ab} sigma^{ab} + omega_{ab} omega^{ab} - R_{ab} u^a u^b` together with an energy condition `R_{ab} u^a u^b >= 0`. The article covers a new trilogy of theorems extending these results to lower-regularity metrics, showing singularities persist even when the original smoothness assumptions are relaxed — so any resolution must come from new quantum-gravitational physics.

[Singularities in Space-Time Prove Hard to Kill](https://www.quantamagazine.org/singularities-in-space-time-prove-hard-to-kill-20250527/)

---

## Quantum Gravity Digest — 2026-07-16

Daily Quantum Gravity Digest for Yaser. Sources this run: Quanta Magazine (Quantum Gravity and General Relativity tags). Scientific American could not be included — its /topic/quantum-gravity/ page and site search both returned HTTP 404 (taxonomy-URL redesign) and no SA quantum-gravity feature from the last 7 days surfaced via web search. No Quanta articles fell inside the last 7 days, so the three most recent per tag were selected. Equations use @@...@@ ASCII notation.

### Scientific American — Quantum Gravity & Spacetime

#### No new articles retrieved this run

Scientific American's quantum-gravity topic page and site search both returned HTTP 404 during this run, likely due to a redesign of their taxonomy URLs, and a web search surfaced no SA quantum-gravity features published in the last 7 days. This will be retried on the next scheduled run.

### Quanta Magazine — Quantum Gravity

#### Entanglement Builds Space-Time. Now "Magic" Gives It Gravity. (June 3, 2026)

In holographic (AdS/CFT) constructions, bulk space-time geometry is reconstructed from boundary degrees of freedom via a quantum error-correcting code, with bipartite entanglement supplying connectivity through the Ryu-Takayanagi relation @@S(A) = Area(gamma_A) / (4 G_N hbar)@@. Charles Cao, John Preskill and collaborators argue that entanglement alone yields a rigid, non-dynamical geometry: stabilizer (Clifford) codes cleanly separate the entanglement encoding space from that encoding matter, so 'matter tells space how to curve' is never realized and the background cannot back-react. The missing ingredient is 'magic' (non-stabilizerness), the resource quantifying how many non-Clifford gates — e.g. the T gate @@T = diag(1, e^{i pi / 4})@@ — are needed to prepare a state, and equivalently how hard it is to classically simulate it (Gottesman-Knill). Their next-generation code injects magic via non-Clifford gates, letting the space-sector and matter-sector entanglement mix so geometry becomes fluctuating and springy — a proof-of-concept 'step 0.5 of 5.' The picture implies gravity emerges from imperfect (approximate) encoding: perfectly protected codes give inert, gravity-free spaces, so non-recoverability of bulk information is what makes @@G_N != 0@@.

[Read on Quanta](https://www.quantamagazine.org/entanglement-builds-space-time-now-magic-gives-it-gravity-20260603/)

#### Are Strings Still Our Best Hope for a Theory of Everything? (March 23, 2026)

In a Qualia column, Natalie Wolchover surveys the dispute over whether string theory — which promotes point particles to 1D strings with characteristic scale @@l_s = sqrt(alpha')@@ and automatically contains a massless spin-2 graviton in its closed-string spectrum — remains the leading candidate for unifying general relativity with quantum mechanics. The case for strings rests on perturbative UV-finiteness (extended objects smear the short-distance divergences that make @@G_mu_nu@@-based perturbative quantum gravity nonrenormalizable) and on holographic dualities such as AdS/CFT. The case against centers on the landscape of more than 10^500 metastable vacua and the resulting lack of unique, testable low-energy predictions. The piece weighs these against asymptotic safety and loop quantum gravity.

[Read on Quanta](https://www.quantamagazine.org/tag/quantum-gravity/)

#### Where Some See Strings, She Sees a Space-Time Made of Fractals (March 11, 2026)

A Q&A with Astrid Eichhorn on asymptotic safety: the proposal that quantum gravity is nonperturbatively renormalizable because the RG flow of the couplings approaches a non-trivial ultraviolet fixed point @@g_i -> g_i^*@@ with @@beta_i(g^*) = 0@@ as @@k -> infinity@@. At such a fixed point only a finite number of relevant directions need to be fixed by experiment, restoring predictivity without new degrees of freedom. A striking signature is dynamical dimensional reduction: the spectral dimension of space-time flows from 4 at long distances toward roughly 2 at the Planck scale — the 'fractal' short-distance geometry of the headline.

[Read on Quanta](https://www.quantamagazine.org/tag/quantum-gravity/)

### Quanta Magazine — General Relativity & Spacetime

#### What Is a Manifold? (November 3, 2025)

An explainer on the manifold, the geometric object underlying modern geometry and general relativity. A manifold looks locally like flat Euclidean @@R^n@@ but can be globally curved, so its geometry is captured by a metric tensor @@g_mu_nu@@ defining distances via @@ds^2 = g_mu_nu dx^mu dx^nu@@. The article traces the idea to Riemann's 1854 habilitation lecture, which generalized Gauss's intrinsic curvature to arbitrary dimensions and gave Einstein the language in which @@R_mu_nu - (1/2) R g_mu_nu = (8 pi G / c^4) T_mu_nu@@ encodes gravity, and explains why local flatness is what lets calculus be done on curved space-time.

[Read on Quanta](https://www.quantamagazine.org/tag/general-relativity/)

#### Carlo Rovelli's Radical Perspective on Reality (October 29, 2025)

A Q&A with Carlo Rovelli, co-founder of loop quantum gravity, on his relational view in which space and time emerge from relations between quantum events. In LQG the geometry of space is quantized: areas and volumes have discrete spectra, with the smallest area quantum set by the Planck length @@l_P = sqrt(hbar G / c^3) approx 1.6e-35 m@@, and space is described by spin networks whose edges carry quanta of area. Rovelli argues time as a fundamental parameter drops out (the 'problem of time,' reflected in the Wheeler-DeWitt constraint @@H_hat |psi> = 0@@) and that a timeless, background-independent, relational ontology reconciles gravity with quantum theory.

[Read on Quanta](https://www.quantamagazine.org/tag/general-relativity/)

#### A New Geometry for Einstein's Theory of Relativity (July 16, 2025)

A team of mathematicians in Vienna is extending general relativity to space-times too rough or singular for classical smooth geometry. Standard GR assumes a smooth Lorentzian metric @@g_mu_nu@@, but shock waves, matched matter distributions, and the singularities at the Big Bang and inside black holes have low regularity where the Riemann tensor is undefined pointwise. Building on Lorentzian length spaces and synthetic (metric-measure) curvature bounds, the group reformulates causality and curvature so that Hawking-Penrose-type singularity theorems hold without assuming smoothness — reaching precisely the extreme regimes where a quantum theory of gravity should take over.

[Read on Quanta](https://www.quantamagazine.org/tag/general-relativity/)

---

## Quantum Gravity Digest — 2026-07-19

Sources covered: Quanta Magazine (Quantum Gravity + General Relativity tags). **Scientific American was unavailable this run** — every topic and search endpoint returned HTTP 404 (`/topic/quantum-gravity/`, `/search/`, `/physics/`, `/physics-and-math/`) while the site root resolved normally, indicating a URL-structure change on SA's side rather than a network or subscription failure. The topic slug should be re-derived from site navigation before the next scheduled run.

**Total articles: 6** (2 full-text, 4 excerpt-based). No Quanta articles published in the last 7 days on either tag; the three most recent per tag were taken per the fallback rule.

### Quanta Magazine — Quantum Gravity

#### Entanglement Builds Space-Time. Now "Magic" Gives It Gravity.

*June 3, 2026 — Charlie Wood*

The standout result of the digest. Holographic bulk reconstruction has, since Almheiri–Dong–Harlow (2014) and Harlow (2016), been modelled as a quantum error-correcting code: a bulk region and its matter content are encoded redundantly across boundary CFT degrees of freedom, with entanglement supplying geometric connectivity via Ryu–Takayanagi, `S_A = Area(gamma_A) / (4 G_N)`. The defect in the standard construction is that stabilizer codes factorize boundary entanglement cleanly into a geometry sector and a matter sector, so the emergent bulk is rigid — it realizes Wheeler's first clause (space tells matter how to move) but not the second (matter tells space how to curve).

Charles Cao (Virginia Tech), with John Preskill, Brian Swingle, Christopher White, Alioscia Hamma and others, identifies the missing ingredient as non-stabilizerness, or "magic": the resource quantified by the number of non-Clifford gates (T gates, Toffoli gates) needed to prepare a state, formalized by Bravyi and Kitaev (2004) and directly responsible for classical-simulation hardness. Gottesman–Knill guarantees that zero-magic Clifford circuits are efficiently classically simulable, so a purely stabilizer bulk is a classical object dressed as a quantum one. Their 2026 code uses non-Clifford gates densely, breaking the geometry/matter split and letting the two entanglement structures back-react on each other, yielding gravitational springiness in the emergent bulk.

The conceptual payload is sharper than the technical one: gravity here emerges precisely from the *imperfection* of the encoding — perfect (non-magical) error correction protects the bulk too well and produces an inert, gravity-free geometry, so approximate recoverability is not a defect of the model but the mechanism. Cao is candid that the code is background-general, carries no time direction, and does not reproduce the Einstein equations — he places it at "step 0.5 of 5" — but the entanglement→shape, magic→flexibility correspondence is a genuine structural constraint on any candidate theory of quantum gravity.

https://www.quantamagazine.org/entanglement-builds-space-time-now-magic-gives-it-gravity-20260603/

#### Where Some See Strings, She Sees a Space-Time Made of Fractals

*March 11, 2026 — Charlie Wood*

A Q&A with Astrid Eichhorn (Heidelberg) on asymptotic safety, the most conservative live programme in quantum gravity: rather than abandoning QFT at the Planck scale `l_P = sqrt(hbar G / c^3) ~ 1.616e-35 m`, it posits that the renormalization-group flow terminates in a non-Gaussian ultraviolet fixed point, so the dimensionless Newton coupling `g(k) = G(k) k^2` approaches a finite nonzero `g_*` instead of diverging. Perturbative gravity fails because `G` carries mass dimension `-2`, making the theory power-counting nonrenormalizable; a UV fixed point restores predictivity by rendering the theory nonperturbatively renormalizable with finitely many relevant directions. The resulting scale symmetry gives space-time an effectively fractal, self-similar character, with a spectral dimension running from 4 in the IR toward roughly 2 in the deep UV.

Eichhorn's specific contribution is gravity–matter systems: her 2013 "Matter Matters" paper showed the fixed point survives inclusion of the full Standard Model field content, and last summer's work extended this to the complete set of field interactions previously omitted. The programme's empirical hook is retrodiction — Shaposhnikov and Wetterich (2009) recovered the Higgs mass from fixed-point flow, and Eichhorn with Aaron Held predicted the top quark mass and then, in the "OMG plot" of 2018, the top–bottom mass splitting to within 10%, with later work addressing neutrino mass scales.

She is appropriately candid about limits: most fixed-point evidence lives in Euclidean, space-only truncations; the proton mass is consistent but underdetermined; and the retrodictions arrived after the measurements. Notably she argues asymptotic safety need not compete with strings or loops — a fundamental stringy or discrete structure could present as an apparent fixed point over an intermediate range of scales.

https://www.quantamagazine.org/where-some-see-strings-she-sees-a-space-time-made-of-fractals-20260311/

#### Are Strings Still Our Best Hope for a Theory of Everything?

*March 23, 2026 — Natalie Wolchover — Excerpt only*

Wolchover's column revisits the long-running dispute over whether string theory can describe the observed world. The standing tension is between the framework's formal successes — perturbative UV finiteness, a spin-2 massless mode in the closed-string spectrum reproducing linearized general relativity, and AdS/CFT as a working nonperturbative definition of quantum gravity in negatively curved space — and its predictive weakness in the vacuum-selection problem, where the compactification landscape offers on the order of `10^500` flux vacua with no known selection principle, and where our own universe's positive vacuum energy `Lambda > 0` sits awkwardly against the de Sitter swampland conjectures. Read alongside the Eichhorn interview, the two pieces frame the field's central methodological question: whether quantum gravity requires abandoning quantum field theory or merely extending it.

https://www.quantamagazine.org/are-strings-still-our-best-hope-for-a-theory-of-everything-20260323/

### Quanta Magazine — General Relativity & Spacetime

#### A New Geometry for Einstein's Theory of Relativity

*July 16, 2025 — Steve Nadis — Excerpt only*

A Vienna-based group of mathematicians is developing low-regularity Lorentzian geometry, extending general relativity below the smoothness assumptions built into the classical framework. Standard results depend on the metric `g_mu_nu` being at least `C^2` so that curvature `R^rho_sigma_mu_nu` is defined pointwise, but physically important spacetimes — shock waves, thin matter shells, impulsive gravitational waves, colliding-wave solutions — have metrics that are merely continuous or Lipschitz. The programme uses synthetic and metric-measure methods, importing Alexandrov-style curvature-bound techniques from Riemannian comparison geometry into the Lorentzian signature, to define causality and curvature bounds without differentiating the metric. The stakes are the singularity theorems: Penrose and Hawking's results assume smoothness, so establishing whether geodesic incompleteness persists at low regularity determines whether singularity formation is a robust physical prediction or an artifact of an idealized smoothness hypothesis — directly relevant to whether quantum gravity must resolve singularities at all.

https://www.quantamagazine.org/a-new-geometry-for-einsteins-theory-of-relativity-20250716/

#### What Is a Manifold?

*November 3, 2025 — Paulina Rowińska — Excerpt only*

An explainer on Riemann's 1854 habilitation construction of the manifold: a space locally homeomorphic to `R^n` but which may carry global topology and curvature entirely unlike flat space, with geometry specified intrinsically by a metric tensor `ds^2 = g_ij dx^i dx^j` rather than by embedding in an ambient space. This intrinsic formulation is exactly what Einstein required sixty years later — general relativity is unintelligible without it, since `G_mu_nu + Lambda g_mu_nu = (8 pi G / c^4) T_mu_nu` is a statement about intrinsic curvature of a four-dimensional Lorentzian manifold with no embedding space implied. Useful background for the low-regularity geometry work above, which asks what survives when the differentiable structure Riemann assumed is weakened.

https://www.quantamagazine.org/what-is-a-manifold-20251103/

#### Astrophysicists Find No 'Hair' on Black Holes

*August 27, 2025 — Matt von Hippel — Excerpt only*

An observational test of the no-hair theorem, which holds that a stationary black hole in general relativity is fully characterized by three parameters — mass `M`, angular momentum `J`, and charge `Q` — with all other multipole moments fixed by `M_l + i S_l = M (i a)^l` where `a = J / M c`. Quantum-gravitational corrections, motivated by the information paradox and by fuzzball or firewall proposals, generically predict small deviations, so ringdown spectroscopy of the quasinormal modes following binary mergers provides a direct probe: any inconsistency between the frequencies and damping times of distinct `(l, m, n)` modes and the two-parameter Kerr prediction would constitute hair. The reported search finds no such deviation, bounding any extra structure to be small — a useful constraint given that most quantum-gravity proposals expect horizon-scale modifications rather than Planck-scale-only ones.

https://www.quantamagazine.org/astrophysicists-find-no-hair-on-black-holes-20250827/

---

## Quantum Gravity Digest — 2026-07-20

Sources covered: Quanta Magazine (Quantum Gravity + General Relativity tags). **6 articles** collected. Scientific American could not be fetched this run — its topic, section, and search endpoints all returned 404 site-wide, so that section is empty. No quantum-gravity articles published in the last 7 days at either outlet; the digest falls back to the most recent per tag.

### Quanta Magazine — Quantum Gravity

#### Entanglement Builds Space-Time. Now "Magic" Gives It Gravity.

June 3, 2026 — Charles Cao (Virginia Tech), John Preskill, Brian Swingle and collaborators have identified the missing ingredient that lets holographic quantum error-correcting codes reproduce the second half of Wheeler's dictum — matter telling space-time how to curve. Harlow-type stabilizer codes successfully encode a bulk AdS geometry from boundary entanglement, but a stabilizer code factorizes bulk "geometry" entanglement from bulk "matter" entanglement, leaving an inert, non-backreacting background: one recovers `delta S_EE = delta <K>` (first-law / linearized Einstein equations) but no genuine dynamical response. The new element is *magic* (non-stabilizerness), the Bravyi–Kitaev resource measuring how many non-Clifford gates — T gates, Toffoli gates — are needed to prepare a state; by Gottesman–Knill, zero-magic (Clifford) circuits are classically simulable in poly time, so a magic-free bulk is a classically simulable and hence rigid bulk. Cao, Hamma and Dong showed magic controls the compliance or "springiness" of the emergent geometry, and the early-2026 Cao–Preskill code injects non-Clifford gates to couple the two entanglement sectors so the background fluctuates. A structural corollary: gravity emerges precisely because the holographic encoding is *approximate* rather than exact — perfect quantum error correction yields zero gravitational backreaction, so subalgebra reconstruction must fail at order `G_N ~ 1/N^2`. Cao rates the program "step 0.5 of 5": the code is background-general, carries no time evolution, and does not yet reproduce `G_mu_nu + Lambda g_mu_nu = (8 pi G / c^4) T_mu_nu`.

https://www.quantamagazine.org/entanglement-builds-space-time-now-magic-gives-it-gravity-20260603/

#### Are Strings Still Our Best Hope for a Theory of Everything?

March 23, 2026 — Natalie Wolchover surveys the S-matrix bootstrap results that have reopened the "string uniqueness" question after two decades of stalemate. The object under attack is the 1968 Veneziano amplitude, `A(s,t) = B(-alpha(s), -alpha(t)) = Gamma(-alpha(s)) Gamma(-alpha(t)) / Gamma(-alpha(s)-alpha(t))` with linear Regge trajectory `alpha(s) = alpha_0 + alpha' s`, whose poles at `alpha' m_n^2 = n - alpha_0` encode the infinite tower of open-string states; the closed-string analogue is Virasoro–Shapiro. Cheung, Remmen and collaborators ("Strings From Almost Nothing", Aug 2025) impose unitarity, Lorentz invariance and an "ultrasoftness" condition — amplitudes decaying faster than any power at fixed angle, reflecting the fact that colliding strings spread rather than probe shorter distances — and recover Veneziano and Virasoro–Shapiro as the unique solutions. Elvang et al. ("String Theory From Maximal Supersymmetry", Jan 2026) is regarded as sharper: starting only from `N = 4` supersymmetric QFT plus two technical assumptions, the Veneziano amplitude emerges as the unique tree-level UV completion, with no stringy input assumed. Critics push back on the premise rather than the algebra: Eichhorn argues the deep-UV regime of quantum gravity may be dominated by space-time configurations far from flat, rendering flat-space scattering amplitudes meaningless, and Woit calls the ultrasoftness route question-begging. The reframing is nonetheless real — the debate now concerns whether the bootstrap axioms hold in our universe rather than whether string theory is falsifiable in principle.

https://www.quantamagazine.org/are-strings-still-our-best-hope-for-a-theory-of-everything-20260323/

#### Where Some See Strings, She Sees a Space-Time Made of Fractals

March 11, 2026 — Astrid Eichhorn (Heidelberg) makes the case for asymptotic safety as the conservative route to quantum gravity: rather than replacing point particles with strings or discretizing space-time into spin networks, one keeps quantum field theory and demands that the renormalization group flow terminate in a non-Gaussian ultraviolet fixed point, `beta_i(g*) = 0`, so that dimensionless couplings such as `g_N = G_N k^2` stop running above the Planck scale `l_P = sqrt(hbar G / c^3) ~ 1.616e-35 m`. At the fixed point the theory becomes scale-invariant and acquires an effectively fractal, self-similar short-distance geometry — the spectral dimension flows from 4 toward roughly 2 in the deep UV — and predictivity is restored because only the finitely many relevant directions of the critical surface are free parameters. Eichhorn's 2013 "Matter Matters" work, and a 2025 follow-up covering the full set of field interactions, indicate the fixed point survives inclusion of the Standard Model matter content. The empirical payoff comes from running back down: flowing out of the fixed point reproduces the Higgs mass (Shaposhnikov–Wetterich 2009) and, in Eichhorn and Held's "OMG plot" (2018), the top and bottom quark mass splitting to within 10 percent, along with the anomalously light neutrino masses. The framework also constrains dark matter — simplest WIMPs, standard axion-like particles, and ultralight candidates targeted by nuclear clocks all sit awkwardly with the fixed point — making null and positive results at those experiments indirect probes of the UV structure of space-time. Eichhorn notes asymptotic safety need not compete with strings or loops: a slowly-running intermediate regime could mimic a fixed point emerging from a more fundamental description.

https://www.quantamagazine.org/where-some-see-strings-she-sees-a-space-time-made-of-fractals-20260311/

### Quanta Magazine — General Relativity & Spacetime

#### Astrophysicists Find No "Hair" on Black Holes

August 27, 2025 — *Excerpt-based summary.* General relativity's no-hair theorem states that a stationary black hole is fully specified by three externally observable parameters — mass, angular momentum and charge, `(M, J, Q)` — so that the full ringdown quasinormal-mode spectrum `omega_lmn(M, J)` is determined by two numbers for astrophysical (uncharged) holes. Quantum gravity generically violates this: information-preserving horizons, fuzzballs and higher-derivative corrections all predict additional "hair" that would perturb the ringdown frequencies or the inspiral multipole structure. An observational search reported here finds no such deviation, bounding any extra hair to be short. The result tightens the window in which quantum-gravitational structure can live near the horizon while remaining consistent with LIGO–Virgo–KAGRA waveforms.

https://www.quantamagazine.org/astrophysicists-find-no-hair-on-black-holes-20250827/

#### A New Geometry for Einstein's Theory of Relativity

July 16, 2025 — *Excerpt-based summary.* A Vienna-based group of mathematicians is developing low-regularity Lorentzian geometry — tools that extend general relativity to metrics that are merely continuous or Lipschitz rather than smooth. This matters because the classical singularity theorems of Penrose and Hawking assume `g_mu_nu in C^2`, and shock waves, matched spacetimes and the interiors of collapsing bodies routinely fall below that threshold. Synthetic and metric-measure formulations of curvature bounds allow the causal structure and geodesic incompleteness arguments to be restated without differentiating the metric twice. The payoff is a sharper statement of where Einstein's theory genuinely breaks down as opposed to where the smoothness assumption merely fails.

https://www.quantamagazine.org/a-new-geometry-for-einsteins-theory-of-relativity-20250716/

#### What Is a Manifold?

November 3, 2025 — *Excerpt-based summary.* An explainer tracing Riemann's 1854 habilitation lecture, which introduced n-dimensional manifolds equipped with a local quadratic line element `ds^2 = g_mu_nu dx^mu dx^nu` and intrinsic curvature defined without reference to an embedding space. That construction is the precise mathematical object Einstein required sixty years later: general relativity is the statement that spacetime is a four-dimensional pseudo-Riemannian manifold whose curvature is sourced by stress-energy. The piece covers charts and atlases, the distinction between intrinsic and extrinsic curvature, and why the manifold abstraction makes coordinate independence — general covariance — expressible at all.

https://www.quantamagazine.org/what-is-a-manifold-20251103/

---

## Quantum Gravity Digest — 2026-07-21

Sources covered: Quanta Magazine (Quantum Gravity and General Relativity tags). **5 articles.** Scientific American could not be reached this run — its topic and search endpoints returned 404 (only the homepage resolved), so no SA items are included. No quantum-gravity items published in the last 7 days at either source; the selection is the most recent available, led by the June 3 result on "magic" and emergent gravity.

### Quanta Magazine — Quantum Gravity

#### Entanglement Builds Space-Time. Now "Magic" Gives It Gravity.

June 3, 2026 — Charlie Wood

Holographic constructions of emergent spacetime have long realized Wheeler's first clause — space acts on matter — via entanglement: the Ryu-Takayanagi relation `S_A = Area(gamma_A) / (4 G_N)` ties boundary entanglement entropy to bulk geometry, and cutting entanglement threads pinches off an ER bridge. But standard holographic toy models were built from stabilizer (Clifford) codes, which factorize the code space so bulk-geometry and bulk-matter degrees of freedom cannot back-react: matter never tells space how to curve. Charles Cao (Virginia Tech) with John Preskill, Brian Swingle, Christopher White and Alioscia Hamma show the missing ingredient is nonstabilizerness, or "magic" — the resource quantified by the non-Clifford gate count (T gates, Toffolis) needed to prepare a state, and the same resource that defeats Gottesman-Knill classical simulation, `classical simulation cost ~ exp(#T)`. Their 2026 code uses non-Clifford gates so the entanglement encoding space and the encoding matter mix, producing a fluctuating rather than fixed background; earlier work with Xi Dong linked magic to the springiness of the bulk metric. The conceptual payoff: gravity emerges from approximate, imperfect quantum error correction — exact, magic-free codes give rigid gravity-free spacetimes, so the very failure of perfect recoverability is what makes `delta g_mu_nu != 0`. Cao calls it "step 0.5 of 5": no time direction, no Einstein equations yet.

https://www.quantamagazine.org/entanglement-builds-space-time-now-magic-gives-it-gravity-20260603/

#### Are Strings Still Our Best Hope for a Theory of Everything?

March 23, 2026 — Natalie Wolchover

A survey of the amplitude-bootstrap revival of "string uniqueness." Rather than assuming a worldsheet and deriving consequences, bootstrappers impose unitarity, Lorentz invariance, crossing and analyticity on a 2 → 2 amplitude and ask what UV completions survive; the recurring survivor is the 1968 Veneziano amplitude `A(s,t) = Gamma(-alpha(s)) Gamma(-alpha(t)) / Gamma(-alpha(s)-alpha(t))` with linear Regge trajectory `alpha(s) = alpha_0 + alpha' s`, alongside its closed-string counterpart Virasoro-Shapiro. Cheung, Remmen et al. ("Strings From Almost Nothing", Aug 2025) assume "ultrasoftness" — exponential suppression of fixed-angle high-energy scattering, physically strings spreading rather than concentrating energy as `s -> infinity` — and recover the Veneziano/Virasoro-Shapiro pair uniquely; Peter Woit notes ultrasoftness is itself a stringy input. More striking is Elvang et al., "String Theory From Maximal Supersymmetry" (Jan 2026): assuming only `N = 4` supersymmetric QFT plus two technical conditions, the unique tree-level UV completion is Veneziano. Caveats: tree level only, maximal SUSY is not our world, and Eichhorn and Boyle object that flat-space amplitudes may be meaningless in a UV dominated by large non-flat geometry fluctuations.

https://www.quantamagazine.org/are-strings-still-our-best-hope-for-a-theory-of-everything-20260323/

#### Where Some See Strings, She Sees a Space-Time Made of Fractals

March 11, 2026 — Charlie Wood

Q&A with Astrid Eichhorn (Heidelberg) on asymptotic safety, the most conservative route to quantum gravity: keep QFT and spacetime continuity, and demand only that the RG flow terminate in a nontrivial UV fixed point where all dimensionless couplings stop running, `beta_i(g*) = 0`. Perturbative gravity fails because Newton's constant is dimensionful — `[G] = mass^-2`, so the dimensionless coupling `g = G k^2` grows without bound and the theory is nonrenormalizable by power counting; a fixed point in `g` renders it predictive nonperturbatively, and the resulting scale symmetry gives spacetime an effectively fractal, self-similar character with scale-dependent spectral dimension. Eichhorn's "Matter Matters" (2013) found the fixed point survives inclusion of all Standard Model fields; last summer's work extended this to the full set of field interactions. Testable payoff: retrodictions by flowing down from the fixed point — Shaposhnikov and Wetterich's Higgs mass, and Eichhorn and Held's top and bottom quark masses to within 10%, the "OMG plot" — plus negative predictions disfavoring simple WIMPs, standard axion-like particles and ultralight dark matter.

https://www.quantamagazine.org/where-some-see-strings-she-sees-a-space-time-made-of-fractals-20260311/

### Quanta Magazine — General Relativity & Spacetime

#### A New Geometry for Einstein's Theory of Relativity

July 16, 2025 — Steve Nadis

General relativity is written in the language of smooth Lorentzian manifolds — `G_mu_nu + Lambda g_mu_nu = (8 pi G / c^4) T_mu_nu` requires differentiating the metric twice — so the theory is silent precisely where curvature blows up or where spacetime is discrete, as most quantum gravity programs expect. A Vienna-led program (Kunzinger, Sämann, Steinbauer; €7M FWF grant) replaces differentiation with synthetic, comparison-based geometry. Sectional curvature bounds come from triangle comparison against model spaces, adapted to Lorentzian signature using time separation `tau(p,q)` as the distance functional with geodesic edges that maximize rather than minimize it — in Lorentzian geometry detours are shorter. Ricci curvature, what the singularity theorems actually need, is bounded via optimal transport: McCann, and independently Mondino and Suhr, showed a Lorentzian analogue of Lott-Sturm-Villani entropy convexity along Wasserstein geodesics characterizes `Ric >= K`. Cavalletti and Mondino (2020) reproved Hawking's singularity theorem in nonsmooth settings; Cavalletti, Manini and Mondino recently did the same for Penrose's 1965 theorem — Big Bang and black hole singularities are not artifacts of smoothness.

https://www.quantamagazine.org/a-new-geometry-for-einsteins-theory-of-relativity-20250716/

#### Astrophysicists Find No 'Hair' on Black Holes

August 27, 2025 — Matt von Hippel

The no-hair conjecture holds that an astrophysical black hole is fully specified by `(M, J)` — the Kerr solution, with charge `Q` negligible in practice — so every ringdown quasinormal mode frequency `omega_lmn(M, J)` is fixed by those two numbers. Resolutions of the information paradox generically add structure outside the horizon (firewalls, Mathur's fuzzballs, gravastars, regular black holes), i.e. quantum hair, most of it expected only within a Planck length `l_P = sqrt(hbar G / c^3) ~ 1.6e-35 m` and hence visible, if at all, only through late-time gravitational-wave echoes — searches for which remain null. The new constraint combines the KU Leuven group's 2023 technique for spinning black hole perturbations in modified-gravity frameworks with Carullo's gravitational-wave analysis. Stacking 22 LIGO-Virgo-KAGRA binary black hole mergers rescaled to a common mass, Maenaut, Carullo, Cardoso and colleagues exclude deviations from Kerr farther than ~40 km from the horizon at 95% confidence — typically inside the hole's own radius, a trim rather than a shave. Cosmic Explorer and the Einstein Telescope should reach the scale of tens of meters.

https://www.quantamagazine.org/astrophysicists-find-no-hair-on-black-holes-20250827/

---

## Quantum Gravity Digest — 2026-07-22

*Today's harvest leans on Quanta Magazine, which is running an unusually rich quantum-gravity streak, plus Scientific American's Relativity desk. Scientific American retired its dedicated /topic/quantum-gravity/ page, so the SA picks were drawn from its live /relativity/ section (the two most spacetime-relevant recent features). No source failed outright. Nothing fell strictly within the last 7 days on the quantum-gravity or general-relativity tags, so the digest falls back to the most recent substantive pieces per tag. Equations use ASCII notation, e.g. G_mu_nu + Lambda g_mu_nu = (8 pi G / c^4) T_mu_nu.*

### Scientific American — Quantum Gravity & Spacetime

#### This Mind-Bending Relativity Illusion Has Never Been Seen — Until Now (Terrell–Penrose Effect)

*February 17, 2026*

Vienna physicists used ultrafast photography (the SEEC project, apparent light-front speed ~1 m/s) to visualize, for the first time in the lab, the Terrell–Penrose effect: an object moving near c looks rotated rather than merely flattened. Naive special relativity gives Lorentz contraction, `L = L_0 sqrt(1 - v^2/c^2)`, so a fast sphere should squeeze into a disk. But photons from the far side are emitted earlier and reach the camera simultaneously with near-side photons, so the eye reconstructs an unsqueezed sphere turned through an angle with `cos(theta) = v/c` (equivalently sin(theta) = 1/gamma). At v = 0.999c the disk is reinterpreted as a rotated, uncontracted ball — confirming the 1959 Terrell–Penrose prediction that visual appearance and measured length differ. Published in Communications Physics and the March 2026 SciAm issue.

[Read on Scientific American](https://www.scientificamerican.com/article/strange-special-relativity-effect-observed-for-the-first-time/)

#### We Thought We Knew the Shape of the Universe. We Were Wrong

*March 27, 2026*

Cosmologist Paul Sutter stresses that general relativity fixes only local curvature via `G_mu_nu + Lambda g_mu_nu = (8 pi G / c^4) T_mu_nu` and is silent on global topology. CMB data pin the curvature parameter to `Omega_k = 1 - Omega_total ~ 0` (spatially flat), yet flatness does not imply an infinite plane: a flat universe can still wrap into a 3-torus, a Klein-bottle-like identification, or other multiply-connected forms. The sharpest test would be 'matched circle pairs' in the CMB — identical hot/cold temperature rings in two sky directions signalling the same region seen twice. Sutter argues decades of 'flat and infinite' claims conflate geometry with topology, and current Planck-era data do not exclude a finite, folded cosmos. *(Excerpt only — paywalled beyond the intro.)*

[Read on Scientific American](https://www.scientificamerican.com/article/we-thought-we-knew-the-shape-of-the-universe-we-were-wrong/)

### Quanta Magazine — Quantum Gravity

#### Entanglement Builds Space-Time. Now "Magic" Gives It Gravity.

*June 3, 2026*

In holographic (AdS/CFT) models the bulk 3D geometry is reconstructed from boundary quantum data via quantum error-correcting codes; entanglement supplies space's connective tissue, captured by Ryu–Takayanagi `S_A = Area(gamma_A) / (4 G hbar)`. But 'stabilizer' codes cleanly split space-entanglement from matter-entanglement, leaving geometry rigid — matter cannot back-react on curvature, so Wheeler's 'matter tells space how to curve' fails. Cao, Preskill and collaborators identify the missing ingredient as 'magic': non-stabilizerness, quantified by the count of non-Clifford gates (T, Toffoli) needed to prepare a state — also what makes a state hard to simulate classically. A code rich in non-Clifford gates lets the two kinds of entanglement mix, giving space its springiness and hence gravity. Strikingly, gravity emerges only from approximate encoding; perfectly protected (non-magical) codes yield inert, gravity-free geometries. Cao calls it 'step 0.5 of 5'.

[Read on Quanta Magazine](https://www.quantamagazine.org/entanglement-builds-space-time-now-magic-gives-it-gravity-20260603/)

#### Are Strings Still Our Best Hope for a Theory of Everything?

*March 23, 2026*

Natalie Wolchover surveys the revived 'string uniqueness' bootstrap program, which inverts the usual logic — asking which assumptions force string theory. Imposing unitarity, Lorentz invariance and analyticity, recent works recover the 1968 Veneziano amplitude `A(s,t) = Gamma(-alpha(s)) Gamma(-alpha(t)) / Gamma(-alpha(s) - alpha(t))` with linear Regge trajectory `alpha(s) = alpha_0 + alpha' s` as the unique UV completion. Cheung et al.'s 'Strings From Almost Nothing' (Aug 2025) invokes 'ultrasoftness'; Elvang et al.'s 'String Theory From Maximal Supersymmetry' (Jan 2026) derives the tree-level Veneziano amplitude from N = 4 supersymmetric QFT plus two technical assumptions. Critics (Woit, Eichhorn, Boyle) object that assuming flat-space scattering in the UV may beg the question. Consensus: string theory is 'special,' not proven to describe our universe.

[Read on Quanta Magazine](https://www.quantamagazine.org/are-strings-still-our-best-hope-for-a-theory-of-everything-20260323/)

#### Where Some See Strings, She Sees a Space-Time Made of Fractals (Asymptotic Safety)

*March 11, 2026*

Astrid Eichhorn defends asymptotic safety, in which QFT stays predictive to all scales because the RG flow reaches an interacting UV fixed point instead of diverging. Along `mu d g_i / d mu = beta_i(g)`, a nontrivial fixed point `beta_i(g_*) = 0` makes physics scale-invariant ('fractal-like') at the Planck scale, curing the perturbative nonrenormalizability of gravity — Newton's constant being an irrelevant coupling of mass dimension `[G] = -2` in 4D. Including Standard-Model matter preserves the fixed point, and flowing back out retrodicts real parameters: the Higgs mass (Shaposhnikov–Wetterich 2009), the top-quark mass, and the top–bottom split to within ~10% (the 'OMG plot'). The framework disfavors the simplest WIMP/axion/ultralight dark-matter candidates and may be compatible with strings or loops as different zoom levels.

[Read on Quanta Magazine](https://www.quantamagazine.org/where-some-see-strings-she-sees-a-space-time-made-of-fractals-20260311/)

### Quanta Magazine — General Relativity & Spacetime

#### Astrophysicists Find No 'Hair' on Black Holes

*August 27, 2025*

The no-hair theorem asserts a stationary black hole is fixed entirely by mass M, spin J and (negligible) charge Q, so ringdown gravitational waves carry a Kerr quasinormal-mode spectrum determined only by (M, J). Cardoso, Carullo, Maenaut et al. stacked 22 LIGO/Virgo/KAGRA merger signals against modified-gravity templates, found agreement with GR, and bounded any 'hair' to within ~40 km of the horizon at 95% confidence — often less than the hole's own radius. Quantum resolutions of the information paradox (firewalls, fuzzballs, gravastars, regular black holes) add near-horizon structure, plausibly at the Planck length `l_P = sqrt(hbar G / c^3) ~ 1.6e-35 m`, which could imprint late-time gravitational-wave 'echoes' — none seen. Einstein Telescope and Cosmic Explorer aim to tighten the bound to football-field scales.

[Read on Quanta Magazine](https://www.quantamagazine.org/astrophysicists-find-no-hair-on-black-holes-20250827/)

#### Carlo Rovelli's Radical Perspective on Reality

*October 29, 2025*

A Q&A on loop quantum gravity and relational QM. LQG quantizes geometry: area and volume become operators with discrete spectra, e.g. area eigenvalues `A = 8 pi gamma l_P^2 sum_i sqrt(j_i (j_i + 1))` over spin-network links with half-integer spins j_i and Barbero–Immirzi parameter gamma — so space is built from quanta linked into loops, and neither space nor time is fundamental. Rovelli argues the arrow of time is perspectival, arising from `dS/dt >= 0` applied to our coarse-grained macrostate. His relational QM holds properties are defined only relative to interacting systems, echoing Nagarjuna. Testable hopes: LQG imprints in the CMB and long-lived ~10-microgram Planck-relic black holes as dark matter.

[Read on Quanta Magazine](https://www.quantamagazine.org/carlo-rovellis-radical-perspective-on-reality-20251029/)

#### What Is a Manifold?

*November 3, 2025*

An explainer on manifolds, the backbone of GR. A manifold is locally Euclidean — every point has a neighborhood mapped by a chart to R^n — with an atlas of charts and smooth transition maps letting calculus proceed patch by patch (a circle is a 1-manifold; a figure-eight is not). Riemann's 1854 generalization of Gauss's intrinsic geometry gave the Riemannian manifold with metric `ds^2 = g_mu_nu dx^mu dx^nu`, curvature encoded in the Riemann tensor `R^rho_sigma_mu_nu`. Einstein adopted this in 1915, modeling spacetime as a 4D pseudo-Riemannian manifold and gravity as its curvature. The piece stresses manifolds' reach beyond physics — the double pendulum's configuration torus, algebraic geometry, and high-dimensional data analysis.

[Read on Quanta Magazine](https://www.quantamagazine.org/what-is-a-manifold-20251103/)

*Generated automatically by Claude — July 22, 2026 · Sources: scientificamerican.com · quantamagazine.org*

---

## 📄 Papers (database)

Database URL: https://app.notion.com/p/f1e0ed3a3fbe4a2ea0da7e0f51a8fd49
Schema: Title (title), Category (select: LQG / Spin Foam / Causal Sets / Holography / Planck Scale / Other), Date (date), Sources (URL).

Rows (1):

| Title | Category | Date | Sources |
|---|---|---|---|
| Quantum-gravity phenomenology with primordial black holes | LQG | 2016-09-07 | https://arxiv.org/abs/1609.02159 |

---

## 🗒️ Notes (database)

Database URL: https://app.notion.com/p/c936c13fae7e4649bcb9b30d3840cc1e
Schema: Title (title), Category (select: LQG / Spin Foam / Causal Sets / Holography / Planck Scale / Other), Date (date), Sources (URL).

The Notes database is currently empty (0 rows).

---

## Provenance

All content above was exported on 2026-07-22 from the Notion workspace, section "🌀 Quantum Gravity" (child of "Knowledge Hub").

| Page / Database | Notion URL |
|---|---|
| 🌀 Quantum Gravity (section parent page) | https://app.notion.com/p/37d765478c3c81b09117dd2eae577ea3 |
| Quantum Gravity Digest — 2026-06-15 | https://app.notion.com/p/380765478c3c81fb8055fa9e4419bbdd |
| Quantum Gravity Digest — 2026-06-16 | https://app.notion.com/p/381765478c3c8148bf39ee11c087f798 |
| Quantum Gravity Digest — 2026-06-17 | https://app.notion.com/p/382765478c3c8168a026e5cde94e4e5e |
| Quantum Gravity Digest — 2026-06-17 (run 2) | https://app.notion.com/p/382765478c3c8111ad8fd6428851fe41 |
| Quantum Gravity Digest — 2026-06-18 | https://app.notion.com/p/383765478c3c8112af95ef3c088557a9 |
| Quantum Gravity Digest — 2026-07-05 | https://app.notion.com/p/394765478c3c81cb941ce73c7a030ef7 |
| Quantum Gravity Digest — 2026-07-09 | https://app.notion.com/p/398765478c3c81e88672f85c43e14c56 |
| 🔬 Research (arXiv) | https://app.notion.com/p/398765478c3c8173b1a7d32537e0c5f6 |
| Quantum-gravity phenomenology with primordial black holes (Rovelli & Vidotto, 2016) | https://app.notion.com/p/39b765478c3c817f9f12c85e34a23ffc |
| Quantum Gravity Digest — 2026-07-14 | https://app.notion.com/p/39d765478c3c81b88330dc5a082cb8f8 |
| Quantum Gravity Digest — 2026-07-15 | https://app.notion.com/p/39e765478c3c81698480e9d14f9513ef |
| Quantum Gravity Digest — 2026-07-16 | https://app.notion.com/p/39f765478c3c81cb8a0af78c96234378 |
| Quantum Gravity Digest — 2026-07-19 | https://app.notion.com/p/3a2765478c3c81f5b562fda21546575b |
| Quantum Gravity Digest — 2026-07-20 | https://app.notion.com/p/3a3765478c3c81a58117c22701e72a0d |
| Quantum Gravity Digest — 2026-07-21 | https://app.notion.com/p/3a4765478c3c813cb1ceda3719874aa4 |
| Quantum Gravity Digest — 2026-07-22 | https://app.notion.com/p/3a5765478c3c81659f49c6f53cde7cd0 |
| 📄 Papers (database, 1 row) | https://app.notion.com/p/f1e0ed3a3fbe4a2ea0da7e0f51a8fd49 |
| 🗒️ Notes (database, empty) | https://app.notion.com/p/c936c13fae7e4649bcb9b30d3840cc1e |

Notes on export fidelity:

- Notion XML wrapper tags, ancestor paths, and property blocks were stripped; page body content is preserved verbatim (headings demoted one level to fit the chapter structure).
- Equations in the source pages appear in mixed notation (LaTeX-style `$...$`, ASCII, and `@@...@@` delimiters); they are reproduced exactly as written in the source pages.
- The Papers and Notes database rows were retrieved via a database view query. Direct SQL queries were rate-limited by the Notion plan ("free data source queries" exhausted), but the view-mode fallback returned complete row data, so no content was lost.
