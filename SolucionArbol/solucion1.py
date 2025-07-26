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
            return self.opinion < other.opinion
        self.frecuencia += 1 
        if self.experticia != other.experticia:
            return self.experticia < other.experticia
        return self.id < other.id
        
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
        self.porcentaje_consenso = 0

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
        dato = arnbymoda.arbol_maximo()
        self._moda_opinion = dato.opinion
        n = self.cantidad_encuestados()
        self.porcentaje_consenso = dato.frecuencia / n if n != 0 else 0
        return self._moda_opinion
    
    def _order_consenso(self, other): #aqui se ordena por moda
        self.moda()
        if self.porcentaje_consenso != other.porcentaje_consenso:
            return self.porcentaje_consenso < other.porcentaje_consenso
        return self._moda_opinion > other._moda_opinion
            
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

    def mediana_opinion(self):
        n = self.cantidad_encuestados()
        if n == 0:
            return 0

        # Índices a buscar (uno o dos, dependiendo si n es impar o par)
        target_indices = [n // 2] if n % 2 == 1 else [n // 2 - 1, n // 2]
        resultados = []

        # Recorre el árbol inorden sin usar listas, sólo contador
        def inorden_buscar_mediana(nodo, contador):
            if nodo is None or len(resultados) == len(target_indices):
                return contador

            # Visita izquierda
            contador = inorden_buscar_mediana(nodo.izq, contador)

            # Visita actual
            if contador in target_indices:
                resultados.append(nodo.dato.opinion)
            contador += 1

            # Visita derecha
            return inorden_buscar_mediana(nodo.der, contador)

        inorden_buscar_mediana(self.encuestados.raiz, 0)

        # Retornar resultado
        if n % 2 == 1:
            return resultados[0]
        else:
            return min(resultados[0], resultados[1])

    
    def __gt__(self, other):
        if self.promedio_opinion() != other.promedio_opinion():
            return self.promedio_opinion() < other.promedio_opinion()
        if self.promedio_experticia() != other.promedio_experticia():
            return self.promedio_experticia() < other.promedio_experticia()
        return self.cantidad_encuestados() < other.cantidad_encuestados()

    
class Tema:
    def __init__(self, id):
        self.id = id
        self.preguntas = ArbolRB()
        
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
            return self.promedio_opinion() > other.promedio_opinion()
        if self.promedio_experticia() != other.promedio_experticia():
            return self.promedio_experticia() > other.promedio_experticia()
        return self.cantidad_preguntas() > other.cantidad_preguntas()
   
    
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
    
    def insertar_experticia(self, dato):
        nuevo = NodoRB(dato)
        self.raiz = self._insertar_experticia_rec(self.raiz, nuevo)
        self.raiz.color = NEGRO

    def _insertar_experticia_rec(self, raiz, nodo):
        if raiz is None:
            return nodo
        # Orden descendente por experticia
        if nodo.dato.experticia > raiz.dato.experticia:
            raiz.izq = self._insertar_experticia_rec(raiz.izq, nodo)
            raiz.izq.padre = raiz
        elif nodo.dato.experticia < raiz.dato.experticia:
            raiz.der = self._insertar_experticia_rec(raiz.der, nodo)
            raiz.der.padre = raiz
        else:
            # Experticia igual -> orden por id DESCENDENTE
            if nodo.dato.id > raiz.dato.id:
                raiz.izq = self._insertar_experticia_rec(raiz.izq, nodo)
                raiz.izq.padre = raiz
            else:
                raiz.der = self._insertar_experticia_rec(raiz.der, nodo)
                raiz.der.padre = raiz
        return self._balancear(raiz)


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
    
    def insertar_consenso(self, dato):
        nuevo = NodoRB(dato)
        self.raiz = self._insertar_consenso_rec(self.raiz, nuevo)
        self.raiz.color = NEGRO

    def _insertar_consenso_rec(self, raiz, nodo):
        if raiz is None:
            return nodo
        if nodo.dato._order_consenso(raiz.dato):
            raiz.izq = self._insertar_consenso_rec(raiz.izq, nodo)
            raiz.izq.padre = raiz
        else:
            raiz.der = self._insertar_consenso_rec(raiz.der, nodo)
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
    
    def max_min_mediana(self, mayor=True):
        resultado = None
        mejor_valor = None
        for tema in self.inorden():
            for pregunta in tema.preguntas.inorden():
                mediana = pregunta.mediana_opinion()
                if resultado is None:
                    resultado = pregunta
                    mejor_valor = mediana
                elif mayor:
                    if mediana > mejor_valor:
                        resultado = pregunta
                        mejor_valor = mediana
                    elif mediana == mejor_valor and mediana < resultado.mediana_opinion():
                        resultado = pregunta 
                else:
                    if mediana < mejor_valor:
                        resultado = pregunta
                        mejor_valor = mediana
                    elif mediana == mejor_valor and mediana < resultado.mediana_opinion():
                        resultado = pregunta
        return resultado

    
    def max_min_moda(self, max_bool = True):
        arbolPreguntas = ArbolRB()
        for tema in self.inorden():
            for pregunta in tema.preguntas.inorden():
                pregunta.moda()
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
                pregunta.moda()
                arbolPreguntas.insertar_extremismo(pregunta)
        return arbolPreguntas.arbol_maximo()
    
    def max_consenso(self):
        arbolPreguntas = ArbolRB()
        for tema in self.inorden():
            for pregunta in tema.preguntas.inorden():
                pregunta.moda()
                arbolPreguntas.insertar_consenso(pregunta)
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
    texto = ""
    for tema in temas:
            texto = texto + f"[{round(tema.obtener_opinion_promedio(), 2)}] Tema {tema.id}:\n"
            preguntas = tema.preguntas.inorden()
            for pregunta in preguntas:
                ids = [x.id for x in pregunta.encuestados.inorden()]
                todos_los_encuestados.update(pregunta.encuestados.inorden())
                texto = texto + f" [{round(pregunta.obtener_opinion_promedio(), 2)}] Pregunta {pregunta.id}: {ids}\n"
            texto = texto + "\n"

    return texto, todos_los_encuestados
    


def leer_archivo(nombre_archivo):
    with open(nombre_archivo, 'r', encoding='utf-8') as f:
        lista_encuestados = []
        id_encuestado = 1

        linea = f.readline()
        while linea and linea.strip():  # Participantes hasta línea vacía
            partes = linea.strip().split(',')
            if len(partes) == 3:
                nombre = partes[0].strip()
                experticia = int(partes[1].split(':')[1].strip())
                opinion = int(partes[2].split(':')[1].strip())
                encuestado = Encuestado(id_encuestado, nombre, experticia, opinion)
                lista_encuestados.append(encuestado)
                id_encuestado += 1
            linea = f.readline()
        
        # Saltar líneas vacías hasta comenzar los bloques de preguntas
        while linea and not linea.strip():
            linea = f.readline()
            
        arbol_temas = ArbolRB()
        id_tema = 1
        id_pregunta = 1

        tema_actual = Tema(id_tema)

        while linea:
            linea = linea.strip()
            
            if not linea:
                # Línea vacía (posible separación entre temas)
                if tema_actual.preguntas.raiz is not None:
                    arbol_temas.insertar(tema_actual)
                    id_tema += 1
                    id_pregunta = 1
                    tema_actual = Tema(id_tema)
                # Leer siguiente línea
                linea = f.readline()
                continue

            if linea.startswith('{') and linea.endswith('}'):
                pregunta = Pregunta(str(id_tema) + "." + str(id_pregunta))
                contenido = linea[1:-1].split(',')

                for id_str in contenido:
                    id_limpio = id_str.strip()
                    if id_limpio.isdigit():
                        idx = int(id_limpio)
                        if 1 <= idx <= len(lista_encuestados):
                            pregunta.encuestados.insertar(lista_encuestados[idx - 1])

                tema_actual.preguntas.insertar(pregunta)
                id_pregunta += 1

            linea = f.readline()

        # Insertar el último tema si tiene preguntas
        if tema_actual.preguntas.raiz is not None:
            arbol_temas.insertar(tema_actual)

        return arbol_temas

def generar_salida_txt(arbol_temas, nombre_archivo="output.txt"):
    with open(nombre_archivo, 'w', encoding='utf-8') as f:
        # Resultados de la encuesta
        f.write("Resultados de la encuesta:\n\n")
        temas = arbol_temas.inorden()
        todos_los_encuestados = set()
        arbol, todos_los_encuestados = imprimir_estructura(arbol_temas)
        f.write(arbol)
        
        # Lista de encuestados
        f.write("Lista de encuestados:\n")
        arbol_experticia = ArbolRB()
        for encuestado in todos_los_encuestados:
            arbol_experticia.insertar_experticia(encuestado)

        for encuestado in arbol_experticia.inorden():
            f.write(f" ({encuestado.id}, Nombre:'{encuestado.nombre}', Experticia:{encuestado.experticia}, Opinión:{encuestado.opinion})\n")
        f.write("\n")

        # Resultados analíticos
        f.write("Resultados:\n")
        max_prom = arbol_temas.max_min_promedio(False)
        min_prom = arbol_temas.max_min_promedio(True)
        max_exp = max(tema.preguntas.arbol_maximo() for tema in temas if tema.preguntas.raiz is not None)
        min_exp = min(tema.preguntas.arbol_minimo() for tema in temas if tema.preguntas.raiz is not None)
        max_median = arbol_temas.max_min_mediana(True)
        min_median = arbol_temas.max_min_mediana(False)
        max_moda = arbol_temas.max_min_moda(True)
        min_moda = arbol_temas.max_min_moda(False)
        max_extremo = arbol_temas.max_extremismo()
        max_consenso = arbol_temas.max_consenso()

        f.write(f"  Pregunta con mayor promedio de opinion: [{round(max_prom.obtener_opinion_promedio(), 2)}] Pregunta: {max_prom.id}\n")
        f.write(f"  Pregunta con menor promedio de opinion: [{round(min_prom.obtener_opinion_promedio(), 2)}] Pregunta: {min_prom.id}\n")
        f.write(f"  Pregunta con mayor promedio de experticia: [{round(max_exp.obtener_experticia_promedio(), 2)}] Pregunta: {max_exp.id}\n")
        f.write(f"  Pregunta con menor promedio de experticia: [{round(min_exp.obtener_experticia_promedio(), 2)}] Pregunta: {min_exp.id}\n")
        f.write(f"  Pregunta con Mayor mediana de opinion: [{max_median.mediana_opinion()}] Pregunta: {max_median.id}\n")
        f.write(f"  Pregunta con menor mediana de opinion: [{min_median.mediana_opinion()}] Pregunta: {min_median.id}\n")
        f.write(f"  Pregunta con mayor moda de opinion: [{max_moda._moda_opinion}] Pregunta: {max_moda.id}\n")
        f.write(f"  Pregunta con menor moda de opinion: [{min_moda._moda_opinion}] Pregunta: {min_moda.id}\n")
        f.write(f"  Pregunta con mayor extremismo: [{round(max_extremo._extremismos, 2)}] Pregunta: {max_extremo.id}\n")
        f.write(f"  Pregunta con mayor consenso: [{round(max_consenso.porcentaje_consenso, 2)}] Pregunta: {max_consenso.id}\n")

       
if __name__ == "__main__":
    
    arbol_temas = leer_archivo("Test3.txt")
    generar_salida_txt(arbol_temas, "outputTest.txt")