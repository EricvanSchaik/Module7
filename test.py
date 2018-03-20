
def dutch_flag(array: "list"):
    # r indicates the boundary of the red region, b indicates the boundary of the blue region, and i is the index of
    # the current item
    r, i, b = -1, 0, len(array)
    while i < b:
        if array[i] == 1:
            array[r + 1], array[i] = array[i], array[r + 1]
            r += 1
            i += 1
        elif array[i] == 3:
            array[b - 1], array[i] = array[i], array[b - 1]
            b -= 1
        else:
            i += 1
    return array


def check_same_elements(array: "list"):
    for i in range(len(array)):
        for j in range(len(array)):
            if i != j and array[i] == array[j]:
                return True
    return False


def check_same_advanced(array: "list"):
    checked = [0]*len(array)
    for i in range(len(array)):
        if checked[array[i]] == 1:
            return True
        else:
            checked[array[i]] = 1
    return False


def cutter(lengths, log):
    n = len(lengths) - 1 # The amount of lengths
    matrix = [[0 for l in range(log + 1)] for i in range(n + 2)]

    for l in range(0, log + 1):
        matrix[0][l] = l

    for i in range(1, n + 2):
        for l in range(0, log + 1):
            if l - lengths[i - 1] < 0:
                matrix[i][l] = matrix[i-1][l]
            else:
                matrix[i][l] = min(matrix[i - 1][l], matrix[i - 1][l - lengths[i - 1]])

    return matrix[n + 1][log]

newdict = dict()
newdict[1] = 3
newdict[2] = 6
newdict[4] = 9
print(max(newdict))
