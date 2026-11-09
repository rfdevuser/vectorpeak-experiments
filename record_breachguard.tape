# vhs tape script — BreachGuard Vulnerability Percolation benchmark
#
# Prerequisites: none — pure Python standard library
#   python run_breachguard_benchmark.py   ← verify it runs clean before recording
#
# To render:
#   vhs record_breachguard.tape
#
# Output: breachguard-demo.gif
# Convert to MP4 for LinkedIn:
#   ffmpeg -i breachguard-demo.gif -movflags faststart -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" breachguard-demo.mp4

Output breachguard-demo.gif

Set Shell "bash"
Set FontSize 15
Set Width 140
Set Height 42
Set Theme "Dracula"
Set TypingSpeed 40ms
Set Padding 12

# ── Opening prompt ────────────────────────────────────────────────────────────
Sleep 800ms

Type "# CVSS 9.8 is ranked #1. Is it actually the biggest cascade risk?"
Sleep 1.2s
Enter
Sleep 400ms

Type "python run_breachguard_benchmark.py"
Enter

# Script runs instantly — no model load
Sleep 1s

# Header and network stats print
Sleep 2s

# Phase 1 prints — CVSS ranking table
# Key moment: db-01 at #1, dns-01 buried at #15, monitor-01 at #20
Sleep 5s

# FAILURE line prints — hold here so it's readable
Sleep 3s

# Phase 2 prints — Γ₄₃ ranking table
# Key moment: dns-01 jumps to #1, monitor-01 to #2, db-01 drops to #10
Sleep 5s

# γ_c trajectory table prints — CVSS vs Γ₄₃ side by side
Sleep 4s

# Mismatch analysis table
Sleep 4s

# Final banner — 8.4× ratio is the key number
Sleep 4s

# Hold on result before loop
Sleep 2s
