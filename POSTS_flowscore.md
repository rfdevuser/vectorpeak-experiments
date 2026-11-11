# FlowScore — Post Copy

---

## LinkedIn

```
India has ~400 million active UPI users with no credit bureau record.

CIBIL scores them 0. The bank says no.

FlowScore scores them from 30 days of transaction variance alone.

The formula:
  D   = σ_ref / σ_tx              (Curie distance — 1 = healthy, 0 = near default)
  F   = 100 × D²                  (FlowScore, range 0–100)
  PD  = 1 − exp(−T × k₀ × exp(−α·D²))   (Kramers escape rate)

Two constants. No per-borrower fitting.

The Thin-File UPI result:
  CIBIL = 0 — bank rejects
  FlowScore = 60.9 (ELEVATED), PD_90 = 0.210%

The Near Default result (CIBIL = 660 — bank approves):
  FlowScore = 1.6 (NEAR-DEFAULT), PD_90 = 2.229%

The near-default borrower hasn't missed an EMI yet. Their transaction variance
(σ_tx = 68,000 vs σ_ref = 8,500) already shows the stress.

CIBIL approves them. FlowScore flags them.

There's also a CSD flag — critical slowing down:
  AC(lag-1) = 1 − D²
  When AC > 0.75, payment timing autocorrelation has entered the precursor regime.

In a deteriorating borrower trajectory, the CSD flag fires 1 month before the
NEAR-DEFAULT tier is crossed. That's 1 month of intervention window —
restructure, reduce limit, make contact.

52× higher default probability from D=1.0 to D=0.1. No logistic regression.
No historical default data required.

Benchmark (pure Python, zero deps):
[link to repo]
```

---

## Reddit — r/fintech / r/india / r/MachineLearning

**Title:**
```
Scoring India's 400M thin-file UPI borrowers with transaction variance (pure Python benchmark)
```

**Body:**
```
Built a benchmark for a Kramers-escape-rate credit scoring model. Posting because
the CIBIL-vs-FlowScore comparison produced a non-obvious result and I want to know
if there's prior work on the near-default detection.

**The model:**

D = σ_ref / σ_tx   — ratio of reference variance to current transaction variance
F = 100 × D²       — FlowScore [0, 100]
P(default|T) = 1 − exp(−T × k₀ × exp(−α·D²))

Two population constants (k₀=0.008, α=4.0). Not per-borrower fitting.

**The thin-file result:**

| Borrower      | CIBIL  | FlowScore | PD_90   |
|---------------|--------|-----------|---------|
| Thin-File UPI | 0 REJECTED | 60.9    | 0.210%  |
| Near Default  | 660 APPROVED | 1.6  | 2.229%  |

The near-default borrower has CIBIL 660 (bank approves) but transaction variance
8× above baseline. FlowScore catches it. PD_90 is 11× higher than the
thin-file user the bureau rejected.

**The CSD (critical slowing down) flag:**

AC(lag-1) = 1 − D²

When payment timing autocorrelation exceeds 0.75 (D < 0.5), the borrower is in
the critical slowing-down regime — the same precursor that predicts ecosystem
collapse, cardiac arrhythmia, and climate tipping points.

In a 6-month deterioration trajectory, the CSD flag fires 1 month before the
NEAR-DEFAULT tier is crossed. The lender has an intervention window.

**The amplification:**

PD_90 at D=1.0: 0.044%
PD_90 at D=0.1: 2.280%
Ratio: 52×

Is this known? Kramers-based PD with the variance ratio as the driving variable?
Prior work I'm aware of: Schumpeterian creative destruction models, Merton
structural model (but that uses asset value volatility, not transaction variance).

Benchmark: https://github.com/rfdevuser/vectorpeak-experiments
```

---

## Discord — `#fintech` / `#ml-india` / `#showcase`

```
Posted a credit scoring benchmark for India's thin-file market.

The core: D = σ_ref / σ_tx, F = 100 × D², PD from Kramers escape rate.
Two constants (k₀, α). No per-borrower fitting. No credit bureau data needed.

Four phases:

1. Five presets — Healthy, Thin-File UPI, Mild Stress, High-Risk MSME, Near Default
2. CIBIL comparison — thin-file user (CIBIL=0, rejected) has FlowScore 60.9 and
   PD_90=0.210%; near-default borrower (CIBIL=660, approved) has FlowScore 1.6
   and PD_90=2.229%. CIBIL approves the riskier borrower.
3. PD curve across D — 52× amplification from healthy to near-default via exp(−αD²)
4. CSD trajectory — AC=1−D² fires 1 month before NEAR-DEFAULT tier

Pure Python, zero deps. Runs in ~1 second.

https://github.com/rfdevuser/vectorpeak-experiments
```

---

## X / Twitter — 4-tweet thread

**Tweet 1 (hook):**
```
India has 400M UPI users with no credit history.

CIBIL gives them a score of 0. The bank says no.

FlowScore gives them a score in real time from 30 days of transaction variance.

The result is surprising. 🧵
```

**Tweet 2 (the reversal):**
```
Near Default borrower: CIBIL 660 (bank APPROVES)
Thin-File UPI user: CIBIL 0 (bank REJECTS)

FlowScore tells a different story:

Near Default:   FlowScore 1.6, PD_90 = 2.229% ← NEAR-DEFAULT
Thin-File UPI:  FlowScore 60.9, PD_90 = 0.210% ← ELEVATED

The near-default borrower hasn't missed an EMI yet.
Their σ_tx = 68,000 vs σ_ref = 8,500 already shows the stress.
```

**Tweet 3 (the formula):**
```
FlowScore math:

D = σ_ref / σ_tx              (Curie distance)
F = 100 × D²                  (score)
P(default|T) = 1 − exp(−T × k₀ × exp(−α·D²))   (Kramers escape rate)

Two constants: k₀ = 0.008, α = 4.0.
Not logistic regression. Not a fitted scorecard.

52× PD amplification from D=1 to D=0.1.
CSD flag (AC=1−D²>0.75) fires 1 month before NEAR-DEFAULT tier.
```

**Tweet 4 (the link):**
```
Benchmark: 4 phases
  1. Five presets — full certificate (D, F, PD_30/90/180, CSD)
  2. CIBIL comparison — thin-file borrower that bureau rejects
  3. Kramers amplification — 52× from healthy to near-default
  4. CSD trajectory — 1-month early warning

Pure Python, zero deps:
[repo link]
```
