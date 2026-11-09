# vhs tape script — ModelGuard AI Generalisation Risk Intelligence benchmark
#
# Prerequisites: none — pure Python standard library
#   python run_modelguard_benchmark.py   ← verify it runs clean before recording
#
# To render:
#   vhs record_modelguard.tape
#
# Output: modelguard-demo.gif
# Convert to MP4 for LinkedIn:
#   ffmpeg -i modelguard-demo.gif -movflags faststart -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" modelguard-demo.mp4

Output modelguard-demo.gif

Set Shell "bash"
Set FontSize 15
Set Width 140
Set Height 42
Set Theme "Dracula"
Set TypingSpeed 40ms
Set Padding 12

# ── Opening prompt ────────────────────────────────────────────────────────────
Sleep 800ms

Type "# Same val_loss. 9× different generalisation variance. Val loss missed it."
Sleep 1.2s
Enter
Sleep 400ms

Type "python run_modelguard_benchmark.py"
Enter

# Script runs instantly — no model load
Sleep 1s

# Phase 1 prints — model audit table (GPT-3, LLaMA, Mistral, Gemma, Chinchilla)
# Hold so GPT-3's D = 0.5833 and "undertrained at launch" line are readable
Sleep 5s

# Phase 2 prints — variance amplification table
# Key moment: D=1.00 shows ∞ (diverges) and ← MAXIMUM RISK flag
Sleep 4s

# Hold on the ← MAXIMUM RISK line and the spike comparison numbers
Sleep 4s

# Phase 3 prints — the mismatch (3 models, same val_loss, different D)
Sleep 4s

# Hold on the BLOCK lines and the "9× higher" summary
Sleep 4s

# Final banner
Sleep 3s

# Hold before loop
Sleep 2s
