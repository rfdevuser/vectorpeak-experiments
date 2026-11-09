# BreachGuard — Post Copy

---

## LinkedIn

```
We patched the wrong server.

That's what this benchmark shows. Take a 20-node corporate network — web
servers, DNS, Active Directory, databases, monitoring, workstations, IoT.
Rank the vulnerabilities by CVSS score (the industry standard) and patch
the top one first. It's the primary database: CVSS 9.8, critical severity.

After patching it, the cascade threshold — the minimum fraction of
compromised nodes needed to trigger a network-wide lateral movement
cascade — moves by 0.72 percentage points. The network is barely
more resilient.

Now rank by cascade impact instead. The top result is the internal DNS
server: CVSS 6.5, medium severity, ranked 15th by CVSS. After patching
it, the cascade threshold moves by 6.05 percentage points.

Same one patch. 8.4 times more network resilience.

The reason is topology. The DNS server resolves names for 16 of the 20
hosts. The database connects to 3. When a node with 16 connections is
compromised, lateral movement can reach 80% of the network in one hop.
When a node with 3 connections is compromised, it reaches 15%.

CVSS measures how dangerous it is to exploit a single node in isolation.
It says nothing about whether that node's compromise cascades. Those are
different questions, and patching budgets are limited.

The benchmark is pure Python, no dependencies, runs in under a second.
[link to repo]
```

---

## Reddit — r/netsec

**Title:**
```
CVSS 9.8 database vs CVSS 6.5 DNS server: which patch raises network cascade resilience 8.4× more? Reproducible percolation benchmark (pure Python)
```

**Body:**
```
Built a benchmark to quantify the gap between CVSS-priority patching and topology-aware patching on a synthetic 20-node corporate network.

**The metric: Molloy-Reed cascade threshold (Γ₄₃)**

  γ_c = ⟨k⟩ / (⟨k²⟩ − ⟨k⟩)

γ_c is the minimum fraction of compromised nodes at which a lateral movement cascade becomes self-sustaining. Higher γ_c = harder to cascade.

Patching a node raises γ_c by some Δγ_c. BreachGuard ranks patches by Δγ_c instead of CVSS.

**Network:** 20 nodes, 48 edges — web, DNS, AD, app servers, databases, mail, monitoring, workstations, IoT.

**Base γ_c:** 0.1433 (cascade triggers at 3 compromised nodes out of 20)

**CVSS patch #1: db-01 (CVSS 9.8, degree 3)**
  γ_c after: 0.1505  (+0.72pp)

**Γ₄₃ patch #1: dns-01 (CVSS 6.5, degree 16)**
  γ_c after: 0.2038  (+6.05pp)

**8.4× more cascade resilience from the topology-ranked patch.**

**γ_c after 3 patches:**
  CVSS order:  0.1605  (barely moved)
  Γ₄₃ order:  0.5000  (network highly resilient)

**Mismatch table (biggest rank gaps):**

| Node | CVSS | CVSS rank | Γ₄₃ rank | Gap |
|---|---|---|---|---|
| monitor-01 | 4.3 | #20 | #2 | +18 |
| dns-01 | 6.5 | #15 | #1 | +14 |
| db-01 | 9.8 | #1 | #10 | -9 |

The monitoring system (CVSS 4.3, degree 15) ranks dead last by CVSS and second by cascade impact. The critical database (CVSS 9.8, degree 3) ranks first by CVSS and tenth by cascade impact.

**Why:** Cascade propagation scales with ⟨k²⟩ (mean squared degree), not ⟨k⟩. High-degree hubs contribute disproportionately. CVSS doesn't capture this at all.

Pure Python, zero dependencies, runs in under a second:
https://github.com/rfdevuser/vectorpeak-experiments

Interested whether others are using percolation theory or graph centrality metrics in vulnerability prioritisation — and whether this holds on real enterprise network topologies.
```

---

## Discord — security / DevOps communities `#showcase`

```
Built a pure-Python benchmark showing the gap between CVSS-priority patching and percolation-ranked patching on a 20-node network.

The highest-CVSS node (db-01, 9.8, degree 3) gives +0.72pp cascade resilience when patched.
The Γ₄₃-ranked node (dns-01, 6.5, degree 16) gives +6.05pp — 8.4× more impact.

After 3 CVSS-ordered patches: γ_c = 0.1605
After 3 Γ₄₃-ordered patches: γ_c = 0.5000

The monitoring system (CVSS 4.3) ranks #20 by CVSS and #2 by cascade risk.

No dependencies. Pure Python. Runs in under a second:
https://github.com/rfdevuser/vectorpeak-experiments

Curious whether anyone is using graph-based metrics alongside CVSS in production vulnerability management.
```

---

## X / Twitter — 4-tweet thread

**Tweet 1 (hook — attach terminal screenshot or GIF):**
```
We patched the wrong server.

CVSS says patch the database first. CVSS 9.8. Critical.

The topology says patch the DNS server first. CVSS 6.5. Medium.

One patch. 8.4× difference in network cascade resilience.

Here's the benchmark: 🧵
```

**Tweet 2 (the numbers):**
```
20-node corporate network. Base cascade threshold: 14.3% of nodes compromised triggers a self-sustaining lateral movement cascade.

Patch #1 by CVSS:  db-01   (9.8, degree 3)   → threshold moves to 15.1%
Patch #1 by Γ₄₃:  dns-01  (6.5, degree 16)  → threshold moves to 20.4%

After 3 CVSS patches: 16.1%
After 3 Γ₄₃ patches: 50.0%

Same budget. Very different network.
```

**Tweet 3 (the math):**
```
The metric is the Molloy-Reed percolation threshold:

  γ_c = ⟨k⟩ / (⟨k²⟩ − ⟨k⟩)

Cascade propagation scales with ⟨k²⟩ — mean squared degree.
High-degree hubs dominate it disproportionately.

CVSS measures per-node exploit severity in isolation.
It says nothing about ⟨k²⟩.

The monitoring system (CVSS 4.3, degree 15) ranks #20 by CVSS and #2 by cascade risk.
```

**Tweet 4 (the link):**
```
Pure Python. Zero dependencies. Runs in under a second.

CVSS is a severity score.
Γ₄₃ is a cascade score.
They measure different things.

Benchmark:
[repo]
```
