import clases
from merge import merge_sort_temas, merge_sort_encuestados_global
from lectura import leer_archivo_encuesta

# ============================
# DATOS DE LA INSTANCIA DEL ENUNCIADO
# ============================

def crear_instancia_ejemplo():
    """Crea la instancia de ejemplo del enunciado"""
    
    # Encuestados según el enunciado
    encuestados_data = {
        1: clases.Encuestado(1, "Sofia García", 1, 6),
        2: clases.Encuestado(2, "Alejandro Torres", 7, 10),
        3: clases.Encuestado(3, "Valentina Rodriguez", 9, 0),
        4: clases.Encuestado(4, "Juan Lopéz", 10, 1),
        5: clases.Encuestado(5, "Martina Martinez", 7, 0),
        6: clases.Encuestado(6, "Sebastián Pérez", 8, 9),
        7: clases.Encuestado(7, "Camila Fernández", 2, 7),
        8: clases.Encuestado(8, "Mateo González", 4, 7),
        9: clases.Encuestado(9, "Isabella Díaz", 7, 5),
        10: clases.Encuestado(10, "Daniel Ruiz", 2, 9),
        11: clases.Encuestado(11, "Luciana Sánchez", 1, 7),
        12: clases.Encuestado(12, "Lucas Vásquez", 6, 8),
    }

    # Preguntas por tema según el enunciado
    pregunta_1_1 = clases.Pregunta("Pregunta 1.1", [encuestados_data[10], encuestados_data[2]])
    pregunta_1_2 = clases.Pregunta("Pregunta 1.2", [encuestados_data[1], encuestados_data[9], encuestados_data[12], encuestados_data[6]])
    pregunta_2_1 = clases.Pregunta("Pregunta 2.1", [encuestados_data[11], encuestados_data[8], encuestados_data[7]])
    pregunta_2_2 = clases.Pregunta("Pregunta 2.2", [encuestados_data[3], encuestados_data[4], encuestados_data[5]])

    # Temas
    tema_1 = clases.Tema("Tema 1", [pregunta_1_1, pregunta_1_2])
    tema_2 = clases.Tema("Tema 2", [pregunta_2_1, pregunta_2_2])

    return [tema_1, tema_2], list(encuestados_data.values())

# ============================
# FUNCIÓN PRINCIPAL DE PROCESAMIENTO
# ============================

def procesar_encuesta(temas, todos_encuestados):
    """Procesa la encuesta completa y devuelve resultados"""
    
    # Procesar cada tema
    for tema in temas:
        tema.procesar()
    
    # Ordenar temas
    temas_ordenados = merge_sort_temas(temas)
    
    # Ordenar lista global de encuestados
    lista_ordenada_encuestados = merge_sort_encuestados_global(todos_encuestados)
    # Obtener todas las preguntas para estadísticas globales
    todas_preguntas = []
    for tema in temas_ordenados:
        todas_preguntas.extend(tema.preguntas)
    
    # Calcular métricas globales
    estadisticas_globales = calcular_estadisticas_globales(todas_preguntas)
    
    return {
        "temas_ordenados": temas_ordenados,
        "lista_encuestados": [e.mostrar() for e in lista_ordenada_encuestados],
        "estadisticas_globales": estadisticas_globales,
        "todas_preguntas": todas_preguntas
    }

def calcular_estadisticas_globales(preguntas):
    """Calcula las estadísticas globales requeridas"""
    if not preguntas:
        return {}
    
    mayor_prom = max(preguntas, key=lambda p: p.promedio_opinion)
    menor_prom = min(preguntas, key=lambda p: p.promedio_opinion)
    mayor_mediana = max(preguntas, key=lambda p: p.mediana)
    menor_mediana = min(preguntas, key=lambda p: p.mediana)
    mayor_moda = max(preguntas, key=lambda p: p.moda)
    menor_moda = min(preguntas, key=lambda p: p.moda)
    mayor_extremismo = max(preguntas, key=lambda p: p.extremismo)
    mayor_consenso = max(preguntas, key=lambda p: p.consenso)
    
    return {
        "mayor_promedio": mayor_prom,
        "menor_promedio": menor_prom,
        "mayor_mediana": mayor_mediana,
        "menor_mediana": menor_mediana,
        "mayor_moda": mayor_moda,
        "menor_moda": menor_moda,
        "mayor_extremismo": mayor_extremismo,
        "mayor_consenso": mayor_consenso
    }

# ============================
# FUNCIÓN DE VISUALIZACIÓN
# ============================

def mostrar_resultados(resultados):
    """Muestra los resultados en el formato requerido"""
    
    print("\n" + "=" * 60)
    print("Resultados de la encuesta:\n")
    
    # Mostrar temas ordenados
    for tema in resultados["temas_ordenados"]:
        print(tema)
    
    # Mostrar encuestados
    print(f"Lista de encuestados:")
    encuestados_str = "\n".join(f" ({linea})" for linea in resultados["lista_encuestados"])
    print(encuestados_str)
    
    # Mostrar estadísticas globales
    print("\nResultados:")
    stats = resultados["estadisticas_globales"]
    
    print(f"  Pregunta con mayor promedio de opinion: [{stats['mayor_promedio'].promedio_opinion}] {stats['mayor_promedio'].id}")
    print(f"  Pregunta con menor promedio de opinion: [{stats['menor_promedio'].promedio_opinion}] {stats['menor_promedio'].id}")
    print(f"  Pregunta con mayor mediana de opinion: [{stats['mayor_mediana'].mediana}] {stats['mayor_mediana'].id}")
    print(f"  Pregunta con menor mediana de opinion: [{stats['menor_mediana'].mediana}] {stats['menor_mediana'].id}")
    print(f"  Pregunta con mayor valor de moda: [{stats['mayor_moda'].moda}] {stats['mayor_moda'].id}")
    print(f"  Pregunta con menor valor de moda: [{stats['menor_moda'].moda}] {stats['menor_moda'].id}")
    print(f"  Pregunta con mayor extremismo: [{stats['mayor_extremismo'].extremismo}] {stats['mayor_extremismo'].id}")
    print(f"  Pregunta con mayor consenso: [{stats['mayor_consenso'].consenso}] {stats['mayor_consenso'].id}")

# ============================
# EJECUCIÓN PRINCIPAL
# ============================

def main():
    """Función principal"""
    print("SOLUCIÓN USANDO ARREGLOS")
    print("=" * 60)
    
    nombre_archivo = input("Ingrese el nombre del archivo (ejemplo: encuesta1.txt): ").strip()
    temas, todos_encuestados = leer_archivo_encuesta(nombre_archivo)
    
    if temas is None or todos_encuestados is None:
        print("No se pudo cargar el archivo. Usando ejemplo del enunciado.")
        temas, todos_encuestados = crear_instancia_ejemplo()

    # Procesar encuesta
    resultados = procesar_encuesta(temas, todos_encuestados)
    
    # Mostrar resultados
    mostrar_resultados(resultados)
    
    return resultados

# Ejecutar si es el script principal
if __name__ == "__main__":
    resultados = main()