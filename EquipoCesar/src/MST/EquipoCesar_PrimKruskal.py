import heapq
import random



# ----------------------------- KRUSKAL -----------------------------
class UnionFind:
    def __init__(self, elementos):
        self.padre = {elemento: elemento for elemento in elementos}
        self.rango = {elemento: 0 for elemento in elementos}

    def encontrar(self, u): # Encuentra la raiz del conjunto en el que se encuentra el elemento u
        if self.padre[u] != u:
            self.padre[u] = self.encontrar(self.padre[u])
        return self.padre[u]

    def unir(self, u, v): # Une dos conjuntos
        raiz_u = self.encontrar(u)
        raiz_v = self.encontrar(v)

        if raiz_u != raiz_v:
            if self.rango[raiz_u] > self.rango[raiz_v]:
                self.padre[raiz_v] = raiz_u
            elif self.rango[raiz_u] < self.rango[raiz_v]:
                self.padre[raiz_u] = raiz_v
            else:
                self.padre[raiz_v] = raiz_u
                self.rango[raiz_u] += 1

def kruskal(grafo): # Implementacion del Algoritmo de Kruskal para encontrar el arbol de expansion minima.
    # Convierte el grafo a una lista de aristas con (peso, u, v)
    aristas = []
    for u in grafo:
        for v, peso in grafo[u]:
            if (peso, v, u) not in aristas:  # Se asegura de que cada arista se agregue solo una vez
                aristas.append((peso, u, v))
    
    # Ordenar las aristas segun su peso

    print("\nKruskal Grafo ->",grafo)
    print("\nKruskal Aristas ->",aristas)
    aristas.sort()

    # Inicializar la estructura Union-Find
    uf = UnionFind(grafo.keys())

    mst = []
    for peso, u, v in aristas:
        if uf.encontrar(u) != uf.encontrar(v):
            uf.unir(u, v)
            mst.append((u, v, peso))

    return mst




# ----------------------------- PRIM -----------------------------
def prim(grafo):
    mst = []
    
    # Seleccionar un nodo inicial arbitrario
    rand = random.randint(0,len(grafo))
    nodo_inicial = list(grafo.keys())[rand]
    print("\nPrim Nodo inicial ->", nodo_inicial)
    print("\nPrim Grafo ->", grafo)
    
    # Crear una cola de prioridad para seleccionar la arista de menor peso
    bordes = [(peso, nodo_inicial, to) for to, peso in grafo[nodo_inicial]]
    
    heapq.heapify(bordes)
    
    visitados = set([nodo_inicial])
    
    while bordes:
        # Seleccionar la arista de menor peso que conecta un nodo visitado con un nodo no visitado
        peso, frm, to = heapq.heappop(bordes)
        
        if to not in visitados:
            # Añadir la arista al mst
            mst.append((frm, to, peso))
            visitados.add(to)
            
            # Añadir todas las aristas del nuevo nodo al heap
            for siguiente, peso in grafo[to]:
                if siguiente not in visitados:
                    heapq.heappush(bordes, (peso, to, siguiente))
    
    return mst






# Ejemplo
grafo = {
    'a': [('b', 2), ('e', 3)],
    'b': [('a', 2), ('c', 3), ('f', 1)],
    'c': [('b', 3), ('d', 1), ('g', 2)],
    'd': [('c', 1), ('h', 5), ('p', 7)], 
    'e': [('a', 3), ('f', 4), ('i', 4)],
    'f': [('b', 1), ('e', 4), ('g', 3), ('j', 2)],
    'g': [('c', 2), ('f', 3), ('h', 3), ('k', 4)],
    'h': [('d', 5), ('g', 3), ('l', 3), ('m', 6)], 
    'i': [('e', 4), ('j', 3), ('n', 1)],
    'j': [('f', 2), ('i', 3), ('k', 3)],
    'k': [('g', 4), ('j', 3), ('l', 1), ('o', 2)], 
    'l': [('h', 3), ('k', 1), ('q', 5)], 
    'm': [('h', 6), ('r', 1), ('n', 3)],
    'n': [('i', 1), ('m', 3), ('s', 4)], 
    'o': [('k', 2), ('p', 2), ('t', 3)], 
    'p': [('d', 7), ('o', 2), ('s', 1)], 
    'q': [('l', 5), ('r', 4), ('u', 2)], 
    'r': [('m', 1), ('q', 4), ('v', 3)], 
    's': [('n', 4), ('p', 1), ('t', 2), ('w', 5)], 
    't': [('o', 3), ('s', 2), ('u', 1)],
    'u': [('q', 2), ('t', 1), ('w', 4)], 
    'v': [('r', 3), ('w', 1)],
    'w': [('s', 5), ('v', 1), ('x', 2), ('u', 4)], 
    'x': [('w', 2), ('y', 3), ('z', 1)],
    'y': [('x', 3), ('z', 2)], 
    'z': [('x', 1), ('y', 2)], 
}

# Encontrar el mst
mst = prim(grafo)
print("\nPrim Arbol de expansion minima ->", mst)
suma = sum(t[2] for t in mst)
print("\nPrim Peso total ->", suma)



# Encontrar el arbol de expansion minima
mst = kruskal(grafo)
print("\nKruskal Arbol de expansion minima ->", mst)
suma = sum(t[2] for t in mst)
print("\nKruskal Peso total ->", suma)
