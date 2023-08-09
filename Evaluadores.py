from Variable import Variable
import math
from AnalizadorSintactico import analizador_predictivo


def eval_program(arbol, estado):
    estado = eval_decvar(arbol.obtener_hijos()[4], estado)
    estado = eval_cuerpo(arbol.obtener_hijos()[8], estado)

    return estado

def eval_decvar(arbol, estado):
    estado = eval_var(arbol.obtener_hijos()[0], estado)
    estado = eval_s_var(arbol.obtener_hijos()[2], estado)

    return estado

def eval_s_var(arbol, estado):
    if arbol.obtener_hijos()[0].obtener_simbolo() != "":
        estado = eval_decvar(arbol.obtener_hijos()[0], estado)
    
    return estado

def eval_var(arbol, estado):
    estado = eval_valores_var(arbol.obtener_hijos()[2], estado, arbol.obtener_hijos()[0].obtener_lexema())

    return estado

def eval_valores_var(arbol, estado, id):
    
    if arbol.obtener_hijos()[0].obtener_simbolo() == "real":
        tipo = "real"
        estado = agregar_variable(estado, id, tipo)

    elif arbol.obtener_hijos()[0].obtener_simbolo() == "array":
        tipo = "array"
        tamaño = arbol.obtener_hijos()[3].obtener_lexema()
        estado = agregar_variable(estado, id, tipo, tamaño)
        
    return estado

def eval_cuerpo(arbol, estado):
    estado = eval_sent(arbol.obtener_hijos()[0], estado)
    estado = eval_s_sent(arbol.obtener_hijos()[1], estado)
    return estado

def eval_s_sent(arbol, estado):
    
    if arbol.obtener_hijos()[0].obtener_simbolo() != "":
        estado = eval_cuerpo(arbol.obtener_hijos()[0], estado)

    return estado

def eval_sent(arbol, estado):

    if arbol.obtener_hijos()[0].obtener_simbolo() == "ASIGN":
        estado = eval_asign(arbol.obtener_hijos()[0], estado)
    elif arbol.obtener_hijos()[0].obtener_simbolo() == "CICLO":
        estado = eval_ciclo(arbol.obtener_hijos()[0], estado)
    elif arbol.obtener_hijos()[0].obtener_simbolo() == "COND":
        estado = eval_cond(arbol.obtener_hijos()[0], estado)
    elif arbol.obtener_hijos()[0].obtener_simbolo() == "LEER":
        estado = eval_leer(arbol.obtener_hijos()[0], estado)
    elif arbol.obtener_hijos()[0].obtener_simbolo() == "ESCRIBIR":
        estado = eval_escribir(arbol.obtener_hijos()[0], estado)

    return estado

def eval_asign(arbol, estado):

    estado = eval_s_id_asign(arbol.obtener_hijos()[1], estado, arbol.obtener_hijos()[0].obtener_lexema())

    return estado

def eval_s_id_asign(arbol, estado, id):

    
    if arbol.obtener_hijos()[0].obtener_simbolo() == ":=":
        
        valor = eval_expar(arbol.obtener_hijos()[1], estado)
        estado = asignar_variable(estado, id, valor)

    elif arbol.obtener_hijos()[0].obtener_simbolo() == "[":
        valor_posicion = eval_expar(arbol.obtener_hijos()[1], estado)
        valor_variable = eval_expar(arbol.obtener_hijos()[4], estado)
        estado = asignar_variable(estado, id, valor_variable, valor_posicion)

    return estado

def eval_expar(arbol, estado):
    
    resultado = eval_sumres(arbol.obtener_hijos()[0], estado)

    return resultado


def eval_sumres(arbol, estado):

    op1 = eval_muldiv(arbol.obtener_hijos()[0], estado)
    resultado = eval_izq_sumres(arbol.obtener_hijos()[1], estado, op1)  

    return resultado

def eval_izq_sumres(arbol, estado, operando):

    if arbol.obtener_hijos()[0].obtener_simbolo() != "":
        op1 = eval_s_sumres(arbol.obtener_hijos()[0], estado, operando)
        resultado = eval_izq_sumres(arbol.obtener_hijos()[1], estado, op1)
    else:
        resultado = operando

    return resultado


def eval_s_sumres(arbol, estado, operando):
    if arbol.obtener_hijos()[0].obtener_simbolo() == "+":
        resultado = operando + eval_muldiv(arbol.obtener_hijos()[1], estado)
    elif arbol.obtener_hijos()[0].obtener_simbolo() == "-":
        resultado = operando - eval_muldiv(arbol.obtener_hijos()[1], estado)
    else:
        resultado = operando
    
    return resultado

def eval_muldiv(arbol, estado):

    op1 = eval_potra(arbol.obtener_hijos()[0], estado)
    resultado = eval_izq_muldiv(arbol.obtener_hijos()[1], estado, op1)

    return resultado

def eval_izq_muldiv(arbol, estado, operando):

    if arbol.obtener_hijos()[0].obtener_simbolo() != "":
        op1 = eval_s_muldiv(arbol.obtener_hijos()[0], estado, operando)
        resultado = eval_izq_muldiv(arbol.obtener_hijos()[1], estado, op1)
    else:
        resultado = operando

    return resultado

def eval_s_muldiv(arbol, estado, operando):

    if arbol.obtener_hijos()[0].obtener_simbolo() == "*":
        resultado = operando * eval_potra(arbol.obtener_hijos()[1], estado)
    elif arbol.obtener_hijos()[0].obtener_simbolo() == "/":
        resultado = operando / eval_potra(arbol.obtener_hijos()[1], estado)
    else:
        resultado = operando

    return resultado

def eval_potra(arbol, estado):

    if arbol.obtener_hijos()[0].obtener_simbolo() == "pot":
        base = eval_expar(arbol.obtener_hijos()[2], estado)
        exponente = eval_expar(arbol.obtener_hijos()[4], estado)
        resultado = base ** exponente

    elif arbol.obtener_hijos()[0].obtener_simbolo() == "raiz":
        base = eval_expar(arbol.obtener_hijos()[2], estado)
        exponente = eval_expar(arbol.obtener_hijos()[4], estado)
        resultado = base ** (1/exponente)

    elif arbol.obtener_hijos()[0].obtener_simbolo() == "(":
        resultado = eval_expar(arbol.obtener_hijos()[1], estado)

    elif arbol.obtener_hijos()[0].obtener_simbolo() == "numR":
        resultado = float(arbol.obtener_hijos()[0].obtener_lexema())

    elif arbol.obtener_hijos()[0].obtener_simbolo() == "id":
        resultado = eval_id_tipo(arbol.obtener_hijos()[1], estado, arbol.obtener_hijos()[0].obtener_lexema())
    
    elif arbol.obtener_hijos()[0].obtener_simbolo() == "-":
        resultado = eval_potra(arbol.obtener_hijos()[0], estado) * -1

    return resultado

def eval_id_tipo(arbol, estado, nombre):

    if arbol.obtener_hijos()[0].obtener_simbolo() != "":
        posicion = eval_expar(arbol.obtener_hijos()[1], estado)
        valor = obtener_valor_variable(estado, nombre, posicion)
    else:
        valor = obtener_valor_variable(estado, nombre)

    return valor

def eval_or(arbol, estado):

    b1 = eval_and(arbol.obtener_hijos()[0], estado)
    resultado = eval_izq_or(arbol.obtener_hijos()[1], estado, b1)

    return resultado

def eval_izq_or(arbol, estado, bool):

    if arbol.obtener_hijos()[0].obtener_simbolo() != "":
        b1 = eval_and(arbol.obtener_hijos()[1], estado)
        resultado = bool or eval_izq_or(arbol.obtener_hijos()[2], estado, b1)
    else:
        resultado = bool

    return resultado

def eval_and(arbol, estado):

    b1 = eval_not(arbol.obtener_hijos()[0], estado)
    resultado = eval_izq_and(arbol.obtener_hijos()[1], estado, b1)

    return resultado

def eval_izq_and(arbol, estado, bool):

    if arbol.obtener_hijos()[0].obtener_simbolo() != "":
        b1 = eval_not(arbol.obtener_hijos()[1], estado)
        resultado = bool and eval_izq_and(arbol.obtener_hijos()[2], estado, b1)
    else:
        resultado = bool

    return resultado

def eval_not(arbol, estado):

    if arbol.obtener_hijos()[0].obtener_simbolo() == "not":
        resultado = not eval_not(arbol.obtener_hijos()[1], estado)
    elif arbol.obtener_hijos()[0].obtener_simbolo() == "[":
        resultado = eval_or(arbol.obtener_hijos()[1], estado)
    else:
        resultado = eval_exprel(arbol.obtener_hijos()[0], estado)

    return resultado

def eval_exprel(arbol, estado):

    expar1 = eval_expar(arbol.obtener_hijos()[0], estado)
    expar2 = eval_expar(arbol.obtener_hijos()[2], estado)
    op_rel = arbol.obtener_hijos()[1].obtener_lexema()

    if op_rel == ">":
        return expar1 > expar2
    elif op_rel == "<":
        return expar1 < expar2
    elif op_rel == ">=":
        return expar1 >= expar2
    elif op_rel == "<=":
        return expar1 <= expar2
    elif op_rel == "=":
        return expar1 == expar2
    elif op_rel == "!=":
        return expar1 != expar2

def eval_condicion(arbol, estado):

    bool = eval_or(arbol.obtener_hijos()[0], estado)

    return bool

def eval_ciclo(arbol, estado):

    bool = eval_condicion(arbol.obtener_hijos()[1], estado)

    while bool:
        estado = eval_cuerpo(arbol.obtener_hijos()[3], estado)
        bool = eval_condicion(arbol.obtener_hijos()[1], estado)
        
    return estado

def eval_cond(arbol, estado):

    bool = eval_condicion(arbol.obtener_hijos()[1], estado)

    estado = eval_cuerpo_cond(arbol.obtener_hijos()[3], estado, bool)


    return estado

def eval_cuerpo_cond(arbol, estado, bool):

    if bool:
        estado = eval_cuerpo(arbol.obtener_hijos()[0], estado)
    elif len(arbol.obtener_hijos()) >= 1:
        estado = eval_s_cuerpo(arbol.obtener_hijos()[1], estado)

    return estado

def eval_s_cuerpo(arbol, estado):

    if arbol.obtener_hijos()[0].obtener_simbolo() != "":
        estado = eval_cuerpo(arbol.obtener_hijos()[2], estado)

    return estado

def eval_leer(arbol, estado): 
    
    string = arbol.obtener_hijos()[2].obtener_lexema()
    variable = arbol.obtener_hijos()[5].obtener_lexema()

    valor_variable = float(input(string))

    return asignar_variable(estado, variable, valor_variable)

def eval_escribir(arbol, estado):

    sec = eval_sec(arbol.obtener_hijos()[2], estado)

    resultado = ""

    for elem in sec:
        resultado += str(elem)

    print(resultado)

    return estado

def eval_sec(arbol, estado):

    sec = []


    if arbol.obtener_hijos():
        sec.append(eval_valores_sec(arbol.obtener_hijos()[0], estado))

        sec.extend(eval_s_valores_sec(arbol.obtener_hijos()[1], estado))


    return sec

def eval_valores_sec(arbol, estado):

    if arbol.obtener_hijos()[0].obtener_simbolo() == "string":
        resultado = arbol.obtener_hijos()[0].obtener_lexema()

    elif arbol.obtener_hijos()[0].obtener_simbolo() == "EXPAR":
        resultado = eval_expar(arbol.obtener_hijos()[0], estado)

    return resultado

def eval_s_valores_sec(arbol, estado):

    if arbol.obtener_hijos()[0].obtener_simbolo() != "":
        resultado = eval_sec(arbol.obtener_hijos()[1], estado)
    else:
        resultado = []

    return resultado


def analizador_semantico(ruta):

    estado, arbol = analizador_predictivo(ruta)

    if estado == "Exito":
        estados = []
        estados = eval_program(arbol, estados)
    else:
        print("ERROR SEMÁNTICO")
        print(estado)


def agregar_variable(estado, nombre, tipo, tamaño = None):

    if tamaño:
        tamaño = int(math.floor(float(tamaño)))

    nueva_var = Variable(nombre, tipo, tamaño)
    estado.append(nueva_var)

    return estado

def asignar_variable(estado, nombre, valor, posicion = None):

    variable = buscar_variable(estado, nombre)

    if posicion:
        posicion = int(math.floor(float(posicion)))

    variable.asignar_valor(valor, posicion)

    return estado

def obtener_valor_variable(estado, nombre, posicion = None):

    variable = buscar_variable(estado, nombre)

    if posicion != None:
        posicion = int(math.floor(float(posicion)))
        return variable.obtener_valor()[posicion]
    else:
        return variable.obtener_valor()


def buscar_variable(estado, nombre):
    
    variable = None
    i = 0

    while variable == None:
        if estado[i].obtener_nombre() == nombre:
            variable = estado[i]

        i += 1

    return variable