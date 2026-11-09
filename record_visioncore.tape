# vhs tape script — VisionCore CVO benchmark
#
# Prerequisites (run once before recording):
#   pip install numpy scipy
#   python run_cvo_benchmark.py   ← verify it runs clean before recording
#
# To render:
#   vhs record_visioncore.tape
#
# Output: visioncore-demo.gif
# Convert to MP4 for LinkedIn:
#   ffmpeg -i visioncore-demo.gif -movflags faststart -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" visioncore-demo.mp4

Output visioncore-demo.gif

Set Shell "bash"
Set FontSize 15
Set Width 140
Set Height 42
Set Theme "Dracula"
Set TypingSpeed 40ms
Set Padding 12

# ── Opening prompt ────────────────────────────────────────────────────────────
Sleep 800ms

Type "# Same image. Five brightness levels. What does the vision front-end see?"
Sleep 1.2s
Enter
Sleep 400ms

Type "python run_cvo_benchmark.py"
Enter

# Script loads scipy — brief pause
Sleep 2s

# Phase 1 prints — the fingerprint table is the key visual
# All five rows show identical hash → pause long enough for them to be readable
Sleep 6s

# PROOF line and FAILURE line appear — hold here
Sleep 3s

# Phase 2 prints — IoU table across three scales
Sleep 5s

# PROOF line (IoU ≥ 80%) and FAILURE line (CNN shifted %) appear
Sleep 3s

# Final comparison table
Sleep 4s

# Hold on result before loop
Sleep 2s
