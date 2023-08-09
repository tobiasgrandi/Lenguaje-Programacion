from Evaluadores import analizador_semantico

def principal():

    estado = True
    
    while estado:
        accion = ""

        if accion not in ["1", "2"]:
            accion = solicitar_accion()

        if accion == "1":
            ruta = obtener_ruta()
            if comprobar_existe(ruta):
                print(f"Ejecutando {ruta}\n")
                analizador_semantico(ruta)
            else:
                print(f"El archivo {ruta} no existe")
            print()
        elif accion == "2":
            estado = False

def solicitar_accion():
    accion = input("1 - Ejecutar archivo\n2 - Salir\nIngrese la accion: ")
    return accion

def obtener_ruta():
    ruta = input("Ingrese la ruta del archivo: ")

    return ruta

def comprobar_existe(ruta):
    try:
        archivo = open(ruta)
        archivo.close()
    except FileNotFoundError:
        return False
    
    return True

principal()