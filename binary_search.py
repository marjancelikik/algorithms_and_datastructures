def bs(alist: list, x: int):
    assert len(alist) > 0
    beg = 0
    end = len(alist) - 1
    while beg <= end:
        middle = (beg + end) // 2
        if alist[middle] == x:
            return middle
        if alist[middle] < x:
            beg = middle + 1
        else:
            end = middle - 1

    return -1


print(bs([1, 3, 5, 6, 7, 9], 1))



