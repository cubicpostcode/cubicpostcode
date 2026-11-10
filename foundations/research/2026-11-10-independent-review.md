# Investigation 1 — Independent mathematical review

**Reviewed:** 10 November 2026  
**Source:** `CubicPostcode-Foundations-Investigation1-2026-11-10.zip` (separate export tip `3686d49e3c8e52a3faa191c34b2aa1cd5c4d1a1f`).  
**This file:** a faithful GitHub handoff of the review's principal mathematical findings and corrections; the original complete review and source archive are separate local artifacts.

## Executive verdict

Substantial mathematical value. Six experiments from the original ZIP passed when independently run with `python -I experiments/run_all.py`. The Chebyshev shell arithmetic, defined Model A bijection, candidate A* 26-continuity and capacity calculations check out. A central conjecture **C-02 / OP-2** is now **PROVEN** by the cap-centre obstruction; see [complete proof](../mathematics/10-cap-centre-obstruction.md).

No evidence presented establishes compatibility of any candidate numbering with the original public CUBIC POSTCODE convention. Mathematics and production interoperability must remain separate.

## The eleven review verdicts

1. **CONFIRMED: planar square spiral.** Each ring `k` has `8k` points in interval `[(2k-1)^2,(2k+1)^2-1]`, covering the square boundary exactly once; direct and inverse mapping are correct under given conventions. The original independent brute-force walker tested 14,641 points.
2. **CONFIRMED: cubic shells.** `|S_k|=(2k+1)^3-(2k-1)^3=24k²+2` for `k>=1`; start identifier `(2k-1)^3` in zero-based shell-monotone enumeration, shell inverse `k=floor((icbrt(n)+1)/2)`.
3. **CONFIRMED: parity imbalance.** Bipartite checkerboard-class cardinalities on an odd-dimensional Chebyshev shell differ by two; the signed difference in 3D is `2(-1)^k`. The dimensional generalisation is `(-1)^(dk)-(-1)^(d(k-1))`.
4. **CONFIRMED: 6-adjacency obstruction.** Every complete cubic shell has even size but unequal parity-class cardinalities, so it cannot be traversed as one Hamiltonian path with face steps only. Taxicab shells and exact Euclidean squared-radius shells contain no intra-shell face edges. Always state the **shell-monotonicity assumption**.
5. **CONFIRMED: Model A, conditional.** Caps and intermediate planar rings partition the shell, permitting direct reversible rank and unrank. Within each fixed horizontal plane, the defined ordering preserves the chosen planar spiral. Its `k²+2k` jump count includes boundary transitions; it is **not** a demonstration of historical-identifier equivalence.
6. **CONFIRMED: Model A*.** Direction alternation and inward final cap give axial shell-boundary steps and `2k-1` non-face but 26-adjacent internal steps. A* necessarily relaxes part of planar ordering.
7. **CONFIRMED: 22-digit capacity (with domain qualification).** `icbrt(10^22-1)=21,544,346`; largest fully indexed odd cube has side `21,544,345` and radius `K=10,772,172` cells/metres. Its volume in cells is `9,999,997,353,850,624,863,625`. Reserve `2,646,149,375,136,375` identifiers for the next incomplete shell. A physical-Earth unit-volume capacity lower bound uses WGS84 ellipsoid volume near `1.0832×10^21 m³`, requiring at least 22 digits; this is not a production-ready geolocation encoding specification.
8. **CONFIRMED under centred-grid convention: odd-radix refinement.** Grids sharing a **cell-centred** origin and a scale ratio `b` have exactly nested cell boundaries iff `b` is odd. This does **not** prohibit ordinary corner-anchored dyadic octrees.
9. **GAP: asserted Euclidean-shell closed-form impossibility.** Mathematical difficulty of three-square counts does not prove that no exact closed form exists. Define permitted operations before making an impossibility claim. `O(R²)` squared-radius tabulation suffices for one natural precomputation, but no universal required-memory theorem was shown. Downgrade F-13.
10. **CONFIRMED mathematical Newton integer roots, with implementation limitation.** Pure-integer Newton cube root with safe upper seed works for arbitrarily big nonnegative integers. The original floating-seeded Python implementation can raise `OverflowError` (e.g. `float(10**400)`), so it is not a total arbitrary-precision implementation. Fall back to integer-only Newton.
11. **GAP: unconditional optimality.** Fixed-width O(1) counts are machine-model-dependent. The comparison decision-tree `Ω(log n)` bound is limited to that class of threshold algorithms. Writing `Θ(b)` output bits gives `Ω(b)`, **not `Ω(M(b))`**. Remove the unsupported global asymptotic-optimality claim; qualify upper bounds and models. Downgrade F-19.

## Newly proved theorem C-02

A cubic shell at radius `k>=2` has upper and lower cap centres `(0,0,±k)`. Under origin-first planar ordering, each must appear first in its own cap. Any 26-adjacent predecessor elsewhere in the shell would require the same two horizontal coordinates of magnitude at most 1 and a vertical coordinate `±(k-1)`; this lies strictly inside the shell. Thus each distinct cap centre would have to be first in the *entire* shell, impossible. See [formal proof](../mathematics/10-cap-centre-obstruction.md).

## Other correction notices

- F-12: a `PROVEN (outline)` label for candidate Model B exceeds the available formal proof; separate verified shell counting from its unverified full bijection.
- F-13: replace the Euclidean impossibility theorem with an open algorithmic question.
- F-19: limit mathematical-complexity claims to precisely stated arithmetic models and actual lower bounds.
- Do not conflate physical volume addressability with identifier semantics, coordinate anchoring, spatial geodesy, reference epoch, quantisation or checksum specification.
- Retain original conjecture and superseded claims as **dated historical records**; never silently rewrite research history.

## Relevant earlier literature (context, not novelty evidence)

- Rosenberg & Strong, “Addressing arrays by shells” (1972), listed at https://oeis.org/A319514; full source not independently inspected here.
- Matthew Szudzik, “The Rosenberg-Strong Pairing Function” (2017): https://arxiv.org/abs/1706.04129
- Rosenberg, “Managing Storage for Extendible Arrays” (1975): https://epubs.siam.org/doi/abs/10.1137/0204024
- Itai, Papadimitriou & Szwarcfiter, “Hamilton Paths in Grid Graphs” (1982): https://epubs.siam.org/doi/10.1137/0211056
- Lattice points and three-square representation counts are not reducible to an unsupported universal algorithmic impossibility.

## Design cautions

**Cubic versus Euclidean geometry:** Chebyshev shells are axis-aligned and natural for arithmetic rank/unrank, but are not shells of equal physical distance from Earth centre. Selecting them is an architectural choice.

**A versus A*:** A prioritises planar rank consistency but has long coordinate jumps; A* prioritises consecutive 26-adjacency but gives up part of planar consistency. Both are research candidates pending compatibility checks with historical 22-digit identifiers.

**Next investigation:** OP-1: find constructions or sharp lower bounds for minimal face-jump traversals / two 6-adjacent path covers on `S_k`. Use exact SAT/ILP checks for `k=1,2,3`, then search for an all-`k` proof and direct rank/unrank. Separately recover historical coordinate/ID examples before touching production code.
