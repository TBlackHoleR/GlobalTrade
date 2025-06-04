"""
Contiene la clase Envio para gestionar productos y calcular costos de envío.
"""

import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

class Producto:
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio

class Envio:
    def __init__(self):
        self.productos = []
        self.historial = []

    def agregar_producto(self, producto, cantidad):
        self.productos.append((producto, cantidad))

    def calcular_costo_total(self):
        return sum(producto.precio * cantidad for producto, cantidad in self.productos)
#Generar rastreo del producto
    def generar_rastreo(self):
        ubicacion = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        self.historial.append(ubicacion)
        return ubicacion
#productos
class SistemaLogistico:
    def __init__(self):
        self.productos = {
            "Collar": Producto("Collar", 10),
            "Juguete": Producto("Juguete", 15),
            "Comida para Perro": Producto("Comida para Perro", 20),
            "Comida para Gato": Producto("Comida para Gato", 25),
            "Cama para Perro": Producto("Cama para Perro", 40),
            "Cama para Gato": Producto("Cama para Gato", 45)
        }

        self.envio_actual = Envio()
        self.ventana_principal = tk.Tk()
        self.ventana_principal.title("Chronos Supply Chain")
        self.ventana_principal.geometry("600x800")

        self.crear_componentes()
#componentes
    def crear_componentes(self):
        tk.Label(self.ventana_principal, text="Nombre del Cliente:").pack(pady=5)
        self.entry_nombre = tk.Entry(self.ventana_principal, width=50)
        self.entry_nombre.pack(pady=5)

        tk.Label(self.ventana_principal, text="País:").pack(pady=6)
        self.entry_pais = tk.Entry(self.ventana_principal, width=50)
        self.entry_pais.pack(pady=5)

        tk.Label(self.ventana_principal, text="Seleccionar Producto:").pack(pady=5)
        self.combo_producto = ttk.Combobox(self.ventana_principal, values=list(self.productos.keys()), width=47)
        self.combo_producto.pack(pady=5)

        tk.Label(self.ventana_principal, text="Cantidad:").pack(pady=5)
        self.entry_cantidad = tk.Entry(self.ventana_principal, width=5)
        self.entry_cantidad.pack(pady=5)

        boton_agregar = tk.Button(self.ventana_principal, text="Agregar Producto", command=self.agregar_producto)
        boton_agregar.pack(pady=20)

        boton_calcular = tk.Button(self.ventana_principal, text="Calcular Total", command=self.calcular_total_compra)
        boton_calcular.pack(pady=20)

        boton_generar_rastreo = tk.Button(self.ventana_principal, text="Generar Rastreo", command=self.generar_rastreo)
        boton_generar_rastreo.pack(pady=20)

        boton_mostrar_historial = tk.Button(self.ventana_principal, text="Mostrar Historial", command=self.mostrar_historial)
        boton_mostrar_historial.pack(pady=20)
#botones producto
    def agregar_producto(self):
        producto_nombre = self.combo_producto.get()
        cantidad_str = self.entry_cantidad.get()
        if cantidad_str.isdigit():
            cantidad = int(cantidad_str)
            producto = self.productos[producto_nombre]
            self.envio_actual.agregar_producto(producto, cantidad)
            messagebox.showinfo("Producto Agregado", f"{cantidad} de {producto_nombre} añadido al envío.")

    def calcular_total_compra(self):
        total_final = self.envio_actual.calcular_costo_total()
        nombre_cliente = self.entry_nombre.get()
        pais_cliente = self.entry_pais.get()
        mensaje_final = f"Gracias {nombre_cliente} de {pais_cliente} por su compra. El total es: Q {total_final}."
        messagebox.showinfo("Gracias por tu compra", mensaje_final)

    def generar_rastreo(self):
        ubicacion = self.envio_actual.generar_rastreo()
        messagebox.showinfo("Rastreo generado", f"Rastreo generado en {ubicacion}")

    def mostrar_historial(self):
        mensaje = "Historial de Rastreo:\n"
        for ubicacion in self.envio_actual.historial:
            mensaje += f"- Envío generado en {ubicacion}\n"
        messagebox.showinfo("Historial de Rastreo", mensaje)

    def run(self):
        self.ventana_principal.mainloop()

if __name__ == "__main__":
    sistema = SistemaLogistico()
    sistema.run()