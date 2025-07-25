# ============================
# FUNCIONES DE ORDENAMIENTO MERGE SORT
# ============================

def merge_sort_simple(arr):
    """Merge sort básico para números"""
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort_simple(arr[:mid])
    right = merge_sort_simple(arr[mid:])
    
    return merge_simple(left, right)

def merge_simple(left, right):
    """Merge básico para números"""
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def merge_sort_encuestados(encuestados):
    """Ordena encuestados por opinión (desc), luego por experticia (desc)"""
    if len(encuestados) <= 1:
        return encuestados
    
    mid = len(encuestados) // 2
    left = merge_sort_encuestados(encuestados[:mid])
    right = merge_sort_encuestados(encuestados[mid:])
    
    return merge_encuestados(left, right)

def merge_encuestados(left, right):
    """Merge para encuestados: opinión desc, luego experticia desc"""
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        # Primero por opinión descendente, luego por experticia descendente
        if (left[i].opinion > right[j].opinion or 
            (left[i].opinion == right[j].opinion and left[i].experticia > right[j].experticia)):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def merge_sort_preguntas(preguntas):
    """Ordena preguntas por promedio opinión (desc), experticia (desc), num encuestados (desc)"""
    if len(preguntas) <= 1:
        return preguntas
    
    mid = len(preguntas) // 2
    left = merge_sort_preguntas(preguntas[:mid])
    right = merge_sort_preguntas(preguntas[mid:])
    
    return merge_preguntas(left, right)

def merge_preguntas(left, right):
    """Merge para preguntas con criterios de desempate"""
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        # Criterios de ordenamiento para preguntas
        if (left[i].promedio_opinion > right[j].promedio_opinion or
            (left[i].promedio_opinion == right[j].promedio_opinion and 
             left[i].promedio_experticia > right[j].promedio_experticia) or
            (left[i].promedio_opinion == right[j].promedio_opinion and 
             left[i].promedio_experticia == right[j].promedio_experticia and
             len(left[i].encuestados) > len(right[j].encuestados))):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def merge_sort_temas(temas):
    """Ordena temas por promedio total (desc), experticia (desc), num encuestados (desc)"""
    if len(temas) <= 1:
        return temas
    
    mid = len(temas) // 2
    left = merge_sort_temas(temas[:mid])
    right = merge_sort_temas(temas[mid:])
    
    return merge_temas(left, right)

def merge_temas(left, right):
    """Merge para temas con criterios de desempate"""
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        # Criterios de ordenamiento para temas
        if (left[i].promedio_total > right[j].promedio_total or
            (left[i].promedio_total == right[j].promedio_total and 
             left[i].promedio_experticia > right[j].promedio_experticia) or
            (left[i].promedio_total == right[j].promedio_total and 
             left[i].promedio_experticia == right[j].promedio_experticia and
             left[i].total_encuestados > right[j].total_encuestados)):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def merge_sort_encuestados_global(encuestados):
    """Ordena encuestados globalmente por experticia (desc), luego por ID (desc)"""
    if len(encuestados) <= 1:
        return encuestados
    
    mid = len(encuestados) // 2
    left = merge_sort_encuestados_global(encuestados[:mid])
    right = merge_sort_encuestados_global(encuestados[mid:])
    
    return merge_encuestados_global(left, right)

def merge_encuestados_global(left, right):
    """Merge para encuestados globales: experticia desc, luego ID desc"""
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if (left[i].experticia > right[j].experticia or 
            (left[i].experticia == right[j].experticia and left[i].id > right[j].id)):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result
