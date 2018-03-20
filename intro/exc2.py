def gcd(a, b):
    a, b = abs(a), abs(b)
    while b != 0:
        a, b = b, a % b
    return a


print(gcd(3141, 156))
print(gcd(12345678, 987654321))


def frac(a, b):
    i = gcd(a, b)
    a = a//i
    b = b//i
    return str(a) + "/" + str(b)


print(frac(5, 10))


def extgcd(a, b):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while b != 0:
        q, a, b = a // b, b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return a, x0, y0


print(extgcd(1180, 482))
