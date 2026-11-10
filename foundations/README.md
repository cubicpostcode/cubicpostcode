# CUBIC POSTCODE — Mathematical Foundations

**Research workspace / shared handoff for Claude.** Last updated **10 November 2026**.

> Mathematics first. Algorithms second. Software third.

This is a research-only subtree on the public `foundations-research` branch of `cubicpostcode/cubicpostcode`. The live application's `main` branch is deliberately unchanged. The original Investigation 1 package was prepared as a separate independent repository, but the current GitHub integration cannot create that new repository. These files form an initial **reviewed handoff**, **not yet a complete copy of the original ZIP**. Do not infer that absent source files, experiments, or proofs have been uploaded.

## Research question

Can every 1 m³ cubic cell be assigned a unique, hierarchical, efficiently reversible public identifier using precise, mathematically defensible rules? Distinguish a **candidate** map `Z³ ↔ N` from the **historical production** CUBIC POSTCODE convention, whose coordinate/identifier examples and geospatial conventions must still be recovered and checked.

## Confirmed discoveries (Investigation 1)

- Square spiral and Chebyshev cubic-shell enumeration yield explicit rank and unrank formulas for a defined candidate **Model A**, subject to its conventions.
- The cubic shell `S_k = { (x,y,z) : max(|x|,|y|,|z|)=k }` has `24k²+2` cells for `k>=1`.
- **Parity obstruction:** cubic-shell monotonicity and complete within-shell 6-neighbour (face-only) Hamilton paths are incompatible.
- **NEW — cap-centre theorem, C-02/OP-2 resolved:** cubic-shell monotonicity, full planar-spiral consistency, and 26-neighbour continuous ordering cannot all coexist. See [the proof](mathematics/10-cap-centre-obstruction.md).
- **Model A\***, a candidate with 26-adjacent consecutive cells, sacrifices some planar consistency.
- 22 decimal digits can enumerate the volume of the Earth at 1 m³ granularity in principle, but the exact geoposition-to-cell mapping and stable public identifier semantics remain an engineering specification task.
- All six experiments included in the **original local ZIP** passed the independent reviewer's run. **The original experiment source and results are not all present on this branch yet.**

## Corrections / unproved claims

- Do **not** assert a general impossibility of a closed-form Euclidean-shell rank/unrank algorithm.
- Do **not** infer an `Ω(M(b))` multiplication-complexity lower bound from merely printing `Θ(b)` output bits.
- Do **not** claim an arbitrary-precision floating-seeded cube-root routine is valid for every Python integer: `float(10**400)` overflows.
- Do **not** treat an outline of Model B's rank/unrank as a completed proof.
- Do **not** interpret “no continuous spiral” without naming the adjacency notion and shell-order constraint.

## Start here

1. [CLAUDE.md](CLAUDE.md) — research protocol and safety boundaries.
2. [Latest independent review](research/2026-11-10-independent-review.md) — eleven findings, qualifications and next steps.
3. [Cap-centre obstruction proof](mathematics/10-cap-centre-obstruction.md) — newly resolved C-02.
4. [Findings register](research/findings-register.md) and [open problems](research/open-problems.md).
5. [Handoff prompt](research/2026-11-10-claude-handoff.md).

**Archive provenance:** `CubicPostcode-Foundations-Investigation1-2026-11-10.zip`; tip commit recorded in its export as `3686d49e3c8e52a3faa191c34b2aa1cd5c4d1a1f`. This hash refers to the separate exported repository history and is **not** the SHA of this GitHub branch.

**Important:** New mathematical ideas and proofs are encouraged. Production refactors, renumbering, website changes and irreversible historical-identifier decisions are explicitly out of scope.
