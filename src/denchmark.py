import numpy as np
import timeit

# Создаем матрицы
A = np.random.rand(1000, 1000)
B = np.random.rand(1000, 1000)

# Замеряем время умножения матриц
times = timeit.repeat("np.dot(A, B)", number=10, repeat=3)

# Рассчитываем среднее время
avg_time = np.mean(times)

# Выводим среднее время
print("Среднее время умножения матрицы 1000 на 1000 с помощью numpy:", avg_time)



# Создаем матрицы
A = np.random.rand(1000, 1000)
B = np.random.rand(1000, 1000)

# Преобразуем элементы матриц в Decimal
A = A.astype(Decimal)
B = B.astype(Decimal)

# Замеряем время умножения матриц
times = timeit.repeat("np.dot(A, B)", number=10, repeat=3)

# Рассчитываем среднее время
avg_time = np.mean(times)

# Выводим среднее время
print("Среднее время умножения матрицы 1000 на 1000 с элементами Decimal:", avg_time)