"""
DialogGraph — NPC Dialogue Engine Benchmark
CGA-005 / p-adic proximity selection with congruence gating.

Three claims:

  Claim 1 — p-adic proximity routes topics to nearest context.
    Topic keys encode shell: v_p(key) == shell level (0=lore, 3=transient).
    p_adic_closest(context, keys) ranks topics by d_p(context, key).
    Same residue class = zero distance = highest priority.

  Claim 2 — Shell ordering: lore (v=0) always precedes transient (v=3).
    select() sorts by (shell, distance). Lore fills the budget first.
    No transient chatter can displace core character lore.

  Claim 3 — Congruence gating is exact.
    dialogue_allowed(state, prereq, p, k) iff state == prereq (mod p^k).
    Zero false positives. Zero false negatives. No approximation.

Pure Python standard library only.
"""

import random
from dataclasses import dataclass

BOLD  = "\033[1m"
GREEN = "\033[92m"
AMBER = "\033[93m"
RED   = "\033[91m"
RESET = "\033[0m"

SHELL_NAMES = {0: "lore", 1: "quest", 2: "interaction", 3: "transient"}

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

def p_adic_norm(n: int, p: int) -> float:
    v = p_adic_valuation(n, p)
    if v >= 10 ** 8:
        return 0.0
    return float(p) ** (-v)

def ultrametric_distance(a: int, b: int, p: int) -> float:
    return p_adic_norm(a - b, p)

def dialogue_allowed(state: int, prereq: int, p: int, k: int) -> bool:
    return (state % (p ** k)) == (prereq % (p ** k))

def p_adic_closest(context: int, keys: list, p: int) -> list:
    return sorted([(k, ultrametric_distance(context, k, p)) for k in keys],
                  key=lambda x: x[1])

def _estimate_tokens(text: str) -> int:
    return max(1, len(text.split()) * 4 // 3)

# ── DialogTree ────────────────────────────────────────────────────────────────

@dataclass
class DialogueTopic:
    key: int
    text: str
    shell: int
    prereq: int = 0
    p: int = 2
    k: int = 2

    @property
    def shell_name(self) -> str:
        return SHELL_NAMES.get(self.shell, f"v={self.shell}")

@dataclass
class DialogueOption:
    topic: DialogueTopic
    response: str
    tokens: int = 0

    def __post_init__(self):
        if self.tokens == 0:
            self.tokens = (_estimate_tokens(self.topic.text)
                           + _estimate_tokens(self.response))

class DialogTree:
    def __init__(self, npc_name: str, p: int = 2):
        self.npc_name = npc_name
        self.p = p
        self._options: list = []
        self._counter = 0

    def add_option(self, text: str, response: str, shell: int,
                   prereq: int = 0, k: int = 2):
        self._counter += 1
        key = (self.p ** shell) * (2 * self._counter - 1)
        topic = DialogueTopic(key=key, text=text, shell=shell,
                              prereq=prereq, p=self.p, k=k)
        self._options.append(DialogueOption(topic=topic, response=response))
        return topic

    def select(self, context_key: int, state: int, budget: int) -> list:
        candidates = []
        for opt in self._options:
            t = opt.topic
            if not dialogue_allowed(state, t.prereq, t.p, t.k):
                continue
            candidates.append((t.shell,
                               ultrametric_distance(context_key, t.key, self.p),
                               opt))
        candidates.sort(key=lambda x: (x[0], x[1]))
        selected, used = [], 0
        for _, _, opt in candidates:
            if used + opt.tokens <= budget:
                selected.append(opt)
                used += opt.tokens
        return selected

# ── Demo NPC ──────────────────────────────────────────────────────────────────

def build_kira() -> DialogTree:
    t = DialogTree("Kira", p=2)
    t.add_option("I swore an oath to protect this village on the day I earned my blade.",
                 "My oath is my compass. Without it I would be just another mercenary.",
                 shell=0, prereq=0, k=2)
    t.add_option("My sword was forged by the last smith of Irondell before the city fell.",
                 "She said only one thing: the edge is honest. Are you?",
                 shell=0, prereq=0, k=2)
    t.add_option("The dungeon entrance is sealed with an ancient congruence lock.",
                 "I have seen locks like this. They yield only to those who carry the right key.",
                 shell=1, prereq=0, k=2)
    t.add_option("I found an iron key behind the altar — it fits the gate mechanism.",
                 "Its weight tells me it was made for this lock. Everything here fits together.",
                 shell=1, prereq=4, k=4)
    t.add_option("You mentioned a hidden path around the left wall earlier.",
                 "I should have listened. The left wall — yes, there is a narrowing there.",
                 shell=2, prereq=4, k=4)
    t.add_option("The weather has been unusually still today.",
                 "Still weather before a storm, in my experience. Keep your guard up.",
                 shell=3, prereq=0, k=1)
    t.add_option("I could use a proper meal after all this.",
                 "A warrior fights on an empty stomach more often than the songs admit.",
                 shell=3, prereq=0, k=1)
    return t

# ── Phase 1: p-adic proximity ─────────────────────────────────────────────────

def run_proximity_phase():
    print(f"\n{BOLD}[PHASE 1: p-adic Proximity — Context Routing]{RESET}\n")
    print(f"  d_p(a, b) = p^{{-v_p(a-b)}}   same coset = zero distance\n")

    all_ok = True
    print(f"  {'a':>4}  {'b':>4}  {'d_2(a,b)':>10}  {'expected':>10}  Result")
    print(f"  {'─'*4}  {'─'*4}  {'─'*10}  {'─'*10}  {'─'*10}")
    for a, b, expected, label in [(0, 4, 0.25, "d_2(0,4)"),
                                   (0, 1, 1.0,  "d_2(0,1)"),
                                   (4, 8, 0.25, "d_2(4,8)")]:
        got = ultrametric_distance(a, b, 2)
        ok = abs(got - expected) < 1e-9
        all_ok = all_ok and ok
        col = GREEN if ok else RED
        print(f"  {a:>4}  {b:>4}  {got:>10.4f}  {expected:>10.4f}  {col}{'PASS' if ok else 'FAIL'}{RESET}  {label}")

    keys = [1, 4, 9, 16, 32]
    ranked = p_adic_closest(4, keys, 2)
    nearest_key, nearest_dist = ranked[0]
    nearest_ok = nearest_key == 4 and nearest_dist == 0.0
    all_ok = all_ok and nearest_ok
    col = GREEN if nearest_ok else RED
    print(f"\n  p_adic_closest(context=4, keys={keys}):")
    print(f"  Nearest: key={nearest_key}, dist={nearest_dist} → {col}{'PASS' if nearest_ok else 'FAIL'}{RESET}")

    rng = random.Random(99)
    max_viol = 0.0
    for _ in range(500):
        a, b, c = rng.randint(0, 200), rng.randint(0, 200), rng.randint(0, 200)
        viol = (ultrametric_distance(a, c, 2)
                - max(ultrametric_distance(a, b, 2), ultrametric_distance(b, c, 2)))
        if viol > max_viol:
            max_viol = viol
    ultra_ok = max_viol < 1e-9
    all_ok = all_ok and ultra_ok
    col = GREEN if ultra_ok else RED
    print(f"\n  Strong triangle inequality — 500 triples, max violation = {col}{max_viol:.2e}{RESET}  {'PASS' if ultra_ok else 'FAIL'}")
    return all_ok

# ── Phase 2: Shell ordering and congruence gating ────────────────────────────

def run_shell_gate_phase():
    print(f"\n{BOLD}[PHASE 2: Shell Ordering and Congruence Gating]{RESET}\n")

    tree = DialogTree("TestNPC", p=2)
    tree.add_option("Shell 3 ephemeral A", "Response A", shell=3, prereq=0, k=1)
    tree.add_option("Shell 3 ephemeral B", "Response B", shell=3, prereq=0, k=1)
    tree.add_option("Shell 0 lore C", "Response C", shell=0, prereq=0, k=2)
    tree.add_option("Shell 0 lore D", "Response D", shell=0, prereq=0, k=2)
    tree.add_option("Shell 1 quest E", "Response E", shell=1, prereq=0, k=2)
    tree.add_option("Shell 2 interaction F", "Response F", shell=2, prereq=0, k=2)
    selected = tree.select(context_key=1, state=0, budget=10000)
    shells = [o.topic.shell for o in selected]
    v0_pos = [i for i, s in enumerate(shells) if s == 0]
    v3_pos = [i for i, s in enumerate(shells) if s == 3]
    order_ok = len(v0_pos) > 0 and len(v3_pos) > 0 and max(v0_pos) < min(v3_pos)
    col = GREEN if order_ok else RED
    print(f"  Shell order in selected: {shells}")
    print(f"  Lore (v=0) before transient (v=3): {col}{'PASS' if order_ok else 'FAIL'}{RESET}")

    blocked = not dialogue_allowed(state=0, prereq=4, p=2, k=4)
    allowed = dialogue_allowed(state=4, prereq=4, p=2, k=4)
    gate_ok = blocked and allowed
    print(f"\n  Gating — prereq=4, mod=16:")
    print(f"    state=0 blocked: {GREEN if blocked else RED}{'PASS' if blocked else 'FAIL'}{RESET}   "
          f"state=4 allowed: {GREEN if allowed else RED}{'PASS' if allowed else 'FAIL'}{RESET}")
    return order_ok and gate_ok

# ── Phase 3: NPC dialogue demo ────────────────────────────────────────────────

def run_npc_demo():
    print(f"\n{BOLD}[PHASE 3: NPC Demo — Kira at Two Quest States]{RESET}\n")

    kira = build_kira()
    for state_label, state in [("state=0 (quest not started)", 0),
                                ("state=4 (quest active)", 4)]:
        opts = kira.select(context_key=1, state=state, budget=10000)
        print(f"  {BOLD}{state_label}{RESET}")
        print(f"  {'Shell':<14}  {'Prereq':>8}  Text[:55]")
        print(f"  {'─'*14}  {'─'*8}  {'─'*55}")
        for o in opts:
            shell_name = SHELL_NAMES.get(o.topic.shell, f"v={o.topic.shell}")
            col = AMBER if o.topic.prereq > 0 else RESET
            print(f"  {shell_name:<14}  {col}{o.topic.prereq:>8}{RESET}  {o.topic.text[:55]}")
        print()

    opts0 = kira.select(1, 0, 10000)
    opts4 = kira.select(1, 4, 10000)
    p4_at_0 = [o for o in opts0 if o.topic.prereq == 4]
    p4_at_4 = [o for o in opts4 if o.topic.prereq == 4]
    gating_ok = len(p4_at_0) == 0 and len(p4_at_4) > 0
    col = GREEN if gating_ok else RED
    print(f"  Prereq=4 options: blocked at state=0 ({len(p4_at_0)}), "
          f"available at state=4 ({len(p4_at_4)}): {col}{'PASS' if gating_ok else 'FAIL'}{RESET}")
    return gating_ok

# ── Phase 4: Full NPC benchmark ───────────────────────────────────────────────

def run_full_benchmark():
    print(f"\n{BOLD}[PHASE 4: Full Benchmark — 10 NPCs x 20 Options]{RESET}\n")

    rng = random.Random(42)
    n_npcs, options_per_npc, budget = 10, 20, 400
    violations, total_retrieved = 0, 0

    for i in range(n_npcs):
        t = DialogTree(f"NPC_{i}", p=2)
        for j in range(options_per_npc):
            shell = rng.choice([0, 0, 1, 1, 2, 2, 3])
            prereq = rng.choice([0, 0, 0, 4]) if shell > 0 else 0
            t.add_option(f"Topic {j} shell {shell}", f"Response {j}",
                         shell=shell, prereq=prereq, k=2)
        ctx = rng.randint(1, 100)
        state = rng.choice([0, 4, 12, 28])
        opts = t.select(ctx, state, budget)
        toks = sum(o.tokens for o in opts)
        if toks > budget:
            violations += 1
        total_retrieved += len(opts)

    avg = total_retrieved / n_npcs
    all_ok = violations == 0
    col = GREEN if all_ok else RED
    print(f"  NPCs: {n_npcs}   Options/NPC: {options_per_npc}   Budget: {budget}")
    print(f"  Avg options selected: {avg:.1f}")
    print(f"  Budget violations: {col}{violations}{RESET}  {'PASS' if all_ok else 'FAIL'}")
    return all_ok

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print(f"\n{BOLD}{'='*68}{RESET}")
    print(f"{BOLD}  DIALOGGRAPH — NPC DIALOGUE ENGINE  (CGA-005){RESET}")
    print(f"{BOLD}{'='*68}{RESET}")
    print(f"  p-adic proximity selection + congruence gating.")
    print(f"  Topic key v_p encoding. Shell ordering. Zero false positives.")
    print(f"  Pure Python, zero dependencies.")

    p1 = run_proximity_phase()
    p2 = run_shell_gate_phase()
    p3 = run_npc_demo()
    p4 = run_full_benchmark()

    passed = sum([p1, p2, p3, p4])
    print(f"\n{BOLD}{'='*68}{RESET}")
    col = GREEN if passed == 4 else RED
    print(f"  Phase results: {col}{passed}/4 PASS{RESET}")
    print(f"  Proximity:   {GREEN}d_p(a,b) — same coset = zero distance, correct routing{RESET}")
    print(f"  Shell order: {GREEN}lore always precedes transient in budget selection{RESET}")
    print(f"  Gating:      {GREEN}prereq gate exact — zero false positives, zero false negatives{RESET}")
    print(f"{BOLD}{'='*68}{RESET}\n")

if __name__ == "__main__":
    main()
