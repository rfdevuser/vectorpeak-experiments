# VisionCore — Post Copy

---

## LinkedIn

```
I ran a test on something that gets treated as a solved problem in computer vision.

Take an image. Apply five different brightness levels — deep shadow, overcast,
normal, overexposed, direct sunlight. Ask a standard CNN front-end and a
zero-weight vision operator to describe what they see.

The CNN shifts its activations on every single brightness change. The
zero-weight operator returns a bit-identical fingerprint across all five.
Not approximately the same. Identical. Same hash. Every time.

The reason is mathematical, not empirical. The operator is built from a
single closed-form function that commutes with scalar multiplication —
so multiplying the image by any positive constant cancels out before the
measurement is taken. No training required. No augmentation required.
The invariance is built into the structure.

The second test is adversarial stability. Apply the smallest perturbation
a human cannot see (4 out of 255 pixel units, per-pixel). The CNN shifts
13.8% from noise that is literally invisible. The zero-weight operator's
structural contours at the two coarser scales stay above 80% overlap.

This matters for any vision system deployed in variable lighting — outdoor
cameras, medical imaging, satellite imagery, robotics. A front-end that
shifts with the lighting forces the rest of the model to compensate through
training data, augmentation, and fine-tuning. A front-end that doesn't
shift eliminates that cost entirely.

The benchmark runs locally with numpy and scipy. No GPU. No pretrained model.
No API key.
[link to repo]

The properties shown are exact — not measured approximations. If the math
is wrong the benchmark fails. It hasn't failed.
```

---

## Reddit — r/MachineLearning

**Title:**
```
Zero-weight vision front-end: exact illumination invariance across 5 brightness levels, bit-identical fingerprint — reproducible benchmark (numpy/scipy only)
```

**Body:**
```
Built a benchmark to verify two properties of a LoG-based zero-weight vision front-end against a standard random-weight CNN stem.

**Property 1 — Illumination invariance (exact)**

The operator is ∇²G_σ (Laplacian of Gaussian). It satisfies:

  ∇²G_σ * (aI) = a · (∇²G_σ * I)

So the zero-crossings of a·f(x) are identical to those of f(x) for any a > 0.
This is a mathematical identity, not an approximation.

Benchmark result across 5 brightness levels (a = 0.2, 0.5, 1.0, 1.5, 2.0):

  Transform                    Edge pixels   Fingerprint       Result
  baseline       (a=1.00)            3,252   37bcc3882433    [INVARIANT]
  dim            (a=0.20)            3,252   37bcc3882433    [INVARIANT]
  reduced        (a=0.50)            3,252   37bcc3882433    [INVARIANT]
  bright         (a=1.50)            3,252   37bcc3882433    [INVARIANT]
  overexposed    (a=2.00)            3,252   37bcc3882433    [INVARIANT]

SHA-256 fingerprint is bit-identical across all five transforms.
CNN stem activations shift proportionally on every change.

**Property 2 — Adversarial stability**

L∞ perturbation ε = 4/255 applied. IoU of zero-crossing maps before/after:

  Scale σ     IoU    Result
  σ = 1.0    0.27   NOISE-SENSITIVE  (fine scale — by design)
  σ = 2.0    0.82   STABLE
  σ = 4.0    0.94   STABLE

CNN stem shifted 13.8% from invisible noise. CVO coarse channels stay above 80% IoU.

The σ=1.0 channel being noise-sensitive is intentional — it carries texture/HF detail. The coarse channels carry scene geometry and are structurally stable.

**Why it matters:**
Illumination augmentation during training exists to compensate for a front-end that shifts with lighting. If the front-end is exactly invariant, that cost disappears.

Benchmark (numpy/scipy, no GPU, no pretrained model):
https://github.com/rfdevuser/vectorpeak-experiments

Interested in whether others have benchmarked LoG-based front-ends against learned stems on real datasets — particularly on out-of-distribution lighting conditions.
```

---

## Discord — r/MachineLearning / CV communities `#showcase`

```
Benchmarked a zero-weight LoG-based vision front-end against a CNN stem on two properties:

1. Illumination invariance — ∇²G_σ*(aI) = a·(∇²G_σ*I), so zero-crossings are bit-identical across any brightness scaling. Verified across 5 brightness levels, identical SHA-256 fingerprint each time. CNN activations shift on every change.

2. Adversarial stability — L∞ ε=4/255 perturbation. CVO coarse scales (σ=2,4) stay above 80% IoU. CNN stem shifts 13.8% from invisible noise.

No learned weights. No GPU. numpy/scipy only.

Repo: https://github.com/rfdevuser/vectorpeak-experiments

Curious whether others have compared LoG front-ends to learned stems on real out-of-distribution lighting — the invariance holds exactly in theory but I'd like to know how it performs on natural image datasets.
```

---

## X / Twitter — 4-tweet thread

**Tweet 1 (hook — attach terminal screenshot or GIF):**
```
Applied 5 brightness levels to the same image.

The CNN front-end shifted its output every single time.
The zero-weight operator returned the exact same fingerprint every time.

Not approximately the same. Bit-identical.

Here's why that's not surprising — and why it matters: 🧵
```

**Tweet 2 (the math):**
```
The operator is the Laplacian of Gaussian: ∇²G_σ

It satisfies one identity:
  ∇²G_σ * (aI) = a · (∇²G_σ * I)

So the zero-crossings of a·f(x) = zero-crossings of f(x) for any a > 0.

Multiply the image by 0.2 or 2.0 — the structure is identical.
This is a mathematical guarantee, not a training outcome.
```

**Tweet 3 (adversarial result):**
```
Second test: L∞ perturbation of 4/255 per pixel — invisible to humans.

CNN stem: 13.8% activation shift from noise no eye can detect.

Zero-weight operator (coarse scales):
  σ = 2.0 → IoU 0.82 ✓
  σ = 4.0 → IoU 0.94 ✓

The scene geometry is preserved. The fine-scale channel is intentionally noise-sensitive — that's where texture lives.
```

**Tweet 4 (the link):**
```
Zero learned weights. No GPU. No pretrained model. No API key.

The benchmark runs in under 10 seconds with numpy and scipy:
[repo]

If the math is wrong, the benchmark fails. It hasn't failed.
```
