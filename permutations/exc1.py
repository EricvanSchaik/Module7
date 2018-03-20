from permutations.perm import *

q = test_permutation(20)
print(q)

p = [1, 2, 3, 0, 5, 4, 6, 7, 8, 9]
print(p)
print_permutation(p)
print(is_trivial(p))
print(p[0])
print(cycles(p))

r = trivial_permutation(10)
print(r)
print_permutation(r)
print(r[0])
print(is_trivial(r))

p2 = permutation_from_cycles(10, [[0, 1, 2, 3], [4, 5]])
print(p2)
print_permutation(p2)

print(p == p2)
print(p == r)


def composition(p, q):
    validate_permutation(p)
    validate_permutation(q)
    result = list()
    for i in q:
        result.append(p[i])
    return result

p = [1, 2, 3, 0, 5, 6, 4, 8, 7]
print_permutation(p)
q = composition(p, p)
print_permutation(q)


def inverse(p):
    validate_permutation(p)
    result = list(range(len(p)))
    for i in p:
        result[i] = p.index(i)
    return result


def power(p, i):
    result = p
    while i > 1:
        result = composition(result, p)
        i -= 1
    while i < 0:
        result = inverse(result)
        i += 1
    if i == 0:
        result = trivial_permutation(len(p))
    return result


def period(p):
    result = p
    i = 1
    while not is_trivial(p):
        i += 1
        result = power(p, i)
    return i

p = test_permutation(100)
period(p)
