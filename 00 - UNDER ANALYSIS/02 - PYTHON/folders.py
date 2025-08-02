import os

def crear_carpetas():
    # Rango de números XX desde 38 a 50
    for xx in range(38, 51):
        # Nombre de la carpeta
        nombre_carpeta = f"test_0{xx:02d}"
        # Crear la carpeta si no existe
        if not os.path.exists(nombre_carpeta):
            os.makedirs(nombre_carpeta)
            print(f"Se ha creado la carpeta {nombre_carpeta}")

if __name__ == "__main__":
    crear_carpetas()