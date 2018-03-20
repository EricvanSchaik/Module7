i1 = 1
palindromes = set()
while i1 < 1000:
    i2 = 1
    while i2 < 1000:
        product = i1 * i2
        if str(product) == str(product)[::-1]:
            print(str(product) + " = " + str(i1) + " x " + str(i2))
            palindromes.add(product)
        i2 += 1
    i1 += 1
print("max: " + str(max(palindromes)))
