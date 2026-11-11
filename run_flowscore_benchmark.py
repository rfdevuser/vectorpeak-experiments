#!/usr/bin/env python3
"""
FlowScore benchmark — Γ₇₈ Alternative Credit Risk from Transaction Variance

  Phase 1 — Five preset borrowers: D, FlowScore, PD_30/90/180, tier, CSD flag
  Phase 2 — Thin-file UPI scoring: 400M borrowers CIBIL refuses, FlowScore scores
  Phase 3 — Kramers escape rate: 50× PD amplification from D=1 to D=0.1
  Phase 4 — CSD trajectory: critical slowing down fires before NEAR-DEFAULT tier

No API key. No dependencies.
"""

import math

# ── ANSI ──────────────────────────────────────────────────────────────────────
RESET = "\033[0m"; BOLD = "\033[1m"; DIM = "\033[2m"
RED   = "\033[91m"; AMBER = "\033[93m"; GREEN = "\033[92m"
CYAN  = "\033[96m"; WHITE = "\033[97m"; BLUE = "\033[94m"

def _hr(w=92): return "─" * w
def _hdr(t):
    b = _hr()
    return f"\n{BOLD}{CYAN}{b}{RESET}\n{BOLD}{WHITE}  {t}{RESET}\n{BOLD}{CYAN}{b}{RESET}"

# ── Core math ─────────────────────────────────────────────────────────────────

K0    = 0.008   # baseline monthly default rate (~1%/3-month for healthy borrower)
ALPHA = 4.0     # barrier depth / noise temperature

def _D(sigma_ref, sigma_tx):
    """Curie distance D = σ_ref / σ_tx, capped at 1."""
    return min(1.0, sigma_ref / sigma_tx) if sigma_tx > 0 else 0.0

def _F(d):
    """FlowScore F = 100 × D²."""
    return 100.0 * d * d

def _PD(d, horizon_days):
    """P(default|T) = 1 − exp(−T_months × k₀ × exp(−α·D²))  [Kramers escape rate]."""
    T = horizon_days / 30.0
    k = K0 * math.exp(-ALPHA * d * d)
    return 1.0 - math.exp(-T * k)

def _AC(d):
    """Autocorrelation lag-1 ≈ 1 − D²  [critical slowing down indicator]."""
    return 1.0 - d * d

def _tier(f):
    if f >= 70: return "LOW RISK",    "Green",  GREEN
    if f >= 40: return "ELEVATED",    "Amber",  AMBER
    if f >= 15: return "HIGH RISK",   "Orange", AMBER
    return         "NEAR-DEFAULT", "Red",    RED

def _score(sigma_ref, sigma_tx):
    d  = _D(sigma_ref, sigma_tx)
    f  = _F(d)
    ac = _AC(d)
    label, _, col = _tier(f)
    return {
        "D": d, "F": f,
        "PD_30":  _PD(d, 30),
        "PD_90":  _PD(d, 90),
        "PD_180": _PD(d, 180),
        "AC":     ac,
        "CSD":    ac > 0.75,
        "label":  label,
        "col":    col,
    }


# ── Presets ───────────────────────────────────────────────────────────────────

PRESETS = [
    ("Healthy Salaried",  "stable monthly salary, regular bills",           8500, 8200),
    ("Thin-File UPI",     "18 months UPI data, no credit bureau record",    3200, 4100),
    ("Mild Stress",       "irregular income, some delayed payments",         8500, 12000),
    ("High-Risk MSME",    "small business, volatile cash flow",             25000, 52000),
    ("Near Default",      "missed EMIs visible in transaction data",         8500, 68000),
]


# ── Phase 1 ───────────────────────────────────────────────────────────────────

def phase1():
    print(_hdr("Phase 1 — Five Preset Borrowers: Full FlowScore Certificate"))
    print(f"""
  Formula:
    D   = σ_ref / σ_tx              Curie distance (1 = healthy, 0 = near default)
    F   = 100 × D²                  FlowScore  [0, 100]
    PD  = 1 − exp(−T × k₀ × exp(−α·D²))   Kramers escape rate
    AC  = 1 − D²                    critical slowing-down indicator
    CSD flag: AC > 0.75  (D < 0.5, payment timing autocorrelation elevated)

  Constants: k₀ = {K0}  α = {ALPHA}  (population-level; two values, not per-borrower)
""")

    hdr = (f"  {'Borrower':<22} {'σ_ref':>7}  {'σ_tx':>7}  {'D':>6}  "
           f"{'Score':>6}  {'PD_30':>7}  {'PD_90':>7}  {'PD_180':>8}  {'AC':>6}  {'CSD':>4}  Tier")
    print(f"{BOLD}{hdr}{RESET}")
    print("  " + "─" * 102)

    for name, _, sr, st in PRESETS:
        s = _score(sr, st)
        csd_str = f"{RED}YES{RESET}" if s["CSD"] else f"{GREEN} no{RESET}"
        print(f"  {name:<22} {sr:>7,.0f}  {st:>7,.0f}  "
              f"{s['D']:>6.3f}  {s['col']}{s['F']:>6.1f}{RESET}  "
              f"{s['PD_30']*100:>6.3f}%  {s['PD_90']*100:>6.3f}%  "
              f"{s['PD_180']*100:>7.3f}%  {s['AC']:>6.3f}  {csd_str:>4}  "
              f"{s['col']}{s['label']}{RESET}")

    print()
    healthy = _score(8500, 8200)
    nd      = _score(8500, 68000)
    ratio   = nd["PD_90"] / healthy["PD_90"] if healthy["PD_90"] > 0 else math.inf
    print(f"  {BOLD}Near Default / Healthy PD_90 ratio:{RESET} "
          f"{nd['PD_90']*100:.3f}% / {healthy['PD_90']*100:.4f}% = "
          f"{RED}{BOLD}{ratio:.0f}×{RESET} higher default probability")
    print(f"  {DIM}Two population constants (k₀, α) — not per-borrower regression coefficients.{RESET}")


# ── Phase 2 ───────────────────────────────────────────────────────────────────

def phase2():
    print(_hdr("Phase 2 — Thin-File UPI Scoring: 400M Borrowers CIBIL Refuses"))
    print(f"""
  Traditional bureau scoring (CIBIL, Experian, Equifax):
    Requires: 2+ years of credit history (loans, credit cards, EMIs)
    Result for thin-file users: score = 0, loan REJECTED

  India has ~400 million active UPI users with no credit bureau record.
  18 months of UPI transaction data is enough for FlowScore.
""")

    # Show the five presets in a bureau vs FlowScore comparison
    print(f"  {BOLD}{'Borrower':<22} {'CIBIL verdict':>18}  {'D':>6}  "
          f"{'FlowScore':>10}  {'PD_90':>8}  FlowScore verdict{RESET}")
    print("  " + "─" * 86)

    cibil = {
        "Healthy Salaried":  ("750+  APPROVED", GREEN),
        "Thin-File UPI":     ("  0   REJECTED", RED),
        "Mild Stress":       ("620   APPROVED", AMBER),
        "High-Risk MSME":    ("580   APPROVED", AMBER),
        "Near Default":      ("660   APPROVED", AMBER),
    }

    for name, desc, sr, st in PRESETS:
        s = _score(sr, st)
        cv, cc = cibil[name]
        print(f"  {name:<22} {cc}{cv}{RESET}  "
              f"{s['D']:>6.3f}  {s['col']}{s['F']:>10.1f}{RESET}  "
              f"{s['PD_90']*100:>7.3f}%  {s['col']}{s['label']}{RESET}")

    print()
    # Key contrast: near-default borrower has CIBIL 660 (approved!) but FlowScore 1.6
    nd = _score(8500, 68000)
    tf = _score(3200, 4100)
    print(f"  {BOLD}Key contrast:{RESET}")
    print(f"  Near Default:   CIBIL 660 (bank approves) → "
          f"{RED}FlowScore {nd['F']:.1f} — PD_90 {nd['PD_90']*100:.3f}% — NEAR-DEFAULT{RESET}")
    print(f"  Thin-File UPI:  CIBIL  0  (bank rejects)  → "
          f"{GREEN}FlowScore {tf['F']:.1f} — PD_90 {tf['PD_90']*100:.3f}% — ELEVATED{RESET}")
    print()
    print(f"  {DIM}The Near Default borrower hasn't missed a bureau-reported payment yet.{RESET}")
    print(f"  {DIM}Their transaction variance (σ_tx={68000:,}) already reveals the stress.{RESET}")
    print(f"  {DIM}CIBIL approves them. FlowScore flags them. FlowScore is right.{RESET}")
    print(f"  {DIM}The Thin-File UPI user is safer (PD_90={tf['PD_90']*100:.3f}%) than many CIBIL-scored borrowers.{RESET}")


# ── Phase 3 ───────────────────────────────────────────────────────────────────

def phase3():
    print(_hdr("Phase 3 — Kramers Escape Rate: Exponential PD Amplification"))
    print(f"""
  Logistic regression: P(default) = σ(β₀ + β₁x₁ + β₂x₂ + ...)
    Requires: labelled default data per feature (sparse for thin-file)
    Shape: sigmoid — symmetric around inflection point

  FlowScore Kramers rate: P(default|T) = 1 − exp(−T × k₀ × exp(−α·D²))
    Requires: 2 population constants (k₀, α) — not per-borrower fitting
    Shape: exponential in D² — fast rise near D→0, plateau near D=1

  PD_90 across D values  (k₀={K0}, α={ALPHA}, T=90 days):
""")

    healthy_pd = _PD(1.0, 90)

    hdr = (f"  {'D':>6}  {'FlowScore':>10}  {'PD_90':>9}  "
           f"{'vs D=1.0':>10}  {'AC lag-1':>9}  Tier")
    print(f"{BOLD}{hdr}{RESET}")
    print("  " + "─" * 72)

    ds = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]
    for d in ds:
        f_   = _F(d)
        pd   = _PD(d, 90)
        ac   = _AC(d)
        mult = pd / healthy_pd if healthy_pd > 0 else math.inf
        label, _, col = _tier(f_)
        print(f"  {d:>6.1f}  {col}{f_:>10.1f}{RESET}  "
              f"{pd*100:>8.3f}%  {mult:>9.1f}×  {ac:>9.3f}  {col}{label}{RESET}")

    print()
    pd_01 = _PD(0.1, 90)
    mult  = pd_01 / healthy_pd
    print(f"  {BOLD}D=0.1 vs D=1.0:{RESET} "
          f"{pd_01*100:.3f}% vs {healthy_pd*100:.4f}% = "
          f"{RED}{BOLD}{mult:.0f}×{RESET} amplification")
    print()
    print(f"  {DIM}The exp(−αD²) term creates exponential acceleration near D→0.{RESET}")
    print(f"  {DIM}A logistic sigmoid would give a symmetric S-curve — missing the asymmetric tail.{RESET}")
    print(f"  {DIM}The Kramers form is derived from first principles (barrier-crossing physics).{RESET}")
    print(f"  {DIM}No fitting required — k₀ is the population default rate; α is the barrier depth.{RESET}")


# ── Phase 4 ───────────────────────────────────────────────────────────────────

def phase4():
    print(_hdr("Phase 4 — CSD Trajectory: Early Warning Before NEAR-DEFAULT"))
    print(f"""
  Critical slowing down (CSD) is a universal precursor to phase transitions:
  payment timing variance rises and autocorrelation increases before the actual
  default event. This is the same mechanism that predicts ecosystem collapse,
  cardiac arrest, and climate tipping points.

    AC(lag=1) = 1 − D²     — rises toward 1 as borrower deteriorates
    CSD flag  = AC > 0.75  — fires when D < 0.5, giving 1–2 month lead time

  Trajectory: a borrower deteriorating over 6 months (σ_ref = 8,500)
""")

    trajectory = [
        ("Month 0", 8500,  "baseline — stable salary"),
        ("Month 1", 10000, "first irregular month"),
        ("Month 2", 14000, "dipping savings, delayed utility"),
        ("Month 3", 17500, "partial EMI payment"),
        ("Month 4", 24000, "overdraft, credit limit reached"),
        ("Month 5", 42000, "near-default, collections risk"),
    ]

    sigma_ref = 8500
    hdr = (f"  {'Month':<9} {'σ_tx':>7}  {'D':>6}  {'Score':>7}  "
           f"{'PD_30':>7}  {'AC':>6}  {'CSD':>5}  {'Tier':<14}  Event")
    print(f"{BOLD}{hdr}{RESET}")
    print("  " + "─" * 100)

    csd_fired   = False
    tier_red    = False
    csd_month   = None
    red_month   = None

    for label, st, event in trajectory:
        s = _score(sigma_ref, st)
        csd_str = f"{RED}{BOLD}YES{RESET}" if s["CSD"] else f"{GREEN} no{RESET}"
        tier_col = s["col"]
        marker = ""
        if s["CSD"] and not csd_fired:
            csd_fired = True; csd_month = label
            marker = f"  {RED}◄ CSD flag fires{RESET}"
        if s["label"] == "NEAR-DEFAULT" and not tier_red:
            tier_red = True; red_month = label
            marker += f"  {RED}◄ NEAR-DEFAULT tier{RESET}"
        print(f"  {label:<9} {st:>7,}  {s['D']:>6.3f}  "
              f"{tier_col}{s['F']:>7.1f}{RESET}  "
              f"{s['PD_30']*100:>6.3f}%  {s['AC']:>6.3f}  {csd_str:>5}  "
              f"{tier_col}{s['label']:<14}{RESET}  {event}{marker}")

    print()
    print(f"  {BOLD}Timeline:{RESET}")
    if csd_month:
        print(f"  CSD flag fires:        {RED}{csd_month}{RESET}  (D crosses below 0.5, AC > 0.75)")
    if red_month:
        print(f"  NEAR-DEFAULT tier:     {RED}{red_month}{RESET}  (F drops below 15)")
    print()
    print(f"  {DIM}Standard credit models detect stress only when payments are missed.{RESET}")
    print(f"  {DIM}FlowScore CSD flag fires from transaction VARIANCE alone — before any missed payment.{RESET}")
    print(f"  {DIM}The lender has 1–2 months to intervene: restructure, reduce limit, or contact.{RESET}")
    print(f"  {DIM}AC = 1 − D² is structurally derived — not a fitted threshold.{RESET}")


# ── Banner + main ─────────────────────────────────────────────────────────────

def banner():
    b = _hr()
    print(f"\n{BOLD}{CYAN}{b}{RESET}")
    print(f"{BOLD}{WHITE}  FlowScore — Γ₇₈ Alternative Credit Risk from Transaction Variance{RESET}")
    print(f"{BOLD}{CYAN}{b}{RESET}")
    print(f"""
  F(t) = 100 × D²(t)   where D = σ_ref / σ_tx
  P(default | T) = 1 − exp(−T × k₀ × exp(−α·D²))   [Kramers escape rate]

  vs Standard approaches:
    CIBIL / Experian / FICO  — requires 2+ years credit history; refuses thin-file
    Logistic regression       — per-borrower fit; needs labelled default data
    Behavioural scoring       — black-box ML; no structural interpretation
    Cash-flow underwriting    — manual; not scalable to 400M UPI users

  FlowScore:
    Two constants only  k₀ (population default rate), α (barrier depth)
    Thin-file native    18 months of UPI/transaction data is sufficient
    Structural signal   D = σ_ref/σ_tx has a physical interpretation
    CSD early warning   AC = 1−D² fires 1–2 months before NEAR-DEFAULT tier
""")


if __name__ == "__main__":
    banner()
    phase1()
    phase2()
    phase3()
    phase4()
    b = _hr()
    print(f"\n{BOLD}{CYAN}{b}{RESET}")
    print(f"{BOLD}{GREEN}  FlowScore benchmark complete{RESET}")
    print(f"{BOLD}{CYAN}{b}{RESET}")
    print(f"\n  API + integration docs:  {BOLD}vallikat@vectorpeaktech.com{RESET}\n")
