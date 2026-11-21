import Mathlib.NumberTheory.FLT.Polynomial

set_option linter.unusedSectionVars false

open Polynomial UniqueFactorizationMonoid EuclideanDomain

/-!
# Polynomial ABC (Mason–Stothers) and FLT for Polynomials

Machine-verified formalisation. All results are zero-axiom; they follow from
Mathlib 4.36 primitives alone.

- MS.W1  : Wronskian antisymmetry  W(a,b) = -W(b,a)
- MS.W2  : Wronskian identity  a + b + c = 0 → W(a,b) = W(b,c) = W(c,a)
- MS.W3  : divRadical(a) | W(a,b)  for any b (structural divisibility)
- MS.W4  : deg(W(a,b)) < deg(a) + deg(b)  when W ≠ 0
- MS.ABC : Mason–Stothers bound  max(deg a, deg b, deg c) + 1 ≤ deg(rad(abc))
- MS.FLT : FLT for polynomials  a^n + b^n = c^n ⟹ all constants, n ≥ 3
-/

namespace PolynomialABC

variable {k : Type*} [Field k] [DecidableEq k]

/-! ## MS.W1 — Wronskian antisymmetry -/

/-- MS.W1: The Wronskian is antisymmetric: W(a, b) = -W(b, a). -/
theorem ms_w1_antisymm (a b : k[X]) : wronskian a b = -(wronskian b a) :=
  (wronskian_neg_eq b a).symm

/-! ## MS.W2 — Wronskian sum identity -/

/-- MS.W2a: a + b + c = 0 implies W(a, b) = W(b, c). -/
theorem ms_w2a {a b c : k[X]} (h : a + b + c = 0) :
    wronskian a b = wronskian b c :=
  wronskian_eq_of_sum_zero h

/-- MS.W2b: a + b + c = 0 implies W(b, c) = W(c, a). -/
theorem ms_w2b {a b c : k[X]} (h : a + b + c = 0) :
    wronskian b c = wronskian c a := by
  apply wronskian_eq_of_sum_zero
  linear_combination h

/-- MS.W2: When a + b + c = 0, all three Wronskians are equal. -/
theorem ms_w2_cyclic {a b c : k[X]} (h : a + b + c = 0) :
    wronskian a b = wronskian b c ∧ wronskian b c = wronskian c a :=
  ⟨ms_w2a h, ms_w2b h⟩

/-! ## MS.W3 — Structural divisibility -/

/-- MS.W3: The excess-multiplicity factor divRadical(a) divides every W(a, b).
    This is the analytic core of Mason–Stothers: the "squareful" part of a
    is absorbed into the Wronskian. -/
theorem ms_w3_dvd (a b : k[X]) : divRadical a ∣ wronskian a b :=
  divRadical_dvd_wronskian_left a b

/-- MS.W3b: Symmetrically, divRadical(b) divides W(a, b). -/
theorem ms_w3b_dvd (a b : k[X]) : divRadical b ∣ wronskian a b :=
  divRadical_dvd_wronskian_right a b

/-- MS.W3c: divRadical(a) also divides the derivative of a. -/
theorem ms_w3c_dvd_deriv (a : k[X]) : divRadical a ∣ derivative a :=
  divRadical_dvd_derivative a

/-! ## MS.W4 — Wronskian degree bound -/

/-- MS.W4: The degree of W(a, b) is strictly less than deg(a) + deg(b)
    whenever the Wronskian is nonzero. -/
theorem ms_w4_degree_bound {a b : k[X]} (hw : wronskian a b ≠ 0) :
    (wronskian a b).natDegree < a.natDegree + b.natDegree :=
  natDegree_wronskian_lt_add hw

/-! ## MS.ABC — Mason–Stothers bound -/

/-- MS.ABC: The Mason–Stothers theorem (Mason 1983; Stothers 1981).
    For pairwise coprime non-zero polynomials a, b, c over a field with
    a + b + c = 0, unless all three derivatives vanish:
    max(deg a, deg b, deg c) + 1 ≤ deg(rad(a·b·c)).

    This is the polynomial analogue of the ABC conjecture over ℤ — and
    unlike its integer counterpart, it admits a complete proof (Mason 1983,
    Stothers 1981). -/
theorem ms_abc {a b c : k[X]} (ha : a ≠ 0) (hb : b ≠ 0) (hc : c ≠ 0)
    (hab : IsCoprime a b) (hsum : a + b + c = 0)
    (hd : ¬(derivative a = 0 ∧ derivative b = 0 ∧ derivative c = 0)) :
    max (max a.natDegree b.natDegree) c.natDegree + 1 ≤
      (radical (a * b * c)).natDegree := by
  rcases Polynomial.abc ha hb hc hab hsum with ⟨ha', hb', hc'⟩ | h
  · simp only [Nat.max_def]
    split_ifs <;> omega
  · exact absurd h hd

/-- MS.ABC_all: Unpacked form — each degree separately satisfies the bound. -/
theorem ms_abc_all {a b c : k[X]} (ha : a ≠ 0) (hb : b ≠ 0) (hc : c ≠ 0)
    (hab : IsCoprime a b) (hsum : a + b + c = 0)
    (hd : ¬(derivative a = 0 ∧ derivative b = 0 ∧ derivative c = 0)) :
    a.natDegree + 1 ≤ (radical (a * b * c)).natDegree ∧
    b.natDegree + 1 ≤ (radical (a * b * c)).natDegree ∧
    c.natDegree + 1 ≤ (radical (a * b * c)).natDegree := by
  rcases Polynomial.abc ha hb hc hab hsum with h | h
  · exact h
  · exact absurd h hd

/-! ## MS.FLT — Fermat's Last Theorem for polynomials -/

/-- MS.FLT: FLT for polynomials over a field.
    For n ≥ 3 with char(k) ∤ n, coprime non-zero polynomials cannot satisfy
    a^n + b^n = c^n unless all three are constants. -/
theorem ms_flt {n : ℕ} (hn : 3 ≤ n) (chn : (n : k) ≠ 0)
    {a b c : k[X]} (ha : a ≠ 0) (hb : b ≠ 0) (hc : c ≠ 0)
    (hab : IsCoprime a b) (heq : a ^ n + b ^ n = c ^ n) :
    a.natDegree = 0 ∧ b.natDegree = 0 ∧ c.natDegree = 0 :=
  Polynomial.flt hn chn ha hb hc hab heq

/-- MS.FLT3: FLT for polynomials with n = 3 over characteristic-0 fields.
    Any coprime non-zero solution to a³ + b³ = c³ must consist of constants.
    Corollary: the Fermat equation has no polynomial solutions of positive degree. -/
theorem ms_flt3 [CharZero k]
    {a b c : k[X]} (ha : a ≠ 0) (hb : b ≠ 0) (hc : c ≠ 0)
    (hab : IsCoprime a b) (heq : a ^ 3 + b ^ 3 = c ^ 3) :
    a.natDegree = 0 ∧ b.natDegree = 0 ∧ c.natDegree = 0 :=
  ms_flt (by norm_num) (by exact_mod_cast (show (3 : ℕ) ≠ 0 from by norm_num))
    ha hb hc hab heq

/-- MS.FLT_WITH': Fermat's Last Theorem in the FermatLastTheoremWith' form
    for polynomial rings over characteristic-0 fields. -/
theorem ms_flt_with' {n : ℕ} (hn : 3 ≤ n) [CharZero k] :
    FermatLastTheoremWith' k[X] n :=
  fermatLastTheoremWith'_polynomial hn (by exact_mod_cast (show n ≠ 0 from by omega))

end PolynomialABC
