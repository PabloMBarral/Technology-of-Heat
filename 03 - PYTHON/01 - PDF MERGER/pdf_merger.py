from pypdf import PdfWriter, PdfReader

# Lista de PDFs a unir
pdfs = ['01.pdf', '02.pdf']

# Crear el writer
writer = PdfWriter()

for pdf in pdfs:
    reader = PdfReader(pdf)
    for page in reader.pages:
        writer.add_page(page)

# Guardar el PDF unido
with open("merged_file.pdf", "wb") as f:
    writer.write(f)