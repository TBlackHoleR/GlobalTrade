from fpdf import FPDF
import os
from tkinter import messagebox, Tk

class Producto:
    def __init__(self, nombre, valor):
        self._nombre = nombre
        self._valor = valor

    def calcular_aranceles(self, destino):
        return self._valor * 0.1  # ejemplo arancel 10%

    def generar_documentacion(self):
        return "Documento adjunto del producto."

class Envio:
    def __init__(self, origen, destino, productos):
        self.origen = origen
        self.destino = destino
        self.productos = productos

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "--- DOCUMENTACIÓN ADUANERA ---", ln=True, align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Página {self.page_no()}", 0, 0, "C")

def generar_documento_envio(envio, nombre_archivo="documento_envio.pdf"):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", "", 12)

    pdf.cell(0, 10, f"Origen: {envio.origen}", ln=True)
    pdf.cell(0, 10, f"Destino: {envio.destino}", ln=True)
    pdf.cell(0, 10, f"Cantidad de productos: {len(envio.productos)}", ln=True)
    pdf.ln(5)

    for producto in envio.productos:
        pdf.cell(0, 10, f"Producto: {producto._nombre}", ln=True)
        pdf.cell(0, 10, f"Valor: ${producto._valor:.2f}", ln=True)
        pdf.cell(0, 10, f"Arancel: ${producto.calcular_aranceles(envio.destino):.2f}", ln=True)
        pdf.multi_cell(0, 10, producto.generar_documentacion())
        pdf.cell(0, 10, "---", ln=True)
        pdf.ln(2)

    pdf.cell(0, 10, "FIN DEL DOCUMENTO", ln=True)

    ruta = os.path.join(os.getcwd(), nombre_archivo)
    pdf.output(ruta)

    try:
        if os.name == 'nt':
            os.startfile(ruta)
    except Exception as e:
        print(f"No se pudo abrir el archivo automáticamente: {e}")

    root = Tk()
    root.withdraw()
    messagebox.showinfo("Éxito", f"PDF generado correctamente:\n{ruta}")
    root.destroy()

    return f"PDF generado exitosamente: {ruta}"

# Crear datos de ejemplo
productos = [
    Producto("Camisa", 20.0),
    Producto("Pantalón", 35.5),
]

envio = Envio("Guatemala", "México", productos)

# Llamar a la función
print(generar_documento_envio(envio))
