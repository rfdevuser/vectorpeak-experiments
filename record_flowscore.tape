# vhs tape script — FlowScore Alternative Credit Risk benchmark
#
# Prerequisites: none (pure Python, zero dependencies)
#   python run_flowscore_benchmark.py   ← verify it runs clean before recording
#
# To render:
#   vhs record_flowscore.tape
#
# Output: flowscore-demo.gif
# Convert to MP4 for LinkedIn:
#   ffmpeg -i flowscore-demo.gif -movflags faststart -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" flowscore-demo.mp4

Output flowscore-demo.gif

Set Shell "bash"
Set FontSize 15
Set Width 140
Set Height 44
Set Theme "Dracula"
Set TypingSpeed 40ms
Set Padding 12

# ── Opening prompt ────────────────────────────────────────────────────────────
Sleep 800ms

Type "python run_flowscore_benchmark.py"
Enter

# Script runs instantly — no deps, nothing to install
Sleep 1s

# Banner prints — hold on "vs Standard approaches" block
# Key moment: show the two-constant claim vs "1000s" for ML
Sleep 4s

# Phase 1 header + formula block
Sleep 2s

# Five-preset table — hold so viewer reads all five rows
# Key moment: Near Default PD_90=2.229% (RED) vs Healthy 0.044% (GREEN)
# "51× higher default probability" summary line
Sleep 5s

# Phase 2 header prints
Sleep 2s

# CIBIL vs FlowScore table
# Key moment: Thin-File UPI showing CIBIL=0 REJECTED but FlowScore 60.9 GREEN
#             Near Default showing CIBIL=660 APPROVED but FlowScore 1.6 RED
Sleep 5s

# "Key contrast" summary lines
Sleep 4s

# Phase 3 — Kramers amplification table
Sleep 3s

# PD curve table — D=1.0 → D=0.1
# Key moment: "52× amplification" line at the bottom
Sleep 6s

# Phase 4 — CSD trajectory header
Sleep 2s

# CSD trajectory table
# Key moment: Month 3 → "CSD flag fires" (red arrow)
#             Month 4 → "NEAR-DEFAULT tier" (red arrow)
Sleep 5s

# "1 month lead time" timeline lines
Sleep 4s

# Final banner
Sleep 3s

# Hold before loop
Sleep 2s
