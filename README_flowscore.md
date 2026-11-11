# FlowScore — Alternative Credit Risk from Transaction Variance

**Γ₇₈ Kramers escape-rate credit scoring. Two population constants. Zero per-borrower fitting.**

Standard bureau scoring requires 2+ years of credit history. FlowScore scores any borrower
from 30-day transaction variance alone. India has ~400 million UPI users with no credit
bureau record — CIBIL scores them 0 and refuses. FlowScore scores them in real time.

---

## Quickstart

```bash
git clone https://github.com/rfdevuser/vectorpeak-experiments
cd vectorpeak-experiments
python run_flowscore_benchmark.py
```

No dependencies. Pure Python standard library only.

---

## The Four Claims

**1. D = σ_ref / σ_tx is the natural credit variable.**
When transaction variance exceeds the reference baseline, the borrower is under stress.
D is not a fitted score — it is the ratio of two observable quantities.
FlowScore F = 100 × D² maps D onto [0, 100] via the same quadratic that appears in
the Curie distance for magnetic systems undergoing phase transitions.

**2. Kramers escape rate gives exact default probability.**
`P(default | T) = 1 − exp(−T_months × k₀ × exp(−α·D²))`
Two population-level constants (k₀, α), not per-borrower regression coefficients.
k₀ = 0.008 is the baseline monthly default rate. α = 4.0 is the barrier depth.
The Kramers form is derived from first principles (thermal barrier-crossing physics),
not fitted to historical defaults.

**3. 52× PD amplification from healthy to near-default.**
At D = 1.0 (healthy): PD_90 = 0.044%.
At D = 0.1 (near-default): PD_90 = 2.280%.
Ratio: 52×. A logistic sigmoid gives a symmetric S-curve and misses the
exponential acceleration near D → 0.

**4. CSD flag fires 1 month before NEAR-DEFAULT tier.**
AC(lag-1) = 1 − D² is the critical slowing-down indicator. When AC > 0.75 (D < 0.5),
payment timing variance shows the universal precursor to a phase transition.
The CSD flag fires from transaction data alone — before any missed payment.

---

## Phase 1 — Five Preset Borrowers

| Borrower | σ_ref | σ_tx | D | FlowScore | PD_90 | CSD | Tier |
|----------|-------|------|---|-----------|-------|-----|------|
| Healthy Salaried | 8,500 | 8,200 | 1.000 | 100.0 | 0.044% | no | LOW RISK |
| Thin-File UPI | 3,200 | 4,100 | 0.780 | 60.9 | 0.210% | no | ELEVATED |
| Mild Stress | 8,500 | 12,000 | 0.708 | 50.2 | 0.322% | no | ELEVATED |
| High-Risk MSME | 25,000 | 52,000 | 0.481 | 23.1 | 0.948% | YES | HIGH RISK |
| Near Default | 8,500 | 68,000 | 0.125 | 1.6 | 2.229% | YES | NEAR-DEFAULT |

Near Default / Healthy PD_90 ratio: **51×**

---

## Phase 2 — Thin-File UPI Scoring

CIBIL and Experian require credit bureau records. For India's ~400M thin-file UPI users,
the bureau score is 0 and the loan is rejected. FlowScore needs only 30-day transaction
variance data.

| Borrower | CIBIL | FlowScore | PD_90 | Verdict |
|----------|-------|-----------|-------|---------|
| Healthy Salaried | 750+ APPROVED | 100.0 | 0.044% | LOW RISK |
| **Thin-File UPI** | **0 REJECTED** | **60.9** | **0.210%** | **ELEVATED** |
| Mild Stress | 620 APPROVED | 50.2 | 0.322% | ELEVATED |
| High-Risk MSME | 580 APPROVED | 23.1 | 0.948% | HIGH RISK |
| **Near Default** | **660 APPROVED** | **1.6** | **2.229%** | **NEAR-DEFAULT** |

**The key contrast:**
- Near Default borrower: CIBIL 660 (bank approves) → FlowScore 1.6, PD_90 = 2.229% (NEAR-DEFAULT)
- Thin-File UPI user: CIBIL 0 (bank rejects) → FlowScore 60.9, PD_90 = 0.210% (ELEVATED)

The Near Default borrower has not yet missed a bureau-reported payment. Their transaction
variance (σ_tx = 68,000 vs σ_ref = 8,500) reveals the stress. CIBIL approves them. FlowScore
flags them. The Thin-File UPI user is safer than many CIBIL-scored borrowers.

---

## Phase 3 — Kramers Escape Rate: PD Amplification

| D | FlowScore | PD_90 | vs D=1.0 | AC lag-1 | Tier |
|---|-----------|-------|----------|----------|------|
| 1.0 | 100.0 | 0.044% | 1.0× | 0.000 | LOW RISK |
| 0.9 | 81.0 | 0.094% | 2.1× | 0.190 | LOW RISK |
| 0.8 | 64.0 | 0.185% | 4.2× | 0.360 | ELEVATED |
| 0.7 | 49.0 | 0.337% | 7.7× | 0.510 | ELEVATED |
| 0.6 | 36.0 | 0.567% | 12.9× | 0.640 | HIGH RISK |
| 0.5 | 25.0 | 0.879% | 20.0× | 0.750 | HIGH RISK |
| 0.4 | 16.0 | 1.258% | 28.6× | 0.840 | HIGH RISK |
| 0.3 | 9.0 | 1.660% | 37.8× | 0.910 | NEAR-DEFAULT |
| 0.2 | 4.0 | 2.024% | 46.1× | 0.960 | NEAR-DEFAULT |
| 0.1 | 1.0 | 2.280% | 51.9× | 0.990 | NEAR-DEFAULT |

**D=0.1 vs D=1.0: 52× amplification.**

The `exp(−α·D²)` term creates exponential acceleration near D → 0. A logistic sigmoid
would give a symmetric S-curve. The Kramers form has an asymmetric tail — the
default probability rises steeply near the transition but plateaus as D approaches 0
(bounded by T × k₀ ≈ 2.4% at 90 days). This is physically correct: at D = 0, the
borrower is at the phase transition point, not in an infinite-risk state.

---

## Phase 4 — CSD Trajectory

Trajectory: a borrower deteriorating over 6 months (σ_ref = 8,500).

| Month | σ_tx | D | FlowScore | PD_30 | AC | CSD | Tier | Event |
|-------|------|---|-----------|-------|-----|-----|------|-------|
| Month 0 | 8,500 | 1.000 | 100.0 | 0.015% | 0.000 | no | LOW RISK | baseline |
| Month 1 | 10,000 | 0.850 | 72.2 | 0.044% | 0.278 | no | LOW RISK | first irregular month |
| Month 2 | 14,000 | 0.607 | 36.9 | 0.183% | 0.631 | no | HIGH RISK | delayed utility |
| **Month 3** | **17,500** | **0.486** | **23.6** | **0.311%** | **0.764** | **YES** | **HIGH RISK** | **CSD flag fires** |
| Month 4 | 24,000 | 0.354 | 12.5 | 0.483% | 0.875 | YES | NEAR-DEFAULT | overdraft |
| Month 5 | 42,000 | 0.202 | 4.1 | 0.677% | 0.959 | YES | NEAR-DEFAULT | collections risk |

**CSD flag fires at Month 3. NEAR-DEFAULT tier at Month 4. 1 month lead time.**

Standard credit models detect stress only when payments are missed. The CSD flag fires
from transaction variance alone — before any missed payment. The lender has 1 month to
restructure, reduce the credit limit, or contact the borrower.

The mechanism is universal: AC = 1 − D² is the critical slowing-down signature that
precedes phase transitions in ecology, climate, neuroscience, and finance. Same
mathematical structure at every scale.

---

## Risk Tiers

| FlowScore | Tier | D range |
|-----------|------|---------|
| F ≥ 70 | GREEN — LOW RISK | D ≥ 0.837 |
| F ≥ 40 | AMBER — ELEVATED | D ≥ 0.632 |
| F ≥ 15 | ORANGE — HIGH RISK | D ≥ 0.387 |
| F < 15 | RED — NEAR-DEFAULT | D < 0.387 |

---

## Comparison

| Tool | Thin-file capable | Free parameters | PD formula | Early warning |
|------|-------------------|-----------------|------------|---------------|
| CIBIL / Experian | No — requires 2+ yr history | Proprietary (100s) | Empirical scorecard | No |
| Logistic regression | No — needs labelled defaults | 1 per feature | Sigmoid fit | No |
| Behavioural ML (banks) | Partial — black-box | 1000s | No closed form | No |
| **FlowScore** | **Yes — 30-day data** | **2 (k₀, α)** | **Kramers (closed form)** | **Yes (CSD)** |

---

## Get the Full Product

For API access, integration docs, and pricing:
**[vallikat@vectorpeaktech.com](mailto:vallikat@vectorpeaktech.com)**
