import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from collections import Counter
import heapq
import random
import json

# ==================== NODO HUFFMAN ====================
class Nodo:
    def __init__(self, caracter=None, frecuencia=0):
        self.caracter = caracter
        self.frecuencia = frecuencia
        self.izquierda = None
        self.derecha = None

    def __lt__(self, otro):
        return self.frecuencia < otro.frecuencia

# ==================== FUNCIONES HUFFMAN ====================
def construir_tabla_frecuencias(texto):
    return Counter(texto)

def construir_arbol_huffman(tabla_frecuencias):
    monticulo = [Nodo(caracter, freq) for caracter, freq in tabla_frecuencias.items()]
    heapq.heapify(monticulo)
    
    while len(monticulo) > 1:
        izq = heapq.heappop(monticulo)
        der = heapq.heappop(monticulo)
        combinado = Nodo(frecuencia=izq.frecuencia + der.frecuencia)
        combinado.izquierda = izq
        combinado.derecha = der
        heapq.heappush(monticulo, combinado)
    
    return monticulo[0]

def generar_codigos(nodo, prefijo="", mapa_codigos=None):
    if mapa_codigos is None:
        mapa_codigos = {}
    if nodo.caracter is not None:
        mapa_codigos[nodo.caracter] = prefijo if prefijo else "0"
    else:
        if nodo.izquierda:
            generar_codigos(nodo.izquierda, prefijo + "0", mapa_codigos)
        if nodo.derecha:
            generar_codigos(nodo.derecha, prefijo + "1", mapa_codigos)
    return mapa_codigos

def codificar_huffman(texto, mapa_codigos):
    return ''.join(mapa_codigos[caracter] for caracter in texto)

def decodificar_huffman(texto_codificado, arbol):
    if not texto_codificado:
        return ""
    resultado = []
    nodo = arbol
    for bit in texto_codificado:
        nodo = nodo.izquierda if bit == '0' else nodo.derecha
        if nodo.caracter:
            resultado.append(nodo.caracter)
            nodo = arbol
    return ''.join(resultado)

# ==================== FUNCIONES CIFRADO CÉSAR ====================
def definir_char(ascii_val):
    """Controla letras fuera del rango del abecedario en minúsculas"""
    if ascii_val >= 123:
        return ascii_val - 122 + 96
    if ascii_val < 97:
        return 122 - (96 - ascii_val)
    return ascii_val

def seleccionar_palabra_guia(frase):
    """Selecciona una palabra guía aleatoria de al menos 3 caracteres"""
    palabra = ""
    lista_palabras = [p for p in frase.split() if len(p) >= 3]
    if lista_palabras:
        palabra = random.choice(lista_palabras)
    return palabra

def cifrar_cesar(texto):
    """Cifra el texto usando César y retorna (texto_cifrado, palabra_guia, desplazamiento)"""
    cifrada = []
    salto = random.randint(1, 25)
    texto_minuscula = texto.lower()
    palabra_guia = seleccionar_palabra_guia(texto_minuscula)
    
    for letra in texto_minuscula:
        char = ord(letra)
        if char == 32:  # Espacio
            cifrada.append(' ')
        elif char == 241 or char == 209:  # ñ o Ñ
            char = definir_char(110 + salto)
            cifrada.append(chr(char))
        elif 97 <= char <= 122:  # a-z
            char = definir_char(char + salto)
            cifrada.append(chr(char))
        else:
            cifrada.append(letra)  # Otros caracteres sin cambio
    
    texto_cifrado = "".join(cifrada)
    return texto_cifrado, palabra_guia, salto

def descifrar_cesar_con_desplazamiento(texto_cifrado, desplazamiento):
    """Descifra el texto César usando el desplazamiento conocido"""
    # Crear diccionario de descifrado
    diccionario = {}
    for i in range(97, 123):
        diccionario[chr(i)] = chr(definir_char(i - desplazamiento))
    
    texto_descifrado = ""
    for letra in texto_cifrado:
        if letra == " ":
            texto_descifrado += " "
        elif letra in diccionario:
            texto_descifrado += diccionario[letra]
        else:
            texto_descifrado += letra
    
    return texto_descifrado

def descifrar_cesar(texto_cifrado, palabra_guia):
    """Descifra el texto César usando la palabra guía (método alternativo)"""
    palabras_texto = texto_cifrado.split()
    palabras_candidatas = [p for p in palabras_texto if len(p) == len(palabra_guia)]
    
    desplazamiento = None
    for palabra in palabras_candidatas:
        if not palabra or not palabra_guia:
            continue
        
        salto = ord(palabra[0]) - ord(palabra_guia[0])
        if salto < 0:
            salto += 26
        
        # Verificar con segunda letra si existe
        if len(palabra) > 1 and len(palabra_guia) > 1:
            prueba = definir_char(ord(palabra[1]) - salto)
            if chr(prueba) != palabra_guia[1]:
                continue
        
        desplazamiento = salto
        break
    
    if desplazamiento is None:
        return None, None
    
    # Crear diccionario de descifrado
    diccionario = {}
    for i in range(97, 123):
        diccionario[chr(i)] = chr(definir_char(i - desplazamiento))
    
    texto_descifrado = ""
    for letra in texto_cifrado:
        if letra == " ":
            texto_descifrado += " "
        elif letra in diccionario:
            texto_descifrado += diccionario[letra]
        else:
            texto_descifrado += letra
    
    return texto_descifrado, desplazamiento

# ==================== APLICACIÓN GUI ====================
class AplicacionCesarHuffman:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Sistema de Cifrado César + Compresión Huffman")
        self.ventana.geometry("900x700")
        
        self.texto_original = ""
        
        # Título
        titulo = tk.Label(ventana, text="🔐 Cifrado César + Compresión Huffman", 
                         font=("Arial", 16, "bold"))
        titulo.pack(pady=10)
        
        # Frame de botones
        frame_botones = tk.Frame(ventana)
        frame_botones.pack(pady=10)
        
        tk.Button(frame_botones, text="📂 Cargar Archivo TXT", 
                 command=self.cargar_archivo, width=20, bg="#4CAF50", 
                 fg="white", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5)
        
        tk.Button(frame_botones, text="🔐 CIFRAR + COMPRIMIR", 
                 command=self.cifrar_y_comprimir, width=20, bg="#2196F3", 
                 fg="white", font=("Arial", 10, "bold")).grid(row=0, column=1, padx=5)
        
        tk.Button(frame_botones, text="🔓 DESCOMPRIMIR + DESCIFRAR", 
                 command=self.descomprimir_y_descifrar, width=25, bg="#FF9800", 
                 fg="white", font=("Arial", 10, "bold")).grid(row=0, column=2, padx=5)
        
        # Área de salida
        tk.Label(ventana, text="📋 Registro de Operaciones:", 
                font=("Arial", 12, "bold")).pack(pady=5)
        
        self.salida = scrolledtext.ScrolledText(ventana, height=30, width=100, 
                                                font=("Courier", 10))
        self.salida.pack(padx=10, pady=10)
        
        # Botón limpiar
        tk.Button(ventana, text="🗑️ Limpiar Registro", 
                 command=self.limpiar_salida, width=20, bg="#f44336", 
                 fg="white").pack(pady=5)
    
    def limpiar_salida(self):
        self.salida.delete(1.0, tk.END)
    
    def cargar_archivo(self):
        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo de texto",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        if ruta:
            try:
                with open(ruta, 'r', encoding='utf-8') as archivo:
                    self.texto_original = archivo.read()
                self.salida.insert(tk.END, f"✅ Archivo cargado exitosamente\n")
                self.salida.insert(tk.END, f"📁 Ruta: {ruta}\n")
                self.salida.insert(tk.END, f"📊 Tamaño: {len(self.texto_original)} caracteres\n")
                self.salida.insert(tk.END, f"{'='*80}\n\n")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar el archivo:\n{str(e)}")
    
    def cifrar_y_comprimir(self):
        if not self.texto_original:
            messagebox.showerror("Error", "Primero carga un archivo de texto")
            return
        
        try:
            self.salida.insert(tk.END, "🔐 INICIANDO PROCESO DE CIFRADO Y COMPRESIÓN...\n")
            self.salida.insert(tk.END, f"{'='*80}\n")
            
            # PASO 1: Cifrado César
            self.salida.insert(tk.END, "\n📝 PASO 1: Aplicando Cifrado César...\n")
            texto_cifrado, palabra_guia, desplazamiento = cifrar_cesar(self.texto_original)
            self.salida.insert(tk.END, f"   ✓ Palabra guía seleccionada: '{palabra_guia}'\n")
            self.salida.insert(tk.END, f"   ✓ Desplazamiento aplicado: {desplazamiento}\n")
            self.salida.insert(tk.END, f"   ✓ Texto cifrado: {texto_cifrado[:100]}...\n")
            
            # PASO 2: Compresión Huffman
            self.salida.insert(tk.END, "\n🗜️ PASO 2: Aplicando Compresión Huffman...\n")
            tabla_freq = construir_tabla_frecuencias(texto_cifrado)
            arbol = construir_arbol_huffman(tabla_freq)
            mapa_codigos = generar_codigos(arbol)
            texto_comprimido = codificar_huffman(texto_cifrado, mapa_codigos)
            
            self.salida.insert(tk.END, f"   ✓ Caracteres únicos: {len(mapa_codigos)}\n")
            
            # Calcular estadísticas
            tam_original = len(self.texto_original.encode('utf-8')) * 8
            tam_cifrado = len(texto_cifrado.encode('utf-8')) * 8
            tam_comprimido = len(texto_comprimido)
            compresion = 100 - (tam_comprimido / tam_original * 100)
            
            self.salida.insert(tk.END, f"\n📊 ESTADÍSTICAS:\n")
            self.salida.insert(tk.END, f"   • Tamaño original: {tam_original} bits\n")
            self.salida.insert(tk.END, f"   • Tamaño después de cifrar: {tam_cifrado} bits\n")
            self.salida.insert(tk.END, f"   • Tamaño comprimido: {tam_comprimido} bits\n")
            self.salida.insert(tk.END, f"   • Compresión lograda: {compresion:.2f}%\n")
            
            # PASO 3: Guardar archivo
            self.salida.insert(tk.END, "\n💾 PASO 3: Guardando archivo...\n")
            ruta_guardar = filedialog.asksaveasfilename(
                title="Guardar archivo cifrado y comprimido",
                defaultextension=".txt",
                filetypes=[("Archivos de texto", "*.txt")]
            )
            
            if ruta_guardar:
                # Crear estructura de datos
                datos = {
                    "palabra_guia": palabra_guia,
                    "desplazamiento": desplazamiento,
                    "mapa_codigos": mapa_codigos,
                    "texto_comprimido": texto_comprimido
                }
                
                with open(ruta_guardar, 'w', encoding='utf-8') as archivo:
                    json.dump(datos, archivo, ensure_ascii=False)
                
                self.salida.insert(tk.END, f"   ✅ Archivo guardado en: {ruta_guardar}\n")
                self.salida.insert(tk.END, f"\n{'='*80}\n")
                self.salida.insert(tk.END, "✅ PROCESO COMPLETADO EXITOSAMENTE\n\n")
                messagebox.showinfo("Éxito", "Archivo cifrado y comprimido guardado correctamente")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en el proceso:\n{str(e)}")
            self.salida.insert(tk.END, f"\n❌ ERROR: {str(e)}\n\n")
    
    def descomprimir_y_descifrar(self):
        try:
            # Cargar archivo comprimido
            ruta = filedialog.askopenfilename(
                title="Seleccionar archivo cifrado y comprimido",
                filetypes=[("Archivos de texto", "*.txt")]
            )
            
            if not ruta:
                return
            
            self.salida.insert(tk.END, "🔓 INICIANDO PROCESO DE DESCOMPRESIÓN Y DESCIFRADO...\n")
            self.salida.insert(tk.END, f"{'='*80}\n")
            
            # Leer archivo
            with open(ruta, 'r', encoding='utf-8') as archivo:
                datos = json.load(archivo)
            
            palabra_guia = datos["palabra_guia"]
            desplazamiento = datos["desplazamiento"]
            mapa_codigos = datos["mapa_codigos"]
            texto_comprimido = datos["texto_comprimido"]
            
            # PASO 1: Descompresión Huffman
            self.salida.insert(tk.END, "\n📤 PASO 1: Descomprimiendo con Huffman...\n")
            
            # Reconstruir árbol desde mapa de códigos
            tabla_temp = {char: 1 for char in mapa_codigos.keys()}
            arbol = construir_arbol_huffman(tabla_temp)
            
            # Método alternativo: usar el mapa directamente para decodificar
            mapa_inverso = {v: k for k, v in mapa_codigos.items()}
            texto_cifrado = ""
            codigo_actual = ""
            for bit in texto_comprimido:
                codigo_actual += bit
                if codigo_actual in mapa_inverso:
                    texto_cifrado += mapa_inverso[codigo_actual]
                    codigo_actual = ""
            
            self.salida.insert(tk.END, f"   ✓ Texto descomprimido\n")
            
            # PASO 2: Descifrado César
            self.salida.insert(tk.END, "\n🔑 PASO 2: Descifrando César...\n")
            self.salida.insert(tk.END, f"   • Palabra guía: '{palabra_guia}'\n")
            self.salida.insert(tk.END, f"   • Desplazamiento guardado: {desplazamiento}\n")
            
            # Usar el desplazamiento guardado directamente
            texto_descifrado = descifrar_cesar_con_desplazamiento(texto_cifrado, desplazamiento)
            
            self.salida.insert(tk.END, f"   ✓ Texto descifrado exitosamente usando desplazamiento guardado\n")
            
            # PASO 3: Guardar resultado
            self.salida.insert(tk.END, "\n💾 PASO 3: Guardando texto original...\n")
            ruta_guardar = filedialog.asksaveasfilename(
                title="Guardar texto descifrado",
                defaultextension=".txt",
                filetypes=[("Archivos de texto", "*.txt")]
            )
            
            if ruta_guardar:
                with open(ruta_guardar, 'w', encoding='utf-8') as archivo:
                    archivo.write(texto_descifrado)
                
                self.salida.insert(tk.END, f"   ✅ Archivo guardado en: {ruta_guardar}\n")
                self.salida.insert(tk.END, f"\n📝 VISTA PREVIA (primeros 500 caracteres):\n")
                self.salida.insert(tk.END, f"{'-'*80}\n")
                self.salida.insert(tk.END, f"{texto_descifrado[:500]}...\n")
                self.salida.insert(tk.END, f"{'-'*80}\n")
                self.salida.insert(tk.END, f"\n{'='*80}\n")
                self.salida.insert(tk.END, "✅ PROCESO COMPLETADO EXITOSAMENTE\n\n")
                messagebox.showinfo("Éxito", "Texto descifrado y guardado correctamente")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en el proceso:\n{str(e)}")
            self.salida.insert(tk.END, f"\n❌ ERROR: {str(e)}\n\n")

# ==================== EJECUTAR APLICACIÓN ====================
if __name__ == "__main__":
    ventana = tk.Tk()
    app = AplicacionCesarHuffman(ventana)
    ventana.mainloop()