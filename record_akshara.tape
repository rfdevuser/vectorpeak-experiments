# vhs tape script — Akshara KTP-ID benchmark
#
# Prerequisites (none — pure Python, no deps):
#   python run_akshara_benchmark.py     ← runs immediately offline
#
# To render:
#   vhs record_akshara.tape
#
# Output: akshara-demo.gif  (drop into Reddit post, Discord, or X thread)

Output akshara-demo.gif

Set Shell "bash"
Set FontSize 15
Set Width 140
Set Height 48
Set Theme "Dracula"
Set TypingSpeed 40ms
Set Padding 12

# ── Opening prompt ────────────────────────────────────────────────────────────────────────
Sleep 800ms

Type "# UUID hallucination detection requires a DB query (22ms). KTP-ID checksum: 312ns."
Sleep 1.2s
Enter
Sleep 400ms

Type "python run_akshara_benchmark.py"
Enter

# Phase 1 (routing throughput) prints — pause on the speedup line
Sleep 4s

# Phase 2 (hallucination latency) prints — pause on the 71,795× speedup line
Sleep 3s

# Pause on the 100% catch rate line
Sleep 2s

# Phase 3 (token compression) prints — pause on the 1k entities row
Sleep 3s

# Constrained decoding note — readable pause
Sleep 2s

# Phase 4 (agent loop + memory footprint) prints
Sleep 3s

# O(1) memory table — pause for systems engineers
Sleep 2s

# Rust baseline note — readable pause
Sleep 2s

# Summary table — hold for legibility
Sleep 4s

# Hold on the final banner
Sleep 2s
