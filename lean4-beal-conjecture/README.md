# Lean 4 — Conditional Formalisation of Beal's Conjecture

Mathlib 4.36 · Lean 4

## Files

| File | Sorry | Axioms | Description |
|------|-------|--------|-------------|
| `BealCurve.lean` | 0 | 1 | Frey-Beal discriminant arithmetic; BC.3 multiplicative reduction |
| `BealModularity.lean` | 0 | 6 | Modularity, Ribet, Mazur, Swan, CM classification, Serre axioms |
| `BealMainTheorem.lean` | 1 | 0 | Full assembly; sorry pending Galois rep infrastructure in Mathlib |
| `MasonStothers.lean` | 0 | 0 | Polynomial ABC (Mason–Stothers) and FLT for polynomials — Mathlib primitives only |
| `BSDrZero.lean` | 0 | 4 | Strong BSD rank-zero (Kato + Skinner–Urban + Kobayashi + adelic assembly) |

## Axiom inventory

All 7 named axioms are proved theorems in the mathematical literature, not yet formalised in Mathlib 4.36:

| Lean name | Reference |
|-----------|-----------|
| `multiplicative_reduction_criterion` | Silverman, ATAEC, Prop. VII.5.1 |
| `axiom_modularity` | Breuil–Conrad–Diamond–Taylor 2001 |
| `axiom_ribet_level_lowering` | Ribet 1990, Invent. Math. 100 |
| `axiom_mazur_no_isogeny` | Mazur 1978, Invent. Math. 44 |
| `axiom_swan_conductor_bound` | Serre, Local Fields, Ch. VI |
| `axiom_two_power_newforms_cm` | LMFDB + Cohen–Strömberg |
| `axiom_serre_surjectivity` | Serre 1972, Invent. Math. 15 |
| `C1_KatoUpperBound` | Kato, Astérisque 295 (2004) |
| `C2_SkinnerUrbanIMC` | Skinner–Urban, Inventiones 195 (2014) |
| `C3_KobayashiPM` | Kobayashi, Inventiones 152 (2003) |
| `AdelicAssembly` | Hasse (1930); Tate's thesis (1950) |

## The one sorry

`beal_conjecture` in `BealMainTheorem.lean` has a single `sorry` at step (2–8). The missing piece is Galois representation infrastructure: types for `ρ̄_{E,ℓ}`, the modularity lifting theorem, and Ribet's level-lowering theorem in Lean 4. This is under active development in the [FLT project](https://leanprover-community.github.io/flt-regular/).
