def counting_sort(a: list) -> list:
    c = [0] * (max(a) + 1)
    b = [0] * len(a)
    for x in a:
        c[x] += 1
    for i in range(1, len(c)):
        c[i] += c[i-1]
    print(c)
    for i in range(len(a) - 1, -1, -1):
        print(c[a[i]])
        b[c[a[i]]-1] = a[i]
        c[a[i]] -= 1
    return b


# print(counting_sort([1, 2, 3, 2, 2, 2, 1, 6, 3]))


def merge_sort(a: list, helper: list, left: int, right: int):
    mid = (left + right) // 2
    merge_sort(a, helper, left, mid)
    merge_sort(a, helper, mid + 1, right)
    _merge(a, helper, left, mid, right)


def _merge(a, helper, left, mid, right):
    pass
    # copy from left to right a to helper
    # current = left
    # l = left
    # r = mid + 1
    # merge left and right parts of helper to a
    # copy mid - l elements from helper to a


def quick_sort(arr: list, left: int, right: int):
    index = partition(arr, left, right)

    if left < index - 1:
        quick_sort(arr, left, index - 1)

    if right > index:
        quick_sort(arr, index, right)


def partition(arr: list, left: int, right: int):
    mid = arr[(left + right) // 2]

    while left <= right:

        while arr[left] < mid:
            left += 1

        while arr[right] > mid:
            right -= 1

        if left <= right:
            tmp = arr[left]
            arr[left] = arr[right]
            arr[right] = tmp
            left += 1
            right -= 1

    return left


a = [1, 2, 1, 4, 2, 9]
print(quick_sort(a, 0, 5))
print(a)
