# vhs tape script — StructuralDB Negation Trap benchmark
#
# Prerequisites (run once before recording):
#   pip install sentence-transformers numpy
#   python run_benchmark.py          ← downloads all-MiniLM-L6-v2 (~90 MB, cached after first run)
#
# To render:
#   vhs record_structuraldb.tape
#
# Output: structuraldb-demo.gif  (drop into Reddit post, Discord, or X thread)

Output structuraldb-demo.gif

Set Shell "bash"
Set FontSize 15
Set Width 96
Set Height 36
Set Theme "Dracula"
Set TypingSpeed 40ms
Set Padding 12

# ── Opening prompt ────────────────────────────────────────────────────────────
Sleep 800ms

Type "# Two polar-opposite states. Same entity. What does cosine similarity say?"
Sleep 1.2s
Enter
Sleep 400ms

Type "python run_benchmark.py"
Enter

# Give the model time to load from cache (no download — model pre-cached)
Sleep 3s

# Script runs and prints PHASE 1 (vector failure) + PHASE 2 (StructuralDB intercept)
# vhs captures the output as it scrolls — pause long enough for the key lines to settle

Sleep 8s

# Scroll pause at the FAILURE line so it's readable in the GIF
Sleep 2s

# PHASE 2 prints — pause on the [INTERCEPTED] line
Sleep 3s

# Final banner
Sleep 3s

# Hold on the result for 2 s before loop
Sleep 2s
