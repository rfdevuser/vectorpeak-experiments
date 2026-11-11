# NeuroCore — Adelic Neuromorphic Inference Engine

**NS-030 four-layer SNN architecture. Zero free parameters. Every constant derived.**

The architecture is not trained. It is derived — from a single axiom system (VS-259)
that forces every timing constant, oscillation band count, sleep fraction, and energy
bound from first principles.

---

## Quickstart

```bash
git clone https://github.com/rfdevuser/vectorpeak-experiments
cd vectorpeak-experiments
python run_neurocore_benchmark.py
```

Pure Python, zero dependencies.

---

## The Four Claims

**1. Zero free parameters.**
Every constant in the architecture is derived. No search, no fitting, no calibration.

**2. Neural oscillations from χ = 1/12.**
The brain's 12 oscillatory bands (delta → high-gamma) emerge from the modular Euler
characteristic χ = 1/12. The architecture predicts 12 bands with p=2 octave spacing.
Sleep fraction = 1/3 is a consequence of the same structure.

**3. Thermodynamic energy advantage.**
Transformer attention erases O(n²·d·b) bits per inference at the Landauer limit.
The CANON+ neuromorphic architecture erases O(n·b) bits; p-adic routing is
thermodynamically free. Efficiency ratio: 1/(n·d).

**4. Hierarchical spike precision.**
Depth d fires when |V − V_eq| > 2^(−d). Shallow depths encode coarse structure;
deep depths encode fine structure. The cascade is determined by the input, not by
learned weights.

---

## Phase 1 — All Constants Derived

| Constant | Value | Derivation | Source |
|----------|-------|-----------|--------|
| τ_∞ | 0.15915494 | 1/(2π) | Archimedean timescale |
| p | 2 | forced prime | Integrality of log(p)/log(2) |
| refractory | 0.11031780 | τ_∞ · ln(2) | Inter-depth interval |
| χ | 1/12 | 0.08333333 | Modular Euler characteristic |
| N_bands | 12 | χ⁻¹ | Oscillation modes — not curve-fit |
| sleep | 1/3 | 12-band structure | Consolidation fraction |
| E_Landauer | 2.87×10⁻²¹ J | k_B T ln(2) | Min energy/bit at 300K |

**Comparison — free parameters in common SNN frameworks:**

| Framework | Free parameters |
|-----------|----------------|
| Brian2 (LIF) | 8–12 |
| NEST (AdEx) | 10–15 |
| Intel Loihi 2 | 7+ |
| **NS-030 (NeuroCore)** | **0** |

---

## Phase 2 — 12 Neural Oscillation Bands

The 12 bands emerge from χ = 1/12. Each band is 2× the frequency of the previous
(p=2 is the forced prime). This is not a fit to EEG data.

| Depth | Band | p-adic weight | Brain freq | Role |
|-------|------|--------------|------------|------|
| 0 | delta | 1.000000 | 0.5–4 Hz | Sleep, memory consolidation |
| 1 | theta-low | 0.500000 | 4–6 Hz | Hippocampal navigation |
| 2 | theta-high | 0.250000 | 6–8 Hz | Working memory encoding |
| 3 | alpha-low | 0.125000 | 8–10 Hz | Idle/inhibitory, visual cortex |
| 4 | alpha-high | 0.062500 | 10–12 Hz | Attention gating |
| 5 | beta-low | 0.031250 | 12–16 Hz | Sensorimotor integration |
| 6 | beta-mid | 0.015625 | 16–20 Hz | Motor preparation |
| 7 | beta-high | 0.007812 | 20–30 Hz | Decision-making |
| 8 | gamma-low | 0.003906 | 30–50 Hz | Feature binding |
| 9 | gamma-mid | 0.001953 | 50–80 Hz | Cross-area synchronisation |
| 10 | gamma-high | 0.000977 | 80–120 Hz | Local cortical computation |
| 11 | high-gamma | 0.000488 | 120–200 Hz | Action potentials |

**Sleep = 1/3: derived, not observed.**
With 12 bands and p=2 spacing, the consolidation window that completes one full
depth cycle is τ_∞ · 4. The active window is τ_∞ · 2. Sleep/total = 1/3.
Humans sleep ~8h in 24h = 1/3 of their lives. This is a consequence, not a fit.

---

## Phase 3 — Thermodynamic Energy

```
Transformer attention: O(n²·d·b) erasures at Landauer limit
CANON+ neuromorphic:  O(n·b)   archimedean  +  0 p-adic
Efficiency ratio: 1/(n·d)
```

| Context n | Transformer (Loihi 2) | NeuroCore (Loihi 2) | Speedup |
|-----------|----------------------|---------------------|---------|
| 128 | 33.55 nJ | 4.10 pJ | 8,192× |
| 1,024 | 2.15 µJ | 32.77 pJ | 65,536× |
| 4,096 | 34.36 µJ | 131.07 pJ | **262,144×** |
| 32,768 | 2.20 mJ | 1.05 nJ | 2,097,152× |

**Why p-adic routing is thermodynamically free:**
p-adic valuation v_p(n*) is structural classification — it determines which depth
a spike fires at without erasing information. Only erasure costs Landauer energy.
The adelic architecture separates erasure (ℝ channel) from routing (ℤ_p channel).

---

## The Four Layers

```
L1 — Adelic Encoding
     Input spike encoder: maps (x_∞, v_p(n*)) to depth-tagged spikes
     p=2 is forced — not chosen

L2 — Self-Dual Inference
     Fixed synaptic weight array (canonical kernel — not learned)
     Zero training. ρ_can fixed by self-dual condition.

L3 — Binding & Consolidation
     Dendritic multiplier (adelic product rule) + 1/3 cycle sleep
     v_p(n₁·n₂) = v_p(n₁) + v_p(n₂) — multiplicative integration

L4 — Causal Structure
     Recurrent spike routing with depth ordering
     Causal task graph as depth-ordered routing table
```

---

## Hardware Targets

The derived parameters map directly to neuromorphic hardware:

- **Intel Loihi 2** — 13 cores per neurocore (one per depth level), 2¹³ compartments
- **IBM NorthPole** — 12 SRAM tiles (one per oscillation band), depth cascade in on-chip router
- **Generic SNN** — standard LIF compartments with τ_ref = refractory = 0.1103s

---

## Running the Benchmark

```bash
python run_neurocore_benchmark.py
```

Expected output:
```
Phase 1: 8 derived constants — 0 free parameters vs 8–15 in standard frameworks
Phase 2: 12 bands from χ=1/12 — sleep=1/3 derived
Phase 3: n=4096 → 262,144× energy advantage at Loihi 2 baseline
Phase 4: depth-threshold cascade for input (x_∞=0.75, n*=24)
```

---

## Get the Full Product

For API access, integration docs, and pricing:
**[vallikat@vectorpeaktech.com](mailto:vallikat@vectorpeaktech.com)**
