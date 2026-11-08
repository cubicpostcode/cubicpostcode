# Cubic Postcode specification (DRAFT)

> **Status: DRAFT.** This document reconstructs the original 2020 Cubic Postcode design from its published sources. It is not a redesign. Items marked **UNRESOLVED** await the inventor's decision. No implementation may treat them as settled.

Conformance vectors: [`tests/spec_vectors.json`](../tests/spec_vectors.json). Independent checks: [`tests/test_spec.py`](../tests/test_spec.py), run with `python3 -B tests/test_spec.py -v`.

## 1. Purpose

A Cube Code names one 1 m cube in a 21,000,000 m cube centred on the Earth. The code is the cube's number, written with 22 digits. Cubes are numbered layer by layer, and within each layer in a clockwise square spiral as seen from Greenwich.

**Settled** means that every original source agrees:

- the prose and Python reference on the legacy website (`website.html`);
- the published numbering diagram;
- the original encoders and decoders.

## 2. Frame and units

- Cartesian, Earth-centred, Earth-fixed, in metres.
- +X points toward latitude 0, longitude 0; +Z toward the North Pole; +Y completes a right-handed frame (toward 90° E).
- Conversions use the WGS 84 ellipsoid: a = 6,378,137 m, 1/f = 298.257223563.
- **UNRESOLVED D6:** the WGS 84 realisation and reference epoch, and whether device heights are ellipsoidal or above mean sea level.

## 3. Cells

- **Constants:**
  - S = 21,000,000;
  - H = S / 2 = 10,500,000;
  - A = S² = 441,000,000,000,000 cubes per layer;
  - N = S³ = 9,261,000,000,000,000,000,000 cubes in total.
- A cell is an integer triple (x, y, z) with every coordinate in [−H, H). It is the 1 m cube with corners at integer coordinates whose centre is (x + ½, y + ½, z + ½).
- A point (X, Y, Z) that does not lie on a cell boundary belongs to the cell (⌊X⌋, ⌊Y⌋, ⌊Z⌋).
- **UNRESOLVED D3:** which cell holds a coordinate that is exactly a negative integer, such as X = −3.0. Two candidates exist:
  - *floor*: the half-open interval [i, i + 1), so −3.0 is in cell −3. This matches the comment in the original Python ("2nd Layer – [−1, 0)").
  - *original `coord_round`*: `int(v)` for v ≥ 0, `int(v) − 1` for v < 0, so −3.0 is in cell −4. This is what the original code does.

  They differ only at exact negative integers. Examples: latitude 0 with longitude 180° gives X = −6,378,137 exactly, and longitude −90° gives Y = −6,378,137 exactly.

## 4. Layers

- The layer number is ℓ(x) = 2x for x ≥ 0, and −2x − 1 for x < 0.
- So the first layer is x ∈ [0, 1), the second [−1, 0), the third [1, 2), the fourth [−2, −1), and so on.
- The last two layers are the front face (x = H − 1, nearest Greenwich) and the back face (x = −H).

**Proof that ℓ is a bijection [−H, H) → [0, S).** For x ≥ 0, ℓ takes each even value 0, 2, …, S − 2 once. For x < 0 it takes each odd value 1, 3, …, S − 1 once. The inverse is x = ℓ/2 for even ℓ and −(ℓ + 1)/2 for odd ℓ. ∎

## 5. Squares, corners and the settled sides

- The square number of (y, z) is **n = max(y + 1, z + 1, −y, −z)**. Square n is the boundary of [−n, n − 1]².
- The four corner positions of square n are:

| Corner | Position | Cell (y, z) |
|---|---|---|
| top-left | `left_top = (2(n − 1))² + 1` | (−n, n − 1) |
| top-right | `right_top = left_top + 2n − 1` | (n − 1, n − 1) |
| bottom-right | `right_bottom = right_top + 2n − 1` | (n − 1, −n) |
| bottom-left | `left_bottom = right_bottom + 2n − 1` | (−n, −n) |

**Settled positions p of a cell within its layer:**

- top-left corner: p = `left_top`;
- right side, y = n − 1, z = n − 1 … −n: p = `right_top + n − 1 − z`;
- left side, y = −n, z = −n … n − 2: p = `left_bottom + n + z`.

Cube 1 is (0, −1, 0), and cube 2 is (0, 0, 0), the cube to its right. Square 1 is cubes 1–4, square 2 is 5–16, and square 3 is 17–36.

**Lemma (squares partition the layer).**

- n(y, z) ≤ m holds exactly when (y, z) ∈ [−m, m − 1]².
- So square m has (2m)² − (2m − 2)² = 8m − 4 cells.
- Squares 1…H partition [−H, H)².
- Square n occupies positions [(2n − 2)² + 1, (2n)²], and `left_bottom + 2n − 2 = (2n)²`. ∎

**Lemma (open slots).** The settled rules place 4n distinct positions:

- the top-left corner, at `left_top`;
- the right side, at [`right_top`, `right_bottom`];
- the left side, at [`left_bottom`, (2n)²].

The 4n − 4 remaining cells are the top-row interior (z = n − 1, −n < y < n − 1) and the bottom-row interior (z = −n, −n < y < n − 1). In any one-to-one numbering, those cells must occupy exactly the slots T = [`left_top` + 1, `right_top` − 1] and B = [`right_bottom` + 1, `left_bottom` − 1]. ∎

## 6. Top-row and bottom-row interiors: UNRESOLVED (D1, D2)

The original sources disagree only here.

| Source | Top-row interior | Bottom-row interior |
|---|---|---|
| Published diagram (below), prose ("the second cube … is the adjacent cube on the right … we always go around"), original decoders, published Pi example | `right_top − n + 1 + y` (left to right) | `right_bottom + n − 1 − y` (right to left) |
| Original encoders (website.html Python, `calc/3xyz2cube.html`, `calc/6gps2cube.html`, `calc/mobileGPS.html`) | `right_top − n − y` (right to left) | `right_bottom + n − y` |
| Bug-bounty brief (2023) | examples 2 and 3 agree with the diagram; example 9 agrees with the encoders | no example |

Published diagram (legacy `images/bluecubestt.png`), facing the cube from Greenwich, with north at the top and east to the right:

```
z= 2:  17 18 19 20 21 22
z= 1:  36  5  6  7  8 23
z= 0:  35 16  1  2  9 24
z=-1:  34 15  4  3 10 25
z=-2:  33 14 13 12 11 26
z=-3:  32 31 30 29 28 27
        y=-3 -2 -1  0  1  2
```

**Facts about the candidates** (proved here and checked by the tests; none of them is a choice):

- **The encoders' bottom formula is not one-to-one.** For every square n ≥ 2, `right_bottom + n − y` at y = −n + 1 equals `left_bottom`, the position of the bottom-left corner, and slot `right_bottom + 1` is never used. A complete one-to-one numbering cannot keep it unchanged.
- **Both top-row directions work.** `right_top − n + 1 + y` and `right_top − n − y` are each affine with slope ±1 and map the 2n − 2 top-interior cells onto T. Either one, combined with `right_bottom + n − 1 − y` on the bottom row (which maps onto B), gives a one-to-one numbering.

**Theorem (conditional).** With a top-row rule mapping onto T and a bottom-row rule mapping onto B:

- the position p is a bijection [−H, H)² → [1, A];
- because 0 ≤ p − 1 < A, the code c = ℓ(x)·A + p is a bijection from the cells onto [1, N].

*Proof:* the open-slots lemma, the partition lemma and §4. ∎

**Candidates and their measured effect** (shares of the Earth's surface; 200,000 area-uniform points at height 0):

| Candidate | Top | Bottom | One-to-one | Diagram cells matched | Same code as the original encoders | Same cell as the original decoders | Spiral steps that are not face-adjacent |
|---|---|---|---|---|---|---|---|
| A | diagram | diagram | yes | 36 / 36 | 50.2% | 100% | one per square |
| B | encoders | diagram | yes | 30 / 36 | 75.0% | 75.2% | three per square |
| L (as written) | encoders | encoders | no | 24 / 36 | 100% | 50.2% | — |

- **D1:** which top-row direction is the original design.
- **D2:** whether to adopt `right_bottom + n − 1 − y` for the bottom row. It is the only one-to-one rule that any source supports. It changes the encoders' codes for bottom-row interior cells by one position, which is 1 m.

## 7. The code and its canonical form

- The code of cell (x, y, z) is c = ℓ(x)·A + p, with p from §5–6.
- It is written in decimal with leading zeros to exactly 22 digits. This always fits, because N < 10²².
- Codes run from `0000000000000000000001` to `9261000000000000000000`. `0000000000000000000000` and values above N name no cube; that is 7.39% of 22-digit strings.
- **UNRESOLVED D5:** which other input forms an application should accept. The legacy page mentions numbers without leading zeros, and a dash after a 10-digit prefix (`7636535637-373773383976`). Spaces are another possible form.

## 8. Decoding

Decoding is forced by §7, whatever D1 and D2 turn out to be:

1. ℓ = ⌊(c − 1) / A⌋ and p = ((c − 1) mod A) + 1. Using c mod A instead fails on the last cell of every layer.
2. x = ℓ/2 for even ℓ, and −(ℓ + 1)/2 for odd ℓ.
3. n = ⌊isqrt(p − 1) / 2⌋ + 1. This holds because p ∈ [(2n − 2)² + 1, (2n)²] exactly when isqrt(p − 1) ∈ {2n − 2, 2n − 1}.
4. Recover the cell from p:
   - `right_top` ≤ p ≤ `right_bottom`: right side, y = n − 1, z = `right_top` + n − 1 − p;
   - p ≥ `left_bottom`: left side, y = −n, z = p − `left_bottom` − n;
   - p = `left_top`: (−n, n − 1);
   - p in slot T or slot B: invert the rule chosen under D1/D2.

The cube's centre is (x + ½, y + ½, z + ½).

## 9. Outside the cube: UNRESOLVED (D4)

- **The original says nothing about points outside [−H, H)³.** Its altitude coverage is about 4,100 km above the equator.
- **Without a check, the formulas still produce codes for such points, and these collide or overflow:**
  - cell (0, 10,500,000, 0) yields `0000000441000031500002`, a code that lies in the layer of x = −1, i.e. it is also the code of a cell inside the cube;
  - large x yields codes above N, or with 23 digits.
- **What implementations must do is undecided.**

## 10. Unresolved decisions

| ID | Question | Section |
|---|---|---|
| D1 | Direction of the top-row interior | §6 |
| D2 | Adopting `right_bottom + n − 1 − y` for the bottom-row interior | §6 |
| D3 | Cell of an exact negative integer coordinate | §3 |
| D4 | Behaviour outside the 21,000,000 m cube | §9 |
| D5 | Accepted input forms of a code | §7 |
| D6 | WGS 84 realisation, epoch and height source | §2 |
| D7 | Canonical floating-point procedure from latitude, longitude and height to a cell | §12 |

## 11. Exact arithmetic requirements

- **In-layer values fit a double exactly:** p ≤ A = 4.41 × 10¹⁴ < 2⁵³.
- **Whole codes do not:** a code reaches N ≈ 9.26 × 10²¹, which needs 73 bits. Assembling and parsing codes must use exact integers: Python `int`, JavaScript `BigInt`, or a split into a high part and a low part of 12 digits using integer division.
- **Never use `parseFloat` on a code.** It loses up to 2¹⁹ positions.
- **Never use `parseInt` on a number.** It reads `3.9e-10` as 3.

## 12. Geodetic conversion (informative)

- **Forward:** the original calculators compute

  ```
  N = a / √(1 − e² sin² φ)
  X = (N + h) cos φ cos λ
  Y = (N + h) cos φ sin λ
  Z = (N(1 − e²) + h) sin φ
  ```

  with e² = (2 − f) f, and radians formed as `degrees / 180 * π`.
- **Inverse:** the original calculators use Bowring's method. With atan2 for every angle, it agrees with the forward conversion to within 1 mm up to 100 km of altitude.
- **Implementations disagree only in the last bits.** Different languages and libraries give different last bits, up to 2 × 10⁻⁹ m at Earth radius. That can matter only for points within nanometres of a cell boundary.
- **UNRESOLVED D7:** the canonical procedure for such boundary points. Conformance vectors therefore keep geodetic points at least 1 mm from any boundary.

## 13. Conformance vectors

[`tests/spec_vectors.json`](../tests/spec_vectors.json) contains:

| Group | Contents |
|---|---|
| `settled` | Cells and codes that every source agrees on: corners and sides of squares 1 to 10,500,000 in several layers, the 24 settled diagram cells, the first and last codes, and edge cases |
| `unresolved_d1_d2` | Diagram, Pi, London, Sydney and prose cells, with the code under candidates A, B and L |
| `unresolved_d3` | Points on negative integer boundaries, with both candidate cells |
| `unresolved_d4` | Cells outside the cube, with what the unchecked formulas produce |
| `unresolved_d5` | Input forms awaiting a decision |
| `gps_cells` | Latitude, longitude and height → cell, at least 1 mm from any boundary |
| `code_range` | First and last codes, and strings that name no cube |

## Annex A (informative): known deviations in existing implementations

| Where | Deviation |
|---|---|
| `index.html` 250–257 | Does not implement the spiral: a 44-character string cut to 22 discards Z, so northern and southern points at the same longitude get the same code |
| `index.html` 375–386 | Decoder slices 7, 7 and 8 digits and divides by 10⁷, so every code decodes to about (−35.45°, −135°, 4,669 km); altitude uses a sphere |
| `calc/mobileGPS.html` 174–183; legacy `calc/6gps2cube.html` 183–192 | A three-argument `max` is called with four arguments and drops −z, so bottom-row interior cells get codes from the wrong square. Fixed in `calc/3xyz2cube.html` in 2021 only |
| `calc/mobileGPS.html` 163–168 and legacy calculators | `parseInt` on numbers: the poles and points on longitudes ±90° and ±180° land in the wrong layer |
| `calc/mobileGPS.html` 217–219 | Overflowing codes are silently cut to 22 digits (see D4) |
| `xyz2cube.py` 15 | Square number taken as `max(abs(y), abs(z)) + 1`, which is wrong for negative coordinates; prints `3141592653589871375760` for the Pi example instead of `3141592653589793238462` |
| Legacy `calc/1cube2xyz.html` 214, `calc/2cube2gps.html` 213 | `parseFloat` of the code: decoded cells up to about 200 km off |
| All original decoders | `c mod A` and `c / A` fail on the last cell of each layer |
| Legacy `calc/3xyz2cube.html` 151 | Floating-point display split adds 10¹² for codes ending in about twelve 9s |
| All original encoders | Top and bottom rows: see §6 (D1, D2); exact negative integers: see §3 (D3) |

## Annex B (informative): questions for the inventor

1. D1–D7 above.
2. Is bug-bounty example 9 ((1.4, 2.4) → 18) a typo for x = −1.4?
3. Is the fixed altitude of 31,415 m in `calc/mobileGPS.html` intentional?
4. How was the code `6821822164313072477990` on the legacy London 3D page produced? Under §4–5 it lies in the layer of x = 7,734,492, about 5,100 km off the planet.
5. Which licence and copyright holder apply? The legacy code says CC BY 4.0; this repository's `LICENSE` is a truncated MIT text.

## Annex C: sources

All sources are in the legacy site repository `cubicpostcode/cubicpostcode.github.io`:

- `website.html`: prose specification at 78–140; Python decoder at 382–434; Python encoder at 441–534.
- `images/bluecubestt.png`, `images/cubes22long.png` (2021).
- `bugbounty.html` (2023).
- `calc/1cube2xyz.html` … `calc/6gps2cube.html` (2020 onwards).
