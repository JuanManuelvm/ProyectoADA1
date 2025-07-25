from merge import merge_sort_simple

# ============================
# FUNCIONES DE ESTADÍSTICAS
# ============================

def calcular_mediana(valores):
    """Calcula la mediana de una lista de valores"""
    n = len(valores)
    valores_ordenados = merge_sort_simple(valores[:])  # Copia para no modificar original
    
    if n % 2 == 0:
        return (valores_ordenados[n//2 - 1] + valores_ordenados[n//2]) / 2
    else:
        return valores_ordenados[n//2]

def calcular_moda(valores):
    """Calcula la moda de una lista de valores"""
    if not valores:
        return 0
    
    # Contar frecuencias
    frecuencias = {}
    for valor in valores:
        frecuencias[valor] = frecuencias.get(valor, 0) + 1
    
    # Encontrar el valor con mayor frecuencia
    max_freq = max(frecuencias.values())
    modas = [valor for valor, freq in frecuencias.items() if freq == max_freq]
    
    # Si hay múltiples modas, devolver la menor
    return min(modas)

def calcular_promedio(valores):
    """Calcula el promedio de una lista de valores"""
    if not valores:
        return 0.0
    return sum(valores) / len(valores)

