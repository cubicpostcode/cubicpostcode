# Investigation 2 — dated findings

**Date:** 10 November 2026
**Author:** Claude (independent research session)
**Branch:** `foundations-research` only. No production path was modified.
**Reproduce everything:** `python3 -I foundations/experiments/run_all.py` (Python 3 standard library; the CP-SAT part of one experiment needs `pip install ortools` and is skipped without it).

## What I read, and what I could not read

I read every file under `foundations/` at commit `b1f6ec2` (eight files). The Investigation 1 archive is not on the branch, so I have **not** seen the definitions of Models A, A\* and B, the six original experiments, or findings F-12, F-13 and F-19 in their original wording. Statements below about those models rely only on what the independent review reports, and say so where it matters. To compare the new models with A and A\* exactly, I need the original archive.

## Summary of results

| ID | Result | Status | Where |
|---|---|---|---|
| I2-01 | Cap-centre obstruction theorem: proof checked line by line, assumptions isolated | **INDEPENDENTLY VERIFIED** | `mathematics/11-…` §1 |
| I2-02 | `k >= 2` is sharp: for `k = 1` a planar-consistent, 26-continuous ordering with both cap centres first exists | **PROVEN (new)** | `11-…` §2 |
| I2-03 | Local-minimum principle: breaks ≥ local minima − 1, for any graph; covers 6/18/26-adjacency, any two facets, any dimension | **PROVEN (new)** | `11-…` G1 |
| I2-04 | With both cap centres first, some step has Chebyshev length ≥ `k`; the plane-sequential ordering attains exactly one such step | **PROVEN (new)** | `11-…` G2, G3 |
| I2-05 | Every ordering of `S_k` has a colour-preserving step; face steps plus corner-diagonal steps can never traverse a shell | **PROVEN (new)** | `20-…` Thm 1 |
| I2-06 | **OP-1:** the minimum number of non-face transitions in a complete traversal of `S_k` is exactly 1 for every `k >= 1`; the break can be an edge-diagonal step and cannot be a corner-diagonal step | **PROVEN (new)** | `20-…` Thm 2, 3 |
| I2-07 | **Model C:** shell-monotone bijection `N ↔ Z^3`, one √2 step per shell, face steps elsewhere including between shells; root-free rank, unrank with one cube root and one square root | **PROVEN (new)** | `20-…` Thm 4 |
| I2-08 | Prefix-cube parity law: in a face-continuous enumeration from the origin only even-radius cubes can be prefixes | **PROVEN (new)** | `21-…` Thm 5 |
| I2-09 | **Model D:** fully face-continuous bijection `N ↔ Z^3` in which every even-radius cube is a prefix | **PROVEN (new)** | `21-…` Thm 6 |
| I2-10 | Centred odd-radix towers can be face-continuous prefixes iff radix ≡ 1 (mod 4): radix 3 excluded, radix 5 and 9 admissible | **PROVEN (new)** | `21-…` Thm 7 |
| I2-11 | Exact small cases: exhaustive search for `k = 1`; CP-SAT for `k = 1,2,3` | **OBSERVATION** (agrees with I2-06) | `exp_shell_exact.py` |
| I2-12 | The three encoders present in the repository disagree with one another, and two of them assign the same identifier to different cells | **OBSERVATION** (read-only) | below, `exp_production_readonly.py` |

"New" means new relative to this repository. The proofs are short and elementary, so parts may well be folklore. I found no prior statement of I2-06 to I2-10 in the sources listed in `bibliography.md`, but the search was brief and I make no priority claim.

## The answer to OP-1 in one paragraph

The parity argument already gave "at least one break". The matching construction is simple once the caps are traversed as spirals: spiral outwards over one cap from its centre to a corner, take one edge-diagonal step onto the first ring, run the `2k-1` rings alternately forwards and backwards so that each ring-to-ring move is a vertical face step, drop onto the corner of the opposite cap, and spiral inwards to its centre. The traversal ends on the axis, so the step to the next shell is a face step, and the next shell is the mirror image. This is Model C. It keeps the shell arithmetic `(2k-1)³` of the earlier models, so the cube-root shell inverse is unchanged.

Two questions in the handoff are answered directly:

- *Two 6-adjacent path covers joined across shells?* Yes: paths of `(2k+1)²` and `24k²+2-(2k+1)²` cells, joined to the neighbouring shells by face steps.
- *Direct rank/unrank?* Yes, closed form; see the pseudocode in `mathematics/20-…`.

## A result I did not expect: one shell of slack buys full continuity

The obstruction to face-continuity is purely a parity count, and the count cancels over two consecutive shells. Model D exploits this: it is a Hamiltonian path of the whole lattice by face steps, from the origin, that completes the cube of radius 2, then 4, then 6, and so on. Theorem 5 shows that no face-continuous enumeration can complete more cubes than that.

## Read-only observations on the existing encoders (OP-3)

These are observations about code on this branch, which is byte-identical to `main` for the files named (checked with `git diff` against `origin/main` on 2026-11-10). I changed none of it and I recommend no change without a separate decision, because any fix alters public identifiers.

1. **`calc/mobileGPS.html`** computes `code = slice · 441000000000000 + cube_p`, where `slice` zigzags over `x` and `cube_p` is a one-based spiral index over `(y,z)` on even-sided squares `[-s, s-1]²`. It is a slab-times-spiral product code, **not** a cubic-shell enumeration, so none of Models A, A\*, B, C, D can coincide with it.
2. In that formula, for every ring `s >= 2`, the cells `(y,z) = (-s,-s)` and `(-s+1,-s)` receive the same `cube_p = 4s²-2s+2`, and the value `4s²-4s+4` is never produced. The interior of the top row of each ring is also numbered in the opposite direction to the rest of the ring (ring 2 reads 5, 7, 6, 8). Verified on `[-60,59]²`: exactly 59 colliding pairs.
3. **`xyz2cube.py`** (repository root) uses `max(|y|,|z|)+1` for the ring where the HTML uses `max(y+1, z+1, -y, -z)`. On the same 14,400 cells it produces 10,800 distinct codes and agrees with the HTML formula on 7,140 cells.
4. **`index.html`** uses an unrelated formatter: it concatenates three scaled coordinates and keeps the first 22 characters. Run in Node, two points differing only in the sign of `z` give the same code, because the `z` digits fall beyond character 22. Its decoder reads the fields as 7, 7 and 8 digits, which does not match what the encoder writes.
5. `coord_round` returns `x-1` at exact negative integers (`-2.0 → -3`), and in JavaScript `parseInt(0.0000005)` is `5`, because the number is first printed in exponent notation.

I have treated the HTML calculator as the most likely "historical convention", but that is an inference. **Which of these three is the authoritative public convention is a question only the project owner can answer**, and OP-3 cannot progress without that answer and a set of published identifier examples.

## What remains uncertain

- Everything about Models A, A\*, B beyond the review's summary.
- Whether the break in Model C is best placed after the first cap (current choice, symmetric and simple) or as the last step of the shell (prefix-optimal).
- Two-sided locality of C and D has not been measured. Shell ordering forces rank gaps of order `k²` between face-adjacent cells of neighbouring shells in every such scheme.
- F-13 (Euclidean shells) and F-19 (lower bounds) were **not advanced** in this session. Nothing here should be read as bearing on them, other than the explicit operation counts for C and D.

## Recommended next steps

1. Upload the Investigation 1 archive so A, A\*, B can be compared with C and D on identical conventions.
2. Decide which existing encoder defines the historical identifiers (see observations above) and collect published examples.
3. Mathematics: OP-7 to OP-11 in `open-problems.md`. The most promising is OP-9, a hierarchical face-continuous curve built on centred radix-5 cells, which Theorem 7 shows is not excluded by parity.
4. A second, independent implementation of `c_rank`/`c_unrank` and `d_rank`/`d_unrank` from the tables in the proofs, in another language, as a cross-check of the specification rather than of this code.

## Changelog

- 2026-11-10: added `mathematics/11-…`, `20-…`, `21-…`; `experiments/cubicshell.py`, `exp_cap_centre_general.py`, `exp_shell_exact.py`, `exp_model_c.py`, `exp_model_d.py`, `exp_production_readonly.py`, `run_all.py`; `research/2026-11-10-investigation-2.md`, `research/bibliography.md`. Appended dated sections to `README.md`, `research/findings-register.md` and `research/open-problems.md`; no earlier text was altered.

---

## Correction notice (added 2026-11-11, Investigation 3)

The text above is preserved unchanged. **Observation 2 under "Read-only observations on the existing encoders" is wrong for `calc/mobileGPS.html` as written.**

- The page declares `function max(v1, v2, v3)` but calls it with four arguments. JavaScript ignores `-my_z`, so the page computes `max(y+1, z+1, -y)`.
- The pair `(-s,-s), (-s+1,-s)` does **not** collide in the page: for `s = 2` they give 14 and 3.
- The pair **does** collide in the four-argument formula of the legacy site (`website.html` Python, `calc/3xyz2cube.html`), which is what this section actually analysed.
- The page is still non-injective, in a different way. For example, `(0,-1,-1)` and `(0,0,-2)` both give `...0004`.
- I2-12's broader claim, that encoders disagree and that at least two are not injective, stands. In fact none of the encoders is injective.

The "ring 2" table printed by `exp_production_readonly.py` describes the four-argument formula, not the page.

Details and exact-bytes reproduction: `research/2026-11-11-investigation-3.md` §2 and `experiments/exp_i3_encoder_audit.py`.

The complexity sentence in `mathematics/20-…` ("`O(M(b))` bit operations" for unrank) is withdrawn. See `mathematics/22-rank-unrank-complexity.md`.
