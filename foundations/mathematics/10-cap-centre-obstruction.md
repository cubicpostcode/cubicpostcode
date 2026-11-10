# The cap-centre obstruction theorem

**Date:** 2026-11-10  
**Status:** PROVEN, conditional on the stated three properties  
**Resolves:** C-02 / OP-2 from Investigation 1

## Definitions

For integer `k >= 1`, the Chebyshev cubic shell is

```
S_k = { (x,y,z) in Z^3 : max(|x|,|y|,|z|) = k }.
```

Two distinct cells are **26-adjacent** iff their Chebyshev distance is 1. A shell traversal is **26-continuous** if successive cells in its ordering are 26-adjacent.

**Cap-centre-first property:** on each horizontal cap at `z=+k` and `z=-k`, the cell `(0,0,+k)` respectively `(0,0,-k)` precedes all other cells in that cap. An ordinary origin-first planar square spiral imposes this property on both caps.

## Theorem

For each `k >= 2`, no complete ordering of `S_k` can satisfy both:

1. the cap-centre-first property on **both** its upper and lower caps, and
2. 26-adjacency of **every** consecutive pair of cells within the shell.

Therefore no global enumeration monotone by complete cubic shells can simultaneously preserve the standard origin-first planar spiral in every horizontal plane and be 26-continuous.

## Proof

Set `p+=(0,0,k)`. If `p+` were not the first cell in the shell, it would have a predecessor `q` in `S_k` at Chebyshev distance 1.

Such `q` cannot lie on the upper cap `z=k`, since cap-centre-first makes `p+` earlier than every other cell on that cap. It also cannot be at `z>k` or `z<k-1` by the 26-adjacency condition and shell boundaries. Hence `q=(a,b,k-1)` with `|a|<=1`, `|b|<=1`.

But for `k>=2`, `max(|a|,|b|,|k-1|) <= k-1`; thus `q` is **not** in `S_k`. Contradiction. So `p+` must be the first cell of the shell.

By the same argument on the lower cap, `p-=(0,0,-k)` must **also** be the first cell of `S_k`. Since `p+` and `p-` are distinct for `k>=2`, no such ordering exists. QED.

## Strength and limits

The proof uses only **cap-centre-first**, a weaker assumption than the complete planar square-spiral ordering. The case `k=1` alone does not show this contradiction, but `k=2` settles any claim requiring the property for **all** shells.

This theorem is **not** a universal impossibility of 26-adjacent 3D space-filling traversals, nor an argument against candidate Model A*; such constructions must relax cap-centre-first in at least one cap or another stated assumption.

## Regression observation, not proof

For `k = 2,3,...`, enumerate the 26 potential neighbours of each cap centre and verify that every neighbour outside its own cap lies in the interior cube `[-k+1,k-1]^3`. Finite tests support the proof but do not replace the all-`k` argument.
