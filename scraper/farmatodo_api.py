"""
scraper/farmatodo_api.py

Cliente para consultar la API de Farmatodo.
"""

import requests


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

    respuesta = requests.get(
        BASE_URL,
        params=params,
        headers=headers,
        timeout=20,
    )

    # print(respuesta.raise_for_status())
    # print(respuesta.json())

    return respuesta.json()


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
            "descuento",
            "descripcion_descuento",
            "stock"
        }
    """

    respuesta = obtener_producto(id_producto)

    producto = (
        respuesta["itemSection"][0]
                 ["list"][0]
                 ["product"][0]
    )

    precio_pleno = producto["fullPrice"]
    precio_hoy = producto["offerPrice"]

    # Si no existe descuento, offerPrice suele ser igual al precio pleno.
    if precio_hoy < precio_pleno:
        precio_con_descuento = precio_hoy
    else:
        precio_con_descuento = None

    if precio_con_descuento != None:

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