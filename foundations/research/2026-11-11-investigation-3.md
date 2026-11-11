# Investigation 3: review integration, corrections, and a hierarchical radix-5 numbering (OP-9)

**Date:** 2026-11-11
**Author:** Claude (research session)
**Branch:** `foundations-research` only. No production path (`calc/`, `apps/`, `js/`, `index.html`, `xyz2cube.py`) was modified, and production files on this branch are byte-identical to `origin/main`.

**Reproduce:**

```
python3 -I foundations/experiments/run_all.py
```

The bounded generator search is separate, because it is slow: `python3 -I foundations/experiments/exp_i3_radix5_grammar.py`.

**Input:** the independent review `research/2026-11-10-review-of-investigation-2.md` and its test `experiments/exp_review_i2_independent.py`, at commit `53a2fb8`.

## Summary

| ID | Result | Status | Where |
|---|---|---|---|
| I3-01 | The reviewer's test passes in a real checkout: independent C/D tables equal `cubicshell.py` at all 9,261 cells of the radius-10 cube | **OBSERVATION** (confirms review) | `exp_review_i2_independent.py` |
| I3-02 | Extended check: third independent spiral, exhaustive radius 30 (226,981 cells), break locations, boundaries, ranks up to `10^1000`, `icbrt` to 9,000 bits | **OBSERVATION** | `exp_i3_extended_verification.py` |
| I3-03 | **Correction to I2-12.** `calc/mobileGPS.html` uses a 3-argument `max`; the I2-12 collision pair belongs to the 4-argument legacy formula, not to this page. No encoder in the repository is injective | **OBSERVATION**, with structure **PROVEN** | §2, `exp_i3_encoder_audit.py` |
| I3-04 | **Correction to file 20.** Unrank "`O(M(b))` bit operations" is withdrawn. The proven bound for the code as written is `O(D(b) log b)`; `icbrt` uses `log₂ b + O(1)` Newton steps | **PROVEN** (correction) | `mathematics/22-…` |
| I3-05 | Novelty: no prior statement found of the one-break shell traversal, the prefix parity law, the double-shell construction or the radix ≡ 1 (mod 4) condition. No originality is claimed | literature note | §4 |
| I3-06 | Precise definitions of origin-first, centred prefixes, strong hierarchy H4 and gates. Prefix cubes do not imply hierarchy: Model D splits an aligned 25-block into 613 intervals | definitions; **OBSERVATION** | `mathematics/30-…` §1 |
| I3-07 | **Obstruction:** for every odd radix, a centre-first child order with opposite-corner (Peano-type) pieces is impossible | **PROVEN (new)** | `30-…` Thm 9 |
| I3-08 | Any closed grammar of corner-gated pieces yields a face-continuous, origin-first numbering of Z³ in which every aligned block is one aligned rank interval | **PROVEN (new)** | `30-…` Thm 10 |
| I3-09 | **OP-9, existence: Model H5.** The single-type grammar {edge-adjacent-corner pieces} is closed, giving a face-continuous, origin-first, strongly hierarchical radix-5 numbering with digit-by-digit rank/unrank and no roots | **PROVEN, computer-assisted** | `30-…` Thm 11, `radix5.py` |
| I3-10 | H5 satisfies `‖E(n) − E(m)‖_∞ ≤ 10·|n − m|^{1/3}`; C and D satisfy no such bound | **PROVEN (new)** | `30-…` Thm 12 |
| I3-11 | Exhaustive check of H5 on B₃ (1,953,125 cells) and locality measurements against C and D | **OBSERVATION** | `exp_i3_model_h5.py` |
| I3-12 | H5 cannot address the whole Earth within 22 decimal digits; C and D can | **PROVEN** (arithmetic) | §5 |

"New" means new in this notebook. It is not a priority claim (§4).

## 1. Closing Investigation 2: the independent test (Phase 1.1)

`python3 -I experiments/exp_review_i2_independent.py` output:

```
C PASS: radius 10, 9261 rank+unrank comparisons, steps {(0, 0, 1): 9250, (0, 1, 1): 10}
D PASS: radius 10, 9261 rank+unrank comparisons, steps {(0, 0, 1): 9260}
```

This settles the review's open reproducibility point: the comparison against the exact repository code now passes in a real checkout.

`experiments/exp_i3_extended_verification.py` adds the following. All checks pass.

- **A third spiral.** A left-turning turtle walk, built without the loops of either earlier implementation. It equals the reference spiral on 3,969 cells.
- **Exhaustive radius 30.** C and D are rebuilt from the phase tables of files 20 and 21 on top of that walk and compared with `cubicshell.py` in both directions on all 226,981 cells of the radius-30 cube. Every cell appears once, and rank and unrank are inverse at every rank.
- **Specification details for Model C.**
  - The single edge-diagonal step of shell `k` is exactly the cap-to-first-ring step, at rank `(2k−1)³ + (2k+1)² − 1`.
  - Every shell runs from axis to axis.
  - Every shell-to-shell step is a face step.
- **Specification details for Model D.**
  - Every step is a face step.
  - The radius-`r` cube is a prefix exactly for even `r ≤ 30`.
  - Blocks start at rank `(4j−3)³`, on the axis.
- **Large integers.**
  - Boundary ranks at shells `k ≈ 10^20 … 10^333`.
  - 1,200 random ranks per model with up to 1,000 digits, far beyond float range.
  - 500 random cells with coordinates up to `10^300`.
  - The step type across each tested boundary matches the specification.
- **`icbrt`.** It agrees with an independent bisection cube root at perfect cubes, their neighbours and random inputs up to 9,000 bits.

## 2. Correction to I2-12: which encoders are injective (Phase 1.2)

**What Investigation 2 said** (preserved in `research/2026-11-10-investigation-2.md`, observation 2): in `calc/mobileGPS.html`, cells `(−s,−s)` and `(−s+1,−s)` collide for every `s ≥ 2`.

**What is true.** `calc/mobileGPS.html` declares `function max(v1, v2, v3)` and calls it as `max(my_y + 1, my_z + 1, -my_y, -my_z)`. JavaScript drops the fourth argument.

`exp_i3_encoder_audit.py` slices the page's own source bytes, from `function coord_round` to the padded string, runs them in Node on 28,800 cells, and confirms they compute `max(y+1, z+1, −y)`. The I2-12 pair is refuted for the page: `(−2,−2)` gives 14 and `(−1,−2)` gives 3, as the reviewer reported.

**Why I2-12 went wrong.** It analysed a re-typed formula with a four-argument maximum, not the executable bytes. This experiment avoids re-typing for exactly that reason.

**The same defect was recorded earlier elsewhere.** The three-argument `max` was reported as defect B3, with a Sydney example, in `docs/research/2026-11-08-preservation-first-audit.md` on branch `claude/serene-archimedes-2mz259` (commit `7832ed9`). That branch was not merged, and Investigation 2 read only `foundations/`.

**Structure of the page's map** (PROVEN; checked on `[−60,59]²`):

- Write `n = max(y+1, z+1, −y, −z)`. The page's square number `n' = max(y+1, z+1, −y)` differs from `n` exactly on **bottom-row interior** cells: `z = −n` and `−n < y < n−1`.
- On those cells the page computes:
  - `cube_p = 4m² − m + 2 − n` for `y < 0`, with `m = −y`;
  - `cube_p = 4m² − 5m + 3 + n` for `y ≥ 0`, with `m = y + 1`.
- On every other cell it agrees with the four-argument formula, including the reversed top row.
- Because `n'` always equals one of `y+1`, `z+1`, `−y`, the page's bottom-row branch is **dead code**.

**Injectivity of each encoder.**

| Encoder | Injective? | Evidence |
|---|---|---|
| **`calc/mobileGPS.html`** (this repository; the same arithmetic appears in the legacy site's `calc/mobileGPS.html` and `calc/6gps2cube.html`) | **No** | Reviewer's witness reproduced from the page's bytes: `(0,−1,−1)` and `(0,0,−2)` both give `0000000000000000000004`. Infinite family: `(0,−n)` gets `cube_p = n+2`, which another cell of the same layer also gets (checked for `n = 2…59`). On `[−60,59]²`: 12,656 distinct `cube_p` among 14,400 cells and 127 non-positive values, exactly the reviewer's counts. New: with `cube_p ≤ 0` in layer 0 the page prints strings such as `0000000000000000000-10` (55 such strings in the window); for `x ≠ 0` the code falls into the preceding layer's range |
| **Four-argument legacy formula** (legacy `website.html` Python and `calc/3xyz2cube.html` after 2021-02-06; not in this repository) | **No** | Exactly the I2-12 pairs `(−s,−s), (−s+1,−s)` collide at `4s² − 2s + 2`: 59 pairs in the window. **I2-12 was a correct statement about this formula, attributed to the wrong file** |
| **`xyz2cube.py`** (repository root, the real module) | **No** | 10,800 distinct codes among 14,400 cells; `(y,z) = (−1,0)` and `(−1,−1)` collide. It turns the inventor's Pi example into `3141592653589871375760`, not the published `…793238462` |
| **`index.html` `formatCubeCode`** (exact bytes run in Node) | **No** | `(0,0,0)`, `(0,0,1000)` and `(0,0,−1000)` all give `6378137000000063781370`. London's ECEF point and its `z`-mirror give the same code. The decoder reads 7/7/8-digit fields the encoder never writes |

**No encoder present in the repository or the legacy site is injective.** Which convention is authoritative remains an owner decision (OP-3). No production file was changed, and any fix would change public identifiers.

## 3. Bit complexity (Phase 1.3)

See `mathematics/22-rank-unrank-complexity.md`. In short:

- **Operation counts are unchanged and correct.** C and D unrank need one cube root and one square root; rank needs no root; H5 needs no root.
- **Bit cost of the actual `icbrt`.**
  - **[PROVEN]** At most `log₂ L + O(1)` Newton iterations, each with one full-precision division, so `O(D(b) log b)`.
  - **[OBSERVATION]** Exactly `log₂ L` iterations were measured for 64 to 262,144 bits.
- **The cited bound.** The `O(M(b))` bound for precision-doubling root algorithms is cited (Brent 1976; Brent–Zimmermann 2010) but **not re-verified**: the network policy blocked the full texts.
- **Practical cost.** For a 22-digit identifier the cost is negligible. At 300,000 digits, C unrank takes 1.07 s and rank 0.057 s.
- **Optimality.** No lower bound beyond `Ω(b)`, and no optimality claim.

## 4. Novelty and literature (Phase 1.4)

**Searches made.** The searches covered:

- face-continuous and odd-radix Peano/Hilbert curves;
- centre-first odd-radix curves;
- Hamiltonian paths on cube surfaces and grid graphs with parity arguments;
- spiral and shell enumerations of Z³.

**What was found:**

- odd-radix Peano curves (the Cavender thesis states the base-`b` Peano construction for every odd `b`);
- Haverkort's inventories of 3-D Hilbert curves, already in the bibliography;
- a paper on pandimensional space-filling recurrences that places the **midpoint** of a serpentine curve at the centre sub-cell (arXiv:1402.1807). This is related to, but not the same as, starting at the centre;
- counts of Hamiltonian paths in `n×n×n` grids (OEIS A193346).

**What was not found:** a prior statement of the one-break Chebyshev-shell traversal, the prefix-cube parity law, the double-shell construction, the radix ≡ 1 (mod 4) condition, or Theorems 9–11.

**What this does and does not establish.** These are search results, not a literature review. The full texts of most hits could not be opened, because arxiv.org and the university hosts were blocked by this session's network policy. **No originality or priority is claimed.**

- **[Interpretation]** The parity arguments are elementary and probably folklore in the Hamiltonian-path literature.
- **[Interpretation]** The w-flip obstruction (Theorem 9) resembles classical one-way grid orientations.

The bibliography lists only sources whose existence and topic I could confirm, and says what each does **not** contain.

## 5. OP-9: hierarchical radix-5 numbering (Phase 2)

Full statements and proofs are in `mathematics/30-radix5-hierarchical-face-continuous.md`.

**Formalisation (2.1).** Properties H1–H6 are defined there:

- H1: origin first;
- H2: face continuity;
- H3: centred prefix cubes;
- H4: every aligned block of side `5^s` is one rank interval aligned to `125^s`;
- H4(m): bounded fragmentation;
- H5: corner gates;
- H6: effective coding.

H3 is **not** hierarchy. **[OBSERVATION]** Model D satisfies H1–H3, yet splits the aligned 5-block centred at `(5,0,0)` into 23 intervals and the aligned 25-block centred at `(25,0,0)` into 613. Under H3 and H4 the structure is forced: a centre-first Hamiltonian order of the 125 children, with gates.

**The 5×5×5 problem (2.2).**

- Pieces are typed by how the exit corner differs from the entry corner: O (opposite), F (face-diagonal), E (edge-adjacent).
- Lemma 8 (w-flip) turns the gate rule into a parity invariant.
- **[PROVEN] Theorem 9.** With O pieces only, for any odd radix, the admissible moves form a fixed one-way digraph with a source corner, so no centre-first order exists. This explains why a 5,000,053-node search found nothing, and why the classical Peano construction (which **was** found, in 128 nodes) cannot be centred.
- **[PROVEN]** Bipartite colour parity is respected throughout, because all corners and the centre of an odd cube have the majority colour.

**Recursive composition (2.3).**

- **[PROVEN] Theorem 10.** Any closed grammar composes to every level.
- **[PROVEN] Theorem 11.** A bounded search found a closed grammar with a single type, E. It has two 125-step generators, listed in file 30 and re-verified whenever `radix5.py` is imported.
- **[OBSERVATION]** Exhaustive check on B₃:
  - 1,953,125 cells, each once;
  - all steps are face steps;
  - B₀, B₁ and B₂ are prefixes;
  - every aligned 5- and 25-block is one aligned interval;
  - rank inverts unrank;
  - 4,000 random round trips up to `125^40`.
- **[OBSERVATION]** The grammar {F} is also closed. Searches are bounded, so "not found" results are not impossibility claims.

**Outcome against your four options:** outcome **A**, a constructive theorem valid at every level, for corner-gated designs, together with outcome **C**, an obstruction, for Peano-type gates. Non-corner gates are not studied.

## 6. Comparison of candidates (2.4)

Measurements were taken on the same 1,953,125 cells, the radius-62 cube. Each of C, D and H5 enumerates exactly this cube as its first `125³` ranks. Chebyshev distance is used throughout.

| | A | A* | C | D | **H5** | 3-D Hilbert (octree) | Peano radix 3 |
|---|---|---|---|---|---|---|---|
| Consecutive steps | per review; Investigation 1 archive not examined here | 26-adjacent, `2k−1` edge-diagonal steps per shell (review) | face, plus one √2 step per shell | all face | all face | face-continuous variants exist (Haverkort) | all face |
| Shell-monotone | yes (per review) | yes | yes | double shells | no | no | no |
| Origin-centred prefix cubes | — | — | every radius | every even radius | radii `(5^t − 1)/2` | none (corner-anchored) | none (corner-anchored) |
| Strong hierarchy H4 | no | no | no (613 pieces) | no (613 pieces) | **yes**, radix 5, centred | yes, radix 2, corner | yes, radix 3, corner |
| Forward Hölder `‖Δp‖³/Δn` | — | — | unbounded; 7,448 measured | unbounded; 7,448 measured | **≤ 1000 proven**; 45.6 measured | bounded (known) | bounded (known) |
| Face-neighbour rank gap, median / max | — | — | 289 / 181,563 | 317 / 351,509 | **7** / 1,368,887 | — | — |
| Face-neighbour pairs with gap above 1% of the cube | — | — | 24.6% | 13.8% | **2.0%** | — | — |
| Rank / unrank | closed form | closed form | closed form, 1 cube root + 1 square root | closed form, 1 cube root + 1 square root | digit walk, `O(t)` table steps, no roots | digit walk | digit walk |
| Implementation | — | — | about 60 lines | about 70 lines | about 150 lines plus two 124-move tables | standard | standard |

**[Interpretation]** Reading the table:

- **Forward locality.** H5 is far better than C and D, both provably and as measured. H5 gives neighbours in rank order neighbours in space; C and D sweep long rings.
- **Backward locality.** Most face-adjacent cells have very close H5 ranks (median 7), but the worst pair is worse than for C or D. That pair lies across the boundary between the centre child and an outer child at the top level. **No bijection has bounded two-sided locality**, and small consecutive steps (H2) say nothing about this direction.
- **Geographical use.** A hierarchical code lets a prefix name a region (a `5^s`-block). C and D cannot do this. But H5 orders by nested centred blocks, so its digit structure is tied to the ECEF origin, the Earth's centre.
- **Identifier capacity.** **[PROVEN, arithmetic]**
  - B₁₀ has radius 4,882,812 m, which is less than the Earth's radius, so surface cells need B₁₁ and ranks up to `125^11 ≈ 1.16 × 10^23`.
  - 22 decimal digits cover only `10^22 / 125^10 ≈ 10.7` of B₁₁'s 125 level-10 children.
  - **So H5 cannot number the whole Earth within 22 digits.** C and D can: the radius-6,378,137 cube has `2.08 × 10^21` cells.
  - None of C, D or H5 is compatible with the historical numbering.

## 7. Phase 3

Your message stopped at "Our mathematical research is separate from the existing public CUBIC POSTCODE numbering convention". **Phase 3 has not been started.** Its instructions are needed before I do any work on it.

Meanwhile, §2 and §6 already record two engineering facts:

- no repository encoder is injective;
- H5 does not fit the 22-digit budget for the Earth.

## Changelog

- 2026-11-11, added:
  - `mathematics/22-rank-unrank-complexity.md`;
  - `mathematics/30-radix5-hierarchical-face-continuous.md`;
  - `experiments/exp_i3_extended_verification.py`, `exp_i3_encoder_audit.py`, `exp_i3_radix5_generators.py`, `exp_i3_radix5_grammar.py`, `exp_i3_model_h5.py`, `radix5.py`;
  - this file.
- Appended dated sections to `README.md`, `research/2026-11-10-investigation-2.md` (correction notice), `research/findings-register.md`, `research/open-problems.md` and `research/bibliography.md`.
- Added the reviewer's test and the new experiments to `run_all.py`.
- No earlier text was altered.
