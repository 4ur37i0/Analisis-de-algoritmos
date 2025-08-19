import tkinter as tk
import random
import time
import matplotlib.pyplot as plt
from algorithms import (
    busqueda_lineal,
    busqueda_binaria,
    size_lineal,
    tiempo_lineal,
    size_binarios,
    tiempo_binarios,
)


class BusquedaUI:
    def __init__(self, root):
        self.root = root
        self.root.title('Practica 1')

        self.numeros_generados = []

        # Entrada para cantidad de numeros
        tk.Label(root, text='Cantidad de numeros a generar:').pack(pady=5)
        self.e1 = tk.Entry(root)
        self.e1.pack(pady=5)

        # Listbox con Scrollbar
        frame = tk.Frame(root)
        frame.pack(pady=10, fill="both", expand=True)

        self.scrollbar = tk.Scrollbar(frame)
        self.scrollbar.pack(side="right", fill="y")

        self.mylist = tk.Listbox(frame, yscrollcommand=self.scrollbar.set, width=50, height=15)
        self.mylist.pack(side="left", fill="both", expand=True)

        self.scrollbar.config(command=self.mylist.yview)

        # Botón generar
        start_button = tk.Button(root, text="Generar Números", command=self.generar_numeros)
        start_button.pack(pady=10)

        # Frame oculto para busquedas
        self.frame_busquedas = tk.Frame(root)

        # Busqueda lineal
        tk.Label(self.frame_busquedas, text='Numero a buscar:').pack()
        self.entry_number_to_find = tk.Entry(self.frame_busquedas)
        self.entry_number_to_find.pack(pady=2)
        tk.Button(self.frame_busquedas, text="Busqueda Lineal", command=self.buscar_lineal).pack(pady=5)
        tk.Button(self.frame_busquedas, text="Busqueda Binaria", command=self.buscar_binaria).pack(pady=5)

        tk.Button(self.frame_busquedas, text="Graficas promedio de busquedas", command=self.promedio_busquedas).pack(pady=15)

    def generar_numeros(self):
        self.mylist.delete(0, tk.END)
        try:
            cant = int(self.e1.get())
        except ValueError:
            self.mylist.insert(tk.END, "⚠ Ingresa un numero valido")
            return

        arr = []
        while len(arr) < cant:
            random_number = random.randint(1, 100000)
            if random_number not in arr:
                arr.append(random_number)
                self.mylist.insert(tk.END, str(random_number))

        self.numeros_generados = arr
        self.frame_busquedas.pack(pady=10, fill="x")

    def buscar_lineal(self):
        try:
            num = int(self.entry_number_to_find.get())
        except ValueError:
            self.mylist.insert(tk.END, "⚠ Ingresa un numero valido para busqueda lineal")
            return
        inicio = round(time.perf_counter(), 6)
        idx = busqueda_lineal(self.numeros_generados, num)
        fin = round(time.perf_counter(), 6)
        real_time = fin-inicio
        # print("fin:", fin, " inicio:", inicio, " total:",real_time) # mostrar tiempos
        tiempo_lineal.append(real_time)
        size_lineal.append(len(self.numeros_generados))
        if idx != -1:
            self.mylist.insert(tk.END, f"Lineal: Numero {num} encontrado en índice {idx}")
        else:
            self.mylist.insert(tk.END, f"Lineal: Numero {num} NO encontrado")

    def buscar_binaria(self):
        try:
            num = int(self.entry_number_to_find.get())
        except ValueError:
            self.mylist.insert(tk.END, "⚠ Ingresa un numero valido para busqueda binaria")
            return
        inicio = round(time.perf_counter(), 6)
        idx = busqueda_binaria(self.numeros_generados, num)
        fin = round(time.perf_counter(), 6)
        real_time = fin - inicio
        tiempo_binarios.append(real_time)
        size_binarios.append(len(self.numeros_generados))
        if idx != -1:
            self.mylist.insert(tk.END, f"Binaria: Numero {num} encontrado (indice en lista ordenada: {idx})")
        else:
            self.mylist.insert(tk.END, f"Binaria: Numero {num} NO encontrado")

    def promedio_busquedas(self):
        print("\nDatos de grafica: \nSize_Lineal:", size_lineal, " \nTiempos_Lineal:", tiempo_lineal, "\n\nSize_Binario:",size_binarios, "\nTiempos_Binario:", tiempo_binarios)
        fig, ax = plt.subplots()

        ax.plot(size_lineal, tiempo_lineal, color="blue", label="Lineal")
        ax.plot(size_binarios, tiempo_binarios, color="red", label="Binaria")

        ax.set_xlabel("Size")
        ax.set_ylabel("Time")

        ax.set_title("Grafica de tiempo de busqueda en funcion del tamaño")

        ax.legend()

        plt.show()