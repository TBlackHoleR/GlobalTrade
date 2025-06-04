"""
Contiene la clase Envio para gestionar productos y calcular costos de envío.
"""

from src.Dos_productos import ProductoPerecedero, ProductoElectronico

class Envio:
    def __init__(self, origen, destino):
        self.origen = origen
        self.destino = destino
        self.productos = []

    def agregar_producto(self, producto):
        if isinstance(producto, (ProductoPerecedero, ProductoElectronico)):
            self.productos.append(producto)

    def calcular_costo_total(self):
        return sum(p.valor for p in self.productos)

    def generar_reporte(self):
        reporte = f"Envío desde {self.origen} hacia {self.destino}:\n"
        for p in self.productos:
            reporte += f"- {p.nombre}: ${p.valor}\n"
        reporte += f"Total: ${self.calcular_costo_total()}"
        return reporte
