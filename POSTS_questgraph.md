# QuestGraph — Social Media Copy (CGA-006)

---

## LinkedIn

Branching quest systems typically use nested if-statements, state machines with explicit transition tables, or scripting layers on top of scripting layers. QuestGraph uses one idea: 2-adic digit encoding.

Every quest node has a single congruence prereq: `state ≡ prereq (mod 2^k)`. That's it. No special fork logic. No merge logic. No side-quest flags in the prereq.

Fork falls out naturally: scholar_approach and warrior_approach both use prereq=16 mod 32. At state=16, both pass. Both available simultaneously. One congruence each.

Merge falls out naturally: breach_vault uses prereq=16 mod 256. Scholar path ends at state=272 (272 mod 256 = 16). Warrior path ends at state=528 (528 mod 256 = 16). Both satisfy the same prereq. One congruence catches all predecessors.

Side quests are orthogonal by construction: delta=1024, and 1024 mod 256 = 0. Main-quest prereqs are structurally unaffected.

Benchmark: full scholar path and full warrior path (7 nodes each), plus fork/merge verification and side-quest isolation. 4/4 PASS. Pure Python. No dependencies.

👉 github.com/rfdevuser/vectorpeak-experiments

---

## Reddit

**Title:** Quest branching and merging from 2-adic number theory — no special cases

**Body:**

QuestGraph encodes all quest state in a single integer. Bits 0-7 track main progress. Bit 8 is the scholar flag. Bit 9 is the warrior flag. Bit 10 is a side quest.

Every node has one prereq: `state % (2^k) == prereq % (2^k)`. That's the entire engine.

Fork: two nodes share prereq=16 mod 32. Both are available at state=16. No special fork logic.

Merge: breach_vault prereq=16 mod 256. Scholar state 272: 272 mod 256 = 16. Warrior state 528: 528 mod 256 = 16. Same check catches both. No special merge logic.

Side quest delta=1024. 1024 mod 256 = 0. Completing the side quest adds 0 to any mod-256 remainder. Main-quest prereqs see nothing.

Benchmark (pure Python, zero deps): https://github.com/rfdevuser/vectorpeak-experiments

4/4 PASS. The math is in the README.

---

## Discord

**QuestGraph benchmark up** — 2-adic quest state machine, fork + merge + side quests, pure Python, no deps.

TL;DR: one integer encodes everything. Fork = two nodes, same prereq mod 32. Merge = one prereq mod 256 catches all branches. Side quest delta = multiple of 256, main prereqs unaffected.

4/4 PASS. `python run_questgraph_benchmark.py`

https://github.com/rfdevuser/vectorpeak-experiments

---

## X / Twitter (4-tweet thread)

**Tweet 1:**
Quest branching without special cases.

QuestGraph encodes all progress in one integer: bits 0-7 = main, bit 8 = scholar, bit 9 = warrior, bit 10 = side quest.

Every node: one congruence. That's the whole engine.

**Tweet 2:**
Fork: scholar and warrior share prereq=16 mod 32.

At state=16, both nodes pass. Both available simultaneously. No fork logic. One congruence each.

**Tweet 3:**
Merge: breach_vault prereq=16 mod 256.

Scholar state=272 → 272 mod 256=16 ✓
Warrior state=528 → 528 mod 256=16 ✓

One check catches all branches. Zero special cases.

**Tweet 4:**
Side quest delta=1024. 1024 mod 256=0. Main prereqs see nothing.

Full scholar + warrior paths: 7/7 nodes each.

4/4 PASS. Pure Python. github.com/rfdevuser/vectorpeak-experiments
