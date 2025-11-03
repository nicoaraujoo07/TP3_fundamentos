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

MENU_PRINCIPAL = """1) Cargar películas
2) Cargar información de ventas 
3) Listar colaboraciones directas 
4) Listar talentos compatibles 
5) Listar talentos incompatibles 
6) Exportar talentos con mayor recaudación 
7) Salir
>>> """


OPCIONES = ["1", "2", "3", "4", "5", "6", "7"]


MSG_INGRESO_PELICULAS = "Ingrese el archivo de películas a cargar: "
MSG_INGRESO_VENTAS = "Ingrese el archivo de ventas a cargar: "
MSG_INGRESO_NOMBRE = "Ingrese el nombre de un talento: "
INVALIDO = "invalido"
INEXISTENTE = "inexistente"


def menu_principal(funciones):
    base_datos = {"peliculas": {}, "ventas": {}}
    while True:
        opcion_elegida = input(MENU_PRINCIPAL)
        if opcion_elegida in funciones:
            funciones.get(opcion_elegida)(base_datos, opcion_elegida)
        elif opcion_elegida == "7":
            print(base_datos)
            break
        else:
            print(OPCION_INVALIDA)
            continue


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


def ingresar_rutas(tipo):
    while True:
        ingreso = input(
            MSG_INGRESO_PELICULAS if tipo == OPCIONES[0] else MSG_INGRESO_VENTAS
        )
        if ingreso == OPCION_RETROCEDER:
            return None
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


def ingresar_datos(archivo, base_datos, contador, tipo):
    for linea in archivo:
        datos = linea.split(",")
        if tipo == "pelicula":
            if datos[0] in base_datos["peliculas"]:
                print(PELICULA_DUPLICADA + f" {datos[0]}")
                continue
            base_datos["peliculas"][datos[0]] = {
                "precio": datos[1],
                "talentos": datos[2].rstrip("\n").split(";"),
            }
        else:
            if datos[0] not in base_datos["peliculas"]:
                print(PELICULA_INEXISTENTE + f"{datos[0]}")
                continue
            base_datos["ventas"][datos[0]] = base_datos["ventas"].get(
                datos[0], 0
            ) + int(datos[1].rstrip("\n"))
        contador += 1
    return contador


def procesar_datos(rutas, base_datos, tipo):
    contador = 0
    for ruta in rutas:
        with open(ruta, "r", encoding="utf8") as archivo:
            archivo.readline()  # Saltear el header
            contador = ingresar_datos(archivo, base_datos, contador, tipo)
    return contador


def cargar_datos(base_datos, tipo):
    rutas = ingresar_rutas(tipo)
    if rutas is None:
        return
    acceder_directorios(rutas)
    try:
        datos_cargados = procesar_datos(
            rutas, base_datos, "pelicula" if tipo == OPCIONES[0] else "venta"
        )
        if datos_cargados is None:
            return
    except (PermissionError, FileNotFoundError, OSError):
        return
    print("OK " + str(datos_cargados))


def normalizar_nombre(nombre):
    tildes = {
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
        "ñ": "n",
        "Ñ": "N",
    }
    for letra, reemplazo in tildes.items():
        nombre = nombre.replace(letra, reemplazo)
    return nombre.lower()


def clasificar_nombre(nombre, base_datos):
    nombre_normalizado_sin_espacios = normalizar_nombre(nombre).replace(" ", "")
    if (
        not nombre_normalizado_sin_espacios
        or not nombre_normalizado_sin_espacios.isalpha()
    ):
        return INVALIDO
    peliculas = base_datos["peliculas"]
    for pelicula in peliculas.values():
        talentos = pelicula["talentos"]
        for talento in talentos:
            if normalizar_nombre(nombre) == normalizar_nombre(talento):
                return talento
    return INEXISTENTE


def pedir_nombre(base_datos) -> str:
    while True:
        ingreso = input(MSG_INGRESO_NOMBRE)
        if ingreso == OPCION_RETROCEDER:
            return None
        clasificacion = clasificar_nombre(ingreso, base_datos)
        if clasificacion == INVALIDO:
            print(ERROR_NOMBRE_TALENTO_INVALIDO)
            continue
        if clasificacion == INEXISTENTE:
            print(ERROR_TALENTO_NO_ENCONTRADO)
            continue
        return clasificacion


def listar_colaboradores_directos(base_datos, nombre):
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
    if not talentos_encontrados:
        print(COLABORADORES_DIRECTOS_INEXISTENTES)
        return None
    return talentos_encontrados


def imprimir_talentos(lista, opcion_elegida):
    if opcion_elegida == OPCIONES[2]:
        print(COLABORADORES_DIRECTOS)
    elif opcion_elegida == OPCIONES[3]:
        print(TALENTOS_COMPATIBLES)
    else:
        print(TALENTOS_INCOMPATIBLES)
    for i, talento in enumerate(lista):
        print(f"{i+1}. {talento}")


def _listar_talentos_compatibles(
    base_datos, nombre, colaboradores_directos, talentos_compatibles, procesados
):
    if nombre not in procesados:
        procesados.append(nombre)
    for colaborador_directo in colaboradores_directos:
        if colaborador_directo in procesados:
            continue
        procesados.append(colaborador_directo)
        nuevos_colaboradores = listar_colaboradores_directos(
            base_datos, colaborador_directo
        )
        if nombre in nuevos_colaboradores:
            nuevos_colaboradores.remove(nombre)

        for talento in nuevos_colaboradores:
            if talento not in talentos_compatibles:
                talentos_compatibles.append(talento)

        _listar_talentos_compatibles(
            base_datos,
            colaborador_directo,
            nuevos_colaboradores,
            talentos_compatibles,
            procesados,
        )
    return talentos_compatibles


def listar_talentos_compatibles(base_datos, nombre):
    colaboradores_directos = listar_colaboradores_directos(base_datos, nombre)
    return _listar_talentos_compatibles(
        base_datos, nombre, colaboradores_directos, [], []
    )


def listar(base_datos, opcion_elegida):
    nombre = pedir_nombre(base_datos)
    if nombre is None:
        return
    if opcion_elegida == OPCIONES[2]:
        talentos_encontrados = listar_colaboradores_directos(base_datos, nombre)
    elif opcion_elegida == OPCIONES[3]:
        talentos_encontrados = listar_talentos_compatibles(base_datos, nombre)
    else:
        talentos_encontrados = listar_talentos_incompatibles(base_datos, nombre)
    if talentos_encontrados is None:
        return
    imprimir_talentos(sorted(talentos_encontrados), opcion_elegida)


FUNCIONES = {
    OPCIONES[0]: cargar_datos,
    OPCIONES[1]: cargar_datos,
    OPCIONES[2]: listar,
    OPCIONES[3]: listar,
    # OPCIONES[4]: listar,
    # OPCIONES[5]: exportar_talentos_mayor_recaudacion,
}


def main():
    menu_principal(FUNCIONES)


if __name__ == "__main__":
    main()

