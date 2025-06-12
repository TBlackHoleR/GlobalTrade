import tkinter as tk
from tkinter import ttk, messagebox, Tk
import random
import datetime
from fpdf import FPDF
import os

# --- PRODUCTOS Y CLASES ---

class Producto:
    def __init__(self, nombre, precio, peso):
        self.nombre = nombre
        self.precio = precio
        self.peso = peso

    def __str__(self):
        return f"{self.nombre} - ${self.precio:.2f} - {self.peso} lb"

class ProductoPerecible(Producto):
    def calcular_arancel(self, pais_destino):
        return 0.07  # Arancel fijo

class ProductoElectronico(Producto):
    def calcular_arancel(self, pais_destino):
        return 0.025  # Arancel fijo

class ProductoHibrido(Producto):
    def calcular_arancel(self, pais_destino):
        return 0.05  # Arancel fijo

def crear_productos_ejemplo():
    productos = {
        'Perecederos': [],
        'Electrónicos': [],
        'Híbridos': []
    }

    perecederos_data = [
        ("Manzanas", 12.50),
        ("Leche Fresca", 9.00),
        ("Carne de Res", 25.00),
        ("Pescado", 22.75),
        ("Yogurt", 6.80),
        ("Queso", 15.20),
        ("Huevos", 7.50),
        ("Fresas", 10.00),
        ("Lechuga", 5.90),
        ("Tomates", 6.20)
    ]
    for nombre, precio in perecederos_data:
        peso = round(random.uniform(1.0, 10.0), 2)
        productos['Perecederos'].append(ProductoPerecible(nombre, precio, peso))

    electronicos_data = [
        ("Smartphone", 699.99, 0.4),
        ("Laptop", 1250.00, 2.5),
        ("Tablet", 450.00, 0.8),
        ("Smartwatch", 199.99, 0.2),
        ("Auriculares", 89.99, 0.3),
        ("Televisor", 999.00, 10.0),
        ("Cámara", 550.00, 1.2),
        ("Consola", 399.99, 3.5),
        ("Drone", 799.99, 2.0),
        ("Altavoz Inteligente", 129.99, 1.0)
    ]
    for nombre, precio, peso in electronicos_data:
        productos['Electrónicos'].append(ProductoElectronico(nombre, precio, peso))

    hibridos_data = [
        ("Refrigerador Inteligente", 1100.00),
        ("Horno con WiFi", 750.00),
        ("Lavadora Smart", 980.00),
        ("Cafetera Programable", 280.00),
        ("Aspiradora Robot", 450.00),
        ("Termostato Inteligente", 220.00),
        ("Sistema de Riego", 360.00),
        ("Báscula Conectada", 140.00),
        ("Purificador de Aire", 300.00),
        ("Robot de Cocina", 600.00)
    ]
    for nombre, precio in hibridos_data:
        peso = round(random.uniform(8.0, 50.0), 2)
        productos['Híbridos'].append(ProductoHibrido(nombre, precio, peso))

    return productos

# --- CLASE ENVIO ---

class Envio:
    def __init__(self):
        self.productos_cantidades = {}
        self.rastreo = []

    def agregar_producto(self, producto, cantidad=1):
        if producto in self.productos_cantidades:
            self.productos_cantidades[producto] += cantidad
        else:
            self.productos_cantidades[producto] = cantidad

    def calcularCostoTotal(self):
        total = 0.0
        for producto, cantidad in self.productos_cantidades.items():
            total += producto.precio * cantidad
        return total

    def generarRastreo(self):
        ubicaciones = ["Guatemala", "México", "Colombia", "España"]
        estados = ["En tránsito", "En aduana", "Entregado"]
        fechas = [datetime.datetime.now() + datetime.timedelta(days=i) for i in range(len(ubicaciones))]

        self.rastreo.clear()
        for i in range(len(ubicaciones)):
            evento = {
                "fecha": fechas[i].strftime("%Y-%m-%d %H:%M:%S"),
                "ubicacion": ubicaciones[i],
                "estado": estados[i % len(estados)]
            }
            self.rastreo.append(evento)
        return self.rastreo

# --- APP INTERFAZ ---

class EnviosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Módulo de Envíos y Rastreo")
        self.root.geometry("900x800")
        self.root.configure(bg='#ffffff')

        self.productos_disponibles = crear_productos_ejemplo()
        self.envio_actual = Envio()

        self.crear_interfaz()

    def crear_interfaz(self):
        style = ttk.Style()
        style.configure('TLabel', font=('Segoe UI', 10), background='#ffffff', foreground='#374151')
        style.configure('Title.TLabel', font=('Segoe UI', 20, 'bold'), background='#ffffff', foreground='#111827')
        style.configure('TButton', font=('Segoe UI', 11), padding=6)
        style.configure('TEntry', font=('Segoe UI', 10))
        style.configure('TCombobox', font=('Segoe UI', 10))

        main_frame = ttk.Frame(self.root, padding=15)
        main_frame.pack(fill='both', expand=True, padx=20, pady=15)

        # Nombre del comprador
        nombre_frame = ttk.Frame(main_frame)
        nombre_frame.pack(fill='x', pady=(0, 15))
        ttk.Label(nombre_frame, text="Nombre del Comprador:", width=20).pack(side='left')
        self.nombre_comprador_var = tk.StringVar()
        self.entry_nombre_comprador = ttk.Entry(nombre_frame, textvariable=self.nombre_comprador_var, width=40)
        self.entry_nombre_comprador.pack(side='left', padx=5)

        # Estructura grid para PDF con algunos valores ficticios predeterminados
        self.grid_structure = [
            ("Número de correlativo", "123456", "Encabezado"),
            ("Fecha de aceptación de Registro", datetime.datetime.now().strftime("%Y-%m-%d"), "Encabezado"),
            ("Aduana de Registro/Inicio de tránsito", "Aduana Central", "Encabezado"),
            ("País de Procedencia", "Estados Unidos", "Tránsito"),
            ("País de Destino", "Guatemala", "Tránsito"),
            ("Aduana de Destino", "Aduana de Guatemala", "Tránsito"),
            ("Depósito Aduanero/Zona Franca", "Zona Franca Norte", "Tránsito"),
            ("Exportador - Número de Identificación", "X123456789", "Partes"),
            ("Exportador - Razón Social", "Exportadora ABC", "Partes"),
            ("Importador - Número de Identificación", "Y987654321", "Partes"),
            ("Importador - Razón Social", "", "Partes"),  # Solicitar ingreso
            ("Transportista - Código", "TR-001", "Partes"),
            ("Transportista - Nombre", "Transportes Rápidos", "Partes"),
            ("Transportista - Nombre del Conductor", "Juan Pérez", "Partes"),
            ("Transportista - ID Unidad", "U-1001", "Partes"),
            ("Transportista - ID Remolque", "R-2002", "Partes"),
            ("Transportista - Contenedor(es)", "Contenedor 10A", "Partes"),
            ("Dispositivo de Seguridad", "GPS Activo", "Carga"),
            ("Cantidad de Bultos", "", "Carga"),  # Solicitar ingreso
            ("Peso Bruto Total", "", "Carga"),  # Calculado de productos
            ("Observaciones Generales", "", "Finalización"),  # Solicitar ingreso
            ("Firma del declarante", "", "Finalización")  # Será nombre comprador
        ]
        # Crear entradas solo para campos vacíos solicitados
        self.grid_entries_vars = {}
        for campo, valor, seccion in self.grid_structure:
            var = tk.StringVar()
            # Si el valor es vacío se crea entrada para el usuario
            if valor == "":
                frame = ttk.Frame(main_frame)
                frame.pack(fill='x', pady=2)
                ttk.Label(frame, text=campo+":", width=25).pack(side='left')
                entry = ttk.Entry(frame, textvariable=var, width=50)
                entry.pack(side='left', padx=5)
            else:
                var.set(valor)
            self.grid_entries_vars[campo] = var

        # Título
        ttk.Label(main_frame, text="Módulo de Envíos y Rastreo", style='Title.TLabel').pack(pady=(5, 15))

        # Selección y adición de productos
        seleccion_frame = ttk.LabelFrame(main_frame, text="Agregar Productos al Envío", padding=12)
        seleccion_frame.pack(fill='x', pady=10)

        ttk.Label(seleccion_frame, text="Categoría:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.categoria_var = tk.StringVar()
        self.combo_categoria = ttk.Combobox(seleccion_frame, textvariable=self.categoria_var,
                                            values=list(self.productos_disponibles.keys()), state='readonly', width=23)
        self.combo_categoria.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        self.combo_categoria.bind("<<ComboboxSelected>>", self.actualizar_productos)
        self.combo_categoria.current(0)

        ttk.Label(seleccion_frame, text="Producto:").grid(row=0, column=2, padx=5, pady=5, sticky='w')
        self.producto_var = tk.StringVar()
        self.combo_producto = ttk.Combobox(seleccion_frame, textvariable=self.producto_var,
                                           values=[], state='readonly', width=30)
        self.combo_producto.grid(row=0, column=3, padx=5, pady=5, sticky='w')

        ttk.Label(seleccion_frame, text="Cantidad:").grid(row=0, column=4, padx=5, pady=5, sticky='w')
        self.cantidad_var = tk.StringVar(value="1")
        self.entry_cantidad = ttk.Entry(seleccion_frame, textvariable=self.cantidad_var, width=6)
        self.entry_cantidad.grid(row=0, column=5, padx=5, pady=5, sticky='w')

        btn_agregar = ttk.Button(seleccion_frame, text="Agregar al Envío", command=self.agregar_producto_envio)
        btn_agregar.grid(row=0, column=6, padx=10, pady=5)

        # Productos seleccionados
        seleccionados_frame = ttk.LabelFrame(main_frame, text="Productos Seleccionados", padding=12)
        seleccionados_frame.pack(fill='both', expand=True, pady=10)

        columns = ("producto", "cantidad", "precio_unit", "peso_unit", "subtotal")
        self.tree_seleccionados = ttk.Treeview(seleccionados_frame, columns=columns, show='headings', selectmode='browse')
        for col, text, width, anchor in [
            ("producto", "Producto", 230, 'w'),
            ("cantidad", "Cantidad", 80, 'center'),
            ("precio_unit", "Precio Unitario ($)", 110, 'e'),
            ("peso_unit", "Peso Unitario (lb)", 120, 'e'),
            ("subtotal", "Subtotal ($)", 110, 'e'),
        ]:
            self.tree_seleccionados.heading(col, text=text)
            self.tree_seleccionados.column(col, width=width, anchor=anchor)
        self.tree_seleccionados.pack(fill='both', expand=True, pady=5)

        btn_eliminar = ttk.Button(seleccionados_frame, text="Eliminar Producto Seleccionado",
                                  command=self.eliminar_producto_seleccionado)
        btn_eliminar.pack(pady=5)

        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(fill='x', pady=10)

        self.label_costo_total = ttk.Label(bottom_frame, text="Costo Total: $0.00", font=('Segoe UI', 12, 'bold'))
        self.label_costo_total.pack(side='left', padx=5)

        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill='x', pady=10)

        self.btn_crear_envio = ttk.Button(btn_frame, text="Crear Envío", command=self.crear_envio)
        self.btn_crear_envio.pack(side='left', padx=10)

        self.btn_generar_rastreo = ttk.Button(btn_frame, text="Generar Rastreo", command=self.generar_rastreo,
                                              state=tk.DISABLED)
        self.btn_generar_rastreo.pack(side='left', padx=10)

        self.btn_info_envio = ttk.Button(btn_frame, text="Información del Envío", command=self.mostrar_info_envio,
                                        state=tk.DISABLED)
        self.btn_info_envio.pack(side='left', padx=10)

        rastreo_frame = ttk.LabelFrame(main_frame, text="Rastreo del Envío", padding=10)
        rastreo_frame.pack(fill='both', expand=True, pady=10)

        self.text_rastreo = tk.Text(rastreo_frame, height=12, width=80)
        self.text_rastreo.pack(padx=5, pady=5, fill='both', expand=True)
        self.text_rastreo.configure(state='disabled')

        self.actualizar_productos()

    def actualizar_productos(self, event=None):
        categoria = self.categoria_var.get()
        productos = self.productos_disponibles.get(categoria, [])
        nombres = [p.nombre for p in productos]
        self.combo_producto['values'] = nombres
        if nombres:
            self.combo_producto.current(0)
            self.producto_var.set(nombres[0])
        else:
            self.combo_producto.set('')
            self.producto_var.set('')

    def agregar_producto_envio(self):
        categoria = self.categoria_var.get()
        producto_nombre = self.producto_var.get()
        cantidad_text = self.cantidad_var.get()

        try:
            cantidad = int(cantidad_text)
            if cantidad < 1:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Error", "Ingrese una cantidad válida (entero mayor que 0).")
            return

        productos = self.productos_disponibles.get(categoria, [])
        producto = next((p for p in productos if p.nombre == producto_nombre), None)
        if producto is None:
            messagebox.showerror("Error", "Producto no válido.")
            return

        self.envio_actual.agregar_producto(producto, cantidad)
        self.actualizar_lista_seleccionados()
        self.cantidad_var.set("1")

    def actualizar_lista_seleccionados(self):
        for i in self.tree_seleccionados.get_children():
            self.tree_seleccionados.delete(i)

        for producto, cantidad in self.envio_actual.productos_cantidades.items():
            subtotal = producto.precio * cantidad
            self.tree_seleccionados.insert('', tk.END, values=(
                producto.nombre,
                cantidad,
                f"${producto.precio:.2f}",
                f"{producto.peso:.2f}",
                f"${subtotal:.2f}"
            ))

        costo_total = self.envio_actual.calcularCostoTotal()
        self.label_costo_total.config(text=f"Costo Total: ${costo_total:.2f}")
        self.btn_generar_rastreo.config(state=tk.DISABLED)
        self.btn_info_envio.config(state=tk.DISABLED)
        self.text_rastreo.configure(state='normal')
        self.text_rastreo.delete('1.0', tk.END)
        self.text_rastreo.configure(state='disabled')

    def eliminar_producto_seleccionado(self):
        selected = self.tree_seleccionados.selection()
        if not selected:
            messagebox.showinfo("Información", "Seleccione un producto para eliminar.")
            return
        item = selected[0]
        values = self.tree_seleccionados.item(item, 'values')
        producto_nombre = values[0]

        producto_a_eliminar = None
        for producto in self.envio_actual.productos_cantidades.keys():
            if producto.nombre == producto_nombre:
                producto_a_eliminar = producto
                break

        if producto_a_eliminar:
            del self.envio_actual.productos_cantidades[producto_a_eliminar]
            self.actualizar_lista_seleccionados()

    def crear_envio(self):
        nombre_comprador = self.nombre_comprador_var.get().strip()
        if not nombre_comprador:
            messagebox.showerror("Error", "Por favor ingrese el nombre del comprador.")
            return

        if not self.envio_actual.productos_cantidades:
            messagebox.showerror("Error", "Debe agregar al menos un producto antes de crear un envío.")
            return

        costo_total = self.envio_actual.calcularCostoTotal()
        messagebox.showinfo("Envío Creado", f"El envío ha sido creado para: {nombre_comprador}\nCosto total: ${costo_total:.2f}")

        self.generar_pdf_envio(nombre_comprador)

        self.btn_generar_rastreo.config(state=tk.NORMAL)
        self.btn_info_envio.config(state=tk.NORMAL)
        self.text_rastreo.configure(state='normal')
        self.text_rastreo.delete('1.0', tk.END)
        self.text_rastreo.configure(state='disabled')

    def generar_pdf_envio(self, nombre_comprador):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "Detalles del Envío", ln=True, align='C')
        pdf.ln(10)

        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, f"Comprador: {nombre_comprador}", ln=True)
        pdf.ln(5)

        pdf.cell(0, 10, "Productos en el Envío:", ln=True)
        pdf.set_font("Arial", '', 12)

        for producto, cantidad in self.envio_actual.productos_cantidades.items():
            subtotal = producto.precio * cantidad
            line = f"{producto.nombre} - Cantidad: {cantidad} - Precio Unitario: ${producto.precio:.2f} - Peso Unitario: {producto.peso:.2f} lb - Subtotal: ${subtotal:.2f}"
            pdf.multi_cell(0, 10, line)

        pdf.ln(5)
        costo_total = self.envio_actual.calcularCostoTotal()
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, f"Costo Total: ${costo_total:.2f}", ln=True)

        # Información adicional con valores y algunos datos solicitados
        pdf.ln(10)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "Información Adicional", ln=True)
        pdf.ln(5)

        col_widths = [70, 70, 40]
        headers = ["Campo", "Valor", "Sección"]
        for i, header in enumerate(headers):
            pdf.cell(col_widths[i], 10, header, border=1, align='C')
        pdf.ln()

        pdf.set_font("Arial", '', 11)

        for campo, valor_pred, seccion in self.grid_structure:
            valor = valor_pred
            # Sobreescribir con valor ingresado si corresponde
            if campo in self.grid_entries_vars and self.grid_entries_vars[campo].get().strip():
                valor = self.grid_entries_vars[campo].get().strip()
            # Peso Bruto Total se calcula sumando pesos * cantidades
            if campo == "Peso Bruto Total":
                peso_total = 0.0
                for prod, cant in self.envio_actual.productos_cantidades.items():
                    peso_total += prod.peso * cant
                valor = f"{peso_total:.2f} lb"
            # Firma del declarante es nombre_comprador
            if campo == "Firma del declarante":
                valor = nombre_comprador

            pdf.cell(col_widths[0], 10, campo, border=1)
            pdf.cell(col_widths[1], 10, valor, border=1)
            pdf.cell(col_widths[2], 10, seccion, border=1)
            pdf.ln()

        # Guardar y abrir PDF
        nombre_archivo = f"envio_{nombre_comprador.replace(' ', '_')}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
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

    def generar_rastreo(self):
        if not self.envio_actual.productos_cantidades:
            messagebox.showerror("Error", "Primero debe crear un envío con productos.")
            return
        rastreo = self.envio_actual.generarRastreo()
        texto = ""
        for evento in rastreo:
            texto += f"Fecha: {evento['fecha']}, Ubicación: {evento['ubicacion']}, Estado: {evento['estado']}\n"
        self.text_rastreo.configure(state='normal')
        self.text_rastreo.delete('1.0', tk.END)
        self.text_rastreo.insert(tk.END, texto)
        self.text_rastreo.configure(state='disabled')

    def mostrar_info_envio(self):
        if not self.envio_actual.productos_cantidades:
            messagebox.showinfo("Info Envío", "No hay envío creado actualmente.")
            return
        info = "Información del Envío:\n\n"
        for producto, cantidad in self.envio_actual.productos_cantidades.items():
            info += f"{producto.nombre}: {cantidad} unidades\n"
        messagebox.showinfo("Info Envío", info)

if __name__ == "__main__":
    root = tk.Tk()
    app = EnviosApp(root)
    root.mainloop()
