def fact(n):
    i = n - 1
    while i > 0:
        n *= i
        i -= 1
    return n


def binom(n, k):
    return int(fact(n) / (fact(n-k) * fact(k)))

