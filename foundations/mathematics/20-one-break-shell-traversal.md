# OP-1 resolved: the minimum number of non-face transitions is exactly one

**Date:** 2026-11-10 (Investigation 2)
**Status:** Theorems 1–4 **PROVEN (new)**. Finite checks are corroboration only.
**Reproduce:** `python3 -I experiments/exp_model_c.py`, `python3 -I experiments/exp_shell_exact.py`
**Reference code:** `experiments/cubicshell.py` (`c_rank`, `c_unrank`)

## Conventions

Cell-centred integer grid `Z^3`, origin `(0,0,0)`. Chebyshev shell `S_k = {max(|x|,|y|,|z|) = k}`, `|S_k| = 24k²+2` for `k >= 1`. A step between consecutive cells is a **face step** (one coordinate changes by 1), an **edge-diagonal step** (two coordinates change by 1, length √2), a **corner-diagonal step** (three coordinates change by 1), or a longer jump. Ranks are zero-based. The **colour** of a cell is `(x+y+z) mod 2`.

## Theorem 1 (parity law for steps)

In every ordering of `S_k`, `k >= 1`, at least one step joins two cells of the same colour. In particular:

1. at least one step is not a face step (the known 6-adjacency obstruction);
2. corner-diagonal steps cannot repair it: `S_k` has no traversal using only face steps and corner-diagonal steps.

*Proof.* `Σ (-1)^(x+y+z)` over the cube `[-r,r]^3` equals `(Σ_{x=-r}^{r} (-1)^x)^3 = (-1)^r`, so over `S_k` it equals `(-1)^k - (-1)^(k-1) = 2(-1)^k`. The colour classes differ by 2 and the majority colour is `k mod 2`. If every step changed colour the ordering would alternate and the classes would differ by at most 1. Face steps and corner-diagonal steps both change colour. ∎

Item 2 is new relative to the handoff: adding the eight corner-diagonal directions to the six face directions leaves the shell graph bipartite, so 14-direction continuity is as impossible as 6-direction continuity.

## Theorem 2 (structure of every optimal traversal)

If an ordering of `S_k` has exactly one non-face step, then that step joins two cells of colour `k mod 2`, the first and last cells of the shell also have colour `k mod 2`, and the two face-continuous pieces each have odd length.

*Proof.* By Theorem 1 the single non-face step preserves colour. It cuts the ordering into two alternating runs. An alternating run has surplus `+1`, `0` or `-1` for the majority colour, and the two surpluses must add up to 2. So both are `+1`: both runs are odd and both start and end in the majority colour. ∎

Consequence: when the single break is a king step, it is necessarily an **edge-diagonal** step.

## Theorem 3 (OP-1: the minimum is 1, for every `k >= 1`)

For every `k >= 1` there is an ordering of `S_k` with exactly one non-face step, and that step is an edge-diagonal step. Equivalently, `S_k` is covered by two vertex-disjoint face-adjacent paths and not by one. The minimum number of non-face transitions in a complete traversal of `S_k` is exactly 1.

### Construction (Model C shell)

Let `σ` be the origin-first square spiral with `σ(0) = (0,0)`, whose ring `r >= 1` occupies ranks `(2r-1)² .. (2r+1)²-1`, starts at `(r,-r+1)`, runs `+y, -x, -y, +x`, and ends at the corner `(r,-r)`. Write `ρ_k(t)`, `0 <= t < 8k`, for the cells of ring `k` in that order, and `m = (2k+1)²`. In local coordinates `(x,y,w)` the shell is visited in three phases:

| Phase | Local ranks `q` | Cell |
|---|---|---|
| start cap | `0 <= q < m` | `(σ(q), k)` |
| rings `i = 0..2k-2` | `q = m + 8k·i + t` | `(ρ_k(t), k-1-i)` for even `i`, `(ρ_k(8k-1-t), k-1-i)` for odd `i` |
| end cap | `q = m + 8k(2k-1) + u`, `0 <= u < m` | `(σ(m-1-u), -k)` |

*Proof.* The three phases partition `S_k` into the cap `w = k`, the `2k-1` rings `|w| < k`, and the cap `w = -k`; the counts add to `2m + 8k(2k-1) = 24k²+2`. Consecutive spiral cells are face-adjacent, as are consecutive ring cells. The junctions are:

- cap to first ring: `(k,-k,k) -> (k,-k+1,k-1)`, the single edge-diagonal step;
- even ring to odd ring: both at `(k,-k)`, a vertical face step;
- odd ring to even ring: both at `(k,-k+1)`, a vertical face step;
- last ring to end cap: the number of rings is odd, so the last ring is traversed forwards and ends at `(k,-k,-k+1)`, directly above `(σ(m-1), -k) = (k,-k,-k)`.

So there is exactly one non-face step. Theorem 1 gives the lower bound. ∎

Every horizontal slice of the shell is visited consecutively, in planar-spiral order or in its exact reverse. The start cap satisfies cap-centre-first and the end cap satisfies cap-centre-last, which is as much as the cap-centre theorem permits.

## Theorem 4 (Model C: a global enumeration with one √2 step per shell)

Define `C: N -> Z^3` by `C(0) = (0,0,0)` and, for `(2k-1)³ <= n < (2k+1)³`, by the Model C shell with `z = w` for odd `k` and `z = -w` for even `k`. Then:

1. `C` is a bijection and is shell-monotone: its first `(2k+1)³` values are exactly the cube of radius `k`.
2. Every step between consecutive shells is a face step along the `z` axis.
3. Inside each shell there is exactly one non-face step, an edge-diagonal step, at local rank `(2k+1)²`. Every step of `C` is therefore 18-adjacent, of Euclidean length at most √2.
4. **Optimality.** Every shell-monotone enumeration has at least `K` non-face steps among its first `(2K+1)³` terms. `C` has exactly `K`.

*Proof.* Shell `k` ends at `w = -k` on the axis and shell `k+1` starts at `w' = k+1` with the opposite sign convention, so the two cells are `(0,0,∓k)` and `(0,0,∓(k+1))`. The origin is followed by `(0,0,1)`. Items 1 and 3 are Theorem 3; item 4 is Theorem 1 applied to each shell. ∎

Comparison, using the count reported in the independent review for Model A\* (`2k-1` non-face internal steps per shell; I have not seen its source): up to radius `K` that is `K²` non-face steps against `K` for Model C. At the 22-digit radius `K = 10,772,172` this is about `1.16 × 10^14` against `1.08 × 10^7`.

## Rank and unrank

```
c_unrank(n):                          c_rank(x, y, z):
  if n == 0: return (0,0,0)             k = max(|x|,|y|,|z|)
  k = (icbrt(n) + 1) div 2              if k == 0: return 0
  q = n - (2k-1)^3                      w = z if k odd else -z
  (x,y,w) = shell cell q                return (2k-1)^3 + local rank of (x,y,w)
  return (x, y, w if k odd else -w)
```

Complexity, with `b` the bit length of the identifier and `M(b)` the cost of multiplying two `b`-bit integers:

- **rank** (cell to identifier) uses no root extraction at all: `O(1)` additions, comparisons and multiplications, hence `O(M(b))` bit operations;
- **unrank** uses one integer cube root of `n`, at most one integer square root of a number below `(2k+1)²`, and `O(1)` further operations; with integer Newton iteration this is `O(M(b))` bit operations.

No lower bound beyond the trivial `Ω(b)` is claimed (see the F-19 correction).

## Evidence

- `exp_model_c.py`: bijection onto the radius-24 cube (117,649 cells), shell-monotonicity, exactly one edge-diagonal step per shell at the predicted rank, face steps everywhere else, slice-wise spiral order, and 20,000 random round trips on ranks up to `10^60`.
- `exp_shell_exact.py`: exhaustive search (no parity pruning) shows `S_1` has no face-adjacent Hamiltonian path, and `S_1 \ {L}` has one exactly for the 14 majority-colour cells `L`. With OR-tools installed, CP-SAT proves for `k = 1,2,3` that one path is infeasible and two paths are feasible.

## Limits and what is not claimed

- Model C is a research candidate. It is **not** compatible with any existing identifier and nothing in production was changed.
- The break position inside a shell is not unique. A variant with the break as the last step of each shell (a single leftover cell) would be optimal for every prefix, not only at shell boundaries; I have not written it out.
- The number of optimal traversals of `S_k` and the set of admissible endpoint pairs are open (OP-10).
