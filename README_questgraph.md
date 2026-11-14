# QuestGraph — Quest Chain Engine (CGA-006)

**Script:** `run_questgraph_benchmark.py`  
**Product:** QuestGraph  
**Dependencies:** none (pure Python standard library)

---

## What it demonstrates

QuestGraph is a 2-adic digit state machine for branching quest chains. Three structural properties:

**Property 1 — Fork: two branches simultaneously available.**  
Scholar and warrior approaches share `prereq=16 mod 32`. At state=16, both nodes pass their congruence check simultaneously. No conditional logic. One congruence check per node.

**Property 2 — Merge: one congruence catches all branch predecessors.**  
`breach_vault` has `prereq=16 mod 256`. Scholar path state=272: `272 mod 256 = 16`. Warrior path state=528: `528 mod 256 = 16`. Both satisfy the same single congruence. Zero special cases.

**Property 3 — Side quest orthogonality.**  
`find_inscription` delta=1024. `1024 mod 256 = 0`. Adding a side-quest completion to any state leaves the mod-256 remainder unchanged. Main-quest prereqs are structurally unaffected by side-quest progress.

---

## State bit layout

| Bits | Value | Meaning |
|---|---|---|
| bits 0-7 | mod 256 | main quest progress (0→4→8→16→32→64→128) |
| bit 8 | 256 | scholar branch flag |
| bit 9 | 512 | warrior branch flag |
| bit 10 | 1024 | side quest A flag (orthogonal to main) |

---

## Running

```bash
python run_questgraph_benchmark.py
```

Expected output: `Phase results: 4/4 PASS`

---

## Benchmark phases

| Phase | Description | Checks |
|---|---|---|
| 1 | 2-adic bit layout + valuation table | 4 valuation cases |
| 2 | Fork (state=16, both branches) + merge (272/528 mod 256=16) | Fork + merge correctness |
| 3 | Side quest orthogonality (state=1032 mod 16=8) | Main prereq unaffected |
| 4 | Full scholar path + full warrior path (7 nodes each) | Both paths 7/7 PASS |

---

For API access and integration: **[vallikat@vectorpeaktech.com](mailto:vallikat@vectorpeaktech.com)**
