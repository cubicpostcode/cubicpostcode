# Findings register — reviewed status (2026-11-10)

Do not overwrite the historical Investigation 1 findings register; this is a reviewed status snapshot for the GitHub handoff.

| ID / theme | Reviewed status | Qualification |
|---|---|---|
| Planar spiral | PROVEN for the specified scheme | Direct inverse via integer square root |
| Cubic shell cardinality | PROVEN | `24k²+2` for `k>=1` |
| Checkerboard parity imbalance | PROVEN | Odd-dimensional cubic shells |
| Shell-ordered full 6-adjacency | PROVEN IMPOSSIBLE | Shell-order constraint is essential |
| Model A encode/decode | PROVEN for candidate | Not verified against historical identifiers |
| Model A* 26-adjacency | PROVEN for candidate | Not fully planar consistent |
| 22-digit capacity | PROVEN arithmetically | Geospatial conventions still missing |
| Odd-radix nesting | PROVEN conditionally | Same cell-centred origin |
| C-02 / OP-2 cap-centre obstruction | **PROVEN (new 2026-11-10)** | Full proof in mathematics/10-... |
| Model B rank/unrank | INCOMPLETE PROOF | Shell arithmetic separate |
| F-13 Euclidean closed-form impossibility | **OPEN / DOWNGRADED** | No impossibility proof |
| Integer Newton roots | PROVEN | Float-seeded arbitrary-precision implementation gap |
| F-19 asymptotic optimality | **OPEN / DOWNGRADED** | `Ω(b)` does not imply `Ω(M(b))` |

An experimental pass is numerical evidence, not a theorem.

## Investigation 2 additions (2026-11-10)

Appended; the table above is unchanged. Details and proofs: `research/2026-11-10-investigation-2.md`.

| ID / theme | Status | Qualification |
|---|---|---|
| C-02 cap-centre obstruction | **INDEPENDENTLY VERIFIED** | Needs shell order, `k>=2`, two caps, full adjacency; all four necessary |
| I2-02 `k=1` exception | PROVEN (new) | Explicit 26-cell ordering |
| I2-03 local-minimum principle | PROVEN (new) | Any graph; breaks ≥ local minima − 1 |
| I2-04 forced jump length ≥ `k` | PROVEN (new) | Attained by the plane-sequential ordering |
| I2-05 colour-preserving step is unavoidable | PROVEN (new) | Face + corner-diagonal steps never suffice |
| I2-06 **OP-1: minimum non-face transitions = 1** | **PROVEN (new)** | All `k>=1`; break is an edge-diagonal step |
| I2-07 Model C encode/decode | PROVEN for candidate (new) | Not compatible with any existing identifier |
| I2-08 prefix-cube parity law | PROVEN (new) | Face-continuous enumerations |
| I2-09 Model D encode/decode | PROVEN for candidate (new) | Not shell-monotone; double shells |
| I2-10 centred radix ≡ 1 (mod 4) | PROVEN (new) | Statement about prefix cubes only |
| I2-11 exact checks `k=1,2,3` | OBSERVATION | Exhaustive search and CP-SAT |
| I2-12 existing encoders collide / disagree | OBSERVATION | Read-only; owner decision needed |
| F-13, F-19 | unchanged: OPEN / DOWNGRADED | Not worked on in Investigation 2 |
