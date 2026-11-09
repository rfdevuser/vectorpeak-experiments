# vhs tape script — VisionCore + AdelicDrive Joint AV Pipeline Benchmark
#
# Prerequisites: numpy scipy
#   pip install numpy scipy
#   python3 run_joint_av_benchmark.py   ← verify it runs clean before recording
#
# To render:
#   vhs record_joint_av.tape
#
# Output: joint-av-demo.gif
# Convert to MP4 for LinkedIn:
#   ffmpeg -i joint-av-demo.gif -movflags faststart -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" joint-av-demo.mp4

Output joint-av-demo.gif

Set Shell "bash"
Set FontSize 15
Set Width 140
Set Height 42
Set Theme "Dracula"
Set TypingSpeed 40ms
Set Padding 12

# ── Opening prompt ────────────────────────────────────────────────────────────
Sleep 800ms

Type "# Attack goal: camera noise → flip BRAKE to ACCELERATE at red light. Watch what happens."
Sleep 1.2s
Enter
Sleep 400ms

Type "python3 run_joint_av_benchmark.py"
Enter

# Script runs (numpy/scipy — may take 1-2s to import)
Sleep 2s

# Phase 1 header + noise budget line appear
# Hold so the IoU table is readable
Sleep 3s

# σ=2 STABLE (0.916) and σ=4 STABLE (0.833) are the key lines
# Hold so viewer can compare σ=1 NOISE-SENS vs coarse STABLE
Sleep 4s

# CVO STABLE summary line + CNN UNSTABLE comparison appear
Sleep 3s

# Phase 2 begins — baseline decision table (BRAKE wins, ACCELERATE last)
# Hold on the BRAKE 0.7715 / ACCELERATE 0.0350 contrast
Sleep 4s

# Attack step 1 table appears — continuous inputs spoofed to highway values
# Key moment: ACCELERATE φ_ℝ = 0.9500 (perfect highway score) but ADS still #3
Sleep 4s

# Attack step 2 (hypothetical full spoof) appears for contrast
Sleep 2s

# Summary rows appear: BRAKE → MAINTAIN → ACCELERATE #3
# Hold on "p-adic flags hold ACCELERATE at #3" line
Sleep 4s

# Phase 3 — the 4-barrier table
# Hold so all four BLOCKED lines are visible together
Sleep 5s

# Key numbers: Max ACCEL ADS = 0.6934 < BRAKE ADS = 0.7715, gap = 0.0781
Sleep 4s

# Combined result — three bullet points
Sleep 3s

# Final banner
Sleep 3s

# Hold before loop
Sleep 2s
