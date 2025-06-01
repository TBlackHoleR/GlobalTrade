"""
Módulo de conversión monetaria entre distintas divisas.
Las tasas son simuladas.
"""

TASAS_CAMBIO = {
    ("USD", "EUR"): 0.91,
    ("USD", "CLP"): 900.0,
    ("EUR", "USD"): 1.1,
    ("CLP", "USD"): 0.0011
}

def convertir_moneda(monto, moneda_origen, moneda_destino):
    if moneda_origen == moneda_destino:
        return monto
    tasa = TASAS_CAMBIO.get((moneda_origen, moneda_destino))
    if not tasa:
        raise ValueError("Tasa no encontrada")
    return monto * tasa
