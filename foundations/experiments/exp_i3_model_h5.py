#!/usr/bin/env python3
"""Investigation 3: verification of Model H5 and locality comparison with Models C and D.

Run from foundations/:  python3 -I experiments/exp_i3_model_h5.py      (about 1-2 minutes)

Part 1 (Model H5, level 3 = the radius-62 cube, 1,953,125 cells, exhaustive):
  bijection onto B_3; every step a face step; B_0, B_1, B_2 are prefixes;
  every aligned 5-block and 25-block (centred on 5Z^3 / 25Z^3) occupies one
  rank interval aligned to a multiple of 125 / 15,625; rank inverts unrank;
  plus random round trips for ranks up to 125^40.

Part 2 (locality, OBSERVATION, same 1,953,125 cells for C, D and H5, all three
  enumerate exactly this cube as their first 125^3 ranks):
  - forward Hoelder ratio  max |p(n+d) - p(n)|_inf^3 / d  over d = 2^i (all n);
  - backward locality: rank gaps between face-adjacent cells (max, median,
    share above 1% of the cube).
"""
from array import array
from pathlib import Path
import random
import statistics
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cubicshell as cs   # noqa: E402
import radix5 as h5       # noqa: E402

R = 62
S = 2 * R + 1
N = S ** 3


def table(unrank):
    xs, ys, zs = array("i"), array("i"), array("i")
    for n in range(N):
        x, y, z = unrank(n)
        xs.append(x); ys.append(y); zs.append(z)
    return xs, ys, zs


def idx(x, y, z):
    return ((x + R) * S + (y + R)) * S + (z + R)


def check_h5(xs, ys, zs):
    rk = array("q", [-1]) * N
    for n in range(N):
        i = idx(xs[n], ys[n], zs[n])
        assert -R <= xs[n] <= R and -R <= ys[n] <= R and -R <= zs[n] <= R
        assert rk[i] == -1
        rk[i] = n
    for n in range(N - 1):
        d = abs(xs[n + 1] - xs[n]) + abs(ys[n + 1] - ys[n]) + abs(zs[n + 1] - zs[n])
        assert d == 1, n
    for t, r in ((0, 0), (1, 2), (2, 12)):
        assert all(max(abs(xs[n]), abs(ys[n]), abs(zs[n])) <= r for n in range(125 ** t))
    for side, block in ((5, 125), (25, 125 ** 2)):
        half = side // 2
        owner = {}
        for n in range(N):
            key = ((xs[n] + half) // side, (ys[n] + half) // side, (zs[n] + half) // side)
            assert owner.setdefault(key, n // block) == n // block, (side, n)
        assert len(owner) == N // block
    for n in range(0, N, 7):
        assert h5.rank(xs[n], ys[n], zs[n]) == n
    rnd = random.Random(3)
    for _ in range(2000):
        n = rnd.randrange(125 ** 40)
        assert h5.rank(*h5.unrank(n)) == n
    for _ in range(2000):
        p = tuple(rnd.randrange(-10 ** 25, 10 ** 25) for _ in range(3))
        assert h5.unrank(h5.rank(*p)) == p
    return rk


def ranks(xs, ys, zs):
    rk = array("q", [0]) * N
    for n in range(N):
        rk[idx(xs[n], ys[n], zs[n])] = n
    return rk


def locality(name, xs, ys, zs, rk):
    hold = []
    d = 1
    while d < N // 2:
        m = 0
        for n in range(0, N - d):
            j = n + d
            c = max(abs(xs[j] - xs[n]), abs(ys[j] - ys[n]), abs(zs[j] - zs[n]))
            if c > m:
                m = c
        hold.append((d, m, m ** 3 / d))
        d *= 4
    gaps = []
    for x in range(-R, R + 1):
        for y in range(-R, R + 1):
            for z in range(-R, R + 1):
                i = idx(x, y, z)
                if x < R:
                    gaps.append(abs(rk[i] - rk[idx(x + 1, y, z)]))
                if y < R:
                    gaps.append(abs(rk[i] - rk[idx(x, y + 1, z)]))
                if z < R:
                    gaps.append(abs(rk[i] - rk[idx(x, y, z + 1)]))
    big = sum(1 for g in gaps if g > N // 100) / len(gaps)
    print(f"  {name}: Hoelder ratio max_n |p(n+d)-p(n)|^3/d for d=1,4,16,...: "
          + ", ".join(f"{r:.1f}" for _, _, r in hold))
    print(f"  {name}: face-neighbour rank gaps: max {max(gaps):,}, median {statistics.median(gaps):,.0f}, "
          f"share above 1% of the cube {100 * big:.1f}%")


def main():
    hx = table(h5.unrank)
    rk = check_h5(*hx)
    print(f"PASS H5: {N:,} cells = the radius-{R} cube B_3, each once; every step a face step; "
          "B_0, B_1, B_2 are prefixes; every aligned 5-block and 25-block is one aligned rank interval; "
          "rank inverts unrank; 4,000 random big round trips")
    print("OBSERVATION locality on the same cube (Chebyshev distance):")
    locality("H5", *hx, rk)
    for name, un in (("C", cs.c_unrank), ("D", cs.d_unrank)):
        t = table(un)
        locality(name, *t, ranks(*t))


if __name__ == "__main__":
    main()
