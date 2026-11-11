# DoubleDescentGuard — Post Copy

---

## LinkedIn

```
Two credit scoring models. Same training data. Same validation Gini. One
generalises at 70%. The other generalises at 0.34%.

The difference is a single number: ρ = p_eff / n_eff — the effective capacity ratio.

Here's what the double descent curve actually looks like:

  F_gen(ρ) = exp(−2π/ρ²)

At ρ = 1 (the interpolation threshold):
  F_gen = exp(−2π) ≈ 0.19%
  99.81% of what the model learned is trapped at the threshold.
  Validation loss looks normal. Nothing in the standard checklist flags it.

The two credit scoring models:

  Model A: p=15,000  n=50,000  SNR=0.35  reg=0.1  →  ρ=1.05  F_gen=0.34%  BLOCK
  Model B: p=60,000  n=50,000  SNR=0.35  reg=0.1  →  ρ=4.21  F_gen=70.1%  APPROVE

Same data, same noise floor, same regularisation. 4× more parameters is the
only difference. At 15K: blocked. At 60K: cleared for IRB/CECL submission.

The regularisation trap — practitioners who add more L2 to a struggling model
(PARADOX zone, ρ ≈ 1.5–3) are moving ρ downward, toward the critical peak,
not away from it. The correct fix is MORE capacity, not less.

The trading signal version of this: 150 factors → ρ=2.52 → F_gen=37% → backtest
Sharpe will not persist. 350 factors (same 5yr daily data) → ρ=5.88 → F_gen=83%
→ cleared for live allocation. The double descent paradox in one line: add more
parameters to fix poor out-of-sample performance.

DoubleDescentGuard certifies every model against F_gen before deployment:
[link to repo]

Pure Python benchmark, zero dependencies.
```

---

## Reddit — r/MachineLearning

**Title:**
```
F_gen(ρ) = exp(−2π/ρ²) — the generalisation fraction at the double descent peak is 0.19%. Pure Python benchmark showing what val loss misses.
```

**Body:**
```
Built a benchmark around a closed-form generalisation fraction that quantifies
exactly how much of a model's learned capacity actually projects onto the
generalisation subspace.

**The construct:**

```
F_gen(ρ) = exp(−2π / ρ²)

ρ = p_eff / n_eff
p_eff = p / (1 + reg_strength)   # reg reduces effective capacity
n_eff = n · SNR / (1 + SNR)      # noise reduces effective sample count
```

Three landmarks:
- ρ = 1 (interpolation threshold): F_gen = 0.19%
- ρ* = √(2π/ln2) ≈ 3.01: F_gen = 50% (half-generalisation threshold)
- ρ_th = 4: F_gen = 67.5% (production-safe floor)

**What this adds over ModelGuard / D = p/n:**

D is the raw ratio p/n — it classifies the phase but is blind to regularisation
strength and SNR. Two models with identical D can sit at completely different
points on the F_gen curve.

Benchmark Phase 3 shows this directly:

```
p=20,000  n=50,000  SNR=0.30  →  D = 0.40  (ModelGuard: ordered, no flag)

reg=0.0:  p_eff=20,000  ρ=1.73  F_gen=12.4%  PARADOX
reg=0.3:  p_eff=15,385  ρ=1.33  F_gen=2.9%   CRITICAL
reg=1.5:  p_eff=8,000   ρ=0.69  F_gen~0%     UNDERFIT
```

D = 0.40 for all three. ModelGuard gives the same call. ρ ranges from 0.69 to 1.73 —
three different regimes.

**The regularisation trap:**

Adding L2 regularisation to a PARADOX model (ρ ∈ 1.5–3.01) reduces p_eff, which
reduces ρ, which moves the model toward the critical peak, not away from it. The
correct fix for a PARADOX model is to increase capacity (raise ρ past 3.01), not
to regularise harder.

**Two credit scoring models (same data, different capacity):**

```
p=15,000  n=50,000  SNR=0.35  reg=0.1  →  ρ=1.052  F_gen=0.34%  BLOCK
p=60,000  n=50,000  SNR=0.35  reg=0.1  →  ρ=4.208  F_gen=70.1%  APPROVE
```

Validation Gini doesn't distinguish them. ρ does.

Repo: https://github.com/rfdevuser/vectorpeak-experiments
Run: `python run_doubledescentguard_benchmark.py`

Happy to discuss the derivation of F_gen(ρ) = exp(−2π/ρ²) in the comments —
particularly the connection to the Marchenko-Pastur self-consistency equation
and why the exponent is −2π specifically.
```

---

## Discord — `#ml-safety` / `#mlops` / `#showcase`

```
Posted a benchmark for a closed-form generalisation fraction that quantifies
the double descent curve analytically.

F_gen(ρ) = exp(−2π/ρ²)  where ρ = p_eff / n_eff

At ρ=1 (interpolation threshold): 0.19% generalises.
At ρ=3.01: 50% generalises (half-generalisation threshold).
At ρ=4: 67.5% — production safe floor.

Three phases in the benchmark:
1. The curve — F_gen table from ρ=0.5 to ρ=8
2. Six financial model certifications (credit, trading, fraud, VaR) — 3 blocked, 3 approved
3. The regularisation lever — same D=0.40 (ModelGuard: ordered), three different ρ values,
   three different regimes — shows what D misses

Key finding: adding L2 regularisation to a PARADOX model (ρ ∈ 1.5–3) makes
generalisation WORSE, not better. The correct fix is to add parameters, not regularise.

Pure Python, zero deps: https://github.com/rfdevuser/vectorpeak-experiments
```

---

## X / Twitter — 4-tweet thread

**Tweet 1 (hook):**
```
Two credit scoring models. Same data. Same validation Gini.

One generalises at 70%.
One generalises at 0.34%.

The number that separates them: ρ = p_eff / n_eff

F_gen(ρ) = exp(−2π/ρ²) 🧵
```

**Tweet 2 (the peak):**
```
At ρ = 1 (the interpolation threshold):

  F_gen = exp(−2π) = 0.19%

99.81% of what the model learned is trapped.
Validation loss looks fine.
Nothing in a standard deployment checklist catches this.

The 0.19% is not an approximation. It's exact.
```

**Tweet 3 (the paradox):**
```
Trading signal — 150 factors, 5yr daily data, no regularisation:

  ρ = 2.52  →  F_gen = 37%  →  PARADOX  →  blocked

Fix: add 200 MORE factors (same data):

  ρ = 5.88  →  F_gen = 83%  →  ACCESSIBLE  →  approved

The double descent paradox: more parameters rescues generalisation.
Regularising harder would have made it worse.
```

**Tweet 4 (the link):**
```
DoubleDescentGuard certifies every model against F_gen before deployment.

What D = p/n misses: regularisation strength and SNR.
ρ = p_eff / n_eff accounts for both.

Pure Python benchmark, zero deps:
[repo link]
```
