"""
QuestGraph — Quest Chain Engine Benchmark
CGA-006 / 2-adic digit state machine with fork, merge, and side quests.

Three claims:

  Claim 1 — Fork: two quest nodes are simultaneously available.
    Scholar and warrior share prereq=16 mod 32. At state=16, both are
    available simultaneously. No conditional logic. One congruence per node.

  Claim 2 — Merge: one congruence catches all branch predecessors.
    Scholar: state=16+256=272; warrior: state=16+512=528.
    breach_vault prereq=16 mod 256.
    272 mod 256 = 16, 528 mod 256 = 16. Both satisfy. Zero special cases.

  Claim 3 — Side quest orthogonality.
    find_inscription delta=1024. 1024 mod 256 = 0.
    Main quest prereqs (mod 256) are completely unaffected.

Pure Python standard library only.
"""

import random
from dataclasses import dataclass, field

BOLD  = "\033[1m"
GREEN = "\033[92m"
AMBER = "\033[93m"
RED   = "\033[91m"
RESET = "\033[0m"

MAIN_MASK      = 255
BRANCH_SCHOLAR = 256
BRANCH_WARRIOR = 512
SIDE_A_FLAG    = 1024

# ── p-adic primitives ─────────────────────────────────────────────────────────

def p_adic_valuation(n: int, p: int) -> int:
    if n == 0:
        return 10 ** 9
    n = abs(n)
    v = 0
    while n % p == 0:
        n //= p
        v += 1
    return v

def congruence_check(state: int, prereq: int, p: int, k: int) -> bool:
    return (state % (p ** k)) == (prereq % (p ** k))

def state_decompose(state: int) -> dict:
    return {
        "state":          state,
        "main_progress":  state & MAIN_MASK,
        "branch_scholar": bool(state & BRANCH_SCHOLAR),
        "branch_warrior": bool(state & BRANCH_WARRIOR),
        "side_a_done":    bool(state & SIDE_A_FLAG),
    }

# ── QuestChain ────────────────────────────────────────────────────────────────

@dataclass
class QuestNode:
    id: str
    name: str
    state_delta: int
    prereq: int = 0
    p: int = 2
    k: int = 2
    alt_prereqs: list = field(default_factory=list)
    node_type: str = "linear"
    track: str = "main"

    def available(self, state: int) -> bool:
        if congruence_check(state, self.prereq, self.p, self.k):
            return True
        return any(congruence_check(state, ap, self.p, ak)
                   for ap, ak in self.alt_prereqs)

class QuestChain:
    def __init__(self, name: str, p: int = 2):
        self.name = name
        self.p = p
        self._nodes: list = []
        self._node_map: dict = {}
        self._completed: set = set()

    def add_node(self, id, name, state_delta, prereq=0, k=2,
                 alt_prereqs=None, node_type="linear", track="main"):
        node = QuestNode(id=id, name=name, state_delta=state_delta,
                         prereq=prereq, p=self.p, k=k,
                         alt_prereqs=alt_prereqs or [],
                         node_type=node_type, track=track)
        self._nodes.append(node)
        self._node_map[id] = node
        return node

    def available_nodes(self, state: int) -> list:
        return [n for n in self._nodes
                if n.available(state) and n.id not in self._completed]

    def complete_node(self, state: int, node_id: str):
        node = self._node_map.get(node_id)
        if node is None or node.id in self._completed:
            return False, state
        if not node.available(state):
            return False, state
        self._completed.add(node_id)
        return True, state + node.state_delta

    def reset(self):
        self._completed.clear()

def build_demo_chain() -> QuestChain:
    q = QuestChain("The Vault of Velantis", p=2)
    q.add_node("accept_quest",    "Accept the Commission",        state_delta=4,              prereq=0,  k=2, node_type="linear", track="main")
    q.add_node("explore_ruins",   "Explore the Ruins",            state_delta=4,              prereq=4,  k=3, node_type="linear", track="main")
    q.add_node("find_entrance",   "Find the Vault Entrance",      state_delta=8,              prereq=8,  k=4, node_type="fork",   track="main")
    q.add_node("scholar_approach","Decipher the Vault Lock",      state_delta=BRANCH_SCHOLAR, prereq=16, k=5, node_type="fork",   track="branch_a")
    q.add_node("warrior_approach","Override the Vault Mechanism", state_delta=BRANCH_WARRIOR, prereq=16, k=5, node_type="fork",   track="branch_b")
    q.add_node("breach_vault",    "Enter the Vault",              state_delta=16,             prereq=16, k=8, node_type="merge",  track="main")
    q.add_node("claim_relic",     "Claim the Adelic Compass",     state_delta=32,             prereq=32, k=8, node_type="linear", track="main")
    q.add_node("return_home",     "Return to the Archivist",      state_delta=64,             prereq=64, k=8, node_type="end",    track="main")
    q.add_node("find_inscription","Discover the Hidden Inscription", state_delta=SIDE_A_FLAG, prereq=8,  k=4, node_type="side",   track="side_a")
    return q

# ── Phase 1: State bit layout ─────────────────────────────────────────────────

def run_state_encoding_phase():
    print(f"\n{BOLD}[PHASE 1: 2-adic State Bit Layout]{RESET}\n")
    print(f"  State integer S encodes all quest progress simultaneously:")
    print(f"  {'Bits':<10}  {'Value':<8}  Meaning")
    print(f"  {'─'*10}  {'─'*8}  {'─'*44}")
    for bits, val, meaning in [
        ("bits 0-7",  f"mod {MAIN_MASK+1}",  "main quest progress (0->4->8->16->32->64->128)"),
        ("bit 8",     str(BRANCH_SCHOLAR),    "scholar branch flag"),
        ("bit 9",     str(BRANCH_WARRIOR),    "warrior branch flag"),
        ("bit 10",    str(SIDE_A_FLAG),       "side quest A flag (orthogonal to main)"),
    ]:
        print(f"  {bits:<10}  {val:<8}  {meaning}")

    print(f"\n  2-adic valuation of key constants:")
    cases = [
        (4,    2, 2,  "v_2(4)=2"),
        (16,   2, 4,  "v_2(16)=4"),
        (256,  2, 8,  "v_2(256)=8"),
        (1024, 2, 10, "v_2(1024)=10"),
    ]
    all_ok = True
    print(f"  {'n':>6}  {'v_2(n)':>8}  {'expected':>8}  Result")
    print(f"  {'─'*6}  {'─'*8}  {'─'*8}  {'─'*10}")
    for n, p, exp, label in cases:
        got = p_adic_valuation(n, p)
        ok = got == exp
        all_ok = all_ok and ok
        col = GREEN if ok else RED
        print(f"  {n:>6}  {got:>8}  {exp:>8}  {col}{'PASS' if ok else 'FAIL'}{RESET}  {label}")
    return all_ok

# ── Phase 2: Fork and merge ────────────────────────────────────────────────────

def run_fork_merge_phase():
    print(f"\n{BOLD}[PHASE 2: Fork and Merge — Single Congruence, All Paths]{RESET}\n")

    chain = build_demo_chain()
    avail = {n.id for n in chain.available_nodes(16)}
    fork_ok = "scholar_approach" in avail and "warrior_approach" in avail
    col = GREEN if fork_ok else RED
    print(f"  Fork — state=16, prereq=16 mod 32:")
    print(f"  Available nodes: {sorted(avail)}")
    print(f"  Both scholar + warrior available simultaneously: {col}{'PASS' if fork_ok else 'FAIL'}{RESET}")
    print()

    chain2 = build_demo_chain()
    chain2._completed = {"accept_quest", "explore_ruins", "find_entrance"}
    avail_scholar = {n.id for n in chain2.available_nodes(272)}
    chain2._completed = {"accept_quest", "explore_ruins", "find_entrance"}
    avail_warrior = {n.id for n in chain2.available_nodes(528)}
    merge_ok = "breach_vault" in avail_scholar and "breach_vault" in avail_warrior
    col = GREEN if merge_ok else RED
    print(f"  Merge — breach_vault prereq=16 mod 256:")
    print(f"    Scholar path: state=272  ->  272 mod 256 = {272%256}  -> breach_vault {'IN' if 'breach_vault' in avail_scholar else 'NOT IN'} available")
    print(f"    Warrior path: state=528  ->  528 mod 256 = {528%256}  -> breach_vault {'IN' if 'breach_vault' in avail_warrior else 'NOT IN'} available")
    print(f"  One congruence catches both predecessors: {col}{'PASS' if merge_ok else 'FAIL'}{RESET}")

    return fork_ok and merge_ok

# ── Phase 3: Side quest orthogonality ─────────────────────────────────────────

def run_side_quest_phase():
    print(f"\n{BOLD}[PHASE 3: Side Quest Orthogonality — Bit Isolation]{RESET}\n")
    print(f"  Side quest delta = {SIDE_A_FLAG} (bit 10 = 2^10).")
    print(f"  {SIDE_A_FLAG} mod 256 = {SIDE_A_FLAG % 256}  ->  main-quest mod-256 prereqs unaffected.\n")

    side_state = 8 + SIDE_A_FLAG  # 1032
    main_still_works = congruence_check(side_state, 8, 2, 4)
    decomp = state_decompose(side_state)

    print(f"  explore_ruins (delta=4->8) + find_inscription (delta={SIDE_A_FLAG})")
    print(f"  Combined state: 8 + {SIDE_A_FLAG} = {side_state}")
    print(f"    main_progress  = {decomp['main_progress']} (unchanged)")
    print(f"    side_a_done    = {decomp['side_a_done']}")
    print(f"    branch_scholar = {decomp['branch_scholar']}")
    print(f"    branch_warrior = {decomp['branch_warrior']}")
    print()
    print(f"  find_entrance prereq=8 mod 16: {side_state} mod 16 = {side_state % 16}")
    col = GREEN if main_still_works else RED
    print(f"  Main quest prereq still satisfied: {col}{'PASS' if main_still_works else 'FAIL'}{RESET}")
    return main_still_works

# ── Phase 4: Full path walk ────────────────────────────────────────────────────

def run_full_path_phase():
    print(f"\n{BOLD}[PHASE 4: Full Quest Paths — Scholar and Warrior]{RESET}\n")

    all_ok = True
    for branch in ("scholar", "warrior"):
        chain = build_demo_chain()
        state = 0
        order = [
            "accept_quest", "explore_ruins", "find_entrance",
            "scholar_approach" if branch == "scholar" else "warrior_approach",
            "breach_vault", "claim_relic", "return_home",
        ]
        print(f"  {BOLD}{branch.capitalize()} path:{RESET}")
        print(f"  {'Node':<24}  {'state_in':>10}  {'state_out':>10}  {'main_bits':>10}  Result")
        print(f"  {'─'*24}  {'─'*10}  {'─'*10}  {'─'*10}  {'─'*8}")

        step_ok = True
        for node_id in order:
            ok, new_state = chain.complete_node(state, node_id)
            col = GREEN if ok else RED
            print(f"  {node_id:<24}  {state:>10}  {new_state:>10}  "
                  f"{new_state & MAIN_MASK:>10}  {col}{'PASS' if ok else 'FAIL'}{RESET}")
            if not ok:
                step_ok = False
            state = new_state if ok else state

        decomp = state_decompose(state)
        main_complete = (state & MAIN_MASK) == 128
        branch_flag = decomp["branch_scholar"] if branch == "scholar" else decomp["branch_warrior"]
        path_ok = step_ok and main_complete and branch_flag
        all_ok = all_ok and path_ok
        col = GREEN if path_ok else RED
        print(f"\n  Final state={state}  main_bits=128: {main_complete}  {branch}_flag: {branch_flag}")
        print(f"  Result: {col}{'PASS' if path_ok else 'FAIL'}{RESET}\n")

    return all_ok

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print(f"\n{BOLD}{'='*68}{RESET}")
    print(f"{BOLD}  QUESTGRAPH — QUEST CHAIN ENGINE  (CGA-006){RESET}")
    print(f"{BOLD}{'='*68}{RESET}")
    print(f"  2-adic digit state machine. Fork. Merge. Parallel side quests.")
    print(f"  Bits 0-7: main. Bit 8: scholar. Bit 9: warrior. Bit 10: side-A.")
    print(f"  Pure Python, zero dependencies.")

    p1 = run_state_encoding_phase()
    p2 = run_fork_merge_phase()
    p3 = run_side_quest_phase()
    p4 = run_full_path_phase()

    passed = sum([p1, p2, p3, p4])
    print(f"{BOLD}{'='*68}{RESET}")
    col = GREEN if passed == 4 else RED
    print(f"  Phase results: {col}{passed}/4 PASS{RESET}")
    print(f"  Fork:       {GREEN}both branches available simultaneously at prereq=16 mod 32{RESET}")
    print(f"  Merge:      {GREEN}one congruence (mod 256) catches scholar=272 and warrior=528{RESET}")
    print(f"  Side quest: {GREEN}bit 10 delta orthogonal to all main-quest mod-256 prereqs{RESET}")
    print(f"{BOLD}{'='*68}{RESET}\n")

if __name__ == "__main__":
    main()
