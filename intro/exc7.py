def divisors(a):
    divs = set()
    i = 1
    n = a
    while i < n:
        n = a / i
        if n % 1 == 0:
            divs.add(i)
            divs.add(int(n))
        i += 1
    return divs


def primes(a):
    primeslst = list()
    factorization = list()
    for i in divisors(a):
        if len(divisors(i)) <= 2:
            primeslst.append(i)
    factorization.append(max(primeslst))
    n = int(a / max(primeslst))
    while n not in primeslst and n != 0:
        primeslst2 = set()
        for i in primeslst:
            if i in divisors(n):
                primeslst2.add(i)
        factorization.append(max(primeslst2))
        n = n / max(primeslst2)
    factorization.append(int(n))
    return factorization

