# ModelGuard — Post Copy

---

## LinkedIn

```
Three fine-tuned models. Same architecture. Same validation loss. Standard
deployment checklist: all three pass.

ModelGuard disagrees with two of them.

The issue is a quantity called the Curie distance: D = parameters / training tokens.
At D ≈ 1, the Marchenko-Pastur self-consistency equation loses its finite solution.
Generalisation variance diverges — not gradually, but vertically. This is the
interpolation threshold.

A model at D = 0.90 and a model at D = 0.20 can produce identical validation loss
while having generalisation variance that differs by an order of magnitude. The
variance component only appears on out-of-distribution inputs — the ones that
arrive in production, not in the validation set.

The parameter count and training token count are known quantities before deployment.
ModelGuard computes D at audit time and blocks deployment for any model in the
critical zone D ∈ [0.85, 1.15]. No additional evaluation needed. No data required.

Benchmark audits GPT-3, LLaMA-3, Mistral 7B, Gemma 2B, and Chinchilla on their
Curie distances, then shows the variance spike as D approaches 1, then reproduces
the mismatch: same val_loss, 9× higher generalisation variance. Pure Python, zero
dependencies.
[link to repo]

The question it answers: does your deployment checklist measure generalisation
variance, or just generalisation loss?
```

---

## Reddit — r/MachineLearning or r/learnmachinelearning

**Title:**
```
Curie distance D = p/n flags deployments that val loss misses — generalisation variance diverges at D ≈ 1 (pure Python benchmark, no deps)
```

**Body:**
```
Built a benchmark for a generalisation risk measure that val loss doesn't capture:
the Curie distance D = parameters / training tokens.

**The problem:**

Validation loss measures `bias² + variance`. When D ≈ 1 (the interpolation threshold),
bias can be near zero while variance is diverging. Val loss underestimates deployment
risk because the variance component only manifests on out-of-distribution inputs —
exactly what arrives in production.

**The construct:**

From Marchenko-Pastur, the asymptotic noise variance is:

```
V = σ² · D / |1 − D|   →   ∞  as D → 1
```

Three phases:
- Ordered (D < 0.85): unique minimiser exists, apply λ* = σ²·(1−D)/D
- Critical (0.85 ≤ D ≤ 1.15): variance maximally elevated — do not deploy
- Disordered (D > 1.15): interpolation regime, implicit regularisation governs

**The benchmark (Phase 3 — the mismatch):**

Three fine-tuned models. Same architecture. Val loss = 0.42 (all three).

| Model | p | n | D | Phase | Variance |
|---|---|---|---|---|---|
| Model A (safe) | 100M | 500M | 0.200 | ordered | 0.0105 |
| Model B (risky) | 100M | 110M | 0.909 | **critical** | **0.094** (9×) |
| Model C | 100M | 102M | 0.980 | **critical** | **∞** |

Standard checklist passes all three. D flags two of them before deployment.

**Known LLMs:**

GPT-3 (175B, 300B tokens): D = 0.583 — 11.7× above Chinchilla ratio, ordered but undertrained.
LLaMA-3 8B (8B, 15T tokens): D = 0.0005 — deeply ordered.
Chinchilla (70B, 1.4T tokens): D = 0.05 — at the Chinchilla optimum.

No model in the benchmark lands in the critical zone — real-world fine-tunes on
smaller token budgets (10–20% of parameters as tokens) are the typical risk case.

Pure Python, zero dependencies: https://github.com/rfdevuser/vectorpeak-experiments

Curious whether others have hit the D ≈ 1 failure mode in practice on fine-tuned
models with constrained training budgets.
```

---

## Discord — ML / AI safety / MLOps communities `#showcase`

```
Built a benchmark for a generalisation risk measure that val loss doesn't capture.

The core: D = parameters / training tokens. At D ≈ 1, Marchenko-Pastur variance
diverges — vertically, not gradually. Standard deployment checklists (val loss,
accuracy, latency) don't measure this.

The benchmark shows three fine-tuned models with identical val_loss = 0.42. Two of
them have D ∈ [0.85, 1.15] — the critical zone — and their generalisation variance
is 9× and ∞× higher than the third. Same loss, completely different risk.

Also audits GPT-3, LLaMA-3, Mistral, Gemma, Chinchilla. Shows the variance spike
as D approaches 1. Pure Python, zero deps:
https://github.com/rfdevuser/vectorpeak-experiments

Posting here because the D ≈ 1 failure mode is easy to hit on fine-tuned models
with constrained training budgets — interested whether anyone's seen this in practice.
```

---

## X / Twitter — 4-tweet thread

**Tweet 1 (hook — attach terminal screenshot or GIF):**
```
Three fine-tuned models. Same val_loss. Standard deployment checklist: all pass.

One has 9× higher generalisation variance than another.
One has variance → ∞.

The difference is a single number: D = parameters / training tokens. 🧵
```

**Tweet 2 (the physics):**
```
At D = 1, the Marchenko-Pastur self-consistency equation loses its finite solution.
Variance diverges vertically.

V = σ² · D / |1 − D|  →  ∞

This is the interpolation threshold. ML training curves don't show it.
Val loss doesn't measure it. D does.
```

**Tweet 3 (the mismatch):**
```
GPT-3: D = 0.58  (175B params, 300B tokens) — ordered phase
LLaMA-3 8B: D = 0.0005 (8B params, 15T tokens) — deeply ordered
Chinchilla: D = 0.05 — at the optimum

The danger zone: fine-tuned models where n ≈ p.
D ∈ [0.85, 1.15] = block deployment.
```

**Tweet 4 (the link):**
```
Pure Python benchmark.
Audits real LLMs, shows the variance spike at D → 1,
reproduces the mismatch: same val_loss, 9× different generalisation variance.

Zero dependencies.

[repo]
```
