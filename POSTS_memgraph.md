# MemGraph — Social Media Copy (CGA-004)

---

## LinkedIn

Game NPCs forget things in the wrong order. The merchant remembers your name but forgets she swore an oath to protect the village. The ancient guardian knows today's rumour but not his own origin story.

MemGraph fixes this with p-adic ultrametric memory trees. Every memory gets a key whose 2-adic valuation encodes its permanence shell: v=0 for lore (sworn oaths, origin stories), v=3 for transient (player just asked about the market). The ordering isn't sorted at query time — it's forced by the arithmetic. Lore always retrieves first. Transient never displaces core character identity.

The guardrail chain is Hensel-exact: a narrative action (enter dungeon, find key, open gate) is valid iff state ≡ prereq (mod 2^k). The valid state set is a clopen ball in Z_2. There is no boundary. No bypass.

Benchmark: 20 NPCs × 50 memories, token budget 300. Zero budget violations. Shell ordering preserved across all 20. Guardrail chain: 5/5 actions correct + blocking test passed.

Four phases. Pure Python. No dependencies.

👉 github.com/rfdevuser/vectorpeak-experiments

---

## Reddit

**Title:** We built NPC memory from p-adic number theory — here's the benchmark

**Body:**

Most NPC memory systems are sorted lists or priority queues with hand-tuned weights. MemGraph does something different: each memory key is assigned so that its 2-adic valuation equals the shell level. v_2(key)=0 → permanent lore. v_2(key)=3 → ephemeral transient.

The retrieval order falls out of the ultrametric structure. p-adic balls are disjoint — shell 0 memories and shell 3 memories live in completely separate regions of Z_2. No sort step. No configuration. The structure forces it.

Guardrails work the same way: `state ≡ prereq (mod 2^k)` is a clopen ball membership test. Valid or invalid. No fuzzy boundary.

Benchmark (pure Python, zero deps): https://github.com/rfdevuser/vectorpeak-experiments

Results: 4/4 PASS — valuation properties, shell ordering, guardrail chain, 20-NPC stress test.

Happy to explain the math if anyone wants the derivation.

---

## Discord

**MemGraph benchmark is up** — p-adic NPC memory tree, pure Python, no deps.

TL;DR: memory keys are assigned so v_2(key) == shell level. Lore (v=0) always retrieves before transient (v=3). The order is structural, not sorted. Guardrail chain is congruence-exact.

4/4 PASS. Run it: `python run_memgraph_benchmark.py`

https://github.com/rfdevuser/vectorpeak-experiments

---

## X / Twitter (4-tweet thread)

**Tweet 1:**
NPC memory that forgets things in the right order — from first principles.

MemGraph uses p-adic ultrametric trees. Memory key k gets v_2(k)=shell. Lore (v=0) always before transient (v=3). The ordering is arithmetic, not sorted.

**Tweet 2:**
The disjoint ball property of Z_2 means memories at different shells never interfere.

Token budget is consumed greedily: lore fills first. Zero boundary overlap. Zero budget violations across 20 NPCs × 50 memories.

**Tweet 3:**
Guardrails are Hensel-exact: action valid iff state ≡ prereq (mod 2^k).

Valid state set = clopen ball in Z_2. No boundary. No bypass. OPEN_GATE at state=0 is blocked structurally, not by an if-statement.

**Tweet 4:**
Four phases. Pure Python. No dependencies.

Results: 4/4 PASS.

Benchmark → github.com/rfdevuser/vectorpeak-experiments
