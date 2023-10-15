def obtener_campos_pacientes(palabras):
    # Línea 1: 48 chars, líneas 2 y 3: 96 chars
    campos = {}
    campos_lista = ['', '', '']
    sep = ", "

    for palabra in palabras:
        palabra = palabra.strip()
        if len(campos_lista[0]) + len(palabra) + len(sep) <= 48:
            campos_lista[0] += palabra + sep
        elif len(campos_lista[1]) + len(palabra) + len(sep) <= 96:
            campos_lista[1] += palabra + sep
        elif len(campos_lista[2]) + len(palabra) + len(sep) <= 96:
            campos_lista[2] += palabra + sep

    campos['pacientes1'] = campos_lista[0].rstrip(sep)
    campos['pacientes2'] = campos_lista[1].rstrip(sep)
    campos['pacientes3'] = campos_lista[2].rstrip(sep)
    return campos


def obtener_campos_fallecidos(palabras):
    # Línea 1: 84 chars, líneas 2: 37 chars
    campos = {}
    campos_lista = ['', '', '']
    sep = ", "

    for palabra in palabras:
        palabra = palabra.strip()
        if len(campos_lista[0]) + len(palabra) + len(sep) <= 84:
            campos_lista[0] += palabra + sep
        elif len(campos_lista[1]) + len(palabra) + len(sep) <= 37:
            campos_lista[1] += palabra + sep

    campos['fallecidos1'] = campos_lista[0].rstrip(sep)
    campos['fallecidos2'] = campos_lista[1].rstrip(sep)
    return campos

def obtener_campo_accidente(accidente):
    campos = {
        'maternidad': "",
        'transito': "",
        'trabajo': "",
        "accidente_otro1": ""
    }
    comparar = accidente.lower()
    if 'maternidad' in comparar:
        campos['maternidad'] = "X"
    elif 'tránsito' in comparar:
        campos['transito'] = "X"
    elif 'trabajo' in comparar:
        campos['trabajo'] = "X"
    else:
        campos['accidente_otro1'] = accidente
    return campos





def obtener_nombres_edades(personas):
    print(personas)
    datos = personas.split(',')

    nombres = []
    edades = []

    for dato in datos:
        nombre, edad = dato.split(':')
        nombres.append(nombre.strip())
        edades.append(edad.strip())

    return nombres, edades

