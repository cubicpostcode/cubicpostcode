#!/usr/bin/env python3
"""Checks around the cap-centre obstruction and its generalisations.
Finite corroboration only; proofs are in mathematics/11-*."""
import itertools
import os
import random
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # python -I
from cubicshell import ring_cell, spiral_unrank


def cheb(p, q=None):
    return max(abs(u - (0 if q is None else v))
               for u, v in zip(p, q or p))


def shell(k, d=3):
    r = range(-k, k + 1)
    return [p for p in itertools.product(r, repeat=d) if cheb(p) == k]


# (a) local-minimum lemma on random orderings: breaks >= local minima - 1
rng = random.Random(1)
for k in (1, 2):
    cells = shell(k)
    for _ in range(300):
        rng.shuffle(cells)
        pos = {p: i for i, p in enumerate(cells)}
        nb = lambda p: [q for q in cells if cheb(p, q) == 1]
        minima = sum(all(pos[q] > pos[p] for q in nb(p)) for p in cells)
        breaks = sum(cheb(cells[i], cells[i + 1]) != 1
                     for i in range(len(cells) - 1))
        assert breaks >= minima - 1

# (b) every facet centre of S_k (k >= 2) in dimension d = 2, 3, 4 has all its
#     king-neighbours inside its own facet
for d in (2, 3, 4):
    for k in range(2, 7):
        for axis in range(d):
            for sgn in (1, -1):
                c = tuple(sgn * k if i == axis else 0 for i in range(d))
                for delta in itertools.product((-1, 0, 1), repeat=d):
                    q = tuple(u + v for u, v in zip(c, delta))
                    if q != c and cheb(q) == k:
                        assert q[axis] == sgn * k

# (c) quantitative form: the nearest shell cell outside the cap is at
#     Chebyshev distance exactly k from the cap centre
for k in range(1, 9):
    c = (0, 0, k)
    assert min(cheb(c, q) for q in shell(k) if q[2] != k) == k


# (d) the plane-sequential order (spiral in every horizontal plane, planes
#     taken from z = +k down to z = -k) is fully planar consistent and has
#     exactly one non-26-adjacent step for k >= 2 (of Chebyshev length k)
#     and none for k = 1, so k >= 2 in the theorem is sharp.
def plane_sequential(k):
    out = [spiral_unrank(q) + (k,) for q in range((2 * k + 1) ** 2)]
    for z in range(k - 1, -k, -1):
        out += [ring_cell(k, t) + (z,) for t in range(8 * k)]
    out += [spiral_unrank(q) + (-k,) for q in range((2 * k + 1) ** 2)]
    return out


for k in range(1, 13):
    seq = plane_sequential(k)
    assert sorted(seq) == sorted(shell(k))
    jumps = [cheb(seq[i], seq[i + 1]) for i in range(len(seq) - 1)]
    long_jumps = [j for j in jumps if j > 1]
    assert long_jumps == ([] if k == 1 else [k])
print("PASS cap-centre checks: local-minimum bound, facet centres in "
      "d=2,3,4, distance-k bound, plane-sequential order (k=1 sharpness)")
