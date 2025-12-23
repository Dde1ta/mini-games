import time
import math
equ = "x**2 - y**2 = 0"

LHS = equ.split("=")[0]
RHS = equ.split("=")[1]

def avg(l):
    n = len(l)
    s = 0
    for i in l:
        s += i

    return s / n

def binary_search(start: float, end: float, x: float, LHS: str, RHS: int, tolerance: float) -> float:
    while start < end:
        y = start + (end - start) / 2

        res = eval(LHS, {'x': x, 'y': y})
        a = 242424242
        if res < int(RHS) + tolerance:
            start = y

        elif res > int(RHS) - tolerance:
            end = y

        else:
            return y

    return 1e-100

arr = []
times = []

for i in range(20000):
    try:
        start = time.perf_counter_ns()
        arr.append(binary_search(0, i, i / 100, LHS, RHS, 1e-4))
        end = time.perf_counter_ns()
        times.append(end - start)
        print(arr[-1], i / 100)
    except Exception as e:
        print(e)

print(avg(times), sum(times))