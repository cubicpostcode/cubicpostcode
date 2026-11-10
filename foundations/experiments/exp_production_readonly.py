#!/usr/bin/env python3
"""READ-ONLY observation of the encoders that exist on this branch (OP-3).

Nothing here changes production code.  Two (y,z) -> in-layer-index maps are
compared on the square [-R, R-1]^2:

  legacy   transcription of calc/mobileGPS.html (ring = max(y+1, z+1, -y, -z))
  python   the repository-root xyz2cube.py      (ring = max(|y|,|z|) + 1)
"""
import importlib.util
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")


def legacy_index(y, z):
    sq = max(y + 1, z + 1, -y, -z)
    left_top = (2 * (sq - 1)) ** 2 + 1
    right_top = left_top + 2 * sq - 1
    right_bottom = right_top + 2 * sq - 1
    left_bottom = right_bottom + 2 * sq - 1
    if sq == -y:
        return left_top if sq == z + 1 else z + left_bottom + sq
    if sq == y + 1:
        return right_top + sq - 1 - z
    if sq == z + 1:
        return right_top - sq - y
    return right_bottom + sq - y


R = 60
cells = [(y, z) for y in range(-R, R) for z in range(-R, R)]
idx = {c: legacy_index(*c) for c in cells}
hits = {}
for c, v in idx.items():
    hits.setdefault(v, []).append(c)
dups = {v: cs for v, cs in hits.items() if len(cs) > 1}
missing = [v for v in range(1, (2 * R) ** 2 + 1) if v not in hits]
# Observed structure: for every ring s >= 2 the two cells (-s,-s) and
# (-s+1,-s) share the index (2s)^2 - 2s + 2, and (2s)^2 - 4s + 4 is unused.
assert dups == {(2 * s) ** 2 - 2 * s + 2: [(-s, -s), (-s + 1, -s)]
                for s in range(2, R + 1)}
assert missing == [(2 * s) ** 2 - 4 * s + 4 for s in range(2, R + 1)]
assert max(idx.values()) == (2 * R) ** 2 and min(idx.values()) == 1
print(f"OBSERVATION legacy calc/mobileGPS.html in-layer map on "
      f"[-{R},{R - 1}]^2: {len(dups)} colliding pairs, one per ring s>=2: "
      f"(-s,-s) and (-s+1,-s) both -> 4s^2-2s+2; index 4s^2-4s+4 unused")
print("  ring 2 as printed by the legacy formula (rows z=1..-2, cols y=-2..1):")
for z in range(1, -3, -1):
    print("   ", " ".join(f"{idx[(y, z)]:3d}" for y in range(-2, 2)))

spec = importlib.util.spec_from_file_location(
    "xyz2cube", os.path.join(ROOT, "xyz2cube.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
py = {c: int(mod.xyz_to_cube(0.5, c[0] + 0.5, c[1] + 0.5)) for c in cells}
distinct = len(set(py.values()))
agree = sum(py[c] == idx[c] for c in cells)
print(f"OBSERVATION root xyz2cube.py on the same {len(cells)} cells: "
      f"{distinct} distinct codes ({len(cells) - distinct} collisions); "
      f"agrees with the legacy map on {agree} cells")
print("  example: (y,z)=(-1,0) and (-1,-1) ->",
      py[(-1, 0)], py[(-1, -1)], "| legacy ->", idx[(-1, 0)], idx[(-1, -1)])
print("  coord_round(-2.0) =", mod.coord_round(-2.0),
      "(floor would give -2)")
