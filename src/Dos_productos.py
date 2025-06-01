"""
Define las clases de productos para el sistema GlobalTrade.
Incluye herencia y polimorfismo para distintos tipos de productos.
"""

from modulos.tarifas import obtener_tarifa_por_pais

class Producto:
    def __init__(self, id, nombre, peso, valor):
        self._id = id
        self._nombre = nombre
        self._peso = peso
        self._valor = valor
        self._pais_origen = ""

    def calcular_aranceles(self, pais_destino):
        tasa = obtener_tarifa_por_pais(pais_destino)
        return self._valor * tasa

    def generar_documentacion(self):
        return f"Producto base: {self._nombre} - ID: {self._id}"

class ProductoPerecedero(Producto):
    def __init__(self, id, nombre, peso, valor, fecha_expiracion):
        super().__init__(id, nombre, peso, valor)
        self.fecha_expiracion = fecha_expiracion

    def generar_documentacion(self):
        return f"Perecedero - Expira: {self.fecha_expiracion}"

class ProductoElectronico(Producto):
    def __init__(self, id, nombre, peso, valor, voltaje):
        super().__init__(id, nombre, peso, valor)
        self.voltaje = voltaje

    def generar_documentacion(self):
        return f"Electrónico - Voltaje: {self.voltaje}"
