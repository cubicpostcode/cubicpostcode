# Rank and unrank cost of Models C, D and H5: what is proven, what is measured, what is cited

**Date:** 2026-11-11 (Investigation 3)
**Purpose:** correct an overstatement in file 20 (complexity paragraph) and file 21 (which refers to it), as asked by the independent review of 2026-11-10. The original text of files 20 and 21 is left unchanged; this note supersedes their complexity sentences.

## The statement being corrected

File 20 says that unrank "uses one integer cube root of `n`, at most one integer square root …, and `O(1)` further operations; with integer Newton iteration this is `O(M(b))` bit operations."

**Verdict.**

- The **operation count is correct**.
- **"`O(M(b))` bit operations" is not established** for the integer Newton iteration actually used in `cubicshell.py`. That code does `Θ(log b)` full-precision divisions. The sentence is withdrawn and replaced by the bounds below.

Notation: `b` is the bit length of the rank. `M(b)` and `D(b)` are the bit costs of multiplying and of dividing `b`-bit integers.

## 1. Arithmetic operation counts (PROVEN, by inspection of the formulas)

| | rank (cell → id) | unrank (id → cell) |
|---|---|---|
| Model C | `O(1)` additions, comparisons and multiplications; no root | 1 integer cube root, at most 1 integer square root, `O(1)` other operations |
| Model D | as for C | as for C |
| Model H5 | `t = ⌈log_125(n+1)⌉` table steps, each `O(1)` operations on integers below `5^t` | the same |

## 2. Bit complexity of the reference code (PROVEN)

**Lemma (iteration count of `icbrt`).** For `n ≥ 2` with `L` bits, `cubicshell.icbrt` performs at most `log₂ L + O(1)` iterations.

*Proof.*

1. **Start and Newton map.** Let `c = n^{1/3}` and `r = ⌊c⌋`. The start is `x₀ = 2^{⌈L/3⌉}`, and since `2^{(L−1)/3} ≤ c`, we have `x₀ ≤ 2c`. Write `f(x) = (2x + n/x²)/3`.
2. **Error contraction.** Then `f(x) − c = (x − c)²(2x + c)/(3x²) ≥ 0`. With relative error `e = x/c − 1`, the next error is `e' = e²(3 + 2e)/(3(1 + e)²) ≤ e²`. In particular `e₀ ≤ 1` gives `e₁ ≤ 5/12`.
3. **The integer step.** The code computes `y = ⌊(2x + ⌊n/x²⌋)/3⌋ = ⌊f(x)⌋`, since `2x` is an integer. Because `f` is increasing on `[c, ∞)` and `f(x) ≥ c`, every integer iterate is at least `r` and at most the corresponding real iterate.
4. **Termination.** While `x > r`, we have `x > c`, so `y ≤ f(x) < x`; the iterates strictly decrease. The loop stops at the first `y ≥ x`, which happens exactly when `x = r`.
5. **Count.** The real error satisfies `e_j ≤ (5/12)^{2^{j−1}}`. Once `e_j·c < 1`, `x_j ≤ r + 1`, and at most two more iterations follow. Since `c < 2^{L/3}`, this takes `j ≤ log₂ L + O(1)`. ∎

**[OBSERVATION]** Measured iteration counts are exactly `log₂ L` for `L` = 64, 256, …, 262,144: 6, 8, 10, 12, 14, 16 and 18 iterations respectively.

Each iteration costs one squaring, one division of an `L`-bit number by a `2L/3`-bit number, and linear work. So:

- **C and D, unrank:** `O(D(b)·log b + Q(b))` bit operations, where `Q(b)` is the cost of `math.isqrt`. With schoolbook arithmetic this is `O(b² log b)`.
- **C and D, rank:** `O(M(b))`, since only a constant number of multiplications and additions of `O(b)`-bit integers are needed. This part of file 20's statement stands.
- **H5:** `O(t)` steps, each touching integers of `O(b)` bits, so `O(b²)` with schoolbook arithmetic and no roots.

## 3. Asymptotically fast bounds (CITED, not re-verified here)

Root extraction to `b` bits in `O(M(b))` bit operations, by Newton iteration with precision doubling, is standard in the computer-arithmetic literature. The usual references are:

- R. P. Brent, *Fast multiple-precision evaluation of elementary functions*, J. ACM 23 (1976) 242–251, doi:10.1145/321941.321944;
- R. P. Brent and P. Zimmermann, *Modern Computer Arithmetic*, Cambridge University Press (2010), arXiv:1004.4710.

**I could not open either text in this session**, because the network policy blocked those hosts. I have **not** checked the exact theorem statements, the division model, or how the integer-floor correction is handled. Until someone does, the safe statement is the reviewer's:

> unrank costs `O(R_cuberoot(b) + R_sqrt(b) + M(b))`

and `R_cuberoot(b) = O(D(b) log b)` for the code as written.

**[Recommendation]** If an `O(M(b))` unrank is wanted, replace `icbrt` by a precision-doubling root (in the style of `math.isqrt`) and prove its bound. This is engineering, not needed for correctness.

## 4. Practical runtime (OBSERVATION)

CPython 3.13, one run each, on a random rank with the stated number of decimal digits:

| digits | `c_unrank` | `c_rank` | `icbrt` alone | `math.isqrt` alone |
|---:|---:|---:|---:|---:|
| 1,000 | 0.0001 s | 0.00001 s | 0.0001 s | < 0.0001 s |
| 10,000 | 0.0040 s | 0.0003 s | 0.0034 s | 0.0004 s |
| 100,000 | 0.166 s | 0.011 s | 0.142 s | 0.016 s |
| 300,000 | 1.07 s | 0.057 s | 0.92 s | 0.072 s |

- Unrank is dominated by `icbrt`.
- For a 22-digit public identifier (about 73 bits), all costs are negligible.
- Asymptotics matter only far outside the intended use.

## 5. Lower bounds and optimality (OPEN)

The only proven lower bound is the trivial `Ω(b)`, from reading the input or writing the output. No claim of optimality is made for any model. File 20 does not claim optimality; this restates the earlier correction to F-19.
