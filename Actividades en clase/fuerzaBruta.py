#Aurelio Rendon Viciego - D01
import tkinter as tk
import random
import matplotlib.pyplot as plt
from tkinter import *


def distanciaEuclidiana (set1, set2):

    xi = set1[0]
    yi = set1[1]
    xj = set2[0]
    yj = set2[1]
    par1 = ((xi) - (xj))**2
    par2 = ((yi) - (yj))**2
    return (par1 + par2) ** .5


class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualizador - El par mas cercano")
        self.root.geometry("400x800")

        self.parMasCercano = []
        self.distancias = []
        self.pares = []

        # Panel de controles
        self.panel = tk.Frame(root)
        self.panel.pack(pady=6)

        # valores de entrys
        self.tx1 = tk.StringVar()
        self.tx2 = tk.StringVar()
        self.tx3 = tk.StringVar()
        self.tx4 = tk.StringVar()
        self.tx5 = tk.StringVar()

        self.ty1 = tk.StringVar()
        self.ty2 = tk.StringVar()
        self.ty3 = tk.StringVar()
        self.ty4 = tk.StringVar()
        self.ty5 = tk.StringVar()

        self.resultado = tk.StringVar()
       
        tk.Label(root, text="P1 (x,y)").pack(pady=10)
        self.lx1 = tk.Entry(root, textvariable=self.tx1)
        self.lx1.pack(pady=5)
        self.ly1 = tk.Entry(root, textvariable=self.ty1)
        self.ly1.pack(pady=5)

        tk.Label(root, text="P2 (x,y)").pack(pady=10)
        self.lx2 = tk.Entry(root, textvariable=self.tx2)
        self.lx2.pack(pady=5)
        self.ly2 = tk.Entry(root, textvariable=self.ty2)
        self.ly2.pack(pady=5)


        tk.Label(root, text="P3 (x,y)").pack(pady=10)
        self.lx3 = tk.Entry(root, textvariable=self.tx3)
        self.lx3.pack(pady=5)
        self.ly3 = tk.Entry(root, textvariable=self.ty3)
        self.ly3.pack(pady=5)

        tk.Label(root, text="P4 (x,y)").pack(pady=10)
        self.lx4 = tk.Entry(root, textvariable=self.tx4)
        self.lx4.pack(pady=5)
        self.ly4 = tk.Entry(root, textvariable=self.ty4)
        self.ly4.pack(pady=5)

        tk.Label(root, text="P5 (x,y)").pack(pady=10)
        self.lx5 = tk.Entry(root, textvariable=self.tx5)
        self.lx5.pack(pady=5)
        self.ly5 = tk.Entry(root, textvariable=self.ty5)
        self.ly5.pack(pady=5)

        tk.Button(root, text="Llenar Random", command= self.llenarRnmd).pack(pady=5)
        tk.Button(root, text="Calcular", command= self.calcular).pack(pady=5)
        tk.Button(root, text="Graficar", command= self.graficar ).pack(pady=5)
        tk.Button(root, text="Limpiar", command= self.limpiar ).pack(pady=5)

        self.lblResultado = tk.Label(root, textvariable=self.resultado)
        self.lblResultado.pack(pady=10)


    def calcular(self):
        x1 = int(self.lx1.get())
        y1 = int(self.ly1.get())
        x2 = int(self.lx2.get())
        y2 = int(self.ly2.get())
        x3 = int(self.lx3.get())
        y3 = int(self.ly3.get())
        x4 = int(self.lx4.get())
        y4 = int(self.ly4.get())
        x5 = int(self.lx5.get())
        y5 = int(self.ly5.get())
        puntos = [(x1, y1), (x2, y2), (x3, y3), (x4, y4), (x5, y5)]
        minima_dist = float("inf") #infinito
        indx = 0
        for (x, y) in puntos:
            indx =+ 1
            self.pares.append((x,y))
            for (xx, yy) in puntos:
                if (x,y) == (xx,yy):
                    pass
                else: 
                    distancia = distanciaEuclidiana([x,y],[xx,yy])
                    self.distancias.append(distancia)
                    if distancia < minima_dist:
                        self.parMasCercano = [(x,y),(xx,yy)]
                        minima_dist = distancia
                    print(f"({x},{y}) a ({xx},{yy}) = {distancia}")
        if indx:
            self.resultado.set(f"El par mas cercano es -> {self.parMasCercano}")
            print(f"Distancias calculadas = {self.distancias} el mas cercano es {self.parMasCercano}") #muestra de registro
        else:
            self.resultado.set("No hay valores para trabajar")

    def llenarRnmd(self):
        self.tx1.set(str(random.randint(1, 100)))
        self.tx2.set(str(random.randint(1, 100)))
        self.tx3.set(str(random.randint(1, 100)))
        self.tx4.set(str(random.randint(1, 100)))
        self.tx5.set(str(random.randint(1, 100)))

        self.ty1.set(str(random.randint(1, 100)))
        self.ty2.set(str(random.randint(1, 100)))
        self.ty3.set(str(random.randint(1, 100)))
        self.ty4.set(str(random.randint(1, 100)))
        self.ty5.set(str(random.randint(1, 100)))

    def graficar(self):
        fig, ax = plt.subplots()
        xs = [par[0] for par in self.pares]
        ys = [par[1] for par in self.pares]
        ax.scatter(xs, ys, color="blue", marker='o', label="Puntos")
        # Añadir etiquetas (x,y) debajo de cada punto
        for (x, y) in self.pares:
            ax.annotate(f"({x},{y})",
                        (x, y), 
                        textcoords="offset points", 
                        xytext=(0, -12),   # desplazamiento (0 en x, -12 en y)
                        ha='center', fontsize=8, color="black")
        ax.set_title("Gráfica de Puntos")
        ax.set_xlabel("Eje X")
        ax.set_ylabel("Eje Y")
        ax.legend()
        plt.show()

    def limpiar(self):
        self.resultado.set("")
        self.parMasCercano = []
        self.distancias = []
        self.pares = []
        
        self.tx1.set("")
        self.tx2.set("")
        self.tx3.set("")
        self.tx4.set("")
        self.tx5.set("")

        self.ty1.set("")
        self.ty2.set("")
        self.ty3.set("")
        self.ty4.set("")
        self.ty5.set("")



root = tk.Tk()
app = GUI(root)
root.mainloop()



