# DoubleDescentGuard — Double Descent Certificate

**F_gen(ρ) = exp(−2π/ρ²) — the generalisation projection fraction.**

At the double descent peak (ρ = 1): F_gen = 0.19%. Less than 1 in 500 capacity
units generalise. The model passes validation. The generalisation deficit is
completely invisible to val loss.

---

## Quickstart

```bash
git clone https://github.com/rfdevuser/vectorpeak-experiments
cd vectorpeak-experiments
python run_doubledescentguard_benchmark.py
```

Pure Python, zero dependencies.

---

## The Construct

ρ is the **effective capacity ratio**:

```
ρ = p_eff / n_eff

p_eff = p / (1 + reg_strength)      regularisation reduces effective capacity
n_eff = n · SNR / (1 + SNR)         noise reduces effective sample count
```

F_gen(ρ) measures what fraction of the model's learned capacity actually projects
onto the generalisation subspace:

```
F_gen(ρ) = exp(−2π / ρ²)
```

Three landmarks on the curve:

| ρ | F_gen | Landmark |
|---|-------|----------|
| 1.00 | **0.19%** | Double descent peak — maximum risk |
| ≈ 3.01 | 50.0% | Half-generalisation threshold (ρ*) |
| 4.00 | **67.5%** | Production-safe floor (ρ_th) |

---

## The F_gen Curve

```
F_gen %
  70 │                                                    ·· ──
  60 │                                               ·····
  50 │                                          ·····         ← ρ* = 3.01
  40 │                                     ·····
  20 │                               ······
   6 │                         ······
   0.19% ←─────────────────────── PEAK at ρ=1
       └────┬──────┬──────┬──────┬──────┬──────┬──▶ ρ
           0.5    1.0    1.5    2.0    3.0    4.0
```

The curve is not symmetric around ρ=1. Recovery is slow — the model must reach
ρ ≈ 3 to recover 50% generalisation, and ρ = 4 to reach the production safe floor.

---

## Five Regimes

| Regime | ρ range | F_gen | Deploy? |
|--------|---------|-------|---------|
| UNDERFIT | ρ < 1 | < 0.19% | DO_NOT_DEPLOY — model cannot fit training data |
| CRITICAL | 1 ≤ ρ < 1.5 | 0.19% – 6% | DO_NOT_DEPLOY — at or near the peak |
| PARADOX | 1.5 ≤ ρ < 3.01 | 6% – 50% | DO_NOT_DEPLOY — overparameterised but < half generalises |
| MARGINAL | 3.01 ≤ ρ < 4 | 50% – 67.5% | CAUTION — acceptable with monitoring |
| ACCESSIBLE | ρ ≥ 4 | ≥ 67.5% | APPROVED — production safe |

---

## Phase 2 — Six Financial Model Certifications

```
Model                          ρ      F_gen    Regime       Verdict
─────────────────────────────  ─────  ───────  ───────────  ──────────────
Credit scoring (critical)      1.052  0.34%    CRITICAL     DO_NOT_DEPLOY
Credit scoring (safe)          4.208  70.1%    ACCESSIBLE   APPROVED
Trading signal (paradox)       2.520  37.2%    PARADOX      DO_NOT_DEPLOY
Trading signal (accessible)    5.880  83.4%    ACCESSIBLE   APPROVED
Fraud detection (large)        9.657  93.5%    ACCESSIBLE   APPROVED
Risk factor model              1.429  4.6%     CRITICAL     DO_NOT_DEPLOY
```

The two credit scoring models have **the same training data** (n=50,000, SNR=0.35,
reg=0.1). The only difference is parameter count: 15,000 vs 60,000. At 15K: 0.34%
generalises and the model is blocked. At 60K: 70.1% generalises and the model is
approved. Validation loss does not distinguish them.

**Trading signal paradox:** 150 factors → ρ=2.52 → F_gen=37% (PARADOX, blocked).
350 factors (same data) → ρ=5.88 → F_gen=83% (ACCESSIBLE, approved).
More parameters rescues generalisation. This is the double descent paradox — the
correct fix is to add capacity, not remove it.

---

## Phase 3 — The Regularisation Lever

For a model with p=20,000, n=50,000, SNR=0.3 (D = 0.40, ModelGuard says ORDERED):

```
reg_strength  p_eff   ρ      F_gen    Regime    Verdict
────────────  ──────  ─────  ───────  ────────  ─────────────
0.00          20,000  1.733  12.4%    PARADOX   DO_NOT_DEPLOY
0.30          15,385  1.333  2.9%     CRITICAL  DO_NOT_DEPLOY
1.50           8,000  0.693  ~0%      UNDERFIT  DO_NOT_DEPLOY
5.00           3,333  0.289  ~0%      UNDERFIT  DO_NOT_DEPLOY
```

ModelGuard sees D = 0.40 for all four — ordered phase, no flag.
DoubleDescentGuard sees ρ ranging from 0.29 to 1.73 — three different regimes.

**The regularisation trap:** adding more L2 regularisation to a PARADOX model
moves ρ *downward* toward the critical peak, then into underfitting. The correct
fix for a PARADOX model is to increase capacity (raise ρ past ρ* = 3.01), not
to regularise harder.

---

## ModelGuard vs DoubleDescentGuard

| Measure | What it captures | Blind to |
|---------|-----------------|---------|
| D = p/n (ModelGuard) | Proximity to interpolation threshold (Marchenko-Pastur) | SNR, regularisation strength |
| ρ = p_eff/n_eff (DDGuard) | Exact generalisation fraction F_gen | Nothing — accounts for both |

They are complementary. D flags the phase; ρ gives the exact F_gen value and
the minimum capacity required to reach each threshold.

---

## Task-Specific Consequences

| Task | CRITICAL consequence |
|------|---------------------|
| Credit scoring | Val Gini will not reflect production. Regulatory approval unlikely. |
| Trading signal | Backtest Sharpe will not persist out-of-sample. Do not allocate capital. |
| Fraud detection | Production false negative rate will exceed validation FNR. |
| Risk factor / VaR | Factor covariance near-singular. VaR certification invalid. |

---

## Running the Benchmark

```bash
python run_doubledescentguard_benchmark.py
```

Expected output:
```
Phase 1: F_gen curve — 0.19% at ρ=1, 50% at ρ=3.01, 67.5% at ρ=4
Phase 2: 6 models certified — 3 blocked, 3 approved
Phase 3: D = 0.40 for all (ModelGuard: ordered) — ρ varies 0.29–1.73 (DDGuard: three regimes)
```

---

## Get the Full Product

For API access, integration docs, and pricing:
**[vallikat@vectorpeaktech.com](mailto:vallikat@vectorpeaktech.com)**
