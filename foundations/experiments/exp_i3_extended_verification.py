#!/usr/bin/env python3
"""Investigation 3, Phase 1.1: extended verification of Models C and D.

Run from foundations/:  python3 -I experiments/exp_i3_extended_verification.py

Extends the reviewer's radius-10 audit (exp_review_i2_independent.py):

1. A third, independent spiral: a "turtle walk" (step forward, turn left
   whenever the cell on the left is unvisited) instead of explicit loops.
2. Models C and D rebuilt from the phase tables of files 20/21 on top of that
   walk, compared exhaustively with cubicshell.py on the radius-30 cube
   (226,981 cells), in both directions.
3. Location checks: in C the single edge-diagonal step of shell k is exactly
   the cap -> first-ring step; every shell starts and ends on the z-axis;
   in D every block boundary falls at (4j-3)^3 and every even-radius cube is
   a prefix.
4. Large integers far beyond float range (ranks up to ~10^1000, coordinates
   up to ~10^300): shell/block boundary ranks, round trips, and the step type
   across each boundary.
5. icbrt against an independent binary-search cube root, at perfect cubes
   and their neighbours, up to 3,000-bit inputs.

Standard library only.  The reference module is imported only after the
independent tables are built.
"""
from collections import Counter
from pathlib import Path
import random
import sys


def turtle_spiral(radius):
    """Planar spiral from the origin by the left-turn rule (orientation of file 20)."""
    left = {(1, 0): (0, 1), (0, 1): (-1, 0), (-1, 0): (0, -1), (0, -1): (1, 0)}
    pos, heading = (0, 0), (1, 0)
    seen, out = {pos}, [pos]
    total = (2 * radius + 1) ** 2
    first = True
    while len(out) < total:
        lx, ly = left[heading]
        cand = (pos[0] + lx, pos[1] + ly)
        if not first and cand not in seen:
            heading = (lx, ly)
        first = False
        pos = (pos[0] + heading[0], pos[1] + heading[1])
        seen.add(pos)
        out.append(pos)
    return out


def build_c(radius, spiral):
    cells = [(0, 0, 0)]
    for k in range(1, radius + 1):
        cap = spiral[:(2 * k + 1) ** 2]
        ring = spiral[(2 * k - 1) ** 2:(2 * k + 1) ** 2]
        shell = [(x, y, k) for x, y in cap]
        for i in range(2 * k - 1):
            seq = ring if i % 2 == 0 else ring[::-1]
            shell += [(x, y, k - 1 - i) for x, y in seq]
        shell += [(x, y, -k) for x, y in cap[::-1]]
        cells += [(x, y, w if k % 2 else -w) for x, y, w in shell]
    return cells


def build_d(radius, spiral):
    assert radius % 2 == 0
    cells = [(0, 0, 0)]
    for j in range(1, radius // 2 + 1):
        a, b = 2 * j - 1, 2 * j
        m, j0 = (2 * b + 1) ** 2, (2 * a - 1) ** 2
        sq = spiral[:m]
        blk = []
        for c in range(j0):                                    # T1 ladder
            x, y = sq[c]
            blk += [(x, y, a), (x, y, b)] if c % 2 == 0 else [(x, y, b), (x, y, a)]
        blk += [(x, y, b) for x, y in sq[j0:]]                 # T2
        blk += [(x, y, a) for x, y in sq[j0:][::-1]]           # T3
        ann = sq[j0:]
        for i, w in enumerate(range(b - 2, -b + 1, -1)):       # M
            blk += [(x, y, w) for x, y in (ann if i % 2 == 0 else ann[::-1])]
        lad = []
        for c in range(m):                                     # B = reversed ladder
            x, y = sq[c]
            lad += [(x, y, -b), (x, y, -b + 1)] if c % 2 == 0 else [(x, y, -b + 1), (x, y, -b)]
        blk += lad[::-1]
        cells += [(x, y, w if j % 2 else -w) for x, y, w in blk]
    return cells


def kind(p, q):
    return tuple(sorted(abs(u - v) for u, v in zip(p, q)))


def cheb(p):
    return max(abs(v) for v in p)


def icbrt_bisect(n):
    lo, hi = 0, 1 << (n.bit_length() // 3 + 2)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if mid ** 3 <= n:
            lo = mid
        else:
            hi = mid - 1
    return lo


def main():
    R = 30
    spiral = turtle_spiral(R + 1)
    c_cells, d_cells = build_c(R, spiral), build_d(R, spiral)
    cube = (2 * R + 1) ** 3
    for name, cells in (("C", c_cells), ("D", d_cells)):
        assert len(cells) == len(set(cells)) == cube, name
        assert all(cheb(p) <= R for p in cells), name

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import cubicshell as ref                          # imported only now

    assert [ref.spiral_unrank(q) for q in range(len(spiral))] == spiral
    for q, (x, y) in enumerate(spiral):
        assert ref.spiral_rank(x, y) == q
    print(f"PASS turtle-walk spiral = reference spiral on {len(spiral)} cells (radius {R + 1})")

    for name, cells, rank, unrank in (("C", c_cells, ref.c_rank, ref.c_unrank),
                                      ("D", d_cells, ref.d_rank, ref.d_unrank)):
        for n, p in enumerate(cells):
            assert unrank(n) == p, (name, n, p, unrank(n))
            assert rank(*p) == n, (name, n, p, rank(*p))
        print(f"PASS {name}: {cube:,} cells of the radius-{R} cube, each exactly once; "
              f"rank and unrank inverse at every rank")

    # Model C: one edge diagonal per shell, at the cap -> first ring junction.
    diag_at = [n for n in range(cube - 1) if kind(c_cells[n], c_cells[n + 1]) == (0, 1, 1)]
    other = Counter(kind(c_cells[n], c_cells[n + 1]) for n in range(cube - 1)) - Counter({(0, 1, 1): len(diag_at)})
    assert set(other) == {(0, 0, 1)}, other
    expected = [(2 * k - 1) ** 3 + (2 * k + 1) ** 2 - 1 for k in range(1, R + 1)]
    assert diag_at == expected, (diag_at[:5], expected[:5])
    for k in range(1, R + 1):
        s, e = (2 * k - 1) ** 3, (2 * k + 1) ** 3 - 1
        sgn = 1 if k % 2 else -1
        assert c_cells[s] == (0, 0, sgn * k) and c_cells[e] == (0, 0, -sgn * k)
        assert {cheb(c_cells[n]) for n in (s, e)} == {k}
        if s > 0:
            assert cheb(c_cells[s - 1]) == k - 1 and kind(c_cells[s - 1], c_cells[s]) == (0, 0, 1)
    print(f"PASS C: exactly one edge-diagonal step per shell, always the cap->first-ring step "
          f"(rank (2k-1)^3+(2k+1)^2-1); every shell runs axis to axis; shell-to-shell steps are face steps")

    # Model D: all face steps; prefixes; block boundaries.
    assert all(kind(d_cells[n], d_cells[n + 1]) == (0, 0, 1) for n in range(cube - 1))
    for r in range(R + 1):
        pref = {p for p in d_cells[:(2 * r + 1) ** 3]}
        is_cube = all(cheb(p) <= r for p in pref)
        assert is_cube == (r % 2 == 0), r
    for j in range(1, R // 2 + 1):
        s = (4 * j - 3) ** 3
        assert d_cells[s] == (0, 0, (1 if j % 2 else -1) * (2 * j - 1))
    print("PASS D: every step a face step; the radius-r cube is a prefix exactly for even r <= 30; "
          "blocks start at rank (4j-3)^3 on the axis")

    # Large integers.
    rnd = random.Random(20261110)
    for k in [10 ** e + d for e in (20, 80, 200, 333) for d in (0, 1, 7)]:
        s, e = (2 * k - 1) ** 3, (2 * k + 1) ** 3 - 1
        for n in (s - 1, s, s + (2 * k + 1) ** 2 - 1, s + (2 * k + 1) ** 2, e, e + 1):
            p = ref.c_unrank(n)
            assert ref.c_rank(*p) == n
        assert cheb(ref.c_unrank(s - 1)) == k - 1 and cheb(ref.c_unrank(s)) == k == cheb(ref.c_unrank(e))
        assert kind(ref.c_unrank(s - 1), ref.c_unrank(s)) == (0, 0, 1)
        d1 = s + (2 * k + 1) ** 2 - 1
        assert kind(ref.c_unrank(d1), ref.c_unrank(d1 + 1)) == (0, 1, 1)
        if k % 2 == 0:
            j = k // 2
            s = (4 * j - 3) ** 3
            for n in (s - 1, s, (4 * j + 1) ** 3 - 1):
                assert ref.d_rank(*ref.d_unrank(n)) == n
            assert kind(ref.d_unrank(s - 1), ref.d_unrank(s)) == (0, 0, 1)
            assert cheb(ref.d_unrank((4 * j + 1) ** 3 - 1)) == 2 * j
            assert cheb(ref.d_unrank((4 * j + 1) ** 3)) == 2 * j + 1
    for digits in (30, 309, 400, 1000):
        for _ in range(300):
            n = rnd.randrange(10 ** digits)
            assert ref.c_rank(*ref.c_unrank(n)) == n
            assert ref.d_rank(*ref.d_unrank(n)) == n
            assert kind(ref.c_unrank(n), ref.c_unrank(n + 1)) in {(0, 0, 1), (0, 1, 1)}
            assert kind(ref.d_unrank(n), ref.d_unrank(n + 1)) == (0, 0, 1)
    for _ in range(500):
        p = tuple(rnd.randrange(-10 ** 300, 10 ** 300) for _ in range(3))
        assert ref.c_unrank(ref.c_rank(*p)) == p
        assert ref.d_unrank(ref.d_rank(*p)) == p
    print("PASS large integers: boundary ranks at shells k ~ 10^20..10^333, random ranks up to 10^1000 "
          "(beyond float range), random cells up to 10^300; steps across every tested boundary as specified")

    for bits in list(range(1, 200)) + [512, 1024, 2048, 3000]:
        for _ in range(3):
            r = rnd.getrandbits(bits) | 1
            for n in (r ** 3 - 1, r ** 3, r ** 3 + 1, rnd.getrandbits(3 * bits)):
                if n >= 0:
                    assert ref.icbrt(n) == icbrt_bisect(n), n
    print("PASS icbrt = independent bisection cube root at perfect cubes, neighbours and random inputs up to 9,000 bits")


if __name__ == "__main__":
    main()
