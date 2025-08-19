# Variables globales para gráficas
size_binarios = []
tiempo_binarios = []
size_lineal = []
tiempo_lineal = []


def busqueda_lineal(arr, num):
    for i in range(len(arr)):
        if arr[i] == num:
            return i
    return -1


def busqueda_binaria(arr, target):  # iterativa
    sorted_arr = sorted(arr)
    left, right = 0, len(sorted_arr) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if sorted_arr[mid] == target:
            return mid
        elif sorted_arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1