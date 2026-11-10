#!/usr/bin/env python3
"""Independent finite table reimplementation of Models C/D from proofs 20/21.

Run from repository foundations/: python3 -I experiments/exp_review_i2_independent.py
No external dependencies. This does NOT import the reference implementation until
all candidate orders and inverse lookup maps have been constructed.
"""
from collections import Counter
from pathlib import Path
import sys


def planar_spiral(radius):
    points = [(0, 0)]
    for r in range(1, radius + 1):
        points.extend((r, y) for y in range(-r + 1, r + 1))
        points.extend((x, r) for x in range(r - 1, -r - 1, -1))
        points.extend((-r, y) for y in range(r - 1, -r - 1, -1))
        points.extend((x, -r) for x in range(-r + 1, r + 1))
    return points


def shell_c(radius):
    k = radius
    spiral = planar_spiral(k)
    ring = spiral[(2*k-1)**2:]
    cells = [(x,y,k) for x,y in spiral]
    for i in range(2*k-1):
        seq = ring if i % 2 == 0 else reversed(ring)
        cells.extend((x,y,k-1-i) for x,y in seq)
    cells.extend((x,y,-k) for x,y in reversed(spiral))
    return [(x,y,w if k%2 else -w) for x,y,w in cells]


def double_shell_d(block):
    j=block; a,b=2*j-1,2*j
    spiral=planar_spiral(b)
    inner=(2*a-1)**2
    cells=[]
    for i,(x,y) in enumerate(spiral[:inner]):
        cells.extend([(x,y,a),(x,y,b)] if i%2==0 else [(x,y,b),(x,y,a)])
    cells.extend((x,y,b) for x,y in spiral[inner:])
    cells.extend((x,y,a) for x,y in reversed(spiral[inner:]))
    ring=spiral[inner:]
    for i,w in enumerate(range(b-2,-b+1,-1)):
        seq=ring if i%2==0 else reversed(ring)
        cells.extend((x,y,w) for x,y in seq)
    bottom=[]
    for i,(x,y) in enumerate(spiral):
        bottom.extend([(x,y,-b),(x,y,-b+1)] if i%2==0 else [(x,y,-b+1),(x,y,-b)])
    cells.extend(reversed(bottom))
    return [(x,y,w if j%2 else -w) for x,y,w in cells]


def independent_order(model, radius=10):
    cells=[(0,0,0)]
    if model=='C':
        for k in range(1,radius+1):cells.extend(shell_c(k))
    else:
        assert radius%2 == 0
        for j in range(1,radius//2+1):cells.extend(double_shell_d(j))
    inverse={p:n for n,p in enumerate(cells)}
    expected={(x,y,z) for x in range(-radius,radius+1)
                      for y in range(-radius,radius+1)
                      for z in range(-radius,radius+1)}
    assert len(cells)==len(inverse)==len(expected)==(2*radius+1)**3
    assert set(cells)==expected
    return cells,inverse


def check(model, radius=10):
    cells,inverse=independent_order(model,radius)
    # Import only AFTER independent order and inverse have been constructed.
    sys.path.insert(0,str(Path(__file__).resolve().parent))
    import cubicshell as reference
    ref_rank=getattr(reference,model.lower()+'_rank')
    ref_unrank=getattr(reference,model.lower()+'_unrank')
    for n,p in enumerate(cells):
        assert ref_unrank(n)==p,(model,'unrank',n,p,ref_unrank(n))
        assert ref_rank(*p)==inverse[p]==n,(model,'rank',n,p,ref_rank(*p))
    steps=Counter(tuple(sorted(abs(a-b) for a,b in zip(p,q)))
                  for p,q in zip(cells,cells[1:]))
    if model=='C':
        assert steps=={(0,0,1):len(cells)-1-radius,(0,1,1):radius},steps
    else:
        assert steps=={(0,0,1):len(cells)-1},steps
    print(f'{model} PASS: radius {radius}, {len(cells)} rank+unrank comparisons, steps {dict(steps)}')

if __name__=='__main__':
    check('C')
    check('D')
