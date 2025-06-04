import tkinter as tk
from tkinter import ttk, messagebox
from src.Dos_productos import ProductoPerecedero, ProductoElectronico
from src.Tres_envios import Envio
from src.Cuatro_conversion import convertir_moneda
from src.Cinco_documentacion import generar_documento_envio
from src.historial import registrar_transaccion, mostrar_historial

class InterfazGlobalTrade:
    def __init__(self, master):
        self.master = master
        self.master.title("GlobalTrade - Gestión de Comercio Internacional")
        self.master.geometry("800x600")

        # Datos de ejemplo
        self.productos_perecederos = [
            ProductoPerecedero(1, "Manzanas", 10, 30, "2025-07-01"),
            ProductoPerecedero(2, "Peras", 8, 25, "2025-06-15"),
            ProductoPerecedero(3, "Uvas", 5, 20, "2025-06-20"),
            ProductoPerecedero(4, "Fresas", 3, 15, "2025-06-10"),
            ProductoPerecedero(5, "Mangos", 7, 28, "2025-06-25")
        ]

        self.productos_electronicos = [
            ProductoElectronico(6, "Celular", 1, 300, 220),
            ProductoElectronico(7, "Laptop", 2, 800, 220),
            ProductoElectronico(8, "Tablet", 1.5, 500, 220),
            ProductoElectronico(9, "Cámara", 1.2, 450, 220),
            ProductoElectronico(10, "Auriculares", 0.5, 150, 220)
        ]

        self.productos_hibridos = [
            ProductoElectronico(11, "Smartwatch", 0.3, 200, 220),
            ProductoElectronico(12, "Dron", 2.5, 1000, 220),
            ProductoElectronico(13, "E-book", 0.8, 120, 220),
            ProductoElectronico(14, "GPS", 1, 250, 220),
            ProductoElectronico(15, "Cámara Deportiva", 0.9, 300, 220)
        ]

        self.paises = ["Guatemala", "México", "Chile", "España", "Estados Unidos", "Alemania", "Japón", "Canadá"]

        self.crear_widgets()

    def crear_widgets(self):
        # Frame para productos
        frame_productos = tk.LabelFrame(self.master, text="Seleccionar Productos", padx=10, pady=10)
        frame_productos.pack(fill="both", expand="yes", padx=20, pady=10)

        # Listbox para productos perecederos
        self.listbox_perecederos = self.crear_listbox(frame_productos, "Productos Perecederos", self.productos_perecederos)

        # Listbox para productos electrónicos
        self.listbox_electronicos = self.crear_listbox(frame_productos, "Productos Electrónicos", self.productos_electronicos)

        # Listbox para productos híbridos
        self.listbox_hibridos = self.crear_listbox(frame_productos, "Productos Híbridos", self.productos_hibridos)

        # Frame para países
        frame_paises = tk.LabelFrame(self.master, text="Información de Envío", padx=10, pady=10)
        frame_paises.pack(fill="both", expand="yes", padx=20, pady=10)

        tk.Label(frame_paises, text="País de Origen:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.origen_var = tk.StringVar()
        self.origen_menu = ttk.Combobox(frame_paises, textvariable=self.origen_var, values=self.paises)
        self.origen_menu.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_paises, text="País de Destino:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.destino_var = tk.StringVar()
        self.destino_menu = ttk.Combobox(frame_paises, textvariable=self.destino_var, values=self.paises)
        self.destino_menu.grid(row=1, column=1, padx=5, pady=5)

        # Frame para botones
        frame_botones = tk.Frame(self.master)
        frame_botones.pack(pady=10)

        tk.Button(frame_botones, text="Conversión Monetaria", command=self.abrir_conversion).grid(row=0, column=0, padx=10)
        tk.Button(frame_botones, text="Generar Envío", command=self.generar_envio).grid(row=0, column=1, padx=10)
        tk.Button(frame_botones, text="Generar Documento", command=self.generar_documento).grid(row=0, column=2, padx=10)

    def crear_listbox(self, parent, titulo, productos):
        frame = tk.Frame(parent)
        frame.pack(side="left", padx=10)

        tk.Label(frame, text=titulo).pack()
        listbox = tk.Listbox(frame, selectmode="multiple", width=30, height=10)
        listbox.pack()

        for producto in productos:
            listbox.insert(tk.END, f"{producto.nombre} (ID: {producto.id})")

        return listbox

    def obtener_productos_seleccionados(self):
        seleccionados = []

        for listbox, productos in [
            (self.listbox_perecederos, self.productos_perecederos),
            (self.listbox_electronicos, self.productos_electronicos),
            (self.listbox_hibridos, self.productos_hibridos)
        ]:
            indices = listbox.curselection()
            for i in indices:
                seleccionados.append(productos[i])

        return seleccionados

    def abrir_conversion(self):
        productos = self.obtener_productos_seleccionados()
        if not productos:
            messagebox.showwarning("Advertencia", "Seleccione al menos un producto.")
            return

        # Aquí puedes implementar la lógica para la conversión monetaria
        messagebox.showinfo("Conversión", "Funcionalidad de conversión monetaria aún no implementada.")

    def generar_envio(self):
        productos = self.obtener_productos_seleccionados()
        if not productos:
            messagebox.showwarning("Advertencia", "Seleccione al menos un producto.")
            return

        origen = self.origen_var.get()
        destino = self.destino_var.get()

        if not origen or not destino:
            messagebox.showwarning("Advertencia", "Seleccione país de origen y destino.")
            return

        envio = Envio(origen=origen, destino=destino)
        for producto in productos:
            envio.agregar_producto(producto)

        registrar_transaccion(envio)
        messagebox.showinfo("Envío", f"Envío generado con éxito.\nCosto total: {envio.calcular_costo_total()}")

    def generar_documento(self):
        productos = self.obtener_productos_seleccionados()
        if not productos:
            messagebox.showwarning("Advertencia", "Seleccione al menos un producto.")
            return

        origen = self.origen_var.get()
        destino = self.destino_var.get()

        if not origen or not destino:
            messagebox.showwarning("Advertencia", "Seleccione país de origen y destino.")
            return

        envio = Envio(origen=origen, destino=destino)
        for producto in productos:
            envio.agregar_producto(producto)

        documento = generar_documento_envio(envio)
        messagebox.showinfo("Documento Generado", documento)
