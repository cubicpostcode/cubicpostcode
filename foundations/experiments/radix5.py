#!/usr/bin/env python3
"""Model H5: a hierarchical, face-continuous, origin-first bijection N <-> Z^3 on
centred radix-5 blocks (Investigation 3, OP-9).  Research candidate only; it is
NOT the production CUBIC POSTCODE identifier and is not compatible with it.

Conventions: cell-centred integer grid; rank 0 is the origin; ranks are
zero-based; B_t = [-r_t, r_t]^3 with r_t = (5^t - 1)/2; the aligned blocks of
level s are the cubes of side 5^s centred on the lattice 5^s * Z^3.

Construction (proof in mathematics/30-radix5-hierarchical-face-continuous.md):
two 125-step *generators* found by search in exp_i3_radix5_grammar.py and
re-verified here on import:

  CENTRE  child grid path from (0,0,0) to a corner; the centre child is the
          previous level's tower, every other child is an E-piece.
  EPIECE  child grid path from corner (-2,-2,-2) to corner (2,-2,-2); every
          child is an E-piece.

An E-piece of side 5^L is entered at one corner cell and left at the corner
cell that differs in exactly one axis.  Child i of a generator is entered at
corner eps_i and left at chi_i = eps_i flipped on one axis ("child type").
"""
from functools import lru_cache

AX = (0, 1, 2)
STEP = {"x": (1, 0, 0), "X": (-1, 0, 0), "y": (0, 1, 0), "Y": (0, -1, 0), "z": (0, 0, 1), "Z": (0, 0, -1)}

CENTRE_MOVES = ("xxyXXXXYxzXyxxYxxYZYzXyZYXzyZXXYxzXyxzYXyyxxYYxxyXyxyZXzXXXyxxxxZXXXXZxxxxZXXXXY"
                "xxxxYXXXXYxxxxYXXXXZxxxxyXXXXyxxxxyyXYXyXYXy")
CENTRE_TYPES = ("xxxxxxxxxxxxxxyxxxyxxxxxyxyxxxxxxxxxzxxxyxxxyyxyyxxyxxxyxxxxxxxxxxxxzyxxxzyxxxxxxxxyyx"
                "xxxxxxxyyxxxzyxxxxxxxxyyxxxxyxxyyxxzxy")
EPIECE_MOVES = ("xxxyxyXXXXyxxxxyXXXXzxxxxYXXXXYxxxxYXXZXXzxYXzyxYxZxzyxyXXYzXXyZxzyZXzyZxzxZYxxyXz"
                "xYXXYxxYXYXXXzyxYxxyXyxyXXYXyyxxxxYYYYZZZZ")
EPIECE_TYPES = ("xxxyxyyxxxxxxxxyyxxxzyxxxxxxxxyyxxxxxxxyxxxxxzxxxyxyxxxyyxyzxxxxyxxxxxyxyxyxxxxxxxx"
                "xxxyyxxxyxxxzxxxyxyyxxyyxyxxyxxxxxyyyyzzzz")


def _flip(v, axes):
    return tuple(-v[i] if i in axes else v[i] for i in AX)


def _matmul(A, B):
    return tuple(tuple(sum(A[i][k] * B[k][j] for k in AX) for j in AX) for i in AX)


def _apply(S, v):
    return tuple(sum(S[i][k] * v[k] for k in AX) for i in AX)


def _diag(s):
    return tuple(tuple(s[i] if i == j else 0 for j in AX) for i in AX)


def _child_symmetry(eps, b):
    """Signed permutation sending canonical entry (-,-,-) to eps and axis 0 to axis b."""
    others = [a for a in AX if a != b]
    cols = {0: b, 1: others[0], 2: others[1]}           # canonical axis j -> actual axis cols[j]
    P = tuple(tuple(1 if cols[j] == i else 0 for j in AX) for i in AX)
    return _matmul(_diag(tuple(-e for e in eps)), P)


def _build(moves, types, start, first_exit):
    """Replay a generator; return children [(offset, symmetry)] and checks the gate rule."""
    cells, out = [start], []
    g, chi = start, first_exit
    for i, mv in enumerate(moves):
        d = STEP[mv]
        a = next(j for j in AX if d[j])
        assert chi[a] == d[a], ("gate rule", i)
        g = tuple(g[j] + d[j] for j in AX)
        eps = _flip(chi, {a})
        b = "xyz".index(types[i if len(types) == len(moves) else i + 1])
        chi = _flip(eps, {b})
        cells.append(g)
        out.append((g, _child_symmetry(eps, b)))
    assert len(set(cells)) == 125 and all(max(map(abs, c)) <= 2 for c in cells)
    return out, g, chi


# CENTRE: child 0 is the centre tower with exit corner c0 = (1,1,1) (canonical frame).
_C_REST, _C_END, _C_EXIT = _build(CENTRE_MOVES, CENTRE_TYPES, (0, 0, 0), (1, 1, 1))
assert _C_EXIT == tuple(1 if v > 0 else -1 for v in _C_END) and all(abs(v) == 2 for v in _C_END)
CENTRE_CHILDREN = [((0, 0, 0), None)] + _C_REST

# EPIECE: child 0 sits at (-2,-2,-2), entered at (-,-,-), type EPIECE_TYPES[0].
_b0 = "xyz".index(EPIECE_TYPES[0])
_E_REST, _E_END, _E_EXIT = _build(EPIECE_MOVES, EPIECE_TYPES, (-2, -2, -2), _flip((-1, -1, -1), {_b0}))
assert _E_END == (2, -2, -2) and _E_EXIT == (1, -1, -1)
EPIECE_CHILDREN = [((-2, -2, -2), _child_symmetry((-1, -1, -1), _b0))] + _E_REST

C_POS = {v: i for i, (v, _) in enumerate(CENTRE_CHILDREN)}
E_POS = {v: i for i, (v, _) in enumerate(EPIECE_CHILDREN)}
_END_SIGN = tuple(1 if v > 0 else -1 for v in _C_END)
IDENTITY = _diag((1, 1, 1))


def tower_frame(L):
    """Reflection applied to the CENTRE generator at level L >= 1: diag(c_{L-1})."""
    c = tuple(s ** (L - 1) for s in _END_SIGN)          # c_0 = (1,1,1), c_L = diag(c_{L-1}) * end sign
    return _diag(c)


def _transpose(S):
    return tuple(tuple(S[j][i] for j in AX) for i in AX)


def level_of_rank(n):
    t, size = 0, 1
    while n >= size:
        t, size = t + 1, size * 125
    return t


def unrank(n):
    if n < 0:
        raise ValueError("rank must be >= 0")
    L = level_of_rank(n)
    centre, kind, S = (0, 0, 0), "C", None
    while L > 0:
        q, n = divmod(n, 125 ** (L - 1))
        side = 5 ** (L - 1)
        if kind == "C":
            F = tower_frame(L)
            v, Sq = CENTRE_CHILDREN[q]
            if q == 0:
                pass                                     # stay in the centre tower
            else:
                centre = tuple(centre[i] + _apply(F, v)[i] * side for i in AX)
                kind, S = "E", _matmul(F, Sq)
        else:
            v, Sq = EPIECE_CHILDREN[q]
            centre = tuple(centre[i] + _apply(S, v)[i] * side for i in AX)
            S = _matmul(S, Sq)
        L -= 1
    return centre


def rank(x, y, z):
    p = (x, y, z)
    L = 0
    while max(map(abs, p)) > (5 ** L - 1) // 2:
        L += 1
    n, centre, kind, S = 0, (0, 0, 0), "C", None
    while L > 0:
        side = 5 ** (L - 1)
        r = (side - 1) // 2
        u = tuple(p[i] - centre[i] for i in AX)
        F = tower_frame(L) if kind == "C" else S
        w = _apply(_transpose(F), u)                     # inverse of a signed permutation
        v = tuple((w[i] + r) // side for i in AX)
        if kind == "C":
            q = C_POS[v]
            if q:
                kind, S = "E", _matmul(F, CENTRE_CHILDREN[q][1])
                centre = tuple(centre[i] + _apply(F, v)[i] * side for i in AX)
        else:
            q = E_POS[v]
            centre = tuple(centre[i] + _apply(S, v)[i] * side for i in AX)
            S = _matmul(S, EPIECE_CHILDREN[q][1])
        n += q * 125 ** (L - 1)
        L -= 1
    return n
