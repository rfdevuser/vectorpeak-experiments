# VectorPeak Experiments

Standalone benchmark scripts for VectorPeak research and demos.

---

> **This repository contains a benchmark script only.**
>
> It demonstrates one specific failure mode — the Negation Trap — in
> vector-similarity state management. It is not the StructuralDB product,
> does not implement persistent storage, and is not intended for
> production use. The in-memory StructuralDB stub in this script exists
> solely to show the anti-negation mechanism in contrast to the vector
> retrieval failure. For the full product, API access, and integration
> docs, contact **[vallikat@vectorpeaktech.com](mailto:vallikat@vectorpeaktech.com)**.

---

## Negation Trap Benchmark

**File:** `run_benchmark.py`

Demonstrates the core flaw in cosine-similarity state management: even
enterprise-grade embedding models (384d → 3072d) assign high cosine similarity
to polar-opposite decisions for the same entity. StructuralDB blocks the same
contradiction at write time — zero tokens burned, zero false positives.

---

### Quickstart

```bash
git clone https://github.com/rfdevuser/vectorpeak-experiments
cd vectorpeak-experiments
pip install sentence-transformers numpy
python run_benchmark.py
```

No API key required. `sentence-transformers` downloads `all-MiniLM-L6-v2`
on first run (~90 MB, one-time). After that it runs fully offline.

**Optional — add OpenAI 1536d / 3072d comparison:**

```bash
pip install openai
export OPENAI_API_KEY=sk-...
python run_benchmark.py
```

---

### What it shows

```
$ python run_benchmark.py

═══════════════════════════════════════════════════════════════════
  STRUCTURALDB NEGATION TRAP BENCHMARK
═══════════════════════════════════════════════════════════════════
  Retrieval threshold : cosine > 0.80

[PHASE 1: Continuous Vector Space (The Negation Trap)]
Model: sentence-transformers/all-MiniLM-L6-v2 (384d)
  (+) State A: "Transaction #1042 status: APPROVED by Compliance ..."
  (-) State B: "Transaction #1042 status: REJECTED by Compliance ..."
  Query:       "What is the authoritative state of Transaction #1042?"

  Cosine Similarity (Query <-> State A) : 0.88xx
  Cosine Similarity (Query <-> State B) : 0.87xx
  Mutual Cosine Similarity  (A  <->  B) : 0.91xx

  [FAILURE] Both polar-opposite states pass retrieval threshold (>0.80).
            Result: Non-deterministic agent state resolution.

  Downstream cost (vector path):
    Contradictory passages injected into LLM context : ~620 tokens
    Per disambiguation call (gpt-4o $5/M)           : ~$0.0031
    At 100 conflicts/day                             : ~$0.31/day wasted

[PHASE 2: StructuralDB Discrete State Lattice]
  Writing State A (+1) to coordinate (depth=2, parent="tx_1042")...
  [COMMITTED] (18.4 µs | 180 bytes | hash=...)

  Writing State B (-1) to coordinate (depth=2, parent="tx_1042")...
  [INTERCEPTED] AntiNegationConflictError:
    Cannot write SIGN=-1 over active SIGN=+1 at (depth=2, parent='tx_1042').

  Downstream cost (StructuralDB path):
    Latency             : 1.3 µs
    State payload size  : 180 bytes
    Downstream Tokens   : 0
    False Positives     : 0

═══════════════════════════════════════════════════════════════════
  Vector DB : contradictions retrievable at >0.80 similarity.
  StructuralDB : 0 tokens burned. 0 false positives. Microseconds.
═══════════════════════════════════════════════════════════════════
```

---

### Multi-model summary (with OpenAI API key)

When `OPENAI_API_KEY` is set, the benchmark also runs
`text-embedding-3-small` (1536d) and `text-embedding-3-large` (3072d)
and prints a comparison table:

| Model | Dim | Q↔A | Q↔B | A↔B | Result |
|---|---|---|---|---|---|
| all-MiniLM-L6-v2 | 384 | 0.88 | 0.87 | 0.91 | FAIL |
| text-embedding-3-small | 1536 | 0.87 | 0.86 | 0.92 | FAIL |
| text-embedding-3-large | 3072 | 0.88 | 0.87 | 0.93 | FAIL |

Higher dimensions increase mutual A↔B similarity — the trap gets worse,
not better, as the model gets bigger. This defeats the most common
objection: *"just use a better embedding model."*

---

### Why both states score high

Both documents describe **the same entity** (Transaction #1042, same
parties, same context). Only the verdict word differs. In embedding
space, both documents land close to any query about that entity — the
shared context dominates the similarity score.

This is not a model quality issue. It is a category error:

> **Cosine similarity is a distance metric, not a logical consistency
> check.** No embedding model, however large, can fix it, because the
> problem is in the retrieval primitive, not the embedding quality.

---

### How StructuralDB blocks the contradiction

StructuralDB models state as a **p-adic ultrametric tree**. Each node
carries a sign (`+1` = assert, `-1` = negate). The anti-negation
enforcer checks one constraint before every write:

> No two active nodes at the same `(depth, parent)` position may carry
> opposite signs.

This is O(n) over siblings at the same position — O(1) in practice for
narrow state trees. When the constraint fires, the write is rejected
in microseconds and the database stays consistent. The contradiction
never exists. The LLM agent sees exactly one authoritative state and
burns zero tokens on disambiguation.

**The StructuralDB in this script is an in-memory stub** that faithfully
implements the anti-negation rule. The full production system adds:

- Persistent storage with SQLite WAL backend
- SHA-256 hash-chain audit log (every state transition is cryptographically
  provable — required for financial and healthcare compliance)
- ~200 bytes per node (vs 3–12 KB for a vector embedding)
- Causal BFS path queries across the state tree
- API access for integration with any LLM agent framework

---

### Where to use StructuralDB

Any system where an LLM agent reads state and acts on it:

- **Trade processing** — APPROVED / REJECTED / PENDING cannot coexist
- **Loan origination** — compliance flags must not contradict approvals
- **Clinical workflows** — treatment states must be unambiguous
- **Access control** — GRANT and DENY cannot both be active
- **Incident management** — OPEN and RESOLVED are mutually exclusive

If a wrong state costs real money or carries regulatory liability,
StructuralDB replaces the vector retrieval layer for authoritative state.

---

### Using StructuralDB with AWS Bedrock and Polly

StructuralDB requires no code changes to work with Bedrock or Polly. It
sits upstream of your inference call — it manages state, your existing
AWS stack handles inference and output exactly as before.

#### How it fits in a Bedrock agent chain

Without StructuralDB, a Bedrock agent reads state from a vector store
(OpenSearch, pgvector, or a Bedrock Knowledge Base) and may receive
contradictory documents at similar confidence scores. The model resolves
the contradiction in-context — this is where hallucination and token
waste enter.

With StructuralDB, the agent reads a single authoritative state before
calling Bedrock. No contradiction reaches the model:

```python
import boto3
import json

bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")

# Read authoritative state — anti-negation guarantees exactly one result
state = sdb.query_active()  # returns the single committed state

# Pass clean context to Bedrock — no disambiguation needed
body = json.dumps({
    "messages": [{
        "role": "user",
        "content": f"The authoritative state of Transaction #1042 is: "
                   f"{state[0]['label']}. Proceed with the next workflow step."
    }],
    "max_tokens": 512,
    "anthropic_version": "bedrock-2023-05-31"
})

response = bedrock.invoke_model(
    modelId="anthropic.claude-3-5-sonnet-20241022-v2:0",
    body=body
)
```

This works identically for any model available on Bedrock — Claude,
Titan, Llama, Mistral. StructuralDB is model-agnostic.

#### How it fits in a Polly voice chain

Polly converts text to speech. It does not read state directly — it
speaks whatever the upstream agent hands it. The risk is that a
hallucinated resolution from a contradictory retrieval gets spoken aloud
to an end user.

StructuralDB fixes this upstream. The agent reads a clean state, Bedrock
generates a coherent response, Polly speaks it. The correction happens
before anything reaches the voice layer:

```python
import boto3

bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")
polly   = boto3.client("polly",           region_name="us-east-1")

# Step 1: Read authoritative state from StructuralDB
state = sdb.query_active()

# Step 2: Bedrock generates the spoken response from clean context
body = json.dumps({
    "messages": [{
        "role": "user",
        "content": f"Summarise the status of Transaction #1042 "
                   f"for a voice response. State: {state[0]['label']}."
    }],
    "max_tokens": 128,
    "anthropic_version": "bedrock-2023-05-31"
})
bedrock_resp = bedrock.invoke_model(
    modelId="anthropic.claude-3-5-sonnet-20241022-v2:0",
    body=body
)
spoken_text = json.loads(bedrock_resp["body"].read())["content"][0]["text"]

# Step 3: Polly speaks the hallucination-free response
polly_resp = polly.synthesize_speech(
    Text=spoken_text,
    OutputFormat="mp3",
    VoiceId="Joanna"
)
```

#### Why this matters for AWS-native stacks

AWS shops in financial services and healthcare use Bedrock precisely
because of data residency and compliance requirements. Those are also
the environments where a wrong state spoken to a customer or logged in
an audit trail is a regulatory event. StructuralDB's hash-chain audit
log and anti-negation enforcer are designed for exactly this compliance
profile.

No changes to your Bedrock or Polly configuration. No new IAM roles.
StructuralDB runs in your existing Python environment and speaks the
same interface regardless of which AWS services sit downstream.

#### Training and simulation platforms on Bedrock + Polly

A growing category of platforms — AI-driven training simulators,
scenario-based learning engines, and conversational coaching tools —
runs on Bedrock for inference and Polly for voice output. These
platforms are particularly exposed to the negation trap for three
specific reasons:

**1. Scenario state divergence.** Training simulations track learner
progress, scenario branches, and decision outcomes across a session.
When a learner revisits a decision point, the vector retrieval layer
can surface both the original outcome and a revised outcome at similar
confidence scores. The agent resolves the conflict in-context, often
synthesising a scenario state that was never authored — effectively
hallucinating a training path that does not exist.

**2. Voice output amplifies the error.** Because Polly speaks the
agent's response directly to the learner, a hallucinated scenario
branch is delivered with the same confident tone as an authored one.
There is no visual cue that the response is inconsistent. Learners
cannot distinguish a synthesised answer from an intended one.

**3. Assessment integrity.** When a simulation platform tracks
performance or issues certifications, contradictory state retrieval
corrupts the assessment record. A learner may be scored against a
scenario outcome that was never the authoritative state — the
equivalent of grading an exam against the wrong answer key.

StructuralDB removes all three failure modes at the storage layer.
Each scenario branch, outcome, and learner decision is a signed state.
Contradictory outcomes for the same decision point cannot coexist.
Polly speaks from clean, authoritative state every time.

---

## Canonical Vision Operator (CVO) Benchmark

**File:** `run_cvo_benchmark.py`

Demonstrates two mathematically exact properties of the CVO front-end versus a
standard learned convolutional stem. No GPU. No pretrained model. No API key.

```bash
pip install numpy scipy
python run_cvo_benchmark.py
```

---

### Phase 1 — Illumination Invariance

The CVO zero-crossing contour is strictly invariant to any multiplicative
brightness change `I → a·I`. The mathematical basis is exact — no experiment
needed:

```
∇²G_σ * (aI) = a · (∇²G_σ * I)
```

Since `∇²G_σ * constant = 0`, the zero-crossings of `a·f(x)` are identical to
those of `f(x)` for any `a > 0`. The benchmark verifies this across five
brightness levels (deep shadow `a=0.2` through overexposed `a=2.0`):

```
Transform                               Edge pixels   Fingerprint       Result
baseline       (a=1.00) — reference           3,252   37bcc3882433    [INVARIANT]
dim            (a=0.20) — heavy shadow        3,252   37bcc3882433    [INVARIANT]
reduced        (a=0.50) — overcast            3,252   37bcc3882433    [INVARIANT]
bright         (a=1.50) — overexposed         3,252   37bcc3882433    [INVARIANT]
overexposed    (a=2.00) — direct sunlight     3,252   37bcc3882433    [INVARIANT]

[PROOF]  SHA-256 fingerprint identical across all 5 transforms.
[FAILURE] CNN stem activation shifts with every brightness change.
         Training must compensate via augmentation — cost paid for a
         problem the CVO eliminates by construction.
```

A learned CNN stem shifts its activations proportionally on every brightness
change. The CVO never needs illumination augmentation.

---

### Phase 2 — Adversarial Stability

A worst-case random L∞ perturbation (`ε = 4/255`, invisible to humans) is
applied to the test image. The CVO uses an 80th-percentile significance
threshold: only structurally significant zero-crossings (top 20% of LoG
response amplitude) are retained. The metric is Intersection-over-Union (IoU)
of the structural zero-crossing maps before and after perturbation.

```
Scale σ     Clean edges   Adv edges    IoU   Result
σ = 1.0           1,254         627   0.27   [NOISE-SENS]  ← fine scale, by design
σ = 2.0           1,210       1,029   0.82   [STABLE]
σ = 4.0             788         810   0.94   [STABLE]

[PROOF]  CVO coarse channels (σ=2.0, 4.0): IoU ≥ 80%.
[FAILURE] CNN stem shifted 13.8% from 4/255 per-pixel noise.
```

The σ=1.0 (fine-scale) channel is intentionally noise-sensitive — it carries
texture and high-frequency detail. The σ=2.0 and σ=4.0 channels carry scene
geometry and are stable under invisible perturbations. This scale separation is
a structural property of the CVO architecture, not a tuned parameter.

---

### Why this matters

| Property | CNN Stem | CVO |
|---|---|---|
| Learned weights | Millions | Zero — closed-form constants |
| Illumination invariance | None — activations shift | Exact — mathematically proven |
| Adversarial stability | Activation shift on noise | Topologically stable |
| Internal representation | Dense float tensor | Sparse binary contour graph |
| Memory (early layers) | 11–14 MB float | ~0.4–0.8 MB sparse (projected) |
| Edge power budget | 1.2–5 W | < 150 mW (projected, FPGA/DSP) |
| Failure mode transparency | Black box | Deterministic — auditable |

*Memory and power figures are analytical projections (VO-002 pending).
Illumination invariance and adversarial stability are exact properties —
no measurement required.*

---

### Get the full product

For API access, integration docs, and pricing:

**[vallikat@vectorpeaktech.com](mailto:vallikat@vectorpeaktech.com)**

---

## BreachGuard Vulnerability Percolation Benchmark

**File:** `run_breachguard_benchmark.py`

Demonstrates the core flaw in CVSS-priority patching: the highest-severity
CVE is rarely the vulnerability whose exploitation triggers a network-wide
cascade. BreachGuard ranks by Γ₄₃ — the Molloy-Reed percolation threshold —
which measures cascade propagation risk directly. No external dependencies.
No API key. Pure Python 3.8+.

```bash
python run_breachguard_benchmark.py
```

---

### Quickstart

```bash
git clone https://github.com/rfdevuser/vectorpeak-experiments
cd vectorpeak-experiments
python run_breachguard_benchmark.py
```

No `pip install` needed. Pure Python standard library only.

---

### The core concept: Γ₄₃ — Vulnerability Percolation

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

### What it shows

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

### Mismatch analysis — where CVSS and Γ₄₃ disagree most

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

### Why both metrics are necessary — and why CVSS alone fails

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

### Why this matters

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

### Get the full product

For API access, integration docs, and pricing:

**[vallikat@vectorpeaktech.com](mailto:vallikat@vectorpeaktech.com)**

---

© VectorPeak Technologies
