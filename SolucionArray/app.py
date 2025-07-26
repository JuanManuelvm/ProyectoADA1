import clases
from merge import merge_sort_temas, merge_sort_encuestados_global
from lectura import leer_archivo_encuesta

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
    
    # Mayor promedio
    mayor_prom_valor = max(p.promedio_opinion for p in preguntas) # Calculo el maximo promedio
    mayor_prom = min(
        (p for p in preguntas if p.promedio_opinion == mayor_prom_valor),
        key=lambda p: p.id
    ) # Calculo todos los que tengan el mismo maximo promedio y escojo el de menor id

    # Menor promedio
    menor_prom_valor = min(p.promedio_opinion for p in preguntas)
    menor_prom = min(
        (p for p in preguntas if p.promedio_opinion == menor_prom_valor),
        key=lambda p: p.id
    )

    # Para mediana
    mayor_mediana_valor = max(p.mediana for p in preguntas)
    mayor_mediana = min(
        (p for p in preguntas if p.mediana == mayor_mediana_valor),
        key=lambda p: p.id
    )

    menor_mediana_valor = min(p.mediana for p in preguntas)
    menor_mediana = min(
        (p for p in preguntas if p.mediana == menor_mediana_valor),
        key=lambda p: p.id
    )

    # Para moda
    mayor_moda_valor = max(p.moda for p in preguntas)
    mayor_moda = min(
        (p for p in preguntas if p.moda == mayor_moda_valor),
        key=lambda p: p.id
    )

    menor_moda_valor = min(p.moda for p in preguntas)
    menor_moda = min(
        (p for p in preguntas if p.moda == menor_moda_valor),
        key=lambda p: p.id
    )

    # Para extremismo: solo mayor, sin reglas de desempate adicionales
    mayor_extremismo_valor = max(p.extremismo for p in preguntas)
    mayor_extremismo = min(
        (p for p in preguntas if p.extremismo == mayor_extremismo_valor),
        key=lambda p: p.id
    )

    # Para consenso: desempate usando moda más baja
    mayor_consenso_valor = max(p.consenso for p in preguntas)
    candidatas_consenso = [p for p in preguntas if p.consenso == mayor_consenso_valor]

    # Entre las candidatas, elegimos la que tenga la menor moda y menor id si empatan
    mayor_consenso = min(candidatas_consenso, key=lambda p: (p.moda, p.id))

    
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
    """Muestra los resultados en el formato requerido y los guarda en un archivo"""
    
    # Abrimos archivo en modo escritura
    with open("outPutTest.txt", "w", encoding="utf-8") as archivo:
        
        def out(text=""):
            print(text)  # imprime en consola
            print(text, file=archivo)  # escribe en archivo

        out("Resultados de la encuesta:\n")
        
        # Mostrar temas ordenados
        for tema in resultados["temas_ordenados"]:
            out(tema)
        
        # Mostrar encuestados
        out("Lista de encuestados:")
        encuestados_str = "\n".join(f" ({linea})" for linea in resultados["lista_encuestados"])
        out(encuestados_str)
        
        # Mostrar estadísticas globales
        out("\nResultados:")
        stats = resultados["estadisticas_globales"]
        
        out(f"  Pregunta con mayor promedio de opinion: [{stats['mayor_promedio'].promedio_opinion}] {stats['mayor_promedio'].id}")
        out(f"  Pregunta con menor promedio de opinion: [{stats['menor_promedio'].promedio_opinion}] {stats['menor_promedio'].id}")
        out(f"  Pregunta con mayor mediana de opinion: [{stats['mayor_mediana'].mediana}] {stats['mayor_mediana'].id}")
        out(f"  Pregunta con menor mediana de opinion: [{stats['menor_mediana'].mediana}] {stats['menor_mediana'].id}")
        out(f"  Pregunta con mayor valor de moda: [{stats['mayor_moda'].moda}] {stats['mayor_moda'].id}")
        out(f"  Pregunta con menor valor de moda: [{stats['menor_moda'].moda}] {stats['menor_moda'].id}")
        out(f"  Pregunta con mayor extremismo: [{stats['mayor_extremismo'].extremismo}] {stats['mayor_extremismo'].id}")
        out(f"  Pregunta con mayor consenso: [{stats['mayor_consenso'].consenso}] {stats['mayor_consenso'].id}")
        
        print("**** SE GENERO UN ARCHIVO DE SALIDA CON ESTE MISMO RESULTADO ****")

# ============================
# EJECUCIÓN PRINCIPAL
# ============================

def main():
    """Función principal"""
    print("SOLUCIÓN USANDO ARREGLOS")
    print("=" * 60)
    nombre_archivo = input("Ingrese el nombre del archivo (ejemplo: encuesta1.txt): ").strip()
    print("=" * 60)

    temas, todos_encuestados = leer_archivo_encuesta(nombre_archivo)
    
    if temas is None or todos_encuestados is None:
        print("No se pudo cargar el archivo.")
        exit()

    # Procesar encuesta
    resultados = procesar_encuesta(temas, todos_encuestados)
    
    # Mostrar resultados
    mostrar_resultados(resultados)
    
    return resultados

# Ejecutar si es el script principal
if __name__ == "__main__":
    resultados = main()