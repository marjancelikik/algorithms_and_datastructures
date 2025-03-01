def intersect(a: list, b: list) -> list:
    i = 0
    j = 0
    intersection = []

    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            intersection.append(a[i])
            i += 1
            j += 1

        if i < len(a) and a[i] < b[j]:
            i += 1
        elif j < len(b) and a[i] > b[j]:
            j += 1

    return intersection


print(intersect([1, 2, 3, 7, 8], [1, 4, 8]))
print(intersect([1], [2]))
print(intersect([2], [1]))
print(intersect([1], [1]))
