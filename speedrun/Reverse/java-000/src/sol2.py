# Curve parameters for secp256k1
p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
a = 0
b = 7

# Modular inverse
def inverse_mod(k, p):
    return pow(k, -1, p)

# Point addition
def point_add(P, Q):
    if P is None:
        return Q
    if Q is None:
        return P

    x1, y1 = P
    x2, y2 = Q

    if x1 == x2 and y1 != y2:
        return None  # Point at infinity

    if P == Q:
        # Point doubling
        if y1 == 0:
            return None
        m = (3 * x1 * x1) * inverse_mod(2 * y1, p) % p
    else:
        if x1 == x2:
            return None
        m = (y2 - y1) * inverse_mod(x2 - x1, p) % p

    x3 = (m * m - x1 - x2) % p
    y3 = (m * (x1 - x3) - y1) % p

    return (x3, y3)

# Example usage
P = (0o11615376121650374234147712415727620557267422416714444335426002334554047606566607775613, -0o6077114355247325330417052411472260416432326704514764170005202327562661631377512470667)  # Replace with your first point's coordinates
Q = (0o12077346633003322030116204134501641554466352254175203365302635013403541442703604104474, 0o14445424345053712276761055603735701657060105133142775770145705516612506144414430704132)  # Replace with your second point's coordinates

result = point_add(P, Q)
print("Result:", result)

