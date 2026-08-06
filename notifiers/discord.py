import requests

from config import DISCORD_WEBHOOK
from config import JUMBO_DISCORD_WEBHOOK
from config import CRUZVERDE_DISCORD_WEBHOOK
from config import FARMATODO_DISCORD_WEBHOOK
from config import MAKRO_DISCORD_WEBHOOK
from config import LAREBAJA_DISCORD_WEBHOOK
from config import ERRORS_DISCORD_WEBHOOK

def enviar_mensaje_canal_olimpica(texto):

    requests.post(
        DISCORD_WEBHOOK,
        json={
            "content": texto
        }
    )

def enviar_mensaje_canal_jumbo(texto):

    requests.post(
        JUMBO_DISCORD_WEBHOOK,
        json={
            "content": texto
        }
    )

def enviar_mensaje_canal_cruzverde(texto):

    requests.post(
        CRUZVERDE_DISCORD_WEBHOOK,
        json={
            "content": texto
        }
    )

def enviar_mensaje_canal_farmatodo(texto):

    requests.post(
        FARMATODO_DISCORD_WEBHOOK,
        json={
            "content": texto
        }
    )

def enviar_mensaje_canal_makro(texto):

    requests.post(
        MAKRO_DISCORD_WEBHOOK,
        json={
            "content": texto
        }
    )

def enviar_mensaje_canal_larebaja(texto):

    requests.post(
        LAREBAJA_DISCORD_WEBHOOK,
        json={
            "content": texto
        }
    )

def enviar_mensaje_canal_errores(texto):

    requests.post(
        ERRORS_DISCORD_WEBHOOK,
        json={
            "content": texto
        }
    )