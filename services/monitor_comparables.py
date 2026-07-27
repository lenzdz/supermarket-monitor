import json

from scraper.jumbo_api import info_producto_jumbo
from scraper.olimpica_api import info_producto_olimpica
from scraper.cruzverde_api import CruzVerdeClient

with open("data/productos_comparables.json", encoding="utf-8") as archivo:
    productos_comparables = json.load(archivo) 

def comparacion_cruzverde_a_olimpica(codigo, precio_prod_cruzverde):

    for producto_comp in productos_comparables:

        mensaje = ""
        # Si el producto que tiene descuento está en la lista de artículos comparables, revisa si el precio en Jumbo es menor que el de Olímpica hoy (en general)
        if (codigo == producto_comp["cruzverde"]):
            item_olimpica = info_producto_olimpica(producto_comp["olimpica"])
            precio_item_olimpica = item_olimpica["precio_hoy"]
            if precio_prod_cruzverde > precio_item_olimpica:
                mensaje += f"⚠️ Ojo: este producto hoy cuesta menos en Olímpica (${precio_item_olimpica:,.0f})."
            break
    return mensaje

def comparacion_jumbo_a_olimpica(ean, resultado):

    for producto_comp in productos_comparables:

        mensaje = ""
        # Si el producto que tiene descuento está en la lista de artículos comparables, revisa si el precio en Jumbo es menor que el de Olímpica hoy (en general)
        if (ean == producto_comp["jumbo"]):
            item_olimpica = info_producto_olimpica(producto_comp["olimpica"])
            if item_olimpica != None:
                precio_item_olimpica = item_olimpica["precio_hoy"]
                if resultado["precio_hoy"] > precio_item_olimpica:
                    mensaje += f"⚠️ Ojo: este producto hoy cuesta menos en Olímpica (${precio_item_olimpica:,.0f})."
                break
    return mensaje

def comparacion_olimpica_a_cruzverde(id_producto, resultado, diccionario_productos_cruzverde):

    for producto_comp in productos_comparables:

        mensaje = ""
        # Si el producto que tiene descuento está en la lista de artículos comparables, revisa si el precio en Cruz Verde es menor que el de Olímpica hoy (en general)
        if (id_producto == producto_comp["olimpica"]):
            for item in diccionario_productos_cruzverde:
                if item["id"] == producto_comp["cruzverde"]:
                    item_cruzverde = item
                    precio_item_cruzverde = item_cruzverde["precio_con_descuento"]
                    if resultado["precio_hoy"] > precio_item_cruzverde:
                        mensaje += f"⚠️ Ojo: este producto hoy cuesta menos en Cruz Verde (${precio_item_cruzverde:,.0f})."
                    break

    return mensaje

def comparacion_olimpica_a_jumbo(id_producto, resultado):

    for producto_comp in productos_comparables:

        mensaje = ""
        # Si el producto que tiene descuento está en la lista de artículos comparables, revisa si el precio en Jumbo es menor que el de Olímpica hoy (en general)
        if (id_producto == producto_comp["olimpica"]):
            # Si el producto está en los comparables que aplican para Jumbo, ejecuta el siguiente bloque
            if (producto_comp["jumbo"] != 0):
                item_jumbo = info_producto_jumbo(producto_comp["jumbo"])
                precio_item_jumbo = item_jumbo["precio_hoy"]
                if resultado["precio_hoy"] > precio_item_jumbo:
                    mensaje += f"⚠️ Ojo: este producto hoy cuesta menos en Jumbo (${precio_item_jumbo:,.0f})."
                break

    return mensaje