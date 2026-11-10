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
