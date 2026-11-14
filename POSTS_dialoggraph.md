# DialogGraph — Social Media Copy (CGA-005)

---

## LinkedIn

NPC dialogue systems route conversations by keyword matching or cosine similarity. DialogGraph does it by p-adic distance.

Every topic key is assigned so its 2-adic valuation equals the shell level. The distance between a context key and a topic key is `d_2(context, topic) = 2^{-v_2(context-topic)}`. Same residue class = zero distance = highest priority. No embeddings. No semantic model. The routing is structural.

Shell ordering enforces character depth: lore (v=0) always fills the token budget before ephemeral chatter (v=3). No transient option can displace core character identity — this is a theorem about ultrametric spaces, not a configuration setting.

Congruence gating (`state ≡ prereq mod 2^k`) unlocks quest-specific and relationship-specific topics with zero false positives. NPC Kira's warrior backstory is available from the first interaction; her knowledge of the iron key is gated behind finding it.

Benchmark: 10 NPCs × 20 options, budget 400. Zero violations. Gating exact across all states.

👉 github.com/rfdevuser/vectorpeak-experiments

---

## Reddit

**Title:** p-adic proximity for NPC dialogue selection — benchmark and explanation

**Body:**

DialogGraph routes topic selection by 2-adic distance rather than cosine similarity. The intuition: topics at the same "resolution level" cluster together in Z_2. Shell 0 (lore) topics are all in the same coset. So are shell 3 (transient) topics. Distance within a shell is zero; distance between shells is bounded below.

Result: select() gives you lore first, transient last, every time — without sorting, without configuration. It falls out of the ultrametric.

Congruence gating is exact: `dialogue_allowed(state, prereq, p, k)` is a clopen ball membership test. No approximation.

Benchmark (pure Python, zero deps): https://github.com/rfdevuser/vectorpeak-experiments

Phase 3 runs NPC Kira at two quest states and shows prereq=4 topics blocked at state=0, unlocked at state=4. The numbers are deterministic.

---

## Discord

**DialogGraph benchmark up** — p-adic proximity NPC dialogue, pure Python, no deps.

Routes topics by 2-adic distance. Shell ordering enforced structurally. Congruence gating exact.

Demo: NPC Kira at state=0 vs state=4 — quest-active topics unlock exactly.

4/4 PASS. `python run_dialoggraph_benchmark.py`

https://github.com/rfdevuser/vectorpeak-experiments

---

## X / Twitter (4-tweet thread)

**Tweet 1:**
NPC dialogue routing via p-adic distance.

d_2(context, topic) = 2^{-v_2(context-topic)}

Same residue class = zero distance = selected first. No embeddings. No semantic model. Structure only.

**Tweet 2:**
Shell ordering falls out of the ultrametric:

v=0 (lore) always before v=3 (ephemeral). Budget filled: lore, then quest topics, then interactions, then chatter.

It's a theorem about disjoint balls, not a priority queue.

**Tweet 3:**
Congruence gating: topic available iff state ≡ prereq (mod 2^k).

NPC Kira's iron key dialogue: blocked at state=0, unlocked at state=4. Zero false positives. Zero false negatives.

**Tweet 4:**
10 NPCs × 20 options, budget 400. Zero violations.

4/4 PASS. Pure Python.

github.com/rfdevuser/vectorpeak-experiments
