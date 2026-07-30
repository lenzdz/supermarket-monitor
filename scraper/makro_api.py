import requests
from bs4 import BeautifulSoup
import re

def info_producto_makro(url):

    html = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    ).text

    soup = BeautifulSoup(html, "html.parser")

    scripts = soup.find_all("script")

    for script in scripts:
        texto = script.string

        if texto and "CatalogProductModel" in texto:
            #print(texto[:1000])
            break

    # Encuentra el nombre del producto
    nombre_del_producto = re.search(
        r'"name":"([^"]+)"',
        html
    ).group(1)

    nombre_del_producto = nombre_del_producto.title()

    # Encuentra el precio pleno del producto (no supe acceder a la API y tocó así, pidoperdón)
    # Elimina lo que está después del precio pleno en el script de HTML
    substring = ',\\\"photosUrl'
    res = texto.split(substring, 1)[0]
    # Elimina lo que está antes del precio pleno en el script de HTML
    index = res.find('price')
    res = res[(index+8):]
    precio_pleno = int(res)

    # Encuentra el precio con descuento o normal, si no lo hay
    precio_hoy = int(
        re.search(r'"price":(\d+)', html).group(1)
    )

    informacion_del_producto = {
                "url": url,
                "nombre": nombre_del_producto,
                "precio_pleno": precio_pleno,
                "precio_hoy": precio_hoy,
                "precio_con_descuento": precio_hoy
            }

    return informacion_del_producto
