import tkinter as tk
from tkinter import ttk, messagebox
import datetime

# Tasas de cambio actualizadas (ejemplo)
TASAS_CAMBIO = {
    'USD': {'GTQ': 7.82},    # Dólar estadounidense
    'EUR': {'GTQ': 8.42},    # Euro
    'CNY': {'GTQ': 1.09},    # Yuan chino
    'JPY': {'GTQ': 0.049},   # Yen japonés
    'MXN': {'GTQ': 0.42},    # Peso mexicano
    'CAD': {'GTQ': 5.86},    # Dólar canadiense
    'GBP': {'GTQ': 9.54},    # Libra esterlina
    'BRL': {'GTQ': 1.51},    # Real brasileño
    'INR': {'GTQ': 0.094},   # Rupia india
    'AUD': {'GTQ': 5.32}     # Dólar australiano
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

class GestorAranceles:
    def __init__(self):
        # Países disponibles (sin Guatemala)
        self.paises_monedas = {
            'USA': 'USD',
            'China': 'CNY',
            'Alemania': 'EUR',
            'Japón': 'JPY',
            'México': 'MXN',
            'Canadá': 'CAD',
            'Reino Unido': 'GBP',
            'Brasil': 'BRL',
            'India': 'INR',
            'Australia': 'AUD'
        }
        
        # Tarifas de aranceles simplificadas
        self.tarifas = {
            'USA': 0.017,
            'China': 0.04,
            'Alemania': 0.023,
            'Japón': 0.026,
            'México': 0.035,
            'Canadá': 0.015,
            'Reino Unido': 0.021,
            'Brasil': 0.045,
            'India': 0.038,
            'Australia': 0.022
        }
        
        # Costos por libra según tipo de producto
        self.costos_por_libra = {
            'Tecnología': 7,
            'Perecederos': 12,
            'Híbridos': 9
        }
    
    def obtener_tasa_cambio(self, moneda_origen):
        """Obtiene tasa de cambio de moneda origen a GTQ"""
        if moneda_origen in TASAS_CAMBIO:
            return TASAS_CAMBIO[moneda_origen]['GTQ']
        # En un sistema real, aquí se consultaría una API
        return 1.0  # Valor por defecto (no usar en producción)
    
    def calcular_costo_total(self, valor_producto, pais_origen, peso_lb, tipo_producto):
        """Calcula costo total del producto"""
        moneda_origen = self.paises_monedas.get(pais_origen, 'USD')
        
        # Convertir a GTQ
        tasa_a_gtq = self.obtener_tasa_cambio(moneda_origen)
        valor_gtq = valor_producto * tasa_a_gtq
        
        # Calcular arancel
        tasa_arancel = self.tarifas.get(pais_origen, 0.05)
        arancel_gtq = valor_gtq * tasa_arancel
        
        # Costos adicionales por tipo de producto (por libra)
        costo_por_libra = self.costos_por_libra.get(tipo_producto, 0)
        costo_extra = peso_lb * costo_por_libra
        
        total_gtq = valor_gtq + arancel_gtq + costo_extra
        
        return {
            'valor_gtq': valor_gtq,
            'arancel_gtq': arancel_gtq,
            'costo_extra': costo_extra,
            'costo_por_libra': costo_por_libra,
            'total_gtq': total_gtq,
            'tasa_arancel': tasa_arancel,
            'moneda_origen': moneda_origen,
            'tasa_cambio': tasa_a_gtq
        }

class ChronosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chronos Supply Chain")
        self.root.geometry("500x600")  # Tamaño más grande para más información
        self.gestor = GestorAranceles()
        
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
        
        # Título de la aplicación
        ttk.Label(main_frame, text="Chronos Supply Chain", 
                 font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Logo (simulado)
        logo_frame = ttk.Frame(main_frame)
        logo_frame.pack(pady=5)
        ttk.Label(logo_frame, text="✈️ CHRONOS", font=('Arial', 12)).pack()
        ttk.Label(logo_frame, text="Importaciones a Guatemala", font=('Arial', 10)).pack()
        
        # 1. Nombre del cliente
        ttk.Label(main_frame, text="Nombre completo:", font=('Arial', 10)).pack(anchor='w', pady=(10, 0))
        self.entry_nombre = ttk.Entry(main_frame, width=35)
        self.entry_nombre.pack(fill='x', pady=(0, 10))
        
        # 2. País de origen
        ttk.Label(main_frame, text="PAIS DEL PEDIDO / HACIA GUATEMALA:", 
                 font=('Arial', 10, 'bold')).pack(anchor='w', pady=(10, 0))
        self.combo_pais = ttk.Combobox(main_frame, values=list(self.gestor.paises_monedas.keys()))
        self.combo_pais.pack(fill='x', pady=(5, 5))
        self.combo_pais.bind('<<ComboboxSelected>>', self.actualizar_moneda)
        
        # Moneda local
        self.label_moneda = ttk.Label(main_frame, text="Seleccione un país", font=('Arial', 9))
        self.label_moneda.pack(anchor='w', pady=(0, 10))
        
        # Valor del producto
        ttk.Label(main_frame, text="Valor del producto:", font=('Arial', 10)).pack(anchor='w', pady=(5, 0))
        self.entry_valor = ttk.Entry(main_frame, width=15)
        self.entry_valor.pack(anchor='w', pady=(0, 10))
        
        # 3. Peso en libras
        ttk.Label(main_frame, text="Peso (libras):", font=('Arial', 10)).pack(anchor='w', pady=(5, 0))
        self.entry_peso = ttk.Entry(main_frame, width=10)
        self.entry_peso.pack(anchor='w', pady=(0, 10))
        
        # Tipo de producto
        ttk.Label(main_frame, text="Tipo de producto:", font=('Arial', 10)).pack(anchor='w', pady=(5, 0))
        self.combo_tipo = ttk.Combobox(main_frame, values=['Tecnología', 'Perecederos', 'Híbridos'])
        self.combo_tipo.pack(fill='x', pady=(0, 15))
        self.combo_tipo.current(0)
        
        # Botón de cálculo
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill='x', pady=10)
        btn_calcular = ttk.Button(btn_frame, text="Calcular Costo Total", command=self.calcular_total, width=20)
        btn_calcular.pack(side='left')
        
        btn_limpiar = ttk.Button(btn_frame, text="Limpiar", command=self.limpiar_campos, width=10)
        btn_limpiar.pack(side='right')
        
        # Área de resultados
        resultados_frame = ttk.LabelFrame(main_frame, text="Resultados del Cálculo", padding=10)
        resultados_frame.pack(fill='x', pady=10)
        
        self.resultados_texto = tk.StringVar()
        self.resultados_texto.set("Complete los datos y haga clic en Calcular")
        ttk.Label(resultados_frame, textvariable=self.resultados_texto, 
                 wraplength=450, justify='left', font=('Arial', 10)).pack(fill='x')
    
    def actualizar_moneda(self, event):
        """Actualiza la información de moneda cuando se selecciona un país"""
        pais = self.combo_pais.get()
        moneda = self.gestor.paises_monedas.get(pais, 'USD')
        
        if moneda in NOMBRES_MONEDA:
            nombre, simbolo = NOMBRES_MONEDA[moneda]
            self.label_moneda.config(text=f"{nombre} ({moneda} {simbolo})")
        else:
            self.label_moneda.config(text=f"Moneda: {moneda}")
    
    def calcular_total(self):
        """Calcula y muestra el costo total con desglose detallado"""
        try:
            # Validar datos
            nombre = self.entry_nombre.get().strip()
            pais = self.combo_pais.get().strip()
            valor = self.entry_valor.get().strip()
            peso = self.entry_peso.get().strip()
            tipo = self.combo_tipo.get()
            
            if not nombre:
                raise ValueError("Ingrese su nombre")
            if not pais:
                raise ValueError("Seleccione un país de origen")
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
            
            # Calcular costos
            resultados = self.gestor.calcular_costo_total(valor_num, pais, peso_num, tipo)
        
            # Formatear resultados con desglose detallado
            resultado_texto = (
                f"Cliente: {nombre}\n"
                f"Origen: {pais} ({resultados['moneda_origen']})\n"
                f"Tipo de producto: {tipo}\n"
                f"Tasa de cambio: 1 {resultados['moneda_origen']} = Q{resultados['tasa_cambio']:.3f}\n"
                "------------------------------------------------\n"
                f"Valor del producto: Q{resultados['valor_gtq']:.2f}\n"
                f"Arancel ({resultados['tasa_arancel']*100:.1f}%): Q{resultados['arancel_gtq']:.2f}\n"
                f"Costos logísticos para {tipo}:\n"
                f"  - Tarifa: Q{resultados['costo_por_libra']}/lb\n"
                f"  - Peso: {peso_num} lb\n"
                f"  - Total logística: Q{resultados['costo_extra']:.2f}\n"
                "------------------------------------------------\n"
                f"TOTAL: Q{resultados['total_gtq']:.2f}"
            )
            
            self.resultados_texto.set(resultado_texto)
            
        except ValueError as e:
            messagebox.showerror("Error", f"Dato inválido: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
    
    def limpiar_campos(self):
        """Limpia todos los campos del formulario"""
        self.entry_nombre.delete(0, tk.END)
        self.combo_pais.set('')
        self.label_moneda.config(text="Seleccione un país")
        self.entry_valor.delete(0, tk.END)
        self.entry_peso.delete(0, tk.END)
        self.combo_tipo.current(0)
        self.resultados_texto.set("Complete los datos y haga clic en Calcular")

# Iniciar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = ChronosApp(root)
    root.mainloop()



