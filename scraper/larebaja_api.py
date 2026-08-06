import requests

from notifiers.discord import enviar_mensaje_canal_errores

BASE_URL = "https://www.larebajavirtual.com/api/catalog_system/pub/products/search"

def obtener_producto(id_producto):

    params = {
        "fq": f"skuId:{id_producto}"
    }

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }

    respuesta = requests.get(
        BASE_URL,
        params=params,
        headers=headers,
        timeout=15
    )

    respuesta.raise_for_status()

    return respuesta.json()

def info_producto_larebaja(id_producto):

    try:

        producto = obtener_producto(id_producto)[0]

        seller = producto["items"][0]["sellers"][0]
        oferta = seller["commertialOffer"]

        informacion_del_producto = {
            "id": id_producto,
            "nombre": producto["productName"].title(),
            "precio_pleno": int(oferta["ListPrice"]),
            "precio_hoy": int(oferta["Price"]),
            "precio_con_descuento": int(oferta["Price"])
        }

        return informacion_del_producto

    except IndexError:

        enviar_mensaje_canal_errores(
            f"IndexError en larebaja_api.py\n"
            f"No se encontró el producto con ID {id_producto}"
        )

        return None

    except KeyError:

        enviar_mensaje_canal_errores(
            f"KeyError en larebaja_api.py\n"
            f"No se encontró el producto con ID {id_producto}"
        )

        return None