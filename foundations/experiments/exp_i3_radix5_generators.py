#!/usr/bin/env python3
"""Investigation 3, Phase 2.2: search for radix-5 generators (OP-9).

Run from foundations/:  python3 -I experiments/exp_i3_radix5_generators.py

Child grid: the 5x5x5 cells {-2..2}^3 of a parent block.  Each child block of
side L = 5^t (t >= 1) is traversed corner to opposite corner; its *entry
state* eps in {-1,+1}^3 names its entry corner.  Leaving a child across the
face in direction d = sigma * e_a requires the exit corner (-eps) to lie on
that face, i.e. sigma = -eps_a; the next child is entered at the mirror
corner, i.e. eps' = -eps with component a restored:  eps'_a = eps_a.

A generator is a Hamiltonian path g_0 .. g_124 of the child grid with states
eps_0 .. eps_124 obeying that rule.  Two kinds are needed:

  PEANO   g_0 = (-2,-2,-2), eps_0 = (-1,-1,-1), ends at (2,2,2) with exit
          corner -eps_124 = (+1,+1,+1)            (corner -> opposite corner)
  CENTRE  g_0 = (0,0,0), eps_0 = -c where c = (+1,+1,+1) is the exit corner
          of the already-built centre block; ends at a grid corner g with
          exit corner -eps_124 = sign(g)           (centre -> outer corner)

The script finds and verifies a PEANO generator, then checks Theorem 9 of
mathematics/30-...: no CENTRE generator of this (opposite-corner) kind exists,
because the admissible moves form a one-way digraph with a source corner.
Standard library only; deterministic; well under a second.
"""
import sys

AX = range(3)
CELLS = [(x, y, z) for x in range(-2, 3) for y in range(-2, 3) for z in range(-2, 3)]


def step(g, eps, a):
    sigma = -eps[a]
    ng = tuple(g[i] + (sigma if i == a else 0) for i in AX)
    neps = tuple(eps[i] if i == a else -eps[i] for i in AX)
    return ng, neps


def inside(g):
    return all(-2 <= v <= 2 for v in g)


def connected(unvisited, start):
    if not unvisited:
        return True
    todo = [start]
    seen = {start}
    while todo:
        p = todo.pop()
        for a in AX:
            for s in (-1, 1):
                q = tuple(p[i] + (s if i == a else 0) for i in AX)
                if q in unvisited and q not in seen:
                    seen.add(q)
                    todo.append(q)
    return len(seen) == len(unvisited)


def search(g0, eps0, accept, limit=5_000_000):
    """Depth-first search for a rule-respecting Hamiltonian path of the child grid."""
    path, states = [g0], [eps0]
    unvisited = set(CELLS) - {g0}
    nodes = [0]

    def options(g, eps):
        out = []
        for a in AX:
            ng, neps = step(g, eps, a)
            if inside(ng) and ng in unvisited:
                onward = sum(1 for b in AX if inside(step(ng, neps, b)[0]) and step(ng, neps, b)[0] in unvisited)
                out.append((onward, a, ng, neps))
        out.sort()
        return out

    def dfs():
        nodes[0] += 1
        if nodes[0] > limit:
            return False
        if not unvisited:
            return accept(path[-1], states[-1])
        g, eps = path[-1], states[-1]
        for _, a, ng, neps in options(g, eps):
            unvisited.discard(ng)
            if connected(unvisited, next(iter(unvisited)) if unvisited else ng) or not unvisited:
                path.append(ng)
                states.append(neps)
                if dfs():
                    return True
                path.pop()
                states.pop()
            unvisited.add(ng)
        return False

    sys.setrecursionlimit(10_000)
    ok = dfs()
    return (path, states, nodes[0]) if ok else (None, None, nodes[0])


def moves(path):
    names = {(1, 0, 0): "x", (-1, 0, 0): "X", (0, 1, 0): "y", (0, -1, 0): "Y", (0, 0, 1): "z", (0, 0, -1): "Z"}
    return "".join(names[tuple(q[i] - p[i] for i in AX)] for p, q in zip(path, path[1:]))


def verify(path, states, g0, eps0, end_ok):
    assert path[0] == g0 and states[0] == eps0
    assert len(path) == 125 and set(path) == set(CELLS)
    for i in range(124):
        d = tuple(path[i + 1][j] - path[i][j] for j in AX)
        assert sum(abs(v) for v in d) == 1
        a = next(j for j in AX if d[j])
        assert d[a] == -states[i][a]                       # leave through the exit corner's face
        assert states[i + 1] == tuple(states[i][j] if j == a else -states[i][j] for j in AX)
    assert end_ok(path[-1], states[-1])


def sgn(v):
    return (v > 0) - (v < 0)


def main():
    peano_end = lambda g, e: g == (2, 2, 2) and tuple(-v for v in e) == (1, 1, 1)
    centre_end = lambda g, e: all(abs(v) == 2 for v in g) and tuple(-v for v in e) == tuple(sgn(v) for v in g)

    p_path, p_states, p_nodes = search((-2, -2, -2), (-1, -1, -1), peano_end)
    assert p_path, "no PEANO generator found within the node limit"
    verify(p_path, p_states, (-2, -2, -2), (-1, -1, -1), peano_end)
    print(f"FOUND PEANO generator ({p_nodes} search nodes): {moves(p_path)}")

    # Theorem 9 (file 30): with opposite-corner pieces only, the admissible moves form a fixed
    # one-way digraph whose corner opposite the sink has in-degree 0, so no Hamiltonian path can
    # start at the centre.  Check the digraph directly for several odd radices and every c.
    for b in (3, 5, 7, 9):
        h = (b - 1) // 2
        cells = [(x, y, z) for x in range(-h, h + 1) for y in range(-h, h + 1) for z in range(-h, h + 1)]
        for c in [(sx, sy, sz) for sx in (-1, 1) for sy in (-1, 1) for sz in (-1, 1)]:
            # entry-state field from Lemma 8 with eps(centre) = -c:  eps_i(g) = -c_i (-1)^(sum_{j != i} g_j)
            def eps(g):
                return tuple(-c[i] * (-1) ** (sum(g) - g[i]) for i in AX)
            indeg = {g: 0 for g in cells}
            for g in cells:
                e = eps(g)
                for a in AX:
                    q = tuple(g[i] + (-e[a] if i == a else 0) for i in AX)
                    if q in indeg:
                        indeg[q] += 1
            sources = [g for g in cells if indeg[g] == 0]
            assert len(sources) == 1 and all(abs(v) == h for v in sources[0]) and sources[0] != (0, 0, 0)
    print("PASS Theorem 9: for radix 3, 5, 7, 9 and every centre exit corner, the opposite-corner gate digraph "
          "has exactly one in-degree-0 cell, a corner; so no centre-first generator of type O exists")
    print("  (a bounded DFS of 5,000,053 nodes earlier found none either, consistent with the theorem)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
