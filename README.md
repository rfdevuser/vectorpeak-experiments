# VectorPeak Experiments

Standalone benchmark scripts for VectorPeak products.
Each script runs with no API key and minimal or no dependencies.

---

| Benchmark | Script | Product | Dependencies |
|---|---|---|---|
| [Negation Trap](README_structuraldb.md) | `run_benchmark.py` | StructuralDB | `sentence-transformers numpy` |
| [Canonical Vision Operator](README_cvo.md) | `run_cvo_benchmark.py` | VisionCore | `numpy scipy` |
| [Vulnerability Percolation](README_breachguard.md) | `run_breachguard_benchmark.py` | BreachGuard | none |
| [Certified Scenario Engine](README_clearseed.md) | `run_clearseed_benchmark.py` | ClearSeed | none |
| [Generalisation Risk Intelligence](README_modelguard.md) | `run_modelguard_benchmark.py` | ModelGuard | none |
| [Joint AV Pipeline Robustness](README_joint_av.md) | `run_joint_av_benchmark.py` | VisionCore + AdelicDrive | `numpy scipy` |
| [Double Descent Certificate](README_doubledescentguard.md) | `run_doubledescentguard_benchmark.py` | DoubleDescentGuard | none |
| [Adelic Neuromorphic Engine](README_neurocore.md) | `run_neurocore_benchmark.py` | NeuroCore | none |
| [Interbank Contagion Certificate](README_contagionguard.md) | `run_contagionguard_benchmark.py` | ContagionGuard | `numpy` |
| [Alternative Credit Risk](README_flowscore.md) | `run_flowscore_benchmark.py` | FlowScore | none |
| [NPC Memory Kernel](README_memgraph.md) | `run_memgraph_benchmark.py` | MemGraph | none |
| [NPC Dialogue Engine](README_dialoggraph.md) | `run_dialoggraph_benchmark.py` | DialogGraph | none |
| [Quest Chain Engine](README_questgraph.md) | `run_questgraph_benchmark.py` | QuestGraph | none |

---

## Quick run

```bash
git clone https://github.com/rfdevuser/vectorpeak-experiments
cd vectorpeak-experiments

# StructuralDB — negation trap in vector state management
pip install sentence-transformers numpy
python run_benchmark.py

# VisionCore — illumination invariance + adversarial stability
pip install numpy scipy
python run_cvo_benchmark.py

# BreachGuard — CVSS vs percolation rank mismatch
python run_breachguard_benchmark.py

# ClearSeed — deterministic replay vs system PRNG
python run_clearseed_benchmark.py

# ModelGuard — Curie distance D = p/n generalisation risk audit
python run_modelguard_benchmark.py

# VisionCore + AdelicDrive — joint AV pipeline adversarial robustness
pip install numpy scipy
python run_joint_av_benchmark.py

# DoubleDescentGuard — exact F_gen certificate (pure Python, no deps)
python run_doubledescentguard_benchmark.py

# ContagionGuard — interbank spectral stability certificate
pip install numpy
python run_contagionguard_benchmark.py

# FlowScore — alternative credit risk from transaction variance
python run_flowscore_benchmark.py

# MemGraph — p-adic ultrametric NPC memory tree
python run_memgraph_benchmark.py

# DialogGraph — p-adic proximity NPC dialogue engine
python run_dialoggraph_benchmark.py

# QuestGraph — 2-adic digit quest chain engine
python run_questgraph_benchmark.py
```

---

## What each benchmark demonstrates

**StructuralDB** — cosine similarity assigns high scores to polar-opposite
decisions for the same entity. StructuralDB blocks the contradiction at
write time: zero tokens, zero false positives, microseconds.

**VisionCore** — the Canonical Vision Operator (CVO) front-end is exactly
invariant to multiplicative brightness changes and structurally stable under
L∞ adversarial perturbations. Zero learned weights. Closed-form constants only.

**BreachGuard** — the highest-CVSS vulnerability is not the one whose
exploitation triggers a network cascade. Γ₄₃ (Molloy-Reed percolation)
ranks patches by cascade threshold improvement. On a 20-node corporate
network, the Γ₄₃-ranked patch delivers 8.4× more cascade resilience than
the CVSS-ranked patch using the same single remediation budget.

**ClearSeed** — regulatory capital scenario generation (FRTB, CCAR, ICAAP)
using a Legendre-symbol PRG. The integer seed is the complete audit key —
any regulator can replay the exact scenario matrix byte-for-byte. Five-check
equidistribution certificate proved unconditionally, not empirically.

**ModelGuard** — the Curie distance D = p/n flags deployments that validation
loss misses. At D ≈ 1, Marchenko-Pastur generalisation variance diverges
regardless of val loss. Two models with identical val_loss and identical σ²
can differ by 40× in generalisation variance at deployment.

**DoubleDescentGuard** — F_gen(ρ) = exp(−2π/ρ²) gives the exact generalisation
fraction at any effective capacity ratio ρ = p_eff/n_eff. At the double descent
peak (ρ=1): F_gen = 0.19% — 99.81% of learned capacity is trapped. Val loss is
blind to this. Same data, 4× more parameters: F_gen jumps from 0.34% to 70.1%.
Accounts for regularisation strength and SNR, which D = p/n (ModelGuard) cannot.

**ContagionGuard** — ρ(W) = spectral radius of the normalised bilateral exposure
matrix W certifies the exact contagion threshold (γ_c = 1/ρ). The Perron vector
of W ranks systemic importance independent of balance-sheet size. In the Eurozone
stress preset, ES1 (200B assets, rank #5 by size) is Perron rank #1 — the structural
amplifier. Injecting 2.5B into ES1 crosses ρ<1; the same capital into FR1 (600B,
rank #1 by size) leaves the network CRITICAL. Zero fitted parameters.

**FlowScore** — D = σ_ref/σ_tx (Curie distance from transaction variance baseline).
FlowScore F = 100·D² and P(default|T) = 1−exp(−T·k₀·exp(−α·D²)) [Kramers escape
rate]. India has ~400M UPI users with no credit history — CIBIL rejects them. A
Thin-File UPI borrower (CIBIL=0, rejected) has FlowScore 60.9 and PD_90=0.210%;
a Near Default borrower (CIBIL=660, approved) has FlowScore 1.6 and PD_90=2.229%.
CSD flag AC=1−D²>0.75 fires 1 month before the NEAR-DEFAULT tier is crossed. 52×
PD amplification from D=1.0 to D=0.1. Two population constants; zero per-borrower
fitting. Pure Python, no dependencies.

**VisionCore + AdelicDrive (joint)** — camera-noise attacks have a structural
ceiling. LoG linearity keeps coarse edge maps stable (σ=2: IoU 0.916, σ=4: IoU 0.833
under L∞ ε=4/255). AdelicDrive's categorical ℤ₂ rule flags then cap ACCELERATE
at ADS 0.693 vs BRAKE 0.772 — a gap of 0.078 that no continuous perturbation
can bridge. Three independent mathematical barriers; none requires training.

**MemGraph** — p-adic valuation assigns each NPC memory to a permanence shell:
v_p(key)=0 (lore, permanent) through v_p(key)=3 (transient, ephemeral). Shell
ordering is a structural property of the valuation — no sort pass, no configuration.
Token budget is consumed greedily in shell order: lore fills first, transient last.
The guardrail chain is Hensel-exact: an action is valid iff state ≡ prereq (mod p^k).
The valid state set is a clopen ball in Z_p — no boundary, no bypass possible.

**DialogGraph** — p-adic proximity routes topic selection to nearest context:
d_p(context, key) = p^{-v_p(context-key)}. Same coset = zero distance = highest
priority. Shell ordering and congruence gating (state ≡ prereq mod p^k) together
enforce that lore always precedes ephemeral chatter in the budget, and that gated
topics are blocked with zero false positives. Demonstrated on NPC Kira at two
quest states: prereq=4 topics unavailable at state=0, available at state=4.

**QuestGraph** — 2-adic digit state machine where bits 0-7 track main-quest
progress, bit 8 is the scholar branch flag, bit 9 is the warrior branch flag,
and bit 10 is a side-quest flag. Fork: scholar and warrior share prereq=16 mod 32 —
both simultaneously available at state=16. Merge: breach_vault prereq=16 mod 256
catches scholar state=272 (272 mod 256=16) and warrior state=528 (528 mod 256=16)
with one congruence check. Side-quest orthogonality: delta=1024, 1024 mod 256=0 —
main-quest prereqs structurally unaffected.

---

For API access, integration docs, and pricing:
**[vallikat@vectorpeaktech.com](mailto:vallikat@vectorpeaktech.com)**
