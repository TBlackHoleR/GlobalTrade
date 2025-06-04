from fpdf import FPDF

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, txt="¡Hola, FPDF está funcionando!", ln=True, align='C')
pdf.output("ejemplo.pdf")

print("PDF generado correctamente.")
