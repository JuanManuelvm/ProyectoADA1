class Encuestado:
    def __init__(self, id, nombre, experticia, opinion):
        self.id = id
        self.nombre = nombre
        self.experticia = experticia
        self.opinion = opinion

    def __str__(self):
        return f"{self.id}: {self.nombre}, Exp: {self.experticia}, Opin: {self.opinion}"

# Nodo árbol binario para encuestados
class NodoEncuestado:
    def __init__(self, encuestado):
        self.encuestado = encuestado
        self.izq = None
        self.der = None

    def insertar(self, nuevo):
        # Ordenar primero por opinion descendente
        if nuevo.opinion > self.encuestado.opinion:
            if self.izq:
                self.izq.insertar(nuevo)
            else:
                self.izq = NodoEncuestado(nuevo)
        elif nuevo.opinion < self.encuestado.opinion:
            if self.der:
                self.der.insertar(nuevo)
            else:
                self.der = NodoEncuestado(nuevo)
        else:
            # Si empatan, ordenar por experticia descendente
            if nuevo.experticia > self.encuestado.experticia:
                if self.izq:
                    self.izq.insertar(nuevo)
                else:
                    self.izq = NodoEncuestado(nuevo)
            else:
                if self.der:
                    self.der.insertar(nuevo)
                else:
                    self.der = NodoEncuestado(nuevo)

    def en_orden(self, resultado):
        if self.izq:
            self.izq.en_orden(resultado)
        resultado.append(self.encuestado)
        if self.der:
            self.der.en_orden(resultado)

class Pregunta:
    def __init__(self, id_pregunta):
        self.id_pregunta = id_pregunta
        self.raiz = None  # Raíz del árbol de encuestados
        self.encuestados = []

    def agregar_encuestado(self, encuestado):
        if self.raiz is None:
            self.raiz = NodoEncuestado(encuestado)
        else:
            self.raiz.insertar(encuestado)
        self.encuestados.append(encuestado)

    def obtener_ordenados(self):
        resultado = []
        if self.raiz:
            self.raiz.en_orden(resultado)
        return resultado

    def obtener_ordenados(self):
        lista = []
        if self.raiz:
            self.raiz.en_orden(lista)
        return lista

    def promedio_opinion(self):
        if not self.encuestados:
            return 0
        return sum(e.opinion for e in self.encuestados) / len(self.encuestados)
    
    def mediana_opinion(self):
        ordenados = sorted([e.opinion for e in self.encuestados_list])
        n = len(ordenados)
        if n % 2 == 1:
            return ordenados[n // 2]
        else:
            return (ordenados[n // 2 - 1] + ordenados[n // 2]) / 2

    def moda_opinion(self):
        opiniones = [e.opinion for e in self.encuestados_list]
        contador = Counter(opiniones)
        moda, freq = max(contador.items(), key=lambda x: (x[1], x[0]))
        return moda

    def extremismo(self):
        extremos = sum(1 for e in self.encuestados_list if e.opinion == 0 or e.opinion == 10)
        return extremos / len(self.encuestados_list)

    def consenso(self):
        opiniones = [e.opinion for e in self.encuestados_list]
        contador = Counter(opiniones)
        moda_freq = max(contador.values())
        return moda_freq / len(self.encuestados_list)

class Tema:
    def __init__(self, nombre):
        self.nombre = nombre
        self.preguntas = []

    def agregar_pregunta(self, pregunta):
        self.preguntas.append(pregunta)

    def promedio_tema(self):
        if not self.preguntas:
            return 0
        return sum(p.promedio_opinion() for p in self.preguntas) / len(self.preguntas)
