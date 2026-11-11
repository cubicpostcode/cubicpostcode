#!/usr/bin/env python3
"""Investigation 3, Phase 1.2: read-only injectivity audit of the repository encoders.

Run from foundations/:  python3 -I experiments/exp_i3_encoder_audit.py

Nothing here modifies production code.  The JavaScript encoders are executed
from the exact bytes of the production files (sliced out of the HTML, not
re-typed), in Node.js; if `node` is unavailable those parts are skipped.

Encoders examined
  M3  calc/mobileGPS.html  (custom three-argument max(), called with four arguments)
  F   index.html           formatCubeCode / convertCubeToGPS
  P   xyz2cube.py          (repository root)
  L4  the four-argument formula published in the legacy site's website.html
      Python and calc/3xyz2cube.html (cubicpostcode.github.io); not in this
      repository, transcribed below for comparison only.
"""
import json
import shutil
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
A = 441_000_000_000_000
G = range(-60, 60)                       # the (y, z) window used in Investigation 2


def corners(n):
    lt = (2 * (n - 1)) ** 2 + 1
    rt = lt + 2 * n - 1
    rb = rt + 2 * n - 1
    return lt, rt, rb, rb + 2 * n - 1


def legacy_cp(y, z, n):
    """Branch structure shared by every legacy encoder, given a square number n."""
    lt, rt, rb, lb = corners(n)
    if n == -y:
        return lt if n == z + 1 else z + lb + n
    if n == y + 1:
        return rt + n - 1 - z
    if n == z + 1:
        return rt - n - y
    return rb + n - y


def l4(y, z):
    return legacy_cp(y, z, max(y + 1, z + 1, -y, -z))


def m3_transcribed(y, z):
    return legacy_cp(y, z, max(y + 1, z + 1, -y))       # what the page actually computes


def run_node(js):
    out = subprocess.run(["node", "-e", js], capture_output=True, text=True, check=True)
    return out.stdout


def mobile_gps_exact():
    """Exact production bytes from calc/mobileGPS.html, from coord_round to the padded string."""
    src = (ROOT / "calc" / "mobileGPS.html").read_text(encoding="utf-8")
    start = src.index("function coord_round(x) {")
    end = src.index("document.getElementById('cube-code').innerHTML = codeStr;")
    body = src[start:end]
    assert "max(my_y + 1, my_z + 1, -my_y, -my_z)" in body and "function max(v1, v2, v3)" in body
    js = (
        "function enc(X, Y, Z) { var res = [X, Y, Z];\n" + body +
        "\nreturn [codeStr, cube_p, slice_number]; }\n"
        "const out = [];\n"
        f"for (const x of [0, 1]) for (let y = {G.start}; y < {G.stop}; y++) for (let z = {G.start}; z < {G.stop}; z++)\n"
        "  out.push([x, y, z].concat(enc(x + 0.5, y + 0.5, z + 0.5)));\n"
        "console.log(JSON.stringify(out));"
    )
    return json.loads(run_node(js))


def index_html_exact():
    src = (ROOT / "index.html").read_text(encoding="utf-8")
    s = src.index("function formatCubeCode(x, y, z) {")
    e = src.index("function liveConvert()")
    fmt = src[s:e]
    js = fmt + (
        "\nconst cases = [[0,0,0],[0,0,1000],[0,0,-1000],[3977994.2,-8873.6,4968874.9],[3977994.2,-8873.6,-4968874.9]];\n"
        "console.log(JSON.stringify(cases.map(c => formatCubeCode(...c))));"
    )
    return json.loads(run_node(js))


def main():
    have_node = shutil.which("node") is not None

    # ---- M3: calc/mobileGPS.html, exact bytes -----------------------------------------
    if have_node:
        rows = mobile_gps_exact()
        layer0 = [r for r in rows if r[0] == 0]
        assert all(r[4] == m3_transcribed(r[1], r[2]) for r in rows), "transcription differs from page"
        print(f"PASS M3 transcription: the page's own bytes agree with max(y+1, z+1, -y) on {len(rows):,} cells "
              "(two layers); the fourth argument -z is ignored")
        cps = Counter(r[4] for r in layer0)
        nonpos = [r for r in layer0 if r[4] <= 0]
        strings = [r[3] for r in rows]
        print(f"OBSERVATION M3 on [-60,59]^2 (x = 0): {len(layer0):,} cells, {len(cps):,} distinct cube_p, "
              f"{len(layer0) - len(cps):,} excess, {len(nonpos)} cells with cube_p <= 0")
        bad_strings = sorted({s for s in strings if len(s) != 22 or not s.isdigit()})
        print(f"OBSERVATION M3 output strings that are not 22 digits: {len(bad_strings)}, e.g. {bad_strings[:3]}")
        by_code = defaultdict(list)
        for r in rows:
            by_code[r[3]].append(tuple(r[:3]))
        cross = [v for v in by_code.values() if len({p[0] for p in v}) > 1]
        print(f"OBSERVATION M3 identical full codes shared across the two layers x=0 and x=1: {len(cross)} codes, "
              f"e.g. {cross[0] if cross else None}")
        ex = {tuple(r[1:3]): r[3] for r in layer0}
        assert ex[(-1, -1)] == ex[(0, -2)] == "0000000000000000000004"
        print("PASS M3 reviewer witness: (y,z)=(-1,-1) and (0,-2) at x=0 both give 0000000000000000000004")
        assert ex[(-2, -2)] != ex[(-1, -2)]
        print(f"PASS M3 Investigation-2 pair refuted: (-2,-2) -> {ex[(-2, -2)][-2:]}, (-1,-2) -> {ex[(-1, -2)][-2:]}")
    else:
        print("SKIP M3 exact-bytes part (node not found); transcription-only checks follow")

    # ---- M3 structure, proved in the report and checked here --------------------------
    branch_reached = Counter()
    for y in G:
        for z in G:
            n = max(y + 1, z + 1, -y, -z)
            nn = max(y + 1, z + 1, -y)
            bottom_interior = z == -n and -n < y < n - 1
            assert (nn != n) == bottom_interior
            if bottom_interior:
                m = -y if y < 0 else y + 1
                want = 4 * m * m - m + 2 - n if y < 0 else 4 * m * m - 5 * m + 3 + n
                assert m3_transcribed(y, z) == want
            branch_reached[("else" if nn not in (-y, y + 1, z + 1) else "other")] += 1
            if not bottom_interior:
                assert m3_transcribed(y, z) == l4(y, z)
    assert branch_reached["else"] == 0
    print("PASS M3 structure: differs from the four-argument formula exactly on bottom-row interior cells; "
          "there cube_p = 4m^2-m+2-n (y<0, m=-y) or 4m^2-5m+3+n (y>=0, m=y+1); the bottom-row branch is dead code")
    for n in range(2, 60):
        v = m3_transcribed(0, -n)
        partner = [(y, z) for y in G for z in G if (y, z) != (0, -n) and m3_transcribed(y, z) == v]
        assert partner, n
    print("PASS M3 infinite witness family checked for n = 2..59: cell (0,-n) gets cube_p = n+2, "
          "which another cell of the same layer also gets")

    # ---- L4: four-argument legacy formula ---------------------------------------------
    vals = Counter(l4(y, z) for y in G for z in G)
    pairs = [(s, l4(-s, -s)) for s in range(2, 61) if l4(-s, -s) == l4(-s + 1, -s)]
    assert len(pairs) == 59 and all(v == 4 * s * s - 2 * s + 2 for s, v in pairs)
    print(f"OBSERVATION L4 (legacy site, four-argument): {len(vals):,} distinct of 14,400; "
          f"exactly the Investigation-2 pairs (-s,-s),(-s+1,-s) for s = 2..60 collide at 4s^2-2s+2")

    # ---- P: xyz2cube.py, real module -------------------------------------------------
    sys.path.insert(0, str(ROOT))
    import xyz2cube                                         # noqa: E402  (prints nothing on import)
    codes = Counter(xyz2cube.xyz_to_cube(0.5, y + 0.5, z + 0.5) for y in G for z in G)
    assert xyz2cube.xyz_to_cube(0.5, -0.5, 0.5) == xyz2cube.xyz_to_cube(0.5, -0.5, -0.5)
    pi = xyz2cube.xyz_to_cube(3561896.5, -8402969.5, -9767161.5)
    print(f"OBSERVATION P xyz2cube.py: {len(codes):,} distinct codes of 14,400 cells; (y,z)=(-1,0),(-1,-1) collide; "
          f"Pi example -> {pi} (published 3141592653589793238462)")

    # ---- F: index.html ----------------------------------------------------------------
    if have_node:
        f = index_html_exact()
        assert f[0] == f[1] == f[2] and f[3] == f[4]
        print(f"PASS F index.html exact bytes: formatCubeCode(0,0,0) = (0,0,+1000) = (0,0,-1000) = {f[0]}; "
              f"London ECEF with z and -z both -> {f[3]}")


if __name__ == "__main__":
    main()
