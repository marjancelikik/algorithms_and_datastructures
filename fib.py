import pytest


def fib(n: int) -> int:
    if n == 0 or n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)


def test_fib():
    expect_result = 2
    result = fib(2)
    assert expect_result == result
