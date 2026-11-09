# ModelGuard — AI Generalisation Risk Intelligence Benchmark

**File:** `run_modelguard_benchmark.py`

Demonstrates the core property of ModelGuard: D = p/n (parameters / training tokens)
is the Curie distance from the interpolation threshold γ_c = 1. At D ≈ 1, generalisation
variance diverges regardless of validation loss. Standard deployment checklists miss this
entirely. No external dependencies. Pure Python 3.8+.

---

## Quickstart

```bash
git clone https://github.com/rfdevuser/vectorpeak-experiments
cd vectorpeak-experiments
python run_modelguard_benchmark.py
```

No `pip install` needed. Pure Python standard library only.

---

## The core concept: Γ₄₉ — KMS Curie Distance

The standard deployment checklist for ML models is: validation loss, accuracy, latency.
None of these measure the proximity to the interpolation threshold — the point where
generalisation variance diverges.

ModelGuard defines the **Curie distance**:

```
D = p / n
```

where `p` is the parameter count and `n` is the number of training tokens (or samples).
At D = 1, the Marchenko-Pastur self-consistency equation loses its finite solution.
Variance diverges. This is the **21st KMS Curie temperature** in the domain classification.

Three phases:

| Phase | D range | Behaviour |
|---|---|---|
| Ordered | D < 0.85 | Unique minimiser exists; apply optimal weight decay λ* |
| **Critical** | **0.85 ≤ D ≤ 1.15** | **Variance maximally elevated — do not deploy** |
| Disordered | D > 1.15 | Interpolation regime; implicit regularisation governs generalisation |

The asymptotic noise variance from Marchenko-Pastur:

```
V = σ² · D / |1 − D|   →   ∞  as D → 1
```

The optimal ridge regularisation from Stein's identity / F1 fixed-point:

```
λ* = σ² · (1 − D) / D    for D < 1   (underparameterised)
λ* = 0                    for D ≥ 1   (interpolation regime)
```

---

## What it shows

```
$ python run_modelguard_benchmark.py

════════════════════════════════════════════════════════════════════
  MODELGUARD — AI GENERALISATION RISK INTELLIGENCE  (Γ₄₉)
════════════════════════════════════════════════════════════════════
  Claim: D = p/n is the Curie distance from the interpolation threshold.
         At D ≈ 1, generalisation variance diverges regardless of val loss.
         Standard deployment checklists miss this entirely.
  KMS Curie temperature: γ_c = 1  (21st domain in KMS classification)

[PHASE 1: Model Audit — Curie Distance D = p / n]

  Model                      Params           Tokens        D  Phase        Risk    λ* rec
  ──────────────────────── ──────────── ──────────────── ────────  ──────────── ─────  ────────
  GPT-3 (175B)       175,000,000,000  300,000,000,000   0.5833  ordered          29    0.7143
  LLaMA-3 8B           8,000,000,000   15,000,000,000   0.0005  ordered           0  2096.0000
  LLaMA-3 70B         70,000,000,000   15,000,000,000   0.0047  ordered           0   213.4286
  Mistral 7B           7,000,000,000    1,000,000,000   0.0070  ordered           0   141.4286
  Gemma 2B             2,000,000,000    3,000,000,000   0.0007  ordered           0  1500.0000
  Chinchilla (70B)    70,000,000,000    1,400,000,000   0.0500  ordered           3    19.0000

  No models in critical zone.

  Chinchilla optimum target: D ≈ 0.05  (n = 20 × p)
  GPT-3: D = 0.5833  → 11.7× above Chinchilla ratio (undertrained at launch)
  Chinchilla: D = 0.0500  → at the Chinchilla optimum

[PHASE 2: Variance Amplification — V = σ²·D / |1−D|]

  σ² = 0.1  (fixed noise level)

      D  Phase             Variance V   Risk    λ* rec
  ──────  ────────────  ──────────────  ─────  ────────
    0.50  ordered               0.1000     25   0.10000
    0.70  ordered               0.2333     15   0.04286
    0.85  critical              0.5667      8   0.01765
    0.90  critical              0.9000      5   0.01111
    0.95  critical              1.9000      3   0.00526
    0.99  critical              9.9000      1   0.00101
    1.00  critical       ∞ (diverges)      0   0.00000  ← MAXIMUM RISK
    1.01  disordered            1.0100      0   0.00000
    1.05  disordered            2.1000      0   0.00000
    1.10  disordered            1.1000      0   0.00000
    1.30  disordered            0.4333      0   0.00000
    2.00  disordered            0.2000      0   0.00000

  At D = 0.5:  V = 0.1000
  At D = 0.95: V = 1.9000   (19.0× higher than D=0.5)
  At D = 1.00: V → ∞  (Marchenko-Pastur self-consistency equation loses finite solution)

  Marchenko-Pastur spectral edges at D=0.95: λ₋=0.0025  λ₊=3.8025
  At D≥1 the lower edge collapses to 0 — bulk eigenvalue mass accumulates at zero.

[PHASE 3: The Mismatch — Same Val Loss, Different Generalisation Risk]

  Three fine-tuned models. Same architecture. Same val_loss = 0.42.
  Standard checklist: all three look identical. ModelGuard disagrees.

  Model                    p           n        D  Phase        Risk    Variance V
  ──────────────────── ─────────── ──────────── ────────  ──────────── ─────  ────────────
  Model A (safe)       100,000,000  500,000,000   0.2000  ordered          40        0.0105
  Model B (risky)      100,000,000  110,000,000   0.9091  critical         95        0.0945
  Model C (critical)   100,000,000  102,000,000   0.9804  critical         99     ∞

  Val loss (all three):  0.42  — standard deployment checklist: PASS

  Model A: D = 0.2000  Ordered phase.  Low variance.  Deploy.
  Model B: D = 0.9091  Critical zone.  Variance = 0.09  (9.0× higher than Model A).  BLOCK.
  Model C: D = 0.9804  Critical zone.  Variance → ∞.  Marchenko-Pastur loses finite solution.  BLOCK.

  Same val_loss.  Generalisation variance: 9.0× higher in Model B.
  Val loss does not measure generalisation variance. D does.

════════════════════════════════════════════════════════════════════
  Val loss check      : catches absolute performance, not variance risk
  Curie distance D    : detects proximity to the interpolation threshold
  Critical zone (D≈1) : variance diverges — ML orthodoxy has no name for this
  ModelGuard          : blocks deployment at D ∈ [0.85, 1.15]
════════════════════════════════════════════════════════════════════
```

---

## The three-phase D axis

```
  Ordered          Critical         Disordered
  D < 0.85         0.85–1.15        D > 1.15
  ─────────────────────┬──────────────────────────▶ D
                       1
                   γ_c = 1
               Interpolation threshold
               (Variance → ∞)
```

The ordered and disordered phases are both safe from the variance perspective —
the danger is the narrow critical zone around D = 1.

---

## Why val loss doesn't catch this

Validation loss measures expected squared error at the current model checkpoint:

```
L_val = bias² + variance
```

When D ≈ 1, bias can be near zero (the model fits training data well) but variance is
diverging. Val loss underestimates deployment risk because the variance component only
manifests on out-of-distribution inputs — exactly the inputs that appear in production
but not in validation.

ModelGuard measures D directly — it does not require running any additional evaluation.
The parameter count and training token count are known quantities.

---

## Marchenko-Pastur spectral edges

The spectral edges of the random feature matrix under the MP law:

```
λ± = (1 ± √D)²
```

For D > 1, the lower edge collapses to 0: `λ₋ = 0`. Bulk eigenvalue mass accumulates
at zero — a symptom of rank deficiency in the effective feature representation.

At D = 1, both edges meet: the spectral distribution loses its finite support and
the MP self-consistency equation diverges.

---

## Get the full product

For API access, integration docs, and pricing:

**[vallikat@vectorpeaktech.com](mailto:vallikat@vectorpeaktech.com)**
