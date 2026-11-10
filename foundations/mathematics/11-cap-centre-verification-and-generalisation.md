# Cap-centre obstruction: independent verification, sharpness and generalisation

**Date:** 2026-11-10 (Investigation 2)
**Status:** the theorem of `10-cap-centre-obstruction.md` is **independently verified (PROVEN)**; Theorems G1–G3 below are **PROVEN (new)**.
**Reproduce:** `python3 -I experiments/exp_cap_centre_general.py`

File 10 is left unchanged as the historical record.

## 1. Verification of the original proof

Conventions as in file 10: `S_k = {max(|x|,|y|,|z|) = k}`, 26-adjacency means Chebyshev distance 1, and "cap-centre-first" means `(0,0,±k)` precedes every other cell of its own cap.

The proof is correct. The single step that carries the weight is this: a 26-neighbour of `p+ = (0,0,k)` has the form `(a,b,k+c)` with `a,b,c ∈ {-1,0,1}`. For `c = +1` it lies outside the cube; for `c = 0` it lies on the cap; for `c = -1` its Chebyshev norm is `max(|a|,|b|,k-1) = k-1` because `k-1 >= 1 >= |a|,|b|`. That last equality is exactly where `k >= 2` is used.

Assumptions actually used, all of them necessary:

| Assumption | Where it is used | What happens without it |
|---|---|---|
| The ordering is restricted to one shell `S_k` (shell-monotonicity of the global enumeration) | the predecessor of `p+` must lie in `S_k` | open, see OP-11 |
| `k >= 2` | the layer below the cap centre is interior | false for `k = 1`, see §2 |
| cap-centre-first on **two** caps | two distinct cells are both forced to be first | one cap alone is harmless: Model C starts at a cap centre |
| every consecutive pair adjacent | the cap centre has a predecessor that is a neighbour | one long jump suffices, see G2 |

The corollary about global enumerations also holds: a shell-monotone enumeration visits `S_k` as a contiguous block, and the plane `z = ±k` meets `S_k` in a full cap whose first cell under an origin-first spiral is its centre.

One wording caution. The theorem does **not** need the planes to be horizontal or the two caps to be opposite. Any two of the six facet centres will do (G1).

## 2. Sharpness: `k = 1` is a real exception

For `k = 1` take the top cap in spiral order, then the ring `z = 0` in spiral-ring order, then the bottom cap in spiral order. This ordering has both cap centres first, is consistent with the planar spiral in every horizontal plane, and every consecutive pair is 26-adjacent (**PROVEN** by the explicit 26-cell list; checked in the experiment). So `k >= 2` cannot be weakened.

## 3. Theorem G1 (local-minimum principle)

Let `G` be any graph on a finite vertex set `V` and let `v_1, ..., v_N` be an ordering of `V`. Call `v_i` a **local minimum** if every `G`-neighbour of `v_i` comes later, and call the pair `(v_i, v_{i+1})` a **break** if it is not an edge of `G`. Then

```
breaks >= (local minima) - 1        and likewise        breaks >= (local maxima) - 1.
```

*Proof.* If `v_i` is a local minimum and `i > 1`, then `v_{i-1}` is earlier than `v_i`, hence not a neighbour, so `(v_{i-1}, v_i)` is a break. Distinct local minima give distinct breaks, and at most one local minimum has `i = 1`. Reverse the ordering for maxima. ∎

The cap-centre theorem is the case "two forced local minima, zero breaks allowed". G1 immediately gives these extensions (**PROVEN**):

1. **Any adjacency.** The statement holds for 6-, 18- and 26-adjacency, since a king-neighbourhood contains the other two.
2. **Any two facets.** For `k >= 2` each of the six facet centres `±k·e_i` has all its shell-neighbours inside its own facet. An ordering of `S_k` in which `m` facet centres are first in their facets has at least `m - 1` breaks.
3. **Any dimension.** In `Z^d`, `d >= 2`, `k >= 2`, the `2d` facet centres of the Chebyshev shell have the same property (checked for `d = 2,3,4`; the proof is the same one-line norm computation).

## 4. Theorem G2 (the forced jump has length at least `k`)

Let `k >= 1` and take any ordering of `S_k` with cap-centre-first on both caps. Then some consecutive pair is at Chebyshev distance **at least `k`**.

*Proof.* At most one cap centre is first in the shell; let `c = (0,0,k)` be the other (the lower case is symmetric) and `q` its predecessor. Cap-centre-first puts `q` outside the cap, so `q = (x,y,z)` with `z < k`. Either `z = -k`, at distance `2k` from `c`, or `|z| < k`, and then `max(|x|,|y|) = k`, at distance at least `k`. ∎

So the discontinuity is not a near miss: it grows linearly with the shell radius. For `k = 1` the bound is 1 and is met by §2.

## 5. Theorem G3 (the bound in G2 is attained)

The **plane-sequential ordering** of `S_k` (top cap in spiral order, rings `z = k-1, ..., -k+1` each in spiral-ring order, bottom cap in spiral order) is consistent with the origin-first planar spiral in every horizontal plane, and for `k >= 2` it has exactly one step that is not 26-adjacent, of Chebyshev length exactly `k`.

*Proof.* With the spiral convention of `experiments/cubicshell.py`, ring `r` starts at `(r,-r+1)` and ends at `(r,-r)`. Cap to ring: `(k,-k,k) -> (k,-k+1,k-1)`. Ring to ring: `(k,-k,z) -> (k,-k+1,z-1)`. Both are edge-diagonal steps. Last ring to bottom centre: `(k,-k,-k+1) -> (0,0,-k)`, Chebyshev length `k`. ∎

**Consequence for the C-02 trade-off.** Under shell-monotonicity and full planar-spiral consistency, the minimum number of non-26-adjacent steps per shell is exactly **1** for every `k >= 2`, and the minimum possible length of that step is exactly `k`. The trade-off is therefore completely quantified.

## 6. What remains uncertain

- I have **not** seen the Investigation 1 definitions of Model A or Model A\*. G3 is stated for the ordering defined here; I do not claim it equals Model A.
- Without shell-monotonicity the question is open (OP-11). One necessary condition follows from G1: each plane `z = c`, `c != 0`, must be entered for the first time from one of the nine cells `(a,b,c∓1)`, `|a|,|b| <= 1`, of an adjacent plane.
