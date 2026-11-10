#!/usr/bin/env python3
"""Model C: exhaustive finite verification (evidence for, not a proof of,
the all-k theorem in mathematics/20-one-break-shell-traversal.md)."""
import os
import random
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # works with python -I
from collections import Counter
from cubicshell import c_rank, c_unrank, step_type, icbrt

K = 24                                    # cube radius checked exhaustively
N = (2 * K + 1) ** 3
prev, seen = None, set()
breaks = Counter()
for n in range(N):
    p = c_unrank(n)
    k = max(map(abs, p))
    assert (2 * k - 1) ** 3 <= n < (2 * k + 1) ** 3 or (n == 0 and k == 0)
    assert c_rank(*p) == n
    assert p not in seen
    seen.add(p)
    if prev is not None:
        t = step_type(prev, p)
        kp = max(map(abs, prev))
        if kp != k:
            assert t == 6, ("shell boundary step must be a face step", n)
        elif t != 6:
            assert t == 18, ("the only non-face step is an edge diagonal", n)
            assert n - (2 * k - 1) ** 3 == (2 * k + 1) ** 2
            assert sum(prev) % 2 == sum(p) % 2 == k % 2
            breaks[k] += 1
    prev = p
assert len(seen) == N
# Each horizontal slice of each shell is visited in planar-spiral order or in
# its exact reverse (weak planar consistency), and consecutively.
from cubicshell import spiral_rank
for k in range(1, 9):
    base, planes = (2 * k - 1) ** 3, {}
    for q in range(24 * k * k + 2):
        x, y, z = c_unrank(base + q)
        planes.setdefault(z, []).append((q, spiral_rank(x, y)))
    for z, lst in planes.items():
        qs, rs = [a for a, _ in lst], [b for _, b in lst]
        assert qs == list(range(qs[0], qs[0] + len(qs)))
        assert rs == sorted(rs) or rs == sorted(rs, reverse=True)
assert all(breaks[k] == 1 for k in range(1, K + 1)) and len(breaks) == K

rng = random.Random(20261110)
for _ in range(20000):                    # huge ranks, round trip + steps
    n = rng.randrange(10 ** rng.randrange(1, 60))
    p, q = c_unrank(n), c_unrank(n + 1)
    assert c_rank(*p) == n and step_type(p, q) in (6, 18)
for n in (10 ** 22 - 1, 10 ** 400):
    assert c_rank(*c_unrank(n)) == n and icbrt(n) ** 3 <= n < (icbrt(n) + 1) ** 3
print(f"PASS Model C: bijection onto the radius-{K} cube ({N} cells), "
      f"shell-monotone, exactly one edge-diagonal step per shell, "
      f"face steps elsewhere; 20000 random big-rank round trips")
