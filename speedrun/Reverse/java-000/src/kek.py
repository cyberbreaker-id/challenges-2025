import random

# Curve parameters
p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F  # Field prime
a = 0
b = 7

# Legendre symbol (Euler's criterion) to check if a number is a quadratic residue mod p
def is_quadratic_residue(n, p):
    return pow(n, (p - 1) // 2, p) == 1

# Tonelli-Shanks algorithm to compute sqrt(n) mod p (when p ≡ 3 mod 4, we can shortcut)
def mod_sqrt(n, p):
    # p % 4 == 3 shortcut
    return pow(n, (p + 1) // 4, p)

def generate_random_point():
    while True:
        x = random.randrange(0, p)
        rhs = (x ** 3 + a * x + b) % p
        if is_quadratic_residue(rhs, p):
            y = mod_sqrt(rhs, p)
            return (x, y)

# Example
x, y = generate_random_point()
print(f"Random point on secp256k1:\nx = {oct(x)}\ny = {oct(y)}")

