from typing import List
from merge import merge_sort_encuestados, merge_sort_preguntas
from estadisticas import calcular_mediana, calcular_moda, calcular_promedio

# ============================
# CLASES
# ============================

class Encuestado:
    def __init__(self, id: int, nombre: str, experticia: int, opinion: int):
        self.id = id
        self.nombre = nombre
        self.experticia = experticia
        self.opinion = opinion
    
    def mostrar(self):
        return f"{self.id}, Nombre: '{self.nombre}', Experticia:{self.experticia}, Opinion:{self.opinion}"

    def __repr__(self):
        return f"{self.id}"

class Pregunta:
    def __init__(self, id: str, encuestados: List[Encuestado] = None):
        self.id = id
        self.encuestados: List[Encuestado] = encuestados if encuestados else []
        self.promedio_opinion = 0.0
        self.promedio_experticia = 0.0
        self.mediana = 0.0
        self.moda = 0
        self.extremismo = 0.0
        self.consenso = 0.0

    def calcular_estadisticas(self):
        if not self.encuestados:
            return
            
        opiniones = [e.opinion for e in self.encuestados]
        experticias = [e.experticia for e in self.encuestados]

        self.promedio_opinion = round(calcular_promedio(opiniones), 2)
        self.promedio_experticia = round(calcular_promedio(experticias), 2)
        self.mediana = calcular_mediana(opiniones)
        self.moda = calcular_moda(opiniones)

        # Calcular extremismo (porcentaje de opiniones 0 o 10)
        extremos = [op for op in opiniones if op == 0 or op == 10]
        self.extremismo = round((len(extremos) / len(opiniones)), 2)


        # Calcular consenso (porcentaje de la moda)
        moda_count = opiniones.count(self.moda)
        self.consenso = round((moda_count / len(opiniones)), 2)

    def ordenar_encuestados(self):
        self.encuestados = merge_sort_encuestados(self.encuestados)

    def procesar(self):
        self.ordenar_encuestados()
        self.calcular_estadisticas()

    def __repr__(self):
        return f"[{self.promedio_opinion:.2f}] {self.id}: ({', '.join(str(e) for e in self.encuestados)})"

class Tema:
    def __init__(self, nombre: str, preguntas: List[Pregunta] = None):
        self.nombre = nombre
        self.preguntas: List[Pregunta] = preguntas if preguntas else []
        self.promedio_total = 0.0
        self.promedio_experticia = 0.0
        self.total_encuestados = 0

    def calcular_promedios(self):
        if not self.preguntas:
            return
        
        promedios = [p.promedio_opinion for p in self.preguntas]
        experticias = [p.promedio_experticia for p in self.preguntas]
        
        self.promedio_total = round(calcular_promedio(promedios), 2)
        self.promedio_experticia = round(calcular_promedio(experticias), 2)
        self.total_encuestados = sum(len(p.encuestados) for p in self.preguntas)

    def ordenar_preguntas(self):
        # Procesar cada pregunta primero
        for p in self.preguntas:
            p.procesar()
        # Luego ordenar las preguntas
        self.preguntas = merge_sort_preguntas(self.preguntas)

    def procesar(self):
        self.ordenar_preguntas()
        self.calcular_promedios()

    def __repr__(self):
        result = f"[{self.promedio_total:.2f}] {self.nombre}:\n"
        for p in self.preguntas:
            result += f" {p}\n"

        return result
