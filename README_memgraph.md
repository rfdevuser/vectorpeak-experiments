# MemGraph — NPC Memory Kernel (CGA-004)

**Script:** `run_memgraph_benchmark.py`  
**Product:** MemGraph  
**Dependencies:** none (pure Python standard library)

---

## What it demonstrates

MemGraph is a p-adic ultrametric memory tree for game NPCs. Three structural properties, all verified from first principles:

**Property 1 — Shell-ordered retrieval with zero overhead.**  
Each memory key is assigned so that `v_p(key) == shell`. Shell 0 (lore: sworn oaths, origin stories) always retrieves before shell 3 (transient: player asked about the market). The ordering is not sorted at query time — it is forced by the arithmetic of `v_p(key)`. No configuration. No bookkeeping.

**Property 2 — Token budget never exceeded.**  
The disjoint ball property of `Z_p` means memories at different shells never interfere. Budget is consumed greedily in shell order: lore fills first, transient last. Zero boundary overlap means no memory is split across a budget boundary.

**Property 3 — Guardrail chain is Hensel-lifting exact.**  
Narrative actions (ENTER_DUNGEON, FIND_KEY, OPEN_GATE, DEFEAT_BOSS, CLAIM_TREASURE) are valid iff `state ≡ prereq (mod p^k)`. The valid state set is a clopen ball in `Z_p` — there is no boundary. Any state outside is strictly disjoint. The guardrail cannot be bypassed by partial progress.

---

## Running

```bash
python run_memgraph_benchmark.py
```

Expected output: `Phase results: 4/4 PASS`

---

## Benchmark phases

| Phase | Description | Checks |
|---|---|---|
| 1 | p-adic valuation table + ultrametric check | 5 valuation cases + 500 triples |
| 2 | Shell ordering + token budget enforcement | 7-memory tree + 40-memory/100-token test |
| 3 | Guardrail chain (5 actions) + blocking test | OPEN_GATE blocked at state=0 |
| 4 | Full scenario: 20 NPCs × 50 memories, budget=300 | Zero budget violations |

---

For API access and integration: **[vallikat@vectorpeaktech.com](mailto:vallikat@vectorpeaktech.com)**
