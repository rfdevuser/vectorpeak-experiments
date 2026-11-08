# VectorPeak Experiments

Standalone benchmark scripts for VectorPeak research and demos.

---

## Negation Trap Benchmark

**File:** `negation_trap_benchmark.py`

Demonstrates the core flaw in vector-similarity state management: a vector
store can return contradictory decisions (APPROVED + REJECTED) at high
cosine similarity simultaneously. StructuralDB blocks the same contradiction
at write time with a `ConflictingStateError` — zero re-planning cost.

### What it shows

| Engine | Contradiction | LLM re-plan cost | Safe to act? |
|---|---|---|---|
| Vector DB (cosine) | ✗ Both APPROVED and REJECTED returned at ~0.91 similarity | ~14,000 tokens | No |
| StructuralDB | ✓ ConflictingStateError raised in < 1 ms | 0 tokens | Yes |

### Dependencies

No external databases required. The benchmark runs fully in-memory.

```bash
pip install numpy   # only if you want to extend with real embeddings
```

The core script uses only the Python standard library (`math`, `hashlib`,
`time`). `numpy` is listed for completeness if you wire in a real embedding
model.

### Run

```bash
python negation_trap_benchmark.py
```

### Expected output

```
=================================================================
  NEGATION TRAP BENCHMARK
  StructuralDB vs. Vector Similarity State Management
=================================================================

[1/3] Seeding state engines with trade decisions...

  StructuralDB: wrote APPROVED (id=1, sign=+1)

[2/3] Querying with ambiguous trade signal...

  Query: 'Trade with partial doc failure, otherwise approved profile'

  ┌─ Vector DB results (top-2 by cosine similarity) ──────────────┐
  │  [0.9xxx]  APPROVED    Trade T-2024-001: APPROVED — credit ...
  │  [0.9xxx]  REJECTED    Trade T-2024-001: REJECTED — document...
  └────────────────────────────────────────────────────────────────┘

  ⚠  CONFLICT DETECTED IN VECTOR RESULTS:
      APPROVED  similarity = 0.9xxx
      REJECTED  similarity = 0.9xxx
      Similarity gap       = 0.0xxx

  The vector DB cannot distinguish which decision is authoritative.
  An LLM agent consuming these results must re-reason from scratch,
  typically costing 10,000–20,000 tokens of re-planning context.

[3/3] Attempting to write REJECTED into StructuralDB...

  ✓  ConflictingStateError raised in 0.0xx ms:
     Cannot write sign=-1 label='T-2024-001: REJECTED' at depth=0: ...

=================================================================
  RESULTS SUMMARY
=================================================================

  Vector DB
    Query time          : x.xx ms
    Contradiction found : YES — both APPROVED and REJECTED returned
    Agent re-plan cost  : ~14,000 tokens (estimated)
    Safe to act on?     : NO

  StructuralDB
    Block time          : 0.0xx ms
    Contradiction found : blocked at write — REJECTED never entered DB
    Agent re-plan cost  : 0 tokens
    Safe to act on?     : YES — APPROVED is the only authoritative state
```

### How it works

StructuralDB models state as a **p-adic ultrametric tree**. Each node
carries a sign (`+1` = assert, `-1` = negate). The anti-negation enforcer
checks a single constraint before every write:

> No two active nodes at the same `(depth, parent)` position may carry
> opposite signs.

This is O(n) over siblings — O(1) in practice for narrow trees. When the
constraint fires, the write is rejected and the database remains
consistent. The LLM agent reading StructuralDB sees exactly one
authoritative state; no disambiguation pass required.

Vector databases have no equivalent mechanism. Cosine similarity is a
distance metric, not a logical consistency check. Two semantically
opposite statements can produce nearly identical embedding vectors when
the query lands between them, which is exactly what happens in
real-world edge cases (partial failures, mid-state transitions, stale
cache entries).

### Extending the benchmark

To plug in a real embedding model (e.g. OpenAI `text-embedding-3-small`):

```python
import openai

client = openai.OpenAI()

def embed(text: str) -> list[float]:
    resp = client.embeddings.create(model="text-embedding-3-small", input=text)
    return resp.data[0].embedding
```

Replace the stub `APPROVED_VEC` / `REJECTED_VEC` / `QUERY_VEC` constants
with calls to `embed(...)` on the corresponding trade text. The
`ConflictingStateError` from StructuralDB will fire regardless of which
embedding model you use — it is enforced at the structural layer, not the
semantic layer.

---

© VectorPeak Technologies
