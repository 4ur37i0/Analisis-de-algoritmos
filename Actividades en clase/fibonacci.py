#Aurelio Rendon Viciego - ICOM
import tkinter as tk
import time
import matplotlib.pyplot as plt # pyright: ignore[reportMissingModuleSource]
import tracemalloc

espacios_dinamica = []
espacios_no_dinamica = []
tiempos_dinamica = []
tiempos_no_dinamica = []
rangos = []


# Usando un diccionario para memorización
def fibonacci_con_dp(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fibonacci_con_dp(n-1, memo) + fibonacci_con_dp(n-2, memo)
    return memo[n]

# Usando el decorador lru_cache de functools para memorización automática
from functools import lru_cache
@lru_cache(maxsize=None)
def fibonacci_con_lru(n):
    if n <= 1:
        return n
    return fibonacci_con_lru(n-1) + fibonacci_con_lru(n-2)


def fibonacci_sin_dp(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        a, b = 0, 1
        for _ in range(n - 1):
            a, b = b, a + b
        return b


for i in range(100):
    rangos.append(i)
    tracemalloc.start()
    inicio = round(time.perf_counter(), 6)
    fibonacci_con_dp(i)
    fin = round(time.perf_counter(), 6)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    tiempos_dinamica.append(fin - inicio)
    espacios_dinamica.append(peak)

for i in range(100):
    
    tracemalloc.start()
    inicio = round(time.perf_counter(), 6)
    fibonacci_sin_dp(i)
    fin = round(time.perf_counter(), 6)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    tiempos_no_dinamica.append(fin - inicio)
    espacios_no_dinamica.append(peak)


fig, g1 = plt.subplots()
g1.plot(rangos, espacios_dinamica, color="blue", label="Dinamica")
g1.plot(rangos, espacios_no_dinamica, color="red", label="No dinamica")
g1.set_xlabel("Rango")
g1.set_ylabel("Espacio")
g1.set_title("Complegidad espacial")
g1.legend()


fig, g2 = plt.subplots()
g2.plot(rangos, tiempos_dinamica, color="blue", label="Dinamica")
g2.plot(rangos, tiempos_no_dinamica, color="red", label="No dinamica")
g2.set_xlabel("Rango")
g2.set_ylabel("Tiempo")
g2.set_title("Complegidad temporal")
g2.legend()
plt.show()

