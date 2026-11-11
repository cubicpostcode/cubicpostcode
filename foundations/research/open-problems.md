# Open problems and priorities (as of 2026-11-10)

## OP-1 — Minimum face-jump complete cubic-shell traversals (PRIORITY)

For `S_k={max(|x|,|y|,|z|)=k}`, find sharp lower bounds and constructive orderings that minimise transitions which are not 6-adjacent. Can `S_k` be covered by two vertex-disjoint 6-adjacent paths with endpoint requirements compatible with neighbouring shells? Can such an ordering have direct rank/unrank?

Methods: exact-cover / SAT / ILP for `k=1,2,3`; verify cardinality, uniqueness, adjacency, end points and shell-boundary connections; search for symbolic generalisation and all-k proof. Finite tests alone never prove the universal statement.

## OP-2 / C-02 — Cap-centre consistency versus king continuity (RESOLVED)

**Status: PROVEN on 2026-11-10** via [cap-centre obstruction](../mathematics/10-cap-centre-obstruction.md). Retain the historical conjecture wording in older research notes for provenance. No full cubic shell traversal for `k>=2` has both cap-centres-first ordering and 26-adjacent steps.

## OP-3 — Historical-identifier compatibility

Collect original coordinate-to-22-digit identifier examples, origin and axis conventions; test against A, A*, symmetries and distinct hierarchical schemes. Without these, production numbering must not be changed.

## OP-4 — Euclidean-shell efficient rank/unrank

Define computational model and admissible closed forms. Explore exact representation counts `r_3(n)`, summatory formulas, integer arithmetic and practical time-memory bounds. Do not assert no closed form can exist.

## OP-5 — Complexity bounds

State upper bounds with precisely defined input bit length and multiplication cost, and prove nontrivial lower bounds independently. Generic output-size lower bound is only `Ω(b)`.

## OP-6 — Geographic discretisation

Specify Earth reference system, epoch, metres, cell anchoring, origin, axis orientation, height, quantisation, boundary assignment, error handling and versioning. Keep physical-cell capacity distinct from stable public identifier semantics.

---

# Update after Investigation 2 (2026-11-10)

Appended; the text above is unchanged.

## OP-1 — RESOLVED

**Status: PROVEN on 2026-11-10.** The minimum is exactly one non-face transition per shell for every `k >= 1`, attained by Model C with closed-form rank/unrank and face steps between shells. See `mathematics/20-one-break-shell-traversal.md`.

## OP-3 — sharpened

The repository contains three mutually inconsistent encoders, two of which are not injective (observations in `research/2026-11-10-investigation-2.md`). Before any compatibility test: the owner must state which encoder is authoritative and supply published identifier examples.

## OP-7 — Prefix-optimal one-break traversal

Write out and prove the variant of Model C in which the single break is the last step of each shell, so that every prefix (not only complete shells) has the minimum number of non-face steps.

## OP-8 — Higher dimensions

For odd `d` the shell colour surplus is ±2, so one break is necessary. Is one break sufficient for every odd `d >= 5`? For even `d >= 4` the surplus is 0: is the Chebyshev shell Hamiltonian by face steps? (`d = 2` is the ring.)

## OP-9 — A hierarchical face-continuous centred code (most promising)

Theorem 7 excludes centred radix 3 and allows radix 5 for origin-first prefix cubes. Is there a face-continuous enumeration in which **every** aligned block of side `5^t` (not only the origin-centred ones) is contiguous apart from a bounded number of pieces? This would combine Model D's continuity with prefix-style hierarchy.

## OP-10 — Counting and endpoints

Which pairs of cells are the endpoints of a one-break traversal of `S_k`? For `k = 1` the removable single cells are exactly the 14 majority-colour cells. How many optimal traversals are there?

## OP-11 — Planar consistency without shell order

Does a 26-continuous bijection `N -> Z^3` exist that restricts to the origin-first spiral in every horizontal plane, when shell-monotonicity is dropped? Necessary: each plane `z = c != 0` is first entered from the 3×3 centre of an adjacent plane.

## OP-12 — Locality

Measure and bound worst-case and average locality of Models C and D against 3-D Hilbert-type curves (see `research/bibliography.md`), with the metric stated.

---

# Update after Investigation 3 (2026-11-11)

Appended; the text above is unchanged.

## OP-9 — RESOLVED (existence), with refinements open

**Status:** existence is **PROVEN, computer-assisted** for corner-gated designs. Model H5 is strongly hierarchical: every aligned `5^s`-block is one interval, with no fragmentation. Peano-type (opposite-corner) gates are **PROVEN impossible** for a centre-first order. See `mathematics/30-…`.

## OP-13 — Classification of radix-5 grammars

Which corner-gated type sets admit closed grammars? `{E}` and `{F}` do (by search). Is there a proof, without search, that a closed grammar exists for every radix `b ≡ 1 (mod 4)`? Can `b ≡ 3 (mod 4)` be handled at all once centred prefixes (H3) are dropped?

## OP-14 — Non-corner gates

Theorem 9 assumes corner gates. With entry and exit cells elsewhere on the boundary, which properties improve? In particular, is the worst face-neighbour rank gap better?

## OP-15 — Backward locality of H5

Bound the worst rank gap between face-adjacent cells within `B_t` as a function of `t`. Compare H5, C, D, Hilbert and Peano under one stated metric. Can the generator choice reduce the top-level centre-child seam?

## OP-16 — Capacity-aware hierarchy

H5 needs `125^11 > 10^22` ranks to reach the Earth's surface. Is there a hierarchical, face-continuous code (for example with mixed radices, or anchored differently) that covers the Earth within 22 digits? This is linked to Phase 3, which awaits instructions.
