# OP-9: a hierarchical, face-continuous, origin-first numbering on centred radix-5 blocks

**Date:** 2026-11-11 (Investigation 3)
**Author:** Claude (research session)
**Status:**

| Result | Status |
|---|---|
| Definitions H1–H6 | definitions |
| Lemma 8 (w-flip) | **PROVEN** |
| Theorem 9 (opposite-corner obstruction) | **PROVEN** |
| Theorem 10 (closed grammar gives a hierarchical numbering) | **PROVEN** |
| Theorem 11 (Model H5 exists) | **PROVEN, computer-assisted** |
| Theorem 12 (Hölder bound) | **PROVEN** |
| Remaining items | **OBSERVATION**, marked |

**Reproduce:**

```
python3 -I experiments/exp_i3_radix5_generators.py
python3 -I experiments/exp_i3_radix5_grammar.py
python3 -I experiments/exp_i3_model_h5.py
```

**Reference code:** `experiments/radix5.py` (`unrank`, `rank`).

Model H5 is a research candidate. It is **not** the production CUBIC POSTCODE numbering and is not compatible with any existing identifier.

## 1. What "hierarchical" must mean

**Conventions.**

- Cells are integer points of Z³, the cell-centred grid.
- Adjacency is face adjacency (6-adjacency).
- Ranks are zero-based.
- `r_s = (5^s − 1)/2`.
- `B_s = [−r_s, r_s]³` is the centred cube of side `5^s`.
- An **aligned block of level s** is `Q_s(v) = 5^s·v + B_s` for `v ∈ Z³`. For every `s`, these blocks tile Z³, and each level-`s+1` block is the disjoint union of 125 level-`s` blocks.

For a bijection `E : N → Z³` consider:

| | Property |
|---|---|
| H1 | **Origin first:** `E(0) = (0,0,0)`. |
| H2 | **Face continuity:** `E(n)` and `E(n+1)` are face-adjacent for every `n`. |
| H3 | **Centred prefix cubes:** `E([0, 125^t)) = B_t` for every `t`. |
| H4 | **Strong hierarchy:** for every `s` and `v`, `E⁻¹(Q_s(v))` is a single interval of length `125^s` starting at a multiple of `125^s`. |
| H4(m) | **Bounded fragmentation:** each `E⁻¹(Q_s(v))` is a union of at most `m` intervals, with `m` independent of `s`. |
| H5 | **Gates:** consecutive level-`s` blocks share a face, and each is entered and left at corner cells. |
| H6 | **Effective coding:** rank and unrank use `O(t)` table steps for `t` levels. |

**Why H3 is not hierarchy.** Model D (file 21) satisfies H1, H2 and H3, because every `r_t` is even. It fails H4 badly:

- **[OBSERVATION]** In Model D, the aligned 5-block centred at `(5,0,0)` falls into 23 separate rank intervals, and the aligned 25-block centred at `(25,0,0)` into 613. Model C behaves the same way.
- **[Interpretation]** The fragment count grows with the block size, so neither C nor D satisfies H4(m) for any `m`.

Theorem 7 of file 21 only removed a parity barrier to H3.

**H4 forces the structure studied here.** Under H3 and H4, `B_{t+1}` is visited as 125 consecutive intervals, one per child block. The first interval is `B_t`, so the centre child comes first. Hence:

- the child order is a Hamiltonian path of the 5×5×5 child grid starting at its centre;
- every non-centre child is visited by a face path of its block from an entry cell to an exit cell;
- consecutive children are joined by a face step across their common face.

This note studies the case where entry and exit cells are **corners** (H5). Non-corner gates are not excluded by anything below.

## 2. Gates and the w-flip lemma

A non-centre child entered at corner `ε ∈ {±1}³` (relative to its own centre) and left at corner `χ = ε` with the axes in `D ⊆ {x,y,z}` flipped, `D ≠ ∅`, is a piece of **type D**. Types up to symmetry are:

- **O**: `|D| = 3`, opposite corner;
- **F**: `|D| = 2`, face-diagonal corner;
- **E**: `|D| = 1`, edge-adjacent corner.

**Gate rule.** Leaving child `g` towards `g + σe_a` requires the exit corner to lie on that face, so `χ_a = σ`. The next child is then entered at the mirror corner: `ε' = χ` with component `a` flipped.

**Lemma 8 (w-flip).** Put `w_i = ε_i·(−1)^{g_i}` for the child at grid position `g` with entry corner `ε`. A step from a child of type `D` flips `w` exactly on `D`.

*Proof.* Moving along axis `a` flips `(−1)^{g_a}`. The new entry is `ε' = ε` flipped on `D Δ {a}`. So `w` flips on `(D Δ {a}) Δ {a} = D`. ∎

## 3. An obstruction: Peano-type gates cannot start at the centre

**Theorem 9.** Let `b ≥ 3` be odd. There is no ordering of the `b³` children of a block that:

- starts at the centre child;
- obeys the gate rule;
- traverses every non-centre child corner to **opposite** corner (type O).

*Proof.*

1. Suppose all types are O. By Lemma 8, `w` flips on every axis at each step. Along a Hamiltonian path of the bipartite child grid, `(−1)^{step}` equals the colour `(−1)^{g_x+g_y+g_z}`, up to a fixed sign.
2. Hence `ε_i(g) = λ_i·(−1)^{Σ_{j≠i} g_j}` for constant signs `λ_i`. The gate rule forces motion along axis `a` in direction `σ = χ_a = −ε_a`.
3. So on every line parallel to axis `a`, all moves go one way, namely `−λ_a·(−1)^{(sum of the other two coordinates)}`. The admissible moves form a fixed digraph, the 3-D "Manhattan" orientation.
4. At each corner child `(±(b−1)/2, ±(b−1)/2, ±(b−1)/2)`, every sum of two coordinates is even. So the three lines through it point in directions `−λ_x`, `−λ_y`, `−λ_z`.
5. The corner with sign vector `(λ_x, λ_y, λ_z)` therefore has in-degree 0. A Hamiltonian path must start at any vertex of in-degree 0, so it starts at that corner and not at the centre. ∎

*Consequence.* A centre-first hierarchy cannot be built from Peano-type (opposite-corner) pieces, at any level whose children are blocks rather than single cells.

- **[OBSERVATION]** A bounded depth-first search found the corner-to-opposite-corner (Peano) generator immediately. It found no centre generator in 5,000,053 nodes, as Theorem 9 predicts.

## 4. Closed grammars give hierarchical numberings

A **grammar** consists of:

- a set `T` of types;
- for each type `τ ∈ T`, a **piece generator**: a Hamiltonian path of `{−2..2}³` from child `(−2,−2,−2)`, entered at corner `(−,−,−)`, to the child at the exit corner of type `τ`, leaving outward. It obeys the gate rule, and every child has a type in `T`.
- a **centre generator**: a Hamiltonian path from child `(0,0,0)`, whose exit corner is `c₀ = (+,+,+)`, to a corner child `g`, leaving at `sign(g)`. Every non-centre child has a type in `T`.

The grammar is **closed** when every type it uses has a generator in it. Generators act under the 48 signed axis permutations: an actual child with entry `ε` and flip axes `D` uses the canonical generator mapped by the symmetry `S = diag(−ε)·P` with `P(D_canonical) = D`.

**Theorem 10.** A closed grammar with corner gates defines a bijection `E : N → Z³` with properties H1–H5, as follows:

- `C₀` is the origin, and `c₀ = (+,+,+)`.
- `C_L` is the centre generator reflected by `F_L = diag(c_{L−1})`, with child 0 equal to `C_{L−1}` and the other children pieces of side `5^{L−1}`.
- `c_L = F_L·sign(g)`.
- `E` restricted to `[0, 125^L)` is `C_L`.

*Proof.* By induction on `L`, prove two claims:

- (a) every piece of level `L` and type `τ`, under any symmetry, is a face path covering its block, from its entry corner cell to its exit corner cell;
- (b) `C_L` is a face path covering `B_L`, from the origin to the corner cell of `B_L` in direction `c_L`.

In both, every level-`s` sub-block (`s ≤ L`) is one interval aligned to a multiple of `125^s`.

**Base case `L = 0`.** A single cell is trivially such a path.

**Step.** Concatenate the 125 children in generator order. Inside each child, the inductive hypothesis applies. At each junction:

- child `i` ends at its exit corner cell `χ_i`;
- by the gate rule, that cell lies on the face towards child `i+1`;
- child `i+1` begins at the mirror corner cell, which is the adjacent cell across that face.

Endpoints:

- A piece begins at child `(−2,−2,−2)`, entered at its own entry corner, so it starts at the piece's corner cell. It ends at the exit corner child, leaving outward, so it ends at the piece's exit corner cell.
- For `C_L`, the reflection `F_L` sends the generator's assumed `c₀` to `C_{L−1}`'s true exit corner `c_{L−1}`. The path ends at the corner cell of `B_L` in direction `F_L·sign(g) = c_L`.

The gate rule is invariant under signed permutations, so the symmetric copies are valid.

**Alignment.** The child of the block `Q_L(u)` at grid offset `v` is `Q_{L−1}(5u + v)`. So the descendants at depth `L − s` are exactly the aligned level-`s` blocks inside, each traversed as one aligned interval.

**Conclusion.** Since `C_L` starts with `C_{L−1}`, the maps agree on common ranks. Since the cubes `B_L` exhaust Z³, `E` is a bijection. ∎

**Theorem 11 (existence, computer-assisted).** The grammar `T = {E}` is closed. Hence a numbering **Model H5** with H1–H6 exists.

*Certificate.* The two generators below were found by bounded search (`exp_i3_radix5_grammar.py`). They are re-verified on import of `radix5.py`:

- each is a Hamiltonian path of the 125 children;
- every step obeys the gate rule;
- the start and end conditions hold.

Each line lists 124 moves, where x/X means ±x and similarly for y and z. "Types" gives the flip axis of each child.

```
CENTRE  moves  xxyXXXXYxzXyxxYxxYZYzXyZYXzyZXXYxzXyxzYXyyxxYYxxyXyxyZXzXXXyxxxxZXXXXZxxxxZXXXXY
               xxxxYXXXXYxxxxYXXXXZxxxxyXXXXyxxxxyyXYXyXYXy        ends at child (-2,2,-2)
        types  xxxxxxxxxxxxxxyxxxyxxxxxyxyxxxxxxxxxzxxxyxxxyyxyyxxyxxxyxxxxxxxxxxxxzyxxxzyxxxxxxxxyyx
               xxxxxxxyyxxxzyxxxxxxxxyyxxxxyxxyyxxzxy       (children 1..124)
EPIECE  moves  xxxyxyXXXXyxxxxyXXXXzxxxxYXXXXYxxxxYXXZXXzxYXzyxYxZxzyxyXXYzXXyZxzyZXzyZxzxZYxxyXz
               xYXXYxxYXYXXXzyxYxxyXyxyXXYXyyxxxxYYYYZZZZ   from (-2,-2,-2) to (2,-2,-2)
        types  xxxyxyyxxxxxxxxyyxxxzyxxxxxxxxyyxxxxxxxyxxxxxzxxxyxyxxxyyxyzxxxxyxxxxxyxyxyxxxxxxxx
               xxxyyxxxyxxxzxxxyxyyxxyyxyxxyxxxxxyyyyzzzz   (children 0..124)
```

The proof of Theorem 11 is Theorem 10 together with this finite certificate. The certificate can be checked by hand in principle, and is checked by machine on every import.

**Independent checks [OBSERVATION]** (`exp_i3_model_h5.py`), on the whole of `B_3` (1,953,125 cells):

- bijection;
- every step a face step;
- `B_0`, `B_1`, `B_2` are prefixes;
- every aligned 5-block and 25-block is one aligned interval;
- rank inverts unrank;
- 4,000 random round trips with ranks below `125^40` and coordinates below `10^25`.

**Further search results [OBSERVATION]** (bounded searches; a failure to find is not a proof of non-existence):

- The grammar `{F}` is also closed.
- An O-piece built from E-children also exists.
- No F-piece was found within the bounds using E-children only, and no E-piece using F-children only.

## 5. Locality

**Theorem 12 (Hölder bound).** In Model H5, `|E(n) − E(m)|_∞ ≤ 10·|n − m|^{1/3}` for all `n ≠ m`.

*Proof.*

1. Let `n < m` and choose `s ≥ 1` with `125^{s−1} ≤ m − n < 125^s`.
2. By H4, ranks are cut into aligned intervals of length `125^s`, so `n` and `m` lie in the same interval or in two consecutive ones.
3. Consecutive level-`s` blocks contain face-adjacent cells (H2), so they are face-neighbours. Their union has Chebyshev diameter at most `2·5^s − 1`.
4. Finally, `5^s ≤ 5·(m − n)^{1/3}`. ∎

**For C and D no such bound exists.** In shell `k`, Model C runs each ring of `8k` cells contiguously. Ring positions `t` and `t + 4k` are on opposite sides of the ring, at Chebyshev distance `2k`. So `|ΔE|³/Δn ≥ (2k)³/(4k) = 2k²`, which is unbounded. Model D's annulus layers give the same.

**Backward locality: no bijection controls it.** For every bijection, some face-adjacent pairs have rank gaps that grow with the domain.

- **[Interpretation]** This is the standard fact for space-filling orders. Its usual proofs go through isoperimetry, and it is not re-proved here.
- Measured values for H5, C and D are in `research/2026-11-11-investigation-3.md`.
- Small steps between consecutive cells (H2) say nothing about this direction.

## 6. Rank and unrank

**Unrank.**

1. Write `n` in base 125. There are `t = ⌈log_125(n+1)⌉` digits.
2. Walk down the levels. At each level, take the digit's child offset and symmetry from a 125-entry table, compose symmetries and accumulate `centre += S·v·5^{L−1}`.

**Rank.** Walk down the levels in the same way. At each level, find the child containing the point by `v = (S^T(p − centre) + r_{L−1}) // 5^{L−1}`, and read its digit from the inverse table.

**Cost.** Both use `O(t)` table steps and `O(t)` additions and multiplications by powers of 5.

- The bit cost is `O(b²)` with schoolbook arithmetic, where `b` is the bit length.
- It is `O(M(b) log b)` if the radix conversions are done by divide and conquer. That second figure is a standard bound, not re-proved here.

No root extraction is needed, unlike Models C and D.

## 7. What is not claimed

- No claim about non-corner gate designs. Theorem 9 is specific to corner gates of type O.
- No claim that H5's generators are optimal, canonical or unique. A bounded search found them; many others presumably exist.
- No claim about other radices beyond Theorem 9 and file 21's parity condition.
- No compatibility with existing identifiers, and nothing in production was changed.
