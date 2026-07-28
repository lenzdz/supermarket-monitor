import base64
import json
import requests

# BASE_URL = "https://www.jumbocolombia.com/_v/segment/graphql/v1"


# def obtener_flags_producto(product_id):
#     # 1. Crear {"id":98321}
#     variables = json.dumps(
#         {"id": product_id},
#         separators=(",", ":")
#     )

#     # 2. Convertir a Base64
#     variables_b64 = base64.b64encode(
#         variables.encode("utf-8")
#     ).decode("utf-8")

#     # 3. Crear el objeto extensions
#     extensions = {
#         "persistedQuery": {
#             "version": 1,
#             "sha256Hash": "7c16412d187093332665a3e33f79165687dbedbe291daa6842655678493fd1fd",
#             "sender": "tiendasjumboqaio.jumbo-minicart@2.x",
#             "provider": "vtex.search-graphql@0.x"
#         },
#         "variables": variables_b64
#     }

#     params = {
#         "workspace": "master",
#         "maxAge": "short",
#         "appsEtag": "remove",
#         "domain": "store",
#         "locale": "es-CO",
#         "operationName": "getProductInfo",
#         "variables": "{}",
#         "extensions": json.dumps(
#             extensions,
#             separators=(",", ":")
#         )
#     }

#     headers = {
#         "User-Agent": "Mozilla/5.0",
#         "Accept": "application/json"
#     }

#     respuesta = requests.get(
#         BASE_URL,
#         params=params,
#         headers=headers
#     )

#     # print("URL generada:")
#     # print(respuesta.url)
#     # print()

#     # print("Status:", respuesta.status_code)

#     #print(respuesta.text)
#     return respuesta.json()

BASE_URL = "https://www.jumbocolombia.com/_v/public/graphql/v1"


import base64
import json
import requests

BASE_URL = "https://www.jumbocolombia.com/_v/segment/graphql/v1"


def obtener_producto(product_id):

    variables = json.dumps(
        {"id": int(product_id)},
        separators=(",", ":")
    )

    variables_b64 = base64.b64encode(
        variables.encode("utf-8")
    ).decode("utf-8")

    extensions = {
        "persistedQuery": {
            "version": 1,
            "sha256Hash": "7c16412d187093332665a3e33f79165687dbedbe291daa6842655678493fd1fd",
            "sender": "tiendasjumboqaio.jumbo-minicart@2.x",
            "provider": "vtex.search-graphql@0.x"
        },
        "variables": variables_b64
    }

    params = {
        "workspace": "master",
        "maxAge": "short",
        "appsEtag": "remove",
        "domain": "store",
        "locale": "es-CO",
        "__bindingId": "2aad81c0-c729-41f4-a13b-002deae8039a",
        "operationName": "getProductInfo",
        "variables": "{}",
        "extensions": json.dumps(
            extensions,
            separators=(",", ":")
        )
    }

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }

    respuesta = requests.get(
        BASE_URL,
        params=params,
        headers=headers,
        timeout=30
    )

    # print("URL generada:")
    # print(respuesta.url)
    # print()

    # print("Status:", respuesta.status_code)

    return respuesta.json()

def obtener_descuento(info_producto):
    precio_pleno = info_producto["data"]["product"]["items"][0]["sellers"][0]["commertialOffer"]["Price"]

    try:
        cards = (
            info_producto["data"]["getProduct"]["product"]["cards"]
        )

        if not cards:
            return None

        return cards[0]["finalPrice"]
    except KeyError:
        teasers = (
                info_producto["data"]["product"]["items"][0]["sellers"][0]["commertialOffer"]["teasers"]
            )

        if not teasers:
            return None

        # Precio con descuento, si hay
        descuento = info_producto["data"]["product"]["items"][0]["sellers"][0]["commertialOffer"]["teasers"][0]["effects"]["parameters"][0]["value"]
        precio_con_descuento = int(precio_pleno - ((precio_pleno*int(descuento))/100))

        return precio_con_descuento

def info_producto_jumbo(id_producto):
    info_producto_desde_api = obtener_producto(id_producto)

    precio_con_descuento = obtener_descuento(info_producto_desde_api)

    # Nombre del producto
    nombre_del_producto = str(info_producto_desde_api["data"]["product"]["productName"]).title()

    # Precio pleno del producto
    precio_pleno = info_producto_desde_api["data"]["product"]["items"][0]["sellers"][0]["commertialOffer"]["ListPrice"]

    # Precio de hoy del producto (puede ser pleno o tener descuento para todos los medios de pago)
    precio_hoy = info_producto_desde_api["data"]["product"]["items"][0]["sellers"][0]["commertialOffer"]["Price"]

    informacion_del_producto = {
        "id": id_producto,
        "nombre": nombre_del_producto,
        "precio_pleno": precio_pleno,
        "precio_hoy": precio_hoy,
        "precio_con_descuento": precio_con_descuento
    }

    return informacion_del_producto