#abecedario en asii va del 97 al 122
import random

def cifrar(palabra):
    cifrada = []
    salto = random.randint(1,25)
    palabraMinuscula = palabra.lower()
    for letra in palabraMinuscula:
        char = int(ord(letra))
        if (char != 32 ): # Con esto maneja los espacios
            if (char == 241 or char == 209 ): # Con esto maneja las ñ Ñ
                print("----")
                char = definirChar( 110 + salto)
            else:
                char = definirChar(char + salto)
        cifrada.append(chr(char))
    print("Cifrada es = ","".join(cifrada))
    return "".join(cifrada)


def definirChar(ascii):
    if (ascii >= 123): return ascii - 122 + 96
    return ascii


def cifradoCesar(cifrada):
    iteraciones = []
    for i in range(1, 26):
        for letra in cifrada:
            char = int(ord(letra))
            if (char != 32 ): # Con esto maneja los espacios
                if (char == 241 or char == 209 ): # Con esto maneja las ñ Ñ
                    char = definirChar( 110 + i)
                else:
                    char = definirChar(char + i)
            iteraciones.append(chr(char))
        print(f"Iteracion {i} ._ {"".join(iteraciones)}")
        iteraciones = []


prueba = cifrar("PALABRA DE PRUEBA")
cifradoCesar(prueba)
