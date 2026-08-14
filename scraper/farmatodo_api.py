"""
scraper/farmatodo_api.py

Cliente para consultar la API de Farmatodo.
"""

import requests

from notifiers.discord import enviar_mensaje_canal_errores


BASE_URL = (
    "https://gw-backend.farmatodo.com/ah/api/productEndpoint/v2/getItem"
)


def obtener_producto(
    id_producto
):
    """
    Consulta un producto en la API de Farmatodo.

    Parámetros
    ----------
    id_producto : str | int
        ID interno del producto.

    id_store : int
        Tienda desde donde consultar el inventario.

    ciudad : str
        Código de la ciudad.

    delivery_type : str
        Tipo de entrega.

    Retorna
    -------
    dict
        Respuesta JSON completa de la API.
    """

    params = {
        "source": "WEB",
        "idItem": id_producto,
        "idCustomerWebSafe": "ahZzfnN0dW5uaW5nLWJhc2UtMTY0NDAyci4LEgRVc2VyIiRlNWQzMzA0Yi1iMjBiLTRhMWItODExYS1jMjM3ZWFhYmRiZTQM",
        "idStoreGroup": 26,
        "nearbyStores": "26,20,67,3,85,24,31,88,81,83,89,15,54,1122",
        "token": "21af12f83ce8d30758ab7bd056274615",
        "tokenIdWebSafe": "ahZzfnN0dW5uaW5nLWJhc2UtMTY0NDAycl0LEgRVc2VyIiRlNWQzMzA0Yi1iMjBiLTRhMWItODExYS1jMjM3ZWFhYmRiZTQMCxIFVG9rZW4iJDg5YTVlMDBlLTY2MGEtNDAzZC05MDYwLWNjMTZiZjM5NTI2NAw",
        "key": "AIzaSyAidR6Tt0K60gACR78aWThMQb7L5u6Wpag",
        "deliveryType": "EXPRESS",
        "storeId": 26,
        "city": "BOG",
        "isShoppingCart": "false",
        "customerId": "undefined",
    }

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "country": "COL",
        "finalCountry": "Colombia",
        "source": "WEB",
        "ipaddress": "179.19.83.254",
    }

    try:

        respuesta = requests.get(
            BASE_URL,
            params=params,
            headers=headers,
            timeout=20,
        )

        # print(respuesta.raise_for_status())
        # print(respuesta.json())

        if not respuesta.ok:

            enviar_mensaje_canal_errores(
                f"Error HTTP {respuesta.status_code} en Farmatodo API\n"
                f"Producto: {id_producto}\n"
                f"Respuesta: {respuesta.text[:500]}"
            )

            return None

        try:

            return respuesta.json()

        except requests.exceptions.JSONDecodeError:

            enviar_mensaje_canal_errores(
                f"Farmatodo no devolvió JSON válido\n"
                f"Producto: {id_producto}\n"
                f"Status: {respuesta.status_code}\n"
                f"Content-Type: {respuesta.headers.get('Content-Type')}\n"
                f"Respuesta: {respuesta.text[:500]}"
            )

            return None

    except requests.exceptions.Timeout:

        enviar_mensaje_canal_errores(
            f"Timeout de 20 segundos consultando Farmatodo\n"
            f"Producto: {id_producto}"
        )

        return None

    except requests.exceptions.RequestException as e:

        enviar_mensaje_canal_errores(
            f"Error de conexión consultando Farmatodo\n"
            f"Producto: {id_producto}\n"
            f"Error: {e}"
        )

        return None


def info_producto_farmatodo(id_producto):
    """
    Devuelve la información relevante de un producto.

    Retorna
    -------
    dict
        {
            "id",
            "nombre",
            "precio_pleno",
            "precio_hoy",
            "precio_con_descuento",
        }
    """

    respuesta = obtener_producto(id_producto)

    # La API falló o no devolvió JSON válido.
    if respuesta is None:
        return None

    try:

        producto = (
            respuesta["itemSection"][0]
                     ["list"][0]
                     ["product"][0]
        )

        precio_pleno = producto["fullPrice"]
        precio_hoy = producto["offerPrice"]

        # Si no existe descuento, offerPrice suele ser
        # igual al precio pleno.
        if precio_hoy < precio_pleno and precio_hoy != 0:
            precio_con_descuento = precio_hoy
        else:
            precio_con_descuento = None

        if precio_con_descuento is not None:
            informacion_producto = {
                "id": producto["id"],
                "nombre": producto["mediaDescription"],
                "precio_pleno": precio_pleno,
                "precio_hoy": precio_hoy,
                "precio_con_descuento": precio_con_descuento
            }

            return informacion_producto

        else:
            return None

    except (KeyError, IndexError, TypeError):

        enviar_mensaje_canal_errores(
            f"Respuesta inesperada de Farmatodo\n"
            f"Producto: {id_producto}"
        )

        return None