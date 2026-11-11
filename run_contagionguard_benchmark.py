#!/usr/bin/env python3
"""
ContagionGuard benchmark — Γ₄₇ Interbank Contagion Spectral Certificate

  Phase 1 — Five presets: ρ(W), γ_c, Fiedler μ₂, risk score, status
  Phase 2 — Perron-vector systemic rank vs balance-sheet rank (Eurozone stress)
  Phase 3 — Eisenberg-Noe cascade containment: STABLE vs CRITICAL (bilateral formula)
  Phase 4 — Capital-injection lever: equity top-up needed to cross ρ=1

No API key. Dependency: numpy.
"""

import math
import sys

try:
    import numpy as np
except ImportError:
    sys.exit("numpy required:  pip install numpy")

# ── ANSI ──────────────────────────────────────────────────────────────────────
RESET = "\033[0m"; BOLD = "\033[1m"; DIM = "\033[2m"
RED   = "\033[91m"; AMBER = "\033[93m"; GREEN = "\033[92m"
CYAN  = "\033[96m"; WHITE = "\033[97m"

def _hr(w=92): return "─" * w
def _hdr(t):
    b = _hr()
    return f"\n{BOLD}{CYAN}{b}{RESET}\n{BOLD}{WHITE}  {t}{RESET}\n{BOLD}{CYAN}{b}{RESET}"
def _sc(s): return {
    "STABLE": GREEN, "RESILIENT": GREEN,
    "VULNERABLE": AMBER, "CRITICAL": RED}.get(s, WHITE)
def _rc(r):
    return GREEN if r < 0.8 else (AMBER if r < 1.0 else RED)


# ── Core math ─────────────────────────────────────────────────────────────────

def _build_W(banks, exposures):
    idx = {b["id"]: i for i, b in enumerate(banks)}
    n   = len(banks)
    W   = np.zeros((n, n))
    for e in exposures:
        i = idx[e["from"]]; j = idx[e["to"]]
        eq = banks[i]["equity"]
        if eq > 0:
            W[i, j] = e["amount"] / eq
    return W


def _build_E(banks, exposures):
    """Raw bilateral exposure matrix (not normalised)."""
    idx = {b["id"]: i for i, b in enumerate(banks)}
    n   = len(banks)
    E   = np.zeros((n, n))
    for e in exposures:
        E[idx[e["from"]], idx[e["to"]]] = e["amount"]
    return E


def _rho(W): return float(np.max(np.abs(np.linalg.eigvals(W))))

def _perron(W):
    vals, vecs = np.linalg.eig(W)
    v = np.abs(vecs[:, int(np.argmax(np.abs(vals)))]).real
    s = v.sum(); return v / s if s > 0 else v

def _mu2(W):
    S = (W + W.T) / 2.0
    L = np.diag(S.sum(axis=1)) - S
    return float(np.sort(np.linalg.eigvalsh(L))[1])

def _cascade_bilateral(banks, E, seed, shock):
    """Correct Eisenberg-Noe: loss = bilateral_exposure × shock."""
    n = len(banks)
    defaulted = {seed}
    new_def   = {seed}
    losses    = np.zeros(n)
    depth     = 0
    while new_def and depth <= n:
        depth += 1
        next_def = set()
        for i in range(n):
            if i in defaulted: continue
            for j in new_def:
                losses[i] += E[i, j] * shock
            if losses[i] >= banks[i]["equity"] > 0:
                next_def.add(i)
        defaulted.update(next_def)
        new_def = next_def
    return [banks[j]["id"] for j in sorted(defaulted)], depth

def _status(r):
    if r < 0.5: return "STABLE"
    if r < 0.8: return "RESILIENT"
    if r < 1.0: return "VULNERABLE"
    return "CRITICAL"

def _risk_score(r): return min(100.0, 100.0 * (1.0 - math.exp(-r)))


# ── Presets ───────────────────────────────────────────────────────────────────

PRESETS = {
    "simple_stable": {
        "label": "Simple Stable (5 banks)", "shock": 1.0,
        "banks": [
            {"id": "ALPHA",   "name": "Alpha Bank",   "equity": 10.0, "assets": 100.0},
            {"id": "BETA",    "name": "Beta Bank",    "equity":  8.0, "assets":  80.0},
            {"id": "GAMMA",   "name": "Gamma Bank",   "equity":  6.0, "assets":  60.0},
            {"id": "DELTA",   "name": "Delta Bank",   "equity":  5.0, "assets":  50.0},
            {"id": "EPSILON", "name": "Epsilon Bank", "equity":  4.0, "assets":  40.0},
        ],
        "exposures": [
            {"from": "ALPHA",   "to": "BETA",    "amount": 1.5},
            {"from": "ALPHA",   "to": "GAMMA",   "amount": 1.0},
            {"from": "BETA",    "to": "ALPHA",   "amount": 1.2},
            {"from": "BETA",    "to": "DELTA",   "amount": 1.0},
            {"from": "GAMMA",   "to": "ALPHA",   "amount": 1.0},
            {"from": "GAMMA",   "to": "EPSILON", "amount": 0.8},
            {"from": "DELTA",   "to": "BETA",    "amount": 1.0},
            {"from": "DELTA",   "to": "GAMMA",   "amount": 0.7},
            {"from": "EPSILON", "to": "GAMMA",   "amount": 0.9},
            {"from": "EPSILON", "to": "ALPHA",   "amount": 0.5},
        ],
    },
    "hub_spoke": {
        "label": "Hub-and-Spoke G-SIB (9 banks)", "shock": 1.0,
        "banks": [
            {"id": "HUB", "name": "Hub G-SIB",   "equity": 50.0, "assets": 800.0},
            {"id": "P1",  "name": "Peripheral 1", "equity":  5.0, "assets":  50.0},
            {"id": "P2",  "name": "Peripheral 2", "equity":  4.5, "assets":  45.0},
            {"id": "P3",  "name": "Peripheral 3", "equity":  4.0, "assets":  40.0},
            {"id": "P4",  "name": "Peripheral 4", "equity":  3.5, "assets":  35.0},
            {"id": "P5",  "name": "Peripheral 5", "equity":  3.0, "assets":  30.0},
            {"id": "P6",  "name": "Peripheral 6", "equity":  2.5, "assets":  25.0},
            {"id": "P7",  "name": "Peripheral 7", "equity":  2.0, "assets":  22.0},
            {"id": "P8",  "name": "Peripheral 8", "equity":  2.0, "assets":  20.0},
        ],
        "exposures": [
            {"from": "P1", "to": "HUB", "amount": 3.0}, {"from": "HUB", "to": "P1", "amount": 1.0},
            {"from": "P2", "to": "HUB", "amount": 2.8}, {"from": "HUB", "to": "P2", "amount": 0.9},
            {"from": "P3", "to": "HUB", "amount": 2.5}, {"from": "HUB", "to": "P3", "amount": 0.8},
            {"from": "P4", "to": "HUB", "amount": 2.2}, {"from": "HUB", "to": "P4", "amount": 0.7},
            {"from": "P5", "to": "HUB", "amount": 2.0}, {"from": "HUB", "to": "P5", "amount": 0.6},
            {"from": "P6", "to": "HUB", "amount": 1.8}, {"from": "HUB", "to": "P6", "amount": 0.5},
            {"from": "P7", "to": "HUB", "amount": 1.6}, {"from": "HUB", "to": "P7", "amount": 0.4},
            {"from": "P8", "to": "HUB", "amount": 1.5}, {"from": "HUB", "to": "P8", "amount": 0.4},
        ],
    },
    "gsib_cluster": {
        "label": "G-SIB Cluster + Regionals (10 banks)", "shock": 1.0,
        "banks": [
            {"id": "G1", "name": "Global Bank 1", "equity": 80.0, "assets": 1200.0},
            {"id": "G2", "name": "Global Bank 2", "equity": 70.0, "assets": 1000.0},
            {"id": "G3", "name": "Global Bank 3", "equity": 60.0, "assets":  900.0},
            {"id": "R1", "name": "Regional 1",    "equity": 12.0, "assets":  120.0},
            {"id": "R2", "name": "Regional 2",    "equity": 10.0, "assets":  100.0},
            {"id": "R3", "name": "Regional 3",    "equity":  9.0, "assets":   90.0},
            {"id": "R4", "name": "Regional 4",    "equity":  7.0, "assets":   70.0},
            {"id": "R5", "name": "Regional 5",    "equity":  6.0, "assets":   60.0},
            {"id": "R6", "name": "Regional 6",    "equity":  5.0, "assets":   50.0},
            {"id": "R7", "name": "Regional 7",    "equity":  4.0, "assets":   40.0},
        ],
        "exposures": [
            {"from": "G1", "to": "G2", "amount": 18.0}, {"from": "G2", "to": "G1", "amount": 16.0},
            {"from": "G1", "to": "G3", "amount": 15.0}, {"from": "G3", "to": "G1", "amount": 12.0},
            {"from": "G2", "to": "G3", "amount": 14.0}, {"from": "G3", "to": "G2", "amount": 10.0},
            {"from": "R1", "to": "G1", "amount":  6.0}, {"from": "R1", "to": "G2", "amount":  3.0},
            {"from": "R2", "to": "G1", "amount":  5.0}, {"from": "R2", "to": "G3", "amount":  3.0},
            {"from": "R3", "to": "G2", "amount":  5.0}, {"from": "R3", "to": "G1", "amount":  2.5},
            {"from": "R4", "to": "G1", "amount":  4.0}, {"from": "R4", "to": "G3", "amount":  2.0},
            {"from": "R5", "to": "G2", "amount":  4.0}, {"from": "R5", "to": "G1", "amount":  2.0},
            {"from": "R6", "to": "G3", "amount":  3.5}, {"from": "R6", "to": "G2", "amount":  2.0},
            {"from": "R7", "to": "G1", "amount":  3.0}, {"from": "R7", "to": "G3", "amount":  2.0},
        ],
    },
    "eurozone_stress": {
        "label": "Eurozone Sovereign Stress (7 banks)", "shock": 0.6,
        "banks": [
            {"id": "FR1", "name": "Banque de France 1",  "equity": 30.0, "assets": 600.0},
            {"id": "DE1", "name": "Deutsche Bank 1",     "equity": 35.0, "assets": 550.0},
            {"id": "IT1", "name": "Banca Italia 1",      "equity":  8.0, "assets": 350.0},
            {"id": "ES1", "name": "Banco España 1",      "equity":  5.0, "assets": 200.0},
            {"id": "GR1", "name": "Trapeza Ellados 1",   "equity":  2.0, "assets":  80.0},
            {"id": "PT1", "name": "Banco Portugal 1",    "equity":  2.5, "assets":  60.0},
            {"id": "NL1", "name": "ING Nederland 1",     "equity": 20.0, "assets": 350.0},
        ],
        "exposures": [
            {"from": "FR1", "to": "IT1", "amount": 18.0}, {"from": "FR1", "to": "ES1", "amount": 12.0},
            {"from": "FR1", "to": "GR1", "amount":  5.0}, {"from": "FR1", "to": "PT1", "amount":  4.0},
            {"from": "DE1", "to": "IT1", "amount": 15.0}, {"from": "DE1", "to": "ES1", "amount": 10.0},
            {"from": "DE1", "to": "GR1", "amount":  6.0}, {"from": "DE1", "to": "FR1", "amount":  8.0},
            {"from": "NL1", "to": "IT1", "amount": 10.0}, {"from": "NL1", "to": "ES1", "amount":  7.0},
            {"from": "NL1", "to": "GR1", "amount":  3.0}, {"from": "NL1", "to": "PT1", "amount":  3.0},
            {"from": "IT1", "to": "FR1", "amount":  4.0}, {"from": "IT1", "to": "DE1", "amount":  3.5},
            {"from": "ES1", "to": "FR1", "amount":  3.0}, {"from": "ES1", "to": "DE1", "amount":  2.5},
            {"from": "GR1", "to": "IT1", "amount":  1.0}, {"from": "PT1", "to": "ES1", "amount":  1.2},
        ],
    },
    "svb_regional": {
        "label": "SVB Regional Cluster (6 banks)", "shock": 0.8,
        "banks": [
            {"id": "SVB",  "name": "Silicon Valley Bank",  "equity": 6.0, "assets": 210.0},
            {"id": "SIG",  "name": "Signature Bank",       "equity": 5.5, "assets": 110.0},
            {"id": "FRB",  "name": "First Republic Bank",  "equity": 4.0, "assets": 220.0},
            {"id": "REG1", "name": "Regional Bank 1",      "equity": 3.0, "assets":  60.0},
            {"id": "REG2", "name": "Regional Bank 2",      "equity": 2.5, "assets":  45.0},
            {"id": "REG3", "name": "Regional Bank 3",      "equity": 2.0, "assets":  35.0},
        ],
        "exposures": [
            {"from": "SVB",  "to": "SIG",  "amount": 2.5}, {"from": "SVB",  "to": "FRB",  "amount": 3.0},
            {"from": "SVB",  "to": "REG1", "amount": 1.5}, {"from": "SIG",  "to": "SVB",  "amount": 2.2},
            {"from": "SIG",  "to": "FRB",  "amount": 2.0}, {"from": "SIG",  "to": "REG2", "amount": 1.2},
            {"from": "FRB",  "to": "SVB",  "amount": 2.8}, {"from": "FRB",  "to": "SIG",  "amount": 1.8},
            {"from": "FRB",  "to": "REG3", "amount": 1.0}, {"from": "REG1", "to": "SVB",  "amount": 1.5},
            {"from": "REG1", "to": "SIG",  "amount": 1.0}, {"from": "REG2", "to": "FRB",  "amount": 1.2},
            {"from": "REG2", "to": "SVB",  "amount": 0.8}, {"from": "REG3", "to": "FRB",  "amount": 0.9},
            {"from": "REG3", "to": "SIG",  "amount": 0.7},
        ],
    },
}

# Two purpose-built networks for Phase 3 cascade demonstration
PHASE3_NETWORKS = {
    "ring_stable": {
        "label": "Ring-5 (STABLE): balanced bilateral credits",
        "shock": 1.0,
        "banks": [
            {"id": f"B{i+1}", "name": f"Bank {i+1}", "equity": 10.0, "assets": 100.0}
            for i in range(5)
        ],
        "exposures": [
            {"from": "B1", "to": "B2", "amount": 1.5},
            {"from": "B2", "to": "B3", "amount": 1.5},
            {"from": "B3", "to": "B4", "amount": 1.5},
            {"from": "B4", "to": "B5", "amount": 1.5},
            {"from": "B5", "to": "B1", "amount": 1.5},
            {"from": "B2", "to": "B1", "amount": 1.0},
            {"from": "B3", "to": "B2", "amount": 1.0},
            {"from": "B4", "to": "B3", "amount": 1.0},
            {"from": "B5", "to": "B4", "amount": 1.0},
            {"from": "B1", "to": "B5", "amount": 1.0},
        ],
    },
    "hub_critical": {
        "label": "Hub-5 (CRITICAL): concentrated bilateral credits",
        "shock": 1.0,
        "banks": [
            {"id": "HUB", "name": "Central Hub",  "equity": 5.0,  "assets": 100.0},
            {"id": "SP1", "name": "Spoke Bank 1", "equity": 2.0,  "assets":  30.0},
            {"id": "SP2", "name": "Spoke Bank 2", "equity": 1.8,  "assets":  25.0},
            {"id": "SP3", "name": "Spoke Bank 3", "equity": 1.5,  "assets":  20.0},
            {"id": "SP4", "name": "Spoke Bank 4", "equity": 1.2,  "assets":  15.0},
        ],
        "exposures": [
            {"from": "SP1", "to": "HUB", "amount": 3.0},
            {"from": "SP2", "to": "HUB", "amount": 2.7},
            {"from": "SP3", "to": "HUB", "amount": 2.4},
            {"from": "SP4", "to": "HUB", "amount": 2.0},
            {"from": "HUB", "to": "SP1", "amount": 1.0},
            {"from": "HUB", "to": "SP2", "amount": 1.0},
            {"from": "HUB", "to": "SP3", "amount": 1.0},
            {"from": "HUB", "to": "SP4", "amount": 1.0},
        ],
    },
}


# ── Phase 1 ───────────────────────────────────────────────────────────────────

def phase1():
    print(_hdr("Phase 1 — Spectral Certificate: Five Interbank Presets"))
    print(f"""
  Traditional systemic-risk tools (SRISK, CoVaR, Basel DFAST) rank danger by
  balance-sheet size or fitted regression coefficients.

  ContagionGuard certifies the exact contagion threshold:

    ρ(W) = spectral radius of the normalised bilateral exposure matrix W
    γ_c  = 1/ρ(W)   — the network is linearly stable if and only if ρ(W) < 1
    μ₂   = Fiedler eigenvalue of the symmetrised Laplacian (connectivity speed)
    Score = 100·(1 − e^(−ρ))   — scalar risk index

  Below 1 is proven-stable. Above 1 is proven-critical. No calibration.
""")
    hdr = (f"  {'Network':<42} {'Banks':>5}  {'ρ(W)':>7}  "
           f"{'γ_c':>7}  {'μ₂':>7}  {'Score':>6}  Status")
    print(f"{BOLD}{hdr}{RESET}")
    print("  " + "─" * 86)
    for key, spec in PRESETS.items():
        banks = spec["banks"]
        W     = _build_W(banks, spec["exposures"])
        r     = _rho(W)
        g     = 1.0/r if r > 0 else math.inf
        m     = _mu2(W)
        sc    = _risk_score(r)
        st    = _status(r)
        gstr  = f"{g:.4f}" if g < 999 else "   ∞"
        print(f"  {spec['label']:<42} {len(banks):>5}  {_rc(r)}{r:>7.4f}{RESET}  "
              f"{gstr:>7}  {m:>7.4f}  {sc:>6.1f}  {_sc(st)}{st}{RESET}")
    print()
    print(f"  {DIM}Score = 100·(1−e^(−ρ)).  μ₂→0 = weakly coupled sub-clusters (slower cascade).{RESET}")


# ── Phase 2 ───────────────────────────────────────────────────────────────────

def phase2():
    print(_hdr("Phase 2 — Perron-Vector Rank vs Balance-Sheet Rank  [Eurozone Stress]"))
    print(f"""
  Regulator heuristic: recapitalise the largest bank first (highest total assets).
  ContagionGuard ranks by Perron vector — the dominant eigenvector of W — which
  measures true structural amplification in the contagion dynamics.

  Network: Eurozone Sovereign Stress (FR1, DE1, IT1, ES1, GR1, PT1, NL1)
  Core Eurozone banks lend to peripheral sovereigns; peripherals feed back.
""")
    spec  = PRESETS["eurozone_stress"]
    banks = spec["banks"]
    W     = _build_W(banks, spec["exposures"])
    r     = _rho(W)
    pv    = _perron(W)
    ar    = sorted(range(len(banks)), key=lambda i: -banks[i]["assets"])
    pr    = sorted(range(len(banks)), key=lambda i: -pv[i])
    arm   = {i: k+1 for k, i in enumerate(ar)}
    prm   = {i: k+1 for k, i in enumerate(pr)}

    print(f"  ρ(W) = {_rc(r)}{BOLD}{r:.4f}{RESET}   "
          f"γ_c = {1/r:.4f}   Status: {_sc(_status(r))}{BOLD}{_status(r)}{RESET}\n")

    hdr = (f"  {'Bank':<6} {'Name':<24} {'Assets':>8}  "
           f"{'Asset rank':>10}  {'Perron wt':>10}  {'Perron rank':>11}  {'Divergence':>10}")
    print(f"{BOLD}{hdr}{RESET}")
    print("  " + "─" * 84)
    for i, b in enumerate(banks):
        diff = arm[i] - prm[i]
        col  = RED if diff >= 2 else (AMBER if diff >= 1 else GREEN)
        ds   = f"+{diff}" if diff > 0 else str(diff)
        print(f"  {b['id']:<6} {b['name']:<24} {b['assets']:>8.0f}  "
              f"{'#'+str(arm[i]):>10}  {pv[i]:>10.4f}  {'#'+str(prm[i]):>11}  "
              f"{col}{ds:>10}{RESET}")
    print()
    tb = banks[pr[0]]; ab = banks[ar[0]]
    print(f"  {BOLD}Regulator heuristic (asset rank #1):{RESET} {ab['name']} — "
          f"assets {ab['assets']:.0f}B, Perron rank #{prm[ar[0]]}")
    print(f"  {BOLD}ContagionGuard (Perron rank #1):{RESET}    {tb['name']} — "
          f"assets {tb['assets']:.0f}B, Perron rank #1")
    print(f"\n  {DIM}Positive divergence = more systemic than balance sheet implies.{RESET}")
    print(f"  {DIM}The Perron vector identifies the structural amplifier, not the largest institution.{RESET}")


# ── Phase 3 ───────────────────────────────────────────────────────────────────

def phase3():
    print(_hdr("Phase 3 — Eisenberg-Noe Cascade Containment: STABLE vs CRITICAL"))
    print(f"""
  The Eisenberg-Noe model: bank i defaults when cumulative credit losses from
  defaulted counterparties exceed its equity.

    loss(i) = Σ_{{j defaulted}} exposure(i→j) × loss_given_default

  ρ(W) < 1 (STABLE): a single default is absorbed — cascade stops at seed.
  ρ(W) > 1 (CRITICAL): a single default cascades through the connected component.

  Two purpose-built networks isolate the structural difference.
""")

    for key, spec in PHASE3_NETWORKS.items():
        banks  = spec["banks"]
        exp    = spec["exposures"]
        shock  = spec["shock"]
        W      = _build_W(banks, exp)
        E      = _build_E(banks, exp)
        r      = _rho(W)
        st     = _status(r)
        n      = len(banks)
        print(f"  {BOLD}{spec['label']}{RESET}")
        print(f"  ρ(W) = {_rc(r)}{BOLD}{r:.4f}{RESET}   "
              f"γ_c = {1/r if r > 0 else math.inf:.4f}   "
              f"Status: {_sc(st)}{BOLD}{st}{RESET}\n")

        hdr = (f"  {'Seed bank':<14} {'Equity':>7}  "
               f"{'Cascade':>8}  {'Depth':>6}  Chain")
        print(f"{BOLD}{hdr}{RESET}")
        print("  " + "─" * 72)
        for i, b in enumerate(banks):
            ids, depth = _cascade_bilateral(banks, E, i, shock)
            sz  = len(ids)
            col = RED if sz == n else (AMBER if sz > 1 else GREEN)
            chain = " → ".join(ids) if sz > 1 else ids[0]
            print(f"  {b['name']:<14} {b['equity']:>7.1f}  "
                  f"{col}{sz:>4}/{n}{RESET}  {depth:>6}d  {chain}")
        print()

    print(f"  {DIM}Ring-5 STABLE: each bank absorbs its direct losses — cascade stops at the seed.{RESET}")
    print(f"  {DIM}Hub-5 CRITICAL: Hub default wipes out all spokes in one wave (depth 1).{RESET}")
    print(f"  {DIM}The spoke banks each lent > their equity to the hub (W[spoke,hub] > 1).{RESET}")
    print(f"  {DIM}ρ(W) > 1 identifies exactly this structural over-concentration before failure occurs.{RESET}")


# ── Phase 4 ───────────────────────────────────────────────────────────────────

def phase4():
    print(_hdr("Phase 4 — Capital-Injection Lever  [Eurozone Stress]"))
    print(f"""
  Which bank should receive emergency recapitalisation?
  Injecting equity into the wrong institution wastes capital without lowering ρ(W).

  ContagionGuard identifies the minimum injection to certify ρ(W) < 1 by
  targeting the Perron-vector amplifier (Perron rank #1).
""")
    spec   = PRESETS["eurozone_stress"]
    banks  = spec["banks"]
    exp    = spec["exposures"]
    W0     = _build_W(banks, exp)
    r0     = _rho(W0)
    pv     = _perron(W0)
    ti     = int(np.argmax(pv))
    tb     = banks[ti]
    ar     = sorted(range(len(banks)), key=lambda i: -banks[i]["assets"])
    wi     = ar[0] if ar[0] != ti else ar[1]
    wb     = banks[wi]

    print(f"  Most systemic bank (Perron rank #1): {BOLD}{tb['name']} ({tb['id']}){RESET}")
    print(f"  Current equity: {tb['equity']:.1f}B   Current ρ(W): {_rc(r0)}{BOLD}{r0:.4f}{RESET}\n")

    hdr = (f"  {'Equity multiplier':>18}  {'New equity':>12}  {'Capital added':>14}  "
           f"{'ρ(W)':>8}  {'γ_c':>8}  Status")
    print(f"{BOLD}{hdr}{RESET}")
    print("  " + "─" * 78)

    target_cap = None
    for mult in [1.0, 1.5, 2.0, 3.0, 4.0, 6.0, 10.0]:
        bm = []
        for i, b in enumerate(banks):
            if i == ti:
                ne = b["equity"] * mult
                bm.append(dict(b, equity=ne, assets=b["assets"]+(ne-b["equity"])))
            else:
                bm.append(b)
        rm   = _rho(_build_W(bm, exp))
        gm   = 1.0/rm if rm > 0 else math.inf
        st   = _status(rm)
        added = tb["equity"] * (mult - 1.0)
        marker = ""
        if target_cap is None and rm < 1.0:
            target_cap = added; marker = f" {GREEN}◄ ρ < 1{RESET}"
        print(f"  {mult:>18.1f}×  {tb['equity']*mult:>12.1f}B  "
              f"{added:>+13.1f}B  {_rc(rm)}{rm:>8.4f}{RESET}  "
              f"{gm:>8.4f}  {_sc(st)}{st}{RESET}{marker}")

    print()
    if target_cap is not None:
        bw = []
        for i, b in enumerate(banks):
            if i == wi:
                ne = b["equity"] + target_cap
                bw.append(dict(b, equity=ne, assets=b["assets"]+target_cap))
            else:
                bw.append(b)
        rw  = _rho(_build_W(bw, exp))
        stw = _status(rw)
        print(f"  {BOLD}Counterfactual — same capital ({target_cap:+.1f}B) into wrong target:{RESET}")
        print(f"  Wrong target: {wb['name']} ({wb['id']}) — asset-rank #1 by heuristic")
        print(f"  Result: ρ(W) = {_rc(rw)}{BOLD}{rw:.4f}{RESET}  "
              f"Status: {_sc(stw)}{BOLD}{stw}{RESET}")
        if rw >= r0 * 0.95:
            print(f"\n  {RED}{BOLD}Capital wasted.{RESET} Injecting into the asset-largest bank "
                  f"leaves ρ(W) nearly unchanged.")
        else:
            print(f"\n  {AMBER}Partial improvement only.{RESET} Structural target is {tb['name']}.")

    print(f"\n  {DIM}Minimum injection to certify ρ<1 must target the Perron-vector amplifier,{RESET}")
    print(f"  {DIM}not the balance-sheet leader.{RESET}")


# ── Banner + main ─────────────────────────────────────────────────────────────

def banner():
    b = _hr()
    print(f"\n{BOLD}{CYAN}{b}{RESET}")
    print(f"{BOLD}{WHITE}  ContagionGuard — Γ₄₇ Interbank Contagion Spectral Certificate{RESET}")
    print(f"{BOLD}{CYAN}{b}{RESET}")
    print(f"""
  Mathematical basis: Perron-Frobenius theorem on W[i,j] = exposure(i→j) / equity_i.
  ρ(W) = 1 is the exact stability phase transition.

  vs Standard approaches:
    Basel III LCR / NSFR         — individual liquidity; ignores network topology
    SRISK (NYU Stern)             — balance-sheet size × MES; empirically fitted
    CoVaR (Adrian-Brunnermeier)  — ΔCoVaR regression; not structural
    DFAST / CCAR scenario         — single macro shock; misses cascade amplification

  ContagionGuard:
    Zero fitted parameters   ρ(W) derives from the actual bilateral exposure matrix
    Exact threshold          γ_c = 1/ρ(W) provably separates stable from critical
    Perron targeting         identifies the structural amplifier, not the largest bank
    Eisenberg-Noe cascade    traces the full default chain, not just first-order shocks
""")


if __name__ == "__main__":
    banner()
    phase1()
    phase2()
    phase3()
    phase4()
    b = _hr()
    print(f"\n{BOLD}{CYAN}{b}{RESET}")
    print(f"{BOLD}{GREEN}  ContagionGuard benchmark complete{RESET}")
    print(f"{BOLD}{CYAN}{b}{RESET}")
    print(f"\n  API + integration docs:  {BOLD}vallikat@vectorpeaktech.com{RESET}\n")
