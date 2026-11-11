# vhs tape script — ContagionGuard Interbank Contagion Spectral Certificate benchmark
#
# Prerequisites:  pip install numpy
#   python run_contagionguard_benchmark.py   ← verify it runs clean before recording
#
# To render:
#   vhs record_contagionguard.tape
#
# Output: contagionguard-demo.gif
# Convert to MP4 for LinkedIn:
#   ffmpeg -i contagionguard-demo.gif -movflags faststart -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" contagionguard-demo.mp4

Output contagionguard-demo.gif

Set Shell "bash"
Set FontSize 15
Set Width 140
Set Height 42
Set Theme "Dracula"
Set TypingSpeed 40ms
Set Padding 12

# ── Opening prompt ────────────────────────────────────────────────────────────
Sleep 800ms

Type "pip install numpy -q"
Enter
Sleep 4s

Type "python run_contagionguard_benchmark.py"
Enter

# Script runs instantly
Sleep 1s

# Banner prints — hold on the "vs Standard approaches" comparison block
Sleep 3s

# Phase 1 header + explanation prints
Sleep 2s

# Five-preset table — hold so viewer reads all five rows
# Key moment: Eurozone and SVB going RED (CRITICAL) vs STABLE in green
Sleep 5s

# Phase 2 header prints
Sleep 2s

# Eurozone Perron table — hold on the full table
# Key moment: ES1 showing +4 divergence in red
Sleep 5s

# "Regulator heuristic vs ContagionGuard" summary lines
# ES1 is 200B, ranked #1 structurally
Sleep 4s

# Phase 3 — cascade containment
# Ring-5 STABLE shows cascade 1/5 (green) for every seed
Sleep 4s

# Hub-5 CRITICAL: Hub seeds cascade 5/5 (red), spokes cascade 1/5 (green)
# Key moment: the asymmetry — hub default is total; spoke defaults are contained
Sleep 5s

# Phase 4 — capital injection lever table
# Hold on the multiplier sweep: 1.5× + 2.5B → ρ < 1 marker appears
Sleep 5s

# "Capital wasted" counterfactual line
# Key moment: injecting into FR1 (wrong target) stays CRITICAL
Sleep 4s

# Final banner
Sleep 3s

# Hold before loop
Sleep 2s
