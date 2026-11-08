# VectorPeak Experiments

Standalone benchmark scripts for VectorPeak research and demos.

---

## Negation Trap Benchmark

**File:** `run_benchmark.py`

Demonstrates the core flaw in cosine-similarity state management: even
enterprise-grade embedding models (384d → 3072d) assign high cosine similarity
to polar-opposite decisions for the same entity. StructuralDB blocks the same
contradiction at write time — zero tokens burned, zero false positives.

---

### What it shows

```
$ python run_benchmark.py

══════════════════════════════════════════════════════════════════
  STRUCTURALDB NEGATION TRAP BENCHMARK
══════════════════════════════════════════════════════════════════

[PHASE 1: Continuous Vector Space (The Negation Trap)]
Model: sentence-transformers/all-MiniLM-L6-v2 (384d)
  (+) State A: "Transaction #1042 status: APPROVED by Compliance ..."
  (-) State B: "Transaction #1042 status: REJECTED by Compliance ..."
  Query:       "What is the authoritative state of Transaction #1042?"

  Cosine Similarity (Query <-> State A) : 0.88xx
  Cosine Similarity (Query <-> State B) : 0.87xx
  Mutual Cosine Similarity  (A  <->  B) : 0.91xx

  [FAILURE] Both polar-opposite states pass retrieval threshold (>0.80).
           Result: Non-deterministic agent state resolution.

  Downstream cost (vector path):
    Contradictory passages injected into LLM context : ~620 tokens
    Per disambiguation call (gpt-4o $5/M)           : ~$0.0031
    At 100 conflicts/day                             : ~$0.31/day wasted

[PHASE 2: StructuralDB Discrete State Lattice]
  Writing State A (+1) to coordinate (depth=2, parent="tx_1042")... [COMMITTED] (18.4 µs | 198 bytes | hash=...)
  Writing State B (-1) to coordinate (depth=2, parent="tx_1042")...
  [INTERCEPTED] AntiNegationConflictError:
    Cannot write SIGN=-1 over active SIGN=+1 at (depth=2, parent='tx_1042').

  Downstream cost (StructuralDB path):
    Latency             : 12.1 µs
    State payload size  : 198 bytes
    Downstream Tokens   : 0
    False Positives     : 0
```

---

### Why both states score high

Both documents describe **the same trade** (Transaction #1042, same parties,
same context). Only the verdict word differs. In embedding space, both
documents land close to any query about that trade — the shared context
dominates the similarity score. The similarity gap between APPROVED and
REJECTED can be as small as 0.01–0.03 depending on the model and phrasing.

This is not a model quality issue. It is a category error: cosine similarity
is a **distance metric**, not a **logical consistency check**. No embedding
model, however large, can fix it, because the problem is in the retrieval
primitive, not the embedding quality.

---

### Multi-model summary (with OpenAI API key set)

| Model | Dim | Q↔A | Q↔B | A↔B | Result |
|---|---|---|---|---|---|
| all-MiniLM-L6-v2 | 384 | 0.88 | 0.87 | 0.91 | FAIL |
| text-embedding-3-small | 1536 | 0.87 | 0.86 | 0.92 | FAIL |
| text-embedding-3-large | 3072 | 0.88 | 0.87 | 0.93 | FAIL |

Higher dimensions increase mutual A↔B similarity — the trap gets worse,
not better, as the model gets bigger.

---

### Installation

```bash
# Clone
git clone https://github.com/rfdevuser/vectorpeak-experiments
cd vectorpeak-experiments

# Install (local model, no API key needed)
pip install sentence-transformers numpy

# Optional: OpenAI comparison (1536d / 3072d)
pip install openai
export OPENAI_API_KEY=sk-...

# Run
python run_benchmark.py
```

---

### How StructuralDB blocks the contradiction

StructuralDB models state as a **p-adic ultrametric tree**. Each node carries
a sign (`+1` = assert, `-1` = negate). The anti-negation enforcer checks one
constraint before every write:

> No two active nodes at the same `(depth, parent)` position may carry
> opposite signs.

This is O(n) over siblings at the same position — O(1) in practice for
narrow state trees. When the constraint fires, the write is rejected
instantly and the database remains consistent. The contradiction never
exists. The LLM agent sees exactly one authoritative state.

---

### Extending the benchmark

The StructuralDB in this script is an in-memory stub that faithfully
implements the anti-negation rule. To run against the full StructuralDB
product (persistent, distributed, hash-chain audit log), replace the stub
calls with the StructuralDB API client.

---

© VectorPeak Technologies
