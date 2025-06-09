import tkinter as tk
from tkinter import ttk, messagebox
import random

# Clases de productos con polimorfismo
class Producto:
    def __init__(self, nombre, precio, peso):
        self.nombre = nombre
        self.precio = precio
        self.peso = peso
    
    def calcular_arancel(self, pais_destino):
        return 0.0
    
    def precio_final(self, pais_destino):
        return self.precio * (1 + self.calcular_arancel(pais_destino))
    
    def __str__(self):
        return f"{self.nombre} - ${self.precio:.2f} - {self.peso} lb"

class ProductoPerecible(Producto):
    def calcular_arancel(self, pais_destino):
        return 0.07  # Arancel fijo para simplificar

class ProductoElectronico(Producto):
    def calcular_arancel(self, pais_destino):
        return 0.025  # Arancel fijo para simplificar

class ProductoHibrido(Producto):
    def calcular_arancel(self, pais_destino):
        return 0.05  # Arancel fijo para simplificar

# Crear productos de ejemplo
def crear_productos_ejemplo():
    productos = {
        'Perecederos': [],
        'Electrónicos': [],
        'Híbridos': []
    }
    
    # Productos perecederos
    nombres_perecederos = ["Manzanas", "Leche Fresca", "Carne de Res", "Pescado", "Yogurt", 
                          "Queso", "Huevos", "Fresas", "Lechuga", "Tomates"]
    for nombre in nombres_perecederos:
        precio = round(random.uniform(5.0, 30.0), 2)
        peso = round(random.uniform(1.0, 10.0), 2)
        productos['Perecederos'].append(ProductoPerecible(nombre, precio, peso))
    
    # Productos electrónicos
    nombres_electronicos = ["Smartphone", "Laptop", "Tablet", "Smartwatch", "Auriculares",
                           "Televisor", "Cámara", "Consola", "Drone", "Altavoz Inteligente"]
    for nombre in nombres_electronicos:
        precio = round(random.uniform(100.0, 2000.0), 2)
        peso = round(random.uniform(0.5, 15.0), 2)
        productos['Electrónicos'].append(ProductoElectronico(nombre, precio, peso))
    
    # Productos híbridos
    nombres_hibridos = ["Refrigerador Inteligente", "Horno con WiFi", "Lavadora Smart", 
                       "Cafetera Programable", "Aspiradora Robot", "Termostato Inteligente",
                       "Sistema de Riego", "Báscula Conectada", "Purificador de Aire", "Robot de Cocina"]
    for nombre in nombres_hibridos:
        precio = round(random.uniform(150.0, 1200.0), 2)
        peso = round(random.uniform(8.0, 50.0), 2)
        productos['Híbridos'].append(ProductoHibrido(nombre, precio, peso))
    
    return productos

class ChronosApp:
    TASA_CAMBIO_GTQ_USD = 7.82
    
    def __init__(self, root):
        self.root = root
        self.root.title("Chronos Supply Chain - Internacional 🛩️")
        self.root.geometry("820x580")
        self.root.configure(bg='#ffffff')
        self.productos = crear_productos_ejemplo()
        
        # Variables para selección
        self.categoria_seleccionada = tk.StringVar()
        self.producto_seleccionado = tk.StringVar()
        self.cantidad = tk.StringVar(value="1")
        
        # Crear la interfaz
        self.crear_interfaz()
    
    def crear_interfaz(self):
        style = ttk.Style()
        style.configure('TLabel', font=('Segoe UI', 10), background='#ffffff', foreground='#374151')
        style.configure('Title.TLabel', font=('Segoe UI', 20, 'bold'), background='#ffffff', foreground='#111827')
        style.configure('TButton', font=('Segoe UI', 11), padding=6)
        style.configure('TEntry', font=('Segoe UI', 10))
        style.configure('TCombobox', font=('Segoe UI', 10))
        
        main_frame = ttk.Frame(self.root, padding=15, style='Card.TFrame')
        main_frame.pack(fill='both', expand=True, padx=20, pady=15)
        main_frame.configure(relief='flat')
        
        ttk.Label(main_frame, text="Chronos Supply Chain - Internacional🛩️", style='Title.TLabel').pack(pady=(0,18))
        
        # Selección de Categoría
        categoria_frame = ttk.LabelFrame(main_frame, text="Selección de Categoría", padding=12)
        categoria_frame.pack(fill='x', pady=8)
        categoria_frame.configure(style='TLabelframe')
        
        ttk.Label(categoria_frame, text="Categoría:").grid(row=0, column=0, padx=6, pady=6, sticky='w')
        categorias = list(self.productos.keys())
        self.combo_categoria = ttk.Combobox(categoria_frame, values=categorias, textvariable=self.categoria_seleccionada, state='readonly', width=30)
        self.combo_categoria.grid(row=0, column=1, padx=6, pady=6, sticky='w')
        self.combo_categoria.bind('<<ComboboxSelected>>', self.mostrar_productos)
        self.combo_categoria.current(0)
        
        # Selección de Producto
        producto_frame = ttk.LabelFrame(main_frame, text="Selección de Producto", padding=12)
        producto_frame.pack(fill='x', pady=8)
        producto_frame.configure(style='TLabelframe')
        
        ttk.Label(producto_frame, text="Producto:").grid(row=0, column=0, padx=6, pady=6, sticky='w')
        self.combo_producto = ttk.Combobox(producto_frame, values=[], textvariable=self.producto_seleccionado, state='readonly', width=45)
        self.combo_producto.grid(row=0, column=1, padx=6, pady=6, sticky='w')
        self.combo_producto.bind('<<ComboboxSelected>>', self.mostrar_detalle_producto)
        
        self.label_detalle_producto = ttk.Label(producto_frame, text="", font=('Segoe UI', 9, 'italic'), foreground='#6b7280')
        self.label_detalle_producto.grid(row=1, column=0, columnspan=2, padx=6, pady=(2,8), sticky='w')
        
        # Grid Cantidad, Total USD, Total GTQ y Total Peso
        compra_frame = ttk.LabelFrame(main_frame, text="Detalles de Compra", padding=12)
        compra_frame.pack(fill='x', pady=8)
        compra_frame.configure(style='TLabelframe')
        
        ttk.Label(compra_frame, text="Cantidad a comprar:").grid(row=0, column=0, padx=6, pady=6, sticky='w')
        self.entry_cantidad = ttk.Entry(compra_frame, textvariable=self.cantidad, width=10)
        self.entry_cantidad.grid(row=0, column=1, padx=6, pady=6, sticky='w')
        self.entry_cantidad.bind('<KeyRelease>', self.actualizar_totales)
        
        ttk.Label(compra_frame, text="Total en USD:").grid(row=1, column=0, padx=6, pady=6, sticky='w')
        self.label_total_usd = ttk.Label(compra_frame, text="$0.00", foreground='#111827', font=('Segoe UI', 10, 'bold'))
        self.label_total_usd.grid(row=1, column=1, padx=6, pady=6, sticky='w')
        
        ttk.Label(compra_frame, text="Total en Quetzales (Q):").grid(row=2, column=0, padx=6, pady=6, sticky='w')
        self.label_total_gtq = ttk.Label(compra_frame, text="Q0.00", foreground='#111827', font=('Segoe UI', 10, 'bold'))
        self.label_total_gtq.grid(row=2, column=1, padx=6, pady=6, sticky='w')
        
        ttk.Label(compra_frame, text="Peso total (lb):").grid(row=3, column=0, padx=6, pady=6, sticky='w')
        self.label_total_peso = ttk.Label(compra_frame, text="0.00 lb", foreground='#111827', font=('Segoe UI', 10, 'bold'))
        self.label_total_peso.grid(row=3, column=1, padx=6, pady=6, sticky='w')
        
        # Botón Calcular Aranceles
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill='x', pady=14)
        
        btn_calcular = ttk.Button(btn_frame, text="Calcular Aranceles", command=self.calcular_aranceles, width=20)
        btn_calcular.pack(side='left', padx=(0, 10))
        
        # Área de resultados
        resultados_frame = ttk.LabelFrame(main_frame, text="Resultado de Cálculo", padding=12)
        resultados_frame.pack(fill='both', expand=True, pady=8)
        resultados_frame.configure(style='TLabelframe')
        
        self.resultados_texto = tk.StringVar()
        self.resultados_texto.set("Seleccione un producto y cantidad para ver detalles.")
        
        resultados_label = ttk.Label(resultados_frame, textvariable=self.resultados_texto, wraplength=750,
                                    justify='left', font=('Segoe UI', 10))
        resultados_label.pack(fill='both', expand=True)
        
        # Inicializar productos y totales
        self.mostrar_productos()
        self.actualizar_totales()
    
    def mostrar_productos(self, event=None):
        categoria = self.categoria_seleccionada.get()
        productos_categoria = self.productos[categoria]
        
        nombres_productos = [p.nombre for p in productos_categoria]
        self.combo_producto['values'] = nombres_productos
        self.combo_producto.current(0)
        self.mostrar_detalle_producto()
        self.actualizar_totales()
    
    def mostrar_detalle_producto(self, event=None):
        index = self.combo_producto.current()
        categoria = self.categoria_seleccionada.get()
        if index < 0 or not categoria or index >= len(self.productos[categoria]):
            self.label_detalle_producto.config(text="")
            return
        
        producto = self.productos[categoria][index]
        detalles = f"Producto: {producto.nombre} | Precio unitario: ${producto.precio:.2f} | Peso unitario: {producto.peso} lb"
        self.label_detalle_producto.config(text=detalles)
        self.actualizar_totales()
    
    def actualizar_totales(self, event=None):
        cantidad_text = self.cantidad.get()
        try:
            cantidad = int(cantidad_text)
            if cantidad < 1:
                raise ValueError()
        except ValueError:
            self.resultados_texto.set("Ingrese una cantidad válida (entero positivo).")
            self.label_total_usd.config(text="$0.00")
            self.label_total_gtq.config(text="Q0.00")
            self.label_total_peso.config(text="0.00 lb")
            return
        
        index = self.combo_producto.current()
        categoria = self.categoria_seleccionada.get()
        if index < 0 or not categoria or index >= len(self.productos[categoria]):
            self.label_total_usd.config(text="$0.00")
            self.label_total_gtq.config(text="Q0.00")
            self.label_total_peso.config(text="0.00 lb")
            self.resultados_texto.set("Seleccione un producto y cantidad para ver detalles.")
            return
        
        producto = self.productos[categoria][index]
        total_usd = producto.precio * cantidad
        total_gtq = total_usd * self.TASA_CAMBIO_GTQ_USD
        total_peso = producto.peso * cantidad
        
        self.label_total_usd.config(text=f"${total_usd:,.2f}")
        self.label_total_gtq.config(text=f"Q{total_gtq:,.2f}")
        self.label_total_peso.config(text=f"{total_peso:,.2f} lb")
        self.resultados_texto.set("Seleccione un producto y cantidad para ver detalles.")
    
    def calcular_aranceles(self):
        index = self.combo_producto.current()
        categoria = self.categoria_seleccionada.get()
        if index < 0 or not categoria or index >= len(self.productos[categoria]):
            messagebox.showwarning("Advertencia", "Seleccione un producto para calcular aranceles.")
            return
        
        producto = self.productos[categoria][index]
        arancel = producto.calcular_arancel('USA')  # país fijo para simplificar
        message = f"Arancel para {producto.nombre}: {arancel * 100:.1f}%\n\n" \
                  f"Para calcular costos totales con conversión y logística, " \
                  f"diríjase a la opción de conversión en el sistema."
        messagebox.showinfo("Aranceles", message)

# Iniciar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = ChronosApp(root)
    root.mainloop()
