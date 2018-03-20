i1, i2 = 0, 1
som = 0
while i2 <= 4000000:
    if i2 % 2 == 0:
        som += i2
    temp = i2
    i2 += i1
    i1 = temp
print(som)
print(str(9001)[:])
print(str(9001)[::-1])
