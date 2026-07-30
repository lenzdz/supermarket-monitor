"""
scraper/cruzverde_api.py

Cliente para consultar la API de Cruz Verde.
"""

from playwright.sync_api import sync_playwright


class CruzVerdeClient:
    API_URL = "https://api.cruzverde.com.co/product-service/products/detail"

    def __init__(self, headless=True):
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    def iniciar(self):
        """Inicia Playwright y crea la sesión de Cruz Verde."""

        self.playwright = sync_playwright().start()

        self.browser = self.playwright.chromium.launch(
            headless=self.headless
        )

        self.context = self.browser.new_context()

        self.page = self.context.new_page()

        # Crear la sesión una sola vez
        self.page.goto(
            "https://www.cruzverde.com.co/",
            wait_until="networkidle"
        )

        self.page.wait_for_timeout(5000)

    def cerrar(self):
        """Cierra el navegador."""

        if self.browser:
            self.browser.close()

        if self.playwright:
            self.playwright.stop()

    def obtener_producto(
        self,
        producto_id,
        inventory_id="COCV_zona64"
    ):
        """
        Consulta un producto en la API de Cruz Verde.

        Parámetros
        ----------
        producto_id : str
            Ejemplo:
            COCV_146476

        inventory_id : str
            Zona de inventario.

        Retorna
        -------
        dict
            JSON completo devuelto por la API.
        """

        respuesta = self.context.request.get(
            f"{self.API_URL}/{producto_id}",
            params={
                "inventoryId": inventory_id
            }
        )

        respuesta_json = respuesta.json()

        precios = respuesta_json["productData"]["prices"]
        precio_pleno = precios["price-list-col"]

        precio_con_descuento = precio_pleno
        if "price-sale-col" in precios:
            precio_con_descuento = precios["price-sale-col"]
        elif "price-club-col" in precios:
            precio_con_descuento = precios["price-club-col"]

        informacion_del_producto = {
            "id": producto_id,
            "nombre": respuesta_json["productData"]["name"],
            "precio_pleno": precio_pleno,
            "precio_con_descuento": precio_con_descuento
        }

        return informacion_del_producto