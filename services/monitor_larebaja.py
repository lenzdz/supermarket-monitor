import json

# Módulos externos
from datetime import datetime

from scraper.larebaja_api import info_producto_larebaja

from notifiers.discord import enviar_mensaje_canal_larebaja

fecha_hoy = datetime.now().strftime("%d/%m/%Y")

# LÓGICA LA REBAJA -------------------------------------------------- 

def monitor_larebaja(diccionario_productos_cruzverde):

    with open("data/productos_larebaja.json", encoding="utf-8") as archivo:
        productos_larebaja = json.load(archivo)

    enviar_mensaje_canal_larebaja(f"🎉 Productos en oferta ahora ({fecha_hoy}) 🎉")

    counter = 0
    for producto in productos_larebaja:
        id_producto = producto["id"]

        # Verifica si el producto tiene descuentos. Si hay descuentos, devuelve la información del producto; si no los hay, devuelve None.
        resultado = revisar_producto_larebaja(id_producto)

        mensaje = ""
        if resultado:
            counter += 1

            nombre = resultado["nombre"]
            precio_pleno = resultado["precio_pleno"]
            precio_hoy = resultado["precio_hoy"]

            mensaje += (
                f"-------------------------------------------\n"
                f"{producto['emoji']} **{nombre}**\n"
                f"**Precio normal:** ${precio_pleno:,.0f}\n"
                f"**Precio actual:** ${precio_hoy:,.0f}\n"
            )

            enviar_mensaje_canal_larebaja(mensaje)

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

    enviar_mensaje_canal_larebaja(mensaje_final)

def revisar_producto_larebaja(id_producto):

    datos_producto = info_producto_larebaja(id_producto)

    if datos_producto:
        if datos_producto["precio_hoy"] < datos_producto["precio_pleno"]:
            return datos_producto
    
    # Para ver todos los productos en la base de datos, devolver datos_producto
    return None