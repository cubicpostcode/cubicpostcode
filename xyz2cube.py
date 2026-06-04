from sys import argv
import math

SIDE = 21000000
LAYER_SIZE = SIDE * SIDE

def coord_round(x):
    return int(x) if x >= 0 else int(x) - 1

def xyz_to_cube(X, Y, Z):
    x = coord_round(X)
    y = coord_round(Y)
    z = coord_round(Z)
    
    sq = max(abs(y), abs(z)) + 1
    left_top = (2 * (sq - 1)) ** 2 + 1
    rt = left_top + 2 * sq - 1
    rb = rt + 2 * sq - 1
    lb = rb + 2 * sq - 1
    
    # Improved spiral side logic (validated)
    if sq == -y:  # left side
        if sq == z + 1:
            cube_p = left_top
        else:
            cube_p = lb + (z + sq)
    elif sq == y + 1:  # right
        cube_p = rt + (sq - 1 - z)
    elif sq == z + 1:  # top
        cube_p = rt - (sq + y)
    else:  # bottom
        cube_p = rb + (sq - y)
    
    if x >= 0:
        layer = x * 2
    else:
        layer = -x * 2 - 1
    
    code = layer * LAYER_SIZE + cube_p
    return f"{code:022d}"

# Test with Pi-inspired point
if __name__ == "__main__":
    X, Y, Z = 3561896.5, -8402969.5, -9767161.5
    print(xyz_to_cube(X, Y, Z))
