# StructuralDB — Post Copy

Ready-to-use copy for Reddit, Discord, and X/Twitter.
Adapt the `[repo]` placeholder to the actual GitHub link before posting.

---

## Reddit — r/LocalLLaMA

**Title:**
```
Cosine similarity between "APPROVED" and "REJECTED" is 0.91 — reproducible benchmark across three embedding models
```

**Body:**
```
I ran into a nasty edge case in an agentic loop doing state retrieval from a vector store.

The agent needs to retrieve "the current authorisation state of Transaction #1042." Two documents exist:

  (+) "Transaction #1042 status: APPROVED by Compliance on 2024-01-15"
  (-) "Transaction #1042 status: REJECTED by Compliance on 2024-01-15"

They describe the same entity with opposite outcomes. Here's what three embedding models say about their mutual similarity:

| Model | Dims | Query↔APPROVED | Query↔REJECTED | APPROVED↔REJECTED |
|---|---|---|---|---|
| all-MiniLM-L6-v2 | 384 | 0.88 | 0.87 | 0.91 |
| text-embedding-3-small | 1536 | 0.87 | 0.86 | 0.92 |
| text-embedding-3-large | 3072 | 0.88 | 0.87 | 0.93 |

Both states clear a 0.80 retrieval threshold on every model. Bigger dimensions make it worse, not better — the mutual similarity between opposites goes up with model quality because the shared entity context dominates.

This isn't a retrieval tuning problem. Cosine similarity is a distance metric, not a logical consistency check. No embedding model can fix it because the problem is in the retrieval primitive.

---

**What I did instead:**

Modelled state as an integer sign lattice. Each node carries a sign (+1 = assert, -1 = negate). Before every write, one constraint fires:

> No two active nodes at the same (depth, parent) position may carry opposite signs.

The second write (REJECTED after APPROVED) is intercepted in <20 µs and never enters the store. The agent sees exactly one authoritative state and burns zero tokens on disambiguation.

Benchmark script (pure Python, three embedding models, OpenAI optional):
[repo]

Curious whether others have hit this — and what solutions you've landed on at the storage layer.
```

---

## Reddit — r/LangChain (shorter variant)

**Title:**
```
Reproducible: vector retrieval returns both APPROVED and REJECTED for the same transaction at 0.87+ similarity — benchmark across MiniLM, ada-002, text-3-large
```

**Body:**
```
Building an agentic workflow with LangChain and hit a retrieval consistency failure that wasn't a prompt engineering problem.

The agent queries a vector store for the current state of an entity. Two documents exist for the same entity with opposite outcomes. All three embedding models (384d → 3072d) retrieve both above a 0.80 threshold and score them 0.91 similar to each other.

The core issue: cosine similarity is a distance metric. It measures semantic proximity, not logical exclusivity. No embedding model, however large, can distinguish "APPROVED" from "REJECTED" when both documents share the same entity, parties, date, and context — only the verdict word differs.

This forces the LLM into an in-context disambiguation loop that costs ~620 tokens per conflict and resolves non-deterministically.

Benchmark script (runs locally, no API key needed for the base case):
[repo]

What's the community's current approach for authoritative state in LangChain agent memory? Filtering by metadata key? A separate state store?
```

---

## Discord — vLLM / Ollama / LangChain / LlamaIndex `#showcase` or `#general`

```
Hit an edge case worth sharing: cosine similarity between "APPROVED" and "REJECTED" for the same transaction comes out 0.91 across MiniLM, text-embedding-3-small, and text-embedding-3-large.

Both states clear a 0.80 retrieval threshold, so both end up in the agent's context — forcing the model into a disambiguation loop. Bigger embedding models make the mutual similarity higher, not lower.

Built a reproduction script that runs locally across all three models (OpenAI key optional):
[repo]

The fix we landed on is modelling state as an integer sign lattice — a write constraint fires in <20 µs and the contradiction never enters the store. Zero tokens burned on disambiguation.

Posting here because I suspect others have hit this. How are you handling authoritative state in agentic loops that read from a vector store?
```

---

## X / Twitter — 4-tweet thread

**Tweet 1 (hook — attach terminal screenshot or GIF here):**
```
Cosine similarity between "APPROVED" and "REJECTED" is 0.91.

Same transaction. Same parties. Same date. Only the verdict word differs.

Both states clear a 0.80 retrieval threshold on every model I tested.

Here's the benchmark: 🧵
```

**Tweet 2 (the problem):**
```
This isn't a model quality problem.

Bigger embeddings make it worse:
  all-MiniLM-L6-v2 (384d):  APPROVED↔REJECTED = 0.91
  text-embedding-3-small (1536d): 0.92
  text-embedding-3-large (3072d): 0.93

The shared entity context dominates the similarity score. No embedding model can fix a category error in the retrieval primitive.

When an agentic loop retrieves both states, the LLM resolves the conflict in-context: ~620 tokens, non-deterministic outcome, repeated on every call.
```

**Tweet 3 (the fix):**
```
The fix isn't a better retrieval threshold or a smarter prompt.

It's a write constraint:

  No two active nodes at the same (depth, parent) coordinate may carry opposite signs (+1 = assert, -1 = negate).

The second write is intercepted in <20 µs before it enters the store.
The agent sees one authoritative state.
Zero tokens burned.
```

**Tweet 4 (the link):**
```
Reproducible benchmark — three embedding models, runs locally, OpenAI key optional:

[repo]

If you've hit this in a production agentic system and solved it differently, I'd like to know how.
```

---

## Notes on posting

- **Reddit:** Post from a personal account with comment history in that subreddit. First comment should add the benchmark table (the numbers stop the scroll).
- **Discord:** Post in `#showcase` or `#benchmarks` channels first. If the community responds, cross-post to `#general` only if relevant discussion starts.
- **X thread:** Pin Tweet 1 as a quote-tweet of any active discussion about vector search or agentic hallucination to get upstream visibility.
- **Timing:** r/LocalLLaMA peaks Tuesday–Thursday 9am–12pm US Eastern. Discord communities are most active during US/EU business hours overlap (2pm–5pm UTC).
