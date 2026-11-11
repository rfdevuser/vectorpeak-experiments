# vhs tape script — DoubleDescentGuard Double Descent Certificate benchmark
#
# Prerequisites: none — pure Python standard library
#   python run_doubledescentguard_benchmark.py   ← verify it runs clean before recording
#
# To render:
#   vhs record_doubledescentguard.tape
#
# Output: doubledescentguard-demo.gif
# Convert to MP4 for LinkedIn:
#   ffmpeg -i doubledescentguard-demo.gif -movflags faststart -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" doubledescentguard-demo.mp4

Output doubledescentguard-demo.gif

Set Shell "bash"
Set FontSize 15
Set Width 140
Set Height 42
Set Theme "Dracula"
Set TypingSpeed 40ms
Set Padding 12

# ── Opening prompt ────────────────────────────────────────────────────────────
Sleep 800ms

Type "# Two models. Same data. Same val loss. One generalises at 70%. One at 0.34%."
Sleep 1.2s
Enter
Sleep 400ms

Type "python run_doubledescentguard_benchmark.py"
Enter

# Script runs instantly — no dependencies
Sleep 1s

# Phase 1 header + F_gen formula appear
Sleep 2s

# F_gen table prints — hold on ρ=1 row (0.1867%, ← MAXIMUM RISK)
Sleep 4s

# Hold on the ρ* and ρ_th landmark rows (50% and 67.5%)
Sleep 4s

# "99.81% of what the model learned is trapped" summary lines
Sleep 4s

# Phase 2 prints — the 6-model certification table
# Hold on the two credit scoring rows (0.34% vs 70.1%) and the trading contrast
Sleep 5s

# Detail block prints for first three models
# Key moment: credit_critical 0.34% DO_NOT_DEPLOY vs credit_safe 70.1% APPROVED
Sleep 4s

# Trading model contrast lines appear: 150 factors PARADOX, 350 factors ACCESSIBLE
Sleep 4s

# Phase 3 — regularisation lever table
# Hold so all four reg configs are visible (D=0.40 for all — same ModelGuard call)
Sleep 5s

# "D is blind to regularisation and SNR. ρ is not." line
Sleep 4s

# Final banner
Sleep 3s

# Hold before loop
Sleep 2s
