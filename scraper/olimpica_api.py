import base64
import json
import requests

BASE_URL = "https://www.olimpica.com/_v/segment/graphql/v1"


def obtener_flags_producto(product_id):
    # 1. Crear {"id":98321}
    variables = json.dumps(
        {"id": product_id},
        separators=(",", ":")
    )

    # 2. Convertir a Base64
    variables_b64 = base64.b64encode(
        variables.encode("utf-8")
    ).decode("utf-8")

    # 3. Crear el objeto extensions
    extensions = {
        "persistedQuery": {
            "version": 1,
            "sha256Hash": "7743f21f216baaab0deed5195f58ba0dffd4e2672d488284b34b00cb8fa93d31",
            "sender": "olimpica.dinamic-flags@0.x",
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
        headers=headers
    )

    # print("URL generada:")
    # print(respuesta.url)
    # print()

    # print("Status:", respuesta.status_code)

    return respuesta.json()

def obtener_descuento(info_producto):
    teasers = (
        info_producto["data"]["product"]["items"][0]["sellers"][0]["commertialOffer"]["teasers"]
    )

    if not teasers:
        return None

    return teasers[0]["effects"]["parameters"][0]["value"]

def info_producto_olimpica(id_producto):
    info_producto_desde_api = obtener_flags_producto(id_producto)

    try:

        descuento = obtener_descuento(info_producto_desde_api)

        # Nombre del producto
        nombre_del_producto = str(info_producto_desde_api["data"]["product"]["productName"]).title()

        # Precio pleno del producto
        precio_pleno = info_producto_desde_api["data"]["product"]["items"][0]["sellers"][0]["commertialOffer"]["ListPrice"]

        # Precio de hoy del producto (puede ser pleno o tener descuento para todos los medios de pago)
        precio_hoy = info_producto_desde_api["data"]["product"]["items"][0]["sellers"][0]["commertialOffer"]["Price"]

        # Precio con descuento, si hay
        if descuento != None:
            precio_con_descuento = int(precio_pleno - ((precio_pleno*int(descuento))/100))
        else:
            precio_con_descuento = precio_hoy

        informacion_del_producto = {
            "id": id_producto,
            "nombre": nombre_del_producto,
            "precio_pleno": precio_pleno,
            "precio_hoy": precio_hoy,
            "precio_con_descuento": precio_con_descuento
        }

        return informacion_del_producto
    
    except TypeError:

        print("TypeError en API Olímpica: no se encontró un producto con ID " + str(id_producto))
        return None

    except KeyError:
    
            print("KeyError en API Olímpica: no se encontró un producto con ID " + str(id_producto))
            return None