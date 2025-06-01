"""
Genera un documento resumen para exportación e importación.
"""

def generar_documento_envio(envio):
    documento = ["""--- DOCUMENTACIÓN ADUANERA ---"""]
    documento.append(f"Origen: {envio.origen}")
    documento.append(f"Destino: {envio.destino}")
    documento.append(f"Cantidad de productos: {len(envio.productos)}\n")

    for producto in envio.productos:
        documento.append(f"Producto: {producto._nombre}")
        documento.append(f"Valor: ${producto._valor:.2f}")
        documento.append(f"Arancel: ${producto.calcular_aranceles(envio.destino):.2f}")
        documento.append(producto.generar_documentacion())
        documento.append("---")

    documento.append("FIN DEL DOCUMENTO")
    return "\n".join(documento)
