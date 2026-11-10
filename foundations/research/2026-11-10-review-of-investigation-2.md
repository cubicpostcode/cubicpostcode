# Independent review of Investigation 2

**Date:** 2026-11-10  
**Reviewer:** ChatGPT (independent review session)  
**Target:** `foundations-research` branch, `cubicpostcode/cubicpostcode`  
**Handoff:** `research/2026-11-10-message-to-reviewer.md`  
**Scope:** Mathematics files 11, 20 and 21; independent C/D tests; comparison with the actual Investigation 1 archive; read-only production-code analysis; novelty and next research priority. **No production identifier is changed.**

## Executive verdict

**The central constructions and parity results survive adversarial review.** The cap-centre obstruction, the one-break Model C, the face-continuous double-shell Model D, and the centred odd-radix condition have valid-looking all-radius proofs. My independently generated complete radius-10 cube agrees at all 9,261 ranks with separately transcribed analytical rank/unrank formulas from the reference. The new in-repository regression test compares the independently constructed lists **directly** against `cubicshell.py` when run there.

**One material correction:** Investigation 2's exact collision pair for `calc/mobileGPS.html` is **wrong for the code as written**. The page calls a custom *three-argument* `max` with four arguments. JavaScript ignores the fourth, creating a different and more severe collision problem. Please amend Investigation 2's finding I2-12 and preserve the original claim as a dated, corrected observation.

**Qualification:** I tested the independent enumeration locally against a separately transcribed copy of the reference's analytic formulas, not the exact GitHub Python bytes (these were accessible for review through the GitHub connector, but not directly mounted for local execution). The committed standalone script imports the branch's real `cubicshell.py` at runtime and performs the requested exact source comparison; its in-repository execution remains a follow-up check. The finite tests corroborate, but do not replace, universal proofs.

## 1. Adversarial proof checks

### File 11: cap-centre verification and generalisation

- The original proof correctly distinguishes the `k >= 2` obstruction from the `k = 1` exception. For a facet centre `(0,0,k)`, every putative shell neighbour immediately below it has Chebyshev radius at most `k-1` when `k>=2`; if both caps require their centres first, both would be forced to be globally first.
- **G1:** The graph-theoretic local-minimum argument is valid. Every local minimum after position 1 forces a distinct incoming non-edge, giving `breaks >= minima-1`. The reversed-order argument gives the maxima analogue. Symmetry extends the cap statement to any selected facet centres and higher dimensions. The neighbourhood and within-shell hypotheses must remain explicit.
- **G2:** The predecessor of the second cap centre must lie outside its own cap. It is either on the opposite cap (distance `2k`) or on a side (at least one of `|x|,|y|` equals `k`), hence its Chebyshev distance is at least `k`. This is a sound lower bound.
- **G3:** In the plane-sequential construction, cap→ring and ring→ring transitions are 26-adjacent; the last ring→bottom-centre step has Chebyshev length exactly `k`. Thus the bound is attained for `k>=2`. This is an optimal **one non-26-adjacent** jump, not a claim of face-continuity.

**Disposition:** No counterexample to the stated theorems; keep `k=1` and the adjacency definition visible in the claims.

### File 20: one-break shell traversal and Model C

- **Theorem 1:** Each cube's chessboard imbalance is `(-1)^k`; subtracting consecutive cubes leaves shell imbalance `2(-1)^k`. Since a face step and a corner-diagonal step both flip colour, a single all-face/corner-diagonal traversal is impossible. Correct.
- **Theorem 2:** Removing the unique colour-preserving step produces two alternating runs. Their majority surpluses sum to 2, so each has surplus +1 and odd cardinality. The endpoints and the joining step therefore have majority colour. Correct.
- **Theorem 3 junction audit:** The starting cap terminates at `(k,-k,k)`; the first forward ring begins `(k,-k+1,k-1)`, giving the **single edge-diagonal**. A forward ring ends at `(k,-k)`; its reverse successor begins at the same `(x,y)` one layer below. A reverse ring ends at `(k,-k+1)`; its forward successor begins at the same `(x,y)` one layer below. Since `2k-1` is odd, the final ring is forward and ends at `(k,-k,-k+1)`; the final inward cap begins at `(k,-k,-k)`, a face step. Counts: `2(2k+1)^2 + (2k-1)8k = 24k²+2`. All junctions check out, including `k=1`.
- **Theorem 4:** Alternating the vertical sign between shells correctly connects consecutive axial endpoints by a face step. The parity lower bound and construction establish the optimum of one non-face step per shell **under shell-monotonicity**. No preservation of historical public IDs is implied.

**Disposition:** OP-1's asserted optimum is supported by its proof; Model C is structurally distinct from A* (see §3).

### File 21: prefix parity, Model D, odd-radix towers

- **Theorem 5:** The difference of two odd-cube cardinalities is even. A finite alternating face path of that even length contains equally many colours. Its actual thick-shell imbalance is `(-1)^{r'}-(-1)^r`, so any two prefix radii share parity. Starting at the origin requires even radii. The proof is sound.
- **Theorem 6 phase and junction audit:** The top T1 ladder visits `2j0` sites and ends at `(σ(j0-1),b)` because `j0-1` is even. T2 begins at the adjacent `σ(j0)` on `b`; T2→T3 is a unit vertical step; T3→M is vertical at `σ(j0)`. The `2b-3` middle annuli alternate orientation and the final (odd-numbered) annulus is forward, ending at `σ(m-1)`; reverse bottom ladder B begins directly one layer below. B ends at the axial centre `(0,0,-b)`. Adjacent double-shell blocks join axially after sign alternation. Cardinality `4m + (2b-3)(8a+8b) = 48b²-48b+28 = |S_a|+|S_b|`; the phase regions are disjoint and exhaust the block. This justifies the construction independently of finite experiments.
- **Theorem 7, particularly the “if” direction:** For odd radix `b ≡ 1 (mod 4)`, `r_t=(b^t-1)/2` is even for every `t`, so all requested centred cubes occur among Model D's even-radius prefixes. Conversely, when `b ≡ 3 (mod 4)`, already `r_1` is odd, excluded by Theorem 5. Thus the **existence** claim for origin-centred prefix cubes is sound. It does **not** construct a recursively hierarchical traversal in which each translated radix-`b` subblock is contiguous.

**Disposition:** Theorem 7 is correct in its carefully limited prefix sense. The stronger OP-9 hierarchical property is still open.

### Bit-complexity qualification (files 20 and 21)

The stated **number of arithmetic/root operations** is reasonable, but the text's unqualified conclusion that arbitrary-precision unrank costs `O(M(b))` bit operations “with integer Newton iteration” is not fully established by the supplied proof. Multiple full-precision Newton divisions can incur a logarithmic iteration factor. State the safe form `O(R_{\mathrm{cuberoot}}(b)+R_{\mathrm{sqrt}}(b)+M(b))` until a specific root algorithm, multiplication/division model and bit-complexity proof are supplied. This is not a counterexample to closed-form rank/unrank or the bijection theorems.

## 2. Independent implementations and tests

Added `experiments/exp_review_i2_independent.py`. It first constructs the spiral from four explicit perimeter loops, then builds C shells and D double-shells **from the published phase tables**, creates independent finite `unrank` arrays and `rank` dictionaries, and only then imports `cubicshell.py` to compare outputs. Run:

```bash
cd foundations
python3 -I experiments/exp_review_i2_independent.py
```

For the complete cube `[-10,10]^3`, `(2·10+1)^3 = 9,261`:

| Check | C | D |
|---|---:|---:|
| Unique points covering exact radius-10 cube | 9,261/9,261 | 9,261/9,261 |
| Finite independent array vs analytic `unrank` | 9,261 agree | 9,261 agree |
| Independent inverse dictionary vs analytic `rank` | 9,261 agree | 9,261 agree |
| Face transitions | 9,250 | 9,260 |
| Edge-diagonal transitions | 10 | 0 |
| Longer transitions | 0 | 0 |

I also ran 5,000 large-integer rank/unrank round trips **per model** using separately transcribed exact-integer formulas on identifiers up to `10^60`; all passed. These are additional internal consistency tests, not an independent universal proof.

**Reproducibility distinction:** the local tests were executed against the independent lists and analytical formula transcriptions. The committed test file supplies the exact repository-reference comparison and needs execution in a checkout or CI to certify that additional point.

## 3. Actual Investigation 1 archive: Model A* vs C

Recovered and extracted **`CubicPostcode-Foundations-Investigation1-2026-11-10.zip`** (archive tip `3686d49e3c8e52a3faa191c34b2aa1cd5c4d1a1f`). Inspected `experiments/cubic_postcode_math.py`, `model_astar_rank/unrank`, and `mathematics/03-model-A-slice-stacked-cubic-spiral.md`.

- **Yes, A* uses spiral caps and alternating shell direction.** For odd shells it travels bottom→top, with its final cap spiralling inward; for even shells top→bottom, with the final cap inward. Every intermediate ring is in forward spiral order.
- **The reported `2k-1` non-face internal steps per shell is correct.** Its initial cap→ring and every ring→next-ring junction is edge-diagonal; the final ring→inward cap and cross-shell links are face steps. Direct evaluation of the original archive's `model_astar_unrank` for `k=1..10` gave `1,3,5,7,9,11,13,15,17,19` edge diagonals, totalling **100**.
- **C is genuinely different.** C starts on the *opposite* axial cap for the same shell parity and, decisively, **reverses every other intermediate ring** to make its ring-to-ring links face steps. C has one edge diagonal per shell: **10** through radius 10. At rank 1, for example, A* gives `(0,0,-1)` but C gives `(0,0,1)`. They are different identifier assignments, not interchangeable production schemes.
- First ten shells: A* has **100** non-face steps; C has **10**. General totals through shell `K`: `K²` versus `K` respectively.

This resolves Claude's uncertainty about the original archive without speculating from a secondary summary.

## 4. Production encoder audit: correction required

### `calc/mobileGPS.html`

At the relevant lines the page defines:

```js
function max(v1, v2, v3) { /* compares only v1, v2, v3 */ }
var square_number = max(my_y + 1, my_z + 1, -my_y, -my_z);
```

**JavaScript ignores `-my_z` here.** The *actual* value is `max(y+1,z+1,-y)`, not the four-argument maximum described in Investigation 2.

Consequently, the claimed collision `(-s,-s)` vs `(-s+1,-s)` for every `s>=2` is **refuted for the current source**: for `s=2`, these yield respectively `cube_p=14` and `cube_p=3`, not identical values.

But the encoder is **still non-injective**. For fixed `x=0`, both `(y,z)=(-1,-1)` and `(0,-2)` yield `cube_p=4` and hence the identical final identifier. Reproducing the exact written arithmetic over `[-60,59]^2` gave **14,400 input cells but only 12,656 distinct `cube_p` values** (1,744 excess assignments); **127** cells had non-positive `cube_p`. This is a finite diagnosis, not an extrapolation of counts to the whole domain.

The originally proposed four-argument correction might itself reveal additional ring-order problems. **Do not patch this public encoder automatically**: first decide the canonical historical convention and establish fixed regression examples, since changing it would change published identifiers.

### `index.html`

Confirmed a distinct formatter defect: `formatCubeCode` concatenates scaled `x,y,z` fields and truncates to the first 22 characters. At typical ECEF magnitudes the first two fields alone occupy more than 22 characters, so `z` contributes **no digits**. Concrete input example:

- `formatCubeCode(0,0,0)` → `6378137000000063781370`
- `formatCubeCode(0,0,1000)` → the **same** 22-digit string.
- `formatCubeCode(0,0,-1000)` → the **same** 22-digit string.

The decoder reads fixed 7/7/8-character fields, inconsistent with the encoder's actual variable-length 14+-digit coordinate strings. Therefore the formatter is not a reversible identifier mapping. This is a read-only finding only; no production code was changed.

The separate `xyz2cube.py` formula is also not the HTML formula. Its historical authority cannot be inferred from its existence. The earlier review's assumption that `mobileGPS.html` is authoritative remains unproven.

## 5. Novelty and prior literature

A focused external search found literature on face-continuous three-dimensional Hilbert curves, including Haverkort's work (already listed in `research/bibliography.md`). None of the inspected results established the exact one-break Chebyshev-shell traversal, the origin-prefix parity law or this explicit centred radix congruence as a published theorem. **This is not evidence of novelty or priority.** No bibliography entry is added as falsely claiming those results; broader searches in Hamiltonian path covers of polycube surfaces and lattice enumerations remain worthwhile. “New” should mean “new within this research notebook,” not “first in the literature.”

## 6. Recommended next step: OP-9, with prerequisites

**OP-9 is a good high-value *research* priority**, but Theorem 7 only shows the parity barrier is absent at radix 5; it does not guarantee a self-similar block traversal. First formalise whether “bounded number of pieces” is independent of hierarchy level, what “aligned” means, whether the origin-centred prefix property is mandatory at every scale, and the entry/exit gate constraints.

Suggested near-term sequence:

1. Run the newly committed independent C/D reference test in the branch's actual Python environment, then preserve its output.
2. Correct Investigation 2's `mobileGPS.html` collision claim and qualify the bit-complexity bounds. Preserve historical source text and record the correction.
3. Ask the owner to establish the **authoritative published identifier** and historical coordinate/ID test fixtures before considering any encoder change.
4. Make OP-9 a constrained finite search over a centred `5×5×5` block, with explicit face-adjacent gate, parity and tiling conditions; only then generalise to multiple scales. In parallel, OP-7 (prefix-optimal Model C variant) is a comparatively small, well-scoped proof task.
5. Defer production or identifier migration decisions; measure C/D locality (OP-12) before choosing either candidate for applications.

**Bottom line:** The mathematical core is persuasive and independent tests support it. The encoder finding requires a substantive correction, proof of exact bit complexity still needs work, and neither C nor D should be described as a historical or production-compatible CUBIC POSTCODE numbering scheme.
