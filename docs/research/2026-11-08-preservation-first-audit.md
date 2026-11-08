# Cubic Postcode: preservation-first technical report and Phase 1 plan

> **Historical research report. This is not an approved mathematical specification.**
>
> This document records a read-only audit carried out on 8 November 2026. It preserves the findings, measurements, proofs and open questions as they stood on that date.
>
> **No disputed numbering decision has been resolved.** Where the original sources disagree (decisions D1–D7 in §E), this report sets out the alternatives and their consequences without choosing between them. Those decisions belong to the inventor.
>
> The draft specification derived from this work is [`docs/SPEC.md`](../SPEC.md). It is also a draft and also leaves D1–D7 open. Nothing in this report changes any code, any published Cube Code or the live website.

## How to read this report

Every finding carries one of these labels:

| Label | Meaning |
|---|---|
| **[Fact]** | Confirmed directly from a source text, a published image or the git history |
| **[Tested]** | Measured by running code. This is evidence, not proof; the inputs and scripts are given in Appendix R |
| **[Proof]** | Follows by a mathematical argument given in full in §D |
| **[Interpretation]** | The auditor's judgement or reading of intent. Others may reasonably differ |
| **[Unresolved]** | An open question for the inventor (§E, §K). Not decided here |

**Line numbers:**

- `cubicpostcode/cubicpostcode` line numbers refer to commit `e695a72`, the `main` branch on the audit date.
- Legacy-site line numbers refer to `cubicpostcode/cubicpostcode.github.io` at commit `22467a3` (2026-10-20).

**Symbols:**

| Symbol | Meaning |
|---|---|
| S = 21,000,000 | cubes per edge |
| H = S/2 = 10,500,000 | half-width, in cubes |
| A = S² = 441,000,000,000,000 | cubes per layer |
| N = S³ = 9,261,000,000,000,000,000,000 | cubes in total |
| ℓ | layer number |
| n | square ("squareference") number |
| p | position within a layer |
| lt, rt, rb, lb | `left_top`, `right_top`, `right_bottom`, `left_bottom`: the four corners of square n |

---

## 0. Context, scope and decisions

### 0.1 The request

The request was a rigorous, read-only technical audit of the whole `cubicpostcode/cubicpostcode` repository with these aims:

- reconstruct the original Cubic Postcode design and its spiral-based enumeration;
- identify defects with reproducible examples;
- separate confirmed defects from uncertain historical intent;
- measure backward compatibility;
- propose a minimal repair supported by proofs and tests.

Constraints:

- **The original spiral design is to be preserved.** No DCH, Morton, Hilbert or decimal-prefix hierarchy may replace it.
- The founding principles are resilience, simplicity, determinism, portability and long-term stability.

### 0.2 What was examined

- **Main repository:** every file in `cubicpostcode/cubicpostcode` and its full history of 50 commits.
- **Legacy site:** `cubicpostcode/cubicpostcode.github.io`, cloned read-only. Only the postcode-related material was studied:
  - the prose specification and the Python reference code in `website.html`;
  - the published numbering diagrams;
  - the six original calculators, with their GitHub history back to 2020-08-19;
  - the 2023 bug-bounty brief;
  - the 3D London page.
- **Supplied research pack:**
  - the round-1 Claude consultation, as a text extraction;
  - the round-2 report and its scripts.

  The claude.ai share link itself was not opened; its content was taken from the pack's round-1 extraction.

**Method:**

- Every claim in this report was re-derived or re-run during the audit.
- Experiments were piped through standard input, so no project file was written during the audit itself.
- The live site `cubicpostcode.github.io` could not be fetched because the network policy blocked it. All legacy-site evidence therefore comes from its GitHub repository.

### 0.3 Decisions recorded from the user

- **Numbering.** Every point where the original sources disagree stays open for the inventor (§E). No code assignment may change.
- **Phase 1 scope.** Create only a draft specification and independent tests. Leave everything else untouched:
  - existing source files;
  - `tests/test_cube.py`;
  - `README.md`;
  - the converters;
  - published codes;
  - the live website.
- **When `calc/mobileGPS.html` is eventually repaired:** keep its fixed `altitude = 31415`.
- **When the live page's converters eventually switch to the spiral:** add a one-line muted note saying so.

### 0.4 Outcome so far

**Phase 1 was delivered** in commit `2a8b2441e60e7544118713418272ac6af4c6c9a0` on branch `claude/serene-archimedes-2mz259`. It added three files:

| File | Contents |
|---|---|
| `docs/SPEC.md` | Draft specification |
| `tests/spec_vectors.json` | 259 settled vectors; 16 cells that depend on D1/D2, each with the code under candidates A, B and L; the D3–D5 groups; 7 GPS vectors |
| `tests/test_spec.py` | 19 tests: 15 pass and 4 are skipped as UNRESOLVED |

Three deliberate corruptions each made the suite fail: a settled code, a candidate code and an oracle formula.

**Nothing else was changed**, and nothing was merged into `main` or deployed. This report was added afterwards, in its own commit.

### 0.5 Executive summary

1. **[Proof] The design is sound.** It consists of:

   - a 21,000,000 m cube centred on the Earth, divided into 1 m cells;
   - X layers taken in the order 0, −1, 1, −2, …;
   - within each layer, numbering that runs clockwise around nested squares as seen from Greenwich.

   With any consistent rule for the top-row and bottom-row interiors, this is a bijection onto codes 1 … 9,261,000,000,000,000,000,000. That number is below 10²², so every code fits in 22 digits.
2. **[Fact] The original sources disagree only on the top-row and bottom-row interiors of each square.**
   - The published diagram, the prose, the original decoders and the published Pi example agree with each other.
   - The original encoders run the top row the other way, and place the bottom row one position later.
3. **[Proof] Two of the candidate rules are not open choices; one top-row question is.**
   - The encoders' bottom-row formula is not injective: one collision per square per layer.
   - Both top-row directions are mathematically valid.
   - **[Unresolved]** Both points stay open (D1, D2).
4. **[Fact] The current live site, `index.html`, does not implement the spiral at all.** Its encoder discards Z, so northern and southern points collide, and its decoder ignores its input.
5. **[Tested] Implementation defects in other copies:**
   - a `max()` that silently drops one of its four inputs;
   - `parseInt` applied to numbers, which puts the poles and the ±90°/±180° meridians in the wrong layer;
   - `parseFloat` applied to 22-digit codes, which leaves decoders up to 197 km off;
   - a floating-point display split;
   - no domain checks;
   - an off-by-one at the last cell of each layer;
   - a corrupted Python re-implementation (`xyz2cube.py`) that misses the inventor's own Pi example.
6. **[Tested] Compatibility:**
   - 50.2% of the Earth's surface has the same code under every candidate resolution.
   - The live site's current codes cannot be preserved by any resolution.
   - GPS-page codes from 2020 to June 2026 were already imprecise in their last six digits.

---

## A. Faithful reconstruction of the original design

### A.1 Sources and provenance [Fact]

| Source | Content | Lines / commit |
|---|---|---|
| legacy `website.html` | Prose specification. Python decoder and encoder ("Author: Mr. Cubic Postcode, BEng (Hons)", CC BY 4.0; collaboration V. Sokolov, H. Chlegou) | prose 78–98, 114–127, 130–140; decoder 382–434; encoder 441–534 (layer comment 472–476, square comment 482–493, `max` 495, corners 501–504, sides 509–519, layer 525–528, code 531) |
| legacy `images/bluecubestt.png`, `images/cubes22long.png` | Published numbering of cubes 1–36, "facing our matrix of cubes from the Greenwich/Prime Meridian" | uploaded 2021-03-14 (`da8aea7`), updated 2021-03-18 (`8705907`) |
| legacy `bugbounty.html` | £100 bounty "to fix the code bug", with 10 worked examples (plus Python code described as ChatGPT-generated, not used as evidence) | created 2023-06-30 (`f77f253`) |
| legacy `calc/1cube2xyz.html`, `calc/2cube2gps.html` | JS decoders; spiral formulas unchanged since the first upload on 2020-08-19 (`055c795`) | 214–248; 213–247, `ECEFToLLA` 286–311 |
| legacy `calc/3xyz2cube.html` | JS encoder | 104–109, 121, 128–139, 147–153; 3-arg `max` → `Math.max` on 2021-02-06 (`2d358ef`); display split `b40ac90`, then `d356792` (`parseInt` → `Math.floor`) |
| legacy `calc/6gps2cube.html` | GPS → code | 172–177, 183–192, 199–210, 219–228; `toPrecision(22)` until 2026-06-05 (`82d1e4d`), then BigInt |
| legacy `calc/4xyz2gps.html`, `calc/5gps2xyz.html` | Geodetic converters (WGS 84 forward; Bowring inverse) | — |
| legacy `london3d/index.html` | Publishes `6821822164313072477990` as the "Nelson summit" code | 86–87, 148 |
| repo `calc/mobileGPS.html` | Copy of the legacy page; only the title, one heading and two comments differ | 101, 163–168, 174–183, 185–201, 204–207, 210–219 |
| repo `xyz2cube.py` | Re-typed encoder | 4–8, 15–32 |
| repo `gps_ecef.py` | WGS 84 forward conversion; prints on import | 3–17 |
| repo `index.html` | Live site (`CNAME` → cubicpostcode.com). `formatCubeCode` is present in all 22 revisions since the first commit `6e267ae` (2026-06-05); the spiral never appears | 235–257, 259–276, 368–388 |
| repo `js/cubicpostcode.js`, `tests/test_cube.py`, `apps/mobile/*` | 3-line stub; one empty test; Flutter placeholders | — |

### A.2 Timeline [Fact]

| Date | Event |
|---|---|
| 2020-08-19 | First calculators uploaded. The encoder has a 3-argument `max`, a reversed top row and a shifted bottom row; the decoder matches the later diagram |
| 2021-02-06 | `Math.max` fix and exact 10 + 12-digit display, in `3xyz2cube.html` only |
| 2021-03-14 | Numbering diagram published |
| 2023-06-30 | Bug-bounty page created |
| 2026-06-05 | This repository created, with a non-spiral `index.html`; legacy `6gps2cube.html` switched to BigInt |
| 2026-07-30 | "Trafalgar Sky" files added to and removed from this repository (unrelated to the spiral) |
| 2026-11-08 | UI polish commits `655dd07`, `369b07a`, `e695a72` |

### A.3 Published numbering (`bluecubestt.png`) [Fact]

Viewed from +X (Greenwich), with right = +Y (east) and up = +Z (north). Columns are y = −3 … 2.

```
z= 2:  17 18 19 20 21 22
z= 1:  36  5  6  7  8 23
z= 0:  35 16  1  2  9 24
z=-1:  34 15  4  3 10 25
z=-2:  33 14 13 12 11 26
z=-3:  32 31 30 29 28 27
```

`cubes22long.png` shows the same arrangement with every number written in 22 digits with leading zeros.

### A.4 Settled rules: every original source agrees [Fact]

- **Constants:**
  - S = 21,000,000 cubes per edge, so H = 10,500,000;
  - A = S² = 441,000,000,000,000 cubes per layer;
  - N = S³ = 9,261,000,000,000,000,000,000 cubes. The prose says "21 million cubed has 22 digits" (website.html 79, 89).
- **Frame** (website.html 544–550; prose 78):
  - Earth-centred and Earth-fixed;
  - +X toward lat 0 / lon 0, +Z toward the North Pole, right-handed, so +Y points toward 90° E;
  - conversions use WGS 84 (a = 6378137, 1/f = 298.257223563).
- **Cells:** 1 m cubes with integer corners and half-integer centres. The decoders print `X_meters`, and `Y_meters`, `Z_meters` with ±0.5 offsets.
- **Layers** (website.html 472–476; prose 116–125):
  - ℓ(x) = 2x for x ≥ 0, and −2x − 1 for x < 0;
  - so the first layer is x ∈ [0, 1), the second [−1, 0), the third [1, 2), and so on;
  - the last two layers are the front face (x = H−1) and the back face (x = −H).
- **Square ("squareference") number:**
  - n(y, z) = max(y+1, z+1, −y, −z) (website.html 495; `3xyz2cube.html:121` after the author's 2021 fix);
  - square n is the boundary of [−n, n−1]²;
  - square 1 is cubes 1–4, square 2 is 5–16, square 3 is 17–36 (website.html 482–484).
- **Corners** (identical in encoder and decoder):
  - `left_top = (2(n−1))² + 1`, at (−n, n−1);
  - `right_top = left_top + 2n − 1`, at (n−1, n−1);
  - `right_bottom = right_top + 2n − 1`, at (n−1, −n);
  - `left_bottom = right_bottom + 2n − 1`, at (−n, −n).
- **Left side** (y = −n): p = `left_bottom + n + z` for z = −n … n−2, and the top-left corner is `left_top`. The encoders, decoders and diagram all agree.
- **Right side** (y = n−1): p = `right_top + n − 1 − z` for z = n−1 … −n. All sources agree.
- **First cubes:** cube 1 is (0, −1, 0), "first layer … North and West"; cube 2 is the cube on its right (prose 96).
- **Code:** c = ℓ(x)·A + p.
- **Display:** 22 digits with leading zeros (website.html 109; `cubes22long.png`).

### A.5 Where the original sources disagree [Fact] (decisions: [Unresolved], §E)

| Item | Diagram, prose, decoders, Pi example | Original encoders (website.html 517/519; 3xyz2cube 137/139; 6gps2cube 208/210; mobileGPS 199/201) | Bug-bounty examples |
|---|---|---|---|
| Top-row interior (z = n−1, −n < y < n−1) | p = `right_top − n + 1 + y` (left to right, continuous) | p = `right_top − n − y` (right to left) | ex 2 and 3 agree with the diagram; ex 9 agrees with the encoders |
| Bottom-row interior (z = −n, −n < y < n−1) | p = `right_bottom + n − 1 − y` | p = `right_bottom + n − y` (not injective, §D.6) | no bottom example |
| Exact negative integer coordinates | decoders print centres only, so they are silent | `coord_round`: −3.0 → −4 | the comment at website.html 472–473 says [−1, 0), i.e. floor |

**The bug-bounty examples** (legacy `bugbounty.html`). In the bounty's plane coordinates, (x, y) correspond to (y, z) here. The ten worked examples, with the tile each expects:

| Example | Point | Tile |
|---|---|---|
| 1 | (−0.4, 0.4) | 1 |
| 2 | (−0.4, 1.4) | 6 |
| 3 | (−0.4, 2.4) | 19 |
| 4 | (−1.4, 0.4) | 16 |
| 5 | (1.4, 1.4) | 8 |
| 6 | (2.4, 2.4) | 22 |
| 7 | (−2.4, 0.4) | 35 |
| 8 | (2.4, 1.4) | 23 |
| 9 | (1.4, 2.4) | 18 |
| 10 | (−2.4, 1.4) | 36 |

- **[Fact]** Example 9 contradicts both the diagram (which puts 18 at y = −2) and examples 2 and 3.
- **[Fact]** Example 4 also contains a typo: it gives `peripheric_square_n = 1` alongside the corners of square 2.
- **[Interpretation]** Example 9 is probably a sign typo, since x = −1.4 gives 18. This is a question for the inventor (Q2), not a settled fact.

### A.6 Invariants

**[Fact/Proof]** Settled invariants, enforceable now:

- I1: code 1 is (0, −1, 0) and code 2 is (0, 0, 0);
- I2: all square corners and the left/right sides follow A.4;
- I3: layer ℓ occupies the block [ℓA + 1, (ℓ+1)A];
- I4: square n occupies the block [(2n−2)² + 1, (2n)²] and has 8n − 4 cells;
- I5: codes are written with 22-digit zero padding;
- I6: N = 21,000,000³ and N < 10²²;
- I7: the last code, N, is the cell (−H, −H, H−2), a left-side cell.

**[Proof, conditional]** These invariants hold only once D1 and D2 are resolved:

- I8: the numbering is a bijection onto [1, N];
- I9: decode∘encode = id;
- I10: one seam per square with the diagram's top-row direction, or three with the encoders' direction.

---

## B. Confirmed defects

All 15 were reproduced during the audit. The defect class column uses:

| Class | Meaning |
|---|---|
| Impl | The code deviates from a settled rule or from its own evident purpose |
| Conflict | The original sources disagree; the decision is open (§E) |
| Spec-gap | The original says nothing |

Where an entry says "decoded by the original decoders' rule", the measurement treats the original decoders as the reference. That is not a choice for D1 or D2: the comparison only measures how far an encoder's output lands, under the published decoder, from the cell that was encoded.

| # | Severity | Location | Reproduction (Appendix R) | Expected | Actual | Basis | Class |
|---|---|---|---|---|---|---|---|
| B1 | Critical | repo `index.html:250-257` | `formatCubeCode` for (51.5074, −0.1278, 0) and for (−51.5074, −0.1278, 0) | two different codes | both `1035613127381506369263`: 44 characters cut to 22, so Z never reaches the code. (0, 180, 100) gives `-100000000063781370000` | [Tested] | Impl (not the spiral) |
| B2 | Critical | `index.html:375-386` | decode `1234567890123456789012`, or any other code | that code's cell | about (−35.446°, −135.000°, 4,669 km) for every input. Altitude uses a sphere (21.3 km error even with correct ECEF); latitude uses a fixed factor | [Tested] | Impl |
| B3 | High | `calc/mobileGPS.html:174-183`; legacy `6gps2cube.html:183-192`. Fixed in `3xyz2cube.html` on 2021-02-06; never ported | the custom `max(v1, v2, v3)` is called with four arguments and drops −z ([Proof] §D.7) | Sydney (−4646052, 2553206, −3534373) | decoded by the original decoders' rule, the code lands 1,388 km away; Cape Town 2,638 km. Affects every bottom-row interior cell, 25.0% of the surface. Together with B4, outputs differ on 49.8% of the surface (median 3,443 km, max 19,216 km) | [Tested] | Impl |
| B4 | High (open, D1) | encoder top row: website.html:517, `mobileGPS.html:199`, `xyz2cube.py:30`, legacy calculators | cell (0, −1, 1) | the diagram says 6 | the encoders give 7, mirroring the row about y = −½. Through the original encoder and decoder: London lands 17.7 km away, Reykjavik 2,084 km, Tokyo 6,717 km. Affects 24.8% of the surface | [Tested] | Conflict |
| B5 | High | repo `xyz2cube.py:15`. The square is computed as `max(abs(y), abs(z)) + 1`, from the comment at website.html 493 rather than the code at 495 | `python3 xyz2cube.py` (Pi example) | `3141592653589793238462` (published) | `3141592653589871375760`. 22,500 collisions in a 300×300 window. Differs from the original decoders' rule on 75.1% of the surface (median 1,926 km, p90 7,212 km, max 9,005 km) | [Tested] | Impl |
| B6 | High | legacy `1cube2xyz.html:214`, `2cube2gps.html:213` (`parseFloat` of the code) | decode `3508590806758840271506` | centre (3977994.5, −8873.5, 4968874.5) | y = −206139.5, which is 197 km off. Sydney 161 km, Pi example 28 km, Singapore 64 km. Errors reach ½ ulp = 2¹⁸–2¹⁹ positions ([Proof] §D.9) | [Tested] | Impl |
| B7 | Medium (open, D2) | encoder bottom row: website.html:519, `mobileGPS.html:201`, `xyz2cube.py:32`, legacy calculators | cells (−1, −2) and (−2, −2) | two distinct codes | both get 14. One collision and one unused position per square per layer ([Proof] §D.6). The Pi example comes out as …463, not the published …462 | [Tested] | Conflict / Impl |
| B8 | Medium | JS `coord_round` uses `parseInt(number)`: `mobileGPS.html:163-168`; legacy 3xyz2cube 104–109, 6gps2cube 172–177 | North Pole: X = 3.9×10⁻¹⁰ becomes "3.9e-10", which parses as 3 | x = 0, code `0000000161633190314770` | x = 3, code `0000002807633190314770`. Every point on longitude ±90° or ±180°, both poles, and any \|v\| < 10⁻⁶ | [Tested] | Impl |
| B9 | Medium (open, D4) | all encoders: no domain check | cell (0, 10500000, 0) | outside the cube | `0000000441000031500002`, a code in the layer of x = −1, so it collides with a cell inside the cube. `mobileGPS.html:217-219` silently truncates 23-digit overflow | [Tested] | Spec-gap |
| B10 | Medium | all decoders (`cube % a`, `cube / a`) | `0000000441000000000000`, the last cell of layer 0 (a left-side cell) | (0, −10500000, 10499998) | cp = 0 gives NaN (JS) or a complex-number TypeError (Python), and the layer is off by one. The encoder's own definition forces `(c − 1)` division ([Proof] §D.8) | [Tested] | Impl |
| B11 | Low (open, D3) | `coord_round` at exact negative integers (Python and JS) | X = −3.0. At lat 0, lon 180, X = −6378137.0 exactly; at lon −90, Y = −6378137.0 exactly | floor gives −3 and −6378137 | −4 and −6378138, contradicting the comment's [−1, 0) | [Tested] | Conflict (code vs comment) |
| B12 | Low | legacy `3xyz2cube.html:151` (`Math.floor(slice*441 + cube_p*1e-12)`) | cell (3977994, −500000, 499997), a left-side cell | `3508590708999999999999` | `3508590709999999999999`, which is 10¹² too high. Roughly 2.4×10⁻⁷ of Earth-scale cells are affected | [Tested] | Impl |
| B13 | Low | legacy Python decoder `int(cube / a)` (website.html 422) | codes within 205,356 of a layer end, at layer ≈ 8×10⁶ | the correct layer | layer + 1. Only the outer squares are affected, far off the planet | [Tested] | Impl |
| B14 | Low | `index.html` inputs | latitude 999 | rejected | accepted; nothing checks ranges | [Fact] | Spec-gap |
| B15 | Info | historical display | 6gps2cube `toPrecision(22)` before 2026-06-05; 3xyz2cube Number assembly from August 2020 to February 2021 | exact digits | the last ~6 digits wrong by up to ±262,144 positions ([Proof] §D.9) | [Fact/Proof] | Historical |

### B.1 Repository hygiene [Fact] (not mathematical)

- `tests/test_cube.py` is one empty test.
- `js/cubicpostcode.js` is a 3-line stub.
- `gps_ecef.py:17` prints on import.
- `xyz2cube.py` ignores `argv`, unlike the original (website.html 452–457). Its "validated" comment (line 21) is false.
- `LICENSE` is a truncated MIT text ("…to any person obtaining a copy..."). The legacy code is labelled CC BY 4.0.
- `favicon.ico` is referenced but absent.
- `apps/mobile/pubspec.yaml` uses `development_dependencies` where it should use `dev_dependencies`.
- `calc/mobileGPS.html:34-42` loads Google Analytics on a geolocation page.

### B.2 UI defects in `index.html` [Fact] (deferred to Phase 1b)

- The `system_ui` typo (line 21).
- Labels are not associated with their inputs (161–170, 211).
- Status messages are not announced (178), and `aria-live` sits on the button instead (184).
- Every keystroke converts, auto-copies without a `.catch`, and adds a history row (162–170, 271–275, 278–281).
- Auto-copy is attempted on page load (412–419).
- `clearHistory` leaves the map trail (303–306), and `pathPoints` grows without limit (320).
- Reloading from history drops the altitude (297–301).
- A stale altitude is kept when the device reports none (329).
- `if (watchId)` (340).
- `let history` shadows `window.history` (233).
- The location error message is generic (351).

### B.3 Design properties, not defects [Fact] (the spiral keeps them)

- Decimal prefixes are thin square shells, not boxes. **[Interpretation]** The prose at 137–139, which claims prefix autocomplete, does not hold geometrically.
- Adjacent X layers are 2A codes apart.
- Squares have seams.
- There is no check digit, and 7.39% of 22-digit strings name no cube.
- Coverage is ±10,500 km per axis, which is about 4,100 km of altitude over the equator.

### B.4 Uncertain historical items [Unresolved]

- **Bug-bounty example 9** (§A.5).
- **The fixed `altitude = 31415`** in `mobileGPS.html:101`. The real altitude line is commented out next to it.
- **The Nelson code `6821822164313072477990`.**
  - **[Tested]** Under the settled layer and square rules it lies in the layer of x = 7,734,492, about 5,100 km off the planet.
  - **[Tested]** No scheme tested reproduces it at heights of 25–100 m around (51.508045, −0.128217). The schemes tested were the spiral, the `index.html` formatter and DCH.

### B.5 Checked and found harmless [Tested]

- **Legacy `ECEFToLLA` edge cases:** division by zero at X = 0 (Python), and longitude 0 instead of 180 when X < 0 and Y = 0. Neither can occur at a cell centre, because centres are always half-integers.
- **JavaScript (V8) vs Python (glibc)**, using the same formula: the bits differ on 19,947 of 200,000 inputs, by at most 1.9×10⁻⁹ m, with 0 cell differences.
- **The three ECEF formula variants in the code** (`index.html`, the legacy calculators, `gps_ecef.py`): 0 cell differences in 200,000 inputs.

---

## C. Compatibility analysis

### C.1 Candidate completions of the open rows [Tested; bijectivity: Proof]

These candidates are measured here, not chosen.

| Candidate | Top row | Bottom row | Bijective | Diagram cells (of 36) | Bounty examples (of 10) | Pi example | Same code as the original encoders | Same cell as the original decoders | Non-adjacent steps, squares 1–40 |
|---|---|---|---|---|---|---|---|---|---|
| A | diagram | diagram | yes (§D.4) | 36 | 9 | …462 ✓ | 50.2% | 100% | 39 (one seam per square) |
| B | encoder | diagram | yes (§D.5) | 30 | 8 | …462 ✓ | 75.0% | 75.2% | 117 (three per square) |
| L (as published) | encoder | encoder | **no**: 39 collisions in squares 1–40 | 24 | 8 | …463 ✗ | 100% | 50.2% | n/a |
| C | diagram | encoder | **no** | 30 | 9 | …463 ✗ | 75.2% | 75.0% | n/a |

Percentages are shares of the Earth's surface, from 200,000 area-uniform points at height 0.

- **[Proof]** L and C cannot be complete one-to-one code assignments.
- **[Unresolved]** The choice between A and B is a design decision (§E, D1).

### C.2 Effect on existing codes, by population

| Population | Unchanged under every candidate | Depends on D1/D2 | Already unreliable |
|---|---|---|---|
| Left/right sides and all corners (50.2% of the surface), including square 1 | ✓ | | |
| Bottom-row interior (25.0%) | | A and B both name the cell 1 m west of the cell the original encoders used. Keeping the encoders' value means keeping a collision | |
| Top-row interior (24.8%) | | Under A, a code issued by an encoder names the mirror cell y → −1−y; under B it is unchanged | |
| Published diagram, cubes 1–36 | 24 cells | 12 cells | |
| Pi example …462 | | preserved by A and B | |
| Prose example `7636535637373773383976` | decodes the same under A | it is a top-row code under the decoders, so B changes it | |
| GPS-page codes (6gps2cube, mobileGPS) | | | bottom interior wrong (B3); last digits imprecise before 2026-06-05 (B15) |
| `xyz2cube.py` outputs | | | 75% wrong (B5) |
| Live cubicpostcode.com codes since 2026-06-05 | | | not spiral codes; not unique; cannot be preserved |
| Nelson summit code | | | not reproducible (B.4) |

### C.3 City examples [Tested]

All at height 0. The "landed" columns give the distance between the encoded cell and the cell that the original decoders' rule assigns to the code each implementation produced.

| City | Cell | Side of its square | Original encoder (website / 3xyz2cube) | GPS pages (6gps2cube / mobileGPS) | Repo `xyz2cube.py` |
|---|---|---|---|---|---|
| London | (3977994, −8874, 4968874) | top-row interior | 17,747 m | 17,747 m | 17,747 m |
| New York | (1333998, −4654045, 4138300) | left/right side | same | same | 8,792,346 m |
| Sydney | (−4646052, 2553206, −3534373) | bottom-row interior | 1 m | 1,387,578 m | 1 m |
| Tokyo | (−3953076, 3358350, 3699066) | top-row interior | 6,716,701 m | 6,716,701 m | 6,716,701 m |
| São Paulo | (4017263, −4252595, −2532674) | left/right side | same | same | 1,719,922 m |
| Cape Town | (5026357, 1674395, −3539538) | bottom-row interior | 1 m | 2,637,709 m | 1 m |
| Nairobi | (5104424, 3821640, −142862) | left/right side | same | same | same |
| Reykjavik | (2586853, −1042144, 5716860) | top-row interior | 2,084,287 m | 2,084,287 m | 2,084,287 m |
| Singapore | (−1523119, 6191788, 149493) | left/right side | same | same | same |

**Surface-wide distribution** [Tested]. For the original encoder, among the 49.8% of surface points whose code differs from the decoders' rule:

- half land exactly 1 m away (the bottom row);
- the 90th percentile is 6,106 km;
- the maximum is 8,999 km.

### C.4 What must not change [Fact]

- S, A and N.
- The frame axes.
- 1 m cells with half-integer centres.
- ℓ(x).
- The square number.
- The corner values.
- The left and right sides.
- Cube 1 and cube 2.
- 22-digit zero padding.
- The 24 settled diagram cells.

---

## D. Mathematics: definitions and proofs [Proof]

S is any even number, H = S/2, A = S², N = S³. Cells are integer triples in [−H, H)³.

**D.1 Layers.** ℓ(x) = 2x for x ≥ 0, and −2x−1 for x < 0, is a bijection [−H, H) → [0, S).

*Proof.* For x ∈ [0, H), ℓ takes every even value in [0, S−2]. For x ∈ [−H, −1], ℓ takes every odd value in [1, S−1]. Both maps are injective, their images are disjoint, and together they cover [0, S). The inverse is x = ℓ/2 for even ℓ, and −(ℓ+1)/2 for odd ℓ. ∎

**D.2 Squares partition the layer.** Let n(y, z) = max(y+1, z+1, −y, −z). Then:

- (a) n(y, z) ≤ m ⇔ (y, z) ∈ [−m, m−1]²;
- (b) square m = [−m, m−1]² \ [−m+1, m−2]² has exactly 8m − 4 cells;
- (c) squares 1…H partition [−H, H)².

*Proof.*

- (a) n ≤ m ⇔ y+1 ≤ m ∧ −y ≤ m ∧ z+1 ≤ m ∧ −z ≤ m ⇔ −m ≤ y ≤ m−1 ∧ −m ≤ z ≤ m−1.
- (b) By (a), the cells with n = m are those in [−m, m−1]² but not in [−(m−1), m−2]². There are (2m)² − (2m−2)² = 8m − 4 of them.
- (c) By (a) with m = H, each cell has exactly one n in [1, H]. ∎

**D.3 Settled positions and the slots they leave.** Fix n ≥ 1. Write P = [lt, (2n)²] for the 8n − 4 positions of square n. Here lt = (2n−2)² + 1, and lb + 2n − 2 = (2n)².

The settled rules (A.4) place:

- the top-left corner at lt;
- the right side, including two corners, at [rt, rb]: 2n positions;
- the left side, including the bottom-left corner, at [lb, (2n)²]: 2n − 1 positions.

That is 1 + 2n + (2n − 1) = 4n positions, pairwise distinct.

**Claim.** In any injective assignment of square n onto P, the remaining 4n − 4 cells must occupy exactly the slots T = [lt+1, rt−1] and B = [rb+1, lb−1]. Those cells are the top-row interior (2n − 2 cells) and the bottom-row interior (2n − 2 cells).

*Proof.* The three settled ranges are disjoint, because lt < rt ≤ rb < lb. Counting gives |P| − 4n = 4n − 4 = |T| + |B|. ∎

*Consequence.* Any valid resolution of D1/D2 consists of a bijection from the top interior onto T and one from the bottom interior onto B. A resolution could also swap the two rows between T and B, but no source supports that.

**D.4 Candidate A is a bijection with one seam per square.**

- Top: p = rt − n + 1 + y maps y ∈ (−n, n−1) to (lt, rt). It is affine with slope +1, so it is a bijection onto T.
- Bottom: p = rb + n − 1 − y maps y ∈ (−n, n−1) to (rb, lb). It is affine with slope −1, so it is a bijection onto B.

So square n maps bijectively onto P (with D.3), and p is a bijection [−H, H)² → [1, (2H)²] = [1, A] (with D.2(c)).

Because 0 ≤ p − 1 < A, c − 1 = ℓA + (p − 1) is the unique mixed-radix representation. With D.1, c is a bijection [−H, H)³ → [1, S·A] = [1, N].

*Continuity.* On each side, consecutive positions differ by one cell, and the sides join at the corners. Position (2n)² sits at (−n, n−2) and position (2n)² + 1 at (−n−1, n), which are not adjacent. So there is exactly one seam per square. ∎

**D.5 Candidate B is also a bijection.** Its top rule p = rt − n − y maps y ∈ (−n, n−1) to (lt, rt) with slope −1, so it is a bijection onto T. The rest of the argument is as in D.4.

*Continuity.* The path breaks at lt → lt+1 and at rt−1 → rt for every n ≥ 2, in addition to the square seam. That gives three non-adjacent steps per square. **[Tested]** There are 117 in squares 1–40. ∎

**D.6 The published bottom-row formula is not injective.** For n ≥ 2, the encoders' p = rb + n − y behaves as follows:

- At y = −n+1 it gives rb + 2n − 1 = lb, which is the position of the bottom-left corner (−n, −n). That is a collision.
- Over y ∈ (−n, n−1) its range is [rb+2, lb], so slot rb+1 is never used.

So there is exactly one collision and one unused position per square n ≥ 2, in every layer. ∎ **[Tested]** There are 39 collisions in squares 1–40 and 149 in squares 1–150.

**D.7 The three-argument `max` fails exactly on the bottom-row interior.** max(y+1, z+1, −y) < n(y, z) ⇔ −z > max(y+1, z+1, −y). That holds exactly when z = −n and −n < y < n−1.

For such cells, the computed "square" is too small. The right-side branch then yields p = rt′ + y − z, a position in a different square, so the cell receives another cell's code. ∎

**D.8 Decoding is forced by the encoder; it is not a design choice.**

- Since c = ℓA + p with 1 ≤ p ≤ A, ℓ = ⌊(c−1)/A⌋ and p = ((c−1) mod A) + 1.
- The legacy `c mod A` gives 0 when p = A (the last cell of the layer), and `⌊c/A⌋` then gives ℓ + 1. That is B10.
- The square is n = ⌊isqrt(p−1)/2⌋ + 1, because p ∈ [(2n−2)²+1, (2n)²] ⇔ isqrt(p−1) ∈ {2n−2, 2n−1}.
- Settled cells are recovered by inverting A.4:
  - p ∈ [rt, rb] gives the right side;
  - p ≥ lb gives the left side;
  - p = lt gives the top-left corner.
- Positions in T or B are inverted by whichever rule D1/D2 settles.

**D.9 Exactness bounds (portability).**

- p ≤ A = 4.41×10¹⁴ < 2⁵³, so all in-layer arithmetic is exact in IEEE doubles. The layer number satisfies ℓ < 2.1×10⁷.
- c ≤ N = 9.261×10²¹, and 2⁷² < N < 2⁷³. Assembling and parsing a code therefore needs integers wider than 53 bits: Python `int`, JavaScript `BigInt`, or an exact split at 10¹² using integer division.
- A double holding a code of at least 2⁷¹ has a spacing of 2¹⁹ or more. Its rounding error is therefore 2¹⁸–2¹⁹ positions, which explains B6 and B15.
- In JavaScript, `parseInt` on a number first converts it to a string. Values below 10⁻⁶, or of 10²¹ and above, are written in exponent form and parse wrongly (B8).

**D.10 Capacity.** N = 9,261,000,000,000,000,000,000 < 10²² = 10,000,000,000,000,000,000,000. Every code has at most 22 digits, and 7.39% of 22-digit strings (0, and every value above N) name no cube.

**D.11 Empirical checks (evidence, not proof) [Tested].**

- **Candidate A, exhaustive.** Every even S from 2 to 60, every cell of every layer. Injective, onto [1, S³], with the decoder as inverse, and exactly S/2 − 1 seams per layer.
- **Candidate A, full scale.** 300,000 random cells and 300,000 random codes, with 0 round-trip failures.
- **Candidates B, L and C.** Exhaustive over squares 1–40.
- **Surface figures.** 200,000 area-uniform points.
- **Python and JavaScript proposals (§F).** Agree on 150,120 vectors.
- **Legacy Bowring inverse, using atan2.** The figures are maxima over random samples of 20,000 points per height, from two independent runs:

  | Height | Maximum position error |
  |---|---|
  | 0 | 3.5–4.3×10⁻⁹ m |
  | 1 km | 1.1–1.6×10⁻⁸ m |
  | 100 km | 0.9–1.3×10⁻⁴ m |
  | 1,000 km | 0.7–1.0×10⁻² m |
  | 4,000 km | 5.4–8.0×10⁻² m |

  The `index.html` approximation is off by about 21.3–21.4 km at every height.

---

## E. Unresolved decisions register [Unresolved]

These decisions stay open. The specification and the tests must not resolve them.

| ID | Question | Candidates | Evidence | Consequence | Phase 1 treatment |
|---|---|---|---|---|---|
| D1 | Direction of the top-row interior | A: `right_top − n + 1 + y` (diagram). B: `right_top − n − y` (encoders) | For A: the diagram (36/36), the prose ("adjacent cube on the right … we always go around"), all decoders, bounty examples 2 and 3, and continuity. For B: every encoder since 2020, and bounty example 9 | Changes 24.8% of either the encoders' codes (A) or the decoders' results (B) | Both candidates stated; vectors carry both values; tests check facts about each, never a choice |
| D2 | Bottom-row interior | The diagram's `right_bottom + n − 1 − y` is the only injective rule any source supports. Keeping the published formula is mathematically impossible for a bijection (D.6) | Diagram, decoders, Pi example | Changes 25.0% of the encoders' codes by 1 m | Same as D1 |
| D3 | Cell of an exact negative integer coordinate | Floor ([i, i+1)), or the original `coord_round` (−3.0 → −4) | The comment at website.html 472–473 (floor) against the code | Only exact negative integers, e.g. the equator at lon 180 or lon −90 | Both cells listed; test skipped as UNRESOLVED |
| D4 | Points outside the 21,000,000 m cube | Reject, or another rule | The original is silent; the current formulas alias (B9) | Altitudes above about 4,100 km | Examples listed; the aliasing tested as a fact |
| D5 | Accepted input forms | Exactly 22 digits, or also: without leading zeros, with a dash after 10 digits (prose 137–139), with spaces | website.html 382 ("without leading zeros"), 109, 137–139 | Parsing only; no change to the numbering | Strings listed as UNRESOLVED |
| D6 | Geodetic frame | WGS 84 realisation and epoch; ellipsoidal or sea-level heights from devices | The calculators use WGS 84 constants only | Cells drift centimetres a year relative to the ground | Stated as open in SPEC |
| D7 | Canonical floating-point procedure from lat/lon/h to a cell | For example the original order `lat / 180 * PI`, plus a tolerance policy for boundary cases | 0 cell differences in 200,000 inputs; bit differences up to 1.9×10⁻⁹ m | Only points within nanometres of a cell boundary | Geodetic vectors kept at least 1 mm from boundaries |

**[Interpretation]** The evidence for D1 leans toward A, because only A forms a continuous spiral and matches the published diagram. The encoders, however, are what produced codes for users. This report does not decide.

**Non-mathematical questions for the author [Unresolved]:**

- Q1: Was the D1/D2 disagreement the "code bug" the bounty was posted for?
- Q2: Is bug-bounty example 9 a typo for x = −1.4?
- Q3: Is the fixed `altitude = 31415` intentional? It is kept meanwhile.
- Q4: How was `6821822164313072477990` produced?
- Q5: Which licence applies, CC BY 4.0 or MIT, and who is the copyright holder?
- Q6: Should auto-copy be on by default?

---

## F. Reference implementation proposals

These are proposals only. They were **not adopted**, are not part of Phase 1 and do not exist in the repository.

- **[Interpretation]** They embody one possible resolution: candidate A for D1/D2, floor for D3 and rejection for D4. They are kept so that review can start immediately once the inventor decides.
- Lines that depend on a decision are marked `# D1`, `# D2`, `# D3` or `# D4`. Candidate B would change only the two `# D1` lines.

**[Tested]** During the audit these files were run straight from the plan text. They:

- reproduce the Pi example and all 36 diagram cells;
- fill codes 1…40,000 exactly with squares 1–100;
- passed 200,000 random round trips;
- agree between Python and JavaScript on 150,120 vectors;
- reject all invalid inputs tested.

```python
# file: xyz2cube.py  (proposal, not adopted)
"""Cubic Postcode: 1 m ECEF cell <-> 22-digit Cube Code (original spiral numbering).

Command line: python xyz2cube.py X Y Z   (ECEF metres) prints the 22-digit code.
"""
import math
import sys

SIDE = 21_000_000              # cubes along each edge of the giant cube
HALF = SIDE // 2               # cell indices run from -HALF to HALF - 1
LAYER_SIZE = SIDE * SIDE       # 441 000 000 000 000 cubes in each X layer
MAX_CODE = SIDE * LAYER_SIZE   # 9 261 000 000 000 000 000 000 (21 million cubed)


def coord_round(v):
    """Index i of the 1 m cell [i, i + 1) that contains coordinate v."""
    if not math.isfinite(v):
        raise ValueError("coordinates must be finite numbers")
    return math.floor(v)                                # D3


def _corners(n):
    left_top = (2 * (n - 1)) ** 2 + 1
    right_top = left_top + 2 * n - 1
    right_bottom = right_top + 2 * n - 1
    left_bottom = right_bottom + 2 * n - 1
    return left_top, right_top, right_bottom, left_bottom


def cell_to_code(x, y, z):
    """22-digit code of the integer cell (x, y, z)."""
    for v in (x, y, z):
        if not (isinstance(v, int) and -HALF <= v < HALF):
            raise ValueError("cell is outside the 21 million metre cube")   # D4
    n = max(y + 1, z + 1, -y, -z)                       # square number
    left_top, right_top, right_bottom, left_bottom = _corners(n)
    if n == -y:                                         # left side
        cube_p = left_top if n == z + 1 else z + left_bottom + n
    elif n == y + 1:                                    # right side
        cube_p = right_top + n - 1 - z
    elif n == z + 1:                                    # top side
        cube_p = right_top - n + 1 + y                  # D1
    else:                                               # bottom side
        cube_p = right_bottom + n - 1 - y               # D2
    layer = x * 2 if x >= 0 else -x * 2 - 1
    return f"{layer * LAYER_SIZE + cube_p:022d}"


def code_to_cell(code):
    """Integer cell (x, y, z) named by a 22-digit code string."""
    if not (isinstance(code, str) and len(code) == 22 and code.isascii() and code.isdigit()):
        raise ValueError("a Cube Code is exactly 22 digits")
    c = int(code)
    if not 1 <= c <= MAX_CODE:
        raise ValueError("Cube Code is outside 1 .. 9261000000000000000000")
    layer, rest = divmod(c - 1, LAYER_SIZE)
    cube_p = rest + 1
    n = math.isqrt(cube_p - 1) // 2 + 1
    left_top, right_top, right_bottom, left_bottom = _corners(n)
    if cube_p <= right_top:                             # top side
        y, z = cube_p - right_top + n - 1, n - 1        # D1
    elif cube_p <= right_bottom:                        # right side
        y, z = n - 1, right_top + n - 1 - cube_p
    elif cube_p < left_bottom:                          # bottom side
        y, z = right_bottom + n - 1 - cube_p, -n        # D2
    else:                                               # left side
        y, z = -n, cube_p - left_bottom - n
    x = layer // 2 if layer % 2 == 0 else -(layer + 1) // 2
    return x, y, z


def xyz_to_cube(X, Y, Z):
    """22-digit code of the cell containing the ECEF point (X, Y, Z), in metres."""
    return cell_to_code(coord_round(X), coord_round(Y), coord_round(Z))


def cube_to_xyz(code):
    """ECEF centre, in metres, of the cell named by a 22-digit code."""
    x, y, z = code_to_cell(code)
    return x + 0.5, y + 0.5, z + 0.5


if __name__ == "__main__":
    if len(sys.argv) == 4:
        print(xyz_to_cube(*(float(a) for a in sys.argv[1:])))
    else:
        # The original Pi-inspired example; prints 3141592653589793238462
        print(xyz_to_cube(3561896.5, -8402969.5, -9767161.5))
```

```python
# file: gps_ecef.py  (proposal, not adopted)
"""WGS 84 latitude, longitude and ellipsoidal height <-> ECEF metres."""
import math

A = 6378137.0                    # equatorial radius (m)
F = 1 / 298.257223563            # flattening
B = A * (1 - F)                  # polar radius (m)
E2 = (2 - F) * F                 # first eccentricity squared
EP2 = (A * A - B * B) / (B * B)  # second eccentricity squared


def gps_to_ecef(lat_deg, lon_deg, alt_m=0.0):
    if not all(math.isfinite(v) for v in (lat_deg, lon_deg, alt_m)):
        raise ValueError("latitude, longitude and altitude must be finite numbers")
    if not (-90 <= lat_deg <= 90 and -180 <= lon_deg <= 180):
        raise ValueError("latitude must be in [-90, 90] and longitude in [-180, 180]")
    lat = lat_deg / 180 * math.pi    # same operation order as the original calculators (D7)
    lon = lon_deg / 180 * math.pi
    s, c = math.sin(lat), math.cos(lat)
    n = A / math.sqrt(1 - E2 * s * s)
    return ((n + alt_m) * c * math.cos(lon),
            (n + alt_m) * c * math.sin(lon),
            (n * (1 - E2) + alt_m) * s)


def ecef_to_gps(X, Y, Z):
    """Bowring's method, as in the original calculators, using atan2 for every angle."""
    p = math.hypot(X, Y)
    theta = math.atan2(Z * A, p * B)
    st, ct = math.sin(theta), math.cos(theta)
    lat = math.atan2(Z + EP2 * B * st ** 3, p - E2 * A * ct ** 3)
    lon = math.atan2(Y, X)
    s, c = math.sin(lat), math.cos(lat)
    n = A / math.sqrt(1 - E2 * s * s)
    alt = p * c + Z * s - A * A / n  # same value as p / cos(lat) - N, but stable near the poles
    return math.degrees(lat), math.degrees(lon), alt
```

```js
// file: js/cubicpostcode.js  (proposal, not adopted)
/* Cubic Postcode reference implementation for browsers and Node. Exposes CubicPostcode. */
(function (root) {
  'use strict';

  const SIDE = 21000000;                      // cubes along each edge of the giant cube
  const HALF = SIDE / 2;                      // cell indices run from -HALF to HALF - 1
  const LAYER_SIZE = 441000000000000n;        // SIDE * SIDE cubes in each X layer
  const MAX_CODE = 9261000000000000000000n;   // 21 million cubed

  const A = 6378137;                          // WGS 84 equatorial radius (m)
  const F = 1 / 298.257223563;                // flattening
  const B = A * (1 - F);                      // polar radius (m)
  const E2 = (2 - F) * F;                     // first eccentricity squared
  const EP2 = (A * A - B * B) / (B * B);      // second eccentricity squared

  function coordRound(v) {
    if (!Number.isFinite(v)) throw new RangeError('Coordinates must be finite numbers.');
    return Math.floor(v);                                                 // D3
  }

  function corners(n) {
    const leftTop = (2 * (n - 1)) ** 2 + 1;
    const rightTop = leftTop + 2 * n - 1;
    const rightBottom = rightTop + 2 * n - 1;
    const leftBottom = rightBottom + 2 * n - 1;
    return [leftTop, rightTop, rightBottom, leftBottom];
  }

  function isqrt(m) {                         // exact for 0 <= m < 2^52
    let r = Math.floor(Math.sqrt(m));
    if (r * r > m) r -= 1;
    else if ((r + 1) * (r + 1) <= m) r += 1;
    return r;
  }

  function cellToCode(x, y, z) {
    for (const v of [x, y, z]) {
      if (!Number.isInteger(v) || v < -HALF || v >= HALF) {
        throw new RangeError('This point is outside the 21 million metre cube.');   // D4
      }
    }
    const n = Math.max(y + 1, z + 1, -y, -z);                             // square number
    const [leftTop, rightTop, rightBottom, leftBottom] = corners(n);
    let cubeP;
    if (n === -y) cubeP = n === z + 1 ? leftTop : z + leftBottom + n;      // left side
    else if (n === y + 1) cubeP = rightTop + n - 1 - z;                     // right side
    else if (n === z + 1) cubeP = rightTop - n + 1 + y;                     // top side (D1)
    else cubeP = rightBottom + n - 1 - y;                                   // bottom side (D2)
    const layer = x >= 0 ? x * 2 : -x * 2 - 1;
    return (BigInt(layer) * LAYER_SIZE + BigInt(cubeP)).toString().padStart(22, '0');
  }

  function codeToCell(code) {
    if (typeof code !== 'string' || !/^[0-9]{22}$/.test(code)) {
      throw new RangeError('A Cube Code has exactly 22 digits.');
    }
    const c = BigInt(code);
    if (c < 1n || c > MAX_CODE) throw new RangeError('This Cube Code is outside the 21 million metre cube.');
    const layer = Number((c - 1n) / LAYER_SIZE);
    const cubeP = Number((c - 1n) % LAYER_SIZE) + 1;
    const n = Math.floor(isqrt(cubeP - 1) / 2) + 1;
    const [, rightTop, rightBottom, leftBottom] = corners(n);
    let y, z;
    if (cubeP <= rightTop) { y = cubeP - rightTop + n - 1; z = n - 1; }               // top (D1)
    else if (cubeP <= rightBottom) { y = n - 1; z = rightTop + n - 1 - cubeP; }       // right
    else if (cubeP < leftBottom) { y = rightBottom + n - 1 - cubeP; z = -n; }         // bottom (D2)
    else { y = -n; z = cubeP - leftBottom - n; }                                      // left
    const x = layer % 2 === 0 ? layer / 2 : -(layer + 1) / 2;
    return [x, y, z];
  }

  function gpsToECEF(latDeg, lonDeg, altM = 0) {
    if (![latDeg, lonDeg, altM].every(Number.isFinite)) {
      throw new RangeError('Latitude, longitude and altitude must be numbers.');
    }
    if (latDeg < -90 || latDeg > 90 || lonDeg < -180 || lonDeg > 180) {
      throw new RangeError('Latitude must be between -90 and 90, longitude between -180 and 180.');
    }
    const lat = latDeg / 180 * Math.PI;      // same operation order as the original calculators (D7)
    const lon = lonDeg / 180 * Math.PI;
    const s = Math.sin(lat), c = Math.cos(lat);
    const n = A / Math.sqrt(1 - E2 * s * s);
    return [(n + altM) * c * Math.cos(lon), (n + altM) * c * Math.sin(lon), (n * (1 - E2) + altM) * s];
  }

  function ecefToGPS(X, Y, Z) {             // Bowring's method, as in the original calculators
    const p = Math.hypot(X, Y);
    const theta = Math.atan2(Z * A, p * B);
    const st = Math.sin(theta), ct = Math.cos(theta);
    const lat = Math.atan2(Z + EP2 * B * st ** 3, p - E2 * A * ct ** 3);
    const lon = Math.atan2(Y, X);
    const s = Math.sin(lat), c = Math.cos(lat);
    const n = A / Math.sqrt(1 - E2 * s * s);
    return [lat * (180 / Math.PI), lon * (180 / Math.PI), p * c + Z * s - A * A / n];
  }

  const api = {
    SIDE, LAYER_SIZE, MAX_CODE, coordRound, cellToCode, codeToCell, gpsToECEF, ecefToGPS,
    xyzToCode: (X, Y, Z) => cellToCode(coordRound(X), coordRound(Y), coordRound(Z)),
    codeToXYZ: (code) => codeToCell(code).map((v) => v + 0.5),
    gpsToCode: (lat, lon, alt = 0) => api.xyzToCode(...gpsToECEF(lat, lon, alt)),
    codeToGPS: (code) => ecefToGPS(...api.codeToXYZ(code)),
  };
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.CubicPostcode = api;
})(typeof window !== 'undefined' ? window : globalThis);
```

---

## G. Reference vectors, test strategy and earlier research

The complete machine-readable set is [`tests/spec_vectors.json`](../../tests/spec_vectors.json). The tables below are excerpts.

### G.1 Settled vectors (true under every candidate) [Tested]

| Cell (x, y, z) | Code | Why |
|---|---|---|
| (0, −1, 0) | `0000000000000000000001` | cube 1: top-left corner of square 1 |
| (0, 0, 0) | `0000000000000000000002` | cube 2 |
| (−1, −1, −1) | `0000000441000000000004` | second layer, all coordinates negative |
| (0, 1, 0) | `0000000000000000000009` | right side of square 2 (diagram) |
| (0, −2, 0) | `0000000000000000000016` | left side of square 2 (diagram) |
| (−6378137, 0, 0) | `5625516393000000000002` | lat 0, lon 180, if cells are [i, i+1). The D3 alternative is x = −6378138 |
| (0, −10500000, 10499999) | `0000000440999916000005` | outermost square, top-left corner |
| (0, −10500000, 10499998) | `0000000441000000000000` | last cell of layer 0 (B10) |
| (10499999, 10499999, 10499999) | `9260999558999937000004` | corner of the domain |
| (−10500000, −10500000, −10500000) | `9260999999999979000002` | corner of the domain |
| (−10500000, −10500000, 10499998) | `9261000000000000000000` | N, the last code |
| (3977994, −500000, 499997) | `3508590708999999999999` | the B12 display-split case (left side) |
| (1334000, −4654053, 4138306) | `1176588086640836791491` | New York at 10 m: a side cell |

### G.2 Vectors that depend on D1/D2 [Tested; choice: Unresolved]

Both values are kept; no choice is made. Short codes such as `…0006` stand for the full 22-digit zero-padded form.

| Cell | Candidate A (diagram) | Candidate B (encoder top) | Published encoders L | Why |
|---|---|---|---|---|
| (0, −1, 1) | `…0006` | `…0007` | `…0007` | diagram top row |
| (0, 0, 1) | `…0007` | `…0006` | `…0006` | diagram top row |
| (0, 0, −2) | `…0012` | `…0012` | `…0013` | diagram bottom row |
| (0, −1, −2) | `…0013` | `…0013` | `…0014`, colliding with (0, −2, −2) | diagram bottom row |
| (3561896, −8402970, −9767162) | `3141592653589793238462` | `3141592653589793238462` | `3141592653589793238463` | the inventor's Pi example |
| (3977994, −8874, 4968874) | `3508590806758840271506` | `3508590806758840289253` | `3508590806758840289253` | London: top row |
| (−4646066, 2553214, −3534384) | `4097829820967467881460` | `4097829820967467881460` | `4097829820967467881461` | Sydney at 20 m: bottom row |

### G.3 Geodetic vectors that don't depend on the numbering [Tested]

Each cell is at least 1 mm from any boundary. They agree with the current `gps_ecef.py` and with both proposals.

| lat, lon, h (m) | Cell |
|---|---|
| 51.5074, −0.1278, 0 | (3977994, −8874, 4968874) |
| 40.7128, −74.006, 10 | (1334000, −4654053, 4138306) |
| −33.8688, 151.2093, 20 | (−4646066, 2553214, −3534384) |
| 35.6762, 139.6503, 40 | (−3953100, 3358372, 3699089) |
| −23.55, −46.63, 760 | (4017741, −4253102, −2532978) |
| 64.1466, −21.9426, 15 | (2586859, −1042146, 5716873) |
| −1.2921, 36.8219, 1795 | (5105860, 3822716, −142902) |

**Boundary cases.** These are exact in IEEE arithmetic in both CPython and V8; D3 and D7 apply.

| Point | Floor cell | Note |
|---|---|---|
| North Pole | (0, 0, 6356752) | — |
| South Pole at 2,835 m | (0, 0, −6359588) | — |
| lat 0, lon 90 | (0, 6378137, 0) | — |
| lat 0, lon 180 | (−6378137, 0, 0) | `coord_round` gives x = −6378138 |
| lat 0, lon −90 | (0, −6378137, 0) | `coord_round` gives y = −6378138 |

### G.4 Test layers for future implementations

1. The frozen vectors.
2. Exhaustive checks of squares 1–100 in layers 0 and 1.
3. Seeded random round trips, 10⁵ in each direction.
4. Sign and boundary cases.
5. A compatibility oracle against the published encoders.
6. Python/JavaScript agreement on a shared JSON file.
7. Fuzzing with malformed input.

### G.5 Assessment of the earlier Claude research

R1 is the first-round consultation and R2 the second-round report, both from the supplied research pack.

| Earlier claim | Verdict |
|---|---|
| R1: `index.html` truncates the code, northern and southern latitudes collide, and Z is lost | **[Tested] Confirmed** (B1) |
| R1: the reverse converter returns a constant | **[Tested] Confirmed in substance.** R2's refinement (a tiny spread around one point) is correct |
| R1: the encoders' bottom row is off by one; their top-row direction disagrees with the decoders; the Pi example re-encodes to …463 | **[Tested] Confirmed** (B4, B7). R1 left the direction to the author. It is still open (D1), now with the published diagram as further evidence |
| R1: `xyz2cube.py` uses `max(abs)+1` | **[Fact] Confirmed** (B5). The source is the comment at website.html 493 |
| R1: `coord_round` fails at negative integers | **[Tested] Confirmed** (B11). R1 missed the `parseInt` exponent defect (B8) |
| R1: the decoders fail on the last cell of a layer and divide layers in floating point | **[Tested] Confirmed** (B10, B13) |
| R1: JavaScript's 2⁵³ limit | **[Tested] Confirmed.** R1 did not identify the three-argument `max` (B3) or the display split (B12), and did not measure the `parseFloat` loss in the decoders (B6) |
| R1: edge cases in the legacy `ECEFToLLA` | **[Fact] Confirmed by reading**, but never reached at a cell centre |
| R1: the forward WGS 84 conversion is correct | **[Tested] Confirmed** |
| R1: findings on the UI, licence and analytics | **[Fact] Confirmed by reading** (lines in B.1 and B.2) |
| R1: the altitude datum hypothesis | **[Unresolved]** (D6) |
| R1 and R2: recommend Morton or DCH | **Excluded by the mandate.** R2 itself retracted R1's decimal-prefix claim |
| R2: proof of the spiral repair, with exhaustive checks up to S = 40 | **[Proof/Tested] Confirmed, and extended to S = 60.** R2 treated the encoder-versus-decoder choice as settled; this report holds it open (D1/D2) |
| R2: capacity arithmetic | **[Proof] Confirmed** (D.10) |
| R2 scripts | **[Fact] Not self-contained:** `verify.py` needs numpy, `spiral.py` and `t2.py` print on import, and `dch.js` needs a file the bundle lacks |

---

## H. Phase 1 (agreed, and delivered in commit `2a8b244`)

**Scope:** three new files. Nothing else was modified:

- not `README.md` or `tests/test_cube.py`;
- not `xyz2cube.py`, `gps_ecef.py`, `js/`, `index.html`, `calc/`, `apps/`, `docs/APP_STORE_ASSETS.md` or `LICENSE`;
- not the legacy repository.

### H.1 `docs/SPEC.md` (draft)

The status line reads: "DRAFT. This document reconstructs the original 2020 Cubic Postcode design from its published sources. It is not a redesign. Items marked **UNRESOLVED** await the inventor's decision."

**Sections:**

1. Purpose.
2. Frame and units (D6 open).
3. Cells (D3 open).
4. Layers, with proof.
5. Squares, corners and settled sides, with the partition and open-slot lemmas.
6. The top-row and bottom-row interiors, **UNRESOLVED** (D1, D2): the evidence, the facts about each candidate, the conditional theorem and the compatibility table.
7. The code and its canonical form (D5 open).
8. Decoding.
9. Points outside the cube (D4 open).
10. The register of unresolved decisions.
11. Exact arithmetic requirements.
12. Geodetic conversion (D7 open).
13. Conformance vectors.

Annexes cover known deviations, questions for the inventor and sources.

### H.2 `tests/spec_vectors.json`

| Group | Contents |
|---|---|
| `settled` | 259 entries: corners and left/right samples for squares n ∈ {1, 2, 3, 4, 10, 1000, 10500000} in layers x ∈ {0, −1, 1, 10499999, −10500000}, the 24 settled diagram cells, and the G.1 rows |
| `unresolved_d1_d2` | 16 entries, each with codes under candidates A, B and L: the 12 open diagram cells, the Pi example, London, Sydney and the prose example |
| `unresolved_d3` | 4 points with exact negative integer coordinates, and 5 boundary GPS points, each with both candidate cells |
| `unresolved_d4` | 4 out-of-cube cells, with what the unchecked formulas produce |
| `unresolved_d5` | 4 input forms |
| `gps_cells` | 7 rows |
| `code_range` | the first and last codes, and strings that name no cube |

### H.3 `tests/test_spec.py`

- Uses only the Python standard library and imports nothing from the repository. Run it with `python3 -B tests/test_spec.py -v`.
- Contains a settled-rules oracle that returns `None` for any top-row or bottom-row interior cell, so it cannot resolve D1/D2.
- The candidate rules appear as named data, used only to test facts about each one.

**Results:** 19 tests, of which 15 pass and 4 are skipped with an "UNRESOLVED Dn" reason.

| Group | Tests |
|---|---|
| Vectors and capacity | `test_vectors_well_formed`, `test_capacity` |
| Settled rules | `test_layer_map_bijective`, `test_square_partition`, `test_open_slots`, `test_settled_vectors`, `test_published_diagram_settled_cells`, `test_decode_layer_and_position` |
| Facts about the candidates | `test_candidate_facts`, `test_candidates_on_squares_1_to_40`, `test_candidate_vectors`, `test_diagram_agreement_counts` |
| Facts recorded for the open decisions | `test_d3_points_record_both_conventions`, `test_d4_unchecked_formulas_leave_the_cube` |
| Geodesy | `test_gps_cells` |
| Skipped as UNRESOLVED | `test_unresolved_d1_d2`, `test_unresolved_d3`, `test_unresolved_d4`, `test_unresolved_d5` |

**Verification at delivery [Tested]:**

- **Vectors cross-checked.** Every vector was checked against both the separately written §F proposal and a fresh transcription of the published encoders. All 259 settled codes match both, as settled codes must.
- **Mutation checks.** A corrupted settled code, a corrupted candidate code and a corrupted oracle formula each made the suite fail.
- **Clean commit.** The commit added exactly three files, created no `__pycache__`, and left `main` at `e695a72`.

---

## I. Deferred development phases [Interpretation: proposed order]

**Phase 1b (behaviour-preserving):**

- `gps_ecef.py`: remove the print on import, add input validation, and add `ecef_to_gps`.
- `index.html`: fix the UI defects in B.2 while keeping the wording, colours, link chips and the tactile Copy Code button.

**Phase 2 (changes outputs; needs D1–D4 decided):**

- Replace `xyz2cube.py` and `js/cubicpostcode.js` with the §F proposals, adjusted to the decisions.
- Switch the `index.html` converters to the shared module, and add the agreed one-line note.
- Repair `calc/mobileGPS.html`, keeping 31,415 m.
- Add JavaScript tests and a cross-language vectors file.
- Turn the skipped tests into assertions.

**Phase 3 (optional):**

- A CI workflow.
- Text patches for the legacy github.io calculators.
- Resolve the licence question.
- Correct the Flutter and App Store claims.

**Rollback and risks (deferred phases):**

- Each phase is one commit, so `git revert` undoes it.
- Roll back if:
  - any frozen vector fails;
  - `python3 xyz2cube.py` does not print `3141592653589793238462`;
  - the live page throws an error on load;
  - Python and JavaScript disagree on any vector.
- GitHub Pages caching can be handled with a `?v=` query string.
- BigInt needs Safari 14 (2020) or later. Older browsers should get an error message, never a wrong code.

---

## J. Deliberately rejected, to protect conceptual integrity [Interpretation]

- DCH, Morton, Hilbert, or any other re-enumeration.
- A decimal-prefix hierarchy.
- Changing S, the layer order, the start corner, the clockwise direction or the 22-digit padding.
- Resolving D1–D7 inside the specification or the tests.
- A check digit inside the 22 digits.
- A normative digit grouping.
- Replacing the Bowring inverse.
- New frameworks, build tools or versioning machinery.
- Restyling the UI.

---

## K. Questions for the inventor [Unresolved]

1. **D1:** Which top-row direction is original: the diagram's (left to right) or the encoders' (right to left)?
2. **D2:** Should the diagram's bottom-row rule be adopted? The published formula cannot be kept without collisions.
3. **D3:** Are cells half-open [i, i+1), as the comment at website.html 472–473 says? Or should `coord_round`'s behaviour at exact negative integers stand?
4. **D4:** What should happen outside the 21,000,000 m cube?
5. **D5:** Which input forms are acceptable: leading zeros optional, a dash after 10 digits, spaces?
6. **D6 and D7:** Which WGS 84 realisation, epoch and height source apply, and which floating-point procedure is canonical?
7. **Q1–Q6 (§E):**
   - Was this the bounty's "code bug"?
   - Is bounty example 9 a typo?
   - Is the 31,415 m altitude intentional?
   - Where does the Nelson code come from?
   - Which licence and copyright holder apply?
   - Should auto-copy be on by default?

---

## Appendix R: reproducing the findings

**Sources.**

- This repository at commit `e695a72` for repo line numbers.
- The legacy site repository at commit `22467a3`:

  ```bash
  git clone https://github.com/cubicpostcode/cubicpostcode.github.io
  ```

  Then run `git checkout 22467a3`. The files are `website.html`, `bugbounty.html`, `images/bluecubestt.png` and `calc/*.html`. The diagram is read directly from `images/bluecubestt.png`.

**Environment.** The audit used Python 3.13 and Node 22. Every script below:

- uses only the standard library;
- reads from standard input and writes nothing;
- was run from this file before it was committed.

Each script's comments state its expected output.

### R1: legacy formulas, diagram, bounty and Pi example (Python)

Reproduces B4, B7, B3, B9, B10 and B13.

```python
# R1
A = 441_000_000_000_000
def legacy_cp(y, z, four_args=True):          # transcribed from website.html 495-519
    n = max(y + 1, z + 1, -y, -z) if four_args else max(y + 1, z + 1, -y)
    lt = (2 * (n - 1)) ** 2 + 1; rt = lt + 2 * n - 1; rb = rt + 2 * n - 1; lb = rb + 2 * n - 1
    if n == -y: return lt if n == z + 1 else z + lb + n
    if n == y + 1: return rt + n - 1 - z
    if n == z + 1: return rt - n - y
    return rb + n - y
DIAGRAM = [[17, 18, 19, 20, 21, 22], [36, 5, 6, 7, 8, 23], [35, 16, 1, 2, 9, 24],
           [34, 15, 4, 3, 10, 25], [33, 14, 13, 12, 11, 26], [32, 31, 30, 29, 28, 27]]
wrong = [(y, z) for z in range(2, -4, -1) for y in range(-3, 3) if legacy_cp(y, z) != DIAGRAM[2 - z][y + 3]]
print("encoder vs diagram mismatches:", len(wrong))                                  # 12
print("B4/B7 top", legacy_cp(-1, 1), legacy_cp(0, 1), "bottom", legacy_cp(-1, -2), legacy_cp(-2, -2))  # 7 6 14 14 (diagram: 6 7 13 14)
print("B7 Pi", f"{2 * 3561896 * A + legacy_cp(-8402970, -9767162):022d}")          # 3141592653589793238463 (published ...462)
print("B3 Sydney", legacy_cp(2553206, -3534373, four_args=False), legacy_cp(2553206, -3534373))  # 26075454707737 49967156856194
print("B9 alias", legacy_cp(10_500_000, 0) > A)                                    # True: spills into the next layer
print("B10 last cell", A % A)                                                      # 0, then (0 - 1) ** 0.5 is complex
print("B13 float layer", int((7_955_989 * A - 1000) / A))                          # 7955989, expected 7955988
```

### R2: candidate comparison and surface shares (Python)

Reproduces C.1 and C.2. It takes a few seconds.

```python
# R2
import math, random
A = 441_000_000_000_000
def corners(n):
    lt = (2 * n - 2) ** 2 + 1; rt = lt + 2 * n - 1; rb = rt + 2 * n - 1; lb = rb + 2 * n - 1
    return lt, rt, rb, lb
def p_of(y, z, top, bottom):
    n = max(y + 1, z + 1, -y, -z); lt, rt, rb, lb = corners(n)
    if n == -y: return lt if n == z + 1 else z + lb + n
    if n == y + 1: return rt + n - 1 - z
    if n == z + 1: return rt - n + 1 + y if top == "diagram" else rt - n - y
    return rb + n - 1 - y if bottom == "diagram" else rb + n - y
CANDIDATES = {"A": ("diagram", "diagram"), "B": ("encoder", "diagram"),
              "L": ("encoder", "encoder"), "C": ("diagram", "encoder")}
D = [[17, 18, 19, 20, 21, 22], [36, 5, 6, 7, 8, 23], [35, 16, 1, 2, 9, 24],
     [34, 15, 4, 3, 10, 25], [33, 14, 13, 12, 11, 26], [32, 31, 30, 29, 28, 27]]
for name, (t, b) in CANDIDATES.items():
    m = 40
    ps = [p_of(y, z, t, b) for y in range(-m, m) for z in range(-m, m)]
    bij = sorted(ps) == list(range(1, (2 * m) ** 2 + 1))
    seams = "n/a"
    if bij:
        where = {p_of(y, z, t, b): (y, z) for y in range(-m, m) for z in range(-m, m)}
        seams = sum(1 for p in range(1, (2 * m) ** 2) if abs(where[p][0] - where[p + 1][0]) + abs(where[p][1] - where[p + 1][1]) != 1)
    diag = sum(p_of(y, z, t, b) == D[2 - z][y + 3] for z in range(2, -4, -1) for y in range(-3, 3))
    print(name, "bijective:", bij, "collisions:", len(ps) - len(set(ps)), "diagram:", diag, "seams:", seams)
# A: True 0 36 39 | B: True 0 30 117 | L: False 39 24 n/a | C: False 39 30 n/a
R = 6378137.0; F = 1 / 298.257223563; E2 = (2 - F) * F
def ecef(lat, lon):
    rl = lat / 180 * math.pi; ro = lon / 180 * math.pi; s = math.sin(rl); c = math.cos(rl); N = R / math.sqrt(1 - E2 * s * s)
    return N * c * math.cos(ro), N * c * math.sin(ro), N * (1 - E2) * s
random.seed(7); n = 200_000; same = {k: [0, 0] for k in CANDIDATES}; sides = {"side": 0, "top": 0, "bottom": 0}
for _ in range(n):
    X, Y, Z = ecef(math.degrees(math.asin(random.uniform(-1, 1))), random.uniform(-180, 180))
    y, z = math.floor(Y), math.floor(Z); m = max(y + 1, z + 1, -y, -z)
    sides["side" if y in (-m, m - 1) else "top" if z == m - 1 else "bottom"] += 1
    enc, dec = p_of(y, z, "encoder", "encoder"), p_of(y, z, "diagram", "diagram")
    for k, (t, b) in CANDIDATES.items():
        v = p_of(y, z, t, b); same[k][0] += v == enc; same[k][1] += v == dec
print({k: f"{100 * v / n:.2f}%" for k, v in sides.items()})          # side 50.16%, top 24.82%, bottom 25.02%
for k, (e, d) in same.items():
    print(k, f"same as encoders {100 * e / n:.1f}%, same as decoders {100 * d / n:.1f}%")
# A 50.2% / 100.0% | B 75.0% / 75.2% | L 100.0% / 50.2% | C 75.2% / 75.0%
```

### R3: exhaustive bijection of candidate A for small cubes (Python)

Reproduces D.11. It takes about a minute.

```python
# R3
import math
def check(S):
    H, A = S // 2, S * S
    def corners(n):
        lt = (2 * n - 2) ** 2 + 1; rt = lt + 2 * n - 1; rb = rt + 2 * n - 1; return lt, rt, rb, rb + 2 * n - 1
    def enc(x, y, z):
        n = max(y + 1, z + 1, -y, -z); lt, rt, rb, lb = corners(n)
        if y == -n: p = lt if z == n - 1 else lb + n + z
        elif y == n - 1: p = rt + n - 1 - z
        elif z == n - 1: p = rt - n + 1 + y
        else: p = rb + n - 1 - y
        return (2 * x if x >= 0 else -2 * x - 1) * A + p
    def dec(c):
        l, r = divmod(c - 1, A); p = r + 1; n = math.isqrt(p - 1) // 2 + 1; lt, rt, rb, lb = corners(n)
        if p <= rt: y, z = p - rt + n - 1, n - 1
        elif p <= rb: y, z = n - 1, rt + n - 1 - p
        elif p < lb: y, z = rb + n - 1 - p, -n
        else: y, z = -n, p - lb - n
        return (l // 2 if l % 2 == 0 else -(l + 1) // 2), y, z
    seen = set()
    for x in range(-H, H):
        for y in range(-H, H):
            for z in range(-H, H):
                c = enc(x, y, z)
                if not 1 <= c <= S ** 3 or c in seen or dec(c) != (x, y, z): return False
                seen.add(c)
    return len(seen) == S ** 3
print(all(check(S) for S in range(2, 62, 2)))                         # True
```

### R4: JavaScript defects (Node)

Reproduces B1, B2, B6, B8 and B12.

```js
// R4
const R = 6378137, f = 1 / 298.257223563, e2 = 2 * f - f * f;
const gps = (la, lo, h) => { la *= Math.PI / 180; lo *= Math.PI / 180; const s = Math.sin(la), c = Math.cos(la), N = R / Math.sqrt(1 - e2 * s * s);
  return [(N + h) * c * Math.cos(lo), (N + h) * c * Math.sin(lo), (N * (1 - e2) + h) * s]; };
const fmt = (x, y, z) => { const k = 1e7, cx = Math.floor((x + R) * k), cy = Math.floor((y + R) * k), cz = Math.floor((z + R) * k);
  return (cx.toString().padStart(7, '0') + cy.toString().padStart(7, '0') + cz.toString().padStart(8, '0')).substring(0, 22); };
console.log('B1', fmt(...gps(51.5074, -0.1278, 0)), fmt(...gps(-51.5074, -0.1278, 0)));   // 1035613127381506369263 twice
const dec = (s) => { const k = 1e7, x = parseInt(s.slice(0, 7)) / k - R, y = parseInt(s.slice(7, 14)) / k - R, z = parseInt(s.slice(14)) / k - R;
  return [Math.atan2(z, Math.hypot(x, y) * 0.99330562) * 180 / Math.PI, Math.atan2(y, x) * 180 / Math.PI, Math.hypot(x, y, z) - R]; };
console.log('B2', dec('1234567890123456789012'), dec('9999999999999999999999'));           // both about (-35.446, -135.000, 4669116)
// B6: the legacy decoders (1cube2xyz.html 214-248) read the code with parseFloat
function decLegacy(str) { const cube = parseFloat(str), a = 441000000000000, cp = cube % a; const n = parseInt((((cp - 1) ** 0.5) / 2) + 1);
  const rt = (2 * (n - 1)) ** 2 + 2 * n, rb = rt + 2 * n - 1, lb = rb + 2 * n - 1; let Y, Z;
  if (cp >= rt && cp <= rb) Y = n; else if (cp >= lb) Y = -n + 1; else if (cp < rt) Y = cp - rt + n; else Y = rb - cp + n; Y -= 0.5;
  if (cp <= rt) Z = n - 1; else if (cp >= rb && cp <= lb) Z = -n; else if (cp < rb) Z = rt - cp + n - 1; else Z = cp - lb - n; Z += 0.5;
  const nl = parseInt(Math.floor(cube / a)) + 1; return [(nl % 2) !== 0 ? nl / 2 : -(nl - 1) / 2, Y, Z]; }
console.log('B6', decLegacy('3508590806758840271506'), 'expected [3977994.5, -8873.5, 4968874.5]');  // y = -206139.5
const cr = (v) => (v >= 0 ? parseInt(v) : parseInt(v) - 1);
console.log('B8', cr(6399593.6258 * Math.cos(Math.PI / 2)), cr(-3), cr(-2e-7));            // 3 -4 -3 (floor gives 0 -3 -1)
const pad = (x, n) => { const s = '000000000000' + x; return s.substr(s.length - n); };
console.log('B12', pad(Math.floor(7955988 * 441 + 999999999999 * 1e-12), 10) + pad(999999999999 % 1e12, 12)); // 3508590709999999999999
```

### R5: geodetic inverse accuracy (Python)

Reproduces the Bowring and `index.html` figures in D.11.

```python
# R5
import math, random
R = 6378137.0; F = 1 / 298.257223563; E2 = (2 - F) * F; B = R * (1 - F); EP2 = (R * R - B * B) / (B * B)
def fwd(lat, lon, h):
    rl = lat / 180 * math.pi; ro = lon / 180 * math.pi; s = math.sin(rl); c = math.cos(rl); N = R / math.sqrt(1 - E2 * s * s)
    return (N + h) * c * math.cos(ro), (N + h) * c * math.sin(ro), (N * (1 - E2) + h) * s
def bowring(X, Y, Z):
    p = math.hypot(X, Y); th = math.atan2(Z * R, p * B); st, ct = math.sin(th), math.cos(th)
    lat = math.atan2(Z + EP2 * B * st ** 3, p - E2 * R * ct ** 3); s, c = math.sin(lat), math.cos(lat)
    N = R / math.sqrt(1 - E2 * s * s)
    return math.degrees(lat), math.degrees(math.atan2(Y, X)), p * c + Z * s - R * R / N
def web(X, Y, Z):                                   # index.html 383-386
    return (math.degrees(math.atan2(Z, math.hypot(X, Y) * 0.99330562)), math.degrees(math.atan2(Y, X)),
            math.sqrt(X * X + Y * Y + Z * Z) - R)
random.seed(3)
for h in (0, 1000, 100_000, 1_000_000, 4_000_000):
    worst = {"bowring": 0, "web": 0}
    for _ in range(20000):
        lat = math.degrees(math.asin(random.uniform(-0.999, 0.999))); lon = random.uniform(-180, 180)
        e = fwd(lat, lon, h)
        for name, f in (("bowring", bowring), ("web", web)):
            worst[name] = max(worst[name], math.dist(e, fwd(*f(*e))))
    print(h, f"{worst['bowring']:.1e} m", f"{worst['web']:.0f} m")
# Bowring: 4.3e-09 | 1.1e-08 | 8.6e-05 | 6.7e-03 | 5.4e-02 m (sample maxima; another sample gave up to 1.5x more)
# index.html: 21331 | 21338 | 21341 | 21343 | 21375 m
```

### R6: running this repository's own code

Run these in a checkout of the branch:

```bash
python3 -B xyz2cube.py
```

It prints `3141592653589871375760` (B5).

```bash
python3 -B tests/test_spec.py -v
```

It reports `Ran 19 tests … OK (skipped=4)`.
