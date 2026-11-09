# vhs tape script — ClearSeed Certified Scenario Engine benchmark
#
# Prerequisites: none — pure Python standard library
#   python run_clearseed_benchmark.py   ← verify it runs clean before recording
#
# To render:
#   vhs record_clearseed.tape
#
# Output: clearseed-demo.gif
# Convert to MP4 for LinkedIn:
#   ffmpeg -i clearseed-demo.gif -movflags faststart -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" clearseed-demo.mp4

Output clearseed-demo.gif

Set Shell "bash"
Set FontSize 15
Set Width 140
Set Height 42
Set Theme "Dracula"
Set TypingSpeed 40ms
Set Padding 12

# ── Opening prompt ────────────────────────────────────────────────────────────
Sleep 800ms

Type "# Same seed. Two runs. Can the regulator replay your scenarios?"
Sleep 1.2s
Enter
Sleep 400ms

Type "python run_clearseed_benchmark.py"
Enter

# Script runs instantly — no model load
Sleep 1s

# Phase 1 prints — auditability table
# Key moment: System PRNG shows two different values; ClearSeed shows identical
Sleep 4s

# FAILURE lines for PRNG and SUCCESS lines for ClearSeed — hold here
Sleep 3s

# Phase 2 prints — equidistribution certificate table (4 seeds, all REGULATORY GRADE)
Sleep 5s

# Detail check lines for first seed — hold so all 5 PASSes are readable
Sleep 4s

# Phase 3 prints — regulatory presets table
Sleep 4s

# Live generation result — certificate 5/5, REGULATORY GRADE
Sleep 3s

# Final banner
Sleep 3s

# Hold before loop
Sleep 2s
