#!/usr/bin/env python3
"""Investigation 3, Phase 2.2-2.3: radix-5 hierarchical generators with several gate types (OP-9).

Run from foundations/:  python3 -I experiments/exp_i3_radix5_grammar.py

Setting (see mathematics/30-...): a block of side 5^t is split into 125 children
of side 5^(t-1) on the child grid {-2..2}^3.  A non-centre piece is entered at a
corner eps and left at a corner chi = eps flipped on a non-empty axis set D:

  type O : D = {x,y,z}  (opposite corner)
  type F : |D| = 2      (face-diagonal corner)
  type E : |D| = 1      (edge-adjacent corner)

Leaving across the face (axis a, sign s) needs chi_a = s; the next child is
entered at chi with component a flipped.  A *generator* for a type is a
Hamiltonian path of the child grid whose children carry types from an allowed
set, entered/left consistently.  The CENTRE generator starts at child (0,0,0),
whose exit corner is a given c (the exit of the previously built centre block),
and ends at a grid corner g, leaving at the outward corner sign(g).

A grammar is closed if every type used by any generator in it also has a
generator in it.  Then, by induction on the level, every type has a
face-continuous traversal at every level in which every aligned 5^s sub-block
is contiguous (Theorem 9 of file 30).  This script searches for a closed
grammar and verifies every generator it finds, rule by rule.
"""
import itertools
import sys

AX = (0, 1, 2)
CELLS = [(x, y, z) for x in range(-2, 3) for y in range(-2, 3) for z in range(-2, 3)]
CORNERS = [g for g in CELLS if all(abs(v) == 2 for v in g)]
TYPE_SETS = {"O": [frozenset(AX)], "F": [frozenset(s) for s in itertools.combinations(AX, 2)],
             "E": [frozenset([a]) for a in AX]}


def flip(v, D):
    return tuple(-v[i] if i in D else v[i] for i in AX)


def nbrs(g):
    for a in AX:
        for s in (-1, 1):
            q = tuple(g[i] + (s if i == a else 0) for i in AX)
            if all(-2 <= v <= 2 for v in q):
                yield a, s, q


def search(start, first_exit, end_cell, end_exit, allowed, limit):
    """Hamiltonian path from `start` (whose exit corner is first_exit) to end_cell,
    leaving end_cell at end_exit; every other child takes a type from `allowed`."""
    Ds = [D for t in allowed for D in TYPE_SETS[t]]
    unvisited = set(CELLS) - {start}
    path, chis, types = [start], [first_exit], [None]
    count = [0]

    def ok_connect(cur):
        if not unvisited:
            return True
        if end_cell not in unvisited:
            return False
        seen, todo = {end_cell}, [end_cell]
        while todo:
            p = todo.pop()
            for _, _, q in nbrs(p):
                if q in unvisited and q not in seen:
                    seen.add(q)
                    todo.append(q)
        if len(seen) != len(unvisited):
            return False
        # every unvisited cell other than end_cell needs >= 2 neighbours in unvisited + {cur}
        for p in unvisited:
            if p == end_cell:
                continue
            k = sum(1 for _, _, q in nbrs(p) if q in unvisited or q == cur)
            if k < 2:
                return False
        return True

    def dfs():
        count[0] += 1
        if count[0] > limit:
            raise TimeoutError
        g, chi = path[-1], chis[-1]
        cand = []
        for a, s, q in nbrs(g):
            if q not in unvisited or chi[a] != s:
                continue
            eps = flip(chi, {a})                       # entry corner of child q
            last = len(unvisited) == 1
            for D in Ds:
                nchi = flip(eps, D)
                if last and (q != end_cell or nchi != end_exit):
                    continue
                if not last and q == end_cell:
                    continue
                onward = sum(1 for _, _, r in nbrs(q) if r in unvisited)
                cand.append((onward, len(D), a, q, nchi, D))
        cand.sort(key=lambda t: (t[0], t[1]))
        for onward, _, a, q, nchi, D in cand:
            unvisited.discard(q)
            if ok_connect(q):
                path.append(q)
                chis.append(nchi)
                types.append(D)
                if not unvisited or dfs():
                    return True
                path.pop()
                chis.pop()
                types.pop()
            unvisited.add(q)
        return False

    sys.setrecursionlimit(20000)
    try:
        found = dfs()
    except TimeoutError:
        found = False
    return (list(path), list(chis), list(types)) if found else None


def verify(sol, start, first_exit, end_cell, end_exit, allowed):
    path, chis, types = sol
    Ds = {D for t in allowed for D in TYPE_SETS[t]}
    assert path[0] == start and chis[0] == first_exit and len(path) == 125 and set(path) == set(CELLS)
    for i in range(1, 125):
        d = tuple(path[i][j] - path[i - 1][j] for j in AX)
        assert sum(map(abs, d)) == 1
        a = next(j for j in AX if d[j])
        assert chis[i - 1][a] == d[a]                  # leave through a face containing the exit corner
        eps = flip(chis[i - 1], {a})
        assert types[i] in Ds and chis[i] == flip(eps, types[i])
    assert path[-1] == end_cell and chis[-1] == end_exit


def kind(D):
    return {3: "O", 2: "F", 1: "E"}[len(D)]


def moves(path):
    names = {(1, 0, 0): "x", (-1, 0, 0): "X", (0, 1, 0): "y", (0, -1, 0): "Y", (0, 0, 1): "z", (0, 0, -1): "Z"}
    return "".join(names[tuple(q[i] - p[i] for i in AX)] for p, q in zip(path, path[1:]))


def typestring(types):
    return "".join("xyz"[min(D)] if len(D) == 1 else ("O" if len(D) == 3 else "F" + "xyz"[3 - sum(D)])
                   for D in types)


def main():
    c0 = (1, 1, 1)                                     # exit corner of the centre block (wlog)
    print("Each run is a bounded search: 'none within limit' is not a proof of non-existence.", flush=True)
    for allowed in (("E",), ("F",), ("O", "E"), ("O", "F")):
        found = None
        for g in CORNERS:
            sgn = tuple(1 if v > 0 else -1 for v in g)
            sol = search((0, 0, 0), c0, g, sgn, allowed, 40_000)
            if sol:
                verify(sol, (0, 0, 0), c0, g, sgn, allowed)
                found = (g, sol)
                break
        if found:
            print(f"CENTRE generator, types {allowed}: FOUND (verified), ends at child {found[0]}\n"
                  f"  moves {moves(found[1][0])}\n  child types (entry-relative flip axis) "
                  f"{typestring(found[1][2][1:])}", flush=True)
        else:
            print(f"CENTRE generator, types {allowed}: none within limit", flush=True)
        for t, D in (("E", frozenset({0})), ("F", frozenset({0, 1})), ("O", frozenset(AX))):
            sol = search_piece(D, allowed, 40_000)
            if sol:
                entry = (-1, -1, -1)
                ex = flip(entry, D)
                verify_piece(sol, D, allowed)
                print(f"  {t}-piece generator, types {allowed}: FOUND (verified)\n"
                      f"    moves {moves(sol[0])}\n    child types {typestring(sol[2])}", flush=True)
            else:
                print(f"  {t}-piece generator, types {allowed}: none within limit", flush=True)
    return 0


def verify_piece(sol, D_parent, allowed):
    path, chis, types = sol
    entry = (-1, -1, -1)
    assert types[0] in {D for t in allowed for D in TYPE_SETS[t]} and chis[0] == flip(entry, types[0])
    exit_corner = flip(entry, D_parent)
    verify(sol, (-2, -2, -2), chis[0], tuple(2 * v for v in exit_corner), exit_corner, allowed)


def search_piece(D_parent, allowed, limit=40_000):
    """Generator for a piece entered at corner (-,-,-) and left at that corner flipped on D_parent.
    The first child (-2,-2,-2) is entered at (-,-,-) and has its own type; implemented by trying
    each allowed type for the first child and searching the rest."""
    entry = (-1, -1, -1)
    exit_corner = flip(entry, D_parent)
    end_cell = tuple(2 * v for v in exit_corner)
    for t in allowed:
        for D in TYPE_SETS[t]:
            chi0 = flip(entry, D)
            sol = search((-2, -2, -2), chi0, end_cell, exit_corner, allowed, limit)
            if sol:
                sol[2][0] = D
                return sol
    return None


if __name__ == "__main__":
    sys.exit(main())
