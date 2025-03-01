def num_change(n: int, change: list, i: int) -> int:
    if i >= len(change) or n < 0:
        return 0
    if 0 == n:
        return 1

    return num_change(n - change[i], change, i) + num_change(n, change, i + 1)


print(num_change(10, [2, 5, 10], 0))
