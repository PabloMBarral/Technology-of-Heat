from pathlib import Path

def obtener_directorio_actual():
    """
    Obtiene el directorio actual donde se encuentra el archivo Python.

    Returns:
        Path: Objeto Path que representa el directorio actual.
    """
    return Path(__file__).parent

def crear_estructura_carpetas(estructura_carpetas):
    """
    Crea una estructura de carpetas en el directorio actual.

    Args:
        estructura_carpetas: Lista que contiene los nombres de las carpetas a crear.
    """
    directorio_principal = obtener_directorio_actual()

    for carpeta in estructura_carpetas:
        ruta_completa = directorio_principal / carpeta
        ruta_completa.mkdir(parents=True, exist_ok=True)

    print("Estructura de carpetas creada")

estructura_carpetas = ["carpeta1", "carpeta2", "carpeta3/subcarpeta1", "carpeta3/subcarpeta2"]

crear_estructura_carpetas(estructura_carpetas)

