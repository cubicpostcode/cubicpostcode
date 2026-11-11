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

## Investigation 3 additions (2026-11-11)

Appended; the tables above are unchanged. Details: `research/2026-11-11-investigation-3.md`.

| ID / theme | Status | Qualification |
|---|---|---|
| I2-12 encoder collisions | **CORRECTED** | The pair belongs to the 4-argument legacy formula; `mobileGPS.html` uses a 3-argument `max` and collides differently; no encoder is injective |
| File 20 unrank bit cost `O(M(b))` | **WITHDRAWN** | Proven for the code as written: `O(D(b) log b)`; the `O(M(b))` root literature is cited but not re-verified |
| I3-01 / I3-02 reviewer test plus extended C/D checks | OBSERVATION | Radius 10 and exhaustive radius 30; ranks up to `10^1000` |
| I3-07 opposite-corner (Peano-type) gates cannot start at the centre | **PROVEN (new)** | Any odd radix; corner gates of type O only |
| I3-08 closed grammar gives a strongly hierarchical, face-continuous, origin-first numbering | **PROVEN (new)** | Corner gates |
| I3-09 **OP-9: Model H5 exists** (radix 5, centred) | **PROVEN, computer-assisted** | Finite certificate in `mathematics/30-…`; checked on import |
| I3-10 H5 Hölder bound `‖ΔE‖_∞ ≤ 10·Δn^{1/3}` | **PROVEN (new)** | C and D have no such bound |
| I3-11 H5 exhaustive on B₃ plus locality versus C and D | OBSERVATION | 1,953,125 cells |
| I3-12 H5 needs more than 22 digits for the Earth; C and D fit | PROVEN (arithmetic) | Capacity only |
