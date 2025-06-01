"""
Archivo principal del sistema GlobalTrade.
Permite gestionar productos, envíos, conversiones monetarias y documentación.
"""

from modulos.productos import ProductoPerecedero, ProductoElectronico
from modulos.envio import Envio
from modulos.conversion import convertir_moneda
from modulos.documentacion import generar_documento_envio
from modulos.historial import registrar_transaccion, mostrar_historial

# Crear productos de ejemplo
manzanas = ProductoPerecedero(id=1, nombre="Manzanas", peso=10, valor=30, fecha_expiracion="2025-07-01")
celular = ProductoElectronico(id=2, nombre="Celular", peso=1, valor=300, voltaje=220)

# Crear un envío
envio = Envio(origen="Chile", destino="España")
envio.agregar_producto(manzanas)
envio.agregar_producto(celular)

# Registrar la transacción
registrar_transaccion(envio)

# Mostrar la documentación generada
print(generar_documento_envio(envio))

# Mostrar historial
print("\n--- HISTORIAL DE TRANSACCIONES ---")
for registro in mostrar_historial():
    print(registro)
