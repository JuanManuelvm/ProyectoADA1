ROJO = True
NEGRO = False

class Encuestado:
    def __init__(self, id, nombre, experticia, opinion):
        self.id = id
        self.nombre = nombre
        self.experticia = experticia
        self.opinion = opinion

    def __str__(self):
        return f"(Id: {self.id}, Nombre: {self.nombre}, Exp:{self.experticia}, Opin:{self.opinion})"
    
    def __gt__(self, other):
        if self.opinion != other.opinion:
            return self.opinion > other.opinion
        if self.experticia != other.experticia:
            return self.experticia > other.experticia
        return self.id > other.id
        
class Pregunta:
    def __init__(self, id):
        self.id = id
        self.encuestados = ArbolRB()

    def __str__(self):
        return f"(Id: {self.id})"
    
    def promedio_opinion(self):
        return self.encuestados.obtener_promedio("opinion")

    def promedio_experticia(self):
        return self.encuestados.obtener_promedio("experticia")

    def cantidad_encuestados(self):
        return self.encuestados.contar_nodos()

    def __gt__(self, other):
        if self.promedio_opinion() != other.promedio_opinion():
            return self.promedio_opinion() < other.promedio_opinion()
        if self.promedio_experticia() != other.promedio_experticia():
            return self.promedio_experticia() < other.promedio_experticia()
        return self.cantidad_encuestados() < other.cantidad_encuestados()
    
class NodoRB:
    def __init__(self, dato):
        self.dato = dato
        self.color = ROJO
        self.izq = None
        self.der = None
        self.padre = None

    def __str__(self):
        return self.dato

class ArbolRB:
    def __init__(self):
        self.raiz = None

    def insertar(self, dato):
        nuevo = NodoRB(dato)
        self.raiz = self._insertar_rec(self.raiz, nuevo)
        self.raiz.color = NEGRO

    def _insertar_rec(self, raiz, nodo):
        if raiz is None:
            return nodo

        if nodo.dato < raiz.dato:
            raiz.izq = self._insertar_rec(raiz.izq, nodo)
            raiz.izq.padre = raiz
        else:
            raiz.der = self._insertar_rec(raiz.der, nodo)
            raiz.der.padre = raiz

        # Balanceo
        raiz = self._balancear(raiz)
        return raiz

    def _es_rojo(self, nodo):
        return nodo is not None and nodo.color == ROJO

    def _rotar_izquierda(self, h):
        x = h.der
        h.der = x.izq
        if x.izq:
            x.izq.padre = h
        x.izq = h
        x.color = h.color
        h.color = ROJO
        return x

    def _rotar_derecha(self, h):
        x = h.izq
        h.izq = x.der
        if x.der:
            x.der.padre = h
        x.der = h
        x.color = h.color
        h.color = ROJO
        return x

    def _cambiar_colores(self, h):
        h.color = ROJO
        if h.izq: h.izq.color = NEGRO
        if h.der: h.der.color = NEGRO

    def _balancear(self, h):
        if self._es_rojo(h.der) and not self._es_rojo(h.izq):
            h = self._rotar_izquierda(h)
        if self._es_rojo(h.izq) and self._es_rojo(h.izq.izq):
            h = self._rotar_derecha(h)
        if self._es_rojo(h.izq) and self._es_rojo(h.der):
            self._cambiar_colores(h)
        return h

    def inorden(self):
        resultado = []
        self._inorden_rec(self.raiz, resultado)
        return resultado

    def _inorden_rec(self, nodo, resultado):
        if nodo is None:
            return
        self._inorden_rec(nodo.izq, resultado)
        resultado.append(nodo.dato)
        self._inorden_rec(nodo.der, resultado)

    def contar_nodos(self):
        return self._contar(self.raiz)

    def _contar(self, nodo):
        if nodo is None:
            return 0
        return 1 + self._contar(nodo.izq) + self._contar(nodo.der)

    def obtener_promedio(self, atributo):
        suma, cantidad = self._sumar_y_contar(self.raiz, atributo)
        return suma / cantidad if cantidad > 0 else 0

    def _sumar_y_contar(self, nodo, atributo):
        if nodo is None:
            return 0, 0
        if atributo == "opinion":
            valor = nodo.dato.opinion
        elif atributo == "experticia":
            valor = nodo.dato.experticia
        else:
            valor = 0
        suma_izq, cant_izq = self._sumar_y_contar(nodo.izq, atributo)
        suma_der, cant_der = self._sumar_y_contar(nodo.der, atributo)
        return valor + suma_izq + suma_der, 1 + cant_izq + cant_der

        
if __name__ == "__main__":
    e1 = Encuestado(1, "elkin", 9, 6)
    e2 = Encuestado(2, "elkin", 5, 6)
    e3 = Encuestado(3, "elkin", 10,4)
    e5 = Encuestado(4, "elkin", 30, 8)
    e4 = Encuestado(5, "elkin", 3, 8)
    e6 = Encuestado(6, "elkin", 6, 3)
    e7 = Encuestado(8, "elkin", 1, 7)
    e8 = Encuestado(7, "elkin", 1, 7)
    arn = ArbolRB()

    p1 = Pregunta(1)
    p2 = Pregunta(2)
    arnPreguntas = ArbolRB()
    print(e2>e1)

    p1.encuestados.insertar(e1)
    p1.encuestados.insertar(e2)
    p1.encuestados.insertar(e3)
    p1.encuestados.insertar(e4)
    p2.encuestados.insertar(e5)
    p2.encuestados.insertar(e6)
    p2.encuestados.insertar(e7)
    p2.encuestados.insertar(e8)
    arnPreguntas.insertar(p1)
    arnPreguntas.insertar(p2)
    
    for e in arnPreguntas.inorden():
        print(e)
    print(p1.encuestados.obtener_promedio("opinion"))
    print(p2.encuestados.obtener_promedio("opinion"))

    arn.insertar(e1)
    arn.insertar(e2)
    arn.insertar(e3)
    arn.insertar(e4)
    arn.insertar(e5)
    arn.insertar(e6)
    arn.insertar(e8)
    arn.insertar(e7)
    for e in arn.inorden():
        print(e)

