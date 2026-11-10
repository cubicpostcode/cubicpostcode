#!/usr/bin/env python3
"""Exact small-case checks for OP-1 (independent of the parity argument).

1. Pure-Python exhaustive search: S_1 has no face-adjacent Hamiltonian path,
   and S_1 minus a cell L has one iff L is in the majority colour class.
2. If OR-tools is installed, CP-SAT proves for k = 1, 2, 3 that one
   face-adjacent path cannot cover S_k while two paths can.
Finite evidence only; the all-k statements are proved in mathematics/20-*.
"""
import itertools
import sys


def shell(k):
    r = range(-k, k + 1)
    return [p for p in itertools.product(r, r, r) if max(map(abs, p)) == k]


def face_graph(cells):
    cs = set(cells)
    g = {}
    for p in cells:
        g[p] = []
        for a in range(3):
            for s in (1, -1):
                q = list(p)
                q[a] += s
                q = tuple(q)
                if q in cs:
                    g[p].append(q)
    return g


def has_ham_path(cells):
    """Exhaustive depth-first search with memoised dead states.  The only
    pruning is the trivially sound one below; no parity argument is used."""
    g = face_graph(cells)
    ids = {p: i for i, p in enumerate(cells)}
    nb = [[ids[q] for q in g[p]] for p in cells]
    full = (1 << len(cells)) - 1
    dead = set()

    def dfs(v, mask):
        if mask == full:
            return True
        if (v, mask) in dead:
            return False
        # sound pruning: at most one unvisited cell may have fewer than two
        # usable neighbours (it would have to be the final cell of the path)
        stuck = 0
        for u in range(len(cells)):
            if not mask >> u & 1:
                free = sum(1 for w in nb[u] if w == v or not mask >> w & 1)
                if free == 0 or (free == 1 and v not in nb[u]):
                    stuck += 1
                    if free == 0 or stuck > 1:
                        dead.add((v, mask))
                        return False
        for u in nb[v]:
            if not mask >> u & 1 and dfs(u, mask | 1 << u):
                return True
        dead.add((v, mask))
        return False

    return any(dfs(i, 1 << i) for i in range(len(cells)))


S1 = shell(1)
assert len(S1) == 26
assert not has_ham_path(S1)
ok = sorted(L for L in S1 if has_ham_path([p for p in S1 if p != L]))
majority = sorted(p for p in S1 if sum(p) % 2 == 1)      # faces and corners
assert len(majority) == 14 and ok == majority
print("PASS exhaustive k=1: no Hamiltonian path on S_1; S_1 minus L is "
      "traceable exactly for the 14 majority-class cells L")

try:
    from ortools.sat.python import cp_model
except ImportError:
    print("SKIP CP-SAT part (pip install ortools to enable)")
    sys.exit(0)


def cover(k, paths):
    cells = shell(k)
    idx = {p: i + 1 for i, p in enumerate(cells)}
    depots = [0] + list(range(len(cells) + 1, len(cells) + paths))
    model, arcs = cp_model.CpModel(), []
    for p, nbrs in face_graph(cells).items():
        for q in nbrs:
            arcs.append((idx[p], idx[q], model.NewBoolVar("")))
        for d in depots:              # depot arcs cut the circuit into paths
            arcs.append((d, idx[p], model.NewBoolVar("")))
            arcs.append((idx[p], d, model.NewBoolVar("")))
    model.AddCircuit(arcs)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 300
    return solver.StatusName(solver.Solve(model))


for k in (1, 2, 3):
    assert cover(k, 1) == "INFEASIBLE", k
    assert cover(k, 2) in ("OPTIMAL", "FEASIBLE"), k
print("PASS CP-SAT k=1,2,3: one face-adjacent path infeasible, two feasible")
