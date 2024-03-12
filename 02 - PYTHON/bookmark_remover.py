import os
from PyPDF2 import PdfReader, PdfWriter

def remove_bookmarks(pdf_file):
    # Construye la ruta completa al archivo de entrada
    input_pdf = os.path.join(os.getcwd(), pdf_file)

    # Verifica si el archivo PDF de entrada existe
    if not os.path.isfile(input_pdf):
        print(f"El archivo '{pdf_file}' no existe.")
        return

    # Construye la ruta completa al archivo de salida sin bookmarks
    output_pdf = os.path.join(os.getcwd(), 'output.pdf')

    # Abre el archivo PDF de entrada
    with open(input_pdf, 'rb') as file:
        reader = PdfReader(file)
        writer = PdfWriter()

        # Copia las páginas del PDF de entrada al PDF de salida
        for page_num in range(len(reader.pages)):
            writer.add_page(reader.pages[page_num])

        # Escribe el PDF de salida al archivo
        with open(output_pdf, 'wb') as output_file:
            writer.write(output_file)

    print("Los bookmarks han sido eliminados exitosamente.")




# Reemplaza 'nombre_del_archivo.pdf' con el nombre de tu archivo PDF
remove_bookmarks('0A63-0410-2ATIN-004-C-ES.pdf')
