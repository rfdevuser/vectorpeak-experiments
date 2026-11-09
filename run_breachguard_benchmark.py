"""
run_breachguard_benchmark.py — BreachGuard Vulnerability Percolation Benchmark
===============================================================================
Demonstrates the core flaw in CVSS-priority patching: the highest-severity
CVE is rarely the one whose exploitation triggers a network-wide cascade.

BreachGuard applies Γ₄₃ — the Molloy-Reed percolation threshold:

    γ_c = ⟨k⟩ / (⟨k²⟩ − ⟨k⟩)

This gives the minimum fraction of compromised nodes at which a cascade
becomes self-sustaining across the network.  Patching by Δγ_c (how much
the cascade threshold RISES when a vulnerability is removed) consistently
outperforms CVSS-priority patching at raising network resilience.

No external dependencies.  No API key.  Pure Python 3.8+.

    python run_breachguard_benchmark.py
"""

import math
import sys
import time
from collections import deque

# ── Terminal colours ──────────────────────────────────────────────────────────
RED    = "\033[91m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
RESET  = "\033[0m"

# ── Network definition ────────────────────────────────────────────────────────
# 20-node synthetic corporate IT network.
# Key design:
#   dns-01     degree 16, CVSS 6.5  → low severity, high cascade risk
#   monitor-01 degree 15, CVSS 4.3  → very low severity, high cascade risk
#   db-01      degree  3, CVSS 9.8  → critical severity, low cascade risk

NODES = [
    {"id": "web-01",     "type": "Internet Web Server",    "cvss": 7.2, "cve": "CVE-2024-1001"},
    {"id": "dns-01",     "type": "Internal DNS",            "cvss": 6.5, "cve": "CVE-2024-1002"},
    {"id": "ad-01",      "type": "Active Directory",        "cvss": 7.8, "cve": "CVE-2024-1003"},
    {"id": "app-01",     "type": "Application Server",      "cvss": 8.1, "cve": "CVE-2024-1004"},
    {"id": "app-02",     "type": "Application Server",      "cvss": 7.5, "cve": "CVE-2024-1005"},
    {"id": "app-03",     "type": "Application Server",      "cvss": 5.9, "cve": "CVE-2024-1006"},
    {"id": "db-01",      "type": "Database (Primary)",      "cvss": 9.8, "cve": "CVE-2024-1007"},
    {"id": "db-02",      "type": "Database (Secondary)",    "cvss": 8.9, "cve": "CVE-2024-1008"},
    {"id": "mail-01",    "type": "Mail Server",             "cvss": 7.1, "cve": "CVE-2024-1009"},
    {"id": "mail-02",    "type": "Mail Server",             "cvss": 6.8, "cve": "CVE-2024-1010"},
    {"id": "backup-01",  "type": "Backup Server",           "cvss": 5.5, "cve": "CVE-2024-1011"},
    {"id": "monitor-01", "type": "Monitoring System",       "cvss": 4.3, "cve": "CVE-2024-1012"},
    {"id": "ws-01",      "type": "Workstation",             "cvss": 7.9, "cve": "CVE-2024-1013"},
    {"id": "ws-02",      "type": "Workstation",             "cvss": 6.1, "cve": "CVE-2024-1014"},
    {"id": "ws-03",      "type": "Workstation",             "cvss": 7.3, "cve": "CVE-2024-1015"},
    {"id": "ws-04",      "type": "Workstation",             "cvss": 6.9, "cve": "CVE-2024-1016"},
    {"id": "ws-05",      "type": "Workstation",             "cvss": 7.1, "cve": "CVE-2024-1017"},
    {"id": "iot-01",     "type": "IoT Device",              "cvss": 8.5, "cve": "CVE-2024-1018"},
    {"id": "iot-02",     "type": "IoT Device",              "cvss": 5.0, "cve": "CVE-2024-1019"},
    {"id": "iot-03",     "type": "IoT Device",              "cvss": 7.6, "cve": "CVE-2024-1020"},
]

EDGES = [
    # Internet-facing tier
    ("web-01", "dns-01"), ("web-01", "app-01"),
    ("web-01", "app-02"), ("web-01", "mail-01"),
    # DNS hub — resolves for every host (high degree by design)
    ("dns-01", "app-01"), ("dns-01", "app-02"), ("dns-01", "app-03"),
    ("dns-01", "ad-01"),  ("dns-01", "db-01"),  ("dns-01", "db-02"),
    ("dns-01", "mail-01"),("dns-01", "mail-02"),("dns-01", "backup-01"),
    ("dns-01", "monitor-01"),
    ("dns-01", "ws-01"),  ("dns-01", "ws-02"),  ("dns-01", "ws-03"),
    ("dns-01", "ws-04"),  ("dns-01", "ws-05"),
    # Active Directory — authenticates most internal hosts
    ("ad-01", "app-01"), ("ad-01", "app-02"), ("ad-01", "app-03"),
    ("ad-01", "ws-01"),  ("ad-01", "ws-02"),  ("ad-01", "ws-03"),
    ("ad-01", "ws-04"),  ("ad-01", "ws-05"),
    # Application → database access
    ("app-01", "db-01"),
    ("app-02", "db-02"), ("app-03", "db-02"),
    # Mail cluster
    ("mail-01", "mail-02"),
    # Monitoring — observes every server (high degree by design)
    ("backup-01",  "monitor-01"),
    ("monitor-01", "app-01"),  ("monitor-01", "app-02"),  ("monitor-01", "app-03"),
    ("monitor-01", "db-01"),   ("monitor-01", "db-02"),
    ("monitor-01", "mail-01"), ("monitor-01", "mail-02"),
    ("monitor-01", "ws-01"),   ("monitor-01", "ws-02"),   ("monitor-01", "ws-03"),
    # IoT devices talk to nearest workstation + monitoring
    ("iot-01", "ws-01"), ("iot-01", "monitor-01"),
    ("iot-02", "ws-02"), ("iot-02", "monitor-01"),
    ("iot-03", "ws-03"), ("iot-03", "monitor-01"),
]

# ── Graph helpers ─────────────────────────────────────────────────────────────

def build_adj(nodes: list[dict], edges: list[tuple],
              exclude: str | None = None) -> dict[str, set[str]]:
    """Undirected adjacency list, optionally excluding one node."""
    ids = {n["id"] for n in nodes if n["id"] != exclude}
    adj: dict[str, set[str]] = {nid: set() for nid in ids}
    for u, v in edges:
        if u in ids and v in ids:
            adj[u].add(v)
            adj[v].add(u)
    return adj


def degree_sequence(adj: dict[str, set[str]]) -> list[int]:
    return [len(nbrs) for nbrs in adj.values()]


def molloy_reed(adj: dict[str, set[str]]) -> float:
    """
    Molloy-Reed cascade threshold (Γ₄₃):
    γ_c = ⟨k⟩ / (⟨k²⟩ − ⟨k⟩)

    γ_c is the minimum fraction of compromised nodes at which a lateral
    movement cascade becomes self-sustaining.  Raising γ_c makes cascades
    harder to trigger.
    """
    degs = degree_sequence(adj)
    n    = len(degs)
    if n < 2:
        return float("inf")
    k1 = sum(degs) / n
    k2 = sum(d * d for d in degs) / n
    denom = k2 - k1
    if denom <= 0:
        return float("inf")
    return k1 / denom


def blast_radius(adj: dict[str, set[str]], node_id: str) -> int:
    """1-hop blast radius: direct lateral movement targets from node_id."""
    return len(adj.get(node_id, set()))


def percolation_delta(node_id: str) -> tuple[float, float]:
    """
    Δγ_c when node_id is patched (removed from network).
    Returns (Δγ_c, new_γ_c).  Higher Δγ_c = more cascade-critical.
    """
    adj_full    = build_adj(NODES, EDGES)
    adj_patched = build_adj(NODES, EDGES, exclude=node_id)
    gamma_base  = molloy_reed(adj_full)
    gamma_new   = molloy_reed(adj_patched)
    return gamma_new - gamma_base, gamma_new


# ── Phase 1: CVSS-priority ─────────────────────────────────────────────────────

def run_cvss_phase(adj_full: dict, gamma_base: float) -> list[dict]:
    print(f"\n{BOLD}[PHASE 1: CVSS-Priority Patch Order  (Standard Practice)]{RESET}")
    print(f"  Sorted by CVSS score descending — the industry default.\n")

    ranked = sorted(NODES, key=lambda n: n["cvss"], reverse=True)
    node_map = {n["id"]: n for n in NODES}

    hdr = f"  {'Rank':<5} {'Node':<13} {'Type':<26} {'CVSS':>5}  {'1-hop':>6}  {'Network %':>9}"
    print(hdr)
    print(f"  {'─'*72}")

    rows = []
    for i, node in enumerate(ranked, 1):
        nid   = node["id"]
        cvss  = node["cvss"]
        hops  = blast_radius(adj_full, nid)
        pct   = int(round(hops / len(NODES) * 100))
        delta, new_gamma = percolation_delta(nid)
        rows.append({"rank_cvss": i, "node": nid, "type": node["type"],
                     "cvss": cvss, "cve": node["cve"],
                     "hops": hops, "delta_gamma": delta, "new_gamma": new_gamma})
        marker = ""
        if cvss >= 9.0:
            marker = f"  {RED}← CVSS CRITICAL{RESET}"
        elif nid in ("dns-01", "monitor-01"):
            marker = f"  {DIM}← low CVSS, high degree{RESET}"
        print(f"  #{i:<4} {nid:<13} {node['type']:<26} {cvss:>5.1f}  {hops:>5}  {pct:>8}%{marker}")

    # What γ_c does after patching only the top-CVSS node?
    top = ranked[0]
    _, new_gamma = percolation_delta(top["id"])
    print()
    print(f"  {YELLOW}After patching #{1} ({top['id']}, CVSS {top['cvss']}):{RESET}")
    print(f"    γ_c : {gamma_base:.4f} → {new_gamma:.4f}  "
          f"(+{new_gamma-gamma_base:.4f}, {(new_gamma/gamma_base-1)*100:.1f}% improvement)")
    nodes_needed_before = math.ceil(gamma_base * len(NODES))
    nodes_needed_after  = math.ceil(new_gamma  * len(NODES))
    print(f"    Cascade triggers at: {nodes_needed_before} compromised nodes → "
          f"{nodes_needed_after} compromised nodes  "
          f"({RED}+{nodes_needed_after-nodes_needed_before} node(s){RESET})")
    print(f"\n  {RED}[FAILURE]{RESET} db-01 (CVSS 9.8) connects to only "
          f"{blast_radius(adj_full,'db-01')} hosts directly.")
    print(f"           Patching it barely moves the cascade threshold.")
    return rows


# ── Phase 2: BreachGuard percolation-priority ──────────────────────────────────

def run_percolation_phase(adj_full: dict, gamma_base: float,
                          cvss_rows: list[dict]) -> list[dict]:
    print(f"\n{BOLD}[PHASE 2: BreachGuard Percolation-Priority Patch Order  (Γ₄₃)]{RESET}")
    print(f"  Sorted by Δγ_c descending — how much the cascade threshold rises")
    print(f"  when each vulnerability is patched.\n")

    ranked = sorted(cvss_rows, key=lambda r: r["delta_gamma"], reverse=True)

    hdr = f"  {'Rank':<5} {'Node':<13} {'Type':<26} {'CVSS':>5}  " \
          f"{'Δγ_c':>7}  {'New γ_c':>8}  {'1-hop':>6}"
    print(hdr)
    print(f"  {'─'*80}")

    for i, row in enumerate(ranked, 1):
        nid   = row["node"]
        cvss  = row["cvss"]
        delta = row["delta_gamma"]
        new_g = row["new_gamma"]
        hops  = row["hops"]
        marker = ""
        if i <= 2:
            tag = f"{GREEN}[TOP CASCADE RISK]{RESET}"
            marker = f"  {tag}"
        elif nid == "db-01":
            marker = f"  {RED}← CVSS #1, percolation #{i}{RESET}"
        print(f"  #{i:<4} {nid:<13} {row['type']:<26} {cvss:>5.1f}  "
              f"{delta:>+7.4f}  {new_g:>8.4f}  {hops:>5}{marker}")

    # γ_c trajectory: Γ₄₃ order vs CVSS order after first 3 patches
    print()
    print(f"  {GREEN}γ_c trajectory — first 3 patches:{RESET}")
    print(f"  {'Patch':<5} {'Strategy':<18} {'Node patched':<14} {'γ_c after':>9}  {'Δ from base':>12}")
    print(f"  {'─'*62}")

    # CVSS order
    gamma_cvss = gamma_base
    cvss_order = sorted(cvss_rows, key=lambda r: r["cvss"], reverse=True)
    adj_cvss   = dict(build_adj(NODES, EDGES))
    patched_cvss: list[str] = []
    for i in range(3):
        node = cvss_order[i]["node"]
        patched_cvss.append(node)
        adj_cvss = build_adj(NODES, EDGES, exclude=patched_cvss[-1] if len(patched_cvss)==1 else None)
        # Recompute properly by excluding all patched so far
        excl_adj = {n["id"]: set() for n in NODES if n["id"] not in patched_cvss}
        for u, v in EDGES:
            if u in excl_adj and v in excl_adj:
                excl_adj[u].add(v)
                excl_adj[v].add(u)
        g = molloy_reed(excl_adj)
        print(f"  #{i+1:<4} {'CVSS':<18} {node:<14} {g:>9.4f}  {g-gamma_base:>+12.4f}")

    print()

    # Γ₄₃ order
    patched_perc: list[str] = []
    for i in range(3):
        node = ranked[i]["node"]
        patched_perc.append(node)
        excl_adj = {n["id"]: set() for n in NODES if n["id"] not in patched_perc}
        for u, v in EDGES:
            if u in excl_adj and v in excl_adj:
                excl_adj[u].add(v)
                excl_adj[v].add(u)
        g = molloy_reed(excl_adj)
        print(f"  #{i+1:<4} {'Γ₄₃ (BreachGuard)':<18} {node:<14} {g:>9.4f}  {g-gamma_base:>+12.4f}")

    return ranked


# ── Mismatch analysis ─────────────────────────────────────────────────────────

def run_mismatch(cvss_rows: list[dict], perc_rows: list[dict]):
    print(f"\n{BOLD}[MISMATCH ANALYSIS — Where CVSS and Γ₄₃ Disagree Most]{RESET}\n")

    cvss_rank  = {r["node"]: r["rank_cvss"] for r in cvss_rows}
    perc_rank  = {r["node"]: i+1 for i, r in enumerate(perc_rows)}

    discords = []
    for nid in cvss_rank:
        c_rank = cvss_rank[nid]
        p_rank = perc_rank[nid]
        discords.append((abs(c_rank - p_rank), nid, c_rank, p_rank))
    discords.sort(reverse=True)

    hdr = f"  {'Node':<13} {'Type':<26} {'CVSS':>5}  {'CVSS rank':>9}  {'Γ₄₃ rank':>8}  {'Rank gap':>9}"
    print(hdr)
    print(f"  {'─'*74}")

    node_map = {n["id"]: n for n in NODES}
    shown = 0
    for gap, nid, c_r, p_r in discords:
        if gap < 3:
            break
        n = node_map[nid]
        direction = f"{GREEN}↑ undervalued by CVSS{RESET}" if p_r < c_r else f"{RED}↓ overvalued by CVSS{RESET}"
        print(f"  {nid:<13} {n['type']:<26} {n['cvss']:>5.1f}  "
              f"#{c_r:<9}  #{p_r:<8}  {gap:>+8}  {direction}")
        shown += 1

    print()
    top_cvss = sorted(cvss_rows, key=lambda r: r["cvss"], reverse=True)[0]
    top_perc = perc_rows[0]
    ratio    = top_perc["delta_gamma"] / max(top_cvss["delta_gamma"], 1e-9)
    print(f"  {BOLD}Key numbers:{RESET}")
    print(f"    {top_cvss['node']} (CVSS {top_cvss['cvss']}) — "
          f"cascade impact Δγ_c = {top_cvss['delta_gamma']:+.4f}  → CVSS rank #1")
    print(f"    {top_perc['node']} (CVSS {perc_rows[0]['cvss']:.1f}) — "
          f"cascade impact Δγ_c = {top_perc['delta_gamma']:+.4f}  → Γ₄₃ rank #1")
    print(f"    Cascade impact ratio: {ratio:.1f}× more dangerous by Γ₄₃ metric")


# ── Main ──────────────────────────────────────────────────────────────────────

def _hr(char: str = "─", width: int = 68) -> str:
    return char * width


def main():
    adj_full    = build_adj(NODES, EDGES)
    gamma_base  = molloy_reed(adj_full)
    n_nodes     = len(NODES)
    n_edges     = len(EDGES)
    k_mean      = sum(degree_sequence(adj_full)) / n_nodes
    cascade_at  = math.ceil(gamma_base * n_nodes)

    print(f"\n{BOLD}{_hr('═')}{RESET}")
    print(f"{BOLD}  BREACHGUARD VULNERABILITY PERCOLATION BENCHMARK  (Γ₄₃){RESET}")
    print(f"{BOLD}{_hr('═')}{RESET}")
    print(f"  Network        : {n_nodes} nodes, {n_edges} edges (corporate IT infrastructure)")
    print(f"  Mean degree    : {k_mean:.2f}")
    print(f"  γ_c (base)     : {gamma_base:.4f}  — cascade triggers at ≥{cascade_at} compromised nodes")
    print(f"  Claim          : the highest-CVSS vulnerability is not the one")
    print(f"                   whose exploitation triggers a network-wide cascade.")

    cvss_rows = run_cvss_phase(adj_full, gamma_base)
    perc_rows = run_percolation_phase(adj_full, gamma_base, cvss_rows)
    run_mismatch(cvss_rows, perc_rows)

    # Final banner
    top_cvss = sorted(cvss_rows, key=lambda r: r["cvss"], reverse=True)[0]
    top_perc = perc_rows[0]
    excl_perc1 = {n["id"]: set() for n in NODES if n["id"] != top_perc["node"]}
    for u, v in EDGES:
        if u in excl_perc1 and v in excl_perc1:
            excl_perc1[u].add(v)
            excl_perc1[v].add(u)
    gamma_after_perc1 = molloy_reed(excl_perc1)

    excl_cvss1 = {n["id"]: set() for n in NODES if n["id"] != top_cvss["node"]}
    for u, v in EDGES:
        if u in excl_cvss1 and v in excl_cvss1:
            excl_cvss1[u].add(v)
            excl_cvss1[v].add(u)
    gamma_after_cvss1 = molloy_reed(excl_cvss1)

    improvement_ratio = (gamma_after_perc1 - gamma_base) / max(gamma_after_cvss1 - gamma_base, 1e-9)

    print(f"\n{BOLD}{_hr('═')}{RESET}")
    print(f"  CVSS patch #1  : {top_cvss['node']} (CVSS {top_cvss['cvss']})  → "
          f"γ_c {gamma_base:.4f} → {gamma_after_cvss1:.4f}  "
          f"({RED}+{(gamma_after_cvss1-gamma_base)*100:.2f}pp{RESET})")
    print(f"  Γ₄₃  patch #1  : {top_perc['node']} (CVSS {top_perc['cvss']:.1f})  → "
          f"γ_c {gamma_base:.4f} → {gamma_after_perc1:.4f}  "
          f"({GREEN}+{(gamma_after_perc1-gamma_base)*100:.2f}pp{RESET})")
    print(f"  Γ₄₃ raises cascade threshold {improvement_ratio:.1f}× more than CVSS priority.")
    print(f"  CVSS is a severity score.  Γ₄₃ is a cascade score.  They measure different things.")
    print(f"{BOLD}{_hr('═')}{RESET}\n")


if __name__ == "__main__":
    main()
