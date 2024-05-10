import numpy as np
import timeit


size = 10000

A = np.random.rand(size, size)
B = np.random.rand(size, size)

times = []
for i in range(10):
    start = timeit.default_timer()
    np.dot(A, B)
    end = timeit.default_timer()
    times.append(end - start)

avg_time = np.mean(times)

print("Среднее время умножения матрицы "+str(size)+" на "+str(size)+" с помощью numpy:", avg_time)



from decimal import Decimal

A = np.random.rand(size, size)
B = np.random.rand(size, size)

A = A.astype(Decimal)
B = B.astype(Decimal)

times = []
for i in range(10):
    start = timeit.default_timer()
    np.dot(A, B)
    end = timeit.default_timer()
    times.append(end - start)

avg_time = np.mean(times)

print("Среднее время умножения матрицы "+str(size)+" на "+str(size)+" с элементами Decimal:", avg_time)
