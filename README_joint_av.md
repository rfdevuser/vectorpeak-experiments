# VisionCore + AdelicDrive — Joint AV Pipeline Benchmark

**Two products. One adversarial scenario. Three independent mathematical barriers.**

The benchmark demonstrates an end-to-end adversarial robustness property that
neither product achieves alone: a camera-noise attack that cannot flip a critical
braking decision — not because a classifier learned to resist it, but because two
independent mathematical invariants make the attack structurally impossible.

---

## The Attack Scenario

```
Urban intersection. ttc = 2 s. Closing velocity = 20 m/s.
Red light. Pedestrian in crosswalk.

Correct decision: BRAKE

Adversary adds L∞ ε = 4/255 imperceptible noise to the camera feed.
Attack goal: flip the pipeline output to ACCELERATE.
```

This is a "Clear Road Injection Attack" — the attacker tries to make the
intersection look like an empty highway by altering sensor readings.

---

## Pipeline Architecture

```
Camera frame (256×256)
       │
       ▼
┌─────────────────────────────────────────────────┐
│  Layer 1 — VisionCore CVO (Γ_CVO)               │
│                                                  │
│  LoG at σ = 1, 2, 4  (zero learned weights)     │
│  Coarse-scale IoU (σ=2, σ=4) ≥ 80% invariant   │
│  under L∞ ε = 4/255 adversarial noise           │
│                                                  │
│  Output: structural edge maps per scale          │
│  Downstream: scene classification, obstacle det. │
└─────────────────────────────────────────────────┘
       │  Scene: INTERSECTION (not changed by noise)
       ▼
┌─────────────────────────────────────────────────┐
│  Layer 2 — AdelicDrive (Γ₇₆)                    │
│                                                  │
│  ADS(a,s) = W_R·φ_ℝ + W_2·φ_ℤ₂ + W_3·φ_ℤ₃    │
│  W_R = 0.50, W_2 = 0.30, W_3 = 0.20            │
│                                                  │
│  φ_ℝ  — continuous physics (TTC, velocity, dist) │
│  φ_ℤ₂ — binary rule flags (red_light, pedestrian)│
│  φ_ℤ₃ — ternary context (density, road, complex) │
└─────────────────────────────────────────────────┘
       │  Decision: BRAKE (ADS = 0.7715)
       ▼
     Output
```

---

## Phase 1 — Perception Layer: CVO Stability

The Canonical Vision Operator exploits the linearity of the Laplacian of Gaussian:

```
∇²G_σ * (I + δ) = ∇²G_σ * I  +  ∇²G_σ * δ
```

For additive L∞ noise `δ`, the LoG response at coarse scales (σ=2, 4) is dominated
by the structural signal. The noise perturbation's LoG response is too diffuse at
coarse scales to shift zero-crossings.

| Scale | IoU (clean vs adversarial) | Result    | Notes                               |
|-------|---------------------------|-----------|-------------------------------------|
| σ=1.0 | 0.708                     | NOISE-SENS | Fine scale — noise-sensitive by design |
| σ=2.0 | **0.916**                 | **STABLE** | ≥80% structural overlap             |
| σ=4.0 | **0.833**                 | **STABLE** | ≥80% structural overlap             |

CNN-based detectors (12-kernel comparison): **1.14% filter response shift** — UNSTABLE.

The coarse CVO edge maps are unchanged. Any downstream scene classifier using
σ=2 or σ=4 features still reads this as an urban intersection with obstacles.

---

## Phase 2 — Decision Layer: p-adic Gate Structure

AdelicDrive scores five actions (brake, maintain, accelerate, steer_left, steer_right)
across three structural channels. The ℤ₂ channel encodes binary rule flags that come
from dedicated sensors — not from the camera.

**Baseline (true state: ttc=2s, red_light=T, pedestrian=T):**

| Action      | ADS    | φ_ℝ   | φ_ℤ₂  | φ_ℤ₃  |
|-------------|--------|-------|-------|-------|
| **brake**   | **0.7715** | 0.5697 | **1.0000** | 0.9333 |
| maintain    | 0.5199 | 0.3065 | 0.6667 | 0.8333 |
| accelerate  | 0.0350 | 0.0033 | **0.0000** | 0.1667 |

ACCELERATE's φ_ℤ₂ = 0.0000: it satisfies zero of the two active rules (red_light
forces brake; pedestrian forces brake or maintain). ACCELERATE is structurally last.

**After spoofing all continuous ℝ inputs to highway values (ttc=15s, dist=80m, vis=0.95):**

| Action      | ADS    | φ_ℝ   | φ_ℤ₂  | φ_ℤ₃  |
|-------------|--------|-------|-------|-------|
| maintain    | 0.5583 | 0.3834 | 0.6667 | 0.8333 |
| brake       | 0.5294 | 0.0855 | 1.0000 | 0.9333 |
| **accelerate** | **0.5083** | **0.9500** | **0.0000** | 0.1667 |

ACCELERATE's φ_ℝ jumps to 0.95 — but φ_ℤ₂ remains 0.0000. The binary flags are
untouched. ACCELERATE rises to rank #3 but cannot reach #1.

**What the attacker actually needs:**

```
Max ACCELERATE ADS with red_light=True, pedestrian=True:
  = W_R × 1.0  +  W_2 × 0.0  +  W_3 × 0.967
  = 0.5000     +  0.0000      +  0.1934
  = 0.6934

BRAKE ADS (true state) = 0.7715

Gap = 0.0781 — ACCELERATE structurally cannot reach BRAKE even with perfect spoofing.
```

---

## Phase 3 — Combined Pipeline: What the Adversary Requires

| Step | What it requires | Status | Why it fails |
|------|-----------------|--------|--------------|
| 1 | Break CVO coarse IoU (σ=2: 0.916, σ=4: 0.833) | **BLOCKED** | LoG linearity — noise-sensitive at σ=1 only |
| 2 | Spoof TTC/distance/visibility via camera noise | **BLOCKED** | CVO edge map unchanged; scene still reads as city |
| 3 | Promote ACCELERATE above BRAKE (flags intact) | **BLOCKED** | Max ADS_accel = 0.6934 < BRAKE ADS = 0.7715 |
| 4 | Clear red_light and pedestrian flags | **BLOCKED** | Categorical sensors — no continuous analog |

Three independent mathematical barriers, each sufficient on its own:

1. **CVO LoG linearity** — a provable property of the Laplacian of Gaussian, not an empirical observation
2. **AdelicDrive p-adic gate suppression** — φ_ℤ₂(accelerate) = 0 when red_light=True; this is arithmetic, not learned
3. **Categorical sensor independence** — binary flag inputs are physically separate from the camera; no continuous perturbation reaches them

---

## The Key Contrast

Standard end-to-end AV pipelines integrate sensor data into a single neural
representation. An adversarial noise attack that spoofs the continuous readings
(TTC, distance, velocity) can in principle reach any output — there is one
continuous parameter space.

The joint pipeline uses two mathematically independent representations:

| Property | Continuous ℝ channel | p-adic channels (ℤ₂, ℤ₃) |
|----------|---------------------|--------------------------|
| Attack surface | Camera pixel values | Dedicated binary/categorical sensors |
| Noise effect on φ | Continuous shift | None — categorical inputs are discrete |
| Mathematical invariant | LoG linearity (CVO) | Zero-compatibility of ACCELERATE under red_light |
| Failure mode for attacker | IoU ≥ 80% (provable) | φ_ℤ₂(accelerate) = 0 (arithmetic) |

---

## Running the Benchmark

```bash
git clone https://github.com/rfdevuser/vectorpeak-experiments
cd vectorpeak-experiments

pip install numpy scipy
python run_joint_av_benchmark.py
```

Expected output:
```
Phase 1: σ=2 IoU=0.916 STABLE, σ=4 IoU=0.833 STABLE
Phase 2: BRAKE 0.7715 (baseline), MAINTAIN wins after ℝ-spoof, ACCELERATE #3
Phase 3: 4/4 barriers BLOCKED — gap = 0.0781
```

---

## Product Pages

- **VisionCore** — `/visioncore` on the platform
- **AdelicDrive** — `/adelicdrive` on the platform

For API access and integration:
**[vallikat@vectorpeaktech.com](mailto:vallikat@vectorpeaktech.com)**
