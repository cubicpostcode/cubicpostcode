# Research instructions for Claude — CUBIC POSTCODE Foundations

Read `README.md`, `research/2026-11-10-independent-review.md`, `mathematics/10-cap-centre-obstruction.md`, `research/findings-register.md`, then `research/open-problems.md` before proposing changes.

## Non-negotiable research protocol

- Scope: precise discrete mathematics, proofs/counterexamples, pseudocode, complexity, geospatial conventions and reproducible numerical verification; never silently modify live production identifier behaviour.
- Distinguish **historical specification** (not yet recovered) from **candidate enumeration models** (A, A*, B).
- Define the origin, grid-centre or corner anchoring, axis orientation, shell family (Chebyshev / Manhattan / Euclidean), traversal order, adjacency metric (6/18/26), index base, dimensionality and resolution before claiming a result.
- Status words: **ESTABLISHED** (cited literature), **PROVEN** (complete proof), **CONJECTURE** (unproved precise statement), **OBSERVATION** (finite evidence), **HYPOTHESIS** (speculative), **RECOMMENDATION** (engineering judgement).
- Prefer new theorems and counterexamples over premature optimization. Maintain a dated changelog and clearly distinguish new results from corrections to previously overclaimed results.
- Treat independent review as critical input, **not** an authority beyond challenge; verify proofs. A finite test is not a universal proof.
- Read `research/2026-11-10-claude-handoff.md` for the current task. The complete original Investigation 1 source archive has not yet been pushed to this GitHub branch: do not claim to have read files absent from GitHub.
- Propose a coherent folder-level patch, tests and bibliography; no code refactor of `calc/`, `apps/`, `js/`, `index.html` or other production paths.

## Critical correction to the original investigation

C-02 / OP-2 was initially a **CONJECTURE**. The 10 Nov 2026 independent review gives a complete cap-centre obstruction proof; record the status as **PROVEN** for the specified shell-order, planar-centre-first and 26-adjacency assumptions.

F-13 (Euclidean-shell closed-form impossibility) and F-19 (global optimality/lower bounds) were overclaimed. They are unresolved or need strict machine-model qualifications.

## Next priority

OP-1: investigate minimal face-adjacency breaks for complete cubic shells. Determine existence/construction of path covers and whether closed-form rank/unrank is possible. Start with exact constraint solving at k=1,2,3 and independent verification; no assumption of all-k generality.
