# DialogGraph — NPC Dialogue Engine (CGA-005)

**Script:** `run_dialoggraph_benchmark.py`  
**Product:** DialogGraph  
**Dependencies:** none (pure Python standard library)

---

## What it demonstrates

DialogGraph is a p-adic proximity dialogue selection engine for game NPCs. Three structural properties:

**Property 1 — p-adic proximity routes topics to nearest context.**  
Topic keys encode shell: `v_p(key) == shell`. `p_adic_closest(context, keys)` ranks topics by `d_p(context, key) = p^{-v_p(context-key)}`. Same residue class = zero distance = highest priority. The routing is structural — no embeddings, no semantic model.

**Property 2 — Shell ordering: lore always precedes transient.**  
`select()` sorts by `(shell, distance)`. Lore (v=0) fills the token budget before quest topics (v=1), interactions (v=2), and ephemeral chatter (v=3). No transient option can displace core character lore.

**Property 3 — Congruence gating is exact.**  
`dialogue_allowed(state, prereq, p, k)` iff `state ≡ prereq (mod p^k)`. Zero false positives. Zero false negatives. Demonstrated on NPC Kira: prereq=4 topics are blocked at state=0 and unlocked at state=4.

---

## Running

```bash
python run_dialoggraph_benchmark.py
```

Expected output: `Phase results: 4/4 PASS`

---

## Benchmark phases

| Phase | Description | Checks |
|---|---|---|
| 1 | p-adic proximity: d_2 cases + p_adic_closest + ultrametric | 3 distance cases + 500 triples |
| 2 | Shell ordering + gating (prereq=4 blocked/allowed) | lore-before-transient + gate check |
| 3 | NPC Kira demo at state=0 and state=4 | prereq=4 topics gated correctly |
| 4 | Full: 10 NPCs × 20 options, budget=400 | Zero budget violations |

---

For API access and integration: **[vallikat@vectorpeaktech.com](mailto:vallikat@vectorpeaktech.com)**
