import json

# Módulos externos
from datetime import datetime

from scraper.jumbo_api import info_producto_jumbo
from services.monitor_comparables import comparacion_jumbo_a_olimpica

from notifiers.discord import enviar_mensaje_canal_jumbo
from notifiers.discord import enviar_mensaje_canal_errores

fecha_hoy = datetime.now().strftime("%d/%m/%Y")

# LÓGICA JUMBO --------------------------------------------------

def monitor_jumbo():

    with open("data/productos_jumbo.json", encoding="utf-8") as archivo:
        productos_jumbo = json.load(archivo)   

    enviar_mensaje_canal_jumbo(f"🎉 Productos en oferta ahora ({fecha_hoy}) 🎉")

    counter = 0
    for producto in productos_jumbo:
        id_producto = producto["ean"]

        # Verifica si el producto tiene descuentos. Si hay descuentos, devuelve la información del producto; si no los hay, devuelve None.
        resultado = revisar_producto_jumbo(id_producto)

        mensaje = ""
        if resultado:
            counter += 1

            nombre = resultado["nombre"]
            precio_pleno = resultado["precio_pleno"]
            precio_hoy = resultado["precio_hoy"]
            precio_con_descuento = resultado["precio_con_descuento"]

            mensaje += (
                f"-------------------------------------------\n"
                f"{producto['emoji']} **{nombre}**\n"
                f"**Precio normal:** ${precio_pleno:,.0f}\n"
                f"**Precio actual:** ${precio_hoy:,.0f}\n"
            )

            if (precio_con_descuento != None):
                mensaje += (
                    f"**Con Prime:** ${precio_con_descuento:,.0f}\n"
                )

            mensaje += comparacion_jumbo_a_olimpica(id_producto, resultado)

            enviar_mensaje_canal_jumbo(mensaje)

    if (counter == 0):
        mensaje_final = f"-------------------------------------------\n Hoy no hay productos en oferta 🙁"
    elif (counter == 1):
        mensaje_final = (
            f"-------------------------------------------\n"
            f"🎉 Hoy hay {counter} producto en oferta ({fecha_hoy}) 🎉 \n"
        )
    else:
        mensaje_final = (
            f"-------------------------------------------\n"
            f"🎉 Hoy hay {counter} productos en oferta ({fecha_hoy}) 🎉 \n"
        )

    enviar_mensaje_canal_jumbo(mensaje_final)

def revisar_producto_jumbo(id_producto):

    datos_producto = info_producto_jumbo(id_producto)

    try: 
        
        if datos_producto["precio_hoy"] < datos_producto["precio_pleno"]:
            return datos_producto
        elif (datos_producto["precio_con_descuento"] != None) and (datos_producto["precio_con_descuento"] < datos_producto["precio_pleno"]):
            return datos_producto
        
        # Para ver todos los productos en la base de datos, devolver datos_producto
        return None

    except Exception as e:
        enviar_mensaje_canal_errores(
            f"Error en Monitor Jumbo para producto {id_producto}: {type(e).__name__}: {e}"
        )

        return None