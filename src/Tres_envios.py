"""
Contiene la clase Envio para gestionar productos y calcular costos de envío.
"""

from modulos.productos import Producto

class Envio:
    def __init__(self, origen, destino):
        self.origen = origen
        self.destino = destino
        self.productos = []

    def agregar_producto(self, producto):
        if isinstance(producto, Producto):
            self.productos.append(producto)
        else:
            raise ValueError("Solo se permiten objetos tipo Producto")

    def calcular_costo_total(self):
        return sum(p._valor + p.calcular_aranceles(self.destino) for p in self.productos)

    def generar_rastreo(self):
        return f"Envío de {self.origen} a {self.destino} con {len(self.productos)} producto(s)."

    def resumen_productos(self):
        return [f"{p._nombre} - ${p._valor}" for p in self.productos]
