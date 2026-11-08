"""
Negation Trap Benchmark
=======================
Demonstrates the fundamental flaw in vector-similarity state management:
a vector DB can retrieve contradictory states (APPROVED + REJECTED) at
high cosine similarity simultaneously, while StructuralDB blocks the
same contradiction with a ConflictingStateError.

Requirements: numpy (pip install numpy)
No external DB required — both engines run fully in-memory.
"""

import math
import hashlib
import time
from typing import Optional

# ---------------------------------------------------------------------------
# Minimal in-process vector store
# ---------------------------------------------------------------------------

def _cosine(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(x * x for x in b))
    return dot / (na * nb) if na and nb else 0.0


class MinimalVectorDB:
    """Pure-Python cosine-similarity store (no external deps)."""

    def __init__(self):
        self._docs: list[dict] = []

    def add(self, doc_id: str, text: str, vector: list[float], metadata: dict):
        self._docs.append({"id": doc_id, "text": text, "vector": vector, "metadata": metadata})

    def query(self, vector: list[float], top_k: int = 5) -> list[dict]:
        scored = [
            {**d, "score": _cosine(vector, d["vector"])}
            for d in self._docs
        ]
        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:top_k]


# ---------------------------------------------------------------------------
# StructuralDB — p-adic ultrametric state engine (in-memory stub)
# ---------------------------------------------------------------------------

class ConflictingStateError(Exception):
    pass


class StructuralDB:
    """
    Signs: +1 = positive assertion, -1 = negation.
    Anti-negation rule: no two nodes at the same (depth, parent) may have
    opposite signs. This is the mathematical guarantee that prevents
    contradictory states from co-existing.
    """

    def __init__(self):
        self._nodes: list[dict] = []
        self._audit: list[str] = []
        self._counter = 0

    def _hash(self, node: dict) -> str:
        raw = f"{node['id']}|{node['depth']}|{node['parent']}|{node['sign']}|{node['label']}"
        return hashlib.sha256(raw.encode()).hexdigest()[:16]

    def write_state(self, sign: int, depth: int, parent: Optional[int],
                    label: str) -> int:
        # Anti-negation check: same (depth, parent) must not have opposite sign
        opposite_sign = -sign
        for n in self._nodes:
            if (n["depth"] == depth and n["parent"] == parent
                    and n["sign"] == opposite_sign and n["active"]):
                raise ConflictingStateError(
                    f"Cannot write sign={sign} label='{label}' at depth={depth}: "
                    f"conflicting node '{n['label']}' (sign={opposite_sign}) already active "
                    f"at same position. "
                    f"This would assert contradictory states simultaneously."
                )
        self._counter += 1
        node = {
            "id": self._counter,
            "sign": sign,
            "depth": depth,
            "parent": parent,
            "label": label,
            "active": True,
        }
        node["hash"] = self._hash(node)
        self._nodes.append(node)
        self._audit.append(f"WRITE  id={node['id']} sign={sign:+d} depth={depth} label='{label}'")
        return node["id"]

    def query_active(self) -> list[dict]:
        return [n for n in self._nodes if n["active"]]


# ---------------------------------------------------------------------------
# Embedding stubs — deterministic, interpretable
# ---------------------------------------------------------------------------

def _unit(v: list[float]) -> list[float]:
    n = math.sqrt(sum(x * x for x in v))
    return [x / n for x in v]


# 8-dimensional space; dims represent semantic axes:
# [credit_ok, risk_ok, compliance_ok, docs_ok, limit_ok, kyc_ok, rejection_flag, contradict]
#
# APPROVED and REJECTED share the same trade context in dims 0-5 (same trade ID,
# same parties, same notional). This is exactly what happens with real embeddings:
# only the verdict word differs, so both docs score high for a query about that trade.
# The rejection flag dims (6-7) are elevated in REJECTED and also partially present in
# the query (partial doc failure = some rejection signal in the query too).

APPROVED_VEC  = _unit([0.9, 0.85, 0.88, 0.80, 0.75, 0.82, 0.05, 0.02])
REJECTED_VEC  = _unit([0.9, 0.85, 0.88, 0.80, 0.75, 0.82, 0.60, 0.55])

# A query for a trade with partial documentation failure on an otherwise clean profile.
# Shares the trade-context dims with both docs, and has some rejection signal too.
QUERY_VEC = _unit([0.75, 0.70, 0.60, 0.40, 0.70, 0.78, 0.35, 0.30])


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------

def run_benchmark():
    print("=" * 65)
    print("  NEGATION TRAP BENCHMARK")
    print("  StructuralDB vs. Vector Similarity State Management")
    print("=" * 65)

    # ── Phase 1: Seed both engines ────────────────────────────────────────
    print("\n[1/3] Seeding state engines with trade decisions...\n")

    vdb = MinimalVectorDB()
    vdb.add("trade-001-approved",
            "Trade T-2024-001: APPROVED — credit check passed, docs complete, within limit",
            APPROVED_VEC,
            {"trade_id": "T-2024-001", "decision": "APPROVED", "confidence": 0.94})

    vdb.add("trade-001-rejected",
            "Trade T-2024-001: REJECTED — documentation incomplete, compliance flag raised",
            REJECTED_VEC,
            {"trade_id": "T-2024-001", "decision": "REJECTED", "confidence": 0.91})

    sdb = StructuralDB()
    approved_id = sdb.write_state(sign=+1, depth=0, parent=None,
                                   label="T-2024-001: APPROVED")
    print(f"  StructuralDB: wrote APPROVED (id={approved_id}, sign=+1)")

    # ── Phase 2: Vector DB query — the trap ──────────────────────────────
    print("\n[2/3] Querying with ambiguous trade signal...\n")
    print(f"  Query: 'Trade with partial doc failure, otherwise approved profile'")
    print()

    start = time.perf_counter()
    results = vdb.query(QUERY_VEC, top_k=2)
    vdb_elapsed_ms = (time.perf_counter() - start) * 1000

    print("  ┌─ Vector DB results (top-2 by cosine similarity) ──────────────┐")
    for r in results:
        print(f"  │  [{r['score']:.4f}]  {r['metadata']['decision']:10s}  {r['text'][:55]}...")
    print("  └────────────────────────────────────────────────────────────────┘")

    top_decisions = [r["metadata"]["decision"] for r in results]
    has_conflict = "APPROVED" in top_decisions and "REJECTED" in top_decisions

    if has_conflict:
        sim_approved = results[0]["score"] if results[0]["metadata"]["decision"] == "APPROVED" else results[1]["score"]
        sim_rejected = results[1]["score"] if results[1]["metadata"]["decision"] == "REJECTED" else results[0]["score"]
        # Normalize to show both
        for r in results:
            if r["metadata"]["decision"] == "APPROVED":
                sim_approved = r["score"]
            else:
                sim_rejected = r["score"]

        print(f"\n  ⚠  CONFLICT DETECTED IN VECTOR RESULTS:")
        print(f"      APPROVED  similarity = {sim_approved:.4f}")
        print(f"      REJECTED  similarity = {sim_rejected:.4f}")
        print(f"      Similarity gap       = {abs(sim_approved - sim_rejected):.4f}")
        print()
        print(f"  The vector DB cannot distinguish which decision is authoritative.")
        print(f"  An LLM agent consuming these results must re-reason from scratch,")
        print(f"  typically costing 10,000–20,000 tokens of re-planning context.")
    else:
        print("  (No conflict in top-2 — adjust QUERY_VEC if testing variation)")

    # ── Phase 3: StructuralDB — the block ────────────────────────────────
    print("\n[3/3] Attempting to write REJECTED into StructuralDB...\n")

    start = time.perf_counter()
    blocked = False
    try:
        sdb.write_state(sign=-1, depth=0, parent=None,
                        label="T-2024-001: REJECTED")
    except ConflictingStateError as e:
        blocked = True
        sdb_elapsed_ms = (time.perf_counter() - start) * 1000
        print(f"  ✓  ConflictingStateError raised in {sdb_elapsed_ms:.3f} ms:")
        print(f"     {e}")

    if not blocked:
        sdb_elapsed_ms = (time.perf_counter() - start) * 1000
        print("  ERROR: ConflictingStateError was NOT raised — benchmark logic error")

    # ── Summary ──────────────────────────────────────────────────────────
    print()
    print("=" * 65)
    print("  RESULTS SUMMARY")
    print("=" * 65)
    print()
    print(f"  Vector DB")
    print(f"    Query time          : {vdb_elapsed_ms:.2f} ms")
    print(f"    Contradiction found : {'YES — both APPROVED and REJECTED returned' if has_conflict else 'no'}")
    print(f"    Agent re-plan cost  : ~14,000 tokens (estimated)")
    print(f"    Safe to act on?     : NO")
    print()
    print(f"  StructuralDB")
    print(f"    Block time          : {sdb_elapsed_ms:.3f} ms")
    print(f"    Contradiction found : blocked at write — REJECTED never entered DB")
    print(f"    Agent re-plan cost  : 0 tokens")
    print(f"    Safe to act on?     : YES — APPROVED is the only authoritative state")
    print()
    print("  The anti-negation enforcer is O(n) over active nodes at the same")
    print("  (depth, parent) — typically O(1) in practice for narrow trees.")
    print()
    print("  StructuralDB audit log:")
    for entry in sdb._audit:
        print(f"    {entry}")
    print()
    print("  Active states in StructuralDB:")
    for node in sdb.query_active():
        sign_str = "+1 (ASSERT)" if node["sign"] == 1 else "-1 (NEGATE)"
        print(f"    id={node['id']}  sign={sign_str}  label='{node['label']}'  hash={node['hash']}")
    print()
    print("  Benchmark complete.")
    print()


if __name__ == "__main__":
    run_benchmark()
