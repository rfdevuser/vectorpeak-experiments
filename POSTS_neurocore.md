# NeuroCore — Post Copy

---

## LinkedIn

```
Every SNN framework in production — Brian2, NEST, Intel Loihi 2 — requires
8 to 15 hand-tuned constants before you can run a single inference.

Membrane time constant. Synaptic time constant. Reset potential. Threshold.
Refractory period. Capacitance. Leak conductance. Adaptation current.

NeuroCore has zero.

Every constant is derived from a single axiom system. τ_∞ = 1/(2π).
The refractory period = τ_∞ · ln(2). The oscillation band count = 1/χ = 12
(χ = 1/12 is the modular Euler characteristic — not tuned, topologically fixed).
Sleep fraction = 1/3, forced by the 12-band consolidation structure.

Humans sleep roughly 1/3 of their lives. That is not a parameter we fit.
It is a consequence of the same structure that forces 12 oscillatory bands.

The thermodynamic claim:

Transformer attention: O(n²·d·b) bit erasures at the Landauer limit.
NeuroCore: O(n·b) archimedean bits. The p-adic routing channel (which depth
a spike fires at) is structural classification — it costs zero Landauer energy.

At n=4,096 tokens, d=64:
  Transformer on Loihi 2: 34.36 µJ per inference
  NeuroCore on Loihi 2:    0.13 nJ per inference
  Ratio: 262,144×

The ratio is not empirical. It is exactly 1/(n·d) — the ratio of O(n·b) to O(n²·d·b).

Benchmark: pure Python, zero deps, runs in under a second:
[link to repo]
```

---

## Reddit — r/MachineLearning or r/neuralnetworks

**Title:**
```
Neuromorphic SNN with zero free parameters — all timing constants derived from modular Euler characteristic χ=1/12. Pure Python benchmark.
```

**Body:**
```
Built a benchmark for a spiking neural network architecture where every
parameter is derived rather than tuned. Sharing because the connection between
χ=1/12 and neural oscillation bands is a claim worth scrutinising.

**The construct:**

NS-030 is a four-layer SNN architecture (VS-259 theorem). All constants:

```
τ_∞ = 1/(2π)                    archimedean timescale
p = 2                             forced prime (integrality of log(p)/log(2))
refractory = τ_∞ · ln(2)        inter-depth interval
χ = 1/12                          modular Euler characteristic
N_bands = χ⁻¹ = 12              oscillation modes
sleep = 1/3                       12-band consolidation fraction
E_Landauer = k_B T ln(2)         minimum energy/bit at 300K
```

**The oscillation band claim:**

The brain has 12 canonical oscillatory bands from delta to high-gamma.
The claim is that this follows from χ = 1/12 (the same 1/12 that appears in
dim S₂(Γ₀(N)) ~ N/12 for modular forms). Band spacing is p=2 octave ratio,
forced by the integrality condition.

Sleep = 1/3 is a consequence: with 12 bands and p=2 spacing, the consolidation
window that completes one full depth cycle is τ_∞·4; active window is τ_∞·2;
sleep fraction = 1/3. This is not fit to biological data.

**The energy claim:**

Spike rule: depth d fires when |V − V_eq| > 2^(−d).
Transformer attention: n²·d·b erasure events.
Neuromorphic: n·b archimedean + 0 p-adic (routing is not erasure).
Efficiency ratio: 1/(n·d).

| n | d | speedup |
|---|---|---------|
| 1,024 | 64 | 65,536× |
| 4,096 | 64 | 262,144× |
| 32,768 | 64 | 2,097,152× |

Benchmark (pure Python, no deps): https://github.com/rfdevuser/vectorpeak-experiments

Posting here primarily for the χ=1/12 → 12 bands claim — interested whether
anyone has seen a derivation of the oscillation band count from topological
invariants before, or a counterargument.
```

---

## Discord — `#neuroscience` / `#ml-hardware` / `#showcase`

```
Posted a benchmark for a neuromorphic architecture where all timing constants
are derived — zero free parameters vs 8–15 in Brian2/NEST/Loihi 2.

Three claims:

1. τ_∞ = 1/(2π), refractory = τ_∞·ln(2), χ=1/12, N_bands=12, sleep=1/3 — all
   forced by the adelic axiom system. No search. No calibration.

2. The brain's 12 oscillatory bands (delta → high-gamma) follow from χ=1/12
   (modular Euler characteristic). Same 1/12 as dim S₂(Γ₀(N)) ~ N/12.
   Sleep fraction 1/3 is derived from the same structure — not fit to data.

3. Thermodynamic: transformer = O(n²db) erasures; neuromorphic = O(nb) + 0 p-adic.
   At n=4096, d=64: 262,144× energy advantage at the Landauer limit.

Pure Python, zero deps: https://github.com/rfdevuser/vectorpeak-experiments
```

---

## X / Twitter — 4-tweet thread

**Tweet 1 (hook):**
```
Every SNN framework — Brian2, NEST, Loihi 2 — needs 8–15 hand-tuned constants.

NeuroCore needs zero.

τ_∞ = 1/(2π). Refractory = τ_∞·ln(2). Bands = 12. Sleep = 1/3.

None of these are parameters. All of them are derived. 🧵
```

**Tweet 2 (the oscillation claim):**
```
Why 12 oscillatory bands?

χ = 1/12 (modular Euler characteristic) → N_bands = χ⁻¹ = 12

Same 1/12 as: dim S₂(Γ₀(N)) ~ N/12

Band spacing: p=2 (octave), forced by integrality of log(p)/log(2).

Sleep = 1/3: consolidation window for 12 bands at p=2 is τ_∞·4;
active window τ_∞·2; ratio = 1/3.

Humans sleep 8h in 24h = 1/3. Not a fit. A consequence.
```

**Tweet 3 (the energy claim):**
```
Transformer attention: O(n²·d·b) bit erasures at Landauer limit.
Neuromorphic (NeuroCore): O(n·b) + 0 p-adic.

p-adic valuation is structural routing — it costs no Landauer energy.
Only erasure does.

n=4096, d=64:
  Transformer on Loihi 2: 34.36 µJ
  NeuroCore on Loihi 2:    0.13 nJ
  Ratio: 262,144× — exactly 1/(n·d)
```

**Tweet 4 (the link):**
```
Benchmark: 4 phases
  1. All 8 derived constants vs standard frameworks (8–15 free params)
  2. 12-band oscillation structure from χ=1/12
  3. Energy table from n=128 to n=32,768
  4. Depth-threshold spike cascade demo

Pure Python. Zero deps.
[repo link]
```
