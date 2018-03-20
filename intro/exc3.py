def encode(nr):
    if nr < 10:
        return nr
    else:
        return chr(nr+55)


def to_k(n, k):
    string = ""
    count = 1
    i = n
    while i >= k:
        i //= k
        count += 1
    while n > k:
        string += str(encode(n // k**(count-1)))
        n %= k ** (count - 1)
        count += -1
    string += str(encode(n))
    return string


def decode(cha):
    try:
        int(cha)
        return int(cha)
    except ValueError:
        return ord(cha)-55


def from_k(s, k):
    n = 0
    count = 1
    while count <= len(s):
        n += decode(s[count-1])*(k**(len(s)-count))
        count += 1
    return n


def convert(k, m, s):
    return to_k(from_k(s, k), m)
