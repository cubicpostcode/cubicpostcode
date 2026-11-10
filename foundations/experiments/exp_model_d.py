#!/usr/bin/env python3
"""Model D: exhaustive finite verification (evidence for, not a proof of,
the all-j theorem in mathematics/21-double-shell-face-continuity.md)."""
import os
import random
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # works with python -I
from cubicshell import d_rank, d_unrank, step_type

J = 12                                    # double shells checked
K = 2 * J
N = (2 * K + 1) ** 3
prev, seen = None, set()
for n in range(N):
    p = d_unrank(n)
    k = max(map(abs, p))
    j = (k + 1) // 2
    assert n == 0 or (4 * j - 3) ** 3 <= n < (4 * j + 1) ** 3
    assert d_rank(*p) == n
    assert p not in seen
    seen.add(p)
    if prev is not None:
        assert step_type(prev, p) == 6, ("every step must be a face step", n)
    prev = p
assert len(seen) == N
rng = random.Random(20261110)
for _ in range(20000):
    n = rng.randrange(10 ** rng.randrange(1, 60))
    p, q = d_unrank(n), d_unrank(n + 1)
    assert d_rank(*p) == n and step_type(p, q) == 6
print(f"PASS Model D: bijection onto the radius-{K} cube ({N} cells), "
      f"every step a face step, every even-radius cube is a prefix; "
      f"20000 random big-rank round trips")
