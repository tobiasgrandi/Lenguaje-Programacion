from Pila import Pila
from Arbol import Nodo
from TAS import TAS
from AnalizadorLexico import obtener_siguiente_componente_lexico

TERMINALES = ["program", "id",  ";" , "dec", "end", "start", ":", "real", "array", "[", "]", "=", "numR", "(", 
            ")", "{", "}", "+", "-", "*", "/", "raiz", "pot", "while", "if", "else", "print", "input", "string", "opRel", "and", "or", "not", ",", ":="] 


def iniciar_pila(pila):
    pesos = Nodo("Pesos", "")
    inicio = Nodo("PROGRAM", "")

    pila.apilar(pesos)
    pila.apilar(inicio)

def analizador_predictivo(ruta):

    pila = Pila()
    iniciar_pila(pila)

    tas = TAS()

    estado = "En proceso"

    posicion = 0
    raiz_arbol = pila.ver_tope()

    componente_lexico, lexema, posicion = obtener_siguiente_componente_lexico(ruta, posicion)

    while estado == "En proceso":

        tope = pila.desapilar()

        if tope.obtener_simbolo() in TERMINALES:
            if tope.obtener_simbolo() == componente_lexico:
                tope.modificar_lexema(lexema)
                componente_lexico, lexema, posicion = obtener_siguiente_componente_lexico(ruta, posicion)
            else:
                estado = f"\nERROR:\nSe esperaba {tope.obtener_simbolo()}\nSe obtuvo {componente_lexico}\n"

        elif tope.obtener_simbolo() == "Pesos":
            if componente_lexico == "Pesos":
                estado = "Exito"
            else:
                estado = f"\nERROR:\nSe esperaba {tope.obtener_simbolo()}\nSe obtuvo {componente_lexico}\n"

        else:
            if tope.obtener_simbolo() != "":
                produccion = tas.obtener_produccion(tope.obtener_simbolo(), componente_lexico)

                if produccion:
                    if produccion == "epsilon":
                        produccion = ""
                    produccion = produccion.split(" ")
                    produccion.reverse()
                    for elem in produccion:
                        nuevo_nodo = Nodo(elem, "")
                        pila.apilar(nuevo_nodo)
                        tope.agregar_hijo(nuevo_nodo)

                    tope.girar_hijos()

                else:
                    estado = f"\nERROR\nNo existe la producción TAS[{tope.obtener_simbolo()}, {componente_lexico}]\n"

    #if estado != "Exito":
    #    print(generar_arbol(raiz_arbol, ""))
    #    print(estado)
    #    print(componente_lexico, "", lexema)
    #else:
    #    print(estado)

    return estado, raiz_arbol#generar_arbol(raiz_arbol, "")


def generar_arbol(nodo_raiz, desplazamiento):

    arbol = f"{desplazamiento}{nodo_raiz.obtener_simbolo()} ({nodo_raiz.obtener_lexema()})"
    
    for hijo in nodo_raiz.obtener_hijos():
        arbol += f"\n{generar_arbol(hijo, desplazamiento + '  ')} "

    return arbol

#analizador_predictivo("Norma.txt")