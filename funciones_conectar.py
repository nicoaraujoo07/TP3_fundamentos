"""Constantes de Agencia Conectar."""

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

MENU_PRINCIPAL = """1) Cargar películas 
2) Cargar información de ventas 
3) Listar colaboraciones directas 
4) Listar talentos compatibles 
5) Listar talentos incompatibles 
6) Exportar talentos con mayor recaudación 
7) Salir
>>> """

OPCIONES = ["1", "2", "3", "4", "5", "6", "7"]


MSG_INGRESO = "Ingrese el archivo de películas a cargar: "


def menu_principal(funciones):
    base_datos = {"peliculas": {}, "ventas": {}}
    while True:
        opcion_elegida = input(MENU_PRINCIPAL)
        if opcion_elegida in funciones:
            funciones.get(opcion_elegida)(base_datos)
        elif opcion_elegida == "7":
            print(base_datos)
            break
        else:
            print(OPCION_INVALIDA)
            continue


import os


def validar_ruta(ruta: str) -> bool:
    if os.path.exists(ruta):
        if not os.path.isdir(ruta) and ruta.endswith(".csv"):
            return True
        if os.path.isdir(ruta):
            for busqueda in os.listdir(ruta):
                subruta = os.path.join(ruta, busqueda)
                if validar_ruta(subruta):
                    return True
    return False


def ingresar_rutas():
    while True:
        ingreso = input(MSG_INGRESO)
        if ingreso == OPCION_RETROCEDER:
            return
        rutas = ingreso.split()
        for ruta in rutas:
            if not validar_ruta(ruta):
                print(ERROR_IMPORTACION)
                continue
        break
    return rutas


def acceder_directorios(rutas):
    for ruta in rutas:
        if os.path.isdir(ruta):
            rutas.remove(ruta)
            for busqueda in os.listdir(ruta):
                subruta = os.path.join(ruta, busqueda)
                if subruta.endswith(".csv"):
                    rutas.append(subruta)


def ingresar_peliculas(archivo, base_datos, contador):
    for linea in archivo:
        datos = linea.split(",")
        if datos[0] in base_datos["peliculas"]:
            print(PELICULA_DUPLICADA + f" {datos[0]}")
            continue
        base_datos["peliculas"][datos[0]] = {
            "precio": datos[1],
            "actores": datos[2].rstrip("\n").split(";"),
        }
        contador += 1
    return contador


def ingresar_ventas(archivo, base_datos, contador):
    for linea in archivo:
        datos = linea.split(",")
        if datos[0] not in base_datos["peliculas"]:
            print(PELICULA_INEXISTENTE + f"{datos[0]}")
            continue
        base_datos["ventas"][datos[0]] = datos[1]
        contador += 1
    return contador


def cargar_datos(rutas, base_datos, tipo):
    contador = 0
    for ruta in rutas:
        try:
            with open(ruta, "r", encoding="utf8") as archivo:
                archivo.readline()  # Se saltea el header
                if tipo == "pelicula":
                    contador = ingresar_peliculas(archivo, base_datos, contador)
                else:
                    contador = ingresar_ventas(archivo, base_datos, contador)
        except PermissionError as e_permisos:
            raise e_permisos
        except FileNotFoundError as e_fnf:
            raise e_fnf
    return contador


def cargar_peliculas(base_datos):
    rutas = ingresar_rutas()
    acceder_directorios(rutas)
    try:
        peliculas_cargadas = cargar_datos(rutas, base_datos, "pelicula")
    except PermissionError:
        return
    except FileNotFoundError:
        return
    print("OK " + str(peliculas_cargadas))


# def cargar_ventas(base_datos):


FUNCIONES = {
    OPCIONES[0]: cargar_peliculas,
    # OPCIONES[1]: cargar_ventas,
    # OPCIONES[2]: listar_colaboraciones_directas,
    # OPCIONES[3]: listar_talentos_compatibles,
    # OPCIONES[4]: listar_talentos_incompatibles,
    # OPCIONES[5]: exportar_talentos_mayor_recaudacion,
}


menu_principal(FUNCIONES)
