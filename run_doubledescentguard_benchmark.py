"""
DoubleDescentGuard — Γ₅₆ Double Descent Certificate Benchmark

Theorem Γ₅₆.1 — Generalisation projection fraction:
    F_gen(ρ) = exp(−2π/ρ²)
    ρ = p_eff / n_eff   (effective capacity ratio)

    p_eff = p / (1 + reg_strength)   (regularisation reduces effective capacity)
    n_eff = n · SNR / (1 + SNR)      (noise reduces effective sample count)

Corollaries:
    ρ = 1   →  F_gen = exp(−2π) ≈ 0.19%   ← double descent peak, maximum risk
    ρ* ≈ 3.01  →  F_gen = 50%             ← half-generalisation threshold
    ρ_th = 4   →  F_gen ≈ 67.5%           ← production-safe floor

Three phases:
  1. The F_gen curve — what the double descent peak actually looks like
  2. Financial model certifications — six real deployment decisions
  3. The regularisation lever — same model, three different fates

ModelGuard (Γ₄₉) tells you WHICH PHASE you're in (D = p/n).
DoubleDescentGuard tells you WHAT FRACTION of your model actually generalises.

Pure Python standard library only.
"""

import math

BOLD  = "\033[1m"
RED   = "\033[91m"
AMBER = "\033[93m"
GREEN = "\033[92m"
CYAN  = "\033[96m"
RESET = "\033[0m"

# ── Core maths (self-contained) ────────────────────────────────────────────────

RHO_STAR      = math.sqrt(2.0 * math.pi / math.log(2.0))   # ≈ 3.0108
RHO_TH        = 4.0
F_GEN_PEAK    = math.exp(-2.0 * math.pi)                    # ≈ 0.001867
F_GEN_THERMAL = math.exp(-math.pi / 8.0)                    # ≈ 0.6752


def p_eff(p, reg):
    return p / (1.0 + reg)


def n_eff(n, snr):
    return n * snr / (1.0 + snr)


def rho(p, n, reg, snr):
    return p_eff(p, reg) / n_eff(n, snr)


def F_gen(r):
    return math.exp(max(-2.0 * math.pi / r ** 2, -745.0))


def regime(r):
    if r < 1.0:   return "UNDERFIT",   RED
    if r < 1.5:   return "CRITICAL",   RED
    if r < RHO_STAR: return "PARADOX", AMBER
    if r < RHO_TH:   return "MARGINAL", AMBER
    return "ACCESSIBLE", GREEN


def verdict(reg_name):
    return {
        "UNDERFIT":   (RED,   "DO_NOT_DEPLOY"),
        "CRITICAL":   (RED,   "DO_NOT_DEPLOY"),
        "PARADOX":    (RED,   "DO_NOT_DEPLOY"),
        "MARGINAL":   (AMBER, "CAUTION"),
        "ACCESSIBLE": (GREEN, "APPROVED"),
    }[reg_name]


# ── Phase 1: The F_gen curve ───────────────────────────────────────────────────

def run_fgen_curve():
    print(f"\n{BOLD}[PHASE 1: The F_gen Curve — What the Double Descent Peak Looks Like]{RESET}\n")
    print(f"  F_gen(ρ) = exp(−2π/ρ²)   where ρ = p_eff / n_eff\n")

    probe = [
        (0.50, "deeply underfit"),
        (0.80, "approaching peak"),
        (0.95, "near peak"),
        (1.00, "← DOUBLE DESCENT PEAK"),
        (1.10, "just past peak"),
        (1.50, "critical exit"),
        (2.00, "overparameterised"),
        (RHO_STAR, "half-generalisation threshold (ρ*)"),
        (3.50, "marginal"),
        (RHO_TH, "production-safe floor (ρ_th)"),
        (5.00, "safely overparameterised"),
        (8.00, "large-scale overparameterised"),
    ]

    print(f"  {'ρ':>6}  {'F_gen %':>10}  {'Regime':<12}  Notes")
    print(f"  {'─'*6}  {'─'*10}  {'─'*12}  {'─'*44}")

    for r, note in probe:
        fg   = F_gen(r)
        name, col = regime(r)
        is_peak = abs(r - 1.0) < 0.001
        is_star = abs(r - RHO_STAR) < 0.001
        is_th   = abs(r - RHO_TH) < 0.001
        flag    = f"  {RED}← MAXIMUM RISK{RESET}" if is_peak else ""
        flag    = f"  {AMBER}← 50% threshold{RESET}" if is_star else flag
        flag    = f"  {GREEN}← safe floor{RESET}" if is_th else flag
        print(f"  {r:>6.2f}  {fg*100:>9.4f}%  {col}{name:<12}{RESET}  {note}{flag}")

    print()
    print(f"  At ρ = 1 (double descent peak):")
    print(f"    F_gen = {F_GEN_PEAK*100:.4f}%  — less than 1 in 500 capacity units generalise")
    print(f"    99.81% of what the model learned is trapped at the interpolation threshold")
    print(f"    Validation loss looks normal. The generalisation deficit is invisible to it.")
    print()
    print(f"  At ρ* ≈ {RHO_STAR:.4f}: F_gen = 50%  — half-generalisation recovered")
    print(f"  At ρ_th = {RHO_TH:.1f}:    F_gen = {F_GEN_THERMAL*100:.1f}%  — production safe")


# ── Phase 2: Six financial model certifications ────────────────────────────────

MODELS = [
    {
        "label": "Credit scoring (critical)",
        "task":  "credit",
        "p": 15_000, "n": 50_000, "snr": 0.35, "reg": 0.10,
        "note": "near interpolation threshold after reg",
    },
    {
        "label": "Credit scoring (safe)",
        "task":  "credit",
        "p": 60_000, "n": 50_000, "snr": 0.35, "reg": 0.10,
        "note": "4× more parameters, same data",
    },
    {
        "label": "Trading signal (paradox)",
        "task":  "trading",
        "p": 150, "n": 1_250, "snr": 0.05, "reg": 0.0,
        "note": "150 factors on 5yr daily data, low SNR",
    },
    {
        "label": "Trading signal (accessible)",
        "task":  "trading",
        "p": 350, "n": 1_250, "snr": 0.05, "reg": 0.0,
        "note": "350 factors — same data, more capacity",
    },
    {
        "label": "Fraud detection (large)",
        "task":  "fraud",
        "p": 300_000, "n": 100_000, "snr": 0.45, "reg": 0.001,
        "note": "neural net, large training set",
    },
    {
        "label": "Risk factor model",
        "task":  "risk_factor",
        "p": 1_500, "n": 5_000, "snr": 0.25, "reg": 0.05,
        "note": "near critical — VaR implications",
    },
]

TASK_NOTES = {
    "credit": {
        "CRITICAL":   "Val Gini will not reflect production performance. Regulatory approval unlikely.",
        "PARADOX":    "Production Gini significantly below validation. Increase capacity or reduce features.",
        "ACCESSIBLE": "F_gen ≥ 67.5%. Suitable for IRB/CECL submission.",
        "MARGINAL":   "Monitor Gini stability in production. Document ρ for model validation.",
    },
    "trading": {
        "PARADOX":    "Live Sharpe expected significantly below backtest. Do not allocate capital.",
        "ACCESSIBLE": "Backtest Sharpe expected to persist with normal degradation only.",
        "MARGINAL":   "Paper trade before live — wide Sharpe confidence interval.",
    },
    "fraud": {
        "ACCESSIBLE": "Production false negative rate expected to match validation.",
        "CRITICAL":   "Production FNR will exceed validation FNR.",
    },
    "risk_factor": {
        "CRITICAL":   "Factor covariance matrix near-singular. VaR certification invalid.",
        "MARGINAL":   "Covariance estimates usable with Ledoit-Wolf shrinkage applied.",
        "ACCESSIBLE": "Factor covariance stable for regulatory VaR.",
        "PARADOX":    "Covariance estimates unreliable. Use shrinkage or reduce factors.",
    },
}


def run_certifications():
    print(f"\n{BOLD}[PHASE 2: Financial Model Certifications — Six Deployment Decisions]{RESET}\n")
    print(f"  {'Model':<30} {'ρ':>6}  {'F_gen %':>9}  {'Regime':<12}  {'Verdict':<16}  p_eff → p_safe")
    print(f"  {'─'*30} {'─'*6}  {'─'*9}  {'─'*12}  {'─'*16}  {'─'*20}")

    for m in MODELS:
        pe  = p_eff(m["p"], m["reg"])
        ne  = n_eff(m["n"], m["snr"])
        r   = pe / ne
        fg  = F_gen(r)
        name, col = regime(r)
        vcol, vstr = verdict(name)
        p_safe = math.ceil(RHO_STAR * ne * (1.0 + m["reg"]))
        p_opt  = math.ceil(RHO_TH   * ne * (1.0 + m["reg"]))
        print(
            f"  {m['label']:<30} {r:>6.3f}  {fg*100:>8.3f}%  {col}{name:<12}{RESET}  "
            f"{vcol}{vstr:<16}{RESET}  {m['p']:,} → {p_safe:,}"
        )

    print()
    print(f"  {BOLD}Detail — three decisions explained:{RESET}\n")

    for m in MODELS[:3]:
        pe   = p_eff(m["p"], m["reg"])
        ne   = n_eff(m["n"], m["snr"])
        r    = pe / ne
        fg   = F_gen(r)
        name, col = regime(r)
        vcol, vstr = verdict(name)
        p_safe = math.ceil(RHO_STAR * ne * (1.0 + m["reg"]))
        task_note = TASK_NOTES.get(m["task"], {}).get(name, "")

        print(f"  {col}{m['label']}{RESET}")
        print(f"    p={m['p']:,}  n={m['n']:,}  SNR={m['snr']}  reg={m['reg']}")
        print(f"    p_eff={pe:,.0f}  n_eff={ne:,.0f}  ρ={r:.4f}")
        print(f"    F_gen = {fg*100:.4f}%   regime: {col}{name}{RESET}   verdict: {vcol}{vstr}{RESET}")
        if task_note:
            print(f"    {AMBER}{task_note}{RESET}")
        print(f"    To reach ρ* (F_gen=50%): need p_eff ≥ {p_safe:,}")
        print()

    # Highlight the trading paradox
    m = MODELS[2]
    pe = p_eff(m["p"], m["reg"])
    ne = n_eff(m["n"], m["snr"])
    r  = pe / ne
    fg = F_gen(r)
    m2 = MODELS[3]
    pe2 = p_eff(m2["p"], m2["reg"])
    ne2 = n_eff(m2["n"], m2["snr"])
    r2  = pe2 / ne2
    fg2 = F_gen(r2)
    print(f"  {BOLD}Trading model contrast:{RESET}")
    print(f"    150 factors:  ρ={r:.3f}  F_gen={fg*100:.2f}%  → {RED}PARADOX — DO NOT DEPLOY{RESET}")
    print(f"    350 factors:  ρ={r2:.3f}  F_gen={fg2*100:.1f}%   → {GREEN}ACCESSIBLE — APPROVED{RESET}")
    print(f"    Adding 200 more factors (same data) rescues generalisation.")
    print(f"    This is the double descent paradox: more parameters → better, not worse.")


# ── Phase 3: The regularisation lever ─────────────────────────────────────────

def run_regularisation_lever():
    print(f"\n{BOLD}[PHASE 3: The Regularisation Lever — Same Model, Three Different Fates]{RESET}\n")

    base_p, base_n, base_snr = 20_000, 50_000, 0.30
    base_ne = n_eff(base_n, base_snr)

    reg_configs = [
        (0.0,  "no regularisation"),
        (0.30, "moderate L2 / dropout"),
        (1.50, "heavy regularisation"),
        (5.00, "very heavy (near linear model)"),
    ]

    print(f"  Fixed: p={base_p:,}  n={base_n:,}  SNR={base_snr}")
    print(f"  n_eff = {base_ne:,.0f}  (SNR converts {base_n:,} samples to {base_ne:,.0f} effective)\n")
    print(f"  {'reg_strength':>14}  {'p_eff':>10}  {'ρ':>7}  {'F_gen %':>9}  {'Regime':<12}  {'Verdict'}")
    print(f"  {'─'*14}  {'─'*10}  {'─'*7}  {'─'*9}  {'─'*12}  {'─'*16}")

    for reg, desc in reg_configs:
        pe   = p_eff(base_p, reg)
        r    = pe / base_ne
        fg   = F_gen(r)
        name, col = regime(r)
        vcol, vstr = verdict(name)
        print(
            f"  {reg:>14.2f}  {pe:>10,.0f}  {r:>7.3f}  {fg*100:>8.3f}%  "
            f"{col}{name:<12}{RESET}  {vcol}{vstr}{RESET}  ({desc})"
        )

    r0 = p_eff(base_p, 0.0) / base_ne
    r3 = p_eff(base_p, 1.50) / base_ne
    fg0 = F_gen(r0)
    fg3 = F_gen(r3)
    print()
    print(f"  {BOLD}Same model. Same data. Zero → 1.5 reg_strength:{RESET}")
    print(f"    F_gen: {fg0*100:.4f}%  →  {fg3*100:.1f}%  (ρ: {r0:.3f} → {r3:.3f})")
    print(f"    Regularisation is a ρ-shift lever — it moves the model along the F_gen curve.")
    print()
    print(f"  {BOLD}What ModelGuard (D = p/n) would see:{RESET}")
    D = base_p / base_n
    print(f"    D = {base_p:,} / {base_n:,} = {D:.4f}   (ordered phase — same for all three)")
    print(f"    ModelGuard: all three are in the ordered phase. Same D, same risk flag.")
    print(f"    DoubleDescentGuard: ρ varies by reg_strength → three different F_gen values.")
    print(f"    {AMBER}D is blind to regularisation strength and SNR. ρ is not.{RESET}")


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    print(f"\n{BOLD}{'═'*68}{RESET}")
    print(f"{BOLD}  DOUBLEDESCENTGUARD — DOUBLE DESCENT CERTIFICATE  (Γ₅₆){RESET}")
    print(f"{BOLD}{'═'*68}{RESET}")
    print(f"  F_gen(ρ) = exp(−2π/ρ²)  — generalisation projection fraction")
    print(f"  At ρ = 1:  F_gen = {F_GEN_PEAK*100:.4f}%  ← double descent peak")
    print(f"  At ρ* ≈ {RHO_STAR:.2f}: F_gen = 50.0%  ← half-generalisation threshold")
    print(f"  At ρ  = {RHO_TH:.1f}: F_gen = {F_GEN_THERMAL*100:.1f}%  ← production-safe floor")

    run_fgen_curve()
    run_certifications()
    run_regularisation_lever()

    print(f"\n{BOLD}{'═'*68}{RESET}")
    print(f"  Val loss    : measures bias² + variance — blind to generalisation fraction")
    print(f"  D = p/n     : (ModelGuard) phase classification — blind to SNR and reg")
    print(f"  ρ = p_eff/n_eff: (DDGuard) exact F_gen — accounts for both")
    print(f"  At ρ = 1    : {RED}99.81% of learned capacity is trapped — do not deploy{RESET}")
    print(f"  At ρ ≥ {RHO_TH:.1f}  : {GREEN}F_gen ≥ 67.5% — production safe{RESET}")
    print(f"{BOLD}{'═'*68}{RESET}\n")


if __name__ == "__main__":
    main()
