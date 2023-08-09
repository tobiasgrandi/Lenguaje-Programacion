class Pila():

    def __init__(self):
        self.pila = []

    def apilar(self, elem):
        self.pila.append(elem)

    def desapilar(self):
        if not self.esta_vacia():
            return self.pila.pop()
        
    def esta_vacia(self):
        return self.pila == []

    def ver_tope(self):
        if not self.esta_vacia():
            return self.pila[-1]