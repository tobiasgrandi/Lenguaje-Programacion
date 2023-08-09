import string

FIN_ARCHIVO = ""

def leer_archivo(ruta):
    with open(ruta) as archivo:
        return archivo.read()
        
def leer_car(ruta, posicion):
    cadena_archivo = leer_archivo(ruta)
    if posicion < len(cadena_archivo):
        return cadena_archivo[posicion]
    else:
        return FIN_ARCHIVO



def es_id(ruta, posicion):
    
    estado_inicial = 0
    estado_final = 3
    estado_actual = estado_inicial
    lexema = ''
    componente_lexico = ""

    while estado_actual in [0,1]:
        caracter = leer_car(ruta, posicion)
        estado_actual = delta_id(estado_actual, car_a_sim_id(caracter))
        posicion += 1
        if estado_actual == 1:
            lexema += caracter

    if estado_actual == estado_final:
        posicion -= 1


    componente_lexico = buscar_terminal_id(lexema)

    return estado_actual == estado_final, lexema, componente_lexico, posicion

def delta_id(estado, movimiento):

    if estado == 0 and movimiento == "Letra":
        return 1
    elif estado == 0 and movimiento == "Digito":
        return 2
    elif estado == 0 and movimiento == "Otro":
        return 2
    elif estado == 1 and movimiento == "Digito":
        return 1
    elif estado == 1 and movimiento == "Letra":
        return 1
    elif estado == 1 and movimiento == "Otro":
        return 3

def car_a_sim_id(caracter):

    if caracter == FIN_ARCHIVO:
        return "Otro"
    elif caracter in string.ascii_lowercase or caracter in string.ascii_uppercase:
        return "Letra"
    elif caracter.isdigit():
        return "Digito"
    else:
        return "Otro"
    
def buscar_terminal_id(lexema):

    terminales_id = ["program", "dec", "end", "start", "real", "array", "raiz", "pot", "while", "if", "else", "string", "and", "or", "not", "print", "input"]
    lexema = lexema.lower()
    if lexema in terminales_id:
        return lexema
    else:
        return "id"


def es_num_real(ruta, posicion):
    
    estado_inicial = 0
    estado_final = 4
    estado_actual = estado_inicial
    lexema = ''

    while estado_actual in [0,1,2,5]:
        caracter = leer_car(ruta, posicion)
        estado_actual = delta_real(estado_actual, car_a_sim_real(caracter))
        posicion += 1
        if estado_actual in [1,2,5]:
            lexema += caracter
        
    if estado_actual == estado_final:
            posicion -= 1
    
    componente_lexico = "numR"
    return estado_actual == estado_final, lexema, componente_lexico, posicion

def delta_real(estado, movimiento):

    if estado == 0 and movimiento == "Punto":
        return 3
    elif estado == 0 and movimiento == "Digito":
        return 1
    elif estado == 0 and movimiento == "Otro":
        return 3
    elif estado == 1 and movimiento == "Punto":
        return 2
    elif estado == 1 and movimiento == "Digito":
        return 1
    elif estado == 1 and movimiento == "Otro":
        return 4
    elif estado == 2 and movimiento == "Punto":
        return 3
    elif estado == 2 and movimiento == "Digito":
        return 5
    elif estado == 2 and movimiento == "Otro":
        return 3
    elif estado == 5 and movimiento == "Punto":
        return 3
    elif estado == 5 and movimiento == "Digito":
        return 5
    elif estado == 5 and movimiento == "Otro":
        return 4

def car_a_sim_real(caracter):

    if caracter == FIN_ARCHIVO:
        return "Otro"
    elif caracter == ".":
        return "Punto"
    elif caracter.isdigit():
        return "Digito"
    else:
        return "Otro"



def es_cadena(ruta, posicion):
    
    estado_inicial = 0
    estado_final = 3
    estado_actual = estado_inicial
    lexema = ''

    while estado_actual in [0, 1]:
        caracter = leer_car(ruta, posicion)
        estado_actual = delta_cadena(estado_actual, car_a_sim_cadena(caracter))
        posicion += 1
        if estado_actual in [1, 3]:
            lexema += caracter
    
    
    componente_lexico = "string"
    return estado_actual == estado_final, lexema[1:-1], componente_lexico, posicion

def delta_cadena(estado, movimiento):

    if estado == 0 and movimiento == "Letra":
        return 2
    elif estado == 0 and movimiento == "Digito":
        return 2
    elif estado == 0 and movimiento == "Otro":
        return 2
    elif estado == 0 and movimiento == "Comilla":
        return 1
    elif estado == 1 and movimiento == "Letra":
        return 1
    elif estado == 1 and movimiento == "Digito":
        return 1
    elif estado == 1 and movimiento == "Otro":
        return 1
    elif estado == 1 and movimiento == "Comilla":
        return 3

def car_a_sim_cadena(caracter):

    if caracter == FIN_ARCHIVO:
        return "Otro"
    elif caracter.isalpha():
        return "Letra"
    elif caracter.isdigit():
        return "Digito"
    elif caracter == '"':
        return "Comilla"
    else:
        return "Otro"



def es_simb_especial(ruta, posicion):
    
    caracter = leer_car(ruta, posicion)
    
    simbolos_especiales = ['=',',','(',')','[',']',';','>','<','+','-','*','/','^',':', "!"]

    lexema = ""

    componente_lexico = ""
    if caracter in simbolos_especiales:

        if caracter == ":":
            posicion += 1
            caracter = leer_car(ruta, posicion)
            lexema = ":"
            componente_lexico = ":"
            if caracter == "=":
                lexema = ":="
                componente_lexico = ":="
                posicion += 1

        elif caracter == ";":
            lexema = ";"
            posicion += 1
            componente_lexico = ";"

        elif caracter == ",":
            lexema = ","
            posicion += 1
            componente_lexico = ","

        elif caracter == "(":
            lexema = "("
            posicion += 1
            componente_lexico = "("

        elif caracter == ")":
            lexema = ")"
            posicion += 1
            componente_lexico = ")"

        elif caracter == ">":
            posicion += 1
            caracter = leer_car(ruta, posicion)

            if caracter == "=":
                lexema = ">="
            else:
                lexema = ">"

            posicion += 1
            componente_lexico = "opRel"

        elif caracter == "<":
            posicion += 1
            caracter = leer_car(ruta, posicion)

            if caracter == "=":
                lexema = "<="                
            else:
                lexema = "<"

            posicion += 1
            componente_lexico = "opRel"

        elif caracter == "=":
            lexema = "="
            posicion += 1
            componente_lexico = "opRel"

        elif caracter == "+":
            lexema = "+"
            posicion += 1
            componente_lexico = "+"

        elif caracter == "-":
            lexema = "-"
            posicion += 1
            componente_lexico = "-"
        
        elif caracter == "*":
            lexema = "*"
            posicion += 1
            componente_lexico = "*"

        elif caracter == "/":
            lexema = "/"
            posicion += 1
            componente_lexico = "/"

        elif caracter == "[":
            lexema = "["
            posicion += 1
            componente_lexico = "["

        elif caracter == "]":
            lexema = "]"
            posicion += 1
            componente_lexico = "]"

        elif caracter == "!":
            posicion += 1
            caracter = leer_car(ruta, posicion)
            if caracter == "=":
                lexema = "!="
                posicion += 1
                componente_lexico = "opRel"
            else:
                lexema = "!"
                componente_lexico = "!"

        return True, lexema, componente_lexico, posicion
    
    else:
        return False, lexema, componente_lexico, posicion



def obtener_siguiente_componente_lexico(ruta, posicion):

    caracter = leer_car(ruta, posicion)
    componente_lexico = ""
    lexema = ""


    if caracter == FIN_ARCHIVO:
        componente_lexico = "Pesos"
        return componente_lexico, lexema, posicion


    while ord(caracter) in range(0,33):
        posicion += 1
        caracter = leer_car(ruta, posicion)


    if es_id(ruta, posicion)[0]:
        _, lexema, componente_lexico, posicion = es_id(ruta, posicion) 
    elif es_num_real(ruta, posicion)[0]:
        _, lexema, componente_lexico, posicion = es_num_real(ruta, posicion)
    elif es_cadena(ruta, posicion)[0]:
        _, lexema, componente_lexico, posicion = es_cadena(ruta, posicion)
    elif es_simb_especial(ruta, posicion)[0]:
        _, lexema, componente_lexico, posicion = es_simb_especial(ruta, posicion)
    else:
        componente_lexico = "Error"

    return componente_lexico, lexema, posicion

def prueba(ruta):
    posicion = 0
    componente_lexico = ""
    lexema = ""

    while componente_lexico not in ["Pesos", "Error"] :
        componente_lexico, lexema, posicion = obtener_siguiente_componente_lexico(ruta, posicion)
        print((componente_lexico, lexema, posicion))

#prueba(RUTA)