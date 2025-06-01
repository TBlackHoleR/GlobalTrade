"""
Base de datos simulada de tarifas aduaneras por país destino.
"""

TARIFAS_ADUANERAS = {
    "Chile": 0.05,
    "España": 0.12,
    "Estados Unidos": 0.08,
    "Alemania": 0.10,
    "Brasil": 0.09
}

def obtener_tarifa_por_pais(pais_destino):
    return TARIFAS_ADUANERAS.get(pais_destino, 0.05)
