"""Constantes de Agencia Conectar."""

import os

ERROR_IMPORTACION = "El/los archivos a importar deben existir y ser CSV válidos"
ERROR_EXPORTACION = "Error en la exportación"
ERROR_TALENTO_NO_ENCONTRADO = "Talento no existente"
ERROR_NOMBRE_TALENTO_INVALIDO = (
    "El nombre ingresado no debe estar vacío y debe estar compuesto por caracteres "
    "alfabéticos"
)

TALENTOS_INCOMPATIBLES_INEXISTENTES = (
    "No existen talentos incompatibles para el talento ingresado"
)
TALENTOS_COMPATIBLES_INEXISTENTES = (
    "No existen talentos compatibles para el talento ingresado"
)
COLABORADORES_DIRECTOS_INEXISTENTES = (
    "No existen colaboradores directos para el talento ingresado"
)
OPCION_INVALIDA = "Seleccione una opción válida"

PELICULA_DUPLICADA = "Ignorando película duplicada:"
PELICULA_INEXISTENTE = "Ignorando película inexistente:"

COLABORADORES_DIRECTOS = "Colaboradores directos:"
TALENTOS_COMPATIBLES = "Talentos compatibles:"
TALENTOS_INCOMPATIBLES = "Talentos incompatibles:"

OPCION_RETROCEDER = "**"

OK = "OK"

MENU_PRINCIPAL = """1) Cargar películas
2) Cargar información de ventas 
3) Listar colaboraciones directas 
4) Listar talentos compatibles 
5) Listar talentos incompatibles 
6) Exportar talentos con mayor recaudación 
7) Salir
>>> """

OPCIONES = ["1", "2", "3", "4", "5", "6", "7"]

VOCALES_CON_TILDES = {
    "á": "a",
    "é": "e",
    "í": "i",
    "ó": "o",
    "ú": "u",
    "Á": "A",
    "É": "E",
    "Í": "I",
    "Ó": "O",
    "Ú": "U",
}


SEPARADOR_WINDOWS = "/"
SEPARADOR_LINUX = "\\"

DIRECTORIO_ACTUAL = "."

ESPACIO = " "

EXTENSION_VALIDA = ".csv"

MSG_INGRESO_PELICULAS = "Ingrese el archivo de películas a cargar: "
MSG_INGRESO_VENTAS = "Ingrese el archivo de ventas a cargar: "
MSG_INGRESO_NOMBRE = "Ingrese el nombre de un talento: "
MSG_INGRESO_RUTA = "Ingrese la ruta del archivo a guardar: "

INVALIDO = "invalido"
INEXISTENTE = "inexistente"

HEADER_ARCHIVO = "actor,recaudacion\n"


def menu_principal(funciones, base_datos):
    """Muestra el menú de opciones y realiza la opción elegida.
    En caso de que la opción ingresada sea inválida, se imprime
    un mensaje y se vuelve a pedir."""
    while True:
        opcion_elegida = input(MENU_PRINCIPAL)
        if opcion_elegida in OPCIONES[:5]:
            funciones.get(opcion_elegida)(base_datos, opcion_elegida)
        elif opcion_elegida == OPCIONES[5]:
            funciones.get(opcion_elegida)(base_datos)
        elif opcion_elegida == OPCIONES[6]:
            break
        else:
            print(OPCION_INVALIDA)
            continue


def validar_ruta(ruta: str) -> bool:
    """Valida si la ruta ingresada por parámetro es válida
    (Existe y termine con .csv en el caso de ser un archivo)."""
    if not os.path.exists(ruta):
        return False

    if os.path.isdir(ruta):
        return True

    if ruta.endswith(EXTENSION_VALIDA):
        return True

    return False


def pedir_rutas_entrada(tipo):
    """Pide al usuario una o varias rutas y luego las valida,
    si son válidas las devuelve, En caso de ingresar '**' o
    que las rutas sean inválidas (imprime error y luego) vuelve al menú principal."""
    while True:
        ingreso = input(
            MSG_INGRESO_PELICULAS if tipo == OPCIONES[0] else MSG_INGRESO_VENTAS
        )
        if ingreso == OPCION_RETROCEDER:
            return None
        rutas = ingreso.split()
        hay_error = False
        for ruta in rutas:
            if not validar_ruta(ruta):
                print(ERROR_IMPORTACION)
                hay_error = True
                break
        if hay_error is True:
            continue
        return rutas


def acceder_directorios(rutas):
    """Recorre las rutas ingresadas por parámetro y recursivamente las que sean directorios
    hasta que todas las rutas sean a un archivo '.csv'"""
    for ruta in rutas[:]:
        if not os.path.isdir(ruta):
            continue
        _procesar_directorios(rutas, ruta)
    for ruta in rutas:
        if os.path.isdir(ruta):
            acceder_directorios(rutas)


def _procesar_directorios(rutas, ruta):
    rutas.remove(ruta)
    for busqueda in os.listdir(ruta):
        subruta = os.path.join(ruta, busqueda)
        if subruta not in rutas and validar_ruta(subruta):
            rutas.append(subruta)


def ingresar_datos(archivo, base_datos, contador, tipo):
    """Recorre las lineas de un archivo ya abierto e ingresa
    los datos importados en la base de datos. Devuelve la cantidad de
    lineas ingresadas."""
    for linea in archivo:
        datos_importados = linea.split(",")
        if tipo == "pelicula":
            if datos_importados[0] in base_datos["peliculas"]:
                print(PELICULA_DUPLICADA + f" {datos_importados[0]}")
                continue
            base_datos["peliculas"][datos_importados[0]] = {
                "precio": datos_importados[1],
                "talentos": datos_importados[2].rstrip("\n").split(";"),
            }
        else:
            if datos_importados[0] not in base_datos["peliculas"]:
                print(PELICULA_INEXISTENTE + f" {datos_importados[0]}")
                continue
            base_datos["ventas"][datos_importados[0]] = base_datos["ventas"].get(
                datos_importados[0], 0
            ) + int(datos_importados[1].rstrip("\n"))
        contador += 1
    return contador


def procesar_datos(rutas, base_datos, tipo):
    """Recorre las rutas ingresadas por parámetro y procesa los datos."""
    contador = 0
    for ruta in rutas:
        with open(ruta, "r", encoding="utf8") as archivo:
            archivo.readline()  # Saltear el header
            contador = ingresar_datos(archivo, base_datos, contador, tipo)
    return contador


def manejar_carga_archivos(base_datos, tipo):
    """Realiza la carga de datos en la base de datos. En caso de
    ingresar '**' vuelve al menú principal."""
    rutas = pedir_rutas_entrada(tipo)
    if rutas is None:
        return
    acceder_directorios(rutas)
    try:
        datos_cargados = procesar_datos(
            rutas, base_datos, "pelicula" if tipo == OPCIONES[0] else "venta"
        )
    except (PermissionError, FileNotFoundError, OSError, TypeError):
        print(ERROR_IMPORTACION)
        return
    print(OK + " " + str(datos_cargados))


def limpiar_nombre(nombre):
    """Reemplaza las vocales con tilde por vocales normales (sin tilde)
    y reemplaza el nombre por el mismo en minúsculas."""
    tildes = VOCALES_CON_TILDES
    for letra, reemplazo in tildes.items():
        nombre = nombre.replace(letra, reemplazo)
    return nombre.lower()


def clasificar_nombre(nombre, base_datos):
    """Clasifica el nombre dependiendo si es:
    - INVALIDO : cadena vacía o contiene carácteres distintos a alfabéticos
    - INEXISTENTE : es válido pero no existe en la base de datos
    - VALIDO : es válido y existe, devuelve el nombre"""
    nombre_normalizado_sin_espacios = limpiar_nombre(nombre).replace(ESPACIO, "")
    if (
        not nombre_normalizado_sin_espacios
        or not nombre_normalizado_sin_espacios.isalpha()
    ):
        return INVALIDO
    peliculas = base_datos["peliculas"]
    for pelicula in peliculas.values():
        talentos = pelicula["talentos"]
        for talento in talentos:
            if limpiar_nombre(nombre) == limpiar_nombre(talento):
                return talento
    return INEXISTENTE


def pedir_nombre(base_datos) -> str:
    """Pide al usuario el ingreso de un nombre e imprime el error correspondiente a
    la clasificación del mismo para luego volver a pedir al usuario el ingreso.
    En caso de que sea válido, lo devuelve."""
    while True:
        ingreso = input(MSG_INGRESO_NOMBRE)
        if ingreso == OPCION_RETROCEDER:
            return None
        clasificacion = clasificar_nombre(ingreso, base_datos)
        if clasificacion not in [INVALIDO, INEXISTENTE]:
            return clasificacion

        if clasificacion == INVALIDO:
            print(ERROR_NOMBRE_TALENTO_INVALIDO)

        elif clasificacion == INEXISTENTE:
            print(ERROR_TALENTO_NO_ENCONTRADO)

        continue


def listar_colaboradores_directos(base_datos, nombre):
    """Dado un talento, lista los colaboradores directos del mismo.
    Es decir, aquellos que han trabajado directamente con el talento."""
    talentos_encontrados = []
    for pelicula in base_datos["peliculas"].values():
        if nombre not in pelicula["talentos"]:
            continue
        lista = pelicula["talentos"][::]
        lista.remove(nombre)
        for talento in lista:
            if talento in talentos_encontrados:
                continue
            talentos_encontrados.append(talento)
    return talentos_encontrados


def imprimir_talentos(lista, opcion_elegida):
    """Imprime los talentos recorridos de la lista, y
    dependiendo de la opción elegida modifica el encabezado."""
    if opcion_elegida == OPCIONES[2]:
        print(COLABORADORES_DIRECTOS)
    elif opcion_elegida == OPCIONES[3]:
        print(TALENTOS_COMPATIBLES)
    else:
        print(TALENTOS_INCOMPATIBLES)
    for i, talento in enumerate(lista):
        print(f"{i+1}. {talento}")


def procesar_talentos_compatibles(
    nuevos_colaboradores, nombre, colaboradores_directos, talentos_compatibles
):
    """Recorre los colaboradores directos de un colaborador directo del inicial
    y lo agrega a compatibles si es compatible."""
    for talento in nuevos_colaboradores:
        if (
            talento not in talentos_compatibles
            and talento != nombre
            and talento not in colaboradores_directos
        ):
            talentos_compatibles.append(talento)


def _listar_talentos_compatibles(
    base_datos, nombre, colaboradores_directos, talentos_compatibles, procesados
):
    """Recorre los colaboradores directos del talento y agrega los colaboradores directos
    de los colaboradores directos a los talentos_compatibles del inicial recursivamente.
    """
    for colaborador_directo in colaboradores_directos:
        if colaborador_directo in procesados:
            continue
        procesados.append(colaborador_directo)

        nuevos_colaboradores = listar_colaboradores_directos(
            base_datos, colaborador_directo
        )
        if not nuevos_colaboradores:
            continue

        procesar_talentos_compatibles(
            nuevos_colaboradores, nombre, colaboradores_directos, talentos_compatibles
        )

        _listar_talentos_compatibles(
            base_datos,
            colaborador_directo,
            nuevos_colaboradores,
            talentos_compatibles,
            procesados,
        )

    return talentos_compatibles


def listar_talentos_compatibles(base_datos, nombre):
    """Lista los talentos compatibles del talento inicial. En
    caso de que no haya talentos compatibles o colaboradores directos
    imprime un mensaje de error."""
    colaboradores_directos = listar_colaboradores_directos(base_datos, nombre)
    if not colaboradores_directos:
        print(TALENTOS_COMPATIBLES_INEXISTENTES)
        return []
    talentos_compatibles = _listar_talentos_compatibles(
        base_datos, nombre, colaboradores_directos, [], [nombre]
    )
    if not talentos_compatibles:
        print(TALENTOS_COMPATIBLES_INEXISTENTES)
    return talentos_compatibles


def listar_talentos_totales(base_datos):
    """Lista los talentos totales de la base de datos."""
    talentos = []
    for pelicula in base_datos["peliculas"].values():
        for talento in pelicula["talentos"]:
            if talento not in talentos:
                talentos.append(talento)
    return talentos


def _listar_talentos_incompatibles(base_datos, nombre, conectados):
    """Agrega a la lista 'conectados' todos los que
    se conecten de alguna forma con el talento inicial."""
    if nombre not in conectados:
        conectados.append(nombre)
        for talento in listar_colaboradores_directos(base_datos, nombre):
            _listar_talentos_incompatibles(base_datos, talento, conectados)


def listar_talentos_incompatibles(base_datos, nombre):
    """Lista los talentos incompatibles del talento inicial, es decir, aquellos
    que no se conectan con el talento de ninguna forma"""
    talentos_incompatibles = []
    todos = listar_talentos_totales(base_datos)
    conectados = []
    _listar_talentos_incompatibles(base_datos, nombre, conectados)
    for talento in todos:
        if talento not in conectados:
            talentos_incompatibles.append(talento)
    if not talentos_incompatibles:
        print(TALENTOS_INCOMPATIBLES_INEXISTENTES)
    return talentos_incompatibles


def listar_relaciones(base_datos, opcion_elegida):
    """Dependiendo de la opción elegida lista los talentos encontrados y los imprime."""
    nombre = pedir_nombre(base_datos)
    if nombre is None:
        return
    if opcion_elegida == OPCIONES[2]:
        talentos_encontrados = listar_colaboradores_directos(base_datos, nombre)
        if not talentos_encontrados:
            print(COLABORADORES_DIRECTOS_INEXISTENTES)
            return
    elif opcion_elegida == OPCIONES[3]:
        talentos_encontrados = listar_talentos_compatibles(base_datos, nombre)
    else:
        talentos_encontrados = listar_talentos_incompatibles(base_datos, nombre)
    if not talentos_encontrados:
        return
    imprimir_talentos(sorted(talentos_encontrados), opcion_elegida)


def pedir_ruta_salida():
    """Pide al usuario el ingreso de una ruta de salida válida.
    Es decir, que no sea '**' (vuelve al menú), que exista, que no
    contenga espacios y sea un archivo '.csv'."""
    while True:
        ingreso = input(MSG_INGRESO_RUTA)
        if ingreso == OPCION_RETROCEDER:
            return None

        if ESPACIO in ingreso or not ingreso.endswith(EXTENSION_VALIDA):
            print(ERROR_EXPORTACION)
            continue

        ingreso = ingreso.replace(SEPARADOR_LINUX, SEPARADOR_WINDOWS)

        if SEPARADOR_WINDOWS not in ingreso:
            directorio = DIRECTORIO_ACTUAL
        else:
            directorio = ingreso.rsplit(SEPARADOR_WINDOWS, 1)[0]

        if not os.path.exists(directorio):
            print(ERROR_EXPORTACION)
            continue

        return ingreso


def calcular_recaudacion(base_datos, talento):
    """Calcula la recaudación total del talento en base a las
    películas en las que actuó."""
    recaudacion = 0
    for pelicula in base_datos["peliculas"]:
        datos_pelicula = base_datos["peliculas"][pelicula]
        if talento in datos_pelicula["talentos"] and pelicula in base_datos["ventas"]:
            precio = int(datos_pelicula["precio"])
            ventas = int(base_datos["ventas"][pelicula])
            recaudacion += precio * ventas
    return recaudacion


def escribir_archivo(archivo: str, recaudaciones: list) -> None:
    """Abre el archivo ingresado por parámetro y escribe en él
    las recaudaciones por talento."""
    with open(archivo, "w+", encoding="utf8") as file:
        file.write(HEADER_ARCHIVO)
        for recaudacion, talento in sorted(recaudaciones, key=lambda i: (-i[0], i[1])):
            file.write(f"{talento},{recaudacion}\n")


def listar_recaudaciones(base_datos):
    """Crea una lista de tuplas con los valores
    (recaudacion, talento) para cada talento de la base
    de datos."""
    recaudaciones = []
    talentos = listar_talentos_totales(base_datos)
    for talento in talentos:
        recaudacion = calcular_recaudacion(base_datos, talento)
        recaudaciones.append((recaudacion, talento))
    return recaudaciones


def exportar_talentos(base_datos):
    """Exporta, en el archivo pedido al usuario, las recaudaciones de cada talento
    en la base de datos."""
    ingreso = pedir_ruta_salida()
    if ingreso is None:
        return
    recaudaciones = listar_recaudaciones(base_datos)
    try:
        escribir_archivo(ingreso, recaudaciones)
        print(OK)
    except (FileNotFoundError, PermissionError):
        print(ERROR_EXPORTACION)
        return
