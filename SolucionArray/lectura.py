import clases

# ============================
# LECTURA DINÁMICA DE ARCHIVOS
# ============================

def leer_archivo_encuesta(nombre_archivo):
    """
    Lee un archivo de texto con el formato especificado y crea la instancia dinámicamente
    """
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            contenido = archivo.read()
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo '{nombre_archivo}'")
        return None, None
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return None, None
    
    # Dividir el contenido en secciones separadas por doble salto de línea
    secciones = contenido.strip().split('\n\n')
    
    if len(secciones) < 2:
        print("Error: El archivo no tiene el formato correcto")
        return None, None
    
    # Procesar la primera sección (encuestados)
    encuestados_data = {}
    lineas_encuestados = secciones[0].strip().split('\n')
    
    for i, linea in enumerate(lineas_encuestados):
        if linea.strip():  # Ignorar líneas vacías
            encuestado = parsear_encuestado(linea.strip(), i + 1)
            if encuestado:
                encuestados_data[encuestado.id] = encuestado
    
    # Procesar las secciones de temas (resto de secciones)
    temas = []
    
    for tema_idx, seccion_tema in enumerate(secciones[1:], 1):
        if seccion_tema.strip():  # Ignorar secciones vacías
            tema = crear_tema_desde_seccion(seccion_tema, tema_idx, encuestados_data)
            if tema:
                temas.append(tema)
    
    return temas, list(encuestados_data.values())

def parsear_encuestado(linea, id_encuestado):
    """
    Parsea una línea de encuestado del formato:
    'Nombre Apellido, Experticia: X, Opinión: Y'
    """
    try:
        # Dividir por comas
        partes = linea.split(',')
        
        if len(partes) != 3:
            print(f"Advertencia: Formato incorrecto en línea de encuestado: {linea}")
            return None
        
        nombre = partes[0].strip()
        
        # Extraer experticia
        experticia_parte = partes[1].strip()
        if not experticia_parte.startswith('Experticia:'):
            print(f"Advertencia: No se encontró 'Experticia:' en: {experticia_parte}")
            return None
        experticia = int(experticia_parte.split(':')[1].strip())
        
        # Extraer opinión
        opinion_parte = partes[2].strip()
        if not opinion_parte.startswith('Opinión:'):
            print(f"Advertencia: No se encontró 'Opinión:' en: {opinion_parte}")
            return None
        opinion = int(opinion_parte.split(':')[1].strip())
        
        return clases.Encuestado(id_encuestado, nombre, experticia, opinion)
    
    except (ValueError, IndexError) as e:
        print(f"Error al parsear encuestado '{linea}': {e}")
        return None

def crear_tema_desde_seccion(seccion_tema, tema_numero, encuestados_data):
    """
    Crea un tema a partir de una sección que contiene las preguntas
    """
    lineas_preguntas = [linea.strip() for linea in seccion_tema.strip().split('\n') if linea.strip()]
    
    if not lineas_preguntas:
        return None
    
    preguntas = []
    
    for pregunta_idx, linea_pregunta in enumerate(lineas_preguntas, 1):
        pregunta = crear_pregunta_desde_linea(linea_pregunta, tema_numero, pregunta_idx, encuestados_data)
        if pregunta:
            preguntas.append(pregunta)
    
    if preguntas:
        tema_nombre = f"Tema {tema_numero}"
        return clases.Tema(tema_nombre, preguntas)
    
    return None

def crear_pregunta_desde_linea(linea_pregunta, tema_numero, pregunta_numero, encuestados_data):
    """
    Crea una pregunta a partir de una línea del formato: {id1, id2, id3, ...}
    """
    try:
        # Remover llaves y espacios
        linea_limpia = linea_pregunta.strip().strip('{}')
        
        if not linea_limpia:
            return None
        
        # Dividir por comas y convertir a enteros
        ids_str = linea_limpia.split(',')
        ids_encuestados = []
        
        for id_str in ids_str:
            id_str = id_str.strip()
            if id_str:
                try:
                    id_encuestado = int(id_str)
                    ids_encuestados.append(id_encuestado)
                except ValueError:
                    print(f"Advertencia: ID inválido '{id_str}' en pregunta")
        
        # Crear lista de encuestados para esta pregunta
        encuestados_pregunta = []
        for id_enc in ids_encuestados:
            if id_enc in encuestados_data:
                encuestados_pregunta.append(encuestados_data[id_enc])
            else:
                print(f"Advertencia: Encuestado con ID {id_enc} no encontrado")
        
        if encuestados_pregunta:
            pregunta_nombre = f"Pregunta {tema_numero}.{pregunta_numero}"
            return clases.Pregunta(pregunta_nombre, encuestados_pregunta)
        
        return None
    
    except Exception as e:
        print(f"Error al crear pregunta desde línea '{linea_pregunta}': {e}")
        return None
