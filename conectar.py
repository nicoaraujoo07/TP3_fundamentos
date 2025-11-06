"""CONECTAR"""

from funciones_conectar import (
    menu_principal,
    listar_relaciones,
    manejar_carga_archivos,
    exportar_talentos,
)

OPCIONES = ["1", "2", "3", "4", "5", "6", "7"]

FUNCIONES = {
    OPCIONES[0]: manejar_carga_archivos,
    OPCIONES[1]: manejar_carga_archivos,
    OPCIONES[2]: listar_relaciones,
    OPCIONES[3]: listar_relaciones,
    OPCIONES[4]: listar_relaciones,
    OPCIONES[5]: exportar_talentos,
}


def main():
    """Función principal, llama al menú principal."""
    base_datos = {"peliculas": {}, "ventas": {}}
    menu_principal(FUNCIONES, base_datos)


if __name__ == "__main__":
    main()
