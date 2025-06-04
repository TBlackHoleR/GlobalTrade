"""
Módulo para registrar transacciones de envío.
"""

import datetime

HISTORIAL_TRANSACCIONES = []

def registrar_transaccion(envio):
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    HISTORIAL_TRANSACCIONES.append({
        "fecha": fecha,
        "resumen": envio.generar_rastreo(),
        "costo_total": envio.calcular_costo_total()
    })

def mostrar_historial():
    return [f"[{r['fecha']}] {r['resumen']} - Costo: ${r['costo_total']:.2f}" for r in HISTORIAL_TRANSACCIONES]
