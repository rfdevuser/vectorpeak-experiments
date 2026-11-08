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

### Quickstart

```bash
git clone https://github.com/rfdevuser/vectorpeak-experiments
cd vectorpeak-experiments
pip install sentence-transformers numpy
python run_benchmark.py
```

No API key required. `sentence-transformers` downloads `all-MiniLM-L6-v2`
on first run (~90 MB, one-time). After that it runs fully offline.

**Optional — add OpenAI 1536d / 3072d comparison:**

```bash
pip install openai
export OPENAI_API_KEY=sk-...
python run_benchmark.py
```

---

### What it shows

```
$ python run_benchmark.py

═══════════════════════════════════════════════════════════════════
  STRUCTURALDB NEGATION TRAP BENCHMARK
═══════════════════════════════════════════════════════════════════
  Retrieval threshold : cosine > 0.80

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
  Writing State A (+1) to coordinate (depth=2, parent="tx_1042")...
  [COMMITTED] (18.4 µs | 180 bytes | hash=...)

  Writing State B (-1) to coordinate (depth=2, parent="tx_1042")...
  [INTERCEPTED] AntiNegationConflictError:
    Cannot write SIGN=-1 over active SIGN=+1 at (depth=2, parent='tx_1042').

  Downstream cost (StructuralDB path):
    Latency             : 1.3 µs
    State payload size  : 180 bytes
    Downstream Tokens   : 0
    False Positives     : 0

═══════════════════════════════════════════════════════════════════
  Vector DB : contradictions retrievable at >0.80 similarity.
  StructuralDB : 0 tokens burned. 0 false positives. Microseconds.
═══════════════════════════════════════════════════════════════════
```

---

### Multi-model summary (with OpenAI API key)

When `OPENAI_API_KEY` is set, the benchmark also runs
`text-embedding-3-small` (1536d) and `text-embedding-3-large` (3072d)
and prints a comparison table:

| Model | Dim | Q↔A | Q↔B | A↔B | Result |
|---|---|---|---|---|---|
| all-MiniLM-L6-v2 | 384 | 0.88 | 0.87 | 0.91 | FAIL |
| text-embedding-3-small | 1536 | 0.87 | 0.86 | 0.92 | FAIL |
| text-embedding-3-large | 3072 | 0.88 | 0.87 | 0.93 | FAIL |

Higher dimensions increase mutual A↔B similarity — the trap gets worse,
not better, as the model gets bigger. This defeats the most common
objection: *"just use a better embedding model."*

---

### Why both states score high

Both documents describe **the same entity** (Transaction #1042, same
parties, same context). Only the verdict word differs. In embedding
space, both documents land close to any query about that entity — the
shared context dominates the similarity score.

This is not a model quality issue. It is a category error:

> **Cosine similarity is a distance metric, not a logical consistency
> check.** No embedding model, however large, can fix it, because the
> problem is in the retrieval primitive, not the embedding quality.

---

### How StructuralDB blocks the contradiction

StructuralDB models state as a **p-adic ultrametric tree**. Each node
carries a sign (`+1` = assert, `-1` = negate). The anti-negation
enforcer checks one constraint before every write:

> No two active nodes at the same `(depth, parent)` position may carry
> opposite signs.

This is O(n) over siblings at the same position — O(1) in practice for
narrow state trees. When the constraint fires, the write is rejected
in microseconds and the database stays consistent. The contradiction
never exists. The LLM agent sees exactly one authoritative state and
burns zero tokens on disambiguation.

**The StructuralDB in this script is an in-memory stub** that faithfully
implements the anti-negation rule. The full production system adds:

- Persistent storage with SQLite WAL backend
- SHA-256 hash-chain audit log (every state transition is cryptographically
  provable — required for financial and healthcare compliance)
- ~200 bytes per node (vs 3–12 KB for a vector embedding)
- Causal BFS path queries across the state tree
- API access for integration with any LLM agent framework

---

### Where to use StructuralDB

Any system where an LLM agent reads state and acts on it:

- **Trade processing** — APPROVED / REJECTED / PENDING cannot coexist
- **Loan origination** — compliance flags must not contradict approvals
- **Clinical workflows** — treatment states must be unambiguous
- **Access control** — GRANT and DENY cannot both be active
- **Incident management** — OPEN and RESOLVED are mutually exclusive

If a wrong state costs real money or carries regulatory liability,
StructuralDB replaces the vector retrieval layer for authoritative state.

---

### Get the full product

For API access, integration docs, and pricing:

**[vallikat@vectorpeaktech.com](mailto:vallikat@vectorpeaktech.com)**

---

© VectorPeak Technologies
