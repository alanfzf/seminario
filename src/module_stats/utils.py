def obtener_campos_pacientes(palabras):
    # Línea 1: 45 chars, líneas 2 y 3: 91 chars
    campos = {}
    campos_lista = ['', '', '']
    sep = ", "

    for palabra in palabras:
        palabra = palabra.strip()
        if len(campos_lista[0]) + len(palabra) + len(sep) <= 45:
            campos_lista[0] += palabra + sep
        elif len(campos_lista[1]) + len(palabra) + len(sep) <= 91:
            campos_lista[1] += palabra + sep
        elif len(campos_lista[2]) + len(palabra) + len(sep) <= 91:
            campos_lista[2] += palabra + sep

    campos['pacientes1'] = campos_lista[0].rstrip(sep)
    campos['pacientes2'] = campos_lista[1].rstrip(sep)
    campos['pacientes3'] = campos_lista[2].rstrip(sep)
    return campos


def obtener_campos_fallecidos(palabras):
    # Línea 1: 78 chars, líneas 2: 33 chars
    campos = {}
    campos_lista = ['', '']
    sep = ", "

    for palabra in palabras:
        palabra = palabra.strip()
        if len(campos_lista[0]) + len(palabra) + len(sep) <= 78:
            campos_lista[0] += palabra + sep
        elif len(campos_lista[1]) + len(palabra) + len(sep) <= 33:
            campos_lista[1] += palabra + sep

    campos['fallecidos1'] = campos_lista[0].rstrip(sep)
    campos['fallecidos2'] = campos_lista[1].rstrip(sep)
    return campos


def obtener_campo_personal(personal):
    # Línea 1: 70 chars, líneas 2: 91
    campos = {}
    campos_lista = ['', '', ]
    sep = ', '

    for persona in personal:
        if len(campos_lista[0]) + len(persona) + len(sep) <= 70:
            campos_lista[0] += persona + sep
        elif len(campos_lista[1]) + len(persona) + len(sep) <= 91:
            campos_lista[1] += persona + sep

    campos['personal1'] = campos_lista[0].rstrip(sep)
    campos['personal2'] = campos_lista[1].rstrip(sep)
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
    elif 'tránsito' in comparar or 'transito' in comparar:
        campos['transito'] = "X"
    elif 'trabajo' in comparar:
        campos['trabajo'] = "X"
    else:
        campos['accidente_otro1'] = accidente
    return campos

def obtener_campos_hospital(nombre):
    campos = {
        'hospital_igss': "",
        'hospital_roosevelt': "",
        'hospital_general': "",
        'hospital_otro': "",
    }
    comparar = nombre.lower()

    if 'i.g.s.s' in comparar:
        campos['hospital_igss'] = "X"
    elif 'roosevelt' in comparar:
        campos['hospital_roosevelt'] = "X"
    elif 'general' in comparar:
        campos['hospital_general'] = "X"
    else:
        campos['hospital_otro'] = nombre
    return campos


def obtener_nombres_edades(personas):
    print(personas)
    datos = personas.split(',')

    nombres = []
    edades = []

    for dato in datos:
        try:
            nombre, edad = dato.split(':')
            nombres.append(nombre.strip())
            edades.append(edad.strip())
        except Exception as e:
            print(f"La cadena \"{dato}\" es incorrecta no tiene el formato nombre: edad")

    return nombres, edades
