# Face-continuity with one shell of slack: the prefix-cube parity law and Model D

**Date:** 2026-11-10 (Investigation 2)
**Status:** Theorems 5–7 **PROVEN (new)**. Finite checks are corroboration only.
**Reproduce:** `python3 -I experiments/exp_model_d.py`
**Reference code:** `experiments/cubicshell.py` (`d_rank`, `d_unrank`)

The 6-adjacency obstruction says a shell-monotone enumeration cannot be face-continuous. This note asks how much shell-monotonicity must be given up, and the answer is: exactly one shell.

## Theorem 5 (prefix-cube parity law)

Let `E: N -> Z^3` be an injective sequence in which every step is a face step. Say radius `r` is a **prefix radius** if the first `(2r+1)³` cells are exactly the cube `[-r,r]^3`. Then all prefix radii have the same parity. If `E(0)` is the origin, every prefix radius is even.

*Proof.* Let `r < r'` be prefix radii. The cells of rank `(2r+1)³ .. (2r'+1)³ - 1` are exactly the thick shell between the two cubes, visited by face steps, so colours alternate. The count `(2r'+1)³ - (2r+1)³` is even, so the two colours occur equally often. But the colour surplus of the thick shell is `(-1)^(r') - (-1)^r` (see Theorem 1 of file 20), which vanishes only when `r ≡ r' (mod 2)`. Radius 0 is a prefix radius when `E(0)` is the origin. ∎

## Theorem 6 (Model D: the parity law is the only obstruction)

There is a bijection `D: N -> Z^3` with `D(0) = (0,0,0)` in which **every** step is a face step and **every even radius** is a prefix radius: for all `j >= 0` the first `(4j+1)³` cells are exactly the cube of radius `2j`.

By Theorem 5 no face-continuous enumeration from the origin can have more prefix radii. So the set of prefix radii is characterised completely: the even numbers, all attainable at once.

### Construction

Block `j >= 1` is the double shell `S_a ∪ S_b` with `a = 2j-1`, `b = 2j`. Put `m = (2b+1)²` and `j0 = (2a-1)²`, and let `σ` be the spiral of file 20. In local coordinates `(x,y,w)` the block runs from `(0,0,a)` to `(0,0,-b)`:

| Phase | Cells | Order |
|---|---|---|
| T1 | columns `σ(c)`, `c < j0`, layers `w ∈ {a,b}` | ladder zigzag: column `c` is visited `a` then `b` for even `c`, `b` then `a` for odd `c` |
| T2 | `σ(j0..m-1)` on layer `w = b` | outward along the spiral |
| T3 | `σ(m-1..j0)` on layer `w = a` | inward along the spiral |
| M | layers `w = b-2, ..., -b+2`; each is the square annulus `σ(j0..m-1)` | forwards on even layers, backwards on odd layers |
| B | columns `σ(c)`, all `c < m`, layers `w ∈ {-b+1,-b}` | the reverse of the full ladder zigzag that starts at `(σ(0), -b)` |

Block `j` uses `z = w` for odd `j` and `z = -w` for even `j`.

*Proof.* Cells with `w ∈ {a,b}` or `w ∈ {-a,-b}` belong to the block for every `(x,y)` in the `(2b+1)`-square, and cells with `|w| <= b-2` belong to it exactly when `max(|x|,|y|) ∈ {a,b}`, that is for spiral ranks `j0..m-1`. So the phases partition the block, with `2m + (2b-3)(8a+8b) + 2m = 48b²-48b+28 = |S_a| + |S_b|` cells.

Steps inside a phase are spiral steps or vertical steps. The junctions:

- T1 ends at `(σ(j0-1), b)` because `j0-1` is even; T2 starts at `(σ(j0), b)`.
- T2 ends at `(σ(m-1), b)`; T3 starts directly below it.
- T3 ends at `(σ(j0), a) = (a,-a+1,a)`; the first annulus layer starts directly below it.
- An even layer ends at the corner `σ(m-1) = (b,-b)`, where the next (odd) layer starts; an odd layer ends at `σ(j0)`, where the next (even) layer starts.
- There are `2b-3` layers, an odd number, so the last layer ends at `(σ(m-1), -b+2)`. Phase B starts at `(σ(m-1), -b+1)` because `m-1` is even, and ends at `(σ(0), -b)`.
- Block `j` ends at `(0,0,∓b)` and block `j+1` starts at `(0,0,∓(b+1))`. The origin is followed by `(0,0,1)`.

Every step is a face step, and block `j` occupies ranks `(4j-3)³ .. (4j+1)³ - 1`. ∎

Rank and unrank have the same cost profile as Model C: rank needs no root; unrank needs one integer cube root and one integer square root.

## Theorem 7 (centred odd-radix towers)

Let `b >= 3` be odd and `r_t = (b^t - 1)/2`, the radius of the centred cube of side `b^t`. A face-continuous enumeration from the origin can have all the cubes of side `b^t`, `t >= 0`, as prefixes **if and only if `b ≡ 1 (mod 4)`**.

*Proof.* `r_{t+1} = b·r_t + (b-1)/2`. If `b ≡ 3 (mod 4)` then `r_1 = (b-1)/2` is odd and Theorem 5 forbids it. If `b ≡ 1 (mod 4)` every `r_t` is even by induction, and Model D has every even radius as a prefix radius. ∎

So for the centred odd-radix refinement of reviewed finding 8, radix **3 is excluded** for an origin-first face-continuous code, while radix **5** and radix **9** (every second level of radix 3) are admissible, and Model D realises them.

**Scope caution.** Theorem 7 is about origin-centred cubes being *prefixes* of a unit-cell enumeration. It says nothing against curves such as the 3-D Peano curve, where the central sub-block is the middle of its parent rather than a prefix, and it does not make Model D a hierarchical code: in Model D only the origin-centred cubes are contiguous, not every aligned block.

## Comparison of the candidates

| | shell-monotone | non-face steps up to radius `K` | longest step | prefix cubes |
|---|---|---|---|---|
| Model C | yes | `K` (the minimum) | √2 | every radius |
| Model D | no, double shells | 0 | 1 | every even radius (the maximum for 0 breaks) |

## Evidence

`exp_model_d.py`: bijection onto the radius-24 cube (117,649 cells), all steps face steps, block boundaries at `(4j+1)³`, and 20,000 random round trips on ranks up to `10^60`.

## What is not claimed

- No claim of compatibility with existing identifiers; nothing in production was changed.
- No claim that C or D has good *two-sided* locality. In any shell-ordered scheme two face-adjacent cells in neighbouring shells have ranks about `24k²` apart. Hierarchical curves (Hilbert, Peano) trade the origin-first property for bounded locality ratios; see the bibliography.
