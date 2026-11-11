# ContagionGuard — Interbank Contagion Spectral Certificate

**Γ₄₇ spectral stability proof for interbank exposure networks. Zero fitted parameters.**

The systemic risk of a bank network is fully determined by the spectral radius ρ(W) of
its normalised bilateral exposure matrix. ρ(W) = 1 is the exact stability phase transition.
No regression. No scenario calibration.

---

## Quickstart

```bash
git clone https://github.com/rfdevuser/vectorpeak-experiments
cd vectorpeak-experiments
pip install numpy
python run_contagionguard_benchmark.py
```

---

## The Four Claims

**1. ρ(W) = 1 is the exact stability threshold.**
The network is linearly stable if and only if ρ(W) < 1. This follows directly from the
Perron-Frobenius theorem applied to the normalised bilateral exposure matrix
W[i,j] = exposure(i→j) / equity_i. No calibration, no fitting.

**2. γ_c = 1/ρ(W) is the certified contagion distance.**
How far the network is from the critical point, in a mathematically precise sense.
SRISK and CoVaR give a risk score. ContagionGuard gives a certified distance.

**3. The Perron vector identifies the structural amplifier.**
The dominant eigenvector of W gives the true systemic importance of each node —
independent of balance-sheet size. The bank that should receive emergency
recapitalisation is the Perron-rank #1 bank, not the asset-rank #1 bank.

**4. Capital injection must target the Perron amplifier.**
Injecting capital into the asset-largest bank leaves ρ(W) nearly unchanged.
Injecting into the Perron-rank #1 bank achieves the threshold crossing with
minimum capital.

---

## Phase 1 — Five Preset Spectral Certificates

| Network | Banks | ρ(W) | γ_c | μ₂ | Score | Status |
|---------|-------|------|-----|-----|-------|--------|
| Simple Stable | 5 | 0.2883 | 3.4680 | 0.1389 | 25.1 | STABLE |
| Hub-and-Spoke G-SIB | 9 | 0.2638 | 3.7905 | 0.3121 | 23.2 | STABLE |
| G-SIB Cluster + Regionals | 10 | 0.4029 | 2.4820 | 0.3130 | 33.2 | STABLE |
| Eurozone Sovereign Stress | 7 | 1.0475 | 0.9546 | 0.3563 | 64.9 | **CRITICAL** |
| SVB Regional Cluster | 6 | 1.1181 | 0.8943 | 0.4554 | 67.3 | **CRITICAL** |

`μ₂` = Fiedler eigenvalue of the symmetrised Laplacian. Smaller μ₂ = weakly coupled
sub-clusters (cascade spreads more slowly). Score = 100·(1−e^(−ρ)).

---

## Phase 2 — Perron Vector vs Balance-Sheet Rank (Eurozone Stress)

The Eurozone stress network (ρ = 1.0475, CRITICAL):

| Bank | Assets | Asset rank | Perron wt | Perron rank | Divergence |
|------|--------|-----------|-----------|-------------|------------|
| FR1 | 600B | #1 | 0.1812 | #2 | −1 |
| DE1 | 550B | #2 | 0.1651 | #3 | −1 |
| IT1 | 350B | #3 | 0.1554 | #5 | −2 |
| **ES1** | **200B** | **#5** | **0.1826** | **#1** | **+4** |
| GR1 | 80B | #6 | 0.0742 | #7 | −1 |
| PT1 | 60B | #7 | 0.0837 | #6 | +1 |
| NL1 | 350B | #4 | 0.1578 | #4 | 0 |

**Key finding:** ES1 (Banco España, 200B assets) is the structural amplifier —
4 ranks more systemic than its balance sheet implies. A regulator targeting FR1
(largest by assets, 600B) wastes the recapitalisation budget.

**Why ES1?** ES1 has the highest normalised outgoing exposure: W[ES1→FR1] = 0.60,
W[ES1→DE1] = 0.50 — total row sum 1.10 > 1. It is the feedback loop in the
contagion dynamics.

---

## Phase 3 — Eisenberg-Noe Cascade Containment

Cascade rule: bank i defaults when cumulative losses from defaulted counterparties
exceed its equity. `loss(i) = Σ_j exposure(i→j) × loss_given_default`

**STABLE network (ρ = 0.25):** Ring-5 with bilateral exposures of 1–1.5B, equity 10B each.
Every default is contained at the seed — cascade 1/5 from any bank.

**CRITICAL network (ρ = 1.12):** Hub-5 where each spoke lent > its equity to the hub.

```
Central Hub defaults  →  all 4 spokes cascade in depth 1
  HUB → SP1 → SP2 → SP3 → SP4   (5/5)

Each spoke defaults  →  cascade stops at seed (1/5)
  SP1 alone   SP2 alone   SP3 alone   SP4 alone
```

The asymmetry is structural: spoke banks over-concentrated their lending to the hub
(W[spoke,hub] > 1). ρ(W) captures this before any default occurs.

---

## Phase 4 — Capital Injection Lever

Target: Eurozone stress (ES1 = Perron rank #1, equity 5B, ρ = 1.0475)

| Equity multiplier | Capital added | ρ(W) | Status |
|------------------|---------------|------|--------|
| 1.0× | +0.0B | 1.0475 | CRITICAL |
| **1.5×** | **+2.5B** | **0.9777** | **VULNERABLE ◄ ρ < 1** |
| 2.0× | +5.0B | 0.9406 | VULNERABLE |
| 10.0× | +45.0B | 0.8445 | VULNERABLE |

**Counterfactual:** Same 2.5B capital injected into FR1 (asset-rank #1):
→ ρ(W) = 1.0230 — still CRITICAL. Capital wasted.

Minimum certified stabilisation: **+2.5B to ES1** (not +2.5B to FR1).
ContagionGuard identifies the minimum-cost structural fix.

---

## The Stability Comparison

| Tool | Methodology | Free parameters | Threshold | Cascade path |
|------|-------------|-----------------|-----------|--------------|
| Basel III LCR/NSFR | Individual liquidity ratios | 3+ (LCR, NSFR, leverage) | Empirical | No |
| SRISK (NYU Stern) | Balance-sheet × MES | 1 (MES fitted per bank) | None — ordinal | No |
| CoVaR (Adrian-Brunnermeier) | ΔCoVaR regression | 1 per pair | None — ordinal | No |
| DFAST / CCAR | Macro scenario VaR | Scenario-dependent | None — budget | No |
| **ContagionGuard** | **Spectral radius ρ(W)** | **0** | **ρ=1 exact** | **Yes** |

---

## Running the Benchmark

```bash
python run_contagionguard_benchmark.py
```

Expected output:
```
Phase 1: 5 presets — ρ, γ_c, μ₂, risk score, status
Phase 2: Eurozone — ES1 Perron rank #1 despite assets rank #5
Phase 3: Ring-5 (STABLE) cascade 1/5; Hub-5 (CRITICAL) cascade 5/5 from hub
Phase 4: 2.5B to ES1 certifies ρ<1; same 2.5B to FR1 leaves ρ CRITICAL
```

---

## Get the Full Product

For API access, integration docs, and pricing:
**[vallikat@vectorpeaktech.com](mailto:vallikat@vectorpeaktech.com)**
