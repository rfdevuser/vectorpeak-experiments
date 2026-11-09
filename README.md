# VectorPeak Experiments

Standalone benchmark scripts for VectorPeak products.
Each script runs with no API key and minimal or no dependencies.

---

| Benchmark | Script | Product | Dependencies |
|---|---|---|---|
| [Negation Trap](README_structuraldb.md) | `run_benchmark.py` | StructuralDB | `sentence-transformers numpy` |
| [Canonical Vision Operator](README_cvo.md) | `run_cvo_benchmark.py` | VisionCore | `numpy scipy` |
| [Vulnerability Percolation](README_breachguard.md) | `run_breachguard_benchmark.py` | BreachGuard | none |

---

## Quick run

```bash
git clone https://github.com/rfdevuser/vectorpeak-experiments
cd vectorpeak-experiments

# StructuralDB — negation trap in vector state management
pip install sentence-transformers numpy
python run_benchmark.py

# VisionCore — illumination invariance + adversarial stability
pip install numpy scipy
python run_cvo_benchmark.py

# BreachGuard — CVSS vs percolation rank mismatch
python run_breachguard_benchmark.py
```

---

## What each benchmark demonstrates

**StructuralDB** — cosine similarity assigns high scores to polar-opposite
decisions for the same entity. StructuralDB blocks the contradiction at
write time: zero tokens, zero false positives, microseconds.

**VisionCore** — the Canonical Vision Operator (CVO) front-end is exactly
invariant to multiplicative brightness changes and structurally stable under
L∞ adversarial perturbations. Zero learned weights. Closed-form constants only.

**BreachGuard** — the highest-CVSS vulnerability is not the one whose
exploitation triggers a network cascade. Γ₄₃ (Molloy-Reed percolation)
ranks patches by cascade threshold improvement. On a 20-node corporate
network, the Γ₄₃-ranked patch delivers 8.4× more cascade resilience than
the CVSS-ranked patch using the same single remediation budget.

---

For API access, integration docs, and pricing:
**[vallikat@vectorpeaktech.com](mailto:vallikat@vectorpeaktech.com)**
