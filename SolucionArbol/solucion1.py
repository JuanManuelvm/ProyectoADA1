ROJO = True
NEGRO = False

class Encuestado:
    def __init__(self, id, nombre, experticia, opinion):
        self.id = id
        self.nombre = nombre
        self.experticia = experticia
        self.opinion = opinion
        self.frecuencia = 1

    def __str__(self):
        return f"(Id: {self.id}, Nombre: {self.nombre}, Exp:{self.experticia}, Opin:{self.opinion}), frecuencia: {self.frecuencia}"
    
    def obtener_experticia_promedio(self):
        return self.experticia
    
    def obtener_opinion_promedio(self):
        return self.opinion
    
    def __gt__(self, other):
        if self.opinion != other.opinion:
            return self.opinion > other.opinion
        self.frecuencia += 1 
        if self.experticia != other.experticia:
            return self.experticia > other.experticia
        return self.id > other.id
        
    def _order_frecuenci(self, other):
        if self.frecuencia != other.frecuencia:
            return self.frecuencia < other.frecuencia
        return self.opinion > other.opinion
    
class Pregunta:
    def __init__(self, id):
        self.id = id
        self.encuestados = ArbolRB()
        self._promedio_opinion = self.promedio_opinion()
        self._moda_opinion = None
        self._extremismos = 0

    def __str__(self):
        ids =", ".join(str(x.id) for x in self.encuestados.inorden())
        return f"[{self.obtener_opinion_promedio()}]Pregunta {self.id}: ({ids})"
    
    def calcular_extremismos(self):
        n = self.cantidad_encuestados()
        self._extremismos = self.encuestados.contar_extremos()/n if n != 0 else None
        return self._extremismos
    
    def obtener_experticia_promedio(self):
        return self.promedio_experticia()
    
    def obtener_opinion_promedio(self):
        return self.promedio_opinion()
    
    def promedio_opinion(self):
        return self.encuestados.obtener_promedio("opinion")

    def promedio_experticia(self):
        return self.encuestados.obtener_promedio("experticia")

    def cantidad_encuestados(self):
        return self.encuestados.contar_nodos()
    
    def moda(self):
        if self.encuestados.raiz is None:
            return None
        arnbymoda = ArbolRB()
        for x in self.encuestados.inorden():
            arnbymoda.insertar_moda(x)
        self._moda_opinion = arnbymoda.arbol_maximo().opinion
        return self._moda_opinion
            
    def _order_frecuenci(self, other): #aqui se ordena por moda
        self.moda()
        if self._moda_opinion != other._moda_opinion:
            return self._moda_opinion < other._moda_opinion
        return self.id > other.id
    
    def _orden_por_extremismo(self, other):
        self.calcular_extremismos()
        if self._extremismos != other._extremismos:
            return self._extremismos < other._extremismos
        return self.id > other.id
    
    def __gt__(self, other):
        if self.promedio_opinion() != other.promedio_opinion():
            return self.promedio_opinion() > other.promedio_opinion()
        if self.promedio_experticia() != other.promedio_experticia():
            return self.promedio_experticia() > other.promedio_experticia()
        return self.cantidad_encuestados() > other.cantidad_encuestados()

    
class Tema:
    def __init__(self, id):
        self.id = id
        self.preguntas = ArbolRB()
        self._moda_opinion = None
        
    def __str__(self):
        preguntasstr = " \n\t".join(str(x) for x in self.preguntas.inorden())
        return f"[{self.obtener_opinion_promedio()}] Tema: {self.id}:\n \t{preguntasstr} \n"
        
    
    def obtener_experticia_promedio(self):
        return self.promedio_experticia()
    
    def obtener_opinion_promedio(self):
        return self.promedio_opinion()
    
    def cantidad_preguntas(self):
        return self.preguntas.contar_nodos()
    
    def promedio_opinion(self):
        return self.preguntas.obtener_promedio("opinion")

    def promedio_experticia(self):
        return self.preguntas.obtener_promedio("experticia")

 
    def __lt__(self, other):
        if self.promedio_opinion() != other.promedio_opinion():
            return self.promedio_opinion() < other.promedio_opinion()
        if self.promedio_experticia() != other.promedio_experticia():
            return self.promedio_experticia() < other.promedio_experticia()
        return self.cantidad_preguntas() < other.cantidad_preguntas()
   
    
class NodoRB:
    def __init__(self, dato):
        self.dato = dato
        self.color = ROJO
        self.izq = None
        self.der = None
        self.padre = None

    def __str__(self):
        return str(self.dato)

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
    
    def insertar_moda(self, dato):
        nuevo = NodoRB(dato)
        self.raiz = self._insertar_moda_rec(self.raiz, nuevo)
        self.raiz.color = NEGRO

    def _insertar_moda_rec(self, raiz, nodo):
        if raiz is None:
            return nodo
        if nodo.dato._order_frecuenci(raiz.dato):
            raiz.izq = self._insertar_moda_rec(raiz.izq, nodo)
            raiz.izq.padre = raiz
        else:
            raiz.der = self._insertar_moda_rec(raiz.der, nodo)
            raiz.der.padre = raiz

        # Balanceo
        raiz = self._balancear(raiz)
        return raiz
    
    def insertar_extremismo(self, dato):
        nuevo = NodoRB(dato)
        self.raiz = self._insertar_extremismo_rec(self.raiz, nuevo)
        self.raiz.color = NEGRO

    def _insertar_extremismo_rec(self, raiz, nodo):
        if raiz is None:
            return nodo
        if nodo.dato._orden_por_extremismo(raiz.dato):
            raiz.izq = self._insertar_extremismo_rec(raiz.izq, nodo)
            raiz.izq.padre = raiz
        else:
            raiz.der = self._insertar_extremismo_rec(raiz.der, nodo)
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
        
    def arbol_maximo(self):
        nodo = self.raiz
        while nodo.der is not None:
            nodo = nodo.der
        return nodo.dato
    
    def arbol_minimo(self):
        nodo = self.raiz
        while nodo.izq is not None:
            nodo = nodo.izq
        return nodo.dato
            
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
            valor = nodo.dato.obtener_opinion_promedio()
        elif atributo == "experticia":
            valor = nodo.dato.obtener_experticia_promedio()
        else:
            valor = 0
        suma_izq, cant_izq = self._sumar_y_contar(nodo.izq, atributo)
        suma_der, cant_der = self._sumar_y_contar(nodo.der, atributo)
        return valor + suma_izq + suma_der, 1 + cant_izq + cant_der
    
    def max_min_moda(self, max_bool = True):
        arbolPreguntas = ArbolRB()
        for tema in self.inorden():
            for pregunta in tema.preguntas.inorden():
                arbolPreguntas.insertar_moda(pregunta)
        if max_bool:
            return arbolPreguntas.arbol_maximo()
        return arbolPreguntas.arbol_minimo()
    
    def max_min_promedio(self, max_bool = True):
        arbolPreguntas = ArbolRB()
        for tema in self.inorden():
            for pregunta in tema.preguntas.inorden():
                arbolPreguntas.insertar(pregunta)
        if max_bool:
            return arbolPreguntas.arbol_maximo()
        return arbolPreguntas.arbol_minimo()
    
    def max_extremismo(self):
        arbolPreguntas = ArbolRB()
        for tema in self.inorden():
            for pregunta in tema.preguntas.inorden():
                arbolPreguntas.insertar_extremismo(pregunta)
        return arbolPreguntas.arbol_maximo()

    def contar_extremos(self):
        return self._contar_extremos(self.raiz)
    def _contar_extremos(self, nodo):
        if nodo is None:
            return 0
        if nodo.dato.opinion == 0 or nodo.dato.opinion == 10:
            return 1 + self._contar_extremos(nodo.izq) + self._contar_extremos(nodo.der)
        return 0 + self._contar_extremos(nodo.izq) + self._contar_extremos(nodo.der)
    
    def __str__(self):
        return str(self.raiz.dato)

def imprimir_estructura(arbol_temas):
    todos_los_encuestados = set()
    temas = arbol_temas.inorden()

    for tema in temas:
        print(tema)
        preguntas = tema.preguntas.inorden()

        for pregunta in preguntas:
            ids_encuestados = [x.id for x in pregunta.encuestados.inorden()]
            todos_los_encuestados.update(ids_encuestados)

    encuestados_str = ", ".join(str(x) for x in todos_los_encuestados)
    print("Lista de encuestados:")
    print(f"   {{{encuestados_str}}}")  
    

       
if __name__ == "__main__":
    
    
    e1 = Encuestado(1, "elkin", 9, 1)
    e2 = Encuestado(2, "elkin", 5, 3)
    e3 = Encuestado(3, "elkin", 10,1)
    e4 = Encuestado(4, "elkin", 30, 10)#moda 6
    
    e5 = Encuestado(10, "elkin", 3, 8)
    e6 = Encuestado(6, "elkin", 6, 10)#moda 8
    
    e7 = Encuestado(15, "elkin", 1, 4)
    e8 = Encuestado(7, "elkin", 1, 7)#moda 4

    p1 = Pregunta(1)
    p2 = Pregunta(2)
    p3 = Pregunta(3)
    

    p1.encuestados.insertar(e1)
    p1.encuestados.insertar(e2)
    p1.encuestados.insertar(e3)
    p1.encuestados.insertar(e4)
    
    p2.encuestados.insertar(e5)
    p2.encuestados.insertar(e6)
    
    p3.encuestados.insertar(e7)
    p3.encuestados.insertar(e8)
    
    #print(p1)
    t1 = Tema(1)
    t2 = Tema(2)
    # print(p1.moda())
    # print(p2.moda())
    # print(p3.moda())
    
    # print(p1.promedio_opinion())
    # print(p2.promedio_opinion())
    # print(p3.promedio_opinion())
    
    t1.preguntas.insertar(p1)
    t1.preguntas.insertar(p2)
    t2.preguntas.insertar(p3)
    # print(t1.moda())
    arbolTemas = ArbolRB()
    arbolTemas.insertar(t1)
    arbolTemas.insertar(t2)
    
    print(arbolTemas.max_extremismo())
    print(p1.calcular_extremismos())
    print(p2.calcular_extremismos())
    print(p3.calcular_extremismos())
    # print(arbolTemas.max_min_moda())
    # print(arbolTemas.max_min_promedio(False))
    # print(p1.moda())
    # print(t1.preguntas.arbol_maximo())
    # imprimir_estructura(arbolTemas)
    # print(t1.preguntas.obtener_promedio("opinion"))
    # print(t2.preguntas.obtener_promedio("opinion"), end='\n\n')
    
    # print(p1.encuestados.obtener_promedio("opinion"))
    # print(p2.encuestados.obtener_promedio("opinion"))
    # print(p3.encuestados.obtener_promedio("opinion"))
    
    # print("\n")



