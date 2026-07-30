import json

# Módulos externos
from datetime import datetime

from scraper.cruzverde_api import CruzVerdeClient
from services.monitor_comparables import comparacion_cruzverde_a_olimpica

from notifiers.discord import enviar_mensaje_canal_cruzverde

with open("data/productos_cruzverde.json", encoding="utf-8") as f:
    productos_cruzverde = json.load(f)

def monitor_cruzverde():

    cliente = CruzVerdeClient()

    cliente.iniciar()

    try:

        fecha_hoy = datetime.now().strftime("%d/%m/%Y")
        enviar_mensaje_canal_cruzverde(f"🎉 Productos en oferta ahora ({fecha_hoy}) 🎉")
        
        registros = []
        for producto in productos_cruzverde:

            mensaje = ""
            registro = cliente.obtener_producto(
                producto_id = producto["id"]
            )

            registros.append(registro)

            nombre = registro["nombre"]
            precio_pleno = registro["precio_pleno"]
            precio_con_descuento = registro["precio_con_descuento"]

            mensaje += (
                    f"-------------------------------------------\n"
                    f"{producto['emoji']} **{nombre}**\n"
                    f"**Precio normal:** ${precio_pleno:,.0f}\n"
                    f"**Club Cruz Verde:** ${precio_con_descuento:,.0f}\n"
                )

            mensaje += comparacion_cruzverde_a_olimpica(producto["id"], precio_con_descuento)
            
            enviar_mensaje_canal_cruzverde(mensaje)

        if (len(registros) == 0):
            mensaje_final = f"-------------------------------------------\n Hoy no hay productos en oferta 🙁"
        elif (len(registros) == 1):
            mensaje_final = (
                f"-------------------------------------------\n"
                f"🎉 Hoy hay {len(registros)} producto en oferta ({fecha_hoy}) 🎉 \n"
            )
        else:
            mensaje_final = (
                f"-------------------------------------------\n"
                f"🎉 Hoy hay {len(registros)} productos en oferta ({fecha_hoy}) 🎉 \n"
            )

        enviar_mensaje_canal_cruzverde(mensaje)

    finally:

        cliente.cerrar()
    
    return registros