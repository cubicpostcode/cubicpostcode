"""Independent checks of the draft Cubic Postcode specification (docs/SPEC.md).

These tests import nothing from this repository. They check:

* the rules that every original source agrees on ("settled"), and
* mathematical facts about each candidate rule for the points that are still
  unresolved (decisions D1 to D5 in docs/SPEC.md), without choosing a candidate.

Tests that would need a decision are skipped with the reason "UNRESOLVED".

Run from anywhere:  python3 -B tests/test_spec.py -v
"""
import json
import math
import pathlib
import unittest

VECTORS = json.loads(
    pathlib.Path(__file__).with_name("spec_vectors.json").read_text(encoding="utf-8"))

SIDE = 21_000_000              # cubes along each edge of the giant cube
HALF = SIDE // 2               # cell indices run from -HALF to HALF - 1
LAYER_SIZE = SIDE * SIDE       # cubes in each X layer
MAX_CODE = SIDE * LAYER_SIZE   # 21 million cubed

# Published numbering, seen from Greenwich (legacy site images/bluecubestt.png).
# Rows are z = 2 .. -3 (north at the top), columns are y = -3 .. 2 (east to the right).
DIAGRAM = [
    [17, 18, 19, 20, 21, 22],
    [36, 5, 6, 7, 8, 23],
    [35, 16, 1, 2, 9, 24],
    [34, 15, 4, 3, 10, 25],
    [33, 14, 13, 12, 11, 26],
    [32, 31, 30, 29, 28, 27],
]


def diagram_cells():
    for row, z in enumerate(range(2, -4, -1)):
        for col, y in enumerate(range(-3, 3)):
            yield y, z, DIAGRAM[row][col]


# --- Settled rules (identical in the original encoders, decoders, diagram and prose) ---

def layer_of(x):
    return 2 * x if x >= 0 else -2 * x - 1


def x_of_layer(layer):
    return layer // 2 if layer % 2 == 0 else -(layer + 1) // 2


def square_of(y, z):
    return max(y + 1, z + 1, -y, -z)


def corners(n):
    left_top = (2 * (n - 1)) ** 2 + 1
    right_top = left_top + 2 * n - 1
    right_bottom = right_top + 2 * n - 1
    left_bottom = right_bottom + 2 * n - 1
    return left_top, right_top, right_bottom, left_bottom


def settled_position(y, z):
    """Position of (y, z) on its square, or None where it depends on D1/D2."""
    n = square_of(y, z)
    left_top, right_top, right_bottom, left_bottom = corners(n)
    if y == -n:                                   # left side and both left corners
        return left_top if z == n - 1 else left_bottom + n + z
    if y == n - 1:                                # right side and both right corners
        return right_top + n - 1 - z
    return None                                   # top/bottom-row interior: UNRESOLVED


def settled_code(x, y, z):
    p = settled_position(y, z)
    return None if p is None else f"{layer_of(x) * LAYER_SIZE + p:022d}"


# --- Candidate rules for the unresolved interiors (data to test facts about; no choice) ---

TOP = {
    "diagram": lambda n, y: corners(n)[1] - n + 1 + y,    # diagram and decoders
    "encoder": lambda n, y: corners(n)[1] - n - y,        # published encoders
}
BOTTOM = {
    "diagram": lambda n, y: corners(n)[2] + n - 1 - y,    # diagram and decoders
    "encoder": lambda n, y: corners(n)[2] + n - y,        # published encoders
}
CANDIDATES = {"A": ("diagram", "diagram"), "B": ("encoder", "diagram"), "L": ("encoder", "encoder")}


def candidate_position(name, y, z):
    p = settled_position(y, z)
    if p is not None:
        return p
    n = square_of(y, z)
    top, bottom = CANDIDATES[name]
    return TOP[top](n, y) if z == n - 1 else BOTTOM[bottom](n, y)


def candidate_code(name, x, y, z):
    return f"{layer_of(x) * LAYER_SIZE + candidate_position(name, y, z):022d}"


def original_coord_round(v):
    """coord_round as written in the original Python (legacy website.html 447-448)."""
    return int(v) if v >= 0 else int(v) - 1


def wgs84_to_ecef(lat_deg, lon_deg, h):
    """Forward WGS 84 conversion, in the operation order of the original calculators."""
    a = 6378137.0
    f = 1 / 298.257223563
    e2 = (2 - f) * f
    lat = lat_deg / 180 * math.pi
    lon = lon_deg / 180 * math.pi
    s, c = math.sin(lat), math.cos(lat)
    n = a / math.sqrt(1 - e2 * s * s)
    return ((n + h) * c * math.cos(lon), (n + h) * c * math.sin(lon), (n * (1 - e2) + h) * s)


def is_code(s):
    return isinstance(s, str) and len(s) == 22 and s.isascii() and s.isdigit() and 1 <= int(s) <= MAX_CODE


class TestVectorFile(unittest.TestCase):
    def test_vectors_well_formed(self):
        meta = VECTORS["meta"]["constants"]
        self.assertEqual((meta["SIDE"], meta["HALF"], meta["LAYER_SIZE"]), (SIDE, HALF, LAYER_SIZE))
        self.assertEqual(meta["MAX_CODE"], str(MAX_CODE))
        cells = [tuple(e["cell"]) for e in VECTORS["settled"]] + \
                [tuple(e["cell"]) for e in VECTORS["unresolved_d1_d2"]]
        self.assertEqual(len(cells), len(set(cells)), "a cell appears twice")
        for x, y, z in cells:
            for v in (x, y, z):
                self.assertTrue(-HALF <= v < HALF)
        codes = [e["code"] for e in VECTORS["settled"]]
        self.assertEqual(len(codes), len(set(codes)), "a code appears twice")
        for code in codes:
            self.assertTrue(is_code(code), code)
        for entry in VECTORS["unresolved_d1_d2"]:
            for code in entry["candidates"].values():
                self.assertTrue(is_code(code), code)


class TestCapacity(unittest.TestCase):
    def test_capacity(self):
        self.assertEqual(MAX_CODE, 21_000_000 ** 3)
        self.assertLess(MAX_CODE, 10 ** 22)
        self.assertEqual(len(str(MAX_CODE)), 22)
        r = VECTORS["code_range"]
        self.assertEqual(settled_code(*r["first"]["cell"]), r["first"]["code"])
        self.assertEqual(settled_code(*r["last"]["cell"]), r["last"]["code"])
        self.assertEqual(int(r["first"]["code"]), 1)
        self.assertEqual(int(r["last"]["code"]), MAX_CODE)
        for s in r["not_a_cube"]:
            self.assertEqual(len(s), 22)
            self.assertFalse(is_code(s), s)


class TestLayers(unittest.TestCase):
    def test_layer_map_bijective(self):
        xs = range(-1000, 1000)
        self.assertEqual(sorted(layer_of(x) for x in xs), list(range(2000)))
        for x in xs:
            self.assertEqual(x_of_layer(layer_of(x)), x)
        self.assertEqual(layer_of(0), 0)                # first layer: x in [0, 1)
        self.assertEqual(layer_of(-1), 1)               # second layer: x in [-1, 0)
        self.assertEqual(layer_of(HALF - 1), SIDE - 2)  # front face, nearest Greenwich
        self.assertEqual(layer_of(-HALF), SIDE - 1)     # back face, the last layer


class TestSquares(unittest.TestCase):
    M = 60

    def test_square_partition(self):
        counts = {}
        for y in range(-self.M, self.M):
            for z in range(-self.M, self.M):
                n = square_of(y, z)
                counts[n] = counts.get(n, 0) + 1
        self.assertEqual(sorted(counts), list(range(1, self.M + 1)))
        for n, count in counts.items():
            self.assertEqual(count, 8 * n - 4)
            left_top, right_top, right_bottom, left_bottom = corners(n)
            self.assertEqual(left_top, (2 * n - 2) ** 2 + 1)
            self.assertEqual(left_bottom + 2 * n - 2, (2 * n) ** 2)

    def test_open_slots(self):
        """Settled positions leave exactly the top and bottom slots for the open interiors."""
        for n in range(1, self.M + 1):
            left_top, right_top, right_bottom, left_bottom = corners(n)
            cells = [(y, z) for y in range(-n, n) for z in range(-n, n) if square_of(y, z) == n]
            placed = [settled_position(y, z) for y, z in cells]
            known = [p for p in placed if p is not None]
            self.assertEqual(len(known), len(set(known)))
            self.assertEqual(len(known), 4 * n)
            top_slots = set(range(left_top + 1, right_top))
            bottom_slots = set(range(right_bottom + 1, left_bottom))
            all_positions = set(range(left_top, (2 * n) ** 2 + 1))
            self.assertEqual(all_positions - set(known), top_slots | bottom_slots)
            open_cells = [c for c, p in zip(cells, placed) if p is None]
            self.assertEqual(sum(1 for y, z in open_cells if z == n - 1), len(top_slots))
            self.assertEqual(sum(1 for y, z in open_cells if z == -n), len(bottom_slots))


class TestSettled(unittest.TestCase):
    def test_settled_vectors(self):
        for entry in VECTORS["settled"]:
            with self.subTest(cell=entry["cell"]):
                self.assertEqual(settled_code(*entry["cell"]), entry["code"])

    def test_published_diagram_settled_cells(self):
        open_cells = 0
        for y, z, number in diagram_cells():
            p = settled_position(y, z)
            if p is None:
                open_cells += 1
            else:
                self.assertEqual(p, number, (y, z))
        self.assertEqual(open_cells, 12)

    def test_decode_layer_and_position(self):
        for entry in VECTORS["settled"]:
            x, y, z = entry["cell"]
            layer, rest = divmod(int(entry["code"]) - 1, LAYER_SIZE)
            position = rest + 1
            with self.subTest(cell=entry["cell"]):
                self.assertEqual(x_of_layer(layer), x)
                self.assertEqual(position, settled_position(y, z))
                self.assertEqual(math.isqrt(position - 1) // 2 + 1, square_of(y, z))


class TestCandidateFacts(unittest.TestCase):
    """Facts about each candidate rule. None of these tests selects a candidate."""

    def test_candidate_facts(self):
        for n in range(2, 61):
            left_top, right_top, right_bottom, left_bottom = corners(n)
            interior = range(-n + 1, n - 1)
            for name, rule in TOP.items():
                self.assertEqual({rule(n, y) for y in interior}, set(range(left_top + 1, right_top)), name)
            self.assertEqual({BOTTOM["diagram"](n, y) for y in interior},
                             set(range(right_bottom + 1, left_bottom)))
            encoder_bottom = [BOTTOM["encoder"](n, y) for y in interior]
            self.assertEqual(BOTTOM["encoder"](n, -n + 1), settled_position(-n, -n))   # collides
            self.assertNotIn(right_bottom + 1, encoder_bottom)                          # never used

    def test_candidates_on_squares_1_to_40(self):
        m = 40
        for name, bijective in (("A", True), ("B", True), ("L", False)):
            positions = [candidate_position(name, y, z) for y in range(-m, m) for z in range(-m, m)]
            self.assertEqual(sorted(positions) == list(range(1, (2 * m) ** 2 + 1)), bijective, name)

    def test_candidate_vectors(self):
        for entry in VECTORS["unresolved_d1_d2"]:
            with self.subTest(cell=entry["cell"]):
                self.assertIsNone(settled_position(*entry["cell"][1:]))
                for name, code in entry["candidates"].items():
                    self.assertEqual(candidate_code(name, *entry["cell"]), code)

    def test_diagram_agreement_counts(self):
        agree = {name: sum(candidate_position(name, y, z) == number for y, z, number in diagram_cells())
                 for name in CANDIDATES}
        self.assertEqual(agree, {"A": 36, "B": 30, "L": 24})


class TestUnresolvedData(unittest.TestCase):
    """The unresolved groups record facts; they do not choose."""

    def test_d3_points_record_both_conventions(self):
        for entry in VECTORS["unresolved_d3"]["points"]:
            point = entry["point"]
            self.assertEqual(entry["floor_cell"], [math.floor(v) for v in point])
            self.assertEqual(entry["coord_round_cell"], [original_coord_round(v) for v in point])
            self.assertEqual(settled_code(*entry["floor_cell"]), entry["floor_code"])
            self.assertEqual(settled_code(*entry["coord_round_cell"]), entry["coord_round_code"])
            differs = [v < 0 and v == int(v) for v in point]
            self.assertEqual([a != b for a, b in zip(entry["floor_cell"], entry["coord_round_cell"])], differs)

    def test_d4_unchecked_formulas_leave_the_cube(self):
        for entry in VECTORS["unresolved_d4"]:
            x, y, z = entry["cell"]
            inside = all(-HALF <= v < HALF for v in (x, y, z))
            self.assertFalse(inside)
            if not -HALF <= y < HALF:
                p = settled_position(y, z)
                self.assertGreater(p, LAYER_SIZE)         # spills into another layer
                code = layer_of(x) * LAYER_SIZE + p
                self.assertEqual(f"{code:022d}", entry["unchecked_code"])
                self.assertEqual(x_of_layer((code - 1) // LAYER_SIZE), entry["unchecked_code_falls_in_layer_of_x"])
            else:
                code = layer_of(x) * LAYER_SIZE + settled_position(y, z)
                self.assertEqual(str(code).zfill(22), entry["unchecked_code"])
                self.assertGreater(code, MAX_CODE)


class TestGeodesy(unittest.TestCase):
    def test_gps_cells(self):
        # Every vector lies at least 1 mm from a cell boundary, so it does not depend on D3 or D7.
        for entry in VECTORS["gps_cells"]:
            ecef = wgs84_to_ecef(entry["lat"], entry["lon"], entry["h"])
            with self.subTest(place=entry["why"]):
                self.assertEqual([math.floor(v) for v in ecef], entry["cell"])
                margin = min(min(v - math.floor(v), math.floor(v) + 1 - v) for v in ecef)
                self.assertGreaterEqual(margin, 1e-3)


class TestUnresolved(unittest.TestCase):
    """Placeholders for checks that need the inventor's decision (docs/SPEC.md, section 10)."""

    @unittest.skip("UNRESOLVED D1/D2: top/bottom-row interiors await the inventor, see docs/SPEC.md")
    def test_unresolved_d1_d2(self):
        raise NotImplementedError("After D1/D2 are decided, assert encode and decode against the chosen candidate.")

    @unittest.skip("UNRESOLVED D3: cell of an exact negative integer coordinate, see docs/SPEC.md")
    def test_unresolved_d3(self):
        raise NotImplementedError("After D3 is decided, assert the chosen cell for every unresolved_d3 entry.")

    @unittest.skip("UNRESOLVED D4: points outside the 21 million metre cube, see docs/SPEC.md")
    def test_unresolved_d4(self):
        raise NotImplementedError("After D4 is decided, assert the chosen behaviour for every unresolved_d4 entry.")

    @unittest.skip("UNRESOLVED D5: accepted input forms, see docs/SPEC.md")
    def test_unresolved_d5(self):
        raise NotImplementedError("After D5 is decided, assert acceptance or rejection of every unresolved_d5 input.")


if __name__ == "__main__":
    unittest.main()
