class Variable():

    def __init__(self, nombre, tipo, tamaño):
        self.nombre = nombre
        self.tipo = tipo
        self.tamaño = tamaño
        self.valor = None
        self.inicializar_valor()

    def obtener_nombre(self):
        return self.nombre
    
    def obtener_tipo(self):
        return self.tipo
    
    def obtener_tamaño(self):
        return self.tamaño
    
    def obtener_valor(self):
        return self.valor
    
    def asignar_valor(self, nuevo_valor, posicion):
        if self.obtener_tipo() == "real" and str(nuevo_valor).replace(".", "").isdigit():
            self.valor = nuevo_valor
        elif self.obtener_tipo() == "array" and type(self.obtener_valor()) is list and posicion < self.obtener_tamaño():
            self.valor[int(posicion)] = nuevo_valor

    def inicializar_valor(self):
        if self.obtener_tamaño():
            self.valor = []
            for _ in range(self.obtener_tamaño()):
                self.valor.append(None)
        else:
            return None