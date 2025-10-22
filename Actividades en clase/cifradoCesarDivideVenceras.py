# PROBLEMA ACTUAL: Hay la posibilidad de que la palabra cifrada seleccionada tenga el mismo desplazamiento que la palabra guia pero sin serlo (Falso positivo de desplazamiento)

import random

FRASE = "En un lugar de la Mancha de cuyo nombre no quiero acordarme no ha mucho tiempo que vivia un hidalgo de los de lanza en astillero adarga antigua rocin flaco y galgo corredor"
PALABRA_GUIA = ""
FRASE_CIFRADA = ""

# Sirve para cifrar la frase y poder aplciar el Descifrado
def cifrar():
    global PALABRA_GUIA 
    global FRASE_CIFRADA 
    cifrada = []
    salto = random.randint(1,25)
    fraseMinuscula = FRASE.lower()
    PALABRA_GUIA = selectGuia(fraseMinuscula)
    for letra in fraseMinuscula:
        char = ord(letra)
        if char != 32:
            if char == 241 or char == 209:
                char = definirChar(110 + salto)
            else:
                char = definirChar(char + salto)
        cifrada.append(chr(char))
    FRASE_CIFRADA = "".join(cifrada)

# Es la funcion que ayuda a definir la palabra guia sobre la que se trabajara (inspiracion de "codigo enigma")
def selectGuia(frase):
    palabra = ""
    while (len(palabra) < 3 ):
        lista_palabras = frase.split()
        palabra = random.choice(lista_palabras)
        
    return palabra

# Controla letras fuera del rango del abecedario en minusculas sin acentos
def definirChar(ascii):
    if ascii >= 123:
        return ascii - 122 + 96
    if ascii < 97:
        return 122 - (96 - ascii)
    return ascii

# Funcion principal que aplica el decifrado usando programacion dinamica y supuesto principio de Divide y venceras
def descifradoCesar():
    wordsWithLen = []
    for palabra in FRASE_CIFRADA.split():
        if len(palabra) == len(PALABRA_GUIA):
            wordsWithLen.append(palabra)
    desplazamiento = None
    for palabra in wordsWithLen:
        if not palabra or not PALABRA_GUIA:
            continue
        salto = ord(palabra[0]) - ord(PALABRA_GUIA[0])
        if salto < 0:
            salto += 26
        if len(palabra) > 1:
            prueba = definirChar(ord(palabra[1]) - salto)
            if chr(prueba) != PALABRA_GUIA[1]:
                continue
        desplazamiento = salto
        break
    if desplazamiento is None:
        return ""
    diccionario = {}
    for i in range(97,123):
        diccionario[chr(i)] = chr(definirChar(i - desplazamiento))
    texto_descifrado = ""
    for letra in FRASE_CIFRADA:
        if letra == " ":
            texto_descifrado += " "
        elif letra in diccionario:
            texto_descifrado += diccionario[letra]
        else:
            texto_descifrado += letra
    # Vuelve los registros visibles en consola
    print("\nTexto cifrado:", FRASE_CIFRADA)
    print("Palabra guia:", PALABRA_GUIA)
    print("Desplazamiento encontrado:", desplazamiento)
    print("Texto descifrado:", texto_descifrado,"\n")

cifrar()
descifradoCesar()