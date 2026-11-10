#!/usr/bin/env python3
"""Finite corroboration of the cap-centre obstruction, NOT a universal proof."""

def cheb(p):
    return max(map(abs,p))

def neighbors(p):
    x,y,z=p
    return [(x+dx,y+dy,z+dz)
            for dx in (-1,0,1) for dy in (-1,0,1)
            for dz in (-1,0,1) if (dx,dy,dz)!=(0,0,0)]

def check(k):
    assert k >= 2
    for z in (k,-k):
        p=(0,0,z)
        in_shell=[q for q in neighbors(p) if cheb(q)==k]
        # The sole shell-neighbours are on the same cap; under
        # cap-centre-first ordering they must succeed the cap centre.
        assert all(q[2]==z for q in in_shell)
        assert len(in_shell)==8
    return True

if __name__=="__main__":
    for k in range(2,201):
        assert check(k)
    print("PASS: both cap centres for radii 2..200 (finite corroboration)")
