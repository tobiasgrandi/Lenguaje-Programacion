class Nodo():

    def __init__(self, simbolo, lexema):
        self.simbolo = simbolo
        self.lexema = lexema
        self.hijos = []

    def agregar_hijo(self, nodo):
        self.hijos.append(nodo)

    def obtener_lexema(self):
        return self.lexema
    
    def obtener_simbolo(self):
        return self.simbolo
    
    def obtener_hijos(self):
        return self.hijos
    
    def modificar_lexema(self, nuevo_lexema):
        self.lexema = nuevo_lexema
    
    def girar_hijos(self):
        self.hijos.reverse()