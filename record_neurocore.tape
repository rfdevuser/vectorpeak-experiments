# vhs tape script — NeuroCore Adelic Neuromorphic Inference Engine benchmark
#
# Prerequisites: none — pure Python standard library
#   python run_neurocore_benchmark.py   ← verify it runs clean before recording
#
# To render:
#   vhs record_neurocore.tape
#
# Output: neurocore-demo.gif
# Convert to MP4 for LinkedIn:
#   ffmpeg -i neurocore-demo.gif -movflags faststart -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" neurocore-demo.mp4

Output neurocore-demo.gif

Set Shell "bash"
Set FontSize 15
Set Width 140
Set Height 42
Set Theme "Dracula"
Set TypingSpeed 40ms
Set Padding 12

# ── Opening prompt ────────────────────────────────────────────────────────────
Sleep 800ms

Type "# Every SNN framework needs 8-15 tuned constants. NeuroCore needs zero. All derived."
Sleep 1.2s
Enter
Sleep 400ms

Type "python run_neurocore_benchmark.py"
Enter

# Script runs instantly
Sleep 1s

# Phase 1 header + "A standard SNN framework requires 8-15..." line appear
Sleep 2s

# Constants table prints — hold so viewer can read all 8 derived constants
Sleep 4s

# Framework comparison table: Brian2 8-12, NEST 10-15, Loihi2 7+, NS-030 → 0
# Key moment: NS-030 showing 0 in green
Sleep 4s

# Phase 2 prints — 12-band table (delta through high-gamma)
# Hold so the full band structure is visible
Sleep 5s

# "Sleep = 1/3: derived, not observed" section
# Hold on the "not a fit to biological data" conclusion line
Sleep 4s

# Phase 3 — energy table from n=128 to n=32,768
# Key moment: n=4096 row showing 262,144× speedup
Sleep 5s

# "Why p-adic routing is thermodynamically free" explanation
Sleep 3s

# Phase 4 — spike cascade threshold table
# Hold on the depth-threshold YES/NO column
Sleep 4s

# First 5 spike events
Sleep 3s

# Final banner
Sleep 3s

# Hold before loop
Sleep 2s
