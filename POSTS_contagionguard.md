# ContagionGuard — Post Copy

---

## LinkedIn

```
Every major bank stress test — Basel DFAST, CCAR, SRISK — ranks systemic risk by
balance-sheet size, regression coefficients, or scenario VaR.

None of them tell you the exact stability threshold.

ContagionGuard does.

ρ(W) = spectral radius of the normalised bilateral exposure matrix.
γ_c  = 1/ρ(W)  — the network is provably stable if and only if ρ(W) < 1.

This isn't a risk score. It's a certified phase transition point.

In the Eurozone stress network (FR1, DE1, IT1, ES1, GR1, PT1, NL1):

  ρ(W) = 1.0475  → CRITICAL
  Most systemic bank (Perron rank #1): ES1 — Banco España, 200B assets

The regulator heuristic says: recapitalise FR1 first (600B, largest by assets).
ContagionGuard says: inject into ES1.

Same 2.5B capital:
  → Into FR1: ρ(W) = 1.0230. Still CRITICAL. Capital wasted.
  → Into ES1: ρ(W) = 0.9777. VULNERABLE. ρ < 1 threshold crossed.

The Perron vector of W identifies the structural amplifier — the node whose
outgoing exposure (W[ES1→FR1] = 0.60, W[ES1→DE1] = 0.50) drives the feedback
loop. That's not visible from a balance sheet. It's a network eigenvalue.

Benchmark (pure Python + numpy):
[link to repo]
```

---

## Reddit — r/MachineLearning or r/quant

**Title:**
```
Interbank contagion benchmark: spectral radius of exposure matrix vs SRISK/CoVaR. Pure Python + numpy.
```

**Body:**
```
Built a standalone benchmark for a spectral-radius-based systemic risk tool.
Posting because the Perron-vector amplifier result is non-obvious and I want
to know if there's prior work on it.

**Setup:**

Given banks B₁...Bₙ with bilateral exposures E[i,j] (bank i lends E[i,j] to j),
the normalised exposure matrix is W[i,j] = E[i,j] / equity_i.

Spectral radius ρ(W) = max|λ| (Perron-Frobenius dominant eigenvalue).
γ_c = 1/ρ(W) — the network is linearly stable iff ρ(W) < 1.

**Phase 2 result (Eurozone stress):**

Balance-sheet ranking: FR1 (600B) > DE1 (550B) > IT1 (350B) > NL1 (350B) > ES1 (200B)

Perron-vector ranking: ES1 (#1) > FR1 (#2) > DE1 (#3) > NL1 (#4) > IT1 (#5)

ES1 is Perron rank #1 despite being asset rank #5. The reason: ES1's normalised
outgoing exposure sum = W[ES1→FR1] + W[ES1→DE1] = 0.60 + 0.50 = 1.10 > 1.
ES1 is feeding back into FR1 and DE1 more than its equity can absorb.

**Phase 4 result (capital injection):**

Same 2.5B capital:
→ Into FR1 (asset rank #1): ρ drops from 1.0475 to 1.0230. Still CRITICAL.
→ Into ES1 (Perron rank #1): ρ drops from 1.0475 to 0.9777. ρ < 1 threshold crossed.

**The claim:**

The minimum capital injection to certify stability must target the Perron-vector
amplifier. Balance-sheet size is the wrong ranking criterion.

Has this been formalised elsewhere? I've seen Eisenberg-Noe and Acemoglu-Ozdaglar
networks, but I haven't seen the Perron-vector targeting result stated this cleanly.

Benchmark: https://github.com/rfdevuser/vectorpeak-experiments
```

---

## Discord — `#fintech` / `#ml-finance` / `#showcase`

```
Posted a spectral-risk benchmark for interbank networks.

ρ(W) = spectral radius of the normalised bilateral exposure matrix.
If ρ < 1: provably stable. If ρ > 1: contagion-critical. No fitting.

Four phases:

1. Five presets (stable → critical): ρ, γ_c, Fiedler μ₂, risk score
2. Perron vector vs balance sheet — ES1 is the structural amplifier despite being
   5th largest by assets
3. Cascade containment: STABLE network (ρ=0.25) → cascade 1/5; CRITICAL (ρ=1.12) → 5/5
4. Capital injection: +2.5B to ES1 certifies ρ<1; +2.5B to FR1 stays CRITICAL

The cascade containment phase is the clearest: same bilateral structure, different
ρ, completely different cascade behaviour.

https://github.com/rfdevuser/vectorpeak-experiments
```

---

## X / Twitter — 4-tweet thread

**Tweet 1 (hook):**
```
Every bank stress test ranks systemic risk by balance-sheet size.

ContagionGuard ranks by ρ(W) — the spectral radius of the bilateral
exposure matrix.

Eurozone stress network (7 banks): the most dangerous bank is NOT
the largest by assets. It's 5th largest. 🧵
```

**Tweet 2 (the result):**
```
Eurozone stress — 7 banks, ρ(W) = 1.0475 (CRITICAL)

Balance-sheet rank:  FR1 > DE1 > IT1 > NL1 > ES1 > GR1 > PT1
Perron-vector rank:  ES1 > FR1 > DE1 > NL1 > IT1 > PT1 > GR1

ES1 divergence: +4 ranks more systemic than size implies.

Why? W[ES1→FR1] = 0.60, W[ES1→DE1] = 0.50. Row sum = 1.10 > 1.
ES1 feeds back into the two largest banks at > 100% of its equity.
```

**Tweet 3 (the capital injection proof):**
```
Capital injection test — which bank to recapitalise?

Same 2.5B:
→ FR1 (asset rank #1): ρ = 1.0475 → 1.0230. Still CRITICAL.
→ ES1 (Perron rank #1): ρ = 1.0475 → 0.9777. ρ < 1. ✓

The Perron-vector amplifier is the minimum-cost structural fix.
Targeting balance-sheet size wastes the intervention budget.
```

**Tweet 4 (the link):**
```
Benchmark: 4 phases
  1. Five network presets — spectral certificates
  2. Perron rank vs asset rank — ES1 divergence
  3. Eisenberg-Noe cascade: STABLE (1/5) vs CRITICAL (5/5)
  4. Capital injection lever — minimum ρ<1 cost

numpy, ~300 lines:
[repo link]
```
