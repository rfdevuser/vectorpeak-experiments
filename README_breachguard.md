# BreachGuard — Vulnerability Percolation Benchmark

**File:** `run_breachguard_benchmark.py`

Demonstrates the core flaw in CVSS-priority patching: the highest-severity
CVE is rarely the vulnerability whose exploitation triggers a network-wide
cascade. BreachGuard ranks by Γ₄₃ — the Molloy-Reed percolation threshold —
which measures cascade propagation risk directly. No external dependencies.
No API key. Pure Python 3.8+.

---

## Quickstart

```bash
git clone https://github.com/rfdevuser/vectorpeak-experiments
cd vectorpeak-experiments
python run_breachguard_benchmark.py
```

No `pip install` needed. Pure Python standard library only.

---

## The core concept: Γ₄₃ — Vulnerability Percolation

The **Molloy-Reed cascade threshold** is:

```
γ_c = ⟨k⟩ / (⟨k²⟩ − ⟨k⟩)
```

where `⟨k⟩` is the mean degree and `⟨k²⟩` is the mean squared degree of
the network.

`γ_c` is the minimum fraction of compromised nodes at which a lateral
movement cascade becomes self-sustaining. A higher `γ_c` means the network
is harder to cascade. BreachGuard ranks vulnerabilities by **Δγ_c** — how
much the cascade threshold rises when each vulnerability is patched.

---

## What it shows

```
$ python run_breachguard_benchmark.py

════════════════════════════════════════════════════════════════════
  BREACHGUARD VULNERABILITY PERCOLATION BENCHMARK  (Γ₄₃)
════════════════════════════════════════════════════════════════════
  Network        : 20 nodes, 48 edges (corporate IT infrastructure)
  Mean degree    : 4.80
  γ_c (base)     : 0.1433  — cascade triggers at ≥3 compromised nodes
  Claim          : the highest-CVSS vulnerability is not the one
                   whose exploitation triggers a network-wide cascade.

[PHASE 1: CVSS-Priority Patch Order  (Standard Practice)]
  Sorted by CVSS score descending — the industry default.

  Rank  Node         Type                  CVSS   1-hop  Network %
  #1    db-01        Database (Primary)     9.8      3        15%  ← CVSS CRITICAL
  ...
  #15   dns-01       Internal DNS           6.5     16        80%  ← low CVSS, high degree
  #20   monitor-01   Monitoring System      4.3     15        75%  ← low CVSS, high degree

  After patching #1 (db-01, CVSS 9.8):
    γ_c : 0.1433 → 0.1505  (+0.0072, 5.0% improvement)
    Cascade triggers at: 3 compromised nodes → 4 compromised nodes

  [FAILURE] db-01 (CVSS 9.8) connects to only 3 hosts directly.
            Patching it barely moves the cascade threshold.

[PHASE 2: BreachGuard Percolation-Priority Patch Order  (Γ₄₃)]
  Sorted by Δγ_c descending.

  Rank  Node         Type                  CVSS     Δγ_c   New γ_c   1-hop
  #1    dns-01       Internal DNS           6.5  +0.0605   0.2038      16  [TOP CASCADE RISK]
  #2    monitor-01   Monitoring System      4.3  +0.0390   0.1823      15  [TOP CASCADE RISK]
  ...
  #10   db-01        Database (Primary)     9.8  +0.0072   0.1505       3  ← CVSS #1, percolation #10

  γ_c trajectory — first 3 patches:
  Patch   Strategy            Node patched    γ_c after   Δ from base
  #1      CVSS                db-01           0.1505       +0.0072
  #2      CVSS                db-02           0.1583       +0.0150
  #3      CVSS                iot-01          0.1605       +0.0172

  #1      Γ₄₃ (BreachGuard)   dns-01          0.2038       +0.0605
  #2      Γ₄₃ (BreachGuard)   monitor-01      0.4186       +0.2753
  #3      Γ₄₃ (BreachGuard)   app-02          0.5000       +0.3567

════════════════════════════════════════════════════════════════════
  CVSS patch #1  : db-01   (CVSS 9.8)  → γ_c 0.1433 → 0.1505  (+0.72pp)
  Γ₄₃  patch #1  : dns-01  (CVSS 6.5)  → γ_c 0.1433 → 0.2038  (+6.05pp)
  Γ₄₃ raises cascade threshold 8.4× more than CVSS priority.
  CVSS is a severity score.  Γ₄₃ is a cascade score.  They measure different things.
════════════════════════════════════════════════════════════════════
```

---

## Mismatch analysis — where CVSS and Γ₄₃ disagree most

| Node | Type | CVSS | CVSS rank | Γ₄₃ rank | Gap | Direction |
|---|---|---|---|---|---|---|
| monitor-01 | Monitoring System | 4.3 | #20 | #2 | +18 | undervalued by CVSS |
| iot-01 | IoT Device | 8.5 | #3 | #18 | +15 | overvalued by CVSS |
| dns-01 | Internal DNS | 6.5 | #15 | #1 | +14 | undervalued by CVSS |
| db-01 | Database (Primary) | 9.8 | #1 | #10 | +9 | overvalued by CVSS |

The monitoring system (CVSS 4.3) moves from last place to second place.
The critical database (CVSS 9.8) drops from first to tenth. The gap is structural:
CVSS measures severity of exploitation in isolation; Γ₄₃ measures cascade
propagation potential in the actual network topology.

---

## Why both metrics are necessary — and why CVSS alone fails

CVSS answers: *"How bad is it if this node is exploited?"*

Γ₄₃ answers: *"If this node is compromised, does the network cascade?"*

Both questions matter. But patching by CVSS alone allocates resources to nodes
that minimise individual exploit impact — not network resilience.

The critical insight from the Molloy-Reed theorem:

> Cascade propagation depends on the second moment ⟨k²⟩ of the degree
> distribution, not just the degree ⟨k⟩. High-degree hubs contribute
> disproportionately to ⟨k²⟩ and therefore dominate cascade risk.

A monitoring system or DNS server with degree 15–16 dominates the cascade
threshold regardless of its own CVSS score, because it functions as a hub
through which lateral movement propagates to every host it connects to.
Patching db-01 (degree 3) barely changes ⟨k²⟩. Patching dns-01 (degree 16)
collapses it.

---

## Why this matters

| Factor | CVSS-Priority | BreachGuard Γ₄₃ |
|---|---|---|
| Metric | Per-node exploit severity | Network cascade threshold |
| Accounts for topology | No | Yes — Molloy-Reed theorem |
| Patch #1 (this network) | db-01 (degree 3, CVSS 9.8) | dns-01 (degree 16, CVSS 6.5) |
| γ_c improvement, patch #1 | +0.72 pp | +6.05 pp |
| Impact ratio | 1× (baseline) | 8.4× more cascade-resilient |
| After 3 patches, γ_c | 0.1605 | 0.5000 (network resilient) |
| Failure mode | Cascades through high-degree low-CVSS hubs | — |

Three Γ₄₃-ordered patches raise the cascade threshold from 14.3% to 50.0%
of nodes needed for self-sustaining propagation — the network becomes
highly resilient. Three CVSS-ordered patches raise it only to 16.1%.

---

## Get the full product

For API access, integration docs, and pricing:

**[vallikat@vectorpeaktech.com](mailto:vallikat@vectorpeaktech.com)**
