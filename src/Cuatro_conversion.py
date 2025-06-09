import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import subprocess, sys, os

# Monedas disponibles con tasas de cambio a USD (moneda base)
TASAS_CAMBIO = {
    'USD': 1.0,      # Dólar estadounidense (moneda base)
    'GTQ': 7.82,     # Quetzal guatemalteco
    'EUR': 0.93,     # Euro
    'CNY': 7.25,     # Yuan chino
    'JPY': 154.17,   # Yen japonés
    'MXN': 16.77,    # Peso mexicano
    'CAD': 1.36,     # Dólar canadiense
    'GBP': 0.80,     # Libra esterlina
    'BRL': 5.05,     # Real brasileño
    'INR': 83.40,    # Rupia india
    'AUD': 1.52      # Dólar australiano
}

# Nombres completos de monedas con sus símbolos
NOMBRES_MONEDA = {
    'USD': ('Dólar Estadounidense', '$'),
    'EUR': ('Euro', '€'),
    'CNY': ('Yuan Chino', '¥'),
    'JPY': ('Yen Japonés', '¥'),
    'MXN': ('Peso Mexicano', '$'),
    'CAD': ('Dólar Canadiense', 'C$'),
    'GBP': ('Libra Esterlina', '£'),
    'BRL': ('Real Brasileño', 'R$'),
    'INR': ('Rupia India', '₹'),
    'AUD': ('Dólar Australiano', 'A$'),
    'GTQ': ('Quetzal Guatemalteco', 'Q')
}

# Nombres de países
NOMBRES_PAISES = {
    'USA': 'Estados Unidos',
    'CHN': 'China',
    'DEU': 'Alemania',
    'JPN': 'Japón',
    'MEX': 'México',
    'CAN': 'Canadá',
    'GBR': 'Reino Unido',
    'BRA': 'Brasil',
    'IND': 'India',
    'AUS': 'Australia',
    'GTM': 'Guatemala'
}

class GestorAranceles:
    def __init__(self):
        # Países disponibles con sus monedas
        self.paises = {
            'USA': {'moneda': 'USD', 'nombre': 'Estados Unidos'},
            'CHN': {'moneda': 'CNY', 'nombre': 'China'},
            'DEU': {'moneda': 'EUR', 'nombre': 'Alemania'},
            'JPN': {'moneda': 'JPY', 'nombre': 'Japón'},
            'MEX': {'moneda': 'MXN', 'nombre': 'México'},
            'CAN': {'moneda': 'CAD', 'nombre': 'Canadá'},
            'GBR': {'moneda': 'GBP', 'nombre': 'Reino Unido'},
            'BRA': {'moneda': 'BRL', 'nombre': 'Brasil'},
            'IND': {'moneda': 'INR', 'nombre': 'India'},
            'AUS': {'moneda': 'AUD', 'nombre': 'Australia'},
            'GTM': {'moneda': 'GTQ', 'nombre': 'Guatemala'}
        }
        
        # Tarifas de aranceles simplificadas (por país de destino)
        self.tarifas = {
            'USA': 0.017,
            'CHN': 0.04,
            'DEU': 0.023,
            'JPN': 0.026,
            'MEX': 0.035,
            'CAN': 0.015,
            'GBR': 0.021,
            'BRA': 0.045,
            'IND': 0.038,
            'AUS': 0.022,
            'GTM': 0.018  # Arancel para importaciones en Guatemala
        }
        
        # Costos logísticos por libra según tipo de producto (en USD)
        self.costos_logistica = {
            'Tecnología': 7.50,
            'Perecederos': 12.25,
            'Híbridos': 9.75
        }
    
    def obtener_tasa_cambio(self, moneda_origen, moneda_destino):
        """Obtiene tasa de cambio entre dos monedas usando USD como intermediario"""
        # Si alguna moneda no está en las tasas, usar USD como respaldo
        tasa_origen = TASAS_CAMBIO.get(moneda_origen, 1.0)
        tasa_destino = TASAS_CAMBIO.get(moneda_destino, 1.0)
        
        # Convertir: moneda_origen -> USD -> moneda_destino
        # 1 unidad de moneda_origen = (1 / tasa_origen) USD
        # 1 USD = tasa_destino unidades de moneda_destino
        # Por lo tanto: 1 unidad moneda_origen = (tasa_destino / tasa_origen) moneda_destino
        return tasa_destino / tasa_origen
    
    def calcular_costo_total(self, valor_producto, pais_origen, pais_destino, peso_lb, tipo_producto):
        """Calcula costo total del producto con conversión internacional"""
        # Obtener monedas de los países
        moneda_origen = self.paises[pais_origen]['moneda']
        moneda_destino = self.paises[pais_destino]['moneda']
        
        # Obtener tasa de cambio
        tasa_cambio = self.obtener_tasa_cambio(moneda_origen, moneda_destino)
        
        # Convertir el valor del producto a moneda destino
        valor_destino = valor_producto * tasa_cambio
        
        # Calcular arancel (basado en país destino)
        tasa_arancel = self.tarifas.get(pais_destino, 0.05)
        arancel_destino = valor_destino * tasa_arancel
        
        # Costos logísticos (en USD, luego convertimos a moneda destino)
        costo_logistica_usd = peso_lb * self.costos_logistica.get(tipo_producto, 0)
        # Convertir costo logística a moneda destino
        tasa_logistica = self.obtener_tasa_cambio('USD', moneda_destino)
        costo_logistica_destino = costo_logistica_usd * tasa_logistica
        
        total_destino = valor_destino + arancel_destino + costo_logistica_destino
        
        return {
            'valor_destino': valor_destino,
            'arancel_destino': arancel_destino,
            'costo_logistica_destino': costo_logistica_destino,
            'costo_logistica_usd': costo_logistica_usd,
            'total_destino': total_destino,
            'tasa_arancel': tasa_arancel,
            'moneda_origen': moneda_origen,
            'moneda_destino': moneda_destino,
            'tasa_cambio': tasa_cambio,
            'tasa_logistica': tasa_logistica
        }

class ChronosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chronos Supply Chain - Internacional")
        self.root.geometry("700x650")  # Tamaño más grande para el grid
        self.gestor = GestorAranceles()
        
        # Variables para selección
        self.pais_origen = tk.StringVar()
        self.pais_destino = tk.StringVar()
        
        # Crear la interfaz
        self.crear_interfaz()
        
        # Mostrar fecha actual
        fecha_actual = datetime.datetime.now().strftime("%d/%m/%Y")
        ttk.Label(self.root, text=f"Fecha: {fecha_actual}", 
                 font=('Arial', 9)).pack(anchor='ne', padx=10)
    
    def crear_interfaz(self):
        # Marco principal
        main_frame = ttk.Frame(self.root, padding=15)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Botón Menú en la parte superior izquierda
        btn_menu = ttk.Button(main_frame, text="Menú Principal", command=self.regresar_menu)
        btn_menu.pack(anchor='nw', pady=(0, 10))
        
        # Título de la aplicación
        ttk.Label(main_frame, text="Chronos Supply Chain - Internacional", 
                 font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Logo (simulado)
        logo_frame = ttk.Frame(main_frame)
        logo_frame.pack(pady=5)
        ttk.Label(logo_frame, text="✈️ CHRONOS GLOBAL", font=('Arial', 12)).pack()
        ttk.Label(logo_frame, text="Sistema Internacional de Importaciones", font=('Arial', 10)).pack()
        
        # Frame para selección de países
        paises_frame = ttk.LabelFrame(main_frame, text="Selección de Países", padding=10)
        paises_frame.pack(fill='x', pady=10)
        
        # Países de origen
        ttk.Label(paises_frame, text="País Origen:", font=('Arial', 10)).grid(row=0, column=0, padx=5, pady=5, sticky='w')
        paises_origen = list(self.gestor.paises.keys())
        self.combo_origen = ttk.Combobox(paises_frame, values=paises_origen, 
                                        textvariable=self.pais_origen, width=15)
        self.combo_origen.grid(row=0, column=1, padx=5, pady=5)
        self.combo_origen.bind('<<ComboboxSelected>>', self.actualizar_monedas)
        self.combo_origen.current(0)
        
        # Moneda origen
        self.label_moneda_origen = ttk.Label(paises_frame, text="Moneda: ", font=('Arial', 9))
        self.label_moneda_origen.grid(row=0, column=2, padx=10, pady=5, sticky='w')
        
        # Países de destino
        ttk.Label(paises_frame, text="País Destino:", font=('Arial', 10)).grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.combo_destino = ttk.Combobox(paises_frame, values=paises_origen, 
                                         textvariable=self.pais_destino, width=15)
        self.combo_destino.grid(row=1, column=1, padx=5, pady=5)
        self.combo_destino.bind('<<ComboboxSelected>>', self.actualizar_monedas)
        self.combo_destino.current(10)  # Guatemala por defecto
        
        # Moneda destino
        self.label_moneda_destino = ttk.Label(paises_frame, text="Moneda: ", font=('Arial', 9))
        self.label_moneda_destino.grid(row=1, column=2, padx=10, pady=5, sticky='w')
        
        # Frame para detalles del producto
        producto_frame = ttk.LabelFrame(main_frame, text="Detalles del Producto", padding=10)
        producto_frame.pack(fill='x', pady=10)
        
        # Valor del producto
        ttk.Label(producto_frame, text="Valor del producto:", font=('Arial', 10)).grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.entry_valor = ttk.Entry(producto_frame, width=15)
        self.entry_valor.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        
        # Moneda de valor
        self.label_moneda_valor = ttk.Label(producto_frame, text="en USD", font=('Arial', 9))
        self.label_moneda_valor.grid(row=0, column=2, padx=5, pady=5, sticky='w')
        
        # Peso en libras
        ttk.Label(producto_frame, text="Peso (libras):", font=('Arial', 10)).grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.entry_peso = ttk.Entry(producto_frame, width=10)
        self.entry_peso.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        
        # Tipo de producto
        ttk.Label(producto_frame, text="Tipo de producto:", font=('Arial', 10)).grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.combo_tipo = ttk.Combobox(producto_frame, values=['Tecnología', 'Perecederos', 'Híbridos'])
        self.combo_tipo.grid(row=2, column=1, padx=5, pady=5, sticky='w', columnspan=2)
        self.combo_tipo.current(0)
        
        # Botón de cálculo
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill='x', pady=15)
        
        btn_calcular = ttk.Button(btn_frame, text="Calcular Costo Total", 
                                 command=self.calcular_total, width=20)
        btn_calcular.pack(side='left', padx=(0, 10))
        
        btn_limpiar = ttk.Button(btn_frame, text="Limpiar", 
                                command=self.limpiar_campos, width=10)
        btn_limpiar.pack(side='left')
        
        # Área de resultados
        resultados_frame = ttk.LabelFrame(main_frame, text="Resultados del Cálculo", padding=10)
        resultados_frame.pack(fill='both', expand=True, pady=10)
        
        self.resultados_texto = tk.StringVar()
        self.resultados_texto.set("Complete los datos y haga clic en Calcular")
        
        resultados_label = ttk.Label(resultados_frame, textvariable=self.resultados_texto, 
                                   wraplength=650, justify='left', font=('Arial', 10))
        resultados_label.pack(fill='both', expand=True)
        
        # Actualizar monedas iniciales
        self.actualizar_monedas()
    
    def regresar_menu(self):
        self.root.destroy()
        # Ruta al menú principal
        script_dir = os.path.dirname(os.path.abspath(__file__))
        main_script = os.path.abspath(os.path.join(script_dir, '..', 'Uno_main.py'))
        subprocess.Popen([sys.executable, main_script])
        sys.exit()  # Cierra completamente este script
    
    def actualizar_monedas(self, event=None):
        """Actualiza la información de monedas cuando se selecciona un país"""
        # Obtener códigos de países seleccionados
        cod_origen = self.pais_origen.get()
        cod_destino = self.pais_destino.get()
        
        # Actualizar moneda origen
        if cod_origen in self.gestor.paises:
            moneda_origen = self.gestor.paises[cod_origen]['moneda']
            nombre, simbolo = NOMBRES_MONEDA.get(moneda_origen, (moneda_origen, moneda_origen))
            self.label_moneda_origen.config(text=f"Moneda: {nombre} ({simbolo})")
        
        # Actualizar moneda destino
        if cod_destino in self.gestor.paises:
            moneda_destino = self.gestor.paises[cod_destino]['moneda']
            nombre, simbolo = NOMBRES_MONEDA.get(moneda_destino, (moneda_destino, moneda_destino))
            self.label_moneda_destino.config(text=f"Moneda: {nombre} ({simbolo})")
    
    def calcular_total(self):
        """Calcula y muestra el costo total con desglose detallado"""
        try:
            # Obtener países seleccionados
            cod_origen = self.pais_origen.get()
            cod_destino = self.pais_destino.get()
            
            if not cod_origen:
                raise ValueError("Seleccione un país de origen")
            if not cod_destino:
                raise ValueError("Seleccione un país de destino")
            
            # Obtener otros datos
            valor = self.entry_valor.get().strip()
            peso = self.entry_peso.get().strip()
            tipo = self.combo_tipo.get()
            
            if not valor:
                raise ValueError("Ingrese el valor del producto")
            if not peso:
                raise ValueError("Ingrese el peso del producto")
            
            valor_num = float(valor)
            peso_num = float(peso)
            
            if valor_num <= 0:
                raise ValueError("El valor debe ser mayor que cero")
            if peso_num <= 0:
                raise ValueError("El peso debe ser mayor que cero")
            
            # Obtener nombres completos de países
            pais_origen = NOMBRES_PAISES.get(cod_origen, cod_origen)
            pais_destino = NOMBRES_PAISES.get(cod_destino, cod_destino)
            
            # Calcular costos
            resultados = self.gestor.calcular_costo_total(
                valor_num, cod_origen, cod_destino, peso_num, tipo
            )
            
            # Formatear resultados con desglose detallado
            resultado_texto = (
                f"Ruta: {pais_origen} → {pais_destino}\n"
                f"Tipo de producto: {tipo}\n"
                "------------------------------------------------\n"
                f"Valor del producto: {resultados['moneda_origen']}{valor_num:.2f}\n"
                f"Tasa de cambio: 1 {resultados['moneda_origen']} = "
                f"{resultados['tasa_cambio']:.4f} {resultados['moneda_destino']}\n"
                f"Valor en destino: {resultados['moneda_destino']}{resultados['valor_destino']:.2f}\n"
                "------------------------------------------------\n"
                f"Arancel ({resultados['tasa_arancel']*100:.1f}%): "
                f"{resultados['moneda_destino']}{resultados['arancel_destino']:.2f}\n"
                f"Costos logísticos:\n"
                f"  - Tarifa: ${resultados['costo_logistica_usd']:.2f} USD\n"
                f"  - Peso: {peso_num} lb\n"
                f"  - Total logística: {resultados['moneda_destino']}{resultados['costo_logistica_destino']:.2f}\n"
                "------------------------------------------------\n"
                f"TOTAL EN DESTINO: {resultados['moneda_destino']}{resultados['total_destino']:.2f}\n"
                "------------------------------------------------\n"
                f"Tasa logística: 1 USD = {resultados['tasa_logistica']:.4f} {resultados['moneda_destino']}"
            )
            
            self.resultados_texto.set(resultado_texto)
            
        except ValueError as e:
            messagebox.showerror("Error", f"Dato inválido: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
    
    def limpiar_campos(self):
        """Limpia todos los campos del formulario"""
        self.combo_origen.current(0)
        self.combo_destino.current(10)  # Guatemala por defecto
        self.actualizar_monedas()
        self.entry_valor.delete(0, tk.END)
        self.entry_peso.delete(0, tk.END)
        self.combo_tipo.current(0)
        self.resultados_texto.set("Complete los datos y haga clic en Calcular")

# Iniciar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = ChronosApp(root)
    root.mainloop()