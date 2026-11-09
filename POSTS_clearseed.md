# ClearSeed — Post Copy

---

## LinkedIn

```
When a regulator asks to verify your stress test scenarios, what do you hand them?

Under Basel IV FRTB and CCAR, banks submit scenario matrices for capital
calculation. The regulator sees the outputs. But the random sequence that
produced those scenarios — the internal state of the system PRNG — is not
part of the submission. The regulator cannot independently replay it.

ClearSeed solves this with a different construction. Instead of a system
PRNG, it generates scenarios from Legendre symbols over odd primes — a
number-theoretic function with one property that matters here: given only
the integer seed, the output is completely deterministic and reproducible.
The seed is the complete audit key. Any regulator with the seed can replay
the exact scenario matrix, byte-for-byte, without access to the original
system.

The equidistribution guarantee (the property that makes the scenarios
statistically valid) is proved unconditionally from the Pólya-Vinogradov
inequality — not measured from samples. Five independent checks are computed
for every seed and attached as a certificate.

Benchmark covers FRTB IMA (250 scenarios, 10 factors), CCAR Severely Adverse
(500 scenarios, 8 factors), XVA CVA (1,000 scenarios), and ICAAP Pillar 2
(2,000 scenarios). Pure Python, no dependencies.
[link to repo]

The question it answers: if your capital calculation is ever audited, can
you hand the regulator a single number and let them verify everything?
```

---

## Reddit — r/quant or r/algotrading

**Title:**
```
Legendre-symbol PRG for regulatory scenario generation — deterministic replay from integer seed, equidistribution proved unconditionally (pure Python benchmark)
```

**Body:**
```
Built a benchmark for a scenario generation approach that addresses a gap in standard FRTB/CCAR submissions: regulatory audit replay.

**The problem with system PRNGs for regulatory capital:**

Under Basel IV IMA and CCAR stress testing, banks submit scenario matrices for capital calculation. The regulator sees the outputs. The internal PRNG state that produced them is not part of the submission. If a regulator asks to independently verify the scenario generation, a system PRNG submission cannot satisfy the request — you'd need to preserve and hand over the full internal RNG state.

**The ClearSeed construction:**

```
bit_i = (Legendre(seed + pos + 1, p_{pos mod K}) + 1) / 2
```

The integer seed is the complete state. No internal variables. Any party with the seed can replay the exact scenario matrix:

```
System PRNG (run 1):  Scenario[0][0] =  0.73821  — state-dependent, non-reproducible
System PRNG (run 2):  Scenario[0][0] = -0.14209  — different output
ClearSeed (run 1):    Scenario[0][0] = -0.57735  — seed=20260101
ClearSeed (run 2):    Scenario[0][0] = -0.57735  — byte-identical
```

**Equidistribution certificate (5 checks per seed):**

| Check | Threshold | Seed 20260101 | Result |
|---|---|---|---|
| Frequency balance | \|freq−0.5\| < 0.03 | 0.000500 | PASS |
| Pólya-Vinogradov | \|Σχ_p\| < √N·logN | 0.142857 | PASS |
| Chi-squared pairs | χ² < 15 | 2.4040 | PASS |
| Shannon entropy | H > 0.99 bits/bit | 0.999971 | PASS |
| Cross-prime indep | Pearson r < 0.10 | 0.014123 | PASS |

The Pólya-Vinogradov check proves equidistribution directly from the distribution of quadratic residues — not from sampling. The guarantee is unconditional.

Benchmark covers FRTB IMA, CCAR, XVA CVA, Historical VaR, ICAAP Pillar 2. Pure Python, zero dependencies:

https://github.com/rfdevuser/vectorpeak-experiments

Interested whether anyone in quant risk has worked on audit-replay requirements in FRTB IMA submissions — specifically whether regulators are starting to request this.
```

---

## Discord — quant / fintech communities `#showcase`

```
Built a benchmark for regulatory scenario generation using Legendre symbols instead of a system PRNG.

The core property: the integer seed is the complete state. No internal PRNG variables. Given the seed, any regulator can replay the exact scenario matrix byte-for-byte. System PRNGs can't do this — the internal state that produced the scenarios isn't part of the submission.

Five equidistribution checks per seed (frequency balance, Pólya-Vinogradov, chi-squared, Shannon entropy, cross-prime independence). The PV check proves equidistribution unconditionally — not empirically.

Covers FRTB IMA, CCAR, XVA CVA, VaR, ICAAP Pillar 2. Pure Python, zero dependencies:
https://github.com/rfdevuser/vectorpeak-experiments

Posting here because Basel IV audit replay requirements are starting to come up. Curious whether others have hit this in practice.
```

---

## X / Twitter — 4-tweet thread

**Tweet 1 (hook — attach terminal screenshot or GIF):**
```
A bank submits stress test scenarios to the regulator.

The regulator asks: can you reproduce this exact sequence?

With a system PRNG: no. The internal state that generated it isn't saved.

With ClearSeed: the integer seed IS the complete state. 🧵
```

**Tweet 2 (the construction):**
```
ClearSeed generates scenario bits from Legendre symbols over odd primes:

  bit_i = (Legendre(seed + i, p_{i mod K}) + 1) / 2

No internal state. The seed is everything.

Run it twice with seed=20260101 → identical output, byte-for-byte.
Run a system PRNG twice → different output every time.
```

**Tweet 3 (the certificate):**
```
Equidistribution isn't just measured from samples — it's proved.

The Pólya-Vinogradov inequality gives an unconditional upper bound on
|Σ χ_p(n)| / (√N · log N) → 0.

The certificate runs 5 independent checks.
Every regulatory seed ships with one.

FRTB, CCAR, XVA, ICAAP — same guarantee, different parameters.
```

**Tweet 4 (the link):**
```
Pure Python. Zero dependencies. Covers 5 regulatory frameworks.

The benchmark shows the gap between system PRNGs and a certified
deterministic engine on the one property regulators actually care about:
can you hand me a number and let me verify everything myself?

[repo]
```
