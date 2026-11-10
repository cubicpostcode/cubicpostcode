#!/usr/bin/env python3
"""Reference implementations for Investigation 2 (research candidates only).

Candidate models defined here (NOT the production CUBIC POSTCODE identifier):

  Model C  shell-monotone bijection N -> Z^3 with exactly one non-face step
           per cubic shell (an edge-diagonal step of length sqrt 2) and
           face steps everywhere else, including between shells.
  Model D  fully face-continuous (6-adjacent) bijection N -> Z^3 that is
           monotone in *double* shells S_{2j-1} u S_{2j}.

Conventions: cell-centred integer grid, origin (0,0,0) has rank 0, ranks are
zero-based, shells are Chebyshev shells S_k = {max(|x|,|y|,|z|) = k}.
All arithmetic is exact integer arithmetic (no floating point).
"""
from math import isqrt


def icbrt(n):
    """floor(n ** (1/3)) for any integer n >= 0, integer-only Newton."""
    if n < 0:
        raise ValueError("icbrt needs n >= 0")
    if n < 2:
        return n
    x = 1 << -(-n.bit_length() // 3)          # x >= true root
    while True:
        y = (2 * x + n // (x * x)) // 3
        if y >= x:
            return x
        x = y


# ---------------------------------------------------------------- 2-D spiral
# sigma(0) = (0,0).  Ring r >= 1 holds ranks (2r-1)^2 .. (2r+1)^2 - 1, starts
# at (r, -r+1), runs +y, -x, -y, +x and ends at the corner (r, -r).

def ring_cell(r, t):
    """Cell number t (0 <= t < 8r) of ring r >= 1."""
    s, u = divmod(t, 2 * r)
    if s == 0:
        return (r, -r + 1 + u)
    if s == 1:
        return (r - 1 - u, r)
    if s == 2:
        return (-r, r - 1 - u)
    return (-r + 1 + u, -r)


def ring_index(r, x, y):
    """Inverse of ring_cell for max(|x|,|y|) = r >= 1."""
    if x == r and y > -r:
        return y + r - 1
    if y == r:
        return 2 * r + (r - 1 - x)
    if x == -r:
        return 4 * r + (r - 1 - y)
    return 6 * r + (x + r - 1)


def spiral_unrank(q):
    if q == 0:
        return (0, 0)
    r = (isqrt(q) + 1) // 2
    return ring_cell(r, q - (2 * r - 1) ** 2)


def spiral_rank(x, y):
    r = max(abs(x), abs(y))
    if r == 0:
        return 0
    return (2 * r - 1) ** 2 + ring_index(r, x, y)


# ------------------------------------------------------------------ Model C
def c_shell_unrank(k, q):
    """Cell number q (0 <= q < 24k^2+2) of shell k in local coordinates
    (x, y, w); the traversal runs from (0,0,k) to (0,0,-k)."""
    m = (2 * k + 1) ** 2
    if q < m:                                  # starting cap, spiral outward
        x, y = spiral_unrank(q)
        return (x, y, k)
    q -= m
    side = (2 * k - 1) * 8 * k
    if q < side:                               # rings, alternately fwd / rev
        i, t = divmod(q, 8 * k)
        if i & 1:
            t = 8 * k - 1 - t
        x, y = ring_cell(k, t)
        return (x, y, k - 1 - i)
    q -= side                                  # final cap, spiral inward
    x, y = spiral_unrank(m - 1 - q)
    return (x, y, -k)


def c_shell_rank(k, x, y, w):
    m = (2 * k + 1) ** 2
    if w == k:
        return spiral_rank(x, y)
    if w == -k:
        return m + (2 * k - 1) * 8 * k + (m - 1 - spiral_rank(x, y))
    i = k - 1 - w
    t = ring_index(k, x, y)
    if i & 1:
        t = 8 * k - 1 - t
    return m + 8 * k * i + t


def c_unrank(n):
    if n == 0:
        return (0, 0, 0)
    k = (icbrt(n) + 1) // 2
    x, y, w = c_shell_unrank(k, n - (2 * k - 1) ** 3)
    return (x, y, w if k & 1 else -w)          # odd shells start at z = +k


def c_rank(x, y, z):
    k = max(abs(x), abs(y), abs(z))
    if k == 0:
        return 0
    return (2 * k - 1) ** 3 + c_shell_rank(k, x, y, z if k & 1 else -z)


# ------------------------------------------------------------------ Model D
# Double shell j >= 1: a = 2j-1, b = 2j.  Local coordinates (x, y, w), the
# traversal runs from (0,0,a) to (0,0,-b).  m = (2b+1)^2, j0 = (2a-1)^2.

def d_block_unrank(j, q):
    a, b = 2 * j - 1, 2 * j
    m, j0 = (2 * b + 1) ** 2, (2 * a - 1) ** 2
    if q < 2 * m:                              # top slab, layers w = a, b
        if q < 2 * j0:                         # ladder zigzag, columns < j0
            c, e = divmod(q, 2)
            x, y = spiral_unrank(c)
            return (x, y, b if (c + e) & 1 else a)
        if q < m + j0:                         # outward sweep on w = b
            x, y = spiral_unrank(q - j0)
            return (x, y, b)
        x, y = spiral_unrank(2 * m + j0 - 1 - q)   # inward sweep on w = a
        return (x, y, a)
    q -= 2 * m
    ml = 8 * a + 8 * b
    mid = (2 * b - 3) * ml
    if q < mid:                                # annulus layers, fwd / rev
        i, t = divmod(q, ml)
        if i & 1:
            t = ml - 1 - t
        x, y = spiral_unrank(j0 + t)
        return (x, y, b - 2 - i)
    q -= mid                                   # bottom slab, reversed zigzag
    c, e = divmod(2 * m - 1 - q, 2)
    x, y = spiral_unrank(c)
    return (x, y, -b + 1 if (c + e) & 1 else -b)


def d_block_rank(j, x, y, w):
    a, b = 2 * j - 1, 2 * j
    m, j0 = (2 * b + 1) ** 2, (2 * a - 1) ** 2
    c = spiral_rank(x, y)
    ml = 8 * a + 8 * b
    if w >= a:                                 # top slab
        if c < j0:
            e = (c & 1) ^ (1 if w == b else 0)
            return 2 * c + e
        return c + j0 if w == b else 2 * m + j0 - 1 - c
    if w > -a:                                 # annulus layers
        i = b - 2 - w
        t = c - j0
        if i & 1:
            t = ml - 1 - t
        return 2 * m + i * ml + t
    e = (c & 1) ^ (1 if w == -b + 1 else 0)    # bottom slab
    return 2 * m + (2 * b - 3) * ml + (2 * m - 1 - (2 * c + e))


def d_unrank(n):
    if n == 0:
        return (0, 0, 0)
    j = (icbrt(n) + 3) // 4
    x, y, w = d_block_unrank(j, n - (4 * j - 3) ** 3)
    return (x, y, w if j & 1 else -w)


def d_rank(x, y, z):
    k = max(abs(x), abs(y), abs(z))
    if k == 0:
        return 0
    j = (k + 1) // 2
    return (4 * j - 3) ** 3 + d_block_rank(j, x, y, z if j & 1 else -z)


def step_type(p, q):
    """6 = face, 18 = edge diagonal, 26 = corner diagonal, 0 = longer jump."""
    d = sorted(abs(u - v) for u, v in zip(p, q))
    return {(0, 0, 1): 6, (0, 1, 1): 18, (1, 1, 1): 26}.get(tuple(d), 0)
